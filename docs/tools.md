# Tools — Agent Capabilities

OpenClaw agents have access to code execution tools when configured with `"profile": "coding"`. This lets them run shell commands and Python scripts inside their container.

## How It Works

1. User sends a message (via WebChat or CLI)
2. The agent (Llama 3.1) processes the request
3. The agent uses its code execution tool to run commands
4. Output is returned in the chat or written to files

This uses OpenClaw's native code execution capability — no MCP server needed.

## CLI Agent Invocation

You can trigger an agent headlessly from outside the container:

```bash
docker exec <container> node openclaw.mjs agent --agent <agent-id> --message "your instruction"
```

This is particularly useful for:
- Automation scripts that orchestrate multiple agents
- Seeding tasks into agent inboxes
- Triggering agents in the swarm without opening the web UI

## Multi-Agent Communication

Agents communicate via a shared filesystem:

```
swarm/shared/
├── mailbox/
│   ├── coordinator/inbox/   # Coordinator receives compiled responses
│   ├── writer/inbox/        # Writer receives creative tasks
│   ├── critic/inbox/        # Critic receives review tasks
│   ├── researcher/inbox/    # Researcher receives research tasks
│   └── board/               # Shared bulletin board for all agents
└── scripts/
    ├── kickoff.py           # Seeds initial tasks
    └── send_message.py      # Utility for inter-agent messaging
```

Agents read `.md` files from their inbox, process them, and write responses to the coordinator's inbox or the shared board.

## Live Dashboard

A real-time web dashboard (port 8080) visualizes inter-agent communication as it happens. It monitors the mailbox directories and pushes new messages to the browser via WebSocket.

```bash
# Runs automatically with docker compose up -d
open http://localhost:8080
```

## Security Note

Code execution runs inside the container with access only to the mounted workspace and shared volumes. It cannot access the host filesystem beyond the explicitly mounted paths.
