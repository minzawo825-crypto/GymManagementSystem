

from re import search

import asyncpg
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from decimal import Decimal

from members_entry_form.model import MemberCreateRequest, MemberEntryList, MemberRemoveRequest,MemberUpdateRequest,MemberGetRequest
from members_entry_form import service as members_entry_form_service
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



class MemberDeleteRequest(BaseModel):
    syskey: str


@router.post("/entry/create_new_member")
async def member_entry(
    request: Request,
    body: MemberCreateRequest,
    db = Depends(get_db)
):
    logger = get_logger_with_request_id(request)
    try:
        result = await members_entry_form_service.create_new_member(db=db, request=body)
        
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


def serialize_value(val):
    """Recursively converts Decimals to float/int and handles custom types."""
    if isinstance(val, Decimal):
    
        return int(val) if val % 1 == 0 else float(val)
    elif isinstance(val, dict):
        return {k: serialize_value(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [serialize_value(v) for v in val]
    return val
@router.post("/entry/member_list")
async def get_member_list(
    request: Request,
    
    search: MemberEntryList,
    db=Depends(get_db),
    page_size: int = 25,
    cur_page: int = 1,
   
):
    logger = get_logger_with_request_id(request)
    try:
        result =  await members_entry_form_service.get_member_list(db=db, search=search, page_size=page_size, cur_page=cur_page)

        if not result["success"]:
            return resp.error_response(status_code=400, message=result["message"])
        clean_data = serialize_value(result.get("data", []))
        return resp.success_response(
            status_code=200,
            message=result["message"],
            data={
            "items": clean_data,
            "pagination": result.get("pagination", {}),
    },
        )
    except Exception as e:
        logger.error(
            "Error fetching member list data",
            extra={"err_msg": f"{e} Error on Line {sys.exc_info()[-1].tb_lineno}"},
        )
        return resp.error_response(status_code=500, message=str(e))
    



@router.post("/entry/remove")
async def remove_member_route(
    request: Request,
    payload: MemberRemoveRequest, 
    db: asyncpg.Connection = Depends(get_db)
):
    logger = get_logger_with_request_id(request)
    try:
        
        result = await  members_entry_form_service.remove_member(db, payload)
        
        
        if not result.get("success"):
            return resp.error_response(
                status_code=400 if "format" in result.get("message", "") else 404, 
                message=result.get("message", "Failed to remove member")
            )

        return resp.success_response(
            status_code=200, 
            message=result.get("message"),
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Error removing member: {str(e)}", exc_info=True)
        return resp.error_response(status_code=500, message="Internal Server Error")


@router.get("/dropdown")
async def get_dropdown_data(
    request: Request,
    type: Literal["gender", "plan", "service"] = Query(...),
    db: asyncpg.Connection = Depends(get_db),
):
    logger = get_logger_with_request_id(request)
    try:
        # Call service without 'token' parameter
        result = await members_entry_form_service.get_dropdown_data(type, db)

        return resp.success_response(
            status_code=200, 
            message="Success", 
            data={"data_list": result}
        )
    except Exception as e:
        logger.error(
            "Error from get_dropdown data",
            extra={"err_msg": f"{e} Error on Line {sys.exc_info()[-1].tb_lineno}"},
        )
        return resp.error_response(status_code=500, message=str(e))
    # --- EDIT MEMBER ENDPOINTS ---


@router.post("/entry/update_member")
async def update_member(
    request: Request,
    payload: MemberUpdateRequest,
    db: asyncpg.Connection = Depends(get_db)
):
    """
    Updates an existing member record in the database.
    """
    logger = get_logger_with_request_id(request)
    try:
        result = await members_entry_form_service.update_member(db=db, request=payload)
        
        if not result.get("success"):
            return resp.error_response(status_code=400, message=result.get("message", "Failed to update member"))

        return resp.success_response(
            status_code=200,
            message=result.get("message", "Member updated successfully"),
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Error updating member: {str(e)}", exc_info=True)
        return resp.error_response(status_code=500, message="Internal Server Error")

@router.post("/entry/get_member")
async def get_member_by_syskey(
    request: Request,
    payload: MemberGetRequest,
    db: asyncpg.Connection = Depends(get_db)
):
    """
    Fetches a single member record by syskey using POST request body.
    """
    logger = get_logger_with_request_id(request)
    try:
        result = await members_entry_form_service.get_member_by_syskey(db=db, payload=payload)
        
        if not result.get("success"):
            return resp.error_response(
                status_code=400 if "empty" in result.get("message", "") else 404, 
                message=result.get("message", "Failed to fetch member")
            )

        return resp.success_response(
            status_code=200,
            message=result.get("message", "Member details fetched successfully"),
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Error fetching member: {str(e)}", exc_info=True)
        return resp.error_response(status_code=500, message="Internal Server Error")
        
    