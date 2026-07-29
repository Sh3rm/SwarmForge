---
trigger: model_decision
description: Apply when the domain-architect designs, outputs, or validates a swarm blueprint JSON.
---

# Global Rule: Swarm Blueprint JSON Schema

To ensure perfect interoperability, the `domain-architect` MUST always output the swarm design using the following strict JSON schema.

**Required JSON Structure:**
```json
{
  "swarm_name": "string",
  "version": "string",
  "domain": "string",
  "single_agent_justification": "string (REQUIRED — why one well-tooled agent cannot do this job: context pollution, true parallelism, or specialization threshold; multi-agent systems cost 3-15x tokens, so the burden of proof is on decomposition)",
  "execution_substrate": "string (REQUIRED for ops/infrastructure swarms — WHERE host commands run: 'local host' + required binaries, or the remote target + transport; omit only for pure code/document-producing swarms)",
  "constraint_consistency": ["string (record of each hard build/runtime constraint checked against every chosen dependency — e.g. 'CGO_ENABLED=0 vs libvirt binding: pure-Go digitalocean/go-libvirt selected')"],
  "work_items": ["string (OPTIONAL — the product's code deliverables; product components live HERE, never in the agent roster)"],
  "research_waiver": "string (OPTIONAL — only when the swarm deliberately ships zero research capacity; must state the explicit justification qa-validator will audit)",
  "agents": [
    {
      "id": "string",
      "role": "string",
      "model": "string ('inherit', 'flash', or 'pro' — Antigravity tier abstraction, never full model slugs; maps 1:1 to the agent frontmatter `model` key)",
      "tier_evidence": "string (REQUIRED when model is 'pro' — the benchmark citation URL proving the current Pro family beats the session model; omit otherwise)",
      "commandExecutionPolicy": "string (OPTIONAL — 'off'|'sandbox' design intent for the role; 'auto'/'eager' never on state-mutating agents)",
      "tools_required": ["string"],
      "dependencies": ["string"]
    }
  ],
  "hooks": [
    {
      "event": "string (OPTIONAL section — e.g. 'PreToolUse'; the guard hooks the swarm ships in .agents/hooks.json per Rule 02 §5)",
      "matcher": "string (tool name or regex, e.g. 'run_command')",
      "purpose": "string",
      "script_path": "string (e.g. '.agents/hooks/block-destructive.py')"
    }
  ],
  "mcp_servers": {
    "server_name": {
      "command": "string",
      "args": ["string"],
      "env": {},
      "source_url": "string (REQUIRED for any package outside the Known-Good Registry — the live verification URL; omit for registry entries)"
    }
  },
  "workflow_dag": {
    "edges": [
      {"from": "string", "to": "string"}
    ]
  }
}
```
*No deviation from this top-level key structure is permitted. The `work_items`, `research_waiver`, and `hooks` sections and the per-agent `tier_evidence`/`commandExecutionPolicy` keys are OPTIONAL — omit them entirely when not needed; when present they must follow the shapes above. Blueprint fields are design-layer: `id`, `role`, `tools_required`, `dependencies`, `tier_evidence` NEVER leak into generated agent frontmatter.*
