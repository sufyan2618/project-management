from fastapi import FastAPI
from app.routers import auth, projects, task
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import socketio
from app.core.socket import sio



app = FastAPI()
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

#apply cors middleware for frontend route

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL] if isinstance(settings.CLIENT_URL, str) else settings.CLIENT_URL,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"success": True, "message": "Welcome to the FastAPI application!"}


app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(task.router)
@app.get("/health")
def health_check():
    return {"status": "healthy"}