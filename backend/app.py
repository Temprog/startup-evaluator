from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import process_idea  # utils.py must be at repo root

# 1️⃣ Create FastAPI instance
app = FastAPI()  # Must be top-level 'app'

# 2️⃣ Add CORS middleware for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Define Pydantic model for POST data
class Idea(BaseModel):
    name: str
    title: str
    feedback: str

# 4️⃣ Define API POST route
@app.post("/api/submit")
async def submit_idea(idea: Idea):
    return await process_idea(idea.dict())

# 5️⃣ Serve frontend at root
# 'app.py' is in backend/, frontend is in repo root, so use ../frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
