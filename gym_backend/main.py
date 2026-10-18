# main.py ထဲတွင် အပေါ်ဆုံးနားက လိုင်းကို ဤသို့ပြင်ပါ -
# main.py
from fastapi import FastAPI
from analytics.controller import router as analytics_router
from members_entry_form.controller import router as member_router
from equipments_entry_form.controller import router as equipment_router
from fastapi.middleware.cors import CORSMiddleware

# 💡 ဤနေရာသည် အရေးကြီးဆုံးဖြစ်ပါသည် - uvicorn ရှာနေသော "app" က ဒါပါပဲဗျာ
app = FastAPI(title="Gym Management System API")
origins = [
    "http://localhost:4200",      # Angular default url
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],          
)



app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(member_router, prefix="/api/members_entry_form", tags=["Members Management"])
app.include_router(equipment_router, prefix="/api/equipments_entry_form", tags=["Equipments Management"])
@app.get("/")
def read_root():
    return {"message": "Gym Backend API is running successfully!"}