# Heartbeat — The Scout

Every heartbeat cycle, do the following:

1. Check `shared/mailbox/researcher/inbox/` for research requests (ignore `.gitkeep` and `.done` files)
2. If a request exists, compile your research brief and send it to the requester's inbox
3. Rename the processed request by appending `.done`
4. If no requests exist, post a "World Cup 2026 Fact of the Day" to `shared/mailbox/board/`
