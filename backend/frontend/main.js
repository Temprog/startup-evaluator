document.getElementById("ideaForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "<p>Processing...</p>";

    try {
        const res = await fetch("/api/submit", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if(result.status === "success") {
            resultDiv.innerHTML = `
                <h2>${result.ai_idea_emoji} ${data.title}</h2>
                <p><strong>Submitted by:</strong> ${data.name}</p>
                <p><strong>Feedback / Idea:</strong> ${data.feedback}</p>
                <p><strong>AI Sentiment:</strong> ${result.ai_sentiment_emoji} ${result.ai_sentiment}</p>
                <pre>${result.ai_summary}</pre>
            `;
        } else {
            resultDiv.innerHTML = `<p style="color:red;">Error: ${result.error || 'Unknown error'}</p>`;
        }

        e.target.reset();

    } catch (err) {
        resultDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    }
});
