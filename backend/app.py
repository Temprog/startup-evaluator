import os
import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
from utils import process_idea  # make sure utils.py is in backend/

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create FastAPI app
app = FastAPI()

# Mount frontend static files
# Adjust path if frontend is outside backend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# Define request schema
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

# API route
@app.post("/submit")
async def submit_idea(idea: Idea):
    try:
        # Call your utils.py function
        result = await process_idea(idea.dict())
        return result
    except Exception as e:
        return {"status": "error", "step": "submit_idea", "error": str(e)}
