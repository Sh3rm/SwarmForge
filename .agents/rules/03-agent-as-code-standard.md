---
trigger: model_decision
description: Apply when generating, editing, or validating any swarm workspace file — AGENTS.md, .agents/agents/*.md, .agents/skills/, .agents/rules/, .agents/workflows/, or mcp_config.json.
---

# The "Agent as Code" Standard

Every single sub-agent and orchestrator generated in this workspace MUST strictly adhere to the following physical and structural standards. These are Antigravity's real, documented conventions (CLI v1.1.6+) — deviation produces a swarm that Antigravity silently fails to load or that hangs at runtime. This applies to ALL generated swarms:

## 1. Physical Directory Structure
- **Orchestrator (`AGENTS.md`):** MUST be written directly to the project root directory (e.g., `<project-root>/AGENTS.md`). Plain markdown — Antigravity injects it into every prompt in that workspace.
- **Sub-Agents:** MUST be written to `.agents/agents/<agent-name>.md` (or `.agents/agents/<agent-name>/agent.md`) — one file per agent. Custom agent files placed outside an `agents/` subdirectory are silently undiscovered. NEVER use the `.agents/skills/<name>/SKILL.md` layout for worker personas — skills are reusable knowledge packs (frontmatter: `name` + `description` ONLY), not isolated agents.
- **Global Rules:** MUST be written to `.agents/rules/<rule-name>.md` with `trigger:` frontmatter (`always_on` for safety-critical rules; `model_decision` + `description`, or `glob` + `globs`, for the rest). Each rule file MUST stay under 12,000 characters.
- **Workflows:** Invocable pipelines belong in `.agents/workflows/<name>.md` (frontmatter: `description`), callable as `/<name>`.
- **Tooling (MCP):** MUST be written to `.agents/mcp_config.json` (top-level key `mcpServers`). Only add MCP servers for capabilities the native tools lack.

## 2. File Formats (CRITICAL)
- **Root `AGENTS.md` MUST NOT contain YAML frontmatter.** It is plain markdown. Execution mode is a runtime concern (`/plan`), and model selection lives in `/model`, `--model`, or per-agent frontmatter — never in the root file.
- **Every `.agents/agents/<name>.md` MUST begin with a YAML frontmatter block** using ONLY the official keys, followed by an H1-organized system prompt body:

```yaml
---
name: agent-name
description: Use this agent to <action-oriented trigger description — the planner uses this for delegation>.
model: inherit
mainAgent: false
subagent: true
inheritMcp: false
tools: [view_file, grep_search]
commandExecutionPolicy: off
---
```

- `name` MUST match the filename (without `.md`) and be unique.
- `description` MUST be action-oriented ("Use this agent to/when ...") so the orchestrator can delegate correctly.
- `model` MUST be the tier abstraction: `inherit` (parent's model), `flash`, or `pro`. NEVER a full model slug. Reasoning depth is the separate `/effort` axis.
- `tools` MUST be a least-privilege allowlist of VERIFIED Antigravity tool identifiers (e.g., `view_file`, `replace_file_content`, `grep_search`, `run_command`). **A misspelled or unmapped identifier HANGS the subagent process.** If a needed identifier cannot be verified, OMIT the `tools:` key and constrain via `commandExecutionPolicy` and `inheritMcp` instead.
- Workers are `mainAgent: false` + `subagent: true` (only `subagent: true` agents resolve via `invoke_subagent`). Use `hidden: true` for purely internal helpers.
- `commandExecutionPolicy`: `off` for agents with no business executing commands; `sandbox` (default) for command-running agents. `auto`/`eager` require explicit human approval.
- MCP access: `inheritMcp: true` to inherit the workspace servers, or a per-agent `mcpServers` list. Optional `skills:`/`plugins:` lists attach knowledge packs.

> **FORBIDDEN FIELDS:** `max_output_tokens`, `enable_write_tools`, `enable_mcp_tools`, `enable_subagent_tools`, `planning-mode`, `temperature`, `top_p`, `top_k`, `stop_sequences`. These are legacy/API-level fields — Antigravity drops them in frontmatter (and the Agent API rejects them with HTTP 400). Emitting them is a schema violation that `qa-validator` MUST reject.

## 3. Direct File Writes
Do NOT output massive markdown templates inside JSON strings when communicating. If your job is to generate a file, write it directly to the disk using your write tools.

## 4. Dynamic Model Routing (Future-Proof Optimization)
Google updates models constantly. Do NOT hardcode model version strings anywhere in generated files. Routing has two axes:
- **Tier (frontmatter):** `model: inherit | flash | pro`. Heavy reasoning roles (`domain-architect`, `persona-engineer`) run `inherit` on a top-tier orchestrator; high-speed scanners run `flash`.
- **Depth (runtime):** `/effort` (or `--effort`) tunes reasoning depth per delegation without changing models.
The Orchestrator MUST fetch the live roster via `agy models` and verify current benchmarks via web search before finalizing assignments — tier names are marketing; benchmarks are truth (as of mid-2026, Flash-family models outperform legacy Pro models).

## 5. Delegation Topology
- Only reference agents that exist as files with `subagent: true`.
- Respect Antigravity's 10-level subagent nesting cap.
- Choose workspace modes deliberately at invocation: `inherit` for read-only work, `branch` (isolated git worktree) for parallel writers, `share` for deliberate shared handoffs.
