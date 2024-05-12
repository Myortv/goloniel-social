from typing import Optional

from pydantic import BaseModel


class MasterInDB(BaseModel):
    id: int
    user_id: int
    is_approved: Optional[bool] = False

    title: str
    description: Optional[str] = None
    cover_picture: Optional[str] = None
    # link to discord picture


class ViewMaster(MasterInDB):
    rating: Optional[float] = 0
    approvals_amount: Optional[int] = 0


class MasterUpdateProtected(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_picture: Optional[str] = None


class MasterUpdate(BaseModel):
    user_id: int
    is_approved: Optional[bool] = False

    title: Optional[str] = None
    description: Optional[str] = None
    cover_picture: Optional[str] = None


class MasterCreate(BaseModel):
    user_id: int
    is_approved: Optional[bool] = False

    title: str
    description: Optional[str] = None
    cover_picture: Optional[str] = None


class MasterCreateProtected(BaseModel):
    title: str


class MasterCreateWithMaster(BaseModel):
    title: str
    user_id: int
