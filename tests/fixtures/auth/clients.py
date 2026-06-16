import pytest
from dataclasses import dataclass

from app.settings import Settings


@dataclass
class FakeUserRepository:
    users: dict

    def __init__(self):
        self.users = {}

    async def get_user_by_username(self, username: str):
        return self.users.get(username)

    async def get_user_by_email(self, email: str):
        for user in self.users.values():
            if getattr(user, "email", None) == email:
                return user
        return None

    async def create_user(self, user_data):
        user_id = len(self.users) + 1

        user = type("User", (), {
            "id": user_id,
            "username": getattr(user_data, "username", None),
            "email": user_data.email,
            "password": getattr(user_data, "password", None),
            "name": getattr(user_data, "name", None),
        })()

        self.users[user_id] = user
        return user


@pytest.fixture
def user_repository():
    return FakeUserRepository()


@pytest.fixture
def settings():
    return Settings()