# DockerClaw

A minimal Docker setup for [OpenClaw](https://github.com/openclaw/openclaw) that connects to your **local host Ollama** instance, provides a WebChat interface, and uses a joke-generating agent that executes a Python script to print jokes.

## Architecture

```
Browser (localhost:18789)
    │
    ▼
┌──────────────┐         ┌──────────────────┐
│  OpenClaw    │────────▶│  Ollama (host)   │
│  (container) │  :11434 │  llama3.1:latest │
└──────────────┘         └──────────────────┘
    │
    ▼
workspace/joke_printer.py  (executed by the agent)
```

## Prerequisites

- Docker & Docker Compose
- Ollama running locally with `llama3.1:latest` pulled:
  ```bash
  ollama pull llama3.1:latest
  ```

## Quick Start

```bash
docker compose up -d
open http://localhost:18789
```

Login with password: `openclaw`

Chat with the agent — it will generate a joke about your topic and run the Python script to print it.

### Standalone Script (no UI)

Request a Donald Trump joke directly from the terminal:

```bash
python3 workspace/trump_jokes.py
```

This calls Ollama directly and prints the joke — no OpenClaw UI required.

## Documentation

- [Setup Guide](docs/setup.md) — Detailed setup and onboarding
- [Configuration](docs/configuration.md) — Config file reference
- [Tool Use](docs/tools.md) — How the Python script execution works

## Ports

| Port  | Service                          |
|-------|----------------------------------|
| 18789 | Dashboard + WebChat (all-in-one) |

## License

See [LICENSE](LICENSE).
