# azldev CLI — Feature Requests from Agent Testing

Feedback collected while testing AI agent workflows (adding `cowsay` component, building, testing in mock). These are friction points that affect both human and agent productivity.

## 1. `prep-sources --force` — auto-clean output directory

**Pain point:** Every `prep-sources` iteration requires a manual `rm -rf` of the output dir first because `git clone` fails on non-empty directories. This was the #1 friction point in the inner loop.

**Proposed:** `azldev comp prep-sources -p <name> --force` (or `--clean`) that auto-removes the output dir before writing.

## 2. `azldev comp show-spec -p <name>` — read-only spec view

**Pain point:** To inspect an upstream spec before adding overlays, you currently need to:

1. Add a bare `[components.<name>]` entry to `components.toml`
2. Run `azldev comp prep-sources -p <name> --skip-overlays -o /tmp/inspect`
3. Read the spec
4. Remove the temp entry

A dedicated read-only command would eliminate steps 1 and 4.

**Proposed:** `azldev comp show-spec -p <name>` — fetches and displays the upstream spec without requiring the component to be registered. Could also support `--upstream-distro` and `--upstream-version` flags.

## 3. `azldev adv mock shell --run "command"` — non-interactive execution

**Pain point:** Agents need to run commands inside mock chroots but can't easily drive interactive shells. The current workaround is heredoc piping:

```bash
azldev adv mock shell -p <name> <<'CMDS'
some-command --version
exit
CMDS
```

This works but is fragile.

**Proposed:** `azldev adv mock shell -p <name> --run "command"` for single-command execution, or `--script /path/to/script.sh` for multi-command.

## 4. Show `advanced` in top-level help

**Pain point:** `azldev advanced` (alias `adv`) contains essential tools (`mock shell`, `mock build-rpms`, `mcp`, `wget`) but doesn't appear in `azldev --help`. Users and agents only discover it if they already know to look.

**Proposed:** Add a hint at the bottom of `azldev --help`, e.g.:

```
Use "azldev advanced --help" for additional tools (mock, mcp, wget).
```

## 5. `azldev comp test -p <name> --run "command"` — combined build + test

**Pain point:** Testing a built package requires chaining multiple commands:

1. `azldev comp build -p <name>`
2. Find the built RPM in `base/out/`
3. `azldev adv mock shell --add-package /path/to/rpm`
4. Run test commands

**Proposed:** A single command that builds, installs in a chroot, and runs a test command:

```bash
azldev comp test -p <name> --run "<name> --version"
```

Would be especially valuable for CI pipelines and agent workflows.
