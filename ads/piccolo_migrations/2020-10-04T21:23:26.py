from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.table import Table


class User(Table, tablename="piccolo_user"):
    pass


ID = "2020-10-04T21:23:26"
VERSION = "0.13.4"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="ads")

    manager.add_table("Ad", tablename="ad")

    manager.add_column(
        table_class_name="Ad",
        tablename="ad",
        column_name="title",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="slug",
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
        table_class_name="Ad",
        tablename="ad",
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
        table_class_name="Ad",
        tablename="ad",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="view",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="price",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="room",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="visitor",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="address",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="city",
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
        table_class_name="Ad",
        tablename="ad",
        column_name="ad_user",
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
