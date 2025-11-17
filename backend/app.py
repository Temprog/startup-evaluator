from dotenv import load_dotenv
load_dotenv()  # Loads .env locally or from Render environment

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import process_idea  # Our corrected utils.py

app = FastAPI()  # Top-level 'app' required by uvicorn

# CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for form submission
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

# POST route to process ideas
@app.post("/api/submit")
async def submit_idea(idea: Idea):
    """
    Receives a new idea, processes it asynchronously (AI, Supabase, Discord)
    and returns a JSON response with the results or errors.
    """
    return await process_idea(idea.dict())

# Serve frontend at root
# Update this path depending on where your frontend is located relative to app.py
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
