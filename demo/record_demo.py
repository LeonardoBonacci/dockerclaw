#!/usr/bin/env python3
"""Record a demo video of the DockerClaw swarm dashboard using Playwright.

This script:
1. Starts the dashboard server
2. Opens it in a browser with video recording enabled
3. Triggers agent communication (kickoff)
4. Waits for messages to flow, then stops recording

Usage:
    pip install -r requirements.txt
    playwright install chromium
    python record_demo.py

Output: demo/recordings/dockerclaw-demo.webm
"""

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
SWARM_SCRIPTS = PROJECT_ROOT / "swarm" / "shared" / "scripts"


async def record_demo():
    RECORDINGS_DIR.mkdir(exist_ok=True)

    # Start dashboard server
    print("🚀 Starting dashboard server...")
    dashboard_proc = subprocess.Popen(
        [sys.executable, str(DEMO_DIR / "dashboard.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    await asyncio.sleep(2)  # Wait for server to start

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                record_video_dir=str(RECORDINGS_DIR),
                record_video_size={"width": 1280, "height": 720},
            )
            page = await context.new_page()

            print("🌐 Opening dashboard...")
            await page.goto("http://localhost:8080")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)

            # Trigger the kickoff to seed messages
            print("⚽ Triggering agent kickoff...")
            subprocess.run(
                [sys.executable, str(SWARM_SCRIPTS / "kickoff.py")],
                cwd=str(SWARM_SCRIPTS.parent.parent),
            )

            # Wait for messages to appear in the feed
            print("⏳ Waiting for messages to flow...")
            await asyncio.sleep(3)

            # Simulate some inter-agent communication
            sys.path.insert(0, str(SWARM_SCRIPTS))
            from send_message import send

            await asyncio.sleep(1)

            # Researcher reports back
            send(
                recipient="coordinator",
                subject="Research Brief: World Cup 2026",
                body=(
                    "Here are my findings:\n\n"
                    "**Host Cities:** 16 cities across USA, Mexico, Canada\n"
                    "- MetLife Stadium (NYC) — Final\n"
                    "- Estadio Azteca (Mexico City) — Opening\n"
                    "- BMO Field (Toronto)\n\n"
                    "**Key Dates:**\n"
                    "- June 11, 2026 — Opening match\n"
                    "- July 19, 2026 — Final\n\n"
                    "**Favorites:** Brazil, France, Argentina, England\n\n"
                    "**Surprising Facts:**\n"
                    "1. First 48-team World Cup\n"
                    "2. First tri-nation hosted tournament\n"
                    "3. Largest World Cup in history (104 matches)"
                ),
                sender="researcher",
            )
            await asyncio.sleep(2)

            # Coordinator delegates to writer
            send(
                recipient="writer",
                subject="Write Stadium Guide",
                body=(
                    "Based on The Scout's research, please write a compelling guide "
                    "to the top 5 stadiums. Make it vivid — the reader should feel "
                    "like they're walking through the tunnel onto the pitch."
                ),
                sender="coordinator",
            )
            await asyncio.sleep(2)

            # Writer submits to critic
            send(
                recipient="critic",
                subject="Review: Stadium Guide Draft",
                body=(
                    "Here's my stadium guide draft for your review:\n\n"
                    "# The Cathedrals of 2026\n\n"
                    "MetLife Stadium rises from the New Jersey marshlands like a "
                    "colosseum reborn. 82,500 seats, each one a throne...\n\n"
                    "Please rate this. Be honest but fair, VAR."
                ),
                sender="writer",
            )
            await asyncio.sleep(2)

            # Critic responds
            send(
                recipient="writer",
                subject="VAR Review: Stadium Guide ⭐⭐⭐⭐",
                body=(
                    "**Rating: 4/5 — Champions League Quality**\n\n"
                    "✅ Vivid imagery\n"
                    "✅ Great opening hook\n"
                    "⚠️ Minor: needs more local culture context\n\n"
                    "Verdict: Approved with minor revisions. Not a red card in sight."
                ),
                sender="critic",
            )
            await asyncio.sleep(2)

            # Coordinator posts summary
            send(
                recipient="board",
                subject="Sprint 1 Complete",
                body=(
                    "Team update: Research delivered, stadium guide written and reviewed. "
                    "We're on track. Next up: match predictions and fan stories."
                ),
                sender="coordinator",
            )
            await asyncio.sleep(3)

            print("🎬 Finalizing recording...")
            await page.close()
            await context.close()
            await browser.close()

        # Find the recorded video
        videos = list(RECORDINGS_DIR.glob("*.webm"))
        if videos:
            latest = max(videos, key=lambda p: p.stat().st_mtime)
            final_path = RECORDINGS_DIR / "dockerclaw-demo.webm"
            latest.rename(final_path)
            print(f"\n✅ Demo recorded: {final_path}")
            print(f"   Size: {final_path.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print("⚠️  No video file found in recordings/")

    finally:
        dashboard_proc.terminate()
        dashboard_proc.wait()
        print("🛑 Dashboard server stopped.")


if __name__ == "__main__":
    asyncio.run(record_demo())
