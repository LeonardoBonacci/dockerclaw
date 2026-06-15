# DockerClaw

A Docker setup for [OpenClaw](https://github.com/openclaw/openclaw) that connects to your **local Ollama** instance. Includes a single-agent container and a **multi-agent swarm** demonstrating inter-agent communication via a shared filesystem.

## Architecture

### Single Agent (default)

```
Browser (localhost:18789)
    │
    ▼
┌──────────────┐         ┌──────────────────┐
│  OpenClaw    │────────▶│  Ollama (host)   │
│  (container) │  :11434 │  llama3.1:latest │
└──────────────┘         └──────────────────┘
```

### Multi-Agent Swarm

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

### Single agent

```bash
docker compose up -d
open http://localhost:18789
```

### Multi-agent swarm

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

## Documentation

- [Setup Guide](docs/setup.md) — Detailed setup and onboarding
- [Configuration](docs/configuration.md) — Config file reference
- [Tools](docs/tools.md) — Agent capabilities and code execution

- [Setup Guide](docs/setup.md) — Detailed setup and onboarding
- [Configuration](docs/configuration.md) — Config file reference
- [Tool Use](docs/tools.md) — How the Python script execution works

## Ports

| Port  | Service                              |
|-------|--------------------------------------|
| 18789 | Main agent — Dashboard + WebChat     |
| 18800 | Swarm Coordinator (El Capitán)       |
| 18801 | Swarm Writer (The Poet of the Pitch) |
| 18802 | Swarm Critic (VAR)                   |
| 18803 | Swarm Researcher (The Scout)         |

## License

See [LICENSE](LICENSE).
