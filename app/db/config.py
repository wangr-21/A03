import asyncio
import os
from typing import Annotated

import sqlalchemy.ext.asyncio as sa_async
from fastapi import Depends
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


def _init_orm():
    global _engine, _session_factory

    url = os.getenv("DATABASE_URL") or "sqlite+aiosqlite:///data/db.sqlite"

    _engine = create_async_engine(
        url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        # 调试模式下打印SQL语句
        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    )
    _session_factory = sa_async.async_sessionmaker(_engine)

    async def create_all_tables():
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.get_event_loop().create_task(create_all_tables())


_init_orm()
