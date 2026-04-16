---
applyTo: ".github/workflows/**"
description: ALWAYS review these instructions when reading or modifying PR check workflows, or any scripts referenced by the workflows.
---

# PR Check Workflow Guidelines

## Fork-PR-safe pattern: stub + reusable

Problem: `pull_request` triggers on fork PRs run without secrets and with a read-only token. `pull_request_target` runs with write access but checks out the BASE ref by default — easy to footgun into RCE if you then check out PR code with full privileges.

Pattern:

1. **Stub workflow** on the default branch — triggered by `pull_request_target`, guards on repo owner, calls the reusable workflow. This is the only file GitHub will load from the base branch, so it locks the entrypoint.
2. **Reusable workflow** (`workflow_call`) holds the real logic. Lives on the PR branch, so contributors can iterate on it.
3. Stub passes `pull-requests: write` / `contents: read` only. Reusable declares its own minimum permissions.

Never check out PR code into a privileged job and then execute it on the host. Either:
- Run untrusted code inside a container with no secrets mounted, **or**
- Keep the privileged job read-only (lint, comment-post) and isolate code execution to a separate unprivileged job.

## Prefer in-container for anything that executes PR code

If the check builds, renders, or runs PR code, do the whole thing inside the build container. Mock is a critical component of many azldev workflows. It requires many privileges to run successfully. It also is not available in Ubuntu, which is the default runner image for GitHub Actions.

- Mount the PR checkout read-only when possible; if writes are needed (e.g. `git add -N`), mount rw but don't leak host paths or secrets.
- Produce **all outputs** (reports, patches, diffs) inside the container and write them to a bind-mounted output dir. Host-side steps then only read these artifacts (json report, patch files, etc.)
- This eliminates a huge class of config-driven git RCE vectors (`core.fsmonitor`, `core.sshCommand`, hook files, etc.) because the host never runs git against PR-controlled config.

### Container config

The shared runner image is [`.github/workflows/containers/azldev-runner.Dockerfile`](../workflows/containers/azldev-runner.Dockerfile). It's a minimal Azure Linux base with `mock`, `git`, `python3`, `sudo`, and `azldev` itself (installed to `/usr/local/bin` during image build) — enough to run any `azldev` subcommand. Reuse it rather than building a per-check image; add extras via a derived `FROM localhost/azldev-runner` stage if a check genuinely needs more.

`azldev` is baked in via `go install …/azldev@main` during image build. The pin lives in the Dockerfile so it can be reviewed and bumped deliberately. Image build context is `.github/workflows/containers/` only — keep it that way so the build can never see PR-controlled files.

Build it with the caller's UID so bind-mounted writes don't end up root-owned:

```yaml
- name: Build azldev runner
  run: |
    docker build \
      --build-arg UID=$(id -u) \
      -t localhost/azldev-runner \
      -f .github/workflows/containers/azldev-runner.Dockerfile \
      .github/workflows/containers/
```

#### Bind-mount conventions

| Mount | Mode | Purpose |
| ----- | ---- | ------- |
| `pr-head/` → `/workdir` | rw | PR checkout. rw because `azldev` writes to `specs/`, `base/build/`, etc. |
| `<host-output-dir>/` → `/output` | rw | Trusted-shape outputs (JSON reports, patches, ...) the container produces for the host to consume after the run. |
| `.github/workflows/scripts/` → `/scripts` | ro | Helper scripts from the trusted base checkout. |

#### Sandbox flags (minimum viable for `mock`)

```yaml
docker run --rm \
  --cap-add=SYS_ADMIN \
  --security-opt seccomp=unconfined \
  --security-opt apparmor=unconfined \
  ...
```

Why each one is needed:

- **`--cap-add=SYS_ADMIN`** — `mock` sets up mount namespaces for its chroot. Without this you get `mount … exit status 32` during chroot init.
- **`--security-opt seccomp=unconfined`** — `mock` uses syscalls (`unshare`, `pivot_root`, etc.) that Docker's default seccomp profile blocks.
- **`--security-opt apparmor=unconfined`** — `ubuntu-latest` ships the `docker-default` AppArmor profile, which blocks `mount -t tmpfs` on paths under `/var/lib/mock` **even with `SYS_ADMIN` granted**. This is the confusing one; symptom is the same `exit status 32` after seccomp is already unconfined.

Avoid `--privileged` — it grants every capability and removes cgroup restrictions, which is a much bigger blast radius than the three flags above.

`--security-opt no-new-privileges` would be nice but `mock`'s `userhelper` needs setuid, which that flag blocks.

#### Running commands in the container

Use `bash -eu -o pipefail -c '…'` as the entrypoint invocation so a failure inside the heredoc actually fails the step:

```yaml
localhost/azldev-runner \
  bash -eu -o pipefail -c '
    azldev component render -q -a --clean-stale -O json > /output/render.json
    python3 /scripts/check_rendered_specs.py \
      --specs-dir "$(azldev config dump -q -f json | jq -r .project.renderedSpecsDir)" \
      --report /output/report.json \
      --patch /output/rendered-specs.patch
  '
```

Use single-quotes around the `-c` payload so host-side `${{ … }}` interpolation doesn't leak into the container script. If you need to pass a host value in, use `-e VAR=…` and reference `"$VAR"` inside — same script-injection concern as any other shell step.

## Shell hardening in workflow steps

- Start every multi-line `run:` with `set -euo pipefail`.
- Quote **every** expansion involving a workflow input, matrix value, or file path: `"${VAR}"`, not `$VAR`.
- Never interpolate `${{ github.event.pull_request.* }}` directly into a shell script — assign to an `env:` var first, then reference as `"$VAR"`. Direct interpolation is a classic script-injection vector.
- For paths that must stay inside the repo, resolve with `realpath -m` and verify they start with the repo root prefix before use.

## Markdown / HTML injection in PR comments

- Escape any PR-controlled string (file paths, error messages) before dropping into Markdown.
- Prefer code spans (`` `path` ``) or fenced blocks for anything path-like.

## zizmor / pedantic linting

Workflows are linted with `zizmor --pedantic`.

Use `# zizmor: ignore[<rule>]` comments as an absolute last resort, and provide a comprehensive justification for why the rule is being ignored.
