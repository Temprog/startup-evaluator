from dotenv import load_dotenv
load_dotenv()  # ← loads .env from project root for local dev

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from utils import process_idea

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend (relative path)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")

class Idea(BaseModel):
    name: str
    title: str
    feedback: str

@app.post("/api/submit")
async def submit_idea(idea: Idea):
    return await process_idea(idea.dict())
