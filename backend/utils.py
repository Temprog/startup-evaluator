import os
import json
import httpx
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def process_idea(data: dict):

    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # 1️⃣ Correct Anthropic Messages API
    try:
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-3-5-sonnet-latest",
            "max_tokens": 300,
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze this startup idea: {json.dumps(data)}.\n"
                               f"Return a short summary only."
                }
            ]
        }

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )

        ai_result = resp.json()

        # Extract text safely
        ai_summary = ai_result["content"][0]["text"]

    except Exception as e:
        return {"status": "error", "step": "AI", "error": str(e)}

    # 2️⃣ Save to Supabase
    try:
        supabase.table("ideas").insert({
            "name": data["name"],
            "title": data["title"],
            "feedback": data["feedback"],
            "ai_summary": ai_summary,
            "ai_sentiment": ai_sentiment,
            "ai_sentiment_emoji": ai_sentiment_emoji,
            "ai_idea_emoji": ai_idea_emoji
        }).execute()

    except Exception as e:
        return {"status": "error", "step": "Supabase insert", "error": str(e)}

    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }