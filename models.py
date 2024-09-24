from pydantic import BaseModel, Field, EmailStr
from typing import Any, Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, field: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except Exception:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        schema = handler(schema)
        schema.update(type="string")
        return schema


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    last_name: str
    user_name: str
    age: int
    sex: str
    training_level: str
    disc_or_dise: str
    email: EmailStr
    password: Optional[str] = None
    hashed_password: Optional[str] = None

    class Config:
        
        json_encoders = {ObjectId: str}
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True


class UpdateUserModel(BaseModel):

    name: Optional[str] = None
    last_name: Optional[str] = None
    user_name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    training_level: Optional[str] = None
    disc_or_dise: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    
