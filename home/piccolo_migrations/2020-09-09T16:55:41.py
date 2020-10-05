from piccolo.apps.migrations.auto import MigrationManager

ID = "2020-09-09T16:55:41"
VERSION = "0.12.6"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="home")

    manager.add_table("Task", tablename="task")

    manager.add_column(
        table_class_name="Task",
        tablename="task",
        column_name="name",
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
        table_class_name="Task",
        tablename="task",
        column_name="completed",
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

    return manager
