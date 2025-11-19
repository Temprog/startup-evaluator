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
    1. Call Claude 3.5 Sonnet (Anthropic messages API)
    2. Save to Supabase
    3. Optional: notify Discord
    """

    ai_summary = "No summary"
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # ------------------------
    # 1️⃣ Call Anthropic API
    # ------------------------
    try:
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 300,
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze this startup idea:\n{json.dumps(data)}"
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

        # Debug error case
        if "content" not in ai_result:
            return {
                "status": "error",
                "step": "AI",
                "error": "Anthropic did not return 'content'",
                "anthropic_raw_response": ai_result
            }

        ai_summary = ai_result["content"][0]["text"]

    except Exception as e:
        return {
            "status": "error",
            "step": "AI exception",
            "error": str(e)
        }

    # ------------------------
    # 2️⃣ Save to Supabase
    # ------------------------
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
        return {
            "status": "error",
            "step": "Supabase insert",
            "error": str(e)
        }

    # ------------------------
    # 3️⃣ Optional Discord
    # ------------------------
    if DISCORD_WEBHOOK:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    DISCORD_WEBHOOK,
                    json={
                        "content": f"New idea: **{data['title']}** from **{data['name']}**"
                    }
                )
        except Exception as e:
            return {
                "status": "error",
                "step": "Discord",
                "error": str(e)
            }

    # ------------------------
    # DONE
    # ------------------------
    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }
