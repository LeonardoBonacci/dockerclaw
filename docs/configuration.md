# Configuration

OpenClaw configuration lives in `data/openclaw.json` (mounted into the container at `/home/node/.openclaw/openclaw.json`).

## Config File Reference

```json
{
  "gateway": {
    "mode": "local"
  },
  "models": {
    "mode": "replace",
    "providers": {
      "ollama": {
        "baseUrl": "http://host.docker.internal:11434"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/llama3.1:latest"
      }
    },
    "list": [
      {
        "id": "joker",
        "default": true,
        "name": "Joke Bot",
        "description": "Generates jokes and prints them via joke_printer.py",
        "model": {
          "primary": "ollama/llama3.1:latest"
        },
        "tools": {
          "profile": "coding"
        },
        "workspace": "/home/node/workspace"
      }
    ]
  },
  "web": {
    "enabled": true
  }
}
```

## Key Settings

### `gateway`

| Field  | Description                                      |
|--------|--------------------------------------------------|
| `mode` | `local` for self-hosted without cloud features   |

### `models`

| Field                  | Description                                  |
|------------------------|----------------------------------------------|
| `mode`                 | `replace` uses only your configured providers |
| `providers.ollama.baseUrl` | URL to reach Ollama from the container   |

### `agents.defaults`

| Field          | Description                                          |
|----------------|------------------------------------------------------|
| `model.primary`| Default model in `provider/model` format             |

### `agents.list[]`

| Field          | Description                                          |
|----------------|------------------------------------------------------|
| `id`           | Unique agent identifier                              |
| `default`      | Whether this is the default agent                    |
| `model.primary`| Model for this specific agent                        |
| `tools.profile`| Tool capability level (`minimal`, `coding`, `full`)  |
| `workspace`    | Directory the agent can access for code execution    |

### `web`

| Field     | Description                    |
|-----------|--------------------------------|
| `enabled` | Enables the WebChat interface  |

## Customizing the Agent Prompt

The agent's system prompt is defined in `workspace/OPENCLAW.md`. Edit that file to change the agent's behavior. The current prompt instructs it to:
1. Generate a joke based on user input
2. Execute `joke_printer.py` to print the joke via code execution
