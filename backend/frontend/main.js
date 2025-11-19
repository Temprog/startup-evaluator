document.getElementById("ideaForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  const res = await fetch("/api/submit", {             // api/submit is just a naming convention. It will match
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });
  const result = await res.json();
  document.getElementById("result").innerText = JSON.stringify(result, null, 2);
});
