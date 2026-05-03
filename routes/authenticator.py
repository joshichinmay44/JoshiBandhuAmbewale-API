from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/login", tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()

@router.post("/token")
async def login(username: str = Body(), password: str = Body()):
    try:
        password_jwt=common_util.generate_jwt(password)
        username=username
        cursor = conn.cursor()
        cursor.execute("select * from usr.authenticate_script(%s,%s)",(username,password_jwt))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))