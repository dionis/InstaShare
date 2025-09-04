from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.base import get_db
from auth.jwt import verify_access_token
from models.user import User as UserModel
from schemas.user import User as UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(UserModel).filter(UserModel.email == token_data.username).first()
    print(f"User ==>: {user}")
    if user is None:
        raise credentials_exception
    return UserSchema.from_orm(user)


