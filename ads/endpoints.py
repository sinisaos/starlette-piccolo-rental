# import cloudinary.uploader
# import cloudinary
import datetime
import os
import random

import aiofiles
from starlette.authentication import requires
from starlette.responses import RedirectResponse

from accounts.tables import User
from ads.forms import AdEditForm, AdForm, RentForm, ReviewEditForm, ReviewForm
from ads.helpers import count_search_ads, get_ads, get_search_ads
from ads.tables import Ad, Image, Notification, Rent, Review
from settings import BASE_HOST  # CLOUDINARY_API_KEY,; CLOUDINARY_API_SECRET,
from settings import UPLOAD_FOLDER, templates
from utils import pagination


async def ads_list(request):
    """
    All ads
    """
    a = Ad
    i = Image
    # pagination
    page_query = pagination.get_page_number(url=request.url)
    count = await a.count().run()
    paginator = pagination.Pagination(page_query, count)
    results = (
        await get_ads()
        .limit(paginator.page_size)
        .offset(paginator.offset())
        .order_by(a.id, ascending=False)
        .run()
    )
    image_results = [
        await i.select().where(i.ad_image == item["id"]).first().run()
        for item in results
    ]
    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "ads/ads_list.html",
        {
            "request": request,
            "results": zip(results, image_results),
            "page_controls": page_controls,
        },
    )


async def ad(request):
    """
    Single ad
    """
    a = Ad
    i = Image
    r = Review
    d = Rent
    request_path_id = request.path_params["id"]
    path = request.url.path
    results = await get_ads().where(a.id == request_path_id).first().run()
    # update ad views per session
    session_key = f"viewed_ad_{results['id']}"
    if not request.session.get(session_key, False):
        await a.update({a.view: a.view + 1}).where(
            a.id == int(request_path_id)
        ).run()
        request.session[session_key] = True
    image_results = (
        await i.select().where(i.ad_image == int(request_path_id)).run()
    )
    review_results = (
        await r.select(
            r.id,
            r.content,
            r.created,
            r.review_grade,
            r.review_user.username,
            r.ad.id,
        )
        .where(r.ad.id == request_path_id)
        .order_by(r.id, ascending=False)
        .run()
    )
    # if no reviews
    try:
        review_avg = sum(
            item["review_grade"] for item in review_results
        ) / len(review_results)
    except ZeroDivisionError:
        review_avg = None

    # proccesing form for booking ad
    data = await request.form()
    form = RentForm(data)
    if request.method == "POST" and form.validate():
        u = User
        session_user = (
            await u.select(u.id, u.username)
            .where(u.username == request.user.username)
            .first()
            .run()
        )
        start = form.start_date.data
        end = form.end_date.data
        try:
            between = (
                await d.select()
                .where(
                    (d.start_date <= end)
                    & (d.end_date >= start)
                    & (d.ad_rent == int(request_path_id))
                )
                .run()
            )
            now = datetime.datetime.now().date()
            diff = (now - start).total_seconds()
            if diff > 0:
                rent_error = "Both dates can't be in the past."
            days = (end - start).days
            if days < 1:
                rent_error = "The minimum rental period is one day."
            if any(between):
                rent_error = "Already rented in that time."
            rented_apartments = await a.raw(
                f"SELECT * FROM ad JOIN rent "
                f"ON ad.id = rent.ad_rent WHERE ad.id = {request_path_id}"
            ).run()
            return templates.TemplateResponse(
                "ads/ad_detail.html",
                {
                    "request": request,
                    "item": results,
                    "path": path,
                    "images": image_results,
                    "review_results": review_results,
                    "review_count": len(review_results),
                    "review_avg": review_avg,
                    "form": form,
                    "rented_apartments": rented_apartments,
                    "rent_error": rent_error,
                },
            )
        except:  # noqa
            query = Rent(
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                client=session_user["id"],
                ad_rent=results["id"],
            )
            await query.save().run()
            # notification to ad owner
            notification_query = Notification(
                message=f"{results['title']} booked by {session_user['username']}",
                created=datetime.datetime.now(),
                is_read=0,
                sender=session_user["id"],
                recipient=results["ad_user.id"],
            )
            await notification_query.save().run()
            return RedirectResponse(BASE_HOST + path, status_code=302)
    rented_apartments = await a.raw(
        f"SELECT * FROM ad JOIN rent "
        f"ON ad.id = rent.ad_rent WHERE ad.id = {request_path_id}"
    ).run()
    return templates.TemplateResponse(
        "ads/ad_detail.html",
        {
            "request": request,
            "item": results,
            "path": path,
            "images": image_results,
            "review_results": review_results,
            "review_count": len(review_results),
            "review_avg": review_avg,
            "rented_apartments": rented_apartments,
            "form": form,
        },
    )


