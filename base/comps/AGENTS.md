# Component Management — Agent Guide

## Rules

- Keep declaration-only imports in `components.toml`, including components with per-file overlays under `<name>/overlays/`; the shared `{component}` pattern attaches those overlays to declared components. Retain `<name>/<name>.comp.toml` for component-specific settings, including explicit `overlay-files` lists, inline overlays, and build configuration.
- `components.toml` uses `includes` to pull in all `**/*.comp.toml` — no manual wiring needed.
- Canonical example: [`rpm/rpm.comp.toml`](rpm/rpm.comp.toml) — uses modern `[[...overlays]]` syntax with `description` fields. For a larger overlay example (legacy inline syntax, not to be copied for new work), see [`azurelinux-rpm-config/azurelinux-rpm-config.comp.toml`](azurelinux-rpm-config/azurelinux-rpm-config.comp.toml).
- Schema: [`azldev.schema.json`](../../external/schemas/azldev.schema.json)
- Before a version or source-pin update, review upstream release notes, new dependencies, feature removals, ABI/soname changes, and whether existing overlays are still needed. Major version updates require explicit user approval.
- Adding a component to `[component-groups.base-packages].components` routes its **next build** to Base; it does not republish existing RPMs or change its build fingerprint. Every addition must enter the build set in the same change. For an otherwise unchanged component, run `azldev comp update -p <name> --bump`, then finalize locks and rendered specs using the update-component workflow. Plain `update` without `--bump` is insufficient. For `release.calculation = "manual"`, also advance the release in the component's source/config and verify the final rendered release. Verify `azldev comp changed --from <base-ref> --to HEAD -p <name> -q -O json` reports `added` or `changed`, not merely `sourcesChange`. See [Package publishing channels](../../DEVELOPING.md#package-publishing-channels).
- When removing a component, also remove it from `[component-groups.base-packages].components` and remove matching `# srpm: <name>` package exceptions in `components-publish-channels.toml`; then check image definitions, `comps.xml`, and dependants.

## FMF tests

- Put `.fmf/version` at the component root and keep test sources under `<component>/tests/`. Set `render.skip-file-filter = true` in the component config so rendering retains the FMF tree, including `.fmf/version`, plans, scripts, and helpers.
- Re-render after source edits. Lint and execute from `specs/<first-char>/<component>/`, the rendered FMF root: rendered output is the ground truth, and source-only tests do not count as validation.
- Run full `tmt tests lint` and `tmt plans lint` against each rendered tree. Do not hide warnings with `--failed-only`.
- Use `azldev comp test <component>` with `--source-dir` pointing at the rendered FMF root and repeated `--rpm` flags for candidate packages. The repository suite uses `/tests/plans` to discover all tests.
- Run `--provision local` only inside a disposable Azure Linux 4 container, as a non-root user with container-only passwordless sudo. Tests modify packages, users, services, and system configuration.
- Mount the checkout and candidate RPMs read-only. Expose only a task-specific writable artifacts directory under `base/build/work/scratch/`. Never use privileged containers, host PID/network namespaces, or host system-directory mounts.
- Report service, boot, and kernel-policy failures explicitly; containers cannot fully validate those checks. Do not weaken tests or expose host resources to make them pass.

Redirect azldev's project outputs into the container's writable artifacts mount.
For example, save `/artifacts/container.toml` inside the container:

```toml
[project]
log-dir = "/artifacts/logs"
work-dir = "/artifacts/work"
output-dir = "/artifacts/out"
```

Then run from the rendered tree:

```bash
azldev -C /workspace --config-file /artifacts/container.toml \
  comp test azurelinux-repos --provision local \
  --source-dir /workspace/specs/a/azurelinux-repos \
  --rpm /candidates/azurelinux-repos.rpm \
  --rpm /candidates/azurelinux-gpg-keys.rpm \
  --work-dir /artifacts/azurelinux-repos
```

## Skills

- Adding a new component → [`azldev-add-component`](../../.agents/skills/azldev-add-component/SKILL.md)
- Updating or finalizing a component → [`azldev-update-component`](../../.agents/skills/azldev-update-component/SKILL.md)
- Removing component(s) → [`azldev-remove-component`](../../.agents/skills/azldev-remove-component/SKILL.md)
- Fixing overlay issues → [`azldev-overlays`](../../.agents/skills/azldev-overlays/SKILL.md)
- Building and debugging → [`azldev-build-component`](../../.agents/skills/azldev-build-component/SKILL.md)
- Testing in mock chroot → [`azldev-mock`](../../.agents/skills/azldev-mock/SKILL.md)
