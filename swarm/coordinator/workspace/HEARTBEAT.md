# Heartbeat — El Capitán

Every heartbeat cycle, do the following:

1. Check `shared/mailbox/coordinator/inbox/` for new response files
2. If responses exist, read them and compile a summary
3. Post any compiled bulletins to `shared/mailbox/board/`
4. If the board has no fresh content today, assign a new World Cup 2026 topic to the team
