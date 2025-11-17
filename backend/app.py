import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from utils import process_idea  # make sure this is your fixed utils.py

# Load environment variables
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")  # optional
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Create FastAPI app
app = FastAPI()

# Define the request schema
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

@app.post("/api/submit")
async def submit_idea(idea: Idea):
    """
    Receives a startup idea, processes with AI, stores in Supabase,
    optionally sends Discord notification.
    """
    result = await process_idea(idea.dict())
    return result
