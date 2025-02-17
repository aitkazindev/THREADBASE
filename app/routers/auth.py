from fastapi  import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import oauth2
from .. import database, models, utils

router = APIRouter(
    tags=["Authentications"],
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    # generate jwt token
    acsess_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"token": acsess_token, "token_type": "bearer"}

