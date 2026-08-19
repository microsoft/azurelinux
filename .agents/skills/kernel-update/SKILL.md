---
name: kernel-update
description: "Update or rebuild the Azure Linux kernel and kernel-headers components together. Use for kernel version bumps, rolling-lts/azl4 source updates, kernel config refreshes, azl_pkgrelease bumps, kernel changelog updates, and kernel build/test validation."
argument-hint: "Target kernel version, such as 6.18.32.1"
---

# Update the Azure Linux kernel

Use this workflow for `base/comps/kernel`. The kernel is a local-spec
component, not an upstream spec customized with overlays. Every source version
update must also update `base/comps/kernel-headers`, which builds from the same
archive using an upstream spec plus Azure Linux overlays.

## Load supporting guidance

Before acting, read the repository's `AGENTS.md` plus the `azldev`,
`azldev-build-component`, `azldev-mock`, and
`azldev-update-component` skills. Read `azldev-comp-toml` before changing
`kernel.comp.toml`.

## Establish the update

1. Check the worktree and current component:

   ```sh
   git status --short --branch
   azldev comp list -p kernel -q -O json
   azldev comp list -p kernel-headers -q -O json
   ```

2. Read `base/comps/kernel/README.rst`, both component TOML files, the
   kernel-headers version overlay, and the version macros and latest
   `%changelog` entries in `kernel.spec`.
3. Confirm the requested four-part version exists on the
   `rolling-lts/azl4` source branch. Treat a major or minor series change as a
   major version update and obtain explicit user approval.
4. Review upstream changes for removed options, new dependencies, ABI changes,
   and security or regression notes before editing.

Use `base/build/work/scratch/` for downloaded or extracted temporary files;
never use `/tmp`.

## Change a source version

For a target such as `6.18.32.1`:

1. Download the exact archive from
   `microsoft/CBL-Mariner-Linux-Kernel` and calculate its SHA-512 checksum.
2. In `kernel.comp.toml`, update all three source-pin fields together:
   `filename`, `hash`, and `origin.uri`.
3. In `base/comps/kernel/sources`, replace the previous archive's SHA-512 line
   with the new one. This file is the local-spec "upstream" manifest that
   `replace-upstream = true` in `kernel.comp.toml` matches against. Remove the
   old entry rather than adding a second line — leaving it in place lets
   rendering keep both archives, and `azldev comp render` fails with
   `'replace-upstream = true' but no entry with that filename exists` if the
   new filename is missing.
4. In `kernel.spec`:
   * set `specrpmversion` to `6.18.32`;
   * set `kextraversion` to `1`;
   * reset `azl_pkgrelease` to `1`; and
   * add the matching release entry at the top of `%changelog`.
5. Update the version comment at the top of each complete AZL config. Resolve
   every Kconfig option added, removed, or changed by the new source explicitly
   in both affected architecture configs.
6. Update `base/comps/kernel-headers/kernel-headers.comp.toml`:
   * use the same source filename, SHA-512 checksum, and URL as `kernel`;
   * set `kextraversion` to the same fourth version component;
   * reset its `azl_pkgrelease` to `1`; and
   * update comments and descriptions that name the old version.
7. In `base/comps/kernel-headers/overlays/0001-set-specversion-3-part.overlay.toml`,
   set both the `specversion` and `tarfile_release` replacements to the same
   three-part `specrpmversion` used by `kernel.spec`.

The kernel and kernel-headers source version, archive URL, and checksum must
match exactly. Never land a kernel source update without its kernel-headers
update.

Do not automatically change `kabiversion` or `nvidia_open_version`. They
are independent pins. If either must change, update its archive declaration,
checksum, spec references, and packaging include consistently.

## Make a same-version change

For a packaging, patch, or config-only rebuild:

1. Increment `azl_pkgrelease` by one.
2. Add a matching top `%changelog` entry explaining the change.
3. Do not alter the kernel source pin unless the source changed.
4. Do not touch `kernel-headers` unless the change actually affects its
   output. A kernel-only config, patch, or `azl_pkgrelease` bump must not
   rebump or rebuild `kernel-headers`; coordinated updates are only required
   when the shared kernel source archive changes.

## Validate the inputs

Refresh and render before the expensive build:

```sh
azldev comp update -p kernel
azldev comp update -p kernel-headers
azldev comp render -p kernel
azldev comp render -p kernel-headers
git diff --check
git diff -- specs/k/kernel/ specs/k/kernel-headers/
```

Verify that the rendered source manifest, spec version, release, configs, and
changelog match the intended update in both components. Never edit
`specs/k/kernel` or `specs/k/kernel-headers` directly.

The build runs `process_configs.sh -w -n -c` against the complete Azure Linux
configs. Treat missing, mismatched, or invalid options as update work; do not
disable strict config checking or blindly accept defaults. If protected config
values intentionally change, update and run the policy checks documented in
`scripts/ci/kernel/kernel-config-checker/README.md`.

## Build and test

After render review succeeds:

```sh
azldev comp build -p kernel --preserve-buildenv on-failure
azldev comp build -p kernel-headers --preserve-buildenv on-failure
```

Do not report success after the build alone.

1. Locate the newly produced kernel and kernel-headers RPMs under `base/out/`.
2. In an Azure Linux mock chroot, inspect package metadata, dependencies, and
   file lists, then install the applicable kernel and kernel-headers RPM sets.
   Never install target RPMs on the host.
3. A mock chroot uses the host kernel. Do not claim that `uname`, `lsmod`,
   or `modprobe` validates the built kernel there.
4. Boot an image or VM with the new packages for runtime validation. Test every
   affected architecture when infrastructure is available, including the boot
   path and drivers/configurations changed by the update.
5. State explicitly which architecture and runtime tests ran. If a required
   test is unavailable, record the blocker and what was verified instead.

## Finalize

Before opening a PR:

1. Rerun `comp update` and `comp render` for `kernel` and `kernel-headers`.
2. Review `git diff --check` and both complete component diffs.
3. Commit both component inputs, `locks/kernel.lock`,
   `locks/kernel-headers.lock`, and both rendered directories together.
4. Render both components once after committing. If generated output changes,
   stage it and amend the commit.
5. Summarize the source version, release, config decisions, build result, mock
   inspection/install result, and boot coverage in the PR.

## Guardrails

* Preserve minimal divergence from the Azure Linux kernel source.
* Do not edit lock files or rendered specs by hand.
* Do not use `azldev comp update -a` for a single kernel update.
* Do not update the kernel source without updating kernel-headers to match.
* Do not rebump or rebuild kernel-headers for a kernel-only same-version
  change that does not affect its output.
* Do not skip build and package testing for output-affecting changes.
* Do not describe mock-chroot checks as kernel runtime tests.
