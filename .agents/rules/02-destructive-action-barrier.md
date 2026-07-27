# Global Rule: Destructive Action Barrier

All generated swarms and current meta-agents MUST NEVER execute destructive operations autonomously.

**Directives:**
1. Do NOT run `rm -rf`, `mkfs`, `drop database`, or AWS/GCP resource deletion commands.
2. If a destructive operation is required to proceed, the agent MUST explicitly request confirmation from the human operator via interactive prompt.
3. Enforce idempotency: Before creating any file, directory, or resource, check if it already exists to avoid unintended overwrites.
4. Enforce the barrier structurally, not just rhetorically: generated agents that have no business executing commands get `commandExecutionPolicy: off`; command-running agents default to `sandbox`. Never generate an agent with an unrestricted execution policy without explicit human approval.
