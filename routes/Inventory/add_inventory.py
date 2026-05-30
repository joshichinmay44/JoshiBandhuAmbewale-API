from utils import common_util
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordBearer
import logging

router = APIRouter(prefix="/inventory", tags=["inventory"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


common_util=common_util.common_utilities()

conn = common_util.establish_connection_with_db()
conn.autocommit = True

@router.post("/add_inventory")
# async def add_inventory(sku_name : str = Body(), total_units: str =Body(), unit_cost_price: str = Body(), total_cost_price: str = Body(), description: str = Body(), vendor_name: str = Body()):
async def add_inventory(inventory_list: list[dict] = Body()):
    try:
        logging.info("Starting add_inventory process")
        cursor = conn.cursor()
        cursor.execute("SELECT max(batch_id) FROM dm.batch;")
        batch_id = cursor.fetchone() 
        if batch_id[0] is not None:
            batch_no = batch_id[0] +1
        else:
            batch_no = 1
        logging.info("Batch ID:", batch_no)
        for inventory in inventory_list:
            sku_name = inventory.get("sku_name")
            total_units = inventory.get("total_units")
            unit_cost_price = inventory.get("unit_cost_price")
            total_cost_price = inventory.get("total_cost_price")
            description = inventory.get("description")
            vendor_name = inventory.get("vendor_name")
            created_by = inventory.get("created_by")
            print("Received data:", sku_name, total_units, unit_cost_price, total_cost_price, description, vendor_name)
            cursor.execute("CALL dm.usp_add_new_batch(%s::BIGINT, %s::VARCHAR, %s::INT, %s::NUMERIC(19,4), %s::NUMERIC(19,4), %s::TEXT, %s::VARCHAR(200), %s::VARCHAR(100))", (batch_no, sku_name, total_units, unit_cost_price, total_cost_price, description, vendor_name, created_by))
        
        # if inventory_id:
        #     raise HTTPException(status_code=400, detail="Inventory for this SKU already exists")
        # cursor.execute("CALL dim.usp_add_inventory(%s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar, %s::varchar);", (sku_name, total_units, unit_cost_price, total_cost_price, description, vendor_name))
        cursor.close()
        return {"message": "Inventory added successfully", "status": "success"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))