from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

router = APIRouter(prefix="/sku", tags=["sku"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/update_sku")
async def update_sku(sku_id :str =Body(),sku_name: str =Body(), description: str =Body(), updated_by: str =Body()):
    try:
        logging.info("Starting update_sku process")
        print("Received data:", sku_id, sku_name, description, updated_by)
        username=updated_by
        cursor = conn.cursor()
        cursor.execute("CALL dim.usp_update_sku(%s::BIGINT, %s::varchar, %s::text, %s::varchar);", (sku_id, sku_name, description, updated_by))
        cursor.close()
        return {"message": "SKU updated successfully", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))