# common/utils/response_helper.py
from fastapi.responses import JSONResponse
from decimal import Decimal
import math
import asyncpg

def success_response(status_code: int, message: str, data: dict = None):
    """ API အောင်မြင်ရင် ပြန်မည့် Response ပုံစံခွက် """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data or {}
        }
    )

def error_response(status_code: int, message: str):
    """ API Error တက်ရင် ပြန်မည့် Response ပုံစံခွက် """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None
        }
    )
from decimal import Decimal
import math
import asyncpg

def serialize_value(val):
    """Recursively converts Decimals to float/int and handles custom types."""
    if isinstance(val, Decimal):
        # Convert to int if no decimal places, else float
        return int(val) if val % 1 == 0 else float(val)
    elif isinstance(val, dict):
        return {k: serialize_value(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [serialize_value(v) for v in val]
    return val