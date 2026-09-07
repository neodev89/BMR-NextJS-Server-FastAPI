from models.user import UserModel
import uuid

async def get_user_by_id(user_id: uuid.UUID) -> UserModel | None:
    # esempio: chiamata al DB
    return await UserModel.get(user_id)

async def list_users(limit: int = 10) -> list[UserModel]:
    return await UserModel.all().limit(limit)

async def create_user_value(data: dict) -> UserValueModel:
    # esempio: salva nel DB
    new_user = UserValueModel(
        id=0,  # il DB genererà l'ID
        created_at=datetime.utcnow(),
        **data
    )
    return await new_user.save()

async def update_user_value(user_id: int, data: dict) -> UserValueModel | None:
    user = await UserValueModel.get(user_id)
    if not user:
        return None

    for key, value in data.items():
        setattr(user, key, value)

    return await user.save()

async def delete_user_value(user_id: int) -> bool:
    user = await UserValueModel.get(user_id)
    if not user:
        return False

    await user.delete()
    return True