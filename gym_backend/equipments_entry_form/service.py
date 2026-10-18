

# ==========================================
# 1. CREATE NEW MEMBER
# ==========================================
from decimal import Decimal
import datetime
import math
import uuid
import asyncpg
from equipments_entry_form.model import EquipmentCreateRequest , EquipmentEntryList,EquipmentRemoveRequest

async def create_new_equipment(
    db: asyncpg.Connection,
    request: EquipmentCreateRequest,
    user_id: str = "system"  # Pass the current user ID if available
) -> dict:
    try:
        # 1. Generate a unique syskey (Timestamp in ms + random digits)
        syskey_val = str(int(datetime.datetime.now().timestamp() * 1000))

        # 2. Convert date object or string safely to YYYY-MM-DD
        t3_val = request.t3.isoformat() if hasattr(request.t3, "isoformat") else str(request.t3)

        # 3. Handle cost / amount conversion safely
        t8_val = Decimal(str(request.t8)) if request.t8 is not None else Decimal("0.00")

        # 4. Set current UTC timestamp for audit columns
        now_tz = datetime.datetime.now(datetime.timezone.utc)

        query = """
            INSERT INTO equipments (
                syskey, t1, t2, t3, t4, t5, t6, t7, t8, n1,
                createddate, createdby, modifieddate, modifiedby
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                $11, $12, $13, $14
            )
            RETURNING syskey, autokey;
        """

        row = await db.fetchrow(
            query,
            syskey_val,              # $1  (syskey)
            request.t1,              # $2  (t1 - Equipment)
            request.t2,              # $3  (t2 - Description)
            t3_val,                  # $4  (t3 - Date of Purchase)
            str(request.t4),         # $5  (t4 - Quantity)
            request.t5,              # $6  (t5 - Vendor)
            request.t6,              # $7  (t6 - Vendor Address)
            request.t7,              # $8  (t7 - Contact)
            t8_val,                  # $9  (t8 - Amount DECIMAL)
            request.n1,              # $10 (n1 - Status 1 or 4)
            now_tz,                  # $11 (createddate)
            user_id,                 # $12 (createdby)
            now_tz,                  # $13 (modifieddate)
            user_id                  # $14 (modifiedby)
        )

        return {
            "success": True,
            "message": "Equipment created successfully.",
            "data": {
                "syskey": row["syskey"],
                "autokey": row["autokey"]
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

async def get_equipment_list(
    db: asyncpg.Connection,
    request: EquipmentEntryList
) -> dict:
    try:
        limit = request.page_size
        offset = (request.cur_page - 1) * limit

        # 1. Fetch paginated rows matching status n1
        query = """
            SELECT syskey, t1, t2, t3, t4, t5, t6, t7, t8, n1
            FROM equipments
            WHERE n1 = $1
            ORDER BY autokey DESC
            LIMIT $2 OFFSET $3;
        """
        rows = await db.fetch(query, request.n1, limit, offset)

        # 2. Get total record count for table pagination
        count_query = "SELECT COUNT(*) FROM equipments WHERE n1 = $1;"
        total_count = await db.fetchval(count_query, request.n1)

        # 3. Sanitize data types (Decimal, UUID, date) to standard JSON types
        equipment_list = []
        for row in rows:
            item = dict(row)
            for key, val in item.items():
                if isinstance(val, Decimal):
                    item[key] = float(val)  # Convert Decimal to float for t8
                elif isinstance(val, (uuid.UUID, datetime.date, datetime.datetime)):
                    item[key] = str(val)    # Convert date/UUID to string
            equipment_list.append(item)

        return {
            "success": True,
            "message": "Equipment list fetched successfully.",
            "data": {
                "itemname": equipment_list,
                "total_count": total_count,
                "cur_page": request.cur_page,
                "page_size": request.page_size
            }
        }

    except Exception as e:
        print("======== CRITICAL EQUIPMENT LIST ERROR ========")
        print(f"Error Message: {str(e)}")
        import traceback; traceback.print_exc()
        print("==============================================")
        return {
            "success": False,
            "message": str(e)
        }

async def remove_equipment(
    db: asyncpg.Connection,
    payload: EquipmentRemoveRequest
) -> dict:
    """
    Deletes equipment record(s) from PostgreSQL using string, UUID, or int syskey(s).
    Supports single items, lists, or comma-separated strings.
    """
    try:
        # Normalize syskey into a clean list of strings
        syskeys: list[str] = []

        if isinstance(payload.syskey, list):
            syskeys = [str(k).strip() for k in payload.syskey if str(k).strip()]
        elif isinstance(payload.syskey, str) and "," in payload.syskey:
            syskeys = [k.strip() for k in payload.syskey.split(",") if k.strip()]
        elif payload.syskey:
            syskeys = [str(payload.syskey).strip()]

        if not syskeys:
            return {
                "success": False,
                "message": "syskey cannot be empty.",
            }

        # Query using ANY($1) for multi/single deletion
        query = """
            DELETE FROM equipments 
            WHERE syskey = ANY($1::text[])
            RETURNING syskey
        """

        deleted_records = await db.fetch(query, syskeys)
        deleted_syskeys = [str(record["syskey"]) for record in deleted_records]

        if not deleted_syskeys:
            joined_keys = ",".join(syskeys)
            return {
                "success": False,
                "message": f"Equipment with syskey '{joined_keys}' not found or already removed.",
            }

        return {
            "success": True,
            "message": f"Equipment removed successfully.",
            "data": {"syskeys": deleted_syskeys},
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }