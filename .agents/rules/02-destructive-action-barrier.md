# Global Rule: Destructive Action Barrier

All generated swarms and current meta-agents MUST NEVER execute destructive operations autonomously.

**Directives:**
1. Do NOT run `rm -rf`, `mkfs`, `drop database`, or AWS/GCP resource deletion commands.
2. If a destructive operation is required to proceed, the agent MUST use the `<ask_user>` protocol and explicitly request confirmation from the human operator.
3. Enforce idempotency: Before creating any file, directory, or resource, check if it already exists to avoid unintended overwrites.
