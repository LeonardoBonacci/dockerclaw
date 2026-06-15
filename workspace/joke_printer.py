#!/usr/bin/env python3
"""Joke printer — called by the OpenClaw agent to print a generated joke."""

import sys


def print_joke(joke: str) -> str:
    """Format and print a joke."""
    output = f"\n{'=' * 40}\n  {joke}\n{'=' * 40}\n"
    print(output)
    return output


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "Why did the programmer quit? Because they didn't get arrays!"
    print_joke(text)
