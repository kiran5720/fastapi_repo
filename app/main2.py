 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user,auth,vote
from .config import settings

# models.Base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello byddy go learn from mistakeeeeeeee!"}

@app.get("/to_see_git")
async def root2():
    return {"message": "Hello byddy i changed something new in code!1!"}

origins = ['https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


