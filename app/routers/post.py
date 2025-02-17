from .. import models, schemas
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
import app.oauth2 as oauth2
from typing import Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

# Retrieve all posts from the database
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10,skip: int = 0, search: Optional[str] = ""):


    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# Retrieve all current users posts from the database
@router.get("/my", response_model=list[schemas.PostOut])
def get_my_posts(db: Session = Depends(get_db), current_user: any = Depends(oauth2.get_current_user)):
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    posts = db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).all()
    
    return posts

# Adding a single post from the database
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    new_post = models.Post(owner_id =current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Retrieve a single post from the database
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id {id} not found"}
    return post


# Update a single post in the database
@router.put("/{id}", response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)
    if post_to_update.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post_to_update.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
    post_to_update.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_to_update.first()

# Delete a single post from the database
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}




# {
#         "title": "aaa",
#         "content": "is is a new post",
#         "published": true,
#         "id": 7,
#         "created_at": "2025-02-13T17:42:13.291078+09:00",
#         "owner_id": 3,
#         "owner": {
#             "id": 3,
#             "email": "user4@gmail.com",
#             "created_at": "2025-01-31T16:50:23.317759+09:00"
#         }
#     }

# {
#         "Post": {
#             "published": true,
#             "owner_id": 6,
#             "title": "New Post 12",
#             "content": "is is a new post",
#             "id": 10,
#             "created_at": "2025-02-13T18:15:18.989845+09:00"
#         },
#         "votes": 1
#     }