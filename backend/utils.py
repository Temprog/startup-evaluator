    # 1️⃣ Anthropic Claude 3.5 API CALL (FULLY CORRECT)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "claude-3-5-sonnet-latest",  # Check for this model
                    "max_tokens": 300,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Analyze this startup idea:\n{json.dumps(data)}"
                        }
                    ]
                }
            )

            ai_result = resp.json()

            if "error" in ai_result:
                return {"status": "error", "step": "AI", "error": ai_result["error"]}
            
            if len(ai_result["content"]) > 0:
                ai_summary = ai_result["content"][0].get("text", "")
            else:
                ai_summary = "No response from AI."

    except Exception as e:
        return {"status": "error", "step": "AI", "error": str(e)}