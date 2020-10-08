from starlette.routing import Route, Router

from accounts.endpoints import (login, logout, profile, profile_ads,
                                profile_notifications, profile_rented_by_user,
                                profile_rented_from_user, profile_reviews,
                                read_notification, register, user_delete)

accounts_routes = Router(
    [
        Route("/login", endpoint=login, methods=["GET", "POST"], name="login"),
        Route(
            "/register",
            endpoint=register,
            methods=["GET", "POST"],
            name="register",
        ),
        Route(
            "/logout", endpoint=logout, methods=["GET", "POST"], name="logout"
        ),
        Route("/profile", endpoint=profile, methods=["GET"], name="profile"),
        Route(
            "/profile/ads",
            endpoint=profile_ads,
            methods=["GET"],
            name="profile_ads",
        ),
        Route(
            "/profile/reviews",
            endpoint=profile_reviews,
            methods=["GET"],
            name="profile_reviews",
        ),
        Route(
            "/rent-from-user",
            endpoint=profile_rented_from_user,
            methods=["GET"],
            name="profile_rented_from_user",
        ),
        Route(
            "/rent-by-user",
            endpoint=profile_rented_by_user,
            methods=["GET"],
            name="profile_rented_by_user",
        ),
        Route(
            "/user-delete/{id:int}",
            endpoint=user_delete,
            methods=["GET", "POST"],
            name="user_delete",
        ),
        Route(
            "/profile/notifications",
            endpoint=profile_notifications,
            methods=["GET"],
            name="profile_notifications",
        ),
        Route(
            "/read/{id:int}",
            endpoint=read_notification,
            methods=["GET", "POST"],
            name="read_notification",
        ),
    ]
)
