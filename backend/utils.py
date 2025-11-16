import os, httpx, json

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

async def process_idea(data):
    prompt = f"Analyze this startup idea:\n{json.dumps(data)}"
    headers = {"Authorization": f"Bearer {ANTHROPIC_API_KEY}"}
    
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/complete",
            headers=headers,
            json={"model": "claude-3", "prompt": prompt, "max_tokens_to_sample": 300}
        )
        ai_result = resp.json()

    # Save to Supabase
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{SUPABASE_URL}/rest/v1/ideas",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "name": data["name"],
                "title": data["title"],
                "feedback": data["feedback"],
                "ai_summary": ai_result.get("completion"),
                "ai_sentiment": "neutral",
                "ai_sentiment_emoji": "😐",
                "ai_idea_emoji": "💡"
            }
        )

    # Send Discord webhook
    await httpx.post(DISCORD_WEBHOOK, json={"content": f"New idea: {data['title']} by {data['name']}"})

    return {"status": "success", "ai_result": ai_result}
