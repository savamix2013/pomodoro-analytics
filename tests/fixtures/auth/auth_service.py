import pytest
import pytest_asyncio

from app.settings import Settings
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest_asyncio.fixture
async def auth_service(get_db_session):
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
        google_client=None,
        mail_client=None,
    )


@pytest.fixture
def mock_auth_service(user_repository, settings):
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=None,
        mail_client=None,
    )