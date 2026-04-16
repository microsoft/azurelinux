# azurelinux

This branch contains:

* [Distro-wide configuration](distro/)
* [Base project: components, images, etc.](base/)
* [Rendered specs](specs/)

## Getting Started

### Install azldev

The [`azldev`](https://github.com/microsoft/azure-linux-dev-tools) CLI tool drives all component, image, and build workflows. Install it from source (requires Go):

```bash
go install github.com/microsoft/azure-linux-dev-tools/cmd/azldev@main
```

> **Note:** azldev is still in active development, using the latest commit from the `main` branch is recommended for the most up-to-date features and fixes.

### Render specs

The `specs/` directory (as specified by `rendered-specs-dir` config) contains "rendered" spec files created by `azldev`. They are a read-only snapshot of the final spec files after all overlays and modifications have been applied. They are the canonical source for what will be built and packaged.

They can be updated at any time by running `azldev component render -a`, or a single component can be rendered with `azldev component render <name>`.

## AI-Assisted Development (VSCode + GitHub Copilot CLI)

This repo includes [GitHub Copilot](https://docs.github.com/en/copilot) prompt files in `.github/` that automate common workflows. Open VS Code with Copilot Chat in **Agent mode**, attach a prompt (📎), and fill in the inputs.

> **Important:** VSCode works properly when opened as a workspace (i.e. open `code ~/repos/azurelinux`, NOT `code ~/repos`). Otherwise, Copilot may not find the prompt files and won't load the skills.

If the workspace is opened correctly, the agent will automatically gain access to the relevant instructions.

> You may need to ensure [⚙️chat.useAgentSkills](vscode://settings/chat.useAgentSkills) is enabled in your VSCode settings for skills to work properly.

### Prerequisites

The `azl-diagnose` agent and Koji-related tools require:

1. **MCP Python packages** — the MCP servers won't start without them:
   ```bash
   pip3 install --user -r .vscode/mcps/requirements.txt
   ```
2. **Network access to the internal Koji instance** — The internal Koji is only accessible via VPN or the corporate network. If the agent reports connection errors, verify you are connected before retrying.
3. **(Optional) `.env` configuration** — Create a `.env` file (in the workspace root or `.vscode/mcps/`) to pre-configure MCP server settings like the Koji base URL and pre-approved insecure URLs. This avoids the agent having to set the URL or approve self-signed certificates every session. See [.vscode/mcps/.env.example](.vscode/mcps/.env.example) for available variables.

Ask Copilot about any aspect of the project — it can reference the instructions and skills to provide detailed, actionable answers or perform tasks. For example:

```markdown
> Add the cowsay package, but make it clippysay and make clippy the default
```

In VSCode, there are specialized prompts for common tasks. They can be accessed from the chat window by typing `/azl-...` to filter for Azure Linux prompts:

| Prompt | What it does |
|--------|--------------|
| **`azl-diagnose`** | **Diagnose a build failure using a Koji task ID, URL, or package name. Great starting point for any build issue.** |
| `azl-add-component` | Import a package from Fedora — overlays, build & test. |
| `azl-update-component` | Version bump, dependency change, or overlay edit. |
| `azl-debug-component` | Triage build failures, overlay errors, or packaging issues. |
| `azl-review-component` | Audit a component for hygiene and best practices. |
| `azl-migrate-component` | Move an inline entry to a dedicated `.comp.toml` file. |
| `azl-mass-triage` | Batch-triage build failures from a JSON results file — diagnose, bucketize, and summarize. |

### Agents

In addition to prompts, the repo includes **chat agents** that can be selected from the chat participant dropdown (the model/agent next to the Copilot Chat panel). Select the agent, then type your query:

| Agent | What it does |
|-------|--------------|
| `azl-diagnose` | Diagnose build failures — fetch task info/logs, identify root cause, and suggest fixes. Give it a task ID, URL, or package name. |
| `spec-review` | Review spec files against packaging best practices and produce a structured findings report. |

Example: select **azl-diagnose** from the dropdown, then type:

```markdown
> what is the status of the lolcat package
```

```markdown
> https://koji.example.com/koji/taskinfo?taskID=1234
```

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

### Dockerized Batch Triage

For batch triage of build failures, a containerized wrapper runs the `azl-diagnose` agent inside an Azure Linux 3.0 container. The repo is mounted read-only, the agent analyzes a results JSON file, and writes triage reports to `out/triage/`.

```bash
# Default: reads ./results.json
scripts/batch-triage/triage.sh

# Custom results file
scripts/batch-triage/triage.sh --results /path/to/results.json

# With extra instructions
scripts/batch-triage/triage.sh --results /path/to/results.json 'only triage one package'
```

Requirements:

* Docker (buildx recommended)
* GitHub auth ([copilot env var](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli), `copilot` logged in, or `gh` logged in)
* a `.env` file (see above).

Output lands in `out/triage/`.

See [scripts/batch-triage/](scripts/batch-triage/) for the Dockerfile and wrapper script.

### CLI Agents

Copilot CLI also supports agents, use `/agent` to select one, or start the CLI with a specific agent:

```bash
copilot --add-dir . --agent azl-diagnose
```
