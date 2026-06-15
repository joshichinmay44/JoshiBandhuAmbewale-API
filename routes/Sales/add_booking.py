from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
import logging

router = APIRouter(prefix="/sales", tags=["sales"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/add_booking")
async def add_booking(customer_name : str = Body(), sku_name: str =Body(), quantity : str = Body(), lead_generated_by: str = Body(), created_by: str =Body()):
    try:
        logging.info("Starting add_booking process")
        cursor = conn.cursor()
        logging.info("Customer Name: ", customer_name)
        cursor.execute("CALL dm.usp_add_booking(%s::VARCHAR, %s::VARCHAR, %s::NUMERIC(19,4), %s::VARCHAR, %s::VARCHAR)", (customer_name, sku_name, quantity, lead_generated_by, created_by))
        cursor.close()
        return {"message": "Booking added successfully", "status": "success"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))