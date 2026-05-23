from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
import logging

router = APIRouter(prefix="/customer", tags=["add_customer"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/add_customer")
async def add_customer(first_name: str =Body(), last_name: str =Body(), email: str =Body(), phone_number_calling: str =Body(), phone_number_whatsapp: str =Body(), customer_type: str =Body(), customer_mode: str =Body(), created_by: str =Body(), country: str =Body(), state: str =Body(), city: str =Body(), pincode: str =Body(), street: str = Body()):
    try:
        logging.info("Starting add_user process")
        print("Received data:", first_name, last_name, email, phone_number_calling, phone_number_whatsapp, customer_type, customer_mode, created_by, country, state, city, pincode, street)
        username=created_by
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id FROM dim.customer WHERE first_name = %s AND (phone_number_calling=%s OR phone_number_whatsapp=%s);", (first_name, phone_number_calling, phone_number_whatsapp))
        user_id = cursor.fetchone()
        if user_id:
            raise HTTPException(status_code=400, detail="User already exists")
        cursor.execute("CALL dim.usp_insert_new_customer(%s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar);", (first_name, last_name, email, phone_number_calling, phone_number_whatsapp, customer_type, customer_mode, created_by, country, state, city, pincode, street))
        cursor.close()
        return {"message": "User added successfully", "status": "success"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))