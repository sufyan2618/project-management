from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.core.logger import get_logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
logger = get_logger(__name__)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token) 
    if payload is None:
        logger.warning("Invalid token - could not decode")
        raise credentials_exception
    user_id: int = payload.get("user_id")
    if user_id is None:
        logger.warning("Invalid token - missing user_id")
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.warning(f"User not found for token with user_id: {user_id}")
        raise credentials_exception
    
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        logger.info(f"Checking roles for user {current_user.id} with role {current_user.role} against allowed roles: {self.allowed_roles}")
        if current_user.role not in self.allowed_roles:
            logger.warning(f"User {current_user.id} with role {current_user.role} denied access - required roles: {self.allowed_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
        return current_user