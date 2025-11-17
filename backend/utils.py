import os
import json
import httpx
from supabase import create_client, Client

# Environment variables
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def process_idea(data):
    # Example AI call (Anthropic)
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
        ai_result = resp.json()  # extract AI result

    # Example placeholders for AI-extracted fields
    ai_summary = ai_result.get("completion", "")
    ai_sentiment = "neutral"
    ai_sentiment_emoji = "😐"
    ai_idea_emoji = "💡"

    # Save to Supabase
    supabase.table("ideas").insert({
        "name": data["name"],
        "title": data["title"],
        "feedback": data["feedback"],
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment_emoji,
        "ai_idea_emoji": ai_idea_emoji
    }).execute()

    # ✅ Correct async Discord webhook call
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK, json={
            "content": f"New idea submitted:\n**{data['title']}** by **{data['name']}**"
        })

    return {"status": "success", "ai_result": ai_result}
