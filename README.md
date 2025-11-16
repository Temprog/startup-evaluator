# Startup Idea Evaluator

A simple web app to collect startup ideas, generate AI summaries, sentiment, and emojis, store them in Supabase, and notify staff via Discord.

## Features
- Submit idea via frontend form
- AI-generated summary & sentiment (Claude 3)
- Store submissions in Supabase
- Discord webhook notifications

## Setup
1. Copy `.env.example` to `.env` and fill in your keys:
2. Install backend dependencies:
3. Run locally:
uvicorn backend.app:app --reload --port 10000

4. Open browser at http://localhost:10000

5. 5. Deploy
- Push your project to GitHub.
- Create a new Web Service on Render.
- Connect your GitHub repo.
- Set environment variables (SUPABASE_URL, SUPABASE_KEY, DISCORD_WEBHOOK, ANTHROPIC_API_KEY) in Render.
- Start command: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
- Access your live app via the Render URL.


# Folder Structure
frontend/  - HTML/JS/CSS
backend/   - FastAPI backend + utils
.env       - environment variables

