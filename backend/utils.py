import os
import json
import httpx
from supabase import create_client, Client

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def process_idea(data: dict):
    """
    Process a startup idea:
    1. Send the idea to Anthropic Claude
    2. Save result in Supabase
    3. Optionally send a Discord notification
    """

    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # ------------------------------------------------------------
    # 1️⃣ Step 1 — Call Anthropic Claude (correct API format)
    # ------------------------------------------------------------
    try:
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "claude-3-5-sonnet-latest",   # ✅ Correct model
            "max_tokens": 300,                   # Claude expects max_tokens, not max_tokens_to_sample
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze this startup idea:\n{json.dumps(data)}"
                }
            ]
        }

        async with httpx.AsyncClient(timeout=40) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            ai_result = response.json()

        # Claude returns: content: [{ "type": "text", "text": "..."}]
        content_blocks = ai_result.get("content", [])

        if content_blocks and "text" in content_blocks[0]:
            ai_summary = content_blocks[0]["text"]
        else:
            raise ValueError("Anthropic did not return a text response")

    except Exception as e:
        return {
            "status": "error",
            "step": "AI",
            "error": str(e),
            "anthropic_raw_response": ai_result
        }

    # ------------------------------------------------------------
    # 2️⃣ Step 2 — Save to Supabase
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # 3️⃣ Step 3 — Optional Discord Notification
    # ------------------------------------------------------------
    if DISCORD_WEBHOOK:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(DISCORD_WEBHOOK, json={
                    "content": f"🆕 New startup idea submitted:\n**{data['title']}** by **{data['name']}**"
                })
        except Exception as e:
            return {
                "status": "error",
                "step": "Discord webhook",
                "error": str(e)
            }

    # ------------------------------------------------------------
    # 4️⃣ Step 4 — Success Response
    # ------------------------------------------------------------
    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }
