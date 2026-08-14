# Static Validator Usage

`scripts/validate_customizations.py` deterministically flags mechanical issues so the
assessor can spend reasoning budget on architecture. It has **no third-party dependencies**
(standard library only) and works cross-platform.

## Run

The cwd is the repo being assessed, not this skill's folder, so resolve the script's path
relative to this SKILL.md file rather than as a bare relative path:

```bash
# Human-readable report
python <path-to-this-skill-folder>/scripts/validate_customizations.py <scope-folder>

# Machine-readable (for the agent to parse)
python <path-to-this-skill-folder>/scripts/validate_customizations.py <scope-folder> --json
```

`<scope-folder>` is the folder holding customization files, typically `.github`, inside the
repo being assessed. If omitted, it defaults to `.github` under the current directory.

## What it checks

| Code | Check |
|------|-------|
| `FENCED_FRONTMATTER` | Frontmatter wrapped in a ` ``` ` code fence instead of raw `---`. |
| `MISSING_FRONTMATTER` | No `---` YAML frontmatter block found. |
| `INVALID_YAML` | Frontmatter is not parseable as key/value YAML. |
| `MISSING_DESCRIPTION` | No `description` field (discovery surface). |
| `SKILL_NAME_MISMATCH` | Skill `name` doesn't match its folder name. |
| `ABSOLUTE_PATH` | Hard-coded absolute path (e.g. `C:\Users\...`, `/home/...`). |
| `APPLYTO_WILDCARD` | `applyTo: "**"` — always-on, burns context. |
| `LARGE_FILE` | File exceeds the line threshold (bloated agent/instruction). |
| `POSSIBLE_SECRET` | Token/PAT/key-like string detected. |

## Options

- `--json` — emit findings as JSON.
- `--max-lines N` — line threshold for `LARGE_FILE` (default 200).
- `--quiet` — only print findings, suppress the summary.

## Notes

- The validator uses a minimal built-in YAML parser sufficient for frontmatter key/value
  pairs; it is intentionally conservative to avoid false negatives.
- Treat every hit as **evidence to confirm** by opening the file, not as a final verdict.
