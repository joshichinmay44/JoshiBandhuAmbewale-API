# main.py
from fastapi import FastAPI
from routes.Admin import authenticator
from routes.Customer import add_customer
from routes.Customer import get_customers
from routes.Customer import update_customer
from routes.Admin import add_user
from routes.GenericAPIs import get_pin_codes
from routes.Vendor import add_vendor
from routes.Vendor import get_vendors
from routes.Vendor import update_vendor
from routes.SKU import add_sku
from routes.SKU import get_skus
from routes.SKU import update_sku
from routes.Inventory import add_inventory
from routes.Inventory import get_current_inventory
from routes.Sales import add_booking

app = FastAPI()

# Register the routes from other files
app.include_router(authenticator.router)
app.include_router(add_customer.router)
app.include_router(get_customers.router)
app.include_router(update_customer.router)
app.include_router(add_user.router)
app.include_router(get_pin_codes.router)
app.include_router(add_vendor.router)
app.include_router(get_vendors.router)
app.include_router(update_vendor.router)
app.include_router(add_sku.router)
app.include_router(get_skus.router)
app.include_router(update_sku.router)
app.include_router(add_inventory.router)
app.include_router(get_current_inventory.router)
app.include_router(add_booking.router)

@app.get("/")
def home():
    return {"message": "Main API Hub"}
