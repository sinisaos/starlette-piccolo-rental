from .tables import Ad, Review


def get_ads():
    a = Ad
    qs = a.select(
        a.id,
        a.slug,
        a.title,
        a.content,
        a.created,
        a.view,
        a.room,
        a.visitor,
        a.price,
        a.city,
        a.address,
        a.ad_user.username,
        a.ad_user.id,
    )
    return qs


def get_reviews():
    r = Review
    qs = r.select(
        r.id,
        r.content,
        r.created,
        r.review_grade,
        r.review_user.username,
        r.ad.id,
    )
    return qs


def get_search_ads(q):
    a = Ad
    qs = a.select(
        a.id,
        a.slug,
        a.title,
        a.content,
        a.created,
        a.view,
        a.room,
        a.visitor,
        a.price,
        a.city,
        a.ad_user.username,
    ).where(
        (
            (a.title.ilike("%" + q + "%"))
            | (a.content.ilike("%" + q + "%"))
            | (a.city.ilike("%" + q + "%"))
            | (a.address.ilike("%" + q + "%"))
            | (a.ad_user.username.ilike("%" + q + "%"))
        )
    )
    return qs


def count_search_ads(q):
    a = Ad
    qs = a.count().where(
        (
            (a.title.ilike("%" + q + "%"))
            | (a.content.ilike("%" + q + "%"))
            | (a.city.ilike("%" + q + "%"))
            | (a.address.ilike("%" + q + "%"))
            | (a.ad_user.username.ilike("%" + q + "%"))
        )
    )
    return qs
