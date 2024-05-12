from typing import List, Any, Union, Optional

from datetime import datetime

from pydantic import BaseModel


class MessageInDB(BaseModel):
    id: int
    squad_id: int
    owner_id: int
    created_at: datetime

    body: str
