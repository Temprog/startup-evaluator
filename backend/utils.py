supabase.table("ideas").insert({
    "name": data["name"],
    "role": data.get("role", ""),
    "title": data["title"],
    "feedback": data["feedback"],
    "ai_summary": ai_summary,
    "ai_sentiment": ai_sentiment,
    "ai_sentiment_emoji": ai_sentiment_emoji,
    "ai_idea_emoji": ai_idea_emoji
}).execute()
