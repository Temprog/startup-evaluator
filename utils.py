import os
import json
import httpx
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def process_idea(data: dict):
    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # -------------------------------
    # 1️⃣ AI CALL (Anthropic Claude 3)
    # -------------------------------
    try:
        prompt = (
            "Analyze the following startup idea. "
            "Return JSON with two fields: 'summary' and 'sentiment' "
            "(sentiment = positive, neutral, or negative). "
            f"\nIdea:\n{json.dumps(data)}"
        )

        headers = {
            "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json={
                    "model": "claude-3-opus-20240229",
                    "max_tokens": 300,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )

        ai_result = resp.json()
        text = ai_result["content"][0]["text"]

        # Extract summary + sentiment safely
        ai_summary = text

        if "positive" in text.lower():
            ai_sentiment = "positive"
            ai_sentiment_emoji = "😊"
        elif "negative" in text.lower():
            ai_sentiment = "negative"
            ai_sentiment_emoji = "😞"
        else:
            ai_sentiment = "neutral"
            ai_sentiment_emoji = "😐"

    except Exception as e:
        return {"status": "error", "step": "AI", "error": str(e)}

    # ------------------------------------
    # 2️⃣ SAVE TO SUPABASE
    # ------------------------------------
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
        return {"status": "error", "step": "supabase", "error": str(e)}

    # ------------------------------------
    # 3️⃣ DISCORD NOTIFICATION
    # (Correct async — FIXED)
    # ------------------------------------
    try:
        if DISCORD_WEBHOOK:
            async with httpx.AsyncClient() as client:
                await client.post(DISCORD_WEBHOOK, json={
                    "content": f"💡 New Idea Submitted!\n**{data['title']}** by **{data['name']}**"
                })
    except Exception as e:
        # Discord error should NOT break the app
        print("Discord webhook failed:", e)

    # ------------------------------------
    # 4️⃣ RETURN DATA
    # ------------------------------------
    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }
