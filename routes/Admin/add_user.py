from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/login", tags=["add_customer"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/add_user")
async def add_user(username: str =Body(), email: str =Body(), password: str =Body(), first_name: str =Body(), last_name: str =Body(), date_of_birth: str =Body(), phone_number: str =Body(), address: str =Body(), created_by: str =Body()):
    try:
        print("Received data:", username, email, password, first_name, last_name, date_of_birth, phone_number, address)
        cursor = conn.cursor()
        res=cursor.execute("SELECT * FROM usr.validate_username_availability(%s::VARCHAR)", (username,))
        is_username_available = cursor.fetchone()[0]
        if not is_username_available:
            raise HTTPException(status_code=401, detail="Username is already taken")
        password_jwt=common_util.generate_jwt(password)
        cursor.execute("CALL usr.usp_add_new_user(%s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::date, %s::varchar, %s::varchar, %s::varchar);", (username, email, password_jwt, first_name, last_name, date_of_birth, phone_number, address, created_by))
        cursor.close()
        return {"message": "User added successfully", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))