# Developing the Azure Linux distro

## Getting Started

### Install azldev

The [`azldev`](https://github.com/microsoft/azure-linux-dev-tools) CLI tool drives all component, image, and build workflows. Install it from source (requires Go):

```bash
go install "github.com/microsoft/azure-linux-dev-tools/cmd/azldev@$(cat .azldev-version)"
```

`go install` writes executables to the directory reported by `go env GOBIN`.
When that value is empty, it uses `$(go env GOPATH)/bin`. Make sure the install
directory is on `PATH` before starting VS Code or Copilot CLI. For the default
Go configuration:

```bash
export PATH="$(go env GOPATH)/bin:$PATH"
command -v azldev
```

Add the `export` to your shell startup file to persist it. If `go env GOBIN`
prints a custom directory, add that directory instead.

> **Note:** azldev is still in active development, to ensure you have a stable version, install the version pinned by `.azldev-version` in this repo.

### Refresh agent guidance

The `azldev-*` skills and generated instruction wrappers are emitted by azldev. Make
durable guidance changes in azldev, then install the version pinned by
`.azldev-version` using the command above. Always regenerate from that pinned version.
From this repository's root, run:

```bash
azldev docs agent install --full
```

### azldev documentation

See the [azldev user guide](https://github.com/microsoft/azure-linux-dev-tools/tree/main/docs/user) for how-to guides and reference documentation covering components, overlays, images, configuration, and CLI commands.

### Render specs

The `specs/` directory (as specified by `rendered-specs-dir` config) contains "rendered" spec files created by `azldev`. They are a read-only snapshot of the final spec files after all overlays and modifications have been applied. They are the canonical source for what will be built and packaged.

They can be updated at any time by running
`azldev component render -a --spec-editor experimental`, or a single component
can be rendered with `azldev component render <name> --spec-editor experimental`.

### Select the spec editor

Azure Linux uses azldev's experimental structural spec editor. The pinned azldev
still defaults to the legacy editor and has no TOML field or environment variable
for selecting an editor. Pass `--spec-editor experimental` on every invocation
that prepares or edits specs, including local builds:

```bash
azldev comp render -p <name> --spec-editor experimental
azldev comp render -a --clean-stale --spec-editor experimental --fail-on-error
azldev comp build -p <name> --spec-editor experimental
azldev comp prep-sources -p <name> --spec-editor experimental --force -o <dir>
azldev comp diff-sources -p <name> --spec-editor experimental
```

The selection is not persisted by rendering; subsequent commands need the flag
again. Lock updates (`azldev comp update`) and config inspection do not need it.
CI render checks use the same explicit flag. When following generated azldev
skills or older examples, add this flag to the spec-processing commands above.

The structural editor does not yet preserve referenced macros automatically when
removing a subpackage. Keep existing macro-hoisting overlays, such as QEMU's
`testsdir` overlay.

## Component FMF tests

Put `.fmf/version` at `base/comps/<component>/.fmf/version` and keep test sources
under `base/comps/<component>/tests/`. Re-render before linting or running tests.
Use `specs/<first-char>/<component>/` as the FMF root; rendered output is the ground truth.
For example:

```bash
azldev comp render -p azurelinux-repos --spec-editor experimental
```

Run tests with `azldev comp test`, pointing `--source-dir` at the rendered component
root and supplying candidate RPMs with repeated `--rpm` flags.
Use `--provision local` **only inside a disposable Azure Linux 4 container**,
never on the development host. See the [component agent guide](base/comps/AGENTS.md#fmf-tests)
for rendering, linting, and container setup details.

## Package publishing channels

[`base/comps/components-publish-channels.toml`](base/comps/components-publish-channels.toml)
defines where component build outputs are published. Unless overridden, binary,
source, and debuginfo RPMs route to `rpm-sdk`, `rpm-sdk-srpm`, and
`rpm-sdk-debuginfo`. Components listed in
`[component-groups.base-packages].components` instead inherit `rpm-base`,
`rpm-base-srpm`, and `rpm-base-debuginfo`.

This list describes the intended Base package set, including runtime dependency
closure. It does not automatically discover or promote dependencies. Check those
dependencies when promoting a component. Component-specific settings, package
groups, and explicit per-package overrides can change the effective destination;
in particular, `exceptions-packages` keeps selected sibling subpackages in SDK.

### Routing is not publication

**Adding an existing component to the Base list means "publish its next build to
Base," not "copy its existing RPMs into Base."** Publishing settings are excluded
from azldev's build fingerprints. The production post-merge pipeline submits only
components reported as `added` or `changed` by `azldev comp changed`; a routing-only
edit can leave the component `unchanged`. Plain `azldev comp update` may therefore
leave its lock unchanged too.

Every newly listed Base component must enter that build set in the same change.
The separate GitHub Actions **Check Base Promotions** PR check compares committed membership
from the captured target to the prospective merged tree with the matching
change-set JSON and rejects additions that would not build. Already-landed
bumps do not count, even when a stacked parent was squash-merged or rebased.
Lock freshness and rendered-spec correctness
remain separate companion checks. A genuinely new
component or a component already changed by source/config inputs needs no extra
manual bump. Reordering, comments, and membership removals do not require one.

This promotion policy runs only in the GitHub PR check, not in Azure Pipelines
or after merge. If a routing-only promotion bypasses the PR gate, submit a
follow-up bump and verify actual publication.

### Promote an otherwise unchanged component

Add the component to the alphabetically sorted Base list, then explicitly request
a new release without changing its upstream pin:

```bash
azldev comp update -p <name> --bump
azldev comp render -p <name> --spec-editor experimental
```

`--bump` increments the lock's `manual-bump` counter and recomputes its build
fingerprint without fetching a newer upstream revision. Include the channel
configuration, updated lock, and rendered output in the same logical change.
After committing, re-render and stage the resulting specs for an amend, following
the [component finalization workflow](.agents/skills/azldev-update-component/SKILL.md).
For components with manual release calculation, also advance the release in the
component's source/config. Validate the final rendered release and follow the
normal build and smoke-test requirements.

Verify the committed result against your PR baseline:

```bash
azldev comp changed --from <base-ref> --to HEAD -p <name> -q -O json
```

The component must report `added` or `changed`. A spec-tree diff or
`sourcesChange: true` alone does not select an official rebuild. Repeat the
workflow for each otherwise unchanged component being promoted.

### Verify actual publication

The production package-build pipeline submits the selected components and
confirms acceptance; builds run asynchronously. A green submission check is not
proof that the build or publication completed. Before reporting the promotion
done, verify the official build succeeded and the expected RPM versions appeared
in the intended production Base repository for the supported architectures.
Build deployment and consumer repository channel are separate concerns; do not
substitute Preview repository results for production Base verification.

## AI-Assisted Development (VSCode + GitHub Copilot CLI)

This repo includes [GitHub Copilot](https://docs.github.com/en/copilot) prompt files in `.github/` that automate common workflows. Open VS Code with Copilot Chat in **Agent mode**, attach a prompt (📎), and fill in the inputs.

> **Important:** VSCode works properly when opened as a workspace (i.e. open `code ~/repos/azurelinux`, NOT `code ~/repos`). Otherwise, Copilot may not find the prompt files and won't load the skills.

If the workspace is opened correctly, the agent will automatically gain access to the relevant instructions.

> You may need to ensure [⚙️chat.useAgentSkills](vscode://settings/chat.useAgentSkills) is enabled in your VSCode settings for skills to work properly.

### Prerequisites

The `azl-diagnose` agent and Koji-related tools require:

1. **MCP Python packages** — the MCP servers won't start without them:

   ```bash
   pip3 install --user -r scripts/mcps/requirements.txt
   ```

2. **Network access to the internal Koji instance** — The internal Koji is only accessible via VPN or the corporate network. If the agent reports connection errors, verify you are connected before retrying.
3. **(Optional) `.env` configuration** — Create a `.env` file (in the workspace root or `scripts/mcps/`) to pre-configure MCP server settings like the Koji base URL and pre-approved insecure URLs. This avoids the agent having to set the URL or approve self-signed certificates every session. See [scripts/mcps/.env.example](scripts/mcps/.env.example) for available variables.

Ask Copilot about any aspect of the project — it can reference the instructions and skills to provide detailed, actionable answers or perform tasks. For example:

```markdown
> Add the cowsay package, but make it clippysay and make clippy the default
```

In VSCode, there are specialized prompts for common tasks. They can be accessed from the chat window by typing `/azl-...` to filter for Azure Linux prompts:

| Prompt | What it does |
| -------- | -------------- |
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
# Fully interactive mode (from the repo root)
copilot --add-dir .
```

```bash
# Run a specific prompt, then drop to interactive mode
copilot --add-dir . -i "Upgrade vim to the next stable release"
```

The repository configures MCP servers for both VS Code (`.vscode/mcp.json`) and
Copilot CLI (`.mcp.json`), including the `azldev advanced mcp` server. Run Copilot
CLI from the repository root.

The MCP configuration starts `azldev` by name, so it must be on the `PATH`
inherited by Copilot CLI.

The Azure DevOps MCP server also requires the organization name and one enabled
domain. Export them before starting Copilot CLI in any mode:

```bash
export AZURE_DEVOPS_ORG='<organization>'
export AZURE_DEVOPS_DOMAIN='<domain>'
```

Note: `copilot` supports fully autonomous operation (no interactive mode) with
`copilot -p '<prompt>' --additional-mcp-config=@.mcp.json`. The additional MCP
configuration makes the repository's MCP servers available in prompt mode.
`--yolo` (same as `--allow-all-tools --allow-all-paths --allow-all-urls`) is an
option, but use with extreme caution since it grants the agent unrestricted
access to your filesystem and network. For now, it's recommended to use `-i` to
at least have visibility into the agent's thought process and tool usage.

#### Using as a plugin (cross-repo access)

This repo includes a [Copilot plugin manifest](.github/plugin/plugin.json) that makes its skills available from **any** working directory — not just the repo root. This is useful when you're working in another repo but want access to azurelinux skills (component builds, overlay debugging, Koji triage, etc.).

**Install as a plugin (local clone):**

```bash
# One-time install — skills persist across sessions
copilot plugin install --plugin-dir /path/to/azurelinux

# Or load for a single session
copilot --plugin-dir /path/to/azurelinux
```

After installing, all skills are available regardless of your current directory. Use `/skills` to list them.

> **Note:** Remote install via `copilot plugin install microsoft/azurelinux` will work once this branch (`4.0`) becomes the repo's default branch on GitHub. Until then, use the local path.

### Dockerized Batch Triage

For batch triage of build failures, a containerized wrapper runs the `azl-diagnose` agent inside an Azure Linux 3.0 container using `gpt-6-sol` by default. The repo is mounted read-only, the agent analyzes a results JSON file, and writes triage reports to `out/triage/`. Override the model with `--model <model>`.

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
