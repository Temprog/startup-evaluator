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
    1️⃣ Call Anthropic Claude 3.5 API
    2️⃣ Extract summary and sentiment
    3️⃣ Save to Supabase
    4️⃣ Optional: Notify Discord webhook
    """

    ai_summary = ""
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"
    ai_result = {}

    # 1️⃣ Call Anthropic API
    try:
        prompt = f"Analyze this startup idea:\n{json.dumps(data)}"

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
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
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            ai_result = resp.json()

            # Extract AI summary safely
            if "content" in ai_result and len(ai_result["content"]) > 0:
                ai_summary = ai_result["content"][0].get("text", "No response from AI.")
            else:
                ai_summary = "No response from AI."

    except Exception as e:
        return {"status": "error", "step": "AI", "error": str(e)}

    # 2️⃣ Optional: Simple sentiment detection based on keywords
    sentiment_lower = ai_summary.lower()
    if any(word in sentiment_lower for word in ["good", "great", "positive", "excellent"]):
        ai_sentiment = "positive"
        ai_sentiment_emoji = "🔥"
    elif any(word in sentiment_lower for word in ["bad", "poor", "negative", "fail"]):
        ai_sentiment = "negative"
        ai_sentiment_emoji = "⚠️"
    else:
        ai_sentiment = "neutral"
        ai_sentiment_emoji = "😐"

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

    # 4️⃣ Optional: Discord webhook notification
    if DISCORD_WEBHOOK:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(DISCORD_WEBHOOK, json={
                    "content": f"New idea submitted:\n**{data['title']}** by **{data['name']}**"
                })
        except Exception as e:
            return {"status": "error", "step": "Discord webhook", "error": str(e)}

    # ✅ Return structured response
    return {
        "status": "success",
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji,
        "ai_result": ai_result
    }
