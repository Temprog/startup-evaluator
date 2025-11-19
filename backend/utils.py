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
    1. Call Anthropic Claude API
    2. Save to Supabase
    3. Notify Discord (optional)
    """

    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # 1️⃣ Call Anthropic Claude API
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "claude-sonnet-4-5-20250929",
                    "max_tokens": 4096,
                    "temperature": 0.7,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Analyze this startup idea:\n{json.dumps(data)}"
                        }
                    ]
                }
            )
            ai_result = response.json()
            if "content" in ai_result and len(ai_result["content"]) > 0:
                ai_summary = ai_result["content"][0].get("text", "")
            else:
                ai_summary = "No response from AI."

    except Exception as e:
        return {"status": "error", "step": "AI", "error": str(e), "anthropic_raw_response": ai_result}

    # 2️⃣ Save to Supabase
    try:
        supabase.table("ideas").insert({
            "name": data.get("name", ""),
            "title": data.get("title", ""),
            "feedback": data.get("feedback", ""),
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
                    "content": f"New idea submitted:\n**{data.get('title','')}** by **{data.get('name','')}**"
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
