from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependecy import get_auth_service
from app.exception import UserNotFoundException, UserNotCorrectPasswordException
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.login(body.username, body.password)

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)

    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)