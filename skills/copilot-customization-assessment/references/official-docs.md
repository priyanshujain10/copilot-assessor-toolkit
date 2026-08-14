# Official Documentation — Ground Facts Here

Copilot capabilities and file formats change frequently. **Fetch these at assessment time**
with the `web` tool and cite the specific URL for any capability claim in the report. Do not
rely on memory for what is or isn't supported.

## Primary references (always check)

- **Customization cheat sheet** (feature overview, usage comparison, IDE support matrix):
  https://docs.github.com/en/copilot/reference/customization-cheat-sheet
- **Copilot feature matrix** (features by IDE, supported/preview/unsupported):
  https://docs.github.com/en/copilot/reference/copilot-feature-matrix
- **VS Code Copilot customization overview**:
  https://code.visualstudio.com/docs/copilot/customization/overview

## Per-primitive references

| Primitive | GitHub Docs | VS Code Docs |
|-----------|-------------|--------------|
| Custom instructions | https://docs.github.com/en/copilot/concepts/prompting/response-customization | https://code.visualstudio.com/docs/copilot/customization/custom-instructions |
| Prompt files | https://docs.github.com/en/copilot/concepts/prompting/response-customization | https://code.visualstudio.com/docs/copilot/customization/prompt-files |
| Custom agents | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents | https://code.visualstudio.com/docs/copilot/customization/custom-agents |
| Agent skills | https://docs.github.com/en/copilot/concepts/agents/about-agent-skills | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| Hooks | https://docs.github.com/en/copilot/concepts/agents/hooks | — |
| MCP servers | https://docs.github.com/en/copilot/concepts/context/mcp | https://code.visualstudio.com/docs/copilot/customization/mcp-servers |
| Subagents | https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide#using-subagents | — |

## How to use these

1. Confirm the team's IDE(s), then read the **IDE support matrix** to establish which
   features are `supported` / `preview` / `unsupported` for them.
2. Cross-check any org-disabled features (e.g. CLI, MCP, cloud agents, hooks) — a finding
   that recommends or relies on a disabled/unsupported feature is invalid.
3. When you assert "X is/ isn't supported" or "the correct frontmatter field is Y", cite
   the exact doc URL you verified it against in the report.

## Reference: correct file formats (verify against docs above)

- **Custom agent** `.github/agents/*.agent.md` — frontmatter: `description` (required),
  `name`, `tools`, `model`, `argument-hint`, `agents`, `user-invocable`,
  `disable-model-invocation`, `handoffs`, `hooks`.
- **Instructions** `.github/instructions/*.instructions.md` — frontmatter: `description`,
  `name`, `applyTo` (glob; avoid `"**"` unless truly universal).
- **Prompt** `.github/prompts/*.prompt.md` — frontmatter: `description`, `name`,
  `argument-hint`, `agent`, `model`, `tools`.
- **Skill** `.github/skills/<name>/SKILL.md` — frontmatter: `name` (must match folder,
  lowercase, hyphens), `description` (≤1024 chars), `argument-hint`, `user-invocable`,
  `disable-model-invocation`.
- **Repo-wide instructions** `.github/copilot-instructions.md`; third-party `AGENTS.md`.

Frontmatter must be raw YAML between `---` markers — **never** wrapped in a
` ```markdown ` / ` ``` ` code fence.
