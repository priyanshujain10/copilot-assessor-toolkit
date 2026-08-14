# Copilot Customization Standards

The guardrails and quality standards the assessor applies. This reference is part of the
`copilot-customization-assessment` skill (methodology). Keep individual agent files lean and
let them reference these standards rather than restating them.

## Grounding & Evidence

- **Never assert a capability from memory.** Verify against the current official docs and
  cite the URL. Copilot features change frequently.
- **Respect the team's IDE(s) and org constraints.** A recommendation that relies on a
  disabled or unsupported feature is invalid.
- **Every finding needs evidence** — the exact file and line.

## Architecture

- Prefer a **skill/instruction-driven** design over an **agent-per-task** design. Build a
  custom agent only for genuine context isolation or role-based tool restriction.
- Establish shared standards once in a repo-wide `copilot-instructions.md`; do not repeat
  them in every agent.
- Match the primitive to the purpose: always-on standards → **instructions**; one-off
  parameterized task → **prompt**; repeatable multi-step workflow with assets → **skill**;
  isolated/role-restricted persona → **agent**.

## Agent Leanness

- Agent files stay thin: **role + boundaries + short workflow**. No embedded business logic,
  coding standards, or long procedures.
- Put business logic, coding standards, and guardrails in **instructions**; put procedures
  and bundled assets in **skills**. Reference them from the agent.
- Grant the **minimal tool set** the role needs. Avoid `execute`/`edit`/wildcard MCP when
  read-only suffices.

## Frontmatter Correctness

- Frontmatter is **raw YAML between `---` markers** — never wrapped in a ` ```markdown `
  code fence.
- Quote values containing colons; use spaces, not tabs; keep valid indentation.
- Always provide a **keyword-rich `description`** (the discovery surface).
- Skill `name` must match its folder; use only supported frontmatter fields per primitive.
- Avoid `applyTo: "**"` unless the instruction is truly universal — it burns context on
  every request.

## Cost Efficiency

- **Do not use premium/frontier AI models for deterministic work** (e.g. fetching work items
  or tickets from Azure DevOps, Jira, GitHub Issues, etc.). Use scripts + CLIs/REST APIs
  (`az devops`, Jira REST, `gh`) instead — pick the tool matching the team's actual platform.
- Consolidate multiple integration agents wrapping the same system into one skill or a small
  set of scripts.
- Don't over-pin premium models; prefer defaults with a sensible fallback chain.

## Portability & Maintainability

- Use **relative paths** from the file to skills/instructions/scripts — never hard-coded
  absolute or machine-specific paths.
- Extract duplicated logic/guardrails into a single shared instruction/skill and reference
  it; do not copy-paste across files.
- Keep references valid; avoid orphaned links.

## Security

- No secrets/tokens/PATs in customization or script files.
- Least-privilege tools; scope `applyTo`; add guardrails for agents that ingest untrusted
  content and hold write/execute tools (prompt-injection risk).
