#!/usr/bin/env python3
"""Request a Donald Trump joke from Ollama and print it via joke_printer.py."""

import json
import subprocess
import sys
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:latest"
PROMPT = "Generate one short, witty joke about Donald Trump. Just the joke, nothing else. Keep it under 3 sentences."


def get_joke() -> str:
    """Call Ollama to generate a Trump joke."""
    payload = json.dumps({
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False,
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
        return data["response"].strip()


def main():
    print("Requesting a Donald Trump joke from Ollama...")
    joke = get_joke()

    # Run joke_printer.py with the joke
    script = sys.path[0] + "/joke_printer.py" if sys.path[0] else "./joke_printer.py"
    subprocess.run([sys.executable, script, joke], check=True)


if __name__ == "__main__":
    main()
