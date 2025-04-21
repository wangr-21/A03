import base64

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, field_validator

from ..services import fleep
from .auth import CurrentUser

router = APIRouter(prefix="/user", tags=["user"])


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str

    name: str
    title: str | None = None
    department: str | None = None
    avatar: str | None = None
    role: str = "teacher"

    @field_validator("avatar", mode="before")
    @classmethod
    def validate_avatar(cls, v: bytes | None) -> str | None:
        if v is None or (info := fleep.get(v[:256])) is None:
            return None

        return f"data:{info.mime[0]};base64,{base64.b64encode(v).decode()}"


@router.get("/current", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser):
    """获取当前用户信息"""
    return current_user
