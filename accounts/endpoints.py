from starlette.authentication import requires
from starlette.responses import RedirectResponse

from accounts.forms import LoginForm, RegistrationForm
from accounts.tables import User, generate_jwt
from settings import BASE_HOST, templates


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


@requires("authenticated")
async def user_delete(request):
    """
    Delete user
    """
    u = User
    request_path_id = request.path_params["id"]
    if request.method == "POST":
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
