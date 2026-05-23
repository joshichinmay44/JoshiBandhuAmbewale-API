from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
import logging

router = APIRouter(prefix="/vendor", tags=["add_user"])

common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.get("/get_vendors/")
@router.get("/get_vendors/{id}")
async def get_vendors(id: int | None = None):
    try:
        logging.info("Starting get_vendors process")
        cursor = conn.cursor()
        if id:
            cursor.execute("select * from dim.usp_get_vendors() where vendor_id = %s;", (id,))
        else:
            cursor.execute("select * from dim.usp_get_vendors();")
        result = cursor.fetchall()
        cursor.close()
        return {"vendors": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))