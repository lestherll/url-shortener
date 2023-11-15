import typing as t

from pydantic import BaseModel
from fastapi import Query



class UrlIn(BaseModel):
    long_url: str
    custom_url: t.Annotated[str | None, Query(max_length=6)] = None


class UrlOut(BaseModel):
    url: str
