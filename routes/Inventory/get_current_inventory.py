from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
import logging

router = APIRouter(prefix="/inventory", tags=["inventory"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.get("/get_current_inventory")
@router.get("/get_current_inventory/{id}")
async def get_current_inventory(id :int | None = None):
    try:
        cursor = conn.cursor()
        if id:
            query = "SELECT * FROM dm.usp_get_current_inventory() WHERE batch_id = %s;"
            cursor.execute(query, (id,))
        else:
            query = "SELECT * FROM dm.usp_get_current_inventory();"
            cursor.execute(query)
        inventory_data = cursor.fetchall()
        return {"inventory": inventory_data}
    except Exception as e:
        logging.error(f"Error fetching inventory data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")