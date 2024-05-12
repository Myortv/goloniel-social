import re

from typing import Optional, List

from pydantic import BaseModel, validator, SecretStr

from datetime import datetime

from app.core.configs import settings


# from app.utils.password import hash_password


class UserProfileInDB(BaseModel):
    id: int


class UserProfileCreate(BaseModel):
    id: int


class ViewProfile(BaseModel):
    user_id: int
    # master_id: Optional[int] = None


class Profile(ViewProfile):
    # exp: datetime
    role: Optional[str] = None

    @property
    def is_admin(self) -> bool:
        return self.role in settings.ADMIN_ROLES
