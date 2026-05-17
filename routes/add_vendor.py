from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/vendor", tags=["add_vendor"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/add_vendor")
async def add_vendor(vendor_name:str =Body(), contact_name:str =Body(), email:str =Body(), phone_number_calling:str =Body(), phone_number_whatsapp:str =Body(),  street:str =Body(), city:str =Body(), state:str =Body(), pincode:str =Body(), country:str =Body(), created_by:str =Body()):
    try:
        print("In")
        cursor = conn.cursor()
        cursor.execute("CALL dim.usp_add_vendors(%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR,%s::VARCHAR);", (vendor_name,contact_name,email,phone_number_calling,phone_number_whatsapp,street,city,state,pincode,country,created_by))
        cursor.close()
        return {"message": "User added successfully", "status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))