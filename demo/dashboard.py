#!/usr/bin/env python3
"""Real-time agent message dashboard for DockerClaw swarm."""

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

app = FastAPI()

# Path to the shared mailbox — works both locally and in Docker
MAILBOX_ROOT = Path(os.environ.get(
    "MAILBOX_PATH",
    str(Path(__file__).parent.parent / "swarm" / "shared" / "mailbox")
))

# Connected WebSocket clients
connected_clients: Set[WebSocket] = set()

# Message history for new clients
message_history: list = []


class MailboxWatcher(FileSystemEventHandler):
    """Watch for new messages in agent mailboxes."""

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop

    def on_created(self, event: FileCreatedEvent):
        if event.is_directory:
            return
        if not event.src_path.endswith(".md"):
            return
        # Parse the message file
        path = Path(event.src_path)
        # Determine recipient from path (mailbox/<recipient>/inbox/<file>)
        parts = path.parts
        try:
            mailbox_idx = parts.index("mailbox")
            recipient = parts[mailbox_idx + 1]
        except (ValueError, IndexError):
            recipient = "unknown"

        # Read the file content
        time.sleep(0.1)  # Small delay to ensure file is fully written
        try:
            content = path.read_text()
        except Exception:
            content = ""

        # Extract sender from content
        sender = "unknown"
        subject = path.stem
        for line in content.split("\n"):
            if line.startswith("# Message from "):
                sender = line.replace("# Message from ", "").strip()
            elif line.startswith("**Subject:**"):
                subject = line.replace("**Subject:**", "").strip()

        message = {
            "type": "message",
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "filename": path.name,
            "timestamp": time.time(),
            "preview": content[:300],
        }

        message_history.append(message)
        # Broadcast to all connected clients
        asyncio.run_coroutine_threadsafe(broadcast(message), self.loop)


async def broadcast(message: dict):
    """Send a message to all connected WebSocket clients."""
    data = json.dumps(message)
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send_text(data)
        except Exception:
            disconnected.add(client)
    connected_clients.difference_update(disconnected)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    # Send history
    for msg in message_history:
        await websocket.send_text(json.dumps(msg))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.discard(websocket)


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = Path(__file__).parent / "dashboard.html"
    return html_path.read_text()


@app.get("/api/agents")
async def agents_status():
    """Return agent status info."""
    agents = ["coordinator", "writer", "critic", "researcher"]
    result = []
    for agent in agents:
        inbox = MAILBOX_ROOT / agent / "inbox"
        count = len(list(inbox.glob("*.md"))) if inbox.exists() else 0
        result.append({"name": agent, "inbox_count": count})
    return result


@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    handler = MailboxWatcher(loop)
    observer = Observer()
    # Watch all mailbox subdirectories
    observer.schedule(handler, str(MAILBOX_ROOT), recursive=True)
    observer.start()
    app.state.observer = observer


@app.on_event("shutdown")
async def shutdown():
    app.state.observer.stop()
    app.state.observer.join()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
