from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
import config


engine = create_engine(config.DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDepends = Annotated[Session, Depends(get_session)]