from fastapi import FastAPI
from app.routers import auth, projects, task
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base



app = FastAPI()

@app.get("/")
def read_root():
    return {"success": True, "message": "Welcome to the FastAPI application!"}


app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(task.router)
@app.get("/health")
def health_check():
    return {"status": "healthy"}