"""Block by Block dashboard backend (Part 3 + Secret Chapter).

Endpoints:
  GET  /api/status        live player count, read over RCON
  POST /api/command/{cmd} run one of a few safe, fixed commands
  POST /api/ai            natural-language admin console, grounded on commands.json

Run it:
  export RCON_PASSWORD=your-rcon-password
  fastapi dev main.py        # http://localhost:8000
"""
import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from mcrcon import MCRcon
from pydantic import BaseModel

app = FastAPI()

RCON_HOST = os.getenv("RCON_HOST", "localhost")
RCON_PASS = os.getenv("RCON_PASSWORD", "")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")


def rcon(cmd: str) -> str:
    try:
        with MCRcon(RCON_HOST, RCON_PASS, port=25575) as m:
            return m.command(cmd)
    except Exception:
        raise HTTPException(503, "server unreachable")


# ---- live status -----------------------------------------------------------
@app.get("/api/status")
def status():
    resp = rcon("list")
    players = []
    if ":" in resp:
        players = [p.strip() for p in resp.split(":", 1)[1].split(",") if p.strip()]
    return {"online": len(players), "players": players}


# ---- safe fixed-button commands -------------------------------------------
ALLOWED = {"day": "time set day", "night": "time set night", "clear": "weather clear"}


@app.post("/api/command/{cmd}")
def run_command(cmd: str):
    if cmd not in ALLOWED:
        raise HTTPException(400, f"unknown command: {cmd}")
    return {"result": rcon(ALLOWED[cmd]) or "ok"}


# ---- AI admin console (grounded + validated) ------------------------------
COMMANDS = json.load(open("commands.json"))
REFERENCE = "\n".join(
    f"- {name}: {info['syntax']}  (example: {info['example']})"
    for name, info in COMMANDS.items()
)
SYSTEM = {"role": "system", "content": (
    "You are an admin assistant for a Minecraft server.\n"
    "You may ONLY use commands from this reference:\n" + REFERENCE +
    "\nReturn the single exact command to run, with no leading slash. "
    "If nothing fits, return an empty command and explain in 'say'. "
    "Always include a short, friendly 'say'."
)}
SCHEMA = {
    "type": "object",
    "properties": {"command": {"type": "string"}, "say": {"type": "string"}},
    "required": ["command", "say"],
}


def is_allowed(cmd: str) -> bool:
    return bool(cmd) and any(cmd.startswith(name) for name in COMMANDS)


class AiRequest(BaseModel):
    message: str
    history: list = []


@app.post("/api/ai")
def ai(req: AiRequest):
    from ollama import chat  # imported here so the rest works without Ollama
    messages = [SYSTEM] + req.history + [{"role": "user", "content": req.message}]
    out = chat(model=MODEL, messages=messages, format=SCHEMA)
    data = json.loads(out.message.content)

    cmd = (data.get("command") or "").strip().lstrip("/")
    result = error = None
    if is_allowed(cmd):
        try:
            result = rcon(cmd)
        except Exception as e:
            error = str(e)
    elif cmd:
        error = f"'{cmd}' is not in the command reference, so it will not run."
    return {"say": data.get("say"),
            "command": cmd if is_allowed(cmd) else None,
            "result": result, "error": error}


# serve the frontend last so it does not shadow the API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")
