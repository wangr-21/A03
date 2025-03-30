import asyncio
import os
from typing import Annotated

import sqlalchemy.ext.asyncio as sa_async
from fastapi import Depends
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base

_engine: AsyncEngine
_session_factory: sa_async.async_sessionmaker[sa_async.AsyncSession]
Base: type[DeclarativeBase] = declarative_base()


async def get_session():
    session = _session_factory()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()


DBSession = Annotated[sa_async.AsyncSession, Depends(get_session)]


# 数据库驱动配置
# 参考 pyproject.toml 的可选依赖
_DB_DRIVER = {
    "sqlite": "aiosqlite",
    "mysql": "aiomysql",
    "postgresql": "asyncpg",
}


def _init_orm() -> None:
    global _engine, _session_factory

    url = make_url(os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/db.sqlite3"))
    if (backend := url.get_backend_name()) not in _DB_DRIVER:
        raise ValueError(f"不支持的数据库后端: {backend!r}")
    if driver := (url.get_driver_name()) != _DB_DRIVER[backend]:
        raise ValueError(f"不支持的数据库驱动: {driver!r}")

    # 根据数据库类型选择不同的配置
    if backend == "sqlite":
        # SQLite 配置
        _engine = create_async_engine(
            url,
            future=True,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true",
        )
    else:
        # 其他数据库配置（如 MySQL、PostgreSQL 等）
        _engine = create_async_engine(
            url,
            future=True,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true",
        )

    _session_factory = sa_async.async_sessionmaker(_engine)

    async def create_all_tables():
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.get_event_loop().create_task(create_all_tables())


_init_orm()
