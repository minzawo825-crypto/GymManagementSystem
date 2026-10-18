

# ==========================================
# 1. CREATE NEW MEMBER
# ==========================================
import math
import datetime
from decimal import Decimal
import uuid
import asyncpg
from members_entry_form.model import MemberCreateRequest,MemberEntryList, MemberRemoveRequest, MemberUpdateRequest,MemberGetRequest



async def create_new_member(db, request: MemberCreateRequest):
    # 1. Fetch text values using positional parameters ($1)
    gender_name = await db.fetchval(
        "SELECT t1 FROM gender WHERE syskey = $1", 
        request.t4
    )
    plan_name = await db.fetchval(
        "SELECT t1 FROM plan WHERE syskey = $1", 
        request.t6
    )
    service_name = await db.fetchval(
        "SELECT t1 FROM service WHERE syskey = $1", 
        request.t9
    )

    if not all([gender_name, plan_name, service_name]):
        return {"success": False, "message": "Invalid syskey provided for gender, plan, or service."}

        
    # 2. Insert values using positional placeholders ($1 through $11)
    new_syskey = uuid.uuid4().hex
    query = """
        INSERT INTO members (
            syskey, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, n1, createddate
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, 1, NOW()
        )
    """

    # Pass the variables in the exact positional order matching $1 to $11
    await db.execute(
        query,
        new_syskey,          # $1  - syskey
        request.t1,    # $2  - t1 (name)
        request.t2,    # $3  - t2 (uname)
        request.t3,    # $4  - t3 (pwd)
        gender_name,         # $8  - t4 (gender)
       
        str(request.t5),        # $6  - t5 (dor)
        plan_name,           # $7  - t6 (plan)
        request.t7,     # $5  - t4 (addr)
        request.t8,     # $9  - t8 (contact)
        service_name,        # $10 - t9 (service)
        request.t10       # $11 - t10 (amount)
    )

    return {"success": True, "message": "Member created successfully"}

# ==========================================
# 2. GET PAGINATED & FILTERED MEMBER LIST
# =======================================


async def get_member_list(
    db: asyncpg.Connection,
    search: MemberEntryList,
    page_size: int = 25,
    cur_page: int = 1,
) -> dict:
    """Fetch paginated and filtered member list (PostgreSQL Version)."""
    try:
        cur_page = search.cur_page if getattr(search, "cur_page", 0) > 0 else cur_page
        page_size = search.page_size if getattr(search, "page_size", 0) > 0 else page_size
        offset = (cur_page - 1) * page_size

        # Initialize base WHERE clause
        base_where = " WHERE n1 = 1"
        params = []
        param_index = 1

        # Dynamic Filters Construction mapping DB column -> Pydantic field attribute
        filters = [
            ("t1", getattr(search, "members", None), "LIKE"),
            ("t2", getattr(search, "username", None), "LIKE"),
            ("t3", getattr(search, "gender", None), "="),
            ("t4", getattr(search, "plan", None), "="),
            ("t5", getattr(search, "contact", None), "LIKE"),
            ("t6", getattr(search, "address", None), "LIKE"),
            ("t7", getattr(search, "service", None), "="),
        ]

        for field, value, operator in filters:
            if value:
                if operator == "LIKE":
                    base_where += f" AND {field} ILIKE ${param_index}"
                    params.append(f"%{value}%")
                else:
                    base_where += f" AND {field} = ${param_index}"
                    params.append(value)
                param_index += 1

        # 1. Get Total Count using the compiled filters
        count_query = f"SELECT COUNT(*) FROM members{base_where}"
        total_count = await db.fetchval(count_query, *params)
        total_count = total_count if total_count else 0
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1

        # 2. Main Query With Pagination
        query = f"""
            SELECT 
                syskey, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
            FROM members
            {base_where}
            ORDER BY autokey DESC 
            LIMIT ${param_index} OFFSET ${param_index + 1}
        """

        fetch_params = params + [page_size, offset]
        rows = await db.fetch(query, *fetch_params)

        result_data = [dict(row) for row in rows]

        return {
            "success": True,
            "message": "Member list fetched successfully",
            "data": result_data,
            "pagination": {
                "cur_page": cur_page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
            },
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }

# ==========================================
# 3. GET DROPDOWN DATA
# ==========================================



async def get_dropdown_data(type_param: str, db: asyncpg.Connection):
    """
    Fetches dropdown options dynamically based on the type parameter.
    """
    
    queries = {
        "gender": """
            SELECT syskey, t1 
            FROM gender 
            ORDER BY autokey ASC;
        """,
        "plan": """
            SELECT syskey, t1 
            FROM plan 
            ORDER BY autokey ASC;
        """,
        "service": """
            SELECT syskey, t1, CAST(t2 AS TEXT) as t2 
            FROM service 
            ORDER BY autokey ASC;
        """
    }

    query = queries.get(type_param)
    if not query:
        return []

    # Execute asyncpg query
    records = await db.fetch(query)
    
    # Convert asyncpg Record objects to a list of dicts
    result = []
    for row in records:
        data = {
            "syskey": str(row["syskey"]),
            "t1": str(row["t1"])
        }
        if "t2" in row and row["t2"] is not None:
            data["t2"] = str(row["t2"])
        result.append(data)

    return result
# ==========================================
# 3. GET Removed Member
# ==========================================



async def remove_member(
    db: asyncpg.Connection,
    payload: MemberRemoveRequest
) -> dict:
    """
    Deletes a member record from PostgreSQL using string/UUID syskey.
    Uses DELETE FROM to bypass UPDATE check constraints.
    """
    try:
        syskey_str = str(payload.syskey).strip() if payload.syskey else ""
        if not syskey_str:
            return {
                "success": False,
                "message": "syskey cannot be empty.",
            }

        # Hard delete query
        query = """
            DELETE FROM members 
            WHERE syskey = $1 
            RETURNING syskey
        """

        deleted_syskey = await db.fetchval(query, syskey_str)

        if not deleted_syskey:
            return {
                "success": False,
                "message": f"Member with syskey '{syskey_str}' not found or already removed.",
            }

        return {
            "success": True,
            "message": "Member removed successfully.",
            "data": {"syskey": str(deleted_syskey)},        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }
# ==========================================
# 3. GET Update Member
# ==========================================
async def update_member(
    db: asyncpg.Connection,
    request: MemberUpdateRequest
) -> dict:
    """
    Updates an existing member record in PostgreSQL matching the t1-t10 schema.
    """
    try:
        syskey_str = str(request.syskey).strip() if getattr(request, "syskey", None) else ""
        if not syskey_str:
            return {
                "success": False,
                "message": "syskey cannot be empty.",
            }

        # 1. Look up foreign key names (Check if it's already a name or a syskey ID)
        gender_name = None
        if getattr(request, "t4", None):
            gender_name = await db.fetchval("SELECT t1 FROM gender WHERE syskey::text = $1", str(request.t4))
            if not gender_name:  # If not found by syskey, assume it's already the text label
                gender_name = request.t4

        plan_name = None
        if getattr(request, "t6", None):
            plan_name = await db.fetchval("SELECT t1 FROM plan WHERE syskey::text = $1", str(request.t6))
            if not plan_name:
                plan_name = request.t6

        service_name = None
        if getattr(request, "t9", None):
            service_name = await db.fetchval("SELECT t1 FROM service WHERE syskey::text = $1", str(request.t9))
            if not service_name:
                service_name = request.t9

        # 2. Prepare safe string conversions for optional fields
        t5_val = str(request.t5) if getattr(request, "t5", None) is not None else None
        t10_val = str(request.t10) if getattr(request, "t10", None) is not None else None

        # 3. Update query aligning columns directly to create_new_member structure
        query = """
            UPDATE members
            SET
                t1 = COALESCE($2, t1),   -- Name
                t2 = COALESCE($3, t2),   -- Username
                t3 = COALESCE($4, t3),   -- Password
                t4 = COALESCE($5, t4),   -- Gender Name
                t5 = COALESCE($6, t5),   -- Date of Registration (DOR)
                t6 = COALESCE($7, t6),   -- Plan Name
                t7 = COALESCE($8, t7),   -- Address
                t8 = COALESCE($9, t8),   -- Contact
                t9 = COALESCE($10, t9),  -- Service Name
                t10 = COALESCE($11, t10) -- Amount
            WHERE syskey::text = $1
            RETURNING syskey, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
        """

        updated_row = await db.fetchrow(
            query,
            syskey_str,       # $1
            request.t1,       # $2  (t1 - Name)
            request.t2,       # $3  (t2 - Username)
            request.t3,       # $4  (t3 - Password)
            gender_name,      # $5  (t4 - Gender Name)
            t5_val,           # $6  (t5 - DOR)
            plan_name,        # $7  (t6 - Plan Name)
            request.t7,       # $8  (t7 - Address)
            request.t8,       # $9  (t8 - Contact)
            service_name,     # $10 (t9 - Service Name)
            t10_val           # $11 (t10 - Amount)
        )

        if not updated_row:
            return {
                "success": False,
                "message": f"Member with syskey '{syskey_str}' not found.",
            }

        # Convert record to dictionary
        updated_dict = dict(updated_row)

        # 4. Serialize Decimal, UUID, and Date types for JSON response compatibility
        for key, val in updated_dict.items():
            if isinstance(val, Decimal):
                updated_dict[key] = float(val)
            elif isinstance(val, (uuid.UUID, datetime.date, datetime.datetime)):
                updated_dict[key] = str(val)

        return {
            "success": True,
            "message": "Member updated successfully.",
            "data": updated_dict,
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }
# service.py

# service.py

async def get_member_by_syskey(
    db: asyncpg.Connection,
    payload: MemberGetRequest
) -> dict:
    """
    Fetches a single member record from PostgreSQL using syskey via POST request.
    """
    try:
        syskey_str = str(payload.syskey).strip() if payload.syskey else ""
        if not syskey_str:
            return {
                "success": False,
                "message": "syskey cannot be empty.",
            }

        # Query member row - cast UUID/text safely
        query = """
            SELECT syskey, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10
            FROM members
            WHERE syskey::text = $1
        """
        row = await db.fetchrow(query, syskey_str)

        if not row:
            return {
                "success": False,
                "message": f"Member with syskey '{syskey_str}' not found.",
            }

        # Convert asyncpg.Record to a clean, serializable dict
        member_dict = dict(row)

        # Convert non-JSON-serializable types to strings
        for key, value in member_dict.items():
            if value is not None and not isinstance(value, (str, int, float, bool)):
                member_dict[key] = str(value)

        return {
            "success": True,
            "message": "Member details fetched successfully.",
            "data": member_dict,
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }