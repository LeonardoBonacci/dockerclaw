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

## Starting the Stack

```bash
cd dockerclaw
docker compose up -d
```

This starts the OpenClaw container which:
- Connects to your host Ollama via `host.docker.internal:11434`
- Exposes Dashboard + WebChat on port 18789
- Mounts `./workspace` so the agent can execute scripts
- Mounts `./data` for persistent configuration

## First-Time Setup

The repo ships with a pre-configured `data/openclaw.json`. No onboarding needed — just `docker compose up -d`.

Gateway password: `openclaw`

## Verifying It Works

1. Open http://localhost:18789
2. Log in with password `openclaw`
3. Type any message (e.g., "Tell me a joke about Docker")
4. The agent should:
   - Generate a joke using Llama 3.1
   - Execute `joke_printer.py` to print it
   - Return the output in the chat

## Stopping

```bash
docker compose down
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Can't connect to Ollama | Ensure `ollama serve` is running on the host |
| Model not found | Run `ollama pull llama3.1:latest` |
| Port 18789 in use | Change the port mapping in `docker-compose.yml` |
| Script not executing | Check that `workspace/joke_printer.py` exists and the agent has code execution enabled |
