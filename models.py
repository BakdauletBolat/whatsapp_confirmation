from datetime import datetime
from typing import Optional, Any

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class AccountBase(SQLModel):
    secret: str = Field()


class AccountLimit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: Optional[int] = Field(default=None, primary_key=True, foreign_key='account.id')
    limit_of_message: int = Field(default=10)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parameters: dict[str, Any] = Field(sa_column=Column(JSON), default_factory=dict)
    template: str = Field(default='confirm')
    created_at: Optional[datetime] = Field(default=None, nullable=True)
    account_id: Optional[int] = Field(default=None, primary_key=True, foreign_key='account.id')


class Account(AccountBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
