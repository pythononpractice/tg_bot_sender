from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User


async def get_active_users(session: AsyncSession):
    users = await session.execute(
        select(User.telegram_id).filter(User.is_active)
    )
    return users.scalars().all()


async def add_user(session: AsyncSession, telegram_id: str, username: str, first_name: str, last_name: str):
    is_exists = await session.execute(select(User.id).filter(User.telegram_id == telegram_id))
    is_exists = is_exists.scalar()
    if is_exists:
        return False

    user = User(
        telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name
    )
    session.add(user)
    await session.commit()
    return user


async def change_active(session: AsyncSession, user_id: str, is_active: bool) -> None:
    await session.execute(update(User).filter(User.telegram_id == user_id).values(is_active=is_active))
    await session.commit()
