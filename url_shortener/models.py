import typing as t
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    long_url: Mapped[t.Optional[str]] = mapped_column(String(100), unique=True)
    short_url: Mapped[t.Optional[str]] = mapped_column(String(20), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())


class UrlIn(BaseModel):
    long_url: str
    short_url: str | None = None


class UrlOut(UrlIn):
    short_url: str
    created_at: datetime
    model_config = {
        "from_attributes": True,
    }
