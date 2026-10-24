from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    login: str
    password: str

class UserCreate(BaseModel):
    login: str
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    login: str
    role: str

    class Config:
        from_attributes = True

class IncidentCreate(BaseModel):
    equipment_id: int
    reported_id: int
    description: str

class IncidentResponse(BaseModel):
    id: int
    description: str
    status: str
    equipment_name: Optional[str] = None
    station_name: Optional[str] = None
    reporter: Optional[str] = None

    class Config:
        from_attributes = True

class StationResponse(BaseModel):
    id: int
    name: str
    depth: int
    line_name: str

    class Config:
        from_attributes = True

class TrainResponse(BaseModel):
    id: int
    number: str
    model: str
    status: str
    line_name: str

    class Config:
        from_attributes = True