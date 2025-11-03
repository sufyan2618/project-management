from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserLogin, UserRegister
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.schemas.common import APIResponse
from app.services.email_service import EmailService
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.dependencies import get_current_user
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=APIResponse[UserResponse])
async def register_user(user: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(full_name=user.full_name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send welcome email in the background
    background_tasks.add_task(EmailService.send_welcome_email, email=user.email, user_name=user.full_name)

    return {
        "success": True,
        "data": UserResponse.model_validate(new_user),
        "message": "User registered successfully"
    }

@router.post("/login", response_model=APIResponse[UserResponse])
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=600)
    access_token = create_access_token(data={"user_id": db_user.id}, expires_delta=access_token_expires)
    return {
        "success": True,
        "data": UserResponse.model_validate(db_user),
        "message": "Login successful",
        "access_token": access_token,
    }

@router.get("/me", response_model=APIResponse[UserResponse])
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "data": UserResponse.model_validate(current_user)
    }

@router.post("/token")  # Standard OAuth2 endpoint
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """This endpoint is for Swagger UI authorization"""
    db = next(get_db())
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=600)
    access_token = create_access_token(
        data={"user_id": db_user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }