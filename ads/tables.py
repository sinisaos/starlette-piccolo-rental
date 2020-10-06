from piccolo.columns import (Boolean, ForeignKey, Integer, Text, Timestamp,
                             Varchar)
from piccolo.columns.readable import Readable
from piccolo.table import Table

from accounts.tables import User


class Ad(Table):
    title = Varchar(length=255)
    slug = Varchar(length=255)
    content = Text()
    created = Timestamp()
    view = Integer(default=0)
    price = Integer()
    room = Integer()
    visitor = Integer()
    address = Varchar(length=255)
    city = Varchar(length=255)
    ad_user = ForeignKey(references=User)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.title])


class Review(Table):
    content = Text()
    created = Timestamp()
    review_grade = Integer()
    review_user = ForeignKey(references=User)
    ad = ForeignKey(references=Ad)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.ad])


class Image(Table):
    path = Varchar(length=255)
    ad_image = ForeignKey(references=Ad)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.path])


class Rent(Table):
    start_date = Timestamp()
    end_date = Timestamp()
    client = ForeignKey(references=User)
    ad_rent = ForeignKey(references=Ad)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.client])


class Notification(Table):
    message = Varchar(length=150)
    created = Timestamp()
    is_read = Boolean(default=False)
    sender = ForeignKey(references=User)
    recipient = ForeignKey(references=User)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.message])
