# DockerClaw

A multi-agent swarm built on [OpenClaw](https://github.com/openclaw/openclaw) that connects to your **local Ollama** instance. Four agents collaborate via a shared filesystem mailbox.

## Demo

https://github.com/LeonardoBonacci/dockerclaw/raw/main/demo/recordings/dockerclaw-demo.mp4

> Four agents (Coordinator, Researcher, Writer, Critic) collaborating on a World Cup 2026 match preview — each thinking via Ollama's llama3.1, communicating through a shared mailbox.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Shared Volume                        │
│         swarm/shared/mailbox/{agent}/inbox/           │
└────┬──────────┬──────────┬──────────┬───────────────┘
     │          │          │          │
┌────▼────┐ ┌──▼────┐ ┌───▼───┐ ┌───▼──────┐
│Coordin- │ │Writer │ │Critic │ │Researcher│
│ator     │ │:18801 │ │:18802 │ │:18803    │
│:18800   │ └───────┘ └───────┘ └──────────┘
└─────────┘
     All containers → Ollama (host:11434)
```

Four agents collaborate on a topic (e.g., World Cup 2026) by reading tasks from their inboxes, producing work, and posting results to the shared board.

## Prerequisites

- Docker & Docker Compose
- Ollama running locally with `llama3.1:latest` pulled:
  ```bash
  ollama pull llama3.1:latest
  ```

## Quick Start

```bash
cd swarm
docker compose up -d
python3 shared/scripts/kickoff.py   # seed tasks to all agents
```

Then trigger agents via CLI:
```bash
docker exec swarm-researcher node openclaw.mjs agent --agent researcher --message "Check your inbox and process the task"
```

Login password for all agents: `openclaw`

## Live Dashboard

A real-time message dashboard shows inter-agent communication as it happens:

```bash
# Included in docker compose (port 8080):
open http://localhost:8080

# Or run standalone:
pip install -r demo/requirements.txt
python demo/dashboard.py
```

## Recording a Demo Video

Record a video of the swarm in action using Playwright:

```bash
cd demo
pip install -r requirements.txt
playwright install chromium
python record_demo_real.py
```

Output: `demo/recordings/dockerclaw-demo.mp4`

## Documentation

- [Setup Guide](docs/setup.md) — Detailed setup and onboarding
- [Configuration](docs/configuration.md) — Config file reference
- [Tools](docs/tools.md) — Agent capabilities and code execution

## Ports

| Port  | Service                              |
|-------|--------------------------------------|
| 8080  | Live Dashboard (message feed)        |
| 18800 | Swarm Coordinator (El Capitán)       |
| 18801 | Swarm Writer (The Poet of the Pitch) |
| 18802 | Swarm Critic (VAR)                   |
| 18803 | Swarm Researcher (The Scout)         |

## License

See [LICENSE](LICENSE).
