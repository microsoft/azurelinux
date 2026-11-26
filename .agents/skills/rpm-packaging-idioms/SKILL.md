---
name: rpm-packaging-idioms
description: "Fedora-style RPM packaging idioms and anti-patterns for Azure Linux, per ecosystem (Python, Rust, ...), plus verified Azure Linux traps. Use when writing, modifying or reviewing a spec file or a component overlay/build option that affects how a package is built, especially new local specs."
---

# RPM packaging idioms

Azure Linux packages follow Fedora packaging practice unless a component documents otherwise. These cards hold
the Fedora rules (with MUST/SHOULD level and the guideline URL to cite) so you don't need web access.

1. Read [core](references/core.md) and [AZL traps](references/azl-traps.md). For any change to an existing
   component (overlay, build option, patch, version bump), also read [change hazards](references/overlay-hazards.md).
2. Grep the spec (and any overlay replacement text / patches) for the signals below; read every matching card.
3. Compare with 2-3 real specs that use the same macros: `grep -l '<macro>' specs/*/*/*.spec | head`. These are
   contextual AZL examples, including local specs and Fedora imports with downstream overlays, not canonical
   templates. Understand their exceptions; upstream guidelines remain authoritative.
4. Go through **every row** of every card you opened, and decide whether it applies. Don't stop after the first
   few problems. A version bump is never "just" a version bump: check the derived inputs (hashes, vendor
   archives, generator scripts, `License:`), subpackage EVRs and reverse dependencies.
5. When writing, follow the card's canonical shape. When reviewing, report each anti-pattern with its level and
   cite the card's Fedora URL.

| Signal in spec, overlay or patch | Card |
| --- | --- |
| `%pyproject_*`, `%py3_*`, `python3-devel`, `setup.py`, `pyproject.toml`, `pip`, `%{python3_sitelib}` | [Python](references/python.md) |
| `%cargo_*`, `Cargo.toml`, `rust-packaging`, `cargo-rpm-macros`, `%{crates_source}`, `cargo ` | [Rust](references/rust.md) |
| `%gometa`, `%gobuild`, `%goprep`, `%go_vendor_license_*`, `GO_BUILDTAGS`, `go.mod`, `golang-` | [Go](references/go.md) |
| `%{?haskell_setup}`, `%ghc_*`, `ghc-` name, `cabal-rpm`, `.cabal` | [Haskell](references/haskell.md) |
| `%configure`, `%cmake`, `%meson`, `%make_build`, `CFLAGS`/`LDFLAGS`, `%{_libdir}/lib*.so*`, `-devel` with headers | [C/C++](references/c-cpp.md) |

No card for the mechanism? Use the exemplar grep (step 3) and the matching page under
https://docs.fedoraproject.org/en-US/packaging-guidelines/ (e.g. `Golang/`, `Systemd/`, `Perl/`).
That site often serves a "not a bot" challenge page instead of the content. If so, clone the guideline source to a temporary working directory and read `guidelines/modules/ROOT/pages/<Page>.adoc` (e.g. `Golang.adoc`); cite the docs URL either way:

```bash
git clone --depth 1 https://forge.fedoraproject.org/packaging/guidelines.git base/build/work/scratch/fedora-guidelines
```
