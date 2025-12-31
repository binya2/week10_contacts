from typing import Annotated, Union, Any
from bson import ObjectId
from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema


def _parse_id(v: Any) -> Union[int, ObjectId]:
    if isinstance(v, (int, ObjectId)):
        return v

    if isinstance(v, str):
        if v.isdigit():
            return int(v)
        if ObjectId.is_valid(v):
            return ObjectId(v)
    return v


def _serialize_id(v: Any) -> Union[int, str]:
    if isinstance(v, ObjectId):
        return str(v)
    return v

def parse_resource_id(contact_id: str):
    parsed = _parse_id(contact_id)
    return parsed

AbstractID = Annotated[
    Union[int, ObjectId],
    BeforeValidator(_parse_id),
    PlainSerializer(_serialize_id),
    WithJsonSchema({"type": "string", "example": "123 OR 507f1f77bcf86cd799439011"}),
]