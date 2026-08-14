# Copilot Customization Assessor — Agent Plugin

A GitHub Copilot **agent plugin** for **assessing how teams implement Copilot agentic
workflows** — across different projects and architectural patterns — and producing a
professional, evidence-based `review.md`.

The toolkit always **grounds its facts on the current, officially published capabilities**
of GitHub Copilot and the target IDE, and adapts to each team's IDE(s) and org-level
constraints through a short dynamic interview.

This repo is packaged as an [agent plugin](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
(Copilot format) and doubles as its own plugin marketplace.

## Plugin contents

| Component | Path | Role |
|-----------|------|------|
| Custom agent | [agents/copilot-customization-assessor.agent.md](agents/copilot-customization-assessor.agent.md) | Lean AI Solutions Architect persona that runs the assessment. |
| Methodology skill | [skills/copilot-customization-assessment/SKILL.md](skills/copilot-customization-assessment/SKILL.md) | Step-by-step procedure + bundled standards, catalog, rubric, validator, and template. |
| Plugin manifest | [plugin.json](plugin.json) | Declares the plugin (Copilot format). |
| Marketplace manifest | [.github/plugin/marketplace.json](.github/plugin/marketplace.json) | Makes this repo installable as a marketplace. |


Skill assets:
- [references/official-docs.md](skills/copilot-customization-assessment/references/official-docs.md) — doc URLs to ground facts.
- [references/standards.md](skills/copilot-customization-assessment/references/standards.md) — quality standards & guardrails.
- [references/findings-catalog.md](skills/copilot-customization-assessment/references/findings-catalog.md) — recurring issues checklist.
- [references/severity-rubric.md](skills/copilot-customization-assessment/references/severity-rubric.md) — severity / effort / impact scoring.
- [references/validator-usage.md](skills/copilot-customization-assessment/references/validator-usage.md) — how to run the validator.
- [scripts/validate_customizations.py](skills/copilot-customization-assessment/scripts/validate_customizations.py) — deterministic static checks.
- [assets/review-template.md](skills/copilot-customization-assessment/assets/review-template.md) — the `review.md` structure.

## Install the plugin

Prerequisite: enable agent plugins in VS Code — set `chat.plugins.enabled` to `true`.

### Option A — install from source (fastest)

1. In VS Code, run **Chat: Install Plugin From Source** from the Command Palette.
2. Enter this repository's Git URL. VS Code clones and installs the plugin.

Or with the GitHub Copilot CLI:

```bash
copilot plugin install priyanshujain10/copilot-assessor-toolkit
```

### Option B — add as a marketplace

This repo ships a `marketplace.json`, so it can be registered as a plugin marketplace.

- VS Code: add it to the `chat.plugins.marketplaces` setting, e.g. `"priyanshujain10/copilot-assessor-toolkit"`, then
  search `@agentPlugins` in the Extensions view and install **copilot-customization-assessor**.
- CLI: `copilot plugin marketplace add priyanshujain10/copilot-assessor-toolkit` then
  `copilot plugin install copilot-customization-assessor@assessor-toolkit-marketplace`.

### Option C — public discovery

To make the plugin publicly discoverable in the built-in marketplaces, submit it to the
community [github/awesome-copilot](https://github.com/github/awesome-copilot) or
[github/copilot-plugins](https://github.com/github/copilot-plugins) repositories, which VS
Code and the CLI index by default.

> Agent plugins are **not** published to the VS Code *Extension* Marketplace (that is for
> `.vsix` extensions). They are distributed via plugin marketplaces (Git repos) or
> install-from-source, and work in VS Code, the GitHub Copilot CLI, and the Copilot app.

## Use it

After installing, either:
- Select the **Copilot Customization Assessor** agent from the agent picker, or
- Run the skill from chat: type `/` and choose **copilot-customization-assessment**.

Answer the 4–5 dynamic questions (IDE, scope, known issues, org constraints, focus). The
agent grounds facts against official docs, runs the validator, inventories the files, and
writes `review.md`.

Run the validator directly anytime:

```bash
python skills/copilot-customization-assessment/scripts/validate_customizations.py .github
```

## Consume without plugins (JetBrains / vendored)

Agent plugins aren't available in every IDE (e.g. JetBrains). To vendor the customizations
into a repo's `.github` folder instead, run:

```bash
python scripts/install-into-repo.py /path/to/target-repo
```

This copies the `agents/` and `skills/` components into `<target>/.github/`. The plugin
remains the single source of truth.

## Design principles

This toolkit practices what it assesses: a **lean agent**, a **skill** for the multi-step
methodology with standards folded in as a reference, **relative paths** throughout, and a
**deterministic Python validator** for mechanical checks instead of spending premium AI
credits on them.
