#!/usr/bin/env python3
"""Install the Copilot Customization Assessor into a repository's .github folder.

Use this for consumers that don't load agent plugins (for example, JetBrains IDEs) or
teams that prefer to vendor the customizations directly into a repo. It copies the plugin's
`agents/` and `skills/` components into `<target>/.github/agents` and `<target>/.github/skills`.

The plugin remains the single source of truth; this script just projects it into a repo.

Usage:
    python scripts/install-into-repo.py <target-repo> [--force]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ("agents", "skills")


def copy_component(name: str, target_github: Path, force: bool) -> list[str]:
    src = PLUGIN_ROOT / name
    if not src.is_dir():
        return []
    dest = target_github / name
    copied: list[str] = []
    for item in src.rglob("*"):
        if not item.is_file():
            continue
        rel = item.relative_to(src)
        out = dest / rel
        if out.exists() and not force:
            print(f"skip (exists): {out}  (use --force to overwrite)")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, out)
        copied.append(str(out))
    return copied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install the assessor into a repo's .github folder.")
    parser.add_argument("target", help="Path to the target repository root.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args(argv)

    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"error: target repository not found: {target}", file=sys.stderr)
        return 2

    github = target / ".github"
    github.mkdir(exist_ok=True)

    total: list[str] = []
    for component in COMPONENTS:
        total.extend(copy_component(component, github, args.force))

    print(f"\nInstalled {len(total)} file(s) into {github}")
    print("Open the target repo in your IDE; the agent and skill will be discovered under .github/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
