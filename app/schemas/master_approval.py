from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class ApprovalInDB(BaseModel):
    user_profile_id: int
    master_id: int
    created_at: datetime


class ApprovalRequestInDB(BaseModel):
    master_id: int
    state: Optional[str]
    reason: Optional[str]
    created_at: datetime


class ApprovalRequestUpdateByAdmin(BaseModel):
    state: Optional[str]
    reason: Optional[str]
