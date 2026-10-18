# analytics/service.py
from analytics.model import LoginRequest

async def authenticate_user(db, request: LoginRequest) -> dict:
    try:
        # async logic standard အတိုင်း စစ်ဆေးခြင်း
        query = "SELECT syskey, t1, t2, t3, n1 FROM users WHERE t1 = $1 OR t2 = $1"
        user = await db.fetchrow(query, request.username)

        # 1. User မရှိပါက
        if not user:
            return {"success": False, "message": "Username သို့မဟုတ် Password မှားယွင်းနေပါသည်။"}

        db_password = user["t3"]
        status = user["n1"]

        # 2. Status မမှန်ပါက
        if status != 1:
            return {"success": False, "message": "ဤအကောင့်မှာ အသုံးပြုခွင့် ပိတ်ထားပါသည်။"}

        # 3. Password မှားပါက
        if request.password != db_password:
            return {"success": False, "message": "Username သို့မဟုတ် Password မှားယွင်းနေပါသည်။"}

        # 4. အကုန်မှန်ပါက Controller မျှော်လင့်ထားသော Key နာမည်များအတိုင်း Return ပြန်ပေးရန်
        return {
            "success": True,
            "message": "Login Success",
            "access_token": "fake-jwt-token-here",  # သို့မဟုတ် သင့် JWT token generator logic
            "token_type": "bearer",
            "user_info": {
                "syskey": str(user["syskey"]),
                "username": user["t1"],
                "email": user["t2"]
            }
        }

    except Exception as e:
        print(f"Error in authenticate_user: {str(e)}")
        return {"success": False, "message": "Database Error ဖြစ်ပေါ်ခဲ့ပါသည်။"}