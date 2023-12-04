import re

from typing import Optional, List

from pydantic import BaseModel, validator, SecretStr

from datetime import datetime

from app.core.configs import settings


# from app.utils.password import hash_password


class UserProfileInDB(BaseModel):
    id: int
    real_id: int


class UserProfileCreate(BaseModel):
    reai_id: int


class ViewProfile(BaseModel):
    user_profile_id: int
    real_id: int
    master_id: Optional[int] = None


class Profile(ViewProfile):
    # exp: datetime
    role: str

    @property
    def is_admin(self) -> bool:
        return self.role == settings.ADMIN_ROLE_STRING
