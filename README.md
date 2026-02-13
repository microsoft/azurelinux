# azurelinux

This branch contains:

* [Distro-wide configuration](distro/)
* [Base project: components, images, etc.](base/)

## AI-Assisted Development (VSCode + GitHub Copilot CLI)

This repo includes [GitHub Copilot](https://docs.github.com/en/copilot) prompt files in `.github/` that automate common workflows. Open VS Code with Copilot Chat in **Agent mode**, attach a prompt (📎), and fill in the inputs.

> **Important:** VSCode works properly when opened as a workspace (i.e. open `code ~/repos/azurelinux`, NOT `code ~/repos`). Otherwise, Copilot may not find the prompt files and won't load the skills.

If the workspace is opened correctly, the agent will automatically gain access to the relevant instructions.

> You may need to ensure [⚙️chat.useAgentSkills](vscode://settings?id:chat.useAgentSkills) is enabled in your VSCode settings for skills to work properly.

Ask Copilot about any aspect of the project — it can reference the instructions and skills to provide detailed, actionable answers or perform tasks. For example:

```markdown
> Add the cowsay package, but make it clippysay and make clippy the default
```

In VSCode, there are specialized prompts for common tasks. They can be accessed from the chat window by typing `/azl-...` to filter for Azure Linux prompts:

| Prompt | What it does |
|--------|--------------|
| `azl-add-component` | Import a package from Fedora — overlays, build & test. |
| `azl-update-component` | Version bump, dependency change, or overlay edit. |
| `azl-debug-component` | Triage build failures, overlay errors, or packaging issues. |
| `azl-review-component` | Audit a component for hygiene and best practices. |
| `azl-migrate-component` | Move an inline entry to a dedicated `.comp.toml` file. |

### Copilot CLI

The skills and instructions are also compatible with the [GitHub Copilot CLI](https://github.com/features/copilot/cli/) which can be used directly from the terminal without opening VSCode.

```bash
# Fully interactive mode
copilot --add-dir .
```

```bash
# Run a specific prompt, then drop to interactive mode
copilot --add-dir . -i "Upgrade vim to the next stable release"
```

Note: `copilot` supports fully autonomous operation (no interactive mode) with `-p <prompt>` however, until azldev supports a full MCP mode the tool approvals are very difficult. `--yolo` (same as `--allow-all-tools --allow-all-paths --allow-all-urls`) is an option, but use with extreme caution since it grants the agent unrestricted access to your filesystem and network. For now, it's recommended to use `-i` to at least have visibility into the agent's thought process and tool usage.
