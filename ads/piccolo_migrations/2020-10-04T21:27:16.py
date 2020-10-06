from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.table import Table


class Ad(Table, tablename="ad"):
    pass


class User(Table, tablename="piccolo_user"):
    pass


ID = "2020-10-04T21:27:16"
VERSION = "0.13.4"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="ads")

    manager.add_table("Rent", tablename="rent")

    manager.add_table("Image", tablename="image")

    manager.add_table("Review", tablename="review")

    manager.add_table("Notification", tablename="notification")

    manager.add_column(
        table_class_name="Rent",
        tablename="rent",
        column_name="start_date",
        column_class_name="Timestamp",
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Rent",
        tablename="rent",
        column_name="end_date",
        column_class_name="Timestamp",
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Rent",
        tablename="rent",
        column_name="client",
        column_class_name="ForeignKey",
        params={
            "references": User,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Rent",
        tablename="rent",
        column_name="ad_rent",
        column_class_name="ForeignKey",
        params={
            "references": Ad,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Image",
        tablename="image",
        column_name="path",
        column_class_name="Varchar",
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Image",
        tablename="image",
        column_name="ad_image",
        column_class_name="ForeignKey",
        params={
            "references": Ad,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="content",
        column_class_name="Text",
        params={
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="created",
        column_class_name="Timestamp",
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="review_grade",
        column_class_name="Integer",
        params={
            "default": 0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="review_user",
        column_class_name="ForeignKey",
        params={
            "references": User,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="ad",
        column_class_name="ForeignKey",
        params={
            "references": Ad,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Notification",
        tablename="notification",
        column_name="message",
        column_class_name="Varchar",
        params={
            "length": 150,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Notification",
        tablename="notification",
        column_name="created",
        column_class_name="Timestamp",
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Notification",
        tablename="notification",
        column_name="is_read",
        column_class_name="Boolean",
        params={
            "default": False,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Notification",
        tablename="notification",
        column_name="sender",
        column_class_name="ForeignKey",
        params={
            "references": User,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Notification",
        tablename="notification",
        column_name="recipient",
        column_class_name="ForeignKey",
        params={
            "references": User,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    return manager
