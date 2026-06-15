#!/usr/bin/env python3
"""Record a short, punchy GIF-ready demo (20s) showing messages flowing between agents."""

import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

DEMO_DIR = Path(__file__).parent
PROJECT_ROOT = DEMO_DIR.parent
RECORDINGS_DIR = DEMO_DIR / "recordings"
MAILBOX_ROOT = PROJECT_ROOT / "swarm" / "shared" / "mailbox"

AGENTS = ["coordinator", "writer", "critic", "researcher"]


def clean_mailboxes():
    for agent in AGENTS:
        inbox = MAILBOX_ROOT / agent / "inbox"
        if inbox.exists():
            for f in inbox.glob("*.md"):
                if f.name != ".gitkeep":
                    f.unlink()
    board = MAILBOX_ROOT / "board"
    if board.exists():
        for f in board.glob("*.md"):
            if f.name != ".gitkeep":
                f.unlink()


def send(recipient, subject, body, sender):
    if recipient == "board":
        inbox = MAILBOX_ROOT / "board"
    else:
        inbox = MAILBOX_ROOT / recipient / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    ts = int(time.time() * 1000)
    path = inbox / f"msg-{ts}.md"
    path.write_text(f"# Message from {sender}\n**To:** {recipient}\n**Subject:** {subject}\n**Time:** {time.strftime('%H:%M:%S')}\n\n---\n\n{body}\n")


async def main():
    RECORDINGS_DIR.mkdir(exist_ok=True)
    clean_mailboxes()

    # Start dashboard
    dashboard_proc = subprocess.Popen(
        [sys.executable, str(DEMO_DIR / "dashboard.py")],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    await asyncio.sleep(2)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                record_video_dir=str(RECORDINGS_DIR),
                record_video_size={"width": 1280, "height": 720},
            )
            page = await context.new_page()
            await page.goto("http://localhost:8080")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(1.5)

            # Simulate a fast realistic conversation between agents
            send("coordinator", "New Task: World Cup 2026 Opening Match Preview",
                 "Write a compelling preview for Mexico vs TBD at Estadio Azteca, June 11.\nCoordinate research → writing → review.", "human")
            await asyncio.sleep(1.5)

            send("researcher", "Research Request: Estadio Azteca & Mexico",
                 "Gather facts on: stadium capacity & history, Mexico's key players, 48-team format changes. Report back ASAP.", "coordinator")
            await asyncio.sleep(1.2)

            send("writer", "Writing Brief: Match Preview",
                 "Tone: vivid, exciting, accessible. 300 words. Wait for Scout's research before drafting.", "coordinator")
            await asyncio.sleep(1.2)

            send("coordinator", "Research Brief: World Cup 2026",
                 "**Estadio Azteca** — 87,523 capacity, hosted 2 WC finals (1970, 1986)\n**Mexico** — FIFA #15, key players: Edson Álvarez, Santiago Giménez\n**Format** — 48 teams, 12 groups of 4, 104 total matches\n**Fact** — First tri-nation hosted World Cup (USA/MEX/CAN)", "researcher")
            await asyncio.sleep(1.2)

            send("writer", "Research: Opening Match Facts",
                 "**Estadio Azteca** — 87,523 capacity, hosted 2 WC finals (1970, 1986)\n**Mexico** — FIFA #15, key players: Edson Álvarez, Santiago Giménez\n**Format** — 48 teams, 12 groups of 4, 104 total matches", "researcher")
            await asyncio.sleep(1.5)

            send("critic", "Review Request: Match Preview Draft",
                 "The ancient concrete cathedral of Estadio Azteca has witnessed football gods — Pelé's coronation in '70, Maradona's Hand of God in '86. On June 11, 2026, she opens her arms once more...\n\n[300 words of vivid match preview]", "writer")
            await asyncio.sleep(1.2)

            send("coordinator", "Draft Submitted for Review",
                 "Match preview complete (312 words). Sent to VAR for quality review.", "writer")
            await asyncio.sleep(1.5)

            send("coordinator", "VAR Review: ⭐⭐⭐⭐ (4/5)",
                 "**Accuracy:** 5/5 — all facts verified\n**Engagement:** 4/5 — great opening hook, minor pacing issue in paragraph 3\n**Quality:** 4/5 — vivid imagery, strong voice\n\n✅ Approved for publication.", "critic")
            await asyncio.sleep(1.2)

            send("board", "Final Review: Opening Match Preview ⭐⭐⭐⭐",
                 "Approved by VAR. Accuracy 5/5, Engagement 4/5, Quality 4/5. Ready for publication.", "critic")
            await asyncio.sleep(1.2)

            send("board", "✅ Sprint Complete: Opening Match Preview",
                 "Team delivered: Scout researched → Poet wrote → VAR approved.\nArticle ready for publication. Great teamwork! ⚽", "coordinator")
            await asyncio.sleep(2.5)

            await page.close()
            await context.close()
            await browser.close()

        # Rename video
        videos = list(RECORDINGS_DIR.glob("*.webm"))
        if videos:
            latest = max(videos, key=lambda p: p.stat().st_mtime)
            final = RECORDINGS_DIR / "dockerclaw-demo.webm"
            if final.exists():
                final.unlink()
            latest.rename(final)

            # Convert to mp4
            mp4 = RECORDINGS_DIR / "dockerclaw-demo.mp4"
            subprocess.run([
                "ffmpeg", "-i", str(final),
                "-vf", "fps=24,scale=1280:-2",
                "-c:v", "libx264", "-preset", "slow", "-crf", "23",
                "-pix_fmt", "yuv420p", "-an",
                str(mp4), "-y"
            ], capture_output=True)

            # Convert to GIF
            gif = RECORDINGS_DIR / "dockerclaw-demo.gif"
            subprocess.run([
                "ffmpeg", "-i", str(mp4),
                "-vf", "fps=12,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
                "-loop", "0", str(gif), "-y"
            ], capture_output=True)

            # Clean up webm
            final.unlink()

            print(f"✅ MP4: {mp4} ({mp4.stat().st_size/1024:.0f} KB)")
            print(f"✅ GIF: {gif} ({gif.stat().st_size/1024:.0f} KB)")
        else:
            print("⚠️ No video recorded")
    finally:
        dashboard_proc.terminate()
        dashboard_proc.wait()


if __name__ == "__main__":
    asyncio.run(main())
