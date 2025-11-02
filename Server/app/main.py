from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"success": True, "message": "Welcome to the FastAPI application!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}