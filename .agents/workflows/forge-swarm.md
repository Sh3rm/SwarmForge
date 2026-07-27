---
description: Run the full SwarmForge pipeline (Steps 0-7) — research, architect, generate, and validate a new multi-agent swarm for a given domain request.
---

# Workflow: Forge a New Swarm

Execute the complete SwarmForge generation pipeline for the swarm request given as the workflow argument. **The Execution Workflow section of `AGENTS.md` (Steps 0–7) is the single source of truth — follow it exactly; this workflow is only its invocable shortcut** (a plain natural-language request triggers the same pipeline without this command). Step numbers below match `AGENTS.md` one-to-one.

0. **Pre-Flight (Interactive):** Evaluate the request for ambiguity or missing technical constraints. If vague, PAUSE and challenge the user in Turkish with clarifying questions (per the HITL rule). For complex builds, enter Plan Mode and present the architecture as a reviewable Artifact before generation. If explicit and well-defined, proceed.
1. **Information Gathering (Parallel):** Apply the Model Routing Doctrine (AGENTS.md Constraint 9): tiers are aliases (`inherit | flash | pro`), grounded in live benchmark evidence — never run `agy` subcommands (nested `agy` crashes in the sandbox; no model roster is needed). Concurrently `invoke_subagent` the domain-relevant researchers (`researcher-tech-stack`, `researcher-google-cloud`, `researcher-security`, `researcher-vcs-github`, `researcher-academic-independent`, `researcher-anthropic-openai`) with the full Manifesto, including current-model benchmark verification. If a local codebase exists, also spawn `repo-analyzer-worker`. Wait for all reports.
2. **Synthesis & Architecture (Sequential):** Invoke `researcher-synthesizer` to merge the reports, then pass the baseline (including benchmark findings) to `domain-architect` and `memory-manager` for the blueprint and state design.
3. **Infrastructure & Safety (Parallel):** Concurrently invoke `mcp-integrator`, `tool-smith` (if custom scripts are needed), `safety-engineer`, and `telemetry-architect` — with `branch` workspace isolation, since they write files in parallel. Safety-engineer writes target rules FIRST and reports its numbering so later writers continue after it.
4. **Context Optimization (Sequential):** Invoke `context-optimizer` to compress the accumulated payload into a dense Manifesto without losing critical logic.
5. **Persona Generation:** Invoke `persona-engineer` to write the target workspace files (root `AGENTS.md`, `.agents/agents/*`, `.agents/rules/*.md`, `.agents/workflows/*.md`) and run its post-write existence sweep.
6. **Evaluation & Validation (Iterative):** Concurrently invoke `prompt-evaluator`, `qa-validator`, and `dag-validator`. Route failures back to `persona-engineer` (prompt defects) or `domain-architect` (category/topology errors) and re-validate — always re-injecting the Canonical Tool List and schema from rule 03 into every fix prompt.
7. **Final Delivery:** When green, deliver the final architectural tree to the user as a reviewable Artifact and contribute durable lessons to the workspace Knowledge Items.