@requires("authenticated")
async def ad_create(request):
    """
    Ad create form
    """
    u = User
    session_user = (
        await u.select(u.id, u.username)
        .where(u.username == request.user.username)
        .first()
        .run()
    )
    data = await request.form()
    form = AdForm(data)
    title = form.title.data
    if request.method == "POST" and form.validate():
        query = Ad(
            title=title,
            slug="-".join(title.lower().split()),
            content=form.content.data,
            created=datetime.datetime.now(),
            view=0,
            price=form.price.data,
            room=form.room.data,
            visitor=form.visitor.data,
            city=form.city.data,
            address=form.address.data,
            ad_user=session_user["id"],
        )
        await query.save().run()
        return RedirectResponse(url="/ads/images", status_code=302)
    return templates.TemplateResponse(
        "ads/ad_create.html", {"request": request, "form": form}
    )


@requires("authenticated")
async def ad_images(request):
    return templates.TemplateResponse(
        "ads/images.html", {"request": request, "BASE": BASE_HOST}
    )


async def write_file(path, body):
    async with aiofiles.open(path, "wb") as f:
        await f.write(body)
    f.close()


'''
@requires("authenticated")
async def upload(request):
    """
    upload images to Cloudinary because Heroku filesystem is not suitable \
    for files upload. More info on link
    https://help.heroku.com/K1PPS2WM/why-are-my-file-uploads-missing-deleted
    """
    i = Image
    a = Ad
    result = await get_ads().order_by(a.id, ascending=False).first().run()
    # last inserted ad id
    aid = result["id"]
    data = await request.form()
    # convert multidict to list of items for multifile upload
    iter_images = data.multi_items()
    num_of_images = len([i for i in iter_images if i[1] != ""])
    # list of images paths
    images = [data["images" + str(i)] for i in range(num_of_images)]
    # save images path and last inserted ad id to db
    for item in images:
        await i.raw(
            f"INSERT INTO image (path, ad_image) VALUES ('{item}', {aid});"
        ).run()
    return RedirectResponse(url="/ads/", status_code=302)
'''


@requires("authenticated")
async def upload(request):
    i = Image
    a = Ad
    result = await get_ads().order_by(a.id, ascending=False).first().run()
    # last inserted ad id
    aid = result["id"]
    data = await request.form()
    # convert multidict to list of items for multifile upload
    iter_images = data.multi_items()
    # read item and convert to bytes
    byte_images = [await item[1].read() for item in iter_images]
    list_of_paths = []
    # write bytes to file in filesystem
    # name of file with random
    for upload_file in byte_images:
        file_path = f"{UPLOAD_FOLDER}/{random.randint(100,100000)}.jpeg"
        list_of_paths.append(file_path)
        await write_file(file_path, upload_file)
    # store file paths to db and link to single ad
    for item in list_of_paths:
        await i.raw(
            f"INSERT INTO image (path, ad_image) VALUES ('{item}', {aid});"
        ).run()
    return RedirectResponse(url="/ads/", status_code=302)


@requires("authenticated")
async def ad_edit(request):
    """
    Ad edit form
    """
    a = Ad
    i = Image
    request_path_id = request.path_params["id"]
    ad = await get_ads().where(a.id == request_path_id).first().run()
    images = await i.select().where(i.ad_image == ad["id"]).run()
    data = await request.form()
    form = AdEditForm(data)
    new_form_value, form.content.data = form.content.data, ad["content"]
    title = form.title.data
    if request.method == "POST" and form.validate():
        await a.update(
            {
                a.title: title,
                a.slug: "-".join(title.lower().split()),
                a.content: new_form_value,
                a.price: form.price.data,
                a.room: form.room.data,
                a.visitor: form.visitor.data,
                a.city: form.city.data,
                a.address: form.address.data,
            }
        ).where(a.id == request_path_id).run()
        return RedirectResponse(
            url=f"/ads/image-edit/{ad['id']}", status_code=302
        )
    return templates.TemplateResponse(
        "ads/ad_edit.html",
        {
            "request": request,
            "form": form,
            "ad": ad,
            "images": images,
        },
    )


@requires("authenticated")
async def image_edit(request):
    i = Image
    aid = request.path_params["id"]
    # count remaining images
    img_count = await i.count().where(i.ad_image == int(aid)).run()
    return templates.TemplateResponse(
        "ads/image_edit.html",
        {
            "request": request,
            "BASE": BASE_HOST,
            "aid": aid,
            "img_count": img_count,
        },
    )


"""
- uncomment for Cloudinary upload

@requires("authenticated")
async def edit_upload(request):
    # edited ad id
    aid = int((request.url.path).split("/")[-1])
    img_count = await Image.all().filter(ad_image_id=aid).count()
    data = await request.form()
    # list of remaining images paths
    images = [data["images" + str(i)] for i in range(3 - img_count)]
    # save images path and last inserted ad id to db
    for item in images:
        if item:
            async with in_transaction() as conn:
                await conn.execute_query(
                    f"INSERT INTO image (path, ad_image_id) \
                        VALUES ('{item}', {aid});"
                )
    return RedirectResponse(BASE_HOST + f"/ads/edit/{aid}", status_code=302)

"""


@requires("authenticated")
async def edit_upload(request):
    if request.method == "POST":
        # edited ad id
        aid = int((request.url.path).split("/")[-1])
        data = await request.form()
        # convert multidict to list of items for multifile upload
        iter_images = data.multi_items()
        # read item and convert to bytes
        byte_images = [await item[1].read() for item in iter_images]
        list_of_paths = []
        # write bytes to file in filesystem
        # name of file with random
        for upload_file in byte_images:
            file_path = f"{UPLOAD_FOLDER}/{random.randint(100,100000)}.jpeg"
            list_of_paths.append(file_path)
            await write_file(file_path, upload_file)
        # store file paths to db and link to single ad
        for item in list_of_paths:
            await Image.raw(
                f"INSERT INTO image (path, ad_image) VALUES ('{item}', {aid});"
            ).run()
        return RedirectResponse(
            BASE_HOST + f"/ads/edit/{aid}#loaded", status_code=302
        )


@requires("authenticated")
async def image_delete(request):
    """
    Delete image on edit
    """
    i = Image
    request_path_id = request.path_params["id"]
    form = await request.form()
    aid = form["aid"]
    if request.method == "POST":
        # delete related image from filesystem
        # uncomment for Dropzone upload to filesystem
        img = (
            await i.select(i.id, i.path)
            .where(i.id == int(request_path_id))
            .first()
            .run()
        )
        os.remove(img["path"])
        # img = await Image.get(id=id)
        # delete related image
        # uncomment for Cloudinary
        # public_id = (img.path).split("/")[-1].split(".")[0]
        # cloudinary.config(
        #   cloud_name="rkl",
        #   api_key=CLOUDINARY_API_KEY,
        #   api_secret=CLOUDINARY_API_SECRET,
        # )
        # cloudinary.uploader.destroy(public_id)
        await i.delete().where(i.id == int(request_path_id)).run()
        return RedirectResponse(url=f"/ads/edit/{aid}", status_code=302)


@requires("authenticated")
async def ad_delete(request):
    """
    Delete ad
    """
    i = Image
    a = Ad
    request_path_id = request.path_params["id"]
    if request.method == "POST":
        # delete images from filesystem
        images = (
            await i.select().where(i.ad_image == int(request_path_id)).run()
        )
        for img in images:
            os.remove(img["path"])
        # delete images from Cloudinary
        # cloudinary.config(
        #   cloud_name="rkl",
        #   api_key=CLOUDINARY_API_KEY,
        #    api_secret=CLOUDINARY_API_SECRET,
        # )
        # public_ids = [
        #    (img.path).split("/")[-1].split(".")[0] for img in images
        # ]
        # cloudinary.api.delete_resources(public_ids)
        await a.delete().where(a.id == request_path_id).run()
        return RedirectResponse(url="/ads", status_code=302)


@requires("authenticated")
async def review_create(request):
    """
    Review form
    """
    request_path_id = int(request.query_params["next"].split("/")[2])
    request_query_next = request.query_params["next"]
    u = User
    session_user = (
        await u.select(u.id, u.username)
        .where(u.username == request.user.username)
        .first()
        .run()
    )
    data = await request.form()
    form = ReviewForm(data)
    if request.method == "POST" and form.validate():
        query = Review(
            content=form.content.data,
            created=datetime.datetime.now(),
            review_grade=int(form.grade.data),
            ad=request_path_id,
            review_user=session_user["id"],
        )
        await query.save().run()
        return RedirectResponse(
            BASE_HOST + request_query_next, status_code=302
        )
    return templates.TemplateResponse(
        "ads/review_create.html",
        {"request": request, "form": form, "next": request_query_next},
    )


@requires("authenticated")
async def review_edit(request):
    """
    Review edit form
    """
    r = Review
    request_path_id = request.path_params["id"]
    review = await r.select().where(r.id == request_path_id).first().run()
    data = await request.form()
    form = ReviewEditForm(data)
    new_form_value, form.content.data = form.content.data, review["content"]
    if request.method == "POST" and form.validate():
        await r.update(
            {r.content: new_form_value, r.review_grade: int(form.grade.data)}
        ).where(r.id == int(request_path_id)).run()
        return RedirectResponse(url="/ads", status_code=302)
    return templates.TemplateResponse(
        "ads/review_edit.html",
        {"request": request, "form": form, "review": review},
    )


@requires("authenticated")
async def review_delete(request):
    """
    Delete review
    """
    request_path_id = request.path_params["id"]
    if request.method == "POST":
        await Review.delete().where(Review.id == request_path_id).run()
        return RedirectResponse(url="/ads", status_code=302)


async def search(request):
    """
    Search ads
    """
    a = Ad
    i = Image
    count = await a.count().run()
    page_query = pagination.get_page_number(url=request.url)
    q = request.query_params["q"]
    count = await count_search_ads(q).run()
    paginator = pagination.Pagination(page_query, count)
    results = (
        await get_search_ads(q)
        .limit(paginator.page_size)
        .offset(paginator.offset())
        .order_by(a.id, ascending=False)
        .run()
    )
    image_results = [
        await i.select().where(i.ad_image == item["id"]).first().run()
        for item in results
    ]
    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "ads/ads_list.html",
        {
            "request": request,
            "results": zip(results, image_results),
            "page_controls": page_controls,
            "count": count,
        },
    )


async def maps(request):
    """
    Map view
    """
    city = request.path_params["city"]
    results = await Ad.select().run()
    return templates.TemplateResponse(
        "ads/map.html", {"request": request, "results": results, "city": city}
    )
