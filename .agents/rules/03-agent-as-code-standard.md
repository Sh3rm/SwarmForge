---
trigger: model_decision
description: Apply when generating, editing, or validating any swarm workspace file — AGENTS.md, .agents/agents/*.md, .agents/skills/, .agents/rules/, .agents/workflows/, or mcp_config.json.
---

# The "Agent as Code" Standard

Every single sub-agent and orchestrator generated in this workspace MUST strictly adhere to the following physical and structural standards. These are Antigravity's real, documented conventions (CLI v1.1.8+; note the v1.1.7 breaking change: agents declaring `subagent: false` no longer appear in the available-subagents list; v1.1.8 changed nothing in the schema, tools, or rules — it is a print-mode/observability release) — deviation produces a swarm that Antigravity silently fails to load or that hangs at runtime. This applies to ALL generated swarms:

## 1. Physical Directory Structure
- **Orchestrator (`AGENTS.md`):** MUST be written directly to the project root directory (e.g., `<project-root>/AGENTS.md`). Plain markdown — Antigravity injects it into every prompt in that workspace.
- **Sub-Agents:** MUST be written to `.agents/agents/<agent-name>.md` — the CANONICAL emit form, field-proven across SwarmForge itself and every delivered swarm. (The directory form `.agents/agents/<agent-name>/agent.md` is equally official — the subagents doc documents both layouts — so validators ACCEPT it, but generators never EMIT it: one uniform layout per workspace.) One file per agent. Custom agent files placed outside an `agents/` subdirectory are silently undiscovered. NEVER use the `.agents/skills/<name>/SKILL.md` layout for worker personas — skills are reusable knowledge packs (frontmatter: `name` + `description` ONLY), not isolated agents.
- **Global Rules:** MUST be written to `.agents/rules/<rule-name>.md`. The four trigger types are now OFFICIALLY documented (antigravity.google/docs/rules-workflows): **Manual** (`@mention`), **Always On**, **Model Decision** (relevance judged from a natural-language `description`), and **Glob** (file-pattern match). House convention: safety-critical always-on rules use NO frontmatter at all — a bare markdown file in `.agents/rules/` auto-loads as always-on (field-proven form); conditional rules use `trigger: model_decision` + `description` (or `glob` + `globs`) — values MUST be exact strings from this enum, NEVER booleans (`trigger: true` silently breaks activation). Each rule file MUST stay under 12,000 characters.
- **Workflows:** Invocable pipelines belong in `.agents/workflows/<name>.md` (frontmatter: `description`), callable as `/<name>`.
- **Hooks (deterministic guards):** Configured in `.agents/hooks.json`; guard scripts live in `.agents/hooks/`. See §6 — this is the enforcement layer for the Destructive Action Barrier (Rule 02 §5).
- **Tooling (MCP):** MUST be written to `.agents/mcp_config.json` (top-level key `mcpServers`). Only add MCP servers for capabilities the native tools lack. Stdio servers use `command`/`args`/`env` (optionally `cwd`); remote servers use `serverUrl` (NOT `url`) plus optional `headers`, `authProviderType` (`google_credentials` for ADC), and `oauth`. Common optional keys: `disabled`, `disabledTools`. Secrets go in as `${VAR_NAME}` env-substitutions, never literals. Workspace config overrides the global `~/.gemini/config/mcp_config.json`.

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
- `tools` MUST be a least-privilege allowlist drawn EXCLUSIVELY from the **Canonical Tool List** — the only seven officially attested Antigravity identifiers: `view_file`, `replace_file_content`, `write_file`, `grep_search`, `list_dir`, `run_command`, `search_web`. **A misspelled or unmapped identifier HANGS the subagent process** (officially documented hazard) — field-proven hallucinations to reject on sight: `write_to_file`, `find_by_name`, `file_search`, `create_file`, `delete_file`. MCP tool names NEVER belong in `tools:` — MCP access flows through `inheritMcp`/`mcpServers` only. This exact seven-item list MUST be injected verbatim into every generation AND repair/refinement prompt; ad-hoc allowlists in fix loops are how invalid tools re-enter (field-proven: the first forge run needed three repair rounds because each round invented new identifiers).
- Workers are `mainAgent: false` + `subagent: true` (only `subagent: true` agents resolve via `invoke_subagent`; since v1.1.7, `subagent: false` agents are excluded from the subagent list). `mainAgent: true` and `subagent: true` on the same agent is a contradiction — the flags are mutually exclusive per file. Use `hidden: true` for purely internal helpers.
- `commandExecutionPolicy`: `off` for agents with no business executing commands; `sandbox` (default) for command-running agents. `auto`/`eager` require explicit human approval — and are CATEGORICALLY FORBIDDEN on agents whose commands mutate system state (firewall/network/service/database mutations); such agents get `sandbox` plus an explicit HITL confirmation step in their workflow before any permanent change.
- MCP access: `inheritMcp: true` to inherit the workspace servers, or a per-agent `mcpServers` list. Optional `skills:`/`plugins:` lists attach knowledge packs.

> **FORBIDDEN FIELDS:** `max_output_tokens`, `enable_write_tools`, `enable_mcp_tools`, `enable_subagent_tools`, `planning-mode`, `temperature`, `top_p`, `top_k`, `stop_sequences`. These are legacy/API-level fields — Antigravity drops them in frontmatter (and the Agent API rejects them with HTTP 400). Emitting them is a schema violation that `qa-validator` MUST reject.

## 3. Direct File Writes
Do NOT output massive markdown templates inside JSON strings when communicating. If your job is to generate a file, write it directly to the disk using your write tools.

## 4. Dynamic Model Routing (Future-Proof Optimization)
Google updates models constantly. Do NOT hardcode model version strings anywhere in generated files. Routing has two axes:
- **Tier (frontmatter):** `model: inherit | flash | pro`. Heavy reasoning roles (`domain-architect`, `persona-engineer`) run `inherit` on a top-tier orchestrator; high-speed scanners run `flash`.
- **Depth (runtime):** `/effort` (or `--effort`) tunes reasoning depth per delegation without changing models.
Alias→model resolution happens inside Antigravity at runtime, per user — no live roster is needed and the Orchestrator MUST NEVER run `agy` subcommands from the sandboxed terminal tool (nested `agy` crashes: `operation not permitted` on `installation_id`). Ground tier assignments in benchmark evidence gathered via live web search (Researcher Division / `search_web`) before finalizing — tier names are marketing; benchmarks are truth (mid-2026 field reality: Flash-family models outperformed legacy Pro models; re-verify each run).

## 5. Delegation Topology
- Only reference agents that exist as files with `subagent: true`.
- Respect Antigravity's 10-level subagent nesting cap.
- Choose workspace modes deliberately at invocation: `inherit` for read-only work, `branch` (isolated git worktree) for parallel writers, `share` for deliberate shared handoffs.

## 6. Hooks: The Deterministic Enforcement Layer
Rules and prompts are **advisory** — delivered as context, adjudicated by models. Any constraint that must hold with ZERO exceptions (destructive-command bans above all) MUST additionally be implemented as a hook, because hooks execute at the engine layer outside the model's discretion (official: antigravity.google/docs/hooks).
- **Where:** `hooks.json` in `.agents/` (workspace) or `~/.gemini/config/` (global); guard scripts in `.agents/hooks/`.
- **Events (5):** `PreToolUse` (gate a tool call before it runs), `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`.
- **Handler type:** only `command` (shell script; default 30s timeout, configurable per handler).
- **Entry shape:** `{"<hook-name>": {"enabled": true, "PreToolUse": [{"matcher": "<tool name or regex, e.g. run_command>", "hooks": [{"type": "command", "command": "<script path>", "timeout": 30}]}]}}`.
- **Contract:** the script receives the tool-call JSON on stdin (`toolCall` with `name` + `arguments`, plus `conversationId`, `workspacePaths`); for `PreToolUse` it responds on stdout with `{"decision": "allow"|"deny"|"ask"|"force_ask"}` — `deny` (or a non-zero exit code) hard-blocks the invocation and the model cannot override it.
- Generated swarms with a Destructive Action Barrier MUST ship a `PreToolUse` deny hook alongside the prose rule (see Rule 02 §5); SwarmForge's own `.agents/hooks/block-destructive.py` is the reference implementation.
