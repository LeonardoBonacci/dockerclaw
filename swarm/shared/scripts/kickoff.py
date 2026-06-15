#!/usr/bin/env python3
"""Kick off the World Cup 2026 party by seeding initial tasks to all agents."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from send_message import send

print("⚽ WORLD CUP 2026 PARTY — KICKOFF! ⚽")
print("=" * 50)

# Task for The Scout (researcher)
send(
    recipient="researcher",
    subject="Opening Research Brief",
    body=(
        "The party is starting! Please compile an opening research brief about "
        "World Cup 2026. Include:\n"
        "- Host cities and their stadiums\n"
        "- Key dates (opening match, final)\n"
        "- Favorites to win\n"
        "- 3 surprising facts about this tournament\n\n"
        "Post your findings to my inbox so I can share with the team."
    ),
    sender="coordinator",
)

# Task for The Poet (writer)
send(
    recipient="writer",
    subject="Opening Ceremony Poem",
    body=(
        "The World Cup 2026 party has begun! Write an epic opening poem that captures:\n"
        "- The excitement of the first tri-nation World Cup\n"
        "- The scale (48 teams, 16 cities, 3 countries)\n"
        "- The spirit of football bringing people together\n\n"
        "Make it dramatic. Make it memorable. This is the opener!"
    ),
    sender="coordinator",
)

# Task for VAR (critic)
send(
    recipient="critic",
    subject="Prepare Your Rating Criteria",
    body=(
        "VAR, we're kicking off the World Cup 2026 content party. "
        "Please prepare and post to the board:\n"
        "- Your official rating criteria for World Cup content\n"
        "- What makes content 'Ballon d'Or worthy' vs 'straight red card'\n"
        "- Any pet peeves or instant yellow cards you'll be watching for\n\n"
        "The team needs to know your standards before they start producing."
    ),
    sender="coordinator",
)

# Post to the board
board_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mailbox", "board")
os.makedirs(board_dir, exist_ok=True)
with open(os.path.join(board_dir, "000-party-started.md"), "w") as f:
    f.write("""# ⚽ WORLD CUP 2026 PARTY — KICKED OFF! ⚽

**Date:** The party starts NOW.

## The Team
| Agent | Role | Port |
|-------|------|------|
| El Capitán | Coordinator | :18800 |
| The Poet of the Pitch | Creative Writer | :18801 |
| VAR | Critic & Reviewer | :18802 |
| The Scout | Researcher | :18803 |

## The Mission
Create the ultimate collaborative World Cup 2026 experience.
Research. Create. Critique. Compile. Repeat.

## Rules of the Party
1. All communication goes through the mailbox
2. VAR reviews everything (no exceptions)
3. The board is our public gallery
4. Have fun — it's a World Cup party!

---
*Kickoff whistle blown. Let the games begin.* 🏟️
""")

print("\n✅ Initial tasks sent to all agents.")
print("📋 Party announcement posted to the board.")
print("\nOpen the agent dashboards:")
print("  Coordinator: http://localhost:18800")
print("  Writer:      http://localhost:18801")
print("  Critic:      http://localhost:18802")
print("  Researcher:  http://localhost:18803")
print("\nTell any agent 'check your inbox' to get them working!")
