from utils import common_util
from fastapi import HTTPException, APIRouter
import logging

router = APIRouter(prefix="/sales", tags=["get_bookings"])

common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.get("/get_bookings/")
@router.get("/get_bookings/{id}")
async def get_bookings(id: int | None = None):
    try:
        logging.info("Starting get_bookings process")
        cursor = conn.cursor()
        if id:
            cursor.execute("select * from dm.get_bookings() where booking_id = %s;", (id,))
        else:
            cursor.execute("select * from dm.get_bookings();")
        result = cursor.fetchall()
        cursor.close()
        return {"bookings": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))