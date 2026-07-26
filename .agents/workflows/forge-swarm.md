---
description: Run the full SwarmForge 7-step pipeline — research, architect, generate, and validate a new multi-agent swarm for a given domain request.
---

# Workflow: Forge a New Swarm

Execute the complete SwarmForge generation pipeline for the swarm request given as the workflow argument. Follow the Execution Workflow in `AGENTS.md` exactly; this workflow is its invocable form.

1. **Pre-Flight (Interactive):** Evaluate the request for ambiguity or missing technical constraints. If vague, PAUSE and challenge the user in Turkish with clarifying questions (per the HITL rule). For complex builds, enter Plan Mode and present the architecture as a reviewable Artifact before generation. If explicit and well-defined, proceed.
2. **Information Gathering (Parallel):** Run `agy models < /dev/null > .agents/model-list.txt` and read the file to capture the live model roster (direct stdout capture is unreliable under asynchronous execution). Concurrently `invoke_subagent` the domain-relevant researchers (`researcher-tech-stack`, `researcher-google-cloud`, `researcher-security`, `researcher-vcs-github`, `researcher-academic-independent`, `researcher-anthropic-openai`) with the full Manifesto. If a local codebase exists, also spawn `repo-analyzer-worker`. Wait for all reports.
3. **Synthesis & Architecture (Sequential):** Invoke `researcher-synthesizer` to merge the reports, then pass the baseline plus the live model roster to `domain-architect` and `memory-manager` for the blueprint and state design.
4. **Infrastructure & Safety (Parallel):** Concurrently invoke `mcp-integrator`, `tool-smith` (if custom scripts are needed), `safety-engineer`, and `telemetry-architect` — with `branch` workspace isolation, since they write files in parallel.
5. **Context Optimization (Sequential):** Invoke `context-optimizer` to compress the accumulated payload into a dense Manifesto without losing critical logic.
6. **Persona Generation:** Invoke `persona-engineer` to write the target workspace files (root `AGENTS.md`, `.agents/agents/*.md`, `.agents/rules/*.md`, `.agents/workflows/*.md`).
7. **Evaluation & Delivery (Iterative):** Concurrently invoke `prompt-evaluator`, `qa-validator`, and `dag-validator`. Route failures back to `persona-engineer` (prompt defects) or `domain-architect` (category/topology errors) and re-validate. When green, deliver the final architectural tree to the user as a reviewable Artifact and contribute durable lessons to the workspace Knowledge Items.
