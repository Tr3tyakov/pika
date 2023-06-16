from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import PORT, USER_NAME, DB_NAME, HOST, PASSWORD
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base(metadata=MetaData())
