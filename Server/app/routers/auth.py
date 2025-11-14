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
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])
logger = get_logger(__name__)

@router.post("/register", response_model=APIResponse[UserResponse], response_model_exclude_none=True)
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: {user.email}")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Registration failed - email already exists: {user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    # Generate and send verification OTP
    otp = EmailService.generate_otp()
    otp_expiry = datetime.now(datetime.timezone.utc) + timedelta(minutes=5)
    current_time = datetime.now(datetime.timezone.utc)
    
    task = EmailService.send_verification_email.delay(
        email=user.email,
        first_name=user.first_name,
        otp=otp
    )

    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        otp=otp,
        otp_expiry=otp_expiry,
        email_attempts=1,
        last_email_attempt=current_time
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User registered successfully: {new_user.id} - {user.email}")

    return {
        "success": True,
        "data": UserResponse.model_validate(new_user),
        "message": "User registered successfully. Please check your email for verification code."
    }


@router.post("/verify-otp", response_model=APIResponse[UserResponse], response_model_exclude_none=True)
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    logger.info(f"OTP verification attempt for email: {email}")
    
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        logger.warning(f"OTP verification failed - user not found: {email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if db_user.is_verified:
        logger.info(f"OTP verification skipped - user already verified: {email}")
        return {
            "success": True,
            "data": UserResponse.model_validate(db_user),
            "message": "User already verified"
        }
    
    if db_user.otp != otp:
        logger.warning(f"OTP verification failed - invalid OTP for email: {email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    
    if db_user.otp_expiry < datetime.now(datetime.timezone.utc):
        logger.warning(f"OTP verification failed - OTP expired for email: {email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired")
    
    db_user.is_verified = True
    db_user.otp = None  # Clear OTP after successful verification
    db.commit()
    db.refresh(db_user)
    logger.info(f"OTP verified successfully for user: {db_user.id} - {email}")
    
    return {
        "success": True,
        "data": UserResponse.model_validate(db_user),
        "message": "OTP verified successfully"
    }




@router.post("/login", response_model=APIResponse[UserResponse])
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {user.email}")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        logger.warning(f"Failed login attempt for email: {user.email}")
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if db_user.login_attempts > 5:
        logger.warning(f"Account locked due to multiple failed login attempts: {user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account locked. Please signin again later.")


    if not verify_password(user.password, db_user.hashed_password):
        logger.warning(f"Wrong Password for email: {user.email}")
        db_user.login_attempts += 1
        db.commit()
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not db_user.is_verified:
        logger.warning(f"Failed login attempt - unverified email: {user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified") 

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

@router.post("/resend-otp", response_model=APIResponse[None])
def resend_otp(email: str, db: Session = Depends(get_db)):
    logger.info(f"Resend OTP request for email: {email}")
    
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        logger.warning(f"Resend OTP failed - user not found: {email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if db_user.is_verified:
        logger.info(f"Resend OTP skipped - user already verified: {email}")
        return {
            "success": True,
            "message": "User already verified"
        }
    
    # Check rate limiting for email sending
    current_time = datetime.now(datetime.timezone.utc)
    if db_user.last_email_attempt:
        time_since_last_attempt = (current_time - db_user.last_email_attempt).total_seconds()
        
        # If less than 1 minute since last attempt
        if time_since_last_attempt < 60:
            wait_time = int(60 - time_since_last_attempt)
            logger.warning(f"Email rate limit hit for user: {email}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Please wait {wait_time} seconds before requesting another OTP"
            )
        
        # Reset counter if more than 1 hour has passed
        if time_since_last_attempt > 3600:
            db_user.email_attempts = 0
    
    # Check if user has exceeded daily limit (5 emails per hour)
    if db_user.email_attempts >= 5:
        logger.warning(f"Daily email limit exceeded for user: {email}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many OTP requests. Please try again after 1 hour"
        )
    
    otp = EmailService.generate_otp()
    otp_expiry = datetime.now(datetime.timezone.utc) + timedelta(minutes=5)
    db_user.otp = otp
    db_user.otp_expiry = otp_expiry
    db_user.email_attempts += 1
    db_user.last_email_attempt = current_time
    db.commit()
    
    task = EmailService.send_verification_email.delay(
        email=db_user.email,
        first_name=db_user.first_name,
        otp=otp
    )
    
    logger.info(f"OTP resent successfully to email: {email}")
    
    return {
        "success": True,
        "message": "OTP resent successfully"
    }

@router.post("/forgot-password", response_model=APIResponse[None])
def forgot_password(email: str, db: Session = Depends(get_db)):
    logger.info(f"Forgot password request for email: {email}")
    
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        logger.warning(f"Forgot password failed - user not found: {email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Check rate limiting for email sending
    current_time = datetime.now(datetime.timezone.utc)
    if db_user.last_email_attempt:
        time_since_last_attempt = (current_time - db_user.last_email_attempt).total_seconds()
        
        # If less than 1 minute since last attempt
        if time_since_last_attempt < 60:
            wait_time = int(60 - time_since_last_attempt)
            logger.warning(f"Email rate limit hit for user: {email}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Please wait {wait_time} seconds before requesting another OTP"
            )
        
        # Reset counter if more than 1 hour has passed
        if time_since_last_attempt > 3600:
            db_user.email_attempts = 0
    
    # Check if user has exceeded daily limit (5 emails per hour)
    if db_user.email_attempts >= 5:
        logger.warning(f"Daily email limit exceeded for user: {email}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many password reset requests. Please try again after 1 hour"
        )
    
    otp = EmailService.generate_otp()
    otp_expiry = datetime.now(datetime.timezone.utc) + timedelta(minutes=10)
    db_user.otp = otp
    db_user.otp_expiry = otp_expiry
    db_user.email_attempts += 1
    db_user.last_email_attempt = current_time
    db.commit()
    
    task = EmailService.send_password_reset_email.delay(
        email=db_user.email,
        first_name=db_user.first_name,
        otp=otp
    )
    
    logger.info(f"Password reset OTP sent successfully to email: {email}")
    
    return {
        "success": True,
        "message": "Password reset OTP sent successfully"
    }
@router.post("/reset-password", response_model=APIResponse[None])
def reset_password(email: str, otp: str, new_password: str, db: Session = Depends(get_db)):
    logger.info(f"Reset password attempt for email: {email}")
    
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        logger.warning(f"Reset password failed - user not found: {email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if db_user.otp != otp:
        logger.warning(f"Reset password failed - invalid OTP for email: {email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    
    if db_user.otp_expiry < datetime.now(datetime.timezone.utc):
        logger.warning(f"Reset password failed - OTP expired for email: {email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired")
    
    db_user.hashed_password = hash_password(new_password)
    db_user.otp = None  # Clear OTP after successful password reset
    db_user.otp_expiry = None  # Clear OTP expiry after successful password reset
    db.commit()
    
    logger.info(f"Password reset successfully for user: {db_user.id} - {email}")
    
    return {
        "success": True,
        "message": "Password reset successfully"
    }