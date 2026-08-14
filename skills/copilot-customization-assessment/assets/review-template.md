# GitHub Copilot Customization Review

> AI Solutions Architect assessment of the team's Copilot agentic-workflow implementation.
> Replace every `<…>` placeholder. Delete guidance lines before finalizing.

- **Assessed scope:** `<folder / repo>`
- **Assessor:** Copilot Customization Assessor
- **Date:** `<YYYY-MM-DD>`
- **Primary IDE(s):** `<VS Code / Visual Studio / JetBrains / mixed>`
- **Org constraints:** `<e.g. Copilot CLI, MCP, cloud agents, hooks disabled; repos on Azure DevOps>`
- **Focus lenses:** `<architecture / cost / correctness / portability / security>`

---

## 1. Executive Summary

`<3–6 sentences: overall maturity, the single biggest risk, the highest-value change, and
the recommended architectural direction. State the number of findings by severity.>`

| Severity | Count |
|----------|------:|
| Critical | `<n>` |
| High | `<n>` |
| Medium | `<n>` |
| Low | `<n>` |

## 2. Confirmed Context & Capability Baseline

`<What was confirmed with the assessor and verified against official docs. List each
capability claim with its cited doc URL. Note which features are disabled at org level or
unsupported in the team's IDE(s), since these bound what "good" looks like.>`

- Capability baseline verified against: `<doc URLs>`
- Disabled/unsupported (excluded from recommendations): `<…>`

## 3. Inventory

| File | Type | Purpose | Model pinned | Tools | Lines | Notes |
|------|------|---------|--------------|-------|------:|-------|
| `<path>` | agent/instr/prompt/skill | `<…>` | `<…>` | `<…>` | `<n>` | `<…>` |

## 4. Findings

> Grouped by severity, highest first. Each finding cites file + line, explains why it
> matters (with a cited doc), and gives a concrete recommendation.

### Critical

#### [Critical] `<short title>`  (Effort: S/M/L · Impact: High/Med/Low)
- **Evidence:** `<file>#L<line>` — `<what was observed>`
- **Why it matters:** `<rationale grounded in cited official doc URL>`
- **Recommendation:** `<specific fix; include a corrected snippet where useful>`

### High

#### [High] `<short title>`  (Effort: … · Impact: …)
- **Evidence:** `<file>#L<line>`
- **Why it matters:** `<…>`
- **Recommendation:** `<…>`

### Medium

#### [Medium] `<short title>`  (Effort: … · Impact: …)
- **Evidence:** `<file>#L<line>`
- **Why it matters:** `<…>`
- **Recommendation:** `<…>`

### Low

#### [Low] `<short title>`  (Effort: … · Impact: …)
- **Evidence:** `<file>#L<line>`
- **Why it matters:** `<…>`
- **Recommendation:** `<…>`

## 5. Recommended Target Architecture

`<Describe the "to-be" design: a lean set of agents for genuine context isolation, a
repo-wide copilot-instructions.md for shared standards, task-specific instructions files,
skills for repeatable multi-step workflows, and deterministic scripts (e.g. Python + Azure
CLI) for external-system integration instead of premium-model calls. A simple before/after
diagram helps.>`

```
<optional before → after sketch>
```

## 6. Remediation Roadmap

> Ordered by severity, then lowest effort / highest impact.

| # | Finding | Severity | Effort | Impact | Owner | Action |
|--:|---------|----------|--------|--------|-------|--------|
| 1 | `<…>` | Critical | S | High | `<…>` | `<…>` |
| 2 | `<…>` | High | M | High | `<…>` | `<…>` |

## 7. Appendix — Validator Output

`<Paste the raw output of scripts/validate_customizations.py for traceability.>`
