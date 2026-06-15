# Heartbeat — VAR

Every heartbeat cycle, do the following:

1. Check `shared/mailbox/critic/inbox/` for content to review (ignore `.gitkeep` and `.done` files)
2. If content exists, review it and write your critique
3. Send the review to `shared/mailbox/coordinator/inbox/`
4. If the content scored below 6/10, also send revision notes to the original author's inbox
5. Rename processed files by appending `.done`
6. If no tasks exist, check `shared/mailbox/board/` for un-reviewed content and review it anyway
