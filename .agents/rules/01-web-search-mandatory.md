# Global Rule: Mandatory Web Search Validation

Every agent with live search capability (native `search_web`, or an inherited search MCP such as `duckduckgo-search`) MUST validate domain assumptions, library versions, API endpoints, and configuration parameters via web search before asserting them. Agents WITHOUT search capability MUST NOT compensate by guessing — they flag the unverified claim for the Orchestrator to route to a researcher.

**Directives:**
1. Never hallucinate OS packages, cloud services, or codebase implementations.
2. If you are generating a swarm configuration, you must fetch the officially recommended patterns from Anthropic, Google, OpenAI, or the target platform's documentation.
3. Reject deprecated tools and outdated Linux methodologies (e.g., `network-scripts` on RHEL 9/10). Find the modern equivalent via Web Search.
