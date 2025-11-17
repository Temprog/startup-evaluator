import os
import json
import httpx
from supabase import create_client, Client

# Environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Validate environment variables
assert SUPABASE_URL and SUPABASE_KEY and DISCORD_WEBHOOK and ANTHROPIC_API_KEY, "Missing required environment variables"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def process_idea(data):
    """
    Process a new startup idea:
    - Call AI for summary
    - Save to Supabase
    - Notify Discord webhook
    Returns JSON with status and AI result or error info.
    """
    ai_result = {}

    # 1️⃣ Call AI (Anthropic Claude 3 Messages API)
    try:
        prompt = f"Analyze this startup idea:\n{json.dumps(data)}"
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-opus-20240229",  # or claude-3-sonnet, etc.
            "max_tokens": 300,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            resp.raise_for_status()
            ai_result = resp.json()
    except Exception as e:
        return {"status": "error", "step": "AI call", "error": str(e)}

    # 2️⃣ Extract AI response
    try:
        ai_summary = ai_result.get("content", [{}])[0].get("text", "")
    except Exception:
        ai_summary = ""

    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"

    # 3️⃣ Save to Supabase
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

    # 4️⃣ Notify Discord webhook
    try:
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_WEBHOOK, json={
                "content": f"New idea submitted:\n**{data['title']}** by **{data['name']}**"
            })
    except Exception as e:
        return {"status": "error", "step": "Discord webhook", "error": str(e)}

    # ✅ All done
    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }