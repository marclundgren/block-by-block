"""Talk to your Minecraft server from Python over RCON (book Part 1, lesson 10).

Run your server with RCON enabled, then:
    export RCON_PASSWORD=your-rcon-password
    python3 rcon_demo.py
"""
import os
from mcrcon import MCRcon

HOST = os.getenv("RCON_HOST", "localhost")
PASSWORD = os.getenv("RCON_PASSWORD", "")   # never hard-code this


def online_players(mcr) -> list[str]:
    """Parse 'There are 2 of a max of 20 players online: alex, steve'."""
    resp = mcr.command("list")
    if ":" not in resp:
        return []
    names = resp.split(":", 1)[1].strip()
    return [n.strip() for n in names.split(",") if n.strip()]


def main():
    if not PASSWORD:
        raise SystemExit("Set RCON_PASSWORD first.")
    with MCRcon(HOST, PASSWORD, port=25575) as mcr:
        print("online:", online_players(mcr))
        mcr.command("time set day")
        mcr.command("say Python is now in control.")


if __name__ == "__main__":
    main()
