from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

router = APIRouter(prefix="/customer", tags=["update_customer"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/update_customer")
async def update_customer(first_name: str =Body(), last_name: str =Body(), email: str =Body(), phone_number_calling: str =Body(), phone_number_whatsapp: str =Body(), customer_type: str =Body(), customer_mode: str =Body(), updated_by: str =Body(),cust_id: int =Body(), country: str =Body(), state: str =Body(), city: str =Body(), pincode: str =Body(), street: str = Body()):
    try:
        logging.info("Starting add_user process")
        print("Received data:", first_name, last_name, email, phone_number_calling, phone_number_whatsapp, customer_type, customer_mode, updated_by)
        username=updated_by
        cursor = conn.cursor()
        cursor.execute("CALL dim.usp_update_customer(%s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::bigint, %s::varchar, %s::varchar, %s::varchar, %s::varchar);", (first_name, last_name, email, phone_number_calling, phone_number_whatsapp, customer_type, customer_mode, updated_by, cust_id, country, state, city, pincode, street))
        cursor.close()
        return {"message": "User updated successfully", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))