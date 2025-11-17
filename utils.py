import os
import json
import httpx
from supabase import create_client, Client

# Environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def process_idea(data: dict):
    """
    Process a startup idea:
    1. Call AI (Claude 3)
    2. Save to Supabase
    3. Notify Discord (optional)
    """

    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # 1️⃣ Call Claude 3
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
            ai_summary = ai_result.get("completion", "")  # ✅ fixed
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

    # 3️⃣ Notify Discord webhook (optional)
    if DISCORD_WEBHOOK:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(DISCORD_WEBHOOK, json={
                    "content": f"New idea submitted:\n**{data['title']}** by **{data['name']}**"
                })
        except Exception as e:
            return {"status": "error", "step": "Discord webhook", "error": str(e)}

    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }
