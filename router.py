# main.py
from fastapi import FastAPI
from routes import authenticator  # Import your other files

app = FastAPI()

# Register the routes from other files
app.include_router(authenticator.router)

@app.get("/")
def home():
    return {"message": "Main API Hub"}
