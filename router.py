# main.py
from fastapi import FastAPI
from routes import authenticator
from routes import add_customer
from routes import get_customers

app = FastAPI()

# Register the routes from other files
app.include_router(authenticator.router)
app.include_router(add_customer.router)
app.include_router(get_customers.router)
@app.get("/")
def home():
    return {"message": "Main API Hub"}
