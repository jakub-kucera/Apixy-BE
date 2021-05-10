import uuid
from typing import Optional

from pydantic import UUID4, validator

from apixy.entities.shared import ForbidExtraModel


class User(ForbidExtraModel):
    id: Optional[UUID4] = None
    password: str
    superuser: Optional[bool] = False

    oauth_name: str
    token: str
    expires_at: Optional[int] = None
    refresh_token: Optional[str] = None

    @validator("id", pre=True, always=True)
    @classmethod
    def default_id(cls, val: UUID4) -> UUID4:
        return val or uuid.uuid4()

    class Config:
        orm_mode = True
