from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(UserLogin):
    name: str
    email: str
    mobile: int
    cwid: str
    password: str

class RegisterOut(BaseModel):
    message: str

class RolesOut(BaseModel):
    roles: list[str]

class PlanItem(BaseModel):
    plan: str
    role: str
    editable: bool
    opening_date: Optional[date]
    closing_date: Optional[date]

class PlanResponse(BaseModel):
    plan: Dict[str, List[PlanItem]]

class LoginOut(BaseModel):
    accessToken: str
    refreshToken: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JWTUserDetails(BaseModel):
    name: str
    cwid: str

class PlanItems(BaseModel):
    plan: str
    id: int

class AllPlansOut(BaseModel):
    plans: List[PlanItems]
