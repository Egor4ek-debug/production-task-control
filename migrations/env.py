import asyncio
import logging
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

from db.base import Base

from models.product_model import Product
from models.batch_model import Batch
from models.work_center_model import WorkCenter

# from config import DATABASE_URL

load_dotenv()

config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

target_metadata = Base.metadata


def get_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    logger.info(f"Connecting to database at: {url}")
    return url


def run_migrations_offline():
    """Запуск оффлайн — без подключения к БД"""
    logger.info("Running migrations in OFFLINE mode.")
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        logger.info("Starting offline transaction...")
        context.run_migrations()
        logger.info("Offline migration complete.")


def run_migrations_online():
    """Асинхронный онлайн-режим миграции"""
    logger.info("Running migrations in ONLINE (async) mode.")

    async def do_run_migrations():
        logger.info("Creating async engine...")
        connectable = create_async_engine(get_url(), future=True)

        async with connectable.connect() as connection:
            logger.info("Established async DB connection.")
            await connection.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                    compare_type=True,
                    transaction_per_migration=True,
                )
            )
            logger.info("Starting online transaction and running migrations...")
            await connection.run_sync(lambda conn: context.run_migrations())
            logger.info("Online migration complete.")

    asyncio.run(do_run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
