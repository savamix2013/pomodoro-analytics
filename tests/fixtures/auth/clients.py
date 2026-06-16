import pytest
from dataclasses import dataclass

from app.settings import Settings


@dataclass
class FakeUserRepository:
    users: dict = None

    def __post_init__(self):
        self.users = {}

    async def get_user_by_username(self, username: str):
        return self.users.get(username)

    async def get_user_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    async def create_user(self, user_data):
        user_id = len(self.users) + 1
        user = type("User", (), {
            "id": user_id,
            "username": user_data.username if hasattr(user_data, "username") else None,
            "email": user_data.email,
            "password": user_data.password if hasattr(user_data, "password") else None,
        })()

        self.users[user_id] = user
        return user


@pytest.fixture
def user_repository():
    return FakeUserRepository()


@pytest.fixture
def settings():
    return Settings()