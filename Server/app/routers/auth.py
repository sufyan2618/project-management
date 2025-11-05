from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserLogin, UserRegister
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.schemas.common import APIResponse
from app.services.email_service import EmailService
from app.core.logger import get_logger
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.dependencies import get_current_user
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])
logger = get_logger(__name__)

@router.post("/register", response_model=APIResponse[UserResponse], response_model_exclude_none=True)
async def register_user(user: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: {user.email}")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Registration failed - email already exists: {user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(full_name=user.full_name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User registered successfully: {new_user.id} - {user.email}")

    background_tasks.add_task(EmailService.send_welcome_email, email=user.email, user_name=user.full_name)

    return {
        "success": True,
        "data": UserResponse.model_validate(new_user),
        "message": "User registered successfully"
    }

@router.post("/login", response_model=APIResponse[UserResponse])
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {user.email}")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logger.warning(f"Failed login attempt for email: {user.email}")
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=600)
    access_token = create_access_token(data={"user_id": db_user.id}, expires_delta=access_token_expires)
    
    logger.info(f"User logged in successfully: {db_user.id} - {user.email}")
    
    return {
        "success": True,
        "data": UserResponse.model_validate(db_user),
        "message": "Login successful",
        "access_token": access_token,
    }

@router.get("/me", response_model=APIResponse[UserResponse], response_model_exclude_none=True)
def read_current_user(current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.id} fetching their profile")
    
    return {
        "success": True,
        "data": UserResponse.model_validate(current_user)
    }

@router.get("/users", response_model=APIResponse[list[UserResponse]], response_model_exclude_none=True)
def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.id} fetching all users")
    
    users = db.query(User).filter(User.is_active == True).all()
    
    return {
        "success": True,
        "data": [UserResponse.model_validate(user) for user in users],
        "message": "Users fetched successfully"
    }

@router.post("/token")
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    logger.info(f"Swagger OAuth2 login attempt for: {form_data.username}")
    
    db = next(get_db())
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        logger.warning(f"Failed Swagger OAuth2 login for: {form_data.username}")
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
    
    logger.info(f"Swagger OAuth2 login successful for user: {db_user.id}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# TEMPORARY ENDPOINT - Remove after creating first admin
@router.post("/make-first-admin")
def make_first_admin(db: Session = Depends(get_db)):
    """
    Temporary endpoint to make the first registered user an admin.
    This endpoint will only work if there are no admins yet.
    DELETE THIS ENDPOINT after creating your first admin!
    """
    logger.info("Attempting to create first admin user")
    
    # Check if any admin exists
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        logger.warning("Admin already exists, rejecting request")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin user already exists. This endpoint is disabled."
        )
    
    # Get the first user (oldest by created_at)
    first_user = db.query(User).order_by(User.created_at).first()
    
    if not first_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found. Please register first."
        )
    
    # Make them admin
    first_user.role = "admin"
    db.commit()
    db.refresh(first_user)
    
    logger.info(f"First admin created: {first_user.email}")
    
    return {
        "success": True,
        "message": f"User {first_user.email} is now an admin!",
        "data": UserResponse.model_validate(first_user)
    }