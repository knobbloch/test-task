from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class EmptyResponse(BaseModel):
    ...


class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone_numbers: Optional[List[str]]
    building_id: int


class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: Optional[int] = None