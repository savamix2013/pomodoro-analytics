import datetime
from dataclasses import dataclass
from datetime import datetime as dt, timedelta

from jose import jwt, JWTError

from app.exception import (
    UserNotFoundException,
    UserNotCorrectPasswordException,
    TokenExpired,
    TokenNotCorrect,
)
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.schema import UserLoginSchema
from app.users.auth.client import GoogleClient, MailClient
from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    mail_client: MailClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)

        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: str):
        payload = {
            "user_id": user_id,
            "expire": (
                dt.now(tz=datetime.UTC) + timedelta(days=7)
            ).timestamp(),
        }

        encoded_jwt = jwt.encode(
            payload,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM,
        )
        return encoded_jwt

    def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM],
            )
        except JWTError:
            raise TokenNotCorrect

        if payload["expire"] < dt.utcnow().timestamp():
            raise TokenExpired

        return payload["user_id"]