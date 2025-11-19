const form = document.getElementById("ideaForm");
const resultDiv = document.getElementById("result");
const btn = document.getElementById("submitBtn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = Object.fromEntries(new FormData(e.target));

  // Show processing state
  resultDiv.innerHTML = "<p>⏳ Evaluating your idea...</p>";
  btn.innerText = "⏳ Evaluating...";
  btn.disabled = true;

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
        <p><strong>Role / Background:</strong> ${data.role}</p>
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
  } finally {
    btn.innerText = "✨ Evaluate Idea";
    btn.disabled = false;
  }
});
