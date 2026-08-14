---
name: copilot-customization-assessment
description: 'Methodology for assessing a team''s GitHub Copilot customization files (custom agents, instructions, prompts, skills, hooks, MCP). Use when reviewing, auditing, or grading a repo''s .github Copilot setup for architecture, correctness, portability, cost, security, and alignment with current Copilot capabilities. Bundles a static validator, findings catalog, severity rubric, and review.md template.'
argument-hint: 'Path to the customization folder to assess (e.g. .github)'
---

# Copilot Customization Assessment

A repeatable procedure for producing a professional, evidence-based `review.md` of a
team's GitHub Copilot agentic-workflow implementation.

## When to Use

- Reviewing custom agents / instructions / prompts / skills across teams and repos.
- Auditing whether a Copilot setup matches **current** Copilot + IDE capabilities.
- Grading architecture quality, YAML correctness, path portability, model/credit cost,
  security, and logic duplication.

## Ground Rules

1. **Facts over memory.** Copilot changes fast. Verify every capability claim against the
   official docs at review time (see [official docs](./references/official-docs.md)) and
   cite the URL in the report.
2. **Constraints shape the verdict.** Confirm the team's IDE(s) and org-level restrictions
   first; a finding only holds if the feature is actually supported/allowed for them.
3. **Evidence for every finding.** Reference the exact file and line. Run the validator
   before reasoning about architecture so mechanical issues are caught deterministically.

## Procedure

1. **Confirm context.** Ensure intake answers exist: IDE(s), scope folder, known issues,
   org constraints, focus lenses. If missing, ask before proceeding.

2. **Ground capabilities.** Fetch the [official docs](./references/official-docs.md) for
   the confirmed IDE(s). Note which features are supported / preview / unsupported, and
   which are disabled at org level. This becomes your baseline of "what good looks like."

3. **Run the static validator.** Deterministically flags mechanical issues (markdown-fenced
   frontmatter, malformed YAML, absolute paths, missing descriptions, oversized files,
   name/folder mismatches). The cwd is the repo being assessed, not this skill's folder, so
   invoke the script via its path relative to this SKILL.md file, not a bare relative path:

   ```bash
   python <path-to-this-skill-folder>/scripts/validate_customizations.py <scope-folder> --json
   ```

   See [validator usage](./references/validator-usage.md). Treat its output as raw evidence,
   then confirm each hit by reading the file.

4. **Inventory.** Build a table of every customization file: type, purpose, model pinned,
   tools granted, size (lines), and paths referenced. Note duplication across files.

5. **Evaluate** each file and the system as a whole against the
   [findings catalog](./references/findings-catalog.md) and the
   [quality standards](./references/standards.md). Assess at least these dimensions:
   - **Architecture** — agent-per-task sprawl vs. skill/instruction-driven design.
   - **Frontmatter correctness** — valid YAML, no ` ```markdown ` wrappers, required fields.
   - **Agent leanness** — persona files thin; business logic/guardrails/standards in
     instructions; procedures in skills.
   - **Integration approach** — are premium/frontier models used for deterministic data
     fetching (e.g. ADO) that a script + CLI should handle? Flag AI-credit waste.
   - **Portability** — brittle absolute paths vs. relative paths.
   - **Duplication** — repeated logic/guardrails that belong in one shared instruction/skill.
   - **Capability fit** — reliance on features disabled at org level or unsupported in IDE.
   - **Security** — secrets, unrestricted tools, over-broad `applyTo: "**"`, injection risk.

6. **Rate severity** for each finding using the [severity rubric](./references/severity-rubric.md):
   Critical / High / Medium / Low, plus effort and impact.

7. **Write the report.** Produce `review.md` at the repo root using the
   [report template](./assets/review-template.md). Fill every section: executive summary,
   confirmed context & constraints, inventory, findings (grouped by severity with evidence,
   rationale + cited doc, and recommendation), a recommended target architecture, and a
   prioritized remediation roadmap.

## Output

A single `review.md` written in a precise, professional AI Solutions Architect voice —
findings that are specific, cited, severity-rated, and actionable.
