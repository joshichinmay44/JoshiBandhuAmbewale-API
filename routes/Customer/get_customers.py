from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
import logging

router = APIRouter(prefix="/customer", tags=["add_user"])

common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.get("/get_customers/")
@router.get("/get_customers/{id}")
async def get_customers(id: int | None = None):
    try:
        logging.info("Starting get_customers process")
        cursor = conn.cursor()
        if id:
            cursor.execute("select * from dim.usp_get_customers() where customer_id = %s;", (id,))
        else:
            cursor.execute("select * from dim.usp_get_customers();")
        result = cursor.fetchall()
        cursor.close()
        return {"customers": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))