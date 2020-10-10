import cloudinary.api
import cloudinary.uploader
import cloudinary
import os

from starlette.authentication import requires
from starlette.responses import RedirectResponse

from accounts.forms import LoginForm, RegistrationForm
from accounts.tables import User, generate_jwt
from ads.helpers import get_ads, get_reviews
from ads.tables import Ad, Image, Notification, Rent, Review
from settings import (
    BASE_HOST,
    templates,
    # CLOUDINARY_API_KEY,
    # CLOUDINARY_API_SECRET,
)
from utils import pagination


async def register(request):
    """
    Validate form, register and authenticate user
    """
    data = await request.form()
    form = RegistrationForm(data)
    username = form.username.data
    email = form.email.data
    password = form.password.data
    if request.method == "POST" and form.validate():
        if (
            await User.exists().where(User.email == email).run()
            or await User.exists().where(User.username == username).run()
        ):
            user_error = "User with that email or username already exists."
            return templates.TemplateResponse(
                "accounts/register.html",
                {
                    "request": request,
                    "form": form,
                    "user_error": user_error,
                },
            )
        query = User(
            username=username,
            email=email,
            password=password,
        )
        await query.save().run()
        results = await (
            User.select()
            .columns(User.id, User.username, User.password)
            .where((User.username == username))
            .first()
        ).run()
        valid_user = await User.login(username=username, password=password)
        if not valid_user:
            user_error = "Invalid username or password"
            return templates.TemplateResponse(
                "accounts/login.html",
                {
                    "request": request,
                    "form": form,
                    "user_error": user_error,
                },
            )
        response = RedirectResponse(BASE_HOST, status_code=302)
        response.set_cookie(
            "jwt", generate_jwt(results["username"]), httponly=True
        )
        return response
    return templates.TemplateResponse(
        "accounts/register.html", {"request": request, "form": form}
    )


async def login(request):
    """
    Validate form, login and authenticate user
    """
    path = request.query_params["next"]
    data = await request.form()
    form = LoginForm(data)
    username = form.username.data
    password = form.password.data
    if request.method == "POST" and form.validate():
        if await User.exists().where(User.username == username).run():
            results = await (
                User.select()
                .columns(User.id, User.username, User.password)
                .where((User.username == username))
                .first()
            ).run()
            valid_user = await User.login(username=username, password=password)
            if not valid_user:
                user_error = "Invalid username or password"
                return templates.TemplateResponse(
                    "accounts/login.html",
                    {
                        "request": request,
                        "form": form,
                        "user_error": user_error,
                    },
                )
            response = RedirectResponse(BASE_HOST + path, status_code=302)
            response.set_cookie(
                "jwt", generate_jwt(results["username"]), httponly=True
            )
            return response
        else:
            user_error = "Please register you don't have account"
            return templates.TemplateResponse(
                "accounts/login.html",
                {
                    "request": request,
                    "form": form,
                    "user_error": user_error,
                },
            )

    return templates.TemplateResponse(
        "accounts/login.html", {"request": request, "form": form}
    )


@requires("authenticated", redirect="index")
async def profile(request):
    """
    User profile page
    """
    a = Ad
    r = Review
    u = User
    n = Notification
    auth_user = request.user.display_name
    results = await u.select().where(u.username == auth_user).run()
    ads_count = await a.count().where(a.ad_user.username == auth_user).run()
    reviews_count = (
        await r.count().where(r.review_user.username == auth_user).run()
    )
    # all user notification
    notifications_count = (
        await n.count().where(n.recipient.username == auth_user).run()
    )
    # user unread notifications profile
    unread_notifications_count = (
        await n.count()
        .where((n.is_read == False) & (n.recipient.username == auth_user))
        .run()
    )
    return templates.TemplateResponse(
        "accounts/profile.html",
        {
            "request": request,
            "results": results,
            "auth_user": auth_user,
            "ads_count": ads_count,
            "reviews_count": reviews_count,
            "notifications_count": notifications_count,
            "unread_notifications_count": unread_notifications_count,
        },
    )


@requires("authenticated", redirect="index")
async def profile_rented_from_user(request):
    auth_user = request.user.display_name
    rented_from_me = await Rent.raw(
        f"SELECT ad.title, rent.start_date, rent.end_date, "
        f"(SELECT username from piccolo_user WHERE ad.ad_user = piccolo_user.id) as owner, "
        f"(SELECT username from piccolo_user WHERE rent.client = piccolo_user.id) as usr "
        f"FROM ad JOIN rent ON ad.id = rent.ad_rent JOIN piccolo_user ON piccolo_user.id = ad.ad_user "
        f"WHERE piccolo_user.username = '{auth_user}';"
    ).run()
    return templates.TemplateResponse(
        "accounts/rent_by_user.html",
        {
            "request": request,
            "rented_from_me": rented_from_me,
        },
    )


@requires("authenticated", redirect="index")
async def profile_rented_by_user(request):
    u = User
    session_user = (
        await u.select(u.id, u.username)
        .where(u.username == request.user.username)
        .first()
        .run()
    )
    rented_by_me = await Rent.raw(
        f"SELECT ad.title, rent.start_date, rent.end_date, "
        f"(SELECT username from piccolo_user WHERE ad.ad_user = piccolo_user.id) as owner, "
        f"(SELECT username from piccolo_user WHERE rent.client = piccolo_user.id) as usr FROM ad "
        f"JOIN rent ON ad.id = rent.ad_rent JOIN piccolo_user ON piccolo_user.id = ad.ad_user "
        f"WHERE rent.client = {session_user['id']};"
    ).run()
    return templates.TemplateResponse(
        "accounts/rent_from_user.html",
        {
            "request": request,
            "rented_by_me": rented_by_me,
        },
    )


@requires("authenticated", redirect="index")
async def profile_ads(request):
    a = Ad
    auth_user = request.user.display_name
    page_query = pagination.get_page_number(url=request.url)
    count = await a.count().where(a.ad_user.username == auth_user).run()
    paginator = pagination.Pagination(page_query, count)
    ads = (
        await get_ads()
        .where(a.ad_user.username == auth_user)
        .limit(paginator.page_size)
        .offset(paginator.offset())
        .run()
    )
    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "accounts/profile_ads.html",
        {
            "request": request,
            "ads": ads,
            "page_controls": page_controls,
        },
    )


@requires("authenticated", redirect="index")
async def profile_reviews(request):
    r = Review
    auth_user = request.user.display_name
    page_query = pagination.get_page_number(url=request.url)
    count = await r.count().where(r.review_user.username == auth_user).run()
    paginator = pagination.Pagination(page_query, count)
    reviews = (
        await get_reviews()
        .where(r.review_user.username == auth_user)
        .limit(paginator.page_size)
        .offset(paginator.offset())
        .run()
    )
    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "accounts/profile_reviews.html",
        {
            "request": request,
            "reviews": reviews,
            "page_controls": page_controls,
        },
    )


@requires("authenticated", redirect="index")
async def profile_notifications(request):
    n = Notification
    auth_user = request.user.display_name
    page_query = pagination.get_page_number(url=request.url)
    count = await n.count().where(n.recipient.username == auth_user).run()
    paginator = pagination.Pagination(page_query, count)
    notifications = (
        await n.select(
            n.id, n.message, n.created, n.is_read, n.sender.username
        )
        .where(n.recipient.username == auth_user)
        .limit(paginator.page_size)
        .offset(paginator.offset())
        .run()
    )
    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "accounts/profile_notifications.html",
        {
            "request": request,
            "notifications": notifications,
            "page_controls": page_controls,
        },
    )


@requires("authenticated", redirect="index")
async def read_notification(request):
    n = Notification
    request_path_id = request.path_params["id"]
    if request.method == "POST":
        await n.update({n.is_read: True}).where(
            n.id == int(request_path_id)
        ).run()
        return RedirectResponse(url="/accounts/profile", status_code=302)


@requires("authenticated")
async def user_delete(request):
    """
    Delete user
    """
    u = User
    i = Image
    request_path_id = int(request.path_params["id"])
    if request.method == "POST":
        result = await i.raw(
            f"SELECT path FROM image "
            f"JOIN ad on ad.id = image.ad_image "
            f"JOIN piccolo_user on piccolo_user.id = ad.ad_user "
            f"WHERE piccolo_user.id = {request_path_id}"
        ).run()
        image_list = []
        for img in result:
            for k, v in img.items():
                image_list.append(v)
        # Cloudinary image deletion when user account is deleted
        # cloudinary.config(
        #     cloud_name="rkl",
        #     api_key=CLOUDINARY_API_KEY,
        #     api_secret=CLOUDINARY_API_SECRET
        #    )
        # if image_list:
        #     public_ids = [img.split('/')[-1].split('.')[0] for img in image_list]
        #     cloudinary.api.delete_resources(public_ids)
        # Dropzone image deletion when user account is deleted
        if image_list:
            for img in image_list:
                os.remove(img)
        await u.delete().where(u.id == request_path_id).run()
        request.session.clear()
        response = RedirectResponse("/", status_code=302)
        response.delete_cookie("jwt")
        return response


async def logout(request):
    """
    Logout user
    """
    request.session.clear()
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("jwt")
    return response
