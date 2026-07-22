# The "Agent as Code" Standard

Every single sub-agent and orchestrator generated in this workspace MUST strictly adhere to the following physical and structural standards. This applies to ALL agents:

## 1. Physical Directory Structure
- **Orchestrator (`AGENTS.md`):** MUST be written directly to the project root directory (e.g., `<project-root>/AGENTS.md`).
- **Sub-Agent Skills (`SKILL.md`):** MUST be written to `.agents/skills/<skill-name>/SKILL.md`. Never write agent folders to the project root!
- **Global Rules:** MUST be written to `.agents/rules/<rule-name>.md`.
- **Tooling (MCP):** MUST be written to `.agents/mcp_config.json`.

## 2. YAML Frontmatter (CRITICAL)
Every generated `AGENTS.md` and `SKILL.md` file MUST begin with a strict YAML frontmatter block.
- You MUST include `model: <assigned-model>`.
- You MUST include `temperature: 0.1` and `top_p: 0.1`.
- You MUST include `max_output_tokens: 16384`.
- For `AGENTS.md`, you MUST include `planning-mode: true`.

**Example1 (Orchestrator):**
```yaml
---
model: <assigned-dynamically-from-agy-models>
temperature: 0.1
top_p: 0.1
max_output_tokens: 16384
planning-mode: true
enable_subagent_tools: true
enable_write_tools: true
---
```
**Example2 (Worker Agent):**
```yaml
---
name: agent-name
model: <assigned-dynamically-from-agy-models>
temperature: 0.1
top_p: 0.1
max_output_tokens: 16384
enable_write_tools: true
enable_mcp_tools: false
---
```
> **NOTE:** The Orchestrator assigns the actual model at runtime based on the live `agy models` list. Do NOT copy specific model names into generated files.

## 3. Direct File Writes
Do NOT output massive markdown templates inside JSON strings when communicating. If your job is to generate a file, write it directly to the disk using filesystem tools.

## 4. Dynamic Model Routing (Future-Proof Optimization)
Google updates models constantly. Do NOT hardcode model names (like `gemini-3.1-pro-high`) in your architectural designs. The Orchestrator MUST fetch the live list via `agy models` and route tasks dynamically:
- **Heavy Reasoning (High Effort/Thinking):** Assign to top-tier models (e.g., latest Pro or Claude Thinking variants) for `domain-architect`, `persona-engineer`, etc.
- **Data Synthesis (Medium Effort):** Assign to balanced models (e.g., Flash Medium variants) for research synthesis or context integration.
- **Fast Parsing (Low Effort):** Assign to fastest/cheapest models (e.g., Flash Low variants) for rapid scanning (`qa-validator`, `repo-analyzer-worker`).
