# SwarmForge

A meta-agent system that designs and generates production-ready multi-agent swarms. Built for the [Google Antigravity (`agy`)](https://antigravity.google) CLI ecosystem.

You describe what you need. SwarmForge researches the domain, architects the agent hierarchy, writes every prompt and config file, validates the output, and delivers a working swarm — ready to run with `agy`.

## How It Works

SwarmForge is itself a swarm. An orchestrator coordinates 18 specialized sub-agents through a 7-step pipeline:

```
1. Information Gathering    — Fetch live model list, spawn domain researchers in parallel
2. Synthesis                — Merge raw research into a unified architectural baseline
3. Architecture             — Design the swarm blueprint with benchmark-driven model routing
4. Infrastructure & Safety  — Generate MCP configs, safety rules, telemetry, custom tools
5. Context Optimization     — Compress the payload without losing architectural logic
6. Persona Generation       — Write all AGENTS.md and SKILL.md files to disk
7. Evaluation & QA          — Simulate edge cases, validate schemas, verify dependencies
```

If QA finds issues, the pipeline loops back to step 6 automatically.

## Key Design Decisions

- **Dynamic Model Routing.** SwarmForge runs `agy models` at the start of every job and assigns models based on live availability and current benchmarks — not hardcoded names. When Google or Anthropic ships a new model, SwarmForge picks it up on the next run without any code changes.

- **Research Before Architecture.** Every generated swarm includes its own researcher agents. SwarmForge never relies on pre-trained knowledge for domain-specific decisions. It searches the web first, every time.

- **Tokenless Web Search.** Uses [duckduckgo-mcp-server](https://pypi.org/project/duckduckgo-mcp-server/) via `uvx`. No API keys, no rate limits, no cost.

- **Strict QA.** The `qa-validator` checks YAML frontmatter schemas, verifies model names against the live model list, runs dependency pre-flights (`uv`, `npx`), and validates directory structure before anything ships.

## Agent Roster

| Agent | Role | Default Tier |
|---|---|---|
| `domain-architect` | Designs swarm topology with benchmark-driven model selection | Pro / High |
| `persona-engineer` | Writes all system prompts (AGENTS.md, SKILL.md) | Pro / High |
| `prompt-evaluator` | Simulates edge cases against generated prompts | Pro / High |
| `safety-engineer` | Generates domain-specific safety rules | Pro / High |
| `tool-smith` | Builds custom scripts when standard MCP tools aren't enough | Pro / High |
| `memory-manager` | Designs shared context and persistence layers | Pro / High |
| `context-optimizer` | Compresses payloads without losing architectural logic | Flash / High |
| `mcp-integrator` | Generates `mcp_config.json` for the target swarm | Flash / High |
| `telemetry-architect` | Designs logging, tracing, and metrics standards | Flash / Medium |
| `researcher-google-cloud` | Google Cloud, Gemini, Antigravity best practices | Flash / Medium |
| `researcher-anthropic-openai` | Anthropic & OpenAI multi-agent patterns | Flash / Medium |
| `researcher-tech-stack` | Version verification, deprecation checks | Flash / Medium |
| `researcher-security` | OWASP, HITL, guardrail best practices | Flash / Medium |
| `researcher-academic-independent` | arXiv, independent AI research blogs | Flash / Medium |
| `researcher-vcs-github` | Mines GitHub/GitLab for existing agent configs | Flash / Medium |
| `researcher-synthesizer` | Merges all research into a single baseline | Pro / High |
| `repo-analyzer-worker` | Fast concurrent scanning of cloned repos | Flash / Low |
| `qa-validator` | Schema validation, dependency checks, pass/fail reporting | Flash / Low |

> "Default Tier" is a fallback. The orchestrator overrides these at runtime based on the live `agy models` list.

## Prerequisites

- **[Antigravity CLI (`agy`)](https://antigravity.google)** — installed and authenticated
- **Node.js** — for `npx` (Filesystem MCP server)
- **[uv](https://docs.astral.sh/uv/)** — for `uvx` (DuckDuckGo MCP server)

## Setup

```bash
git clone https://github.com/your-username/swarmforge.git
cd swarmforge
```

**Configure filesystem access:**

Open `.agents/mcp_config.json` and change the path to your own projects directory:

```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/your/projects/path"]
}
```

> ⚠️ Do not set this to `/` or `C:\`. This path defines where AI agents can read and write files.

**Model configuration is automatic.** The `model` fields in skill files are fallback defaults. At runtime, the orchestrator runs `agy models`, reads the output, and dynamically assigns the best available model to each sub-agent based on task complexity. You don't need to edit model names manually.

## Project Structure

```
swarmforge/
├── AGENTS.md                          # Orchestrator system prompt
├── README.md
├── .gitignore
└── .agents/
    ├── mcp_config.json                # MCP server configurations
    ├── rules/
    │   ├── 01-web-search-mandatory.md
    │   ├── 02-destructive-action-barrier.md
    │   ├── 03-agent-as-code-standard.md
    │   ├── 04-prompt-injection-shield.md
    │   ├── 05-idempotency-and-state.md
    │   ├── 06-human-in-the-loop.md
    │   ├── 07-conflict-resolution.md
    │   └── 08-blueprint-schema.md
    └── skills/
        ├── context-optimizer/
        ├── domain-architect/
        ├── mcp-integrator/
        ├── memory-manager/
        ├── persona-engineer/
        ├── prompt-evaluator/
        ├── qa-validator/
        ├── repo-analyzer-worker/
        ├── researcher-academic-independent/
        ├── researcher-anthropic-openai/
        ├── researcher-google-cloud/
        ├── researcher-security/
        ├── researcher-synthesizer/
        ├── researcher-tech-stack/
        ├── researcher-vcs-github/
        ├── safety-engineer/
        ├── telemetry-architect/
        └── tool-smith/
```

## Global Rules

All agents (both SwarmForge's own and any it generates) operate under 8 global rules:

1. **Web Search Mandatory** — No hallucinated packages, versions, or configs
2. **Destructive Action Barrier** — No `rm -rf`, `DROP TABLE`, or cloud deletions without human approval
3. **Agent-as-Code Standard** — Strict YAML frontmatter, directory topology, dynamic model routing
4. **Prompt Injection Shield** — All external inputs treated as untrusted
5. **Idempotency & State Safety** — Operations must be safe to re-run
6. **Human-in-the-Loop** — Agents pause and ask when facing critical ambiguity
7. **Conflict Resolution** — Orchestrator resolves inter-agent disagreements; safety wins by default
8. **Blueprint Schema** — Enforced JSON structure for all swarm blueprints

## License

Apache 2.0 — See [LICENSE](LICENSE) for details.
