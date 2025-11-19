headers = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

payload = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 300,
    "messages": [
        {
            "role": "user",
            "content": f"Analyze this startup idea:\n{json.dumps(data)}\nReturn a short summary."
        }
    ]
}

async with httpx.AsyncClient(timeout=30) as client:
    resp = await client.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload
    )

ai_result = resp.json()

if "content" not in ai_result:
    return {
        "status": "error",
        "step": "AI",
        "error": "Anthropic returned no 'content'",
        "anthropic_raw_response": ai_result
    }

ai_summary = ai_result["content"][0]["text"]