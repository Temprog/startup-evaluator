document.getElementById("ideaForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const title = document.getElementById("title").value;
  const feedback = document.getElementById("feedback").value;

  const btn = document.getElementById("submitBtn");
  btn.innerText = "⏳ Evaluating...";
  btn.disabled = true;

  const res = await fetch("/api/submit", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name, title, feedback })
  });

  const data = await res.json();
  const resultBox = document.getElementById("result");

  resultBox.classList.remove("hidden");

  if (data.status === "success") {
    resultBox.innerHTML = `
      <h2>🔥 AI Summary</h2>
      <p>${data.ai_sentiment_emoji} Sentiment: <b>${data.ai_sentiment}</b></p>
      <hr/>
      <div>${data.ai_summary}</div>
    `;
  } else {
    resultBox.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
  }

  btn.innerText = "✨ Evaluate Idea";
  btn.disabled = false;
});
