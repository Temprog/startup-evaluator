import os
import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
from utils import process_idea  # utils.py is in the same folder as app.py

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI
app = FastAPI()

# Mount frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Define request schema
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

# Endpoint to submit ideas
@app.post("/submit")
async def submit_idea(idea: Idea):
    """
    Process a new startup idea using utils.process_idea().
    Returns a JSON response with status and AI result.
    """
    try:
        result = await process_idea(idea.dict())
        return result
    except Exception as e:
        return {"status": "error", "step": "submit_idea", "error": str(e)}
