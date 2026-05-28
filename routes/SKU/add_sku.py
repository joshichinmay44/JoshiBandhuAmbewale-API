from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
import logging

router = APIRouter(prefix="/sku", tags=["sku"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/add_sku")
async def add_sku(sku_name: str =Body(), description: str =Body(), created_by: str =Body()):
    try:
        logging.info("Starting add_sku process")
        print("Received data:", sku_name, description, created_by)
        username=created_by
        cursor = conn.cursor()
        cursor.execute("SELECT sku_id FROM dim.sku WHERE lower(sku_name) = lower(%s::VARCHAR);", (sku_name,))
        try:
            sku_id = cursor.fetchone()
        except Exception as e:
            sku_id = None
        if sku_id:
            raise HTTPException(status_code=400, detail="SKU already exists")
        cursor.execute("CALL dim.usp_add_sku(%s::varchar, %s::text, %s::varchar);", (sku_name, description, created_by))
        cursor.close()
        return {"message": "SKU added successfully", "status": "success"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))