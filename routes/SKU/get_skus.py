from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
import logging

router = APIRouter(prefix="/sku", tags=["add_user"])

common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.get("/get_skus/")
@router.get("/get_skus/{id}")
async def get_skus(id: int | None = None):
    try:
        logging.info("Starting get_skus process")
        cursor = conn.cursor()
        if id:
            cursor.execute("select * from dim.usp_get_skus() where sku_id = %s;", (id,))
        else:
            cursor.execute("select * from dim.usp_get_skus();")
        result = cursor.fetchall()
        cursor.close()
        return {"skus": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))