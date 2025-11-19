import os
import json
import httpx
from supabase import create_client, Client

# Env vars
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def process_idea(data: dict):

    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # 1️⃣ Anthropic Claude 3.5 API CALL (FULLY CORRECT)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "claude-3-5-sonnet-latest",
                    "max_tokens": 300,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Analyze this startup idea:\n{json.dumps(data)}"
                        }
                    ]
                }
            )

            ai_result = resp.json()

            # extract text safely
            if "content" in ai_result and len(ai_result["content"]) > 0:
                ai_summary = ai_result["content"][0].get("text", "")
            else:
                ai_summary = "No response from AI."

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

    # 3️⃣ Discord webhook (optional)
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
