# Heartbeat — The Poet of the Pitch

Every heartbeat cycle, do the following:

1. Check `shared/mailbox/writer/inbox/` for new task files (ignore `.gitkeep` and `.done` files)
2. If a task exists, read it and create your creative response
3. Save the response to the requester's inbox (usually `shared/mailbox/coordinator/inbox/`)
4. Rename the processed task file by appending `.done`
5. If no tasks exist, write a spontaneous World Cup 2026 haiku and post it to `shared/mailbox/board/`
