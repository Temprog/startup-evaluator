from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import process_idea

app = FastAPI()  # Must be top-level 'app'

# CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

# POST route
@app.post("/api/submit")
async def submit_idea(idea: Idea):
    return await process_idea(idea.dict())

# Serve frontend at root
app.mount("/", StaticFiles(directory="backend/frontend", html=True), name="static")
