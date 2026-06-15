# Configuration

Each swarm agent has its own config at `swarm/{role}/data/openclaw.json` (mounted into the container at `/home/node/.openclaw/openclaw.json`).

## Agent Config

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
        "id": "researcher",
        "name": "The Scout",
        "description": "Researches topics and reports findings",
        "tools": { "profile": "coding" },
        "thinking": { "level": "off" }
      }
    ]
  }
}
```

## Swarm Roles

| Agent ID | Name | Role |
|----------|------|------|
| `coordinator` | El Capitán | Assigns tasks, compiles results |
| `writer` | The Poet of the Pitch | Creative content generation |
| `critic` | VAR (Video Assistant Reviewer) | Quality assessment and review |
| `researcher` | The Scout | Fact-finding and research |

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

## Customizing Agent Prompts

Each agent's system prompt is defined in its `workspace/OPENCLAW.md`. Edit that file to change the agent's behavior and role instructions.
