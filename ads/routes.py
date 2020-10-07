from starlette.routing import Route, Router

from ads.endpoints import (ad, ad_create, ad_delete, ad_edit, ad_images,
                           ads_list, edit_upload, filter_search, image_delete,
                           image_edit, maps, review_create, review_delete,
                           review_edit, search, upload)

ads_routes = Router(
    [
        Route(
            "/", endpoint=ads_list, methods=["GET", "POST"], name="ads_list"
        ),
        Route(
            "/{id:int}/{slug:str}",
            endpoint=ad,
            methods=["GET", "POST"],
            name="ad",
        ),
        Route(
            "/create",
            endpoint=ad_create,
            methods=["GET", "POST"],
            name="ad_create",
        ),
        Route(
            "/edit/{id:int}",
            endpoint=ad_edit,
            methods=["GET", "POST"],
            name="ad_edit",
        ),
        Route(
            "/delete/{id:int}",
            endpoint=ad_delete,
            methods=["GET", "POST"],
            name="ad_delete",
        ),
        Route(
            "/images",
            endpoint=ad_images,
            methods=["GET", "POST"],
            name="ad_images",
        ),
        Route("/upload", endpoint=upload, methods=["POST"], name="upload"),
        Route(
            "/image-edit/{id:int}",
            endpoint=image_edit,
            methods=["GET", "POST"],
            name="image_edit",
        ),
        Route(
            "/edit-upload/{aid:int}",
            endpoint=edit_upload,
            methods=["POST"],
            name="edit_upload",
        ),
        Route(
            "/image-delete/{id:int}",
            endpoint=image_delete,
            methods=["POST"],
            name="image_delete",
        ),
        Route(
            "/review-create",
            endpoint=review_create,
            methods=["GET", "POST"],
            name="review_create",
        ),
        Route(
            "/review-edit/{id:int}",
            endpoint=review_edit,
            methods=["GET", "POST"],
            name="review_edit",
        ),
        Route(
            "/review-delete/{id:int}",
            endpoint=review_delete,
            methods=["GET", "POST"],
            name="review_delete",
        ),
        Route("/search", endpoint=search, methods=["GET"], name="search"),
        Route(
            "/filter-search",
            endpoint=filter_search,
            methods=["GET"],
            name="filter_search",
        ),
        Route("/map/{city:str}", endpoint=maps, methods=["GET"], name="maps"),
    ]
)
