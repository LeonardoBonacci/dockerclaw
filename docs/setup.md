# Setup Guide

## Prerequisites

1. **Docker & Docker Compose** installed on your machine
2. **Ollama** running locally on port 11434 with `llama3.1:latest`:

```bash
# Install Ollama (if not already installed)
# https://ollama.com/download

# Pull the model
ollama pull llama3.1:latest

# Verify it's running
curl http://localhost:11434/api/tags
```

## Starting the Swarm

```bash
cd swarm
docker compose up -d
```

This launches 4 OpenClaw containers (coordinator, writer, critic, researcher) that:
- Share a filesystem at `swarm/shared/` for mailbox-based communication
- Each expose their own port (18800–18803)
- All connect to the same host Ollama instance

### Seeding Tasks

```bash
python3 shared/scripts/kickoff.py
```

This writes initial task files into each agent's inbox.

### Triggering Agents

```bash
docker exec swarm-researcher node openclaw.mjs agent --agent researcher --message "Check your inbox and process the task"
docker exec swarm-writer node openclaw.mjs agent --agent writer --message "Check your inbox and process the task"
docker exec swarm-critic node openclaw.mjs agent --agent critic --message "Check your inbox and process the task"
```

## First-Time Setup

The repo ships with pre-configured `swarm/*/data/openclaw.json` files. No onboarding needed — just `docker compose up -d`.

Gateway password: `openclaw`

## Verifying It Works

1. Open http://localhost:18800 (coordinator)
2. Log in with password `openclaw`
3. Send a message — the agent will respond using Llama 3.1

## Stopping

```bash
docker compose down          # single agent
cd swarm && docker compose down   # swarm
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Can't connect to Ollama | Ensure `ollama serve` is running on the host |
| Model not found | Run `ollama pull llama3.1:latest` |
| Port in use | Change the port mapping in the relevant `docker-compose.yml` |
| Agent not responding | Llama 3.1 on CPU can take 30s+ per response — be patient |
| Script not executing | Check that `workspace/joke_printer.py` exists and the agent has code execution enabled |
