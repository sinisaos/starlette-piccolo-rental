from piccolo.engine import engine_finder
from piccolo_admin.endpoints import create_admin
from secure import SecureHeaders
from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route
from starlette.staticfiles import StaticFiles

from accounts.routes import accounts_routes
from accounts.tables import UserAuthentication
from ads.routes import ads_routes
from ads.tables import Ad, Image, Notification, Rent, Review
from home.endpoints import HomeEndpoint
from settings import SECRET_KEY, templates

# Security Headers are HTTP response headers that, when set,
# can enhance the security of your web application
# by enabling browser security policies.
# more on https://secure.readthedocs.io/en/latest/headers.html
secure_headers = SecureHeaders()

routes = [
    Route("/", HomeEndpoint, name="index"),
]

app = Starlette(debug=True, routes=routes)

app.mount(
    "/admin/",
    create_admin(tables=[Ad, Review, Image, Rent, Notification]),
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/accounts", accounts_routes)
app.mount("/ads", ads_routes)

app.add_middleware(AuthenticationMiddleware, backend=UserAuthentication())
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


# middleware for secure headers
@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.starlette(response)
    return response


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder()
    await engine.start_connnection_pool()


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connnection_pool()
