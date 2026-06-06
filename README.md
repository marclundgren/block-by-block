# Block by Block

A self-paced HTML tutorial book that takes you from absolute beginner to
full-stack engineer, using your own self-hosted **Minecraft 1.21.11 Fabric**
server as the throughline.

**33 lessons across 4 parts:**

0. **Launchpad** — WSL2, Docker, Docker Compose, your Fabric server, dev tools
1. **Python** — from `print()` to classes, generators, and typing
2. **Minecraft** — Fabric mods, events, commands, mixins, the `javap` workflow
3. **Full-Stack** — HTTP, HTML/CSS/JS, a FastAPI backend wired to your server via
   RCON, a live web dashboard, databases, and deployment with Compose

## How to read it

It's a single self-contained `index.html` — no build step, no dependencies.

**Option A — open the file directly.** From Windows, browse to:
```
\\wsl$\Ubuntu\home\marc\Dev\block-by-block\index.html
```
(adjust the distro name if yours isn't `Ubuntu`).

**Option B — serve it (recommended; works from Windows *and* Mac):**
```bash
./serve.sh            # then open http://localhost:8000
```
From Windows, `http://localhost:8000` just works thanks to WSL port forwarding.

## Features

- Progress saved in your browser (localStorage) — a Minecraft-style **XP bar**
  fills and levels you up as you complete lessons.
- Keyboard nav: <kbd>←</kbd> / <kbd>→</kbd> between lessons, <kbd>c</kbd> to toggle complete.
- Lesson search, copy buttons on every code block, prev/next paging.
- Every lesson ends with a hands-on **⛏ Try it** task.

The curriculum references your real projects (`realtime-time-sync`,
`autorun-toggle`) and your actual `compose.yml`, so the examples are things you
can run immediately.
