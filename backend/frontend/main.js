document.getElementById("ideaForm").addEventListener("submit", async (e) => { 
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "<p>Processing your idea...</p>";

  try {
    const res = await fetch("/api/submit", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });

    const result = await res.json();

    if(result.status !== "success") {
      resultDiv.innerHTML = `<p style="color:red;">Error at step: ${result.step} - ${result.error}</p>`;
      return;
    }

    // Render nicely formatted HTML
    resultDiv.innerHTML = `
      <h2>${result.ai_idea_emoji} ${data.title}</h2>
      <p>Submitted by: <strong>${data.name}</strong></p>
      <p>Sentiment: ${result.ai_sentiment_emoji} ${result.ai_sentiment}</p>
      <div class="ai-summary">${result.ai_summary.replace(/\n/g, "<br>")}</div>
    `;

    // Scroll to result
    resultDiv.scrollIntoView({ behavior: "smooth" });

    e.target.reset();

  } catch(err) {
    resultDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
  }
});
