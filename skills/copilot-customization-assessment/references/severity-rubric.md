# Severity Rubric

Rate every finding on **severity**, and annotate **effort** and **impact** to support a
prioritized roadmap.

## Severity levels

| Level | Definition | Examples |
|-------|------------|----------|
| **Critical** | Breaks functionality, leaks secrets, or relies on a disabled/unsupported capability so the workflow cannot work as intended. | Secret committed in a file; frontmatter fenced in ` ```markdown ` so the agent never loads; hard dependency on a feature disabled at org level. |
| **High** | Significant architecture, cost, or maintainability problem that materially degrades reliability or wastes premium AI credits. | Agent-per-task sprawl; premium model used for deterministic ADO fetches; duplicated guardrails across many agents. |
| **Medium** | Correctness or portability issue that causes intermittent failures or friction but has a clear workaround. | Brittle absolute paths; weak/missing descriptions; bloated agent files; over-broad `applyTo: "**"`. |
| **Low** | Style, consistency, or minor hygiene issue with limited functional impact. | Inconsistent naming; minor redundancy; missing optional metadata. |

## Effort (to remediate)

- **S** — minutes, mechanical (fix frontmatter, swap to relative path).
- **M** — hours, localized refactor (convert an agent to a skill).
- **L** — days, structural (re-architect agent-per-task into skill-driven design).

## Impact (if fixed)

- **High / Medium / Low** — expected improvement in reliability, cost, or maintainability.

## Finding format (used in review.md)

```
### [SEVERITY] <short title>  (Effort: S/M/L · Impact: High/Med/Low)
- **Evidence:** <file path>#L<line> — <what was observed>
- **Why it matters:** <rationale, grounded in a cited official doc URL>
- **Recommendation:** <specific, actionable fix, with a corrected snippet where useful>
```

## Prioritization

Order the remediation roadmap by severity first, then by lowest effort / highest impact —
so the team gets the biggest reliability and cost wins fastest.
