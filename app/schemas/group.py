from typing import List, Any, Union, Optional

from datetime import datetime

from pydantic import BaseModel

from app.schemas.group_message import MessageInDB


class GroupInDB(BaseModel):
    id: int
    master_id: int

    title: str
    description: str
    created_at: datetime


class ViewGroup(GroupInDB):
    user_profiles_id: Optional[List[int]] = None
    messages: Optional[List[MessageInDB]] = None


class GroupCreate(BaseModel):
    title: str
    description: str


class GroupCreateWithMaster(BaseModel):
    title: str
    description: str
    master_id: int


class GroupUpdate(BaseModel):
    title: str
    description: str


class GroupUpdateProtected(BaseModel):
    master_id: int

    title: str
    description: str
