# model.py ထဲတွင် သွားရောက်ဖြည့်စွက်ရန်

from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="Email")
    password: str = Field(..., description="password")