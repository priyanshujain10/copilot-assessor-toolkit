# Findings Catalog

A checklist of recurring issues in Copilot customization implementations. For each, confirm
against the actual files (with line numbers) and current official docs before reporting.
Map each confirmed issue to a severity using the [severity rubric](./severity-rubric.md).

## A. Architecture & Design

- **A1. Agent-per-task sprawl.** A separate custom agent built for nearly every task. Most
  should be **skills** (on-demand workflows) or **instructions** (always-on standards).
  Reserve custom agents for genuine context isolation or role-based tool restriction.
- **A2. Swiss-army agents.** A single agent granted broad tools trying to do everything.
  Split by role or convert to skills.
- **A3. Wrong primitive.** Standards modeled as prompts, one-off tasks modeled as agents,
  multi-step workflows crammed into instructions. Match primitive to purpose.
- **A4. No shared foundation.** No repo-wide `copilot-instructions.md` establishing common
  standards, so every agent re-states them.

## B. Frontmatter & Format Correctness

- **B1. Markdown-fenced frontmatter.** Frontmatter wrapped in ` ```markdown ` … ` ``` `
  instead of raw `---` YAML delimiters. Silently breaks parsing.
- **B2. Invalid YAML.** Unquoted values containing colons, tabs, bad indentation, unquoted
  glob strings. Causes silent load failures.
- **B3. Missing/weak `description`.** The discovery surface. Without keyword-rich
  descriptions, skills/instructions/agents are never auto-selected.
- **B4. Name/folder mismatch.** Skill `name` doesn't match its folder; agent `name`
  inconsistent with filename.
- **B5. Wrong or unknown fields.** Frontmatter keys not supported by the primitive/IDE.

## C. Agent Leanness

- **C1. Bloated agent files.** Persona files stuffed with business logic, coding standards,
  and long procedures. Keep agents thin: role + boundaries + workflow. Move standards to
  **instructions**, procedures to **skills**.
- **C2. Embedded guardrails.** Safety/guardrail rules duplicated inside each agent instead
  of centralized in an instructions file referenced by all.

## D. Integration & Cost Efficiency

- **D1. AI for deterministic work.** Using premium/frontier models to fetch or manipulate
  data that a script + CLI can do deterministically (e.g. reading ADO work items). Wastes
  premium AI credits and adds nondeterminism. Prefer `.py` scripts using the Azure CLI /
  `az devops` / REST API.
- **D2. Redundant integration agents.** Multiple agents wrapping the same external system
  (e.g. three ADO agents). Consolidate into one skill or a small set of scripts.
- **D3. Over-pinned premium models.** Pinning frontier models where a smaller/default model
  suffices; no fallback chain.

## E. Portability & Maintainability

- **E1. Brittle absolute paths.** Hard-coded machine/user paths (e.g. `C:\Users\...`,
  `/home/<user>/...`) to skills/instructions/scripts. Use **relative** paths from the file.
- **E2. Logic duplication.** The same instructions/guardrails/steps copy-pasted across
  multiple files. Extract into a single shared instruction/skill and reference it.
- **E3. Orphaned references.** Links to files/scripts that don't exist or moved.

## F. Capability Fit (org & IDE constraints)

- **F1. Relies on disabled features.** Uses/recommends Copilot CLI, MCP, cloud agents, or
  hooks when disabled at org level.
- **F2. Unsupported in target IDE.** Depends on a feature marked unsupported/preview for the
  team's IDE in the current feature matrix.
- **F3. Non-portable across the team's IDEs.** Setup assumes one IDE when the team is mixed
  (e.g. VS Code + JetBrains).

## G. Security

- **G1. Secrets in files.** Tokens/PATs/keys committed in customization or script files.
- **G2. Over-broad tool grants.** Agents given `execute`/`edit`/MCP wildcard when read-only
  would do.
- **G3. `applyTo: "**"` overuse.** Always-on instruction burning context on every request.
- **G4. Prompt-injection exposure.** Agents that ingest untrusted content with write/execute
  tools and no guardrails.
