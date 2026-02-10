from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate,PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {"title": "New Post", "content": "cool test post"},
    2: {"title": "Morning Routine", "content": "Just finished a 5-mile run and a heavy breakfast. Feeling energized!"},
    3: {"title": "Tech Review", "content": "The new ergonomic keyboard is a game changer for long coding sessions."},
    4: {"title": "Quick Recipe", "content": "Mix avocado, lime, and salt. Best dip ever. #simpleeats"},
    5: {"title": "Travel Log", "content": "Arrived in Kyoto. The temples are even more breathtaking in person."},
    6: {"title": "Daily Quote", "content": "Consistency is more important than perfection. Keep going!"},
    7: {"title": "Bug Report", "content": "Noticed a lag in the UI when clicking the submit button on mobile."},
    8: {"title": "Movie Night", "content": "Finally watched that classic sci-fi film. The ending was mind-blowing."},
    9: {"title": "Gardening Tip", "content": "Don't overwater your succulents; they prefer dry soil between soakings."},
    10: {"title": "Project Update", "content": "Beta testing starts Monday! Can't wait for everyone to see the new features."},
    11: {"title": "Coffee Thoughts", "content": "Is it really a Monday if you haven't had at least three espressos?"}
}

@app.get("/hello-world")
def hello_world():
    return {"message": "Hello World"} # -> JSON JavaScript Object Notation

@app.get("/posts")
def get_all_post(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="post not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title":post.title,"content":post.content}
    text_posts[max(text_posts.keys())+1] = new_post
    return new_post
