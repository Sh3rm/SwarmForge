# Global Rule: Destructive Action Barrier

All generated swarms and current meta-agents MUST NEVER execute destructive operations autonomously.

**Directives:**
1. Do NOT run `rm -rf`, `mkfs`, `drop database`, or AWS/GCP resource deletion commands.
2. If a destructive operation is required to proceed, execution PAUSES until the human operator confirms. Sub-agents have no channel to the human — they STOP and report the required operation back to the Orchestrator, which obtains confirmation through its own interaction with the operator (Plan Mode / Artifact review per the HITL rule) before re-delegating.
3. Enforce idempotency: Before creating any file, directory, or resource, check if it already exists to avoid unintended overwrites.
4. Enforce the barrier structurally, not just rhetorically: generated agents that have no business executing commands get `commandExecutionPolicy: off`; command-running agents default to `sandbox`. Never generate an agent with an unrestricted execution policy without explicit human approval.
5. **Deterministic enforcement (CRITICAL):** Prose rules and frontmatter policies are adjudicated by models; hooks are not. Every generated swarm MUST additionally ship a `PreToolUse` deny hook — a `hooks.json` entry (matcher `run_command`) plus a guard script in `<target-root>/.agents/hooks/` that returns `{"decision": "deny"}` on the target domain's destructive command patterns (e.g., `rm -rf`, `mkfs`, `git push --force`, `DROP DATABASE`, `terraform destroy`, `kubectl delete namespace`, `firewall-cmd --permanent` commits). The `safety-engineer` derives the domain-specific pattern list and writes both layers, modeling the script on SwarmForge's own `.agents/hooks/block-destructive.py`. Hook denial executes at the engine layer before the shell reaches the command — the model cannot override it (official: antigravity.google/docs/hooks).
