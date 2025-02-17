from typing import Optional
from pydantic import BaseModel
from datetime import datetime 
from pydantic import EmailStr
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

# Create a Pydantic model for the Post

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class ResponsePost(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUser
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: ResponsePost
    votes: int
    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]  # 1 for like, 0 for dislike






class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

