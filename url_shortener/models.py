import typing as t

from pydantic import BaseModel
from fastapi import Query

from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator


class Url(models.Model):
    long_url = fields.TextField()
    custom_url = fields.TextField()
    
    class PydanticMeta: ...
    

UrlIn = pydantic_model_creator(Url, name="UrlIn")


# class UrlIn(BaseModel):
#     long_url: str
#     custom_url: t.Annotated[str | None, Query(max_length=6)] = None


class UrlOut(BaseModel):
    url: str
