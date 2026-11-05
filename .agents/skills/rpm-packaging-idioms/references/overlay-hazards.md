# Change hazards (overlays, build options, version bumps, patches)

Read for **every** change to an existing component. These break other packages, upgrades or security while the
package itself still looks fine. Each level links the Fedora section to cite.

## Before judging any change

- Diff the rendered spec before/after **and** the component TOML. `build.with/without/defines` don't show in the
  spec text: trace each `%bcond`/macro they flip through BuildRequires, configure flags, `%files`, scriptlets.
- "Builds locally" is not evidence the change is complete; check `%files`/subpackages still match what the new
  configuration installs.
- Find consumers before removing or changing anything a package provides:
  `grep -lE '(Build)?Requires:.*\b<name>\b' specs/*/*/*.spec` (also `pkgconfig(...)`, `Recommends:`).

## Hazards

| Change | What breaks | Expect | Level (§) |
| --- | --- | --- | --- |
| Feature/binding disabled (`--without-x`, `build.without`, bcond) | `%files`/`%package` for it still listed → build fails; consumers lose it; config using it fails after upgrade | Remove the subpackage/files/BRs together; check consumers; say what users lose | correctness |
| Shipped (sub)package removed or renamed | Old package stays installed and never updates; deps on it break | `Obsoletes: old < <EVR above last build>` (+ `Provides:` if compatible) on a remaining package | SHOULD ([Renaming/Replacing](https://docs.fedoraproject.org/en-US/packaging-guidelines/#renaming-or-replacing-existing-packages)) |
| Exported symbol removed, struct/ABI changed, or a library version bump | Consumers built against it fail at runtime (undefined symbol) or need rebuild; same SONAME hides it | Don't break ABI downstream; if unavoidable bump SONAME and rebuild every consumer in the same change | correctness ([Shared Libraries](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_shared_libraries)) |
| Version bump of a library others link/build against | ABI change; for ABI-hashed ecosystems (Haskell, OCaml) **every** reverse dep must rebuild | Plan the rebuild chain; see ecosystem card | correctness |
| `Release:`/`Version:`/`Epoch:` edits | EVR goes **down** (incl. subpackages with their own Version that inherit Release) → upgrades skip it | EVR of every binary package only increases | correctness |
| `%config(noreplace)` → `%config` | Admin edits overwritten on upgrade (moved to `.rpmsave`) | Keep `noreplace`; plain `%config` only if old configs can't work, with a comment | SHOULD ([Configuration Files](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_configuration_files)) |
| `systemctl enable/start` in scriptlets, or enabling by default | Re-enables services admins disabled; starts services in image/chroot builds | Use presets (`azurelinux-release` `90-default.preset`) + `%systemd_post`; a service may not enable itself | MUST NOT self-enable ([Scriptlets § Systemd](https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_systemd), [DefaultServices](https://docs.fedoraproject.org/en-US/packaging-guidelines/DefaultServices/)) |
| New scriptlet line that can fail | Non-zero exit breaks install/upgrade | Ensure exit 0 (`\|\| :`) | MUST ([Scriptlets](https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/)) |
| `CFLAGS=...`/`LDFLAGS=...` replaced instead of extended | Distro hardening (FORTIFY, stack protector, CET, PIE) silently dropped | Append to `%{optflags}`/`%{build_cflags}`, document why | MUST honor flags ([Compiler Flags](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_flags)) |
| `rhel`/`fedora` or other global macro defined | Flips **every** conditional on it (BRs, vendoring, features) | Use a targeted bcond/overlay; see AZL trap 1 | correctness |
| Version bump | Sources/hashes, generated archives (vendor tarballs), patches, `License:` all stale | Regenerate every derived input; re-evaluate License; drop upstreamed patches | correctness / MUST ([Licensing](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_licensing)) |
| `%check`/tests/license checks disabled to make it build | Real breakage or licensing defects ship | Fix or skip specific tests with a comment + upstream link | SHOULD run, comment skips ([Test Suites](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_test_suites)); Python: MUST NOT disable whole suite |
| Security feature removed (crypto backend, NTS, seccomp, hardening) for "fewer deps" | Weaker product for everyone, incl. non-Azure users | Needs explicit product rationale; flag for maintainer | warning |
