# Block by Block: project files

These are the starter projects that go with the book. Each one maps to a part of
the curriculum, so you can clone, run, and compare against what you build.

| Folder | Book part | What it is |
|--------|-----------|------------|
| `realtime-time-sync/` | Part 2 | A server-side Fabric mod that syncs in-game time to real local time. |
| `autorun-toggle/` | Part 2 | A client-side Fabric mod: a keybind that toggles auto-run. |
| `mc-tools/` | Part 1 | Python scripts that talk to your server over RCON. |
| `mc-dashboard/` | Part 3 + Secret Chapter | A FastAPI backend, a live web dashboard, and the AI admin console. |

## Quick start

Each folder has its own notes. The two mod folders build with the Gradle wrapper
(or the included Docker one-liner). The Python folders use a virtual environment:

```bash
cd mc-dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## A note on secrets

Nothing here contains a real password. The dashboard reads the RCON password from
an environment variable (`RCON_PASSWORD`), so set yours when you run it and keep
it out of any file you share.

Not affiliated with or endorsed by Mojang or Microsoft. Minecraft is a trademark
of Mojang Synergies AB.
