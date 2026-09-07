# qui inserire le classi per inferire le Response API
from pydantic import BaseModel, ConfigDict
from pydantic.generics import GenericModel
from typing import Optional, TypeVar, Generic, List
import uuid
from datetime import datetime

T = TypeVar("T")

class ResponseAPI(GenericModel, Generic[T]):
    success: bool
    message: str
    data: T
    status: int
    
class UserModel(BaseModel):
    id: uuid.UUID
    created_at: datetime
    user_name: str
    password: str
    name: str
    token: str
    
class UserValueModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    user_name: str
    weight: str
    height: str
    age: str
    token_user: str
    activity: str
    bmr: str
    gender: str
    order: int
    
class JoinedUserTabModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    user_value: List[UserValueModel]
    name: str  
    
class StatisticUser(BaseModel):
    token: str
    email: str
    name: str
    list_weight: List[str]
    list_height: List[str]
    list_age: List[str]
    list_activity: List[str]
    list_bmr: List[str]
    average_weight: str
    average_height: str
    average_age: str
    average_activity: str
    average_bmr: str
    creation_date: str
    list_order: List[int]