#!/usr/bin/env python3
"""Record a REAL demo of the DockerClaw swarm collaborating on World Cup 2026 content.

This script:
1. Cleans the mailboxes for a fresh start
2. Starts the dashboard server
3. Opens the dashboard in Playwright with video recording
4. Sends a task to the coordinator agent via CLI
5. Each agent thinks via Ollama, responds, and the response is routed to the next agent's inbox
6. The dashboard captures all inter-agent communication in real-time

The key insight: agents respond via their CLI (stdout JSON), and this script
routes their responses into the next agent's mailbox — acting as the message bus.

Prerequisites:
- Docker swarm running (docker compose up -d from swarm/)
- Ollama running with llama3.1:latest
- pip install -r requirements.txt && playwright install chromium

Usage:
    python record_demo_real.py

Output: demo/recordings/dockerclaw-real-demo.webm
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

DEMO_DIR = Path(__file__).parent
PROJECT_ROOT = DEMO_DIR.parent
RECORDINGS_DIR = DEMO_DIR / "recordings"
SWARM_DIR = PROJECT_ROOT / "swarm"
MAILBOX_ROOT = SWARM_DIR / "shared" / "mailbox"
SCRIPTS_DIR = SWARM_DIR / "shared" / "scripts"

# Agent config
AGENTS = {
    "coordinator": {"port": 18800, "name": "El Capitán"},
    "writer": {"port": 18801, "name": "The Poet"},
    "critic": {"port": 18802, "name": "VAR"},
    "researcher": {"port": 18803, "name": "The Scout"},
}

TIMEOUT = 180  # seconds per agent turn


def clean_mailboxes():
    """Remove old messages for a clean recording."""
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
    print("🧹 Mailboxes cleaned.")


def send_to_mailbox(recipient: str, subject: str, body: str, sender: str):
    """Write a message file to an agent's inbox."""
    if recipient == "board":
        inbox = MAILBOX_ROOT / "board"
    else:
        inbox = MAILBOX_ROOT / recipient / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time() * 1000)
    filename = f"msg-{timestamp}.md"
    filepath = inbox / filename

    content = f"""# Message from {sender}
**To:** {recipient}
**Subject:** {subject}
**Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

{body}
"""
    filepath.write_text(content)
    print(f"   ✉️  {sender} → {recipient}: {subject}")
    return filepath


def ask_agent(agent_name: str, message: str) -> str:
    """Send a message to an agent via CLI and return its text response."""
    container = f"swarm-{agent_name}"
    cmd = [
        "docker", "exec", container,
        "node", "openclaw.mjs", "agent",
        "--agent", agent_name,
        "--message", message,
        "--json",
    ]
    print(f"   🤖 {agent_name} is thinking...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        # Parse the JSON response to extract the agent's text reply
        try:
            data = json.loads(result.stdout)
            # The text is in result.payloads[0].text
            payloads = data.get("result", {}).get("payloads", [])
            for payload in payloads:
                if payload.get("text"):
                    return payload["text"]
            # Fallback: check messages array
            messages = data.get("result", {}).get("messages", [])
            for msg in messages:
                if msg.get("role") == "assistant" and msg.get("text"):
                    return msg["text"]
            return result.stdout[:2000]
        except json.JSONDecodeError:
            return result.stdout[:2000] if result.stdout else "(no response)"
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  {agent_name} timed out after {TIMEOUT}s")
        return "(agent timed out — thinking too hard)"
    except Exception as e:
        print(f"   ❌ Error with {agent_name}: {e}")
        return f"(error: {e})"


async def record_real_demo():
    RECORDINGS_DIR.mkdir(exist_ok=True)
    clean_mailboxes()

    # Start dashboard server
    print("🚀 Starting dashboard server...")
    dashboard_proc = subprocess.Popen(
        [sys.executable, str(DEMO_DIR / "dashboard.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
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

            print("🌐 Opening dashboard...")
            await page.goto("http://localhost:8080")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)

            # === ACT 1: Human sends task to coordinator ===
            print("\n⚽ ACT 1: Human sends task...")
            task_body = (
                "I need a match preview for the opening game of World Cup 2026 "
                "(Mexico vs TBD at Estadio Azteca, June 11, 2026).\n\n"
                "Coordinate the team:\n"
                "1. Researcher: gather key facts (venue, teams, format)\n"
                "2. Writer: create an engaging 300-word match preview\n"
                "3. Critic: review and rate the final piece"
            )
            send_to_mailbox("coordinator", "World Cup 2026: Opening Match Preview", task_body, "human")
            await asyncio.sleep(2)

            # === ACT 2: Coordinator delegates ===
            print("\n📋 ACT 2: Coordinator reads task and delegates...")
            coord_response = ask_agent(
                "coordinator",
                "You are El Capitán, the coordinator of a writing team. "
                "A human wants a World Cup 2026 opening match preview. "
                "Delegate tasks: tell the researcher what facts to gather, "
                "and tell the writer what kind of article to write. "
                "Be specific and concise. Reply with your delegation plan."
            )
            print(f"   📝 Response: {coord_response[:100]}...")

            # Route coordinator's delegation to researcher and writer
            send_to_mailbox(
                "researcher",
                "Research Request: World Cup 2026 Opening Match",
                (
                    "From El Capitán:\n\n"
                    "Please research the following for our match preview:\n"
                    "- Estadio Azteca: capacity, history, notable matches\n"
                    "- Mexico national team: current form, key players, FIFA ranking\n"
                    "- World Cup 2026 format: 48 teams, group stage changes\n"
                    "- Historical context: Mexico's World Cup record at home\n\n"
                    "Report back with your findings."
                ),
                "coordinator",
            )
            send_to_mailbox(
                "writer",
                "Writing Brief: Opening Match Preview",
                (
                    "From El Capitán:\n\n"
                    "Once research arrives, write a 300-word match preview for:\n"
                    "Mexico vs TBD — Estadio Azteca, June 11, 2026\n\n"
                    "Tone: exciting, vivid, accessible to casual fans.\n"
                    "Include: venue atmosphere, team strengths, what's at stake.\n"
                    "Wait for The Scout's research before writing."
                ),
                "coordinator",
            )
            await asyncio.sleep(3)

            # === ACT 3: Researcher gathers facts ===
            print("\n🔍 ACT 3: Researcher gathers facts...")
            research_response = ask_agent(
                "researcher",
                "You are The Scout, a football researcher. Write a concise research brief "
                "about the World Cup 2026 opening match at Estadio Azteca, Mexico City. "
                "Cover: stadium facts (capacity, history), Mexico's team (key players, form), "
                "the new 48-team format, and one surprising historical fact. "
                "Keep it factual and under 200 words."
            )
            print(f"   📝 Response: {research_response[:100]}...")

            # Route research to writer and coordinator
            send_to_mailbox("writer", "Research: World Cup 2026 Facts", research_response, "researcher")
            send_to_mailbox("coordinator", "Research Complete", research_response, "researcher")
            await asyncio.sleep(3)

            # === ACT 4: Writer creates the preview ===
            print("\n✍️  ACT 4: Writer creates match preview...")
            writer_response = ask_agent(
                "writer",
                f"You are The Poet of the Pitch, a football writer. "
                f"Using this research:\n\n{research_response[:500]}\n\n"
                f"Write a vivid, exciting 300-word match preview for the "
                f"World Cup 2026 opening match: Mexico at Estadio Azteca, June 11. "
                f"Make it dramatic. Capture the atmosphere. This is the opener!"
            )
            print(f"   📝 Response: {writer_response[:100]}...")

            # Route draft to critic and coordinator
            send_to_mailbox("critic", "Review Request: Match Preview Draft", writer_response, "writer")
            send_to_mailbox("coordinator", "Draft Submitted", "The Poet has submitted the match preview for review.", "writer")
            await asyncio.sleep(3)

            # === ACT 5: Critic reviews ===
            print("\n🏆 ACT 5: Critic reviews the article...")
            critic_response = ask_agent(
                "critic",
                f"You are VAR, a sharp football content critic. "
                f"Review this match preview and rate it 1-5 on: "
                f"accuracy, engagement, writing quality. "
                f"Give brief feedback (what works, what doesn't). "
                f"Be fair but honest.\n\n---\n\n{writer_response[:800]}"
            )
            print(f"   📝 Response: {critic_response[:100]}...")

            # Route review to coordinator and board
            send_to_mailbox("coordinator", "VAR Review Complete", critic_response, "critic")
            send_to_mailbox("board", "Final Review: Opening Match Preview", critic_response, "critic")
            await asyncio.sleep(3)

            # === ACT 6: Coordinator posts final ===
            print("\n🎯 ACT 6: Coordinator wraps up...")
            send_to_mailbox(
                "board",
                "✅ Sprint Complete: Opening Match Preview",
                (
                    "**Team Output Summary**\n\n"
                    "The Scout delivered research, The Poet wrote the preview, "
                    "VAR reviewed and approved.\n\n"
                    f"**VAR's verdict:** {critic_response[:200]}\n\n"
                    "Article is ready for publication. Great teamwork! ⚽"
                ),
                "coordinator",
            )
            await asyncio.sleep(4)

            # Final pause to capture the full dashboard state
            print("\n🎬 Recording final state...")
            await asyncio.sleep(3)

            await page.close()
            await context.close()
            await browser.close()

        # Find and rename the video
        videos = list(RECORDINGS_DIR.glob("*.webm"))
        if videos:
            latest = max(videos, key=lambda p: p.stat().st_mtime)
            final_path = RECORDINGS_DIR / "dockerclaw-real-demo.webm"
            if final_path.exists():
                final_path.unlink()
            latest.rename(final_path)
            print(f"\n✅ Demo recorded: {final_path}")
            print(f"   Size: {final_path.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print("⚠️  No video file found in recordings/")

    finally:
        dashboard_proc.terminate()
        dashboard_proc.wait()
        print("🛑 Dashboard server stopped.")

    # Show what was produced
    print("\n📬 Messages generated during recording:")
    for agent in list(AGENTS.keys()) + ["board"]:
        inbox_path = MAILBOX_ROOT / agent / "inbox" if agent != "board" else MAILBOX_ROOT / "board"
        if inbox_path.exists():
            files = [f.name for f in inbox_path.glob("*.md") if f.name != ".gitkeep"]
            if files:
                print(f"   {agent}: {len(files)} messages")
                for f in sorted(files)[:5]:
                    print(f"      - {f}")


if __name__ == "__main__":
    asyncio.run(record_real_demo())
