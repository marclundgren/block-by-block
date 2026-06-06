#!/usr/bin/env bash
# Serve the book locally, then open http://localhost:8000 in your browser.
# (This is literally Lesson 1.1's `python3 -m http.server` in action.)
cd "$(dirname "$0")"
PORT="${1:-8000}"
echo "Block by Block → http://localhost:$PORT   (Ctrl+C to stop)"
exec python3 -m http.server "$PORT"
