# Startup Idea Evaluator
A web app that takes submitted startup ideas and uses Claude to prepare a structured assessment for each one, stores the results in Supabase and alerts staff on Discord. Staff make the final decision; the app gives them a first-pass summary and score so they can review ideas faster.


## Features
- Submit idea via frontend form
- AI-generated summary & sentiment (Claude 3)
- Store submissions in Supabase
- Discord webhook notifications
- 
- Idea submission through a frontend form
- AI-generated summary of each idea
- Refined version of the idea, rewritten more clearly
- Relevance score against a target competition or goal
- Areas for improvement and a feasibility assessment
- Sentiment analysis and an **emoji tag
- Storage of every submission and result in Supabase
- Discord webhook notifications to staff

## How it works
1. A user submits an idea through the frontend form.
2. The FastAPI backend sends it to Claude (Claude 3) with a [rubric-based prompt / N separate prompts: say which] that asks for a structured assessment.
3. The structured output is validated and stored in Supabase.
4. A Discord webhook notifies staff with the summary and score.
5. A staff member reviews the output and makes the final decision.

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
- frontend/  - HTML/JS/CSS
- backend/   - FastAPI backend + utils
- .env       - environment variables

