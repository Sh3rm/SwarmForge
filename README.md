# 🐝 SwarmForge

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Powered by](https://img.shields.io/badge/Powered_by-Antigravity_CLI-black.svg)](https://antigravity.google)
[![Agents](https://img.shields.io/badge/Sub--Agents-19-orange.svg)](#agent-roster)

A meta-agent system that designs and generates production-ready multi-agent swarms. Built for the [Google Antigravity (`agy`)](https://antigravity.google) CLI ecosystem.

You describe what you need. SwarmForge researches the domain, architects the agent hierarchy, writes every prompt and config file, validates the topology, and delivers a working swarm — ready to run with `agy`.

> Sister project of [HiveSmith](https://github.com/Sh3rm/HiveSmith) (the Claude Code edition): same architecture, same 19 agents, same 7-step pipeline — built on Antigravity's native primitives: custom agents, auto-loaded rules, workflows, and MCP config.

## How It Works

SwarmForge is itself a swarm. An orchestrator coordinates 19 specialized sub-agents through a 7-step pipeline (also invocable as the `/forge-swarm` workflow):

```
1. Information Gathering    — Fetch live model list, spawn domain researchers in parallel
2. Synthesis                — Merge raw research into a unified architectural baseline
3. Architecture             — Design the swarm blueprint with benchmark-driven model routing
4. Infrastructure & Safety  — Generate MCP configs, safety rules, telemetry, custom tools
5. Context Optimization     — Compress the payload without losing architectural logic
6. Persona Generation       — Write the target AGENTS.md, .agents/agents/*.md, rules, workflows
7. Evaluation & QA          — Simulate edge cases, validate DAG topology, verify dependencies
```

If QA or DAG validation finds issues, the pipeline loops back for refinement automatically.

## Key Design Decisions

- **Official Antigravity Schema.** Every persona is a real custom agent at `.agents/agents/<name>.md` with the documented frontmatter (`name`, `description`, `tools`, `model`, `subagent`, `inheritMcp`, `commandExecutionPolicy`) — so `invoke_subagent` resolves each one as a true isolated subagent. No legacy fields (`max_output_tokens`, `enable_*`, `planning-mode`): Antigravity drops or rejects them.

- **Team, Not Product.** When you ask for a swarm that builds something, the generated agents are the development *team* (developer, tester, reviewer roles) — never the product's own runtime components role-playing as agents. Ghost infrastructure, template stamping, and tool-wrapper agents are detected and rejected by the evaluation phase.

- **Dynamic Model Routing.** Agent frontmatter uses Antigravity's tier abstraction (`model: inherit | flash | pro`) instead of hardcoded model names, with `/effort` as the orthogonal reasoning-depth axis. The live roster comes from `.agents/model-list.txt` (operator-generated — see Quick Start) and current benchmarks are verified via live web search at the start of every job — tier names are marketing, benchmarks are truth.

- **Structural Safety.** Guardrails are enforced in frontmatter, not just prose: least-privilege `tools:` allowlists, `commandExecutionPolicy: off` for agents with no business running commands, `sandbox` for the rest, and scoped MCP access via `inheritMcp`.

- **Research Before Architecture.** Every generated swarm includes its own researcher agents. SwarmForge never relies on pre-trained knowledge for domain-specific decisions. It searches the web first, every time.

- **Tokenless Web Search.** Uses [duckduckgo-mcp-server](https://pypi.org/project/duckduckgo-mcp-server/) via `uvx`. No API keys, no rate limits, no cost.

- **Strict QA.** The `qa-validator` checks frontmatter schemas against the official Antigravity spec, detects template stamping and unfilled variables, audits MCP scope (no `/`-rooted filesystem servers, no unverified packages), runs dependency pre-flights (`uv`, `npx`), and validates directory structure before anything ships. The `dag-validator` additionally enforces acyclicity, reachability, the 10-level subagent nesting cap, and verified tool identifiers.

## Agent Roster

| Agent | Role | Tier |
|---|---|---|
| `domain-architect` | Designs swarm topology with benchmark-driven model selection | inherit |
| `persona-engineer` | Writes all system prompts (AGENTS.md, .agents/agents/*.md) | inherit |
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

SwarmForge is powered by the [Antigravity (`agy`)](https://antigravity.google) engine (CLI v1.1.6+ required for markdown custom agents).

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

Open `.agents/mcp_config.json` and change the path to your own projects directory:

```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/your/projects/path"]
}
```

> ⚠️ Do not set this to `/` or `C:\`. This path defines where AI agents can read and write files.

**4. Generate your model roster (required before each session where your model lineup may have changed):**

```bash
agy models < /dev/null > .agents/model-list.txt
```

> This must run in your own terminal, **outside** an agy session. The orchestrator reads this file because nested `agy` invocations crash inside Antigravity's command sandbox. The file is gitignored — every user has a different model lineup.

**5. Boot the swarm:**

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
├── .gitignore
└── .agents/
    ├── mcp_config.json                # MCP server configurations
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
    ├── rules/                         # Auto-loaded global rules (trigger-scoped)
    │   ├── 01-web-search-mandatory.md
    │   ├── 02-destructive-action-barrier.md
    │   ├── 03-agent-as-code-standard.md
    │   ├── 04-prompt-injection-shield.md
    │   ├── 05-idempotency-and-state.md
    │   ├── 06-human-in-the-loop.md
    │   ├── 07-conflict-resolution.md
    │   └── 08-blueprint-schema.md
    └── workflows/
        └── forge-swarm.md             # The 7-step pipeline as an invocable /forge-swarm workflow
```

## Global Rules

All agents (both SwarmForge's own and any it generates) operate under 8 global rules. Safety-critical rules are `always_on`; the rest activate via `model_decision` to keep context lean:

1. **Web Search Mandatory** *(always on)* — No hallucinated packages, versions, or configs
2. **Destructive Action Barrier** *(always on)* — No `rm -rf`, `DROP TABLE`, or cloud deletions without human approval; enforced structurally via `commandExecutionPolicy`
3. **Agent-as-Code Standard** — Official Antigravity file formats, frontmatter schema, tier-based model routing
4. **Prompt Injection Shield** *(always on)* — All external inputs treated as untrusted
5. **Idempotency & State Safety** — Operations must be safe to re-run
6. **Human-in-the-Loop** — Plan Mode + Artifacts checkpoints; agents pause and ask when facing critical ambiguity
7. **Conflict Resolution** — Orchestrator resolves inter-agent disagreements; safety wins by default
8. **Blueprint Schema** — Enforced JSON structure for all swarm blueprints

## Contributing

Contributions are welcome. If you have ideas for new agent types, improved safety rules, or better research strategies, feel free to open an issue or submit a pull request.

## License

Apache 2.0 — See [LICENSE](LICENSE) for details.
