#!/usr/bin/env python3
"""Static validator for GitHub Copilot customization files.

Deterministically flags mechanical issues in custom agents, instructions, prompts, and
skills so an assessor can focus reasoning on architecture. Standard library only;
cross-platform.

Usage:
    python validate_customizations.py <scope-folder> [--json] [--max-lines N] [--quiet]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

# File globs that identify customization files.
CUSTOMIZATION_GLOBS = (
    "**/*.agent.md",
    "**/*.instructions.md",
    "**/*.prompt.md",
    "**/skills/**/SKILL.md",
    "copilot-instructions.md",
    "**/copilot-instructions.md",
    "AGENTS.md",
    "**/AGENTS.md",
)

# Conservative secret patterns (avoid matching ordinary prose).
SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),                    # GitHub PAT
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),            # GitHub fine-grained PAT
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),           # Slack token
    re.compile(r"AKIA[0-9A-Z]{16}"),                        # AWS access key id
    re.compile(r"(?i)\b(pat|token|api[_-]?key|secret|password)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
)

# Absolute path patterns (Windows drive path or Unix home path).
ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"[A-Za-z]:\\\\?(?:Users|Program Files|home)\b", re.IGNORECASE),
    re.compile(r"(?<![\w./])/(?:home|Users)/[A-Za-z0-9._-]+/"),
)


@dataclass
class Finding:
    code: str
    severity: str
    file: str
    line: int
    message: str


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def extract_frontmatter(text: str) -> tuple[str | None, int, str | None]:
    """Return (frontmatter_body, start_line, fence_lang_or_None).

    fence_lang is set when the frontmatter is wrapped in a ``` code fence (a defect).
    """
    lines = text.splitlines()
    # Detect a fenced block that wraps a --- frontmatter (the classic mistake).
    for i, line in enumerate(lines[:3]):
        m = re.match(r"^\s*```(\w+)?\s*$", line)
        if m:
            # A fence at the very top wrapping frontmatter-looking content.
            if any(l.strip() == "---" for l in lines[i + 1 : i + 3]):
                return None, i + 1, (m.group(1) or "")
    # Standard frontmatter: first non-empty line is ---.
    idx = 0
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if idx >= len(lines) or lines[idx].strip() != "---":
        return None, idx + 1, None
    for j in range(idx + 1, len(lines)):
        if lines[j].strip() == "---":
            return "\n".join(lines[idx + 1 : j]), idx + 2, None
    return None, idx + 1, None  # unterminated


def parse_simple_yaml(body: str) -> tuple[dict[str, str] | None, int | None]:
    """Minimal top-level key/value parser for frontmatter.

    Returns (mapping, error_line). Good enough to read description/name/applyTo. Returns
    (None, line) if a top-level line is neither a comment, list item, nested value, nor
    a `key:` pair.
    """
    result: dict[str, str] = {}
    for offset, raw in enumerate(body.splitlines()):
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if raw.startswith((" ", "\t", "-")):  # nested / list continuation
            continue
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not m:
            return None, offset + 1
        key, value = m.group(1), m.group(2).strip()
        result[key] = value.strip("'\"")
    return result, None


def check_file(path: Path, root: Path, max_lines: int) -> list[Finding]:
    findings: list[Finding] = []
    rel = _rel(path, root)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:  # boundary: unreadable file
        return [Finding("UNREADABLE", "Low", rel, 1, f"Could not read file: {exc}")]

    line_count = len(text.splitlines())
    fm_body, fm_line, fence_lang = extract_frontmatter(text)

    if fence_lang is not None:
        findings.append(Finding(
            "FENCED_FRONTMATTER", "Critical", rel, fm_line,
            f"Frontmatter is wrapped in a ```{fence_lang} code fence; use raw --- YAML delimiters.",
        ))
    elif fm_body is None:
        findings.append(Finding(
            "MISSING_FRONTMATTER", "High", rel, 1,
            "No YAML frontmatter block (--- ... ---) found.",
        ))
    else:
        mapping, err_line = parse_simple_yaml(fm_body)
        if mapping is None:
            findings.append(Finding(
                "INVALID_YAML", "High", rel, fm_line + (err_line or 1) - 1,
                "Frontmatter line is not a valid YAML key/value pair.",
            ))
            mapping = {}
        if "description" not in mapping or not mapping.get("description"):
            # copilot-instructions.md / AGENTS.md legitimately need no description.
            if path.name not in ("copilot-instructions.md", "AGENTS.md"):
                findings.append(Finding(
                    "MISSING_DESCRIPTION", "Medium", rel, fm_line,
                    "Missing 'description' — the discovery surface for this customization.",
                ))
        if mapping.get("applyTo", "").strip("'\"[] ") == "**":
            findings.append(Finding(
                "APPLYTO_WILDCARD", "Medium", rel, fm_line,
                "applyTo: \"**\" is always-on and burns context on every request; scope it.",
            ))
        if path.name == "SKILL.md":
            folder = path.parent.name
            name = mapping.get("name", "")
            if name and name != folder:
                findings.append(Finding(
                    "SKILL_NAME_MISMATCH", "High", rel, fm_line,
                    f"Skill name '{name}' does not match folder '{folder}'.",
                ))

    if line_count > max_lines:
        findings.append(Finding(
            "LARGE_FILE", "Medium", rel, 1,
            f"File has {line_count} lines (> {max_lines}); consider moving logic to instructions/skills.",
        ))

    for lineno, raw in enumerate(text.splitlines(), start=1):
        for pat in ABSOLUTE_PATH_PATTERNS:
            if pat.search(raw):
                findings.append(Finding(
                    "ABSOLUTE_PATH", "Medium", rel, lineno,
                    "Hard-coded absolute path; use a path relative to the file instead.",
                ))
                break
        for pat in SECRET_PATTERNS:
            if pat.search(raw):
                findings.append(Finding(
                    "POSSIBLE_SECRET", "Critical", rel, lineno,
                    "Possible committed secret/token; remove and rotate it.",
                ))
                break
    return findings


def collect_files(scope: Path) -> list[Path]:
    seen: set[Path] = set()
    for pattern in CUSTOMIZATION_GLOBS:
        for p in scope.glob(pattern):
            if p.is_file():
                seen.add(p.resolve())
    return sorted(seen)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Copilot customization files.")
    parser.add_argument("scope", nargs="?", default=".github",
                        help="Folder holding customization files (default: .github)")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    parser.add_argument("--max-lines", type=int, default=200,
                        help="Line threshold for LARGE_FILE (default 200).")
    parser.add_argument("--quiet", action="store_true", help="Suppress the summary line.")
    args = parser.parse_args(argv)

    scope = Path(args.scope)
    if not scope.exists():
        print(f"error: scope folder not found: {scope}", file=sys.stderr)
        return 2

    root = Path.cwd()
    files = collect_files(scope)
    findings: list[Finding] = []
    for f in files:
        findings.extend(check_file(f, root, args.max_lines))

    if args.json:
        print(json.dumps({
            "scope": str(scope),
            "files_scanned": len(files),
            "findings": [asdict(f) for f in findings],
        }, indent=2))
    else:
        for f in findings:
            print(f"[{f.severity:8}] {f.code:20} {f.file}:{f.line}  {f.message}")
        if not args.quiet:
            crit = sum(1 for f in findings if f.severity == "Critical")
            high = sum(1 for f in findings if f.severity == "High")
            print(f"\nScanned {len(files)} file(s): {len(findings)} finding(s) "
                  f"({crit} Critical, {high} High).")

    # Exit non-zero if any Critical/High findings, useful for CI gating.
    return 1 if any(f.severity in ("Critical", "High") for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
