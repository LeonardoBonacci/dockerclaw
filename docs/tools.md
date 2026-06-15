# Tool Use — Python Script Execution

OpenClaw supports native code execution as an agent tool. When `code_execution` is enabled in the agent's tools list, the agent can run scripts in the mounted `workspace/` directory.

## How It Works

1. User sends a message via WebChat (e.g., "Tell me a joke about cats")
2. The agent (Llama 3.1) generates a joke
3. The agent uses its code execution tool to run `joke_printer.py` with the joke
4. The script output is returned in the chat

This uses OpenClaw's native code execution capability — no MCP server needed.

## The Joke Printer Script

Located at `workspace/joke_printer.py`, this script:
- Accepts a joke (or topic) as a command-line argument
- Prints it with formatting
- Returns the output to the agent

## Adding More Scripts

Place any `.py` file in the `workspace/` directory. The agent can execute it if instructed via the system prompt or user message. The workspace is mounted at `/home/node/workspace` inside the container.

## Security Note

Code execution runs inside the container with access only to the mounted workspace volume. It cannot access the host filesystem beyond `./workspace` and `./data`.

## Standalone Script: trump_jokes.py

For headless/terminal use without the OpenClaw UI:

```bash
python3 workspace/trump_jokes.py
```

This script:
- Calls your local Ollama directly (no OpenClaw container needed)
- Generates a Donald Trump joke via Llama 3.1
- Pipes the result through `joke_printer.py` for formatted output

Requires only Ollama running locally on port 11434.
