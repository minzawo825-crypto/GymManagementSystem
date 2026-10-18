# analytics/controller.py
from fastapi import APIRouter, Depends, Request
import sys

from analytics.model import LoginRequest
from analytics import service as analytics_service
from database.core import get_db
from common.utils.logging_util import get_logger_with_request_id
import common.utils.response_helper as resp

router = APIRouter()

@router.post("/login")
async def login(
    request: Request,
    body: LoginRequest,
    db = Depends(get_db)
):
    logger = get_logger_with_request_id(request)
    try:
        # Service လွှဲပေးခြင်း
        result = await analytics_service.authenticate_user(db=db, request=body)
        
        # 💡 ရလဒ် မအောင်မြင်ပါက 400 Response နှင့် သက်ဆိုင်ရာ message ပြန်မည်
        if not result.get("success"):
            return resp.error_response(
                status_code=400, 
                message=result.get("message", "Invalid username or password")
            )
            
        return resp.success_response(
            status_code=200,
            message="Login success",
            data={
                "access_token": result.get("access_token", ""),
                "token_type": result.get("token_type", "bearer"),
                "user": result.get("user_info", {})
            }
        )
        
    except Exception as e:
        print("======== CRITICAL LOGIN ERROR ========")
        print(f"Error Type: {type(e).__name__} | Message: {str(e)}")
        import traceback; traceback.print_exc()
        print("======================================")

        logger.error(
            "Error from Login Endpoint",
            extra={"err_msg": f"{e} Error on Line {sys.exc_info()[-1].tb_lineno}"},
        )
        return resp.error_response(status_code=500, message="Internal Server Error")