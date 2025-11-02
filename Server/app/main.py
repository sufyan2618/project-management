from fastapi import FastAPI
from app.routers import auth
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"success": True, "message": "Welcome to the FastAPI application!"}


app.include_router(auth.router)
@app.get("/health")
def health_check():
    return {"status": "healthy"}