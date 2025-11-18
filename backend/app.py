import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
from .utils import process_idea

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# CORS (important for frontend → backend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- API ROUTES ----------
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

@app.post("/api/submit")
async def submit_idea(idea: Idea):
    try:
        result = await process_idea(idea.dict())
        return result
    except Exception as e:
        return {"status": "error", "step": "submit_idea", "error": str(e)}

@app.get("/api/test")
def test():
    return {"message": "API is working!"}

# ---------- STATIC FRONTEND ----------
# Serve frontend but DO NOT override /api routes
app.mount("/static", StaticFiles(directory="backend/frontend"), name="static")

@app.get("/")
async def root():
    """
    Serve index.html manually so /api does not get overwritten
    """
    index_path = "backend/frontend/index.html"
    return FileResponse(index_path)
