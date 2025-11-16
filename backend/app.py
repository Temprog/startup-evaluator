import httpx
from anthropic import Anthropic

async def process_idea(data):
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # Generate AI summary
    summary_prompt = f"Summarize this idea: {data['feedback']}"
    sentiment_prompt = f"Provide overall sentiment (positive, neutral, negative) and an emoji: {data['feedback']}"
    idea_emoji_prompt = f"Give one emoji that represents this idea: {data['title']}"

    ai_summary = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=150,
        messages=[{"role": "user", "content": summary_prompt}],
    ).content[0].text

    ai_sentiment = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=50,
        messages=[{"role": "user", "content": sentiment_prompt}],
    ).content[0].text

    ai_idea_emoji = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=5,
        messages=[{"role": "user", "content": idea_emoji_prompt}],
    ).content[0].text

    # Save to Supabase
    supabase.table("ideas").insert({
        "name": data["name"],
        "title": data["title"],
        "feedback": data["feedback"],
        "ai_summary": ai_summary,
        "ai_sentiment": ai_sentiment,
        "ai_sentiment_emoji": ai_sentiment,
        "ai_idea_emoji": ai_idea_emoji
    }).execute()

    # Discord webhook
    async with httpx.AsyncClient() as client_http:
        await client_http.post(DISCORD_WEBHOOK, json={
            "content": f"New idea submitted:\n**{data['title']}** by **{data['name']}**"
        })

    return {
        "summary": ai_summary,
        "sentiment": ai_sentiment,
        "emoji": ai_idea_emoji
    }
