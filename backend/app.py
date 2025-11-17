import os
import json
import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
from utils import process_idea  # Make sure utils.py is corrected

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create FastAPI app
app = FastAPI()

# Serve frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# Define request schema
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

@app.post("/api/submit")
async def submit_idea(idea: Idea):
    # Call the corrected process_idea function from utils.py
    result = await process_idea(idea.dict())
    return result
