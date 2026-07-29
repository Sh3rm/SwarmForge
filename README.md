# 🐝 SwarmForge

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Powered by](https://img.shields.io/badge/Powered_by-Antigravity_CLI-black.svg)](https://antigravity.google)
[![Agents](https://img.shields.io/badge/Sub--Agents-19-orange.svg)](#agent-roster)

A meta-agent system that designs and generates production-ready multi-agent swarms. Built for the [Google Antigravity (`agy`)](https://antigravity.google) CLI ecosystem.

You describe what you need. SwarmForge researches the domain, architects the agent hierarchy, writes every prompt and config file, validates the topology, and delivers a working swarm — ready to run with `agy`.

> Sister project of [HiveSmith](https://github.com/Sh3rm/HiveSmith) (the Claude Code edition): same architecture, same 19 agents, same pipeline — built on Antigravity's native primitives: custom agents, auto-loaded rules, workflows, and MCP config.

## How It Works

SwarmForge is itself a swarm. An orchestrator coordinates 19 specialized sub-agents through an interactive pre-flight step plus a 7-step pipeline. A plain natural-language request is the primary way to use it; `/forge-swarm` is an optional shortcut for the same pipeline:

```
0. Pre-Flight Disambiguation — Challenge vague requests with clarifying questions (skipped when the request is explicit)
1. Information Gathering     — Spawn domain researchers in parallel (incl. live model-benchmark verification)
2. Synthesis & Architecture  — Merge raw research into a unified baseline, then design the blueprint
3. Infrastructure & Safety   — Generate MCP configs, safety rules + guard hooks, telemetry, custom tools
4. Context Optimization      — Compress the payload without losing architectural logic
5. Persona Generation        — Write the target AGENTS.md, .agents/agents/*, rules, workflows; verify Step-3 deliverables (MCP config, guard hooks)
6. Evaluation & QA           — Simulate edge cases, audit anti-patterns, validate DAG topology and dependencies
7. Final Delivery            — Hand the validated swarm tree to the user as a reviewable Artifact
```

If QA or DAG validation finds issues, the pipeline loops back for refinement automatically.

## Key Design Decisions

- **Official Antigravity Schema.** Every persona is a real custom agent at `.agents/agents/<name>.md` with the documented frontmatter key set (`name`, `description`, `tools`, `model`, `mainAgent`, `subagent`, `hidden`, `inheritMcp`, `commandExecutionPolicy`, `mcpServers`, `skills`, `plugins`) — so `invoke_subagent` resolves each one as a true isolated subagent. `mainAgent: false` is always explicit (it defaults to TRUE when omitted — a field-proven trap). No legacy fields (`max_output_tokens`, `enable_*`, `planning-mode`, sampling params): Antigravity drops or rejects them.

- **The Generation Contract.** Workspace rules do not reliably reach subagent contexts, so every delegation to a generator or validator carries a mandatory verbatim payload: the Canonical Tool List, the required frontmatter key set, the known-good MCP registry, the quality/enforcement floor, and the user's original request text. A validator that receives a delegation without the contract refuses with `missing_contract` instead of validating blind.

- **Deterministic Guard Hooks.** The Destructive Action Barrier is not just prose: a `PreToolUse` hook (`.agents/hooks.json` + `.agents/hooks/block-destructive.py`) deterministically denies `rm -rf`, `mkfs`, force-pushes, SQL `DROP`s, and cloud resource deletions at the engine layer — the model cannot override a deny. Generated swarms ship the same dual layer with a domain-tailored pattern list.

- **Team, Not Product.** When you ask for a swarm that builds something, the generated agents are the development *team* (developer roles that implement AND test their own code, blackbox reviewers, docs writers) — never the product's own runtime components role-playing as agents. Ghost infrastructure, template stamping, and tool-wrapper agents are detected and rejected by the evaluation phase.

- **Dynamic Model Routing.** Agent frontmatter uses Antigravity's tier abstraction (`model: inherit | flash | pro`) instead of hardcoded model names, with `/effort` as the orthogonal reasoning-depth axis. Alias→model resolution happens inside Antigravity at runtime, per user — no model roster file is needed, and the orchestrator never runs `agy` subcommands (nested `agy` crashes in the sandbox). Current benchmarks are verified via live web search at the start of every job — tier names are marketing, benchmarks are truth.

- **Structural Safety.** Guardrails are enforced in frontmatter, not just prose: least-privilege `tools:` allowlists, `commandExecutionPolicy: off` for agents with no business running commands, `sandbox` for the rest, and scoped MCP access via `inheritMcp`.

- **Research Before Architecture.** Every generated swarm includes its own researcher agents. SwarmForge never relies on pre-trained knowledge for domain-specific decisions. It searches the web first, every time.

- **Tokenless Web Search.** Uses [duckduckgo-mcp-server](https://pypi.org/project/duckduckgo-mcp-server/) via `uvx`. No API keys, no rate limits, no cost.

- **Strict QA.** The `qa-validator` checks frontmatter schemas against the official Antigravity spec, detects template stamping and unfilled variables, audits MCP scope (no `/`-rooted filesystem servers, no unverified packages), verifies manifesto fidelity, research capacity, environment feasibility, guard hooks (with a live smoke-test), and destructive-ops policy, runs dependency pre-flights (`uv`, `npx`), and validates directory structure before anything ships. The `prompt-evaluator` additionally audits measured anti-patterns (Rule 09): phase-chain rosters, missing single-agent justification, soft verifiers, and bloated or hollow prompts. The `dag-validator` enforces acyclicity, reachability, the 10-level subagent nesting cap, and verified tool identifiers.

## Agent Roster

| Agent | Role | Tier |
|---|---|---|
| `domain-architect` | Designs swarm topology with benchmark-driven model selection | inherit |
| `persona-engineer` | Writes all system prompts (AGENTS.md, agents, rules, workflows) | inherit |
| `prompt-evaluator` | Simulates edge cases; ghost-infrastructure & roster-alignment scans | inherit |
| `safety-engineer` | Generates domain-specific safety rules | inherit |
| `tool-smith` | Builds custom scripts when standard MCP tools aren't enough | inherit |
| `memory-manager` | Designs shared context and persistence layers | inherit |
| `context-optimizer` | Compresses payloads without losing architectural logic | inherit |
| `mcp-integrator` | Generates `mcp_config.json` for the target swarm | inherit |
| `telemetry-architect` | Designs logging, tracing, and metrics standards | inherit |
| `researcher-google-cloud` | Google Cloud, Gemini, Antigravity best practices | inherit |
| `researcher-anthropic-openai` | Anthropic & OpenAI multi-agent patterns | inherit |
| `researcher-tech-stack` | Version verification, deprecation checks | inherit |
| `researcher-security` | OWASP, HITL, guardrail best practices | inherit |
| `researcher-academic-independent` | arXiv, independent AI research blogs | inherit |
| `researcher-vcs-github` | Mines GitHub/GitLab for existing agent configs; clones repos | inherit |
| `researcher-synthesizer` | Merges all research into a single baseline | inherit |
| `dag-validator` | Validates swarm topology — cycles, orphans, nesting cap, tool identifiers | inherit |
| `repo-analyzer-worker` | Fast concurrent scanning of cloned repos | flash |
| `qa-validator` | Schema validation, stamping detection, MCP audit, pass/fail reporting | inherit |

> SwarmForge's own roster is deliberately generously tiered (`inherit` = the orchestrator's top model): it is a creator, and output quality outranks token savings. Cost-aware tiering applies to the swarms it *generates*. Reasoning depth is tuned per delegation via `/effort`.

## 🚀 Quick Start

SwarmForge is powered by the [Antigravity (`agy`)](https://antigravity.google) engine (CLI v1.1.8+ — markdown custom agents; note v1.1.7's breaking change: `subagent: false` agents no longer resolve as subagents; v1.1.8 changed nothing in the schema).

**1. Prerequisites:**

- **[Antigravity CLI (`agy`)](https://antigravity.google)** — installed and authenticated
- **Node.js** — for `npx` (Filesystem MCP server)
- **[uv](https://docs.astral.sh/uv/)** — for `uvx` (DuckDuckGo MCP server)

**2. Clone this repository:**

```bash
git clone https://github.com/Sh3rm/SwarmForge.git
cd SwarmForge
```

**3. Configure filesystem access:**

Open `.agents/mcp_config.json` and change the path to the parent directory where your generated swarms should live:

```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/your/swarms/parent/path"]
}
```

> ⚠️ Do not set this to `/`, `~`, or `C:\`. This path defines where AI agents can read and write files.
>
> **Why does SwarmForge ship a filesystem server when its own doctrine forbids native-duplicating MCP servers?** Deliberate, documented exception: generated swarms are written into *sibling* directories outside SwarmForge's own workspace, which Antigravity's native file tools cannot reach. Scope it as narrowly as possible — the parent folder of your target swarm directories, nothing wider. Generated swarms themselves never receive a filesystem server.

**4. Boot the swarm:**

```bash
agy "Build me a Kubernetes monitoring swarm with Prometheus and Grafana integration"
```

Or invoke the pipeline explicitly as a workflow:

```bash
agy "/forge-swarm Build me a Kubernetes monitoring swarm with Prometheus and Grafana integration"
```

That's it. SwarmForge will research the domain, architect the agent hierarchy, write every prompt and config file, validate the output, and deliver a working swarm into your target directory.

## Project Structure

```
SwarmForge/
├── AGENTS.md                          # Orchestrator system prompt (plain markdown)
├── README.md
├── LICENSE
├── .gitignore
└── .agents/
    ├── mcp_config.json                # MCP server configurations
    ├── hooks.json                     # PreToolUse guard-hook wiring (deterministic layer)
    ├── hooks/
    │   └── block-destructive.py       # PreToolUse guard: deterministic Destructive Action Barrier
    ├── agents/                        # 19 sub-agent personas (official custom-agent format)
    │   ├── context-optimizer.md
    │   ├── dag-validator.md
    │   ├── domain-architect.md
    │   ├── mcp-integrator.md
    │   ├── memory-manager.md
    │   ├── persona-engineer.md
    │   ├── prompt-evaluator.md
    │   ├── qa-validator.md
    │   ├── repo-analyzer-worker.md
    │   ├── researcher-academic-independent.md
    │   ├── researcher-anthropic-openai.md
    │   ├── researcher-google-cloud.md
    │   ├── researcher-security.md
    │   ├── researcher-synthesizer.md
    │   ├── researcher-tech-stack.md
    │   ├── researcher-vcs-github.md
    │   ├── safety-engineer.md
    │   ├── telemetry-architect.md
    │   └── tool-smith.md
    ├── rules/                         # Auto-loaded global rules (always-on = frontmatter-free)
    │   ├── 01-web-search-mandatory.md
    │   ├── 02-destructive-action-barrier.md
    │   ├── 03-agent-as-code-standard.md
    │   ├── 04-prompt-injection-shield.md
    │   ├── 05-idempotency-and-state.md
    │   ├── 06-human-in-the-loop.md
    │   ├── 07-conflict-resolution.md
    │   ├── 08-blueprint-schema.md
    │   └── 09-swarm-quality-doctrine.md
    └── workflows/
        └── forge-swarm.md             # The Step 0-7 pipeline as an invocable /forge-swarm shortcut
```

## Global Rules

All agents (both SwarmForge's own and any it generates) operate under 9 global rules. Safety-critical rules are always-on (frontmatter-free files auto-load as always-on); the rest activate via `trigger: model_decision` to keep context lean — and every rule stays under Antigravity's 12,000-character limit:

1. **Web Search Mandatory** *(always on)* — No hallucinated packages, versions, or configs
2. **Destructive Action Barrier** *(always on)* — No `rm -rf`, `DROP TABLE`, or cloud deletions without human approval; enforced by a deterministic `PreToolUse` deny hook plus `commandExecutionPolicy`, not just prose
3. **Agent-as-Code Standard** — Official Antigravity file formats, frontmatter schema, hooks doctrine, tier-based model routing
4. **Prompt Injection Shield** *(always on)* — All external inputs treated as untrusted
5. **Idempotency & State Safety** — Operations must be safe to re-run
6. **Human-in-the-Loop** — Plan Mode + Artifacts checkpoints; agents pause and ask when facing critical ambiguity
7. **Conflict Resolution** — Orchestrator resolves inter-agent disagreements; safety wins by default
8. **Blueprint Schema** — Enforced JSON structure for all swarm blueprints, including decomposition justification, tier evidence, and guard-hook sections
9. **Swarm Quality Doctrine** — Measured anti-patterns encoded as hard checks: single-agent justification, context-boundary (not phase) decomposition, density-not-mass prompt budgets, verifier hardening, just-in-time context

## Contributing

Contributions are welcome. If you have ideas for new agent types, improved safety rules, or better research strategies, feel free to open an issue or submit a pull request.

## License

Apache 2.0 — See [LICENSE](LICENSE) for details.
