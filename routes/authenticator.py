from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

router = APIRouter(prefix="/login", tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/token")
async def login(username: str = Body(), password: str = Body()):
    try:
        logging.info(Body())
        password_jwt=common_util.generate_jwt(password)
        logging.info(f"Login attempt for user: {username}")
        username=username
        cursor = conn.cursor()
        cursor.execute("select * from usr.authenticate_script(%s,%s)",(username,password_jwt))
        result = cursor.fetchone()
        cursor.close()
        if result[0] != True:
            logging.warning(f"Failed login attempt for user: {username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return {"username": username, "logged_in": bool(result[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))