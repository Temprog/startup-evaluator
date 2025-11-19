document.getElementById("ideaForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = Object.fromEntries(new FormData(e.target));

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "Processing...";

  try {
    const res = await fetch("/api/submit", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });

    if (!res.ok) {
      throw new Error(`Backend error: ${await res.text()}`);
    }

    const json = await res.json();

    if(json.status !== "success") {
      resultDiv.innerHTML = `<p style="color:red;">Error: ${json.error || "Unknown error"}</p>`;
      return;
    }

    // Display nicely
    resultDiv.innerHTML = `
      <h2>${json.ai_idea_emoji} ${data.title}</h2>
      <p><strong>Your Name:</strong> ${data.name}</p>
      <p><strong>Your Role / Background:</strong> ${data.role}</p>
      <p><strong>AI Sentiment:</strong> ${json.ai_sentiment_emoji} (${json.ai_sentiment})</p>
      <div>${json.ai_summary.replace(/\n/g, "<br>")}</div>
    `;

    e.target.reset();

  } catch (err) {
    console.error(err);
    resultDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
  }
});
