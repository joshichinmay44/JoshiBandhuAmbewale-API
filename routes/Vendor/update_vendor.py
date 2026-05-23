from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

router = APIRouter(prefix="/vendor", tags=["update_vendor"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/update_vendor")
async def update_vendor(vendor_name: str =Body(), contact_name: str =Body(), email: str =Body(), phone_number_calling: str =Body(), phone_number_whatsapp: str =Body(), updated_by: str =Body(),vendor_id: int =Body(), country: str =Body(default=None), state: str =Body(default=None), city: str =Body(default=None), pincode: str =Body(default=None), street: str = Body(default=None)):
    try:
        logging.info("Starting add_user process")
        print("Received data:", vendor_name, contact_name, email, phone_number_calling, phone_number_whatsapp, updated_by, vendor_id, country, state, city, pincode, street)
        username=updated_by
        cursor = conn.cursor()
        cursor.execute("CALL dim.usp_update_vendor(%s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::VARCHAR, %s::VARCHAR, %s::VARCHAR, %s::VARCHAR, %s::bigint);", (vendor_name, contact_name, email, phone_number_calling, phone_number_whatsapp, updated_by, country, state, city, pincode, street, vendor_id))
        cursor.close()
        return {"message": "User updated successfully", "status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))