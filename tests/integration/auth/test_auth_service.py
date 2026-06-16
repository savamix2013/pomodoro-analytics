import pytest
from sqlalchemy import select, insert

from app.users.user_profile.models import UserProfile

pytestmark = pytest.mark.asyncio


async def test_base_login__success(auth_service, get_db_session):
    username = "test_username"
    password = "test_password"

    async with get_db_session as session:
        await session.execute(
            insert(UserProfile).values(
                username=username,
                password=password
            )
        )
        await session.commit()

    user_data = await auth_service.login(username=username, password=password)

    async with get_db_session as session:
        login_user = (
            await session.execute(
                select(UserProfile).where(UserProfile.username == username)
            )
        ).scalar_one_or_none()

    assert login_user is not None
    assert user_data.user_id == login_user.id