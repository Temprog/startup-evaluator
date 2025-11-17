from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import process_idea

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Idea(BaseModel):
    name: str
    title: str
    feedback: str

@app.post("/api/submit")
async def submit_idea(idea: Idea):
    return await process_idea(idea.dict())

# ✅ Correct StaticFiles mount
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
