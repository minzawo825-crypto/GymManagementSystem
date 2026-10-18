# members/model.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class MultiSearchModel(BaseModel):
    syskey: str
    # name: Optional[str] = None
class MemberCreateRequest(BaseModel):
    # Personal Info
    t1: str = Field(..., description="Full Name of the member")
    t2: str = Field(..., description="Unique Username")
    t3: str = Field(..., description="Password for member login")
    t4: str = Field(..., description="Male / Female / Other")
    t5: date = Field(..., description="Date of Registration")
    t6: str = Field(..., description="e.g., One Month, Three Months, etc.")
    
    # Contact Details
    t7: str = Field(..., description="Phone number format (999) 999-999-999")
    t8: str = Field(..., description="Living Address")
    
    # Service Details
    t9: str = Field(..., description="Selected Service (e.g., Fitness, Sauna, Cardio)")
    t10: float = Field(..., description="Total Paid Amount")
    n1: int = 1  # status (1=active, 4=deleted) n1: int = 1  # status (1=active, 4=deleted)



class MemberEntryList(BaseModel):
    cur_page: int = 1
    page_size: int = 25
   
    t1: Optional[str] = None #fullname
    t2: Optional[str] = None #username
    t3: Optional[str] = None    #gender
    t4: Optional[str] = None  #plan
    t5: Optional[str] = None   #contact
    t6: Optional[str] = None #address
    t7: Optional[str] = None #service
    t8: Optional[float] = None  #amount
    n1: int = 1  # status (1=active, 4=deleted)
class MemberRemoveRequest(BaseModel):
    syskey: str

class MemberDetailRequest(BaseModel):
    syskey: str

class MemberUpdateRequest(BaseModel):
    syskey: Optional[str] = None
    t1: str
    t2: str
    t3: Optional[str] = None
    t4: str
    t5: str
    t6: str
    t7: str
    t8: str
    t9: str
    t10: float
    n1: int = 1  # status (1=active, 4=deleted)

class MemberGetRequest(BaseModel):
    syskey: str    