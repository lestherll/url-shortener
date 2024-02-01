import typing as t
from datetime import datetime

from pydantic import BaseModel, field_validator
from sqlalchemy import DateTime, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    long_url: Mapped[str] = mapped_column(String(100), unique=True)
    short_url: Mapped[t.Optional[str]] = mapped_column(String(20), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())


class UrlIn(BaseModel):
    long_url: str
    short_url: str | None = None

    @field_validator("short_url")
    @classmethod
    def short_url_must_not_be_empty_or_contain_whitespace(
        cls, v: str | None
    ) -> str | None:
        if isinstance(v, str):
            if v == "" or " " in v:
                raise ValueError("short_url must not be empty or contain whitespace")
        return v


class UrlOut(UrlIn):
    short_url: str
    created_at: datetime
    model_config = {
        "from_attributes": True,
    }
