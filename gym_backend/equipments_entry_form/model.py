# members/model.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from typing import Union, List
class MultiSearchModel(BaseModel):
    syskey: str
    # name: Optional[str] = None
class EquipmentCreateRequest(BaseModel):
    t1: str = Field(..., description="Equipment Name")
    t2: str = Field(..., description="Description")
    t3: str = Field(..., description="Date of purchase as string (YYYY-MM-DD)") # 👈 Change from date to str
    t4: str = Field(..., description="Quantity")
    t5: str = Field(..., description="Vendor")
    t6: str = Field(..., description="Address")
    t7: str = Field(..., description="Contact Number")
    t8: float = Field(..., description="Cost per item")
    n1: int = 1


class EquipmentEntryList(BaseModel):
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
class EquipmentRemoveRequest(BaseModel):
    syskey: Union[str, int, List[Union[str, int]]]