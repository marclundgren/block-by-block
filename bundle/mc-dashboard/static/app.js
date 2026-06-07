const $ = (id) => document.getElementById(id);
const statusEl = $("status"), onlineEl = $("online"),
      rosterEl = $("players"), toastEl = $("toast"),
      chatEl = $("chat"), msgEl = $("msg");

// ---- live status poll ----
async function refresh() {
  try {
    const res = await fetch("/api/status");
    if (!res.ok) throw new Error(res.status);
    const d = await res.json();
    statusEl.className = "badge up";
    statusEl.innerHTML = "<i></i> online";
    onlineEl.textContent = d.online;
    rosterEl.innerHTML = d.players.length
      ? d.players.map(p => `<li>${p}</li>`).join("")
      : `<li style="opacity:.5">nobody online</li>`;
  } catch {
    statusEl.className = "badge down";
    statusEl.innerHTML = "<i></i> offline";
    onlineEl.textContent = "-";
    rosterEl.innerHTML = "";
  }
}

// ---- fixed command buttons ----
async function sendCommand(cmd, btn) {
  btn.disabled = true;
  toastEl.textContent = "";
  try {
    const res = await fetch(`/api/command/${cmd}`, { method: "POST" });
    const d = await res.json();
    toastEl.style.color = res.ok ? "#5fcf80" : "#e0573d";
    toastEl.textContent = d.detail || d.result || "done";
    refresh();
  } catch {
    toastEl.style.color = "#e0573d";
    toastEl.textContent = "request failed";
  } finally {
    btn.disabled = false;
  }
}
document.querySelectorAll("button[data-cmd]").forEach(btn =>
  btn.addEventListener("click", () => sendCommand(btn.dataset.cmd, btn)));

// ---- AI admin console ----
const log = [];
function bubble(who, text) {
  const d = document.createElement("div");
  d.className = "bubble " + who;
  d.textContent = text;
  chatEl.appendChild(d);
  chatEl.scrollTop = chatEl.scrollHeight;
}
async function ask(text) {
  bubble("you", text);
  try {
    const res = await fetch("/api/ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history: log })
    });
    const d = await res.json();
    log.push({ role: "user", content: text });
    log.push({ role: "assistant", content: JSON.stringify(d) });
    let line = d.say || "";
    if (d.command) line += `   (ran: ${d.command})`;
    if (d.error) line += `   note: ${d.error}`;
    bubble("ai", line);
    refresh();
  } catch {
    bubble("ai", "request failed");
  }
}
msgEl.addEventListener("keydown", e => {
  if (e.key === "Enter" && e.target.value.trim()) {
    ask(e.target.value.trim());
    e.target.value = "";
  }
});

refresh();
setInterval(refresh, 4000);
