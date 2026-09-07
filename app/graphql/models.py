import strawberry
from datetime import datetime

@strawberry.type
class UserValueModelGraphQl:
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

@strawberry.input
class UserValueInput:
    user_name: str
    weight: str
    height: str
    age: str
    token_user: str
    activity: str
    bmr: str
    gender: str