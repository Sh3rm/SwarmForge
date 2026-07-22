# Meta-Agent Swarm Memory

This file serves as the long-term persistence layer for the Apex Meta-Agent (Swarm Creator). It records architectural decisions, user preferences, and lessons learned across different sessions to ensure continuous improvement and flawless execution.

## 1. Human Operator Preferences
- **Web Search:** Prefers tokenless, free MCP alternatives (e.g., DuckDuckGo) over metered APIs (Brave/Tavily) when possible.
- **Model Routing:** Strictly enforces Dynamic Model Routing — Orchestrator fetches live `agy models` list at runtime and assigns models by cognitive load tier (High/Medium/Low), never by hardcoded name.
- **QA Standards:** Prefers hyper-strict validation (exact schema matching) over naive structural checks.

## 2. Global Architectural Lessons (Learned the Hard Way)
- **YAML Frontmatter (Session 1):** Always ensure new `SKILL.md` files strictly include `temperature: 0.1`, `top_p: 0.1`, and `max_output_tokens: 16384`. Never assume the blueprint generator adds them automatically.
- **Dependency Pre-flights:** Always ensure runtime dependencies (like `uv` or `npx`) are checked before launching MCP tools, to prevent silent crashes.
