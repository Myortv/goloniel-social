from typing import List, Any, Union, Optional

from datetime import datetime

from pydantic import BaseModel


class LnkGroupUserInDB(BaseModel):
    user_profile_id: int
    group_id: int
    created_at: datetime


class LnkGroupUserCreate(BaseModel):
    user_profile_id: int
    group_id: int


class GroupMembershipRequestInDB(BaseModel):
    id: int
    user_profile_id: int
    group_id: int
    state: Optional[str] = None
    is_accepted: bool
    created_at: datetime


class GroupMembershipRequestCreate(BaseModel):
    user_profile_id: int
    group_id: int


class GroupMembershipRequestUpdate(BaseModel):
    state: str
    is_accepted: Optional[bool] = False


# class GroupMembershipRequestCreate(BaseModel):
#     group_id: int

# class lnkGroupUserInDB(BaseModel):
#     user_id: int
#     group_id: int
#     created_at: datetime
