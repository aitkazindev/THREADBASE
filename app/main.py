from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

#  Create the database tables
#models.Base.metadata.create_all(bind=engine) replaces by alembic

#  Create a FastAPI instance
app = FastAPI()

origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def read_root():
    return {"Text": " Hello World"}


