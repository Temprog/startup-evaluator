import os
import json
import httpx
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def process_idea(data: dict):
    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"

    # 1️⃣ Call AI
    try:
        prompt = f"Analyze this startup idea:\n{json.dumps(data)}"
        headers = {"Authorization": f"Bearer {ANTHROPIC_API_KEY}"}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/complete",
                headers=headers,
                json={
                    "model": "claude-3",
                    "prompt": prompt,
                    "max_tokens_to_sample": 300
                }
            )
            ai_result = resp.json()
            ai_summary = ai_result.get("completion", "")
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

    # ✅ Success
    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }
