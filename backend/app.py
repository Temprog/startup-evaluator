import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import process_idea

# Load environment variables automatically in Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Create FastAPI app
app = FastAPI()

# CORS middleware for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for idea submission
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

# POST route for form submissions
@app.post("/api/submit")
async def submit_idea(idea: Idea):
    result = await process_idea(idea.dict())
    return result

# Serve frontend at root
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
