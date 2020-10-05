import jwt
from piccolo.apps.user.tables import BaseUser
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      AuthenticationError, SimpleUser)

from settings import SECRET_KEY


class User(BaseUser, tablename="piccolo_user"):
    pass


class UserAuthentication(AuthenticationBackend):
    async def authenticate(self, request):
        jwt_cookie = request.cookies.get("jwt")
        if jwt_cookie:
            try:
                payload = jwt.decode(
                    jwt_cookie.encode("utf8"),
                    str(SECRET_KEY),
                    algorithms=["HS256"],
                )
                return (
                    AuthCredentials(["authenticated"]),
                    SimpleUser(payload["user_id"]),
                )
            except AuthenticationError:
                raise AuthenticationError("Invalid auth credentials")
        else:
            # unauthenticated
            return


def generate_jwt(user_id):
    payload = {"user_id": user_id}
    token = jwt.encode(payload, str(SECRET_KEY), algorithm="HS256").decode(
        "utf-8"
    )
    return token
