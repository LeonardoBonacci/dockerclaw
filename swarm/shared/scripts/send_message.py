#!/usr/bin/env python3
"""Send a message to another agent's inbox.

Usage: python3 send_message.py <recipient> <subject> <body> [sender]
Recipients: coordinator, writer, critic, researcher
"""

import os
import sys
import time

MAILBOX_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mailbox")


def send(recipient: str, subject: str, body: str, sender: str = "unknown"):
    inbox = os.path.join(MAILBOX_ROOT, recipient, "inbox")
    os.makedirs(inbox, exist_ok=True)

    timestamp = int(time.time() * 1000)
    filename = f"task-{timestamp}.md"
    filepath = os.path.join(inbox, filename)

    content = f"""# Message from {sender}
**To:** {recipient}
**Subject:** {subject}
**Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

{body}
"""
    with open(filepath, "w") as f:
        f.write(content)

    print(f"✉️  Sent to {recipient}: {filename}")
    return filepath


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <recipient> <subject> <body> [sender]")
        sys.exit(1)

    recipient = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    sender = sys.argv[4] if len(sys.argv) > 4 else "human"

    send(recipient, subject, body, sender)
