import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import APIRouter
from urllib.parse import unquote

from services.user_service import (
    get_user_by_token,
    list_users,
    create_user_value,
    update_user_value,
    delete_user_value
)

from graphql.models import UserValueModelGraphQl, UserValueInput

# --- Query ---
@strawberry.type
class Query:

    @strawberry.field
    async def user_value(self, email: str) -> UserValueModelGraphQl | None:
        data = await get_user_by_email(email)
        return UserValueModelGraphQl(**data.dict()) if data else None

    @strawberry.field
    async def users_value_limit(self, limit: int = 10) -> list[UserValueModelGraphQl]:
        data = await list_users(limit)
        return [UserValueModelGraphQl(**u.dict()) for u in data]

# --- Mutation ---
@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_user_value(self, input: UserValueInput) -> UserValueModelGraphQl:
        data = await create_user_value(input.__dict__)
        return UserValueModelGraphQl(**data.dict())

    @strawberry.mutation
    async def update_user_value(self, email: str, input: UserValueInput) -> UserValueModelGraphQl | None:
        data = await update_user_value(id, input.__dict__)
        return UserValueModelGraphQl(**data.dict()) if data else None

    @strawberry.mutation
    async def delete_user_value(self, email: str) -> bool:
        return await delete_user_value(email)

# --- Schema ---
schema = strawberry.Schema(query=Query, mutation=Mutation)

# --- Router GraphQL ---
graphql_app = GraphQLRouter(schema)

router = APIRouter()
router.include_router(graphql_app, prefix="/graphql")
