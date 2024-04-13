import os

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.exc import OperationalError
from sqlalchemy.event import listen

import geoalchemy2
# from geoalchemy2 import load_spatialite
from geoalchemy2 import load_spatialite_gpkg
from geoalchemy2.admin.dialects.geopackage import create_spatial_ref_sys_view
from geoalchemy2 import alembic_helpers

from alembic import context


from arara.model import Base
from arara.model import GpkgImpl


# from alembic.ddl.impl import DefaultImpl
#
# class GpkgImpl(DefaultImpl):
#     __dialect__ = 'geopackage'

try:
    _ = os.environ['SPATIALITE_LIBRARY_PATH']
except KeyError:
    os.environ['SPATIALITE_LIBRARY_PATH'] = 'mod_spatialite'


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=alembic_helpers.include_object,
        process_revision_directives=alembic_helpers.writer,
        render_item=alembic_helpers.render_item,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # listen(connectable, "connect", load_spatialite)
    listen(connectable, "connect", load_spatialite_gpkg)

    try:
        with connectable.connect() as conn:
            create_spatial_ref_sys_view(conn)
    except OperationalError:
        pass


    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            include_object=alembic_helpers.include_object,
            process_revision_directives=alembic_helpers.writer,
            render_item=alembic_helpers.render_item,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
