# main.py
from fastapi import FastAPI
from routes import authenticator
from routes import add_customer
from routes import get_customers
from routes import update_customer
from routes import add_user
from routes import get_pin_codes
from routes import add_vendor

app = FastAPI()

# Register the routes from other files
app.include_router(authenticator.router)
app.include_router(add_customer.router)
app.include_router(get_customers.router)
app.include_router(update_customer.router)
app.include_router(add_user.router)
app.include_router(get_pin_codes.router)
app.include_router(add_vendor.router)

@app.get("/")
def home():
    return {"message": "Main API Hub"}
