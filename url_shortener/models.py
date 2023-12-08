import typing as t

from pydantic import BaseModel
from fastapi import Query

from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator


class Url(models.Model):
    long_url = fields.TextField()
    short_url = fields.TextField()
    custom_url = fields.CharField(max_length=6, unique=True, null=True)
    url_hash = fields.TextField()
    created_at = fields.DatetimeField()

    class PydanticMeta:
        ...


UrlIn = pydantic_model_creator(
    Url,
    name="UrlIn",
    exclude=(
        "id",
        "url_hash",
        "created_at",
        "short_url"
    ),
    optional=("custom_url",)
)

UrlOut = pydantic_model_creator(
    Url,
    name="UrlOut",
    # COMMENTED FOR DEBUGGIN PURPOSES
    # exclude=(
    #     "id",
    #     "url_hash",
    #     "created_at",
    #     "custom_url",
    # ),
)
