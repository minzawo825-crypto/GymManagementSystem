

from re import search

import asyncpg
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from decimal import Decimal

from equipments_entry_form.model import EquipmentCreateRequest, EquipmentEntryList, EquipmentRemoveRequest

from equipments_entry_form import service as equipments_entry_form_service
from database.core import get_db
from common.utils.logging_util import get_logger_with_request_id
import common.utils.response_helper as resp
from fastapi import APIRouter, Depends, Query, Request
from typing import Literal, Optional
import sys

from database.core import get_db
from common.utils.logging_util import get_logger_with_request_id
import common.utils.response_helper as resp

from members_entry_form.service import remove_member

from auth.service import create_access_token
router = APIRouter()






@router.post("/entry/create_new_equipment")
async def equipment_entry(
    request: Request,
    body: EquipmentCreateRequest,
    db = Depends(get_db)
):
    logger = get_logger_with_request_id(request)
    try:
        result = await equipments_entry_form_service.create_new_equipment(db=db, request=body)
        
        if not result["success"]:
            return resp.error_response(status_code=400, message=result["message"])
            
        return resp.success_response(
            status_code=200,
            message=result["message"]
        )
        
    except Exception as e:
        print("======== CRITICAL MEMBER ENTRY ERROR ========")
        print(f"Error Type: {type(e).__name__} | Message: {str(e)}")
        import traceback; traceback.print_exc()
        print("=============================================")

        logger.error(
            "Error from Member Entry Endpoint",
            extra={"err_msg": f"{e} Error on Line {sys.exc_info()[-1].tb_lineno}"},
        )
        return resp.error_response(status_code=500, message="Internal Server Error")


@router.post("/entry/get_equipment_list")
async def get_equipment_list(
    request: Request,
    body: EquipmentEntryList, # Accepts cur_page, page_size, and optional t1-t8 filters
    db = Depends(get_db)
):
    logger = get_logger_with_request_id(request)
    try:
        result = await equipments_entry_form_service.get_equipment_list(db=db, request=body)
        
        if not result["success"]:
            return resp.error_response(status_code=400, message=result["message"])
            
        return resp.success_response(
            status_code=200,
            message=result["message"],
            data=result["data"]
        )
        
    except Exception as e:
        logger.error(
            "Error from Equipment List Endpoint",
            extra={"err_msg": f"{e} Error on Line {sys.exc_info()[-1].tb_lineno}"},
        )
        return resp.error_response(status_code=500, message="Internal Server Error")

@router.post("/entry/remove")
async def remove_equipment_route(
    request: Request,
    payload: EquipmentRemoveRequest, 
    db: asyncpg.Connection = Depends(get_db)
):
    logger = get_logger_with_request_id(request)
    try:
        # Call the helper function in service.py
        result = await equipments_entry_form_service.remove_equipment(db, payload)
        
        # Check if service function returned a failure dictionary
        if not result.get("success"):
            return resp.error_response(
                status_code=400 if "format" in result.get("message", "") else 404, 
                message=result.get("message", "Failed to remove equipment")
            )

        return resp.success_response(
            status_code=200, 
            message=result.get("message"),
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Error removing equipment: {str(e)}", exc_info=True)
        return resp.error_response(status_code=500, message="Internal Server Error")

