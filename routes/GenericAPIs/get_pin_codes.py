from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
import logging

router = APIRouter(prefix="/address", tags=["add_user"])

common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.get("/get_pin_codes/")
@router.get("/get_pin_codes/{city}")
async def get_customers(city: str | None = None):
    try:
        logging.info("Starting get_customers process")
        cursor = conn.cursor()
        cursor.execute("select * from dim.get_pin_codes(%s) ;", (city,))
        result = cursor.fetchall()
        cursor.close()
        res = [row[0] for row in result]
        return {"pin_codes": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))