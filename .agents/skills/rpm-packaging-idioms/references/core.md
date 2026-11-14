# Core spec idioms (every spec)

Cite `https://docs.fedoraproject.org/en-US/packaging-guidelines/#_<section>` for § names from the main page
(lowercase, spaces → `_`, e.g. `#_tags_and_sections`, `#_patch_guidelines`, `#_build_time_network_access`,
`#_requiring_base_package`, `#_devel_packages`, `#bundling`, `#renaming-or-replacing-existing-packages`).
Other pages: [License field](https://docs.fedoraproject.org/en-US/legal/license-field/),
[SourceURL](https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/),
[Systemd](https://docs.fedoraproject.org/en-US/packaging-guidelines/Systemd/),
[Scriptlets](https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/),
[UsersAndGroups](https://docs.fedoraproject.org/en-US/packaging-guidelines/UsersAndGroups/),
[UnownedDirectories](https://docs.fedoraproject.org/en-US/packaging-guidelines/UnownedDirectories/).

| Seen in spec | Fix | Level (§) |
| --- | --- | --- |
| `Copyright:`/`Packager:`/`Vendor:`/`PreReq:` tags | Remove | MUST NOT (Tags and Sections) |
| `BuildRoot:`, `Group:`, `%clean`, `rm -rf %{buildroot}` at start of `%install`, `%defattr(-,root,root)` | Remove (obsolete) | SHOULD NOT (Tags and Sections) |
| `License:` not an SPDX expression (`MIT License`, `GPLv2+`, `BSD`) | SPDX (`MIT`, `GPL-2.0-or-later`, `BSD-3-Clause`) | MUST (License field page) |
| License text in `%doc` or missing | `%license LICENSE` in every independently installable binary package | MUST (Licensing; main page `#_licensing`) |
| Static `Release:`/hand `%changelog` in an **AZL-authored local spec** | `%autorelease` / `%autochangelog` | AZL rule → warning (`.github/copilot-instructions.md`, cite N/A) |
| `%setup` + `%patchN` | `%autosetup -p1` | style (suggestion) |
| Patch without a comment | Comment: why + upstream status/link | SHOULD (Patch Guidelines) |
| Upstream source with an available download URL listed without a full https URL | Use the full URL; archive filename should include name+version. Local/generated auxiliary sources (e.g. vendor archives, configuration files) need not have upstream URLs | SHOULD (Tags and Sections, SourceURL) |
| Downloads during build (pip/npm/cargo/go fetch, curl) | Everything from Sources; build is offline | MUST NOT (Build Time Network Access) |
| Broad globs on shared dirs (`%{_bindir}/*`, `%{_libdir}/*`) or unowned package dirs | Explicit file lists; own your dirs with `%dir` | SHOULD / MUST own (Explicit lists, Unowned directories) |
| Subpackage `Requires: %{name}` for arch-specific base | `Requires: %{name}%{?_isa} = %{version}-%{release}` | MUST (Requiring Base Package) |
| Development-only unversioned `.so` linker files or headers/`.pc` in main package | `-devel` subpackage; keep runtime-loaded plugins/extension modules in runtime packages | MUST (Devel Packages) |
| Bundled copies of system libraries | Build against system libraries; else `Provides: bundled(...)` | MUST/SHOULD (Bundling) |
| Test suite exists but no `%check` | Run it (skip individual tests with a comment) | SHOULD (Test Suites); ecosystem cards may make smoke test MUST |
| Services: manual `systemctl` in scriptlets | `%systemd_post` / `%systemd_preun` / `%systemd_postun_with_restart` for each unit | MUST use the macros; MUST NOT self-enable (Scriptlets `#_systemd`) |
| Unit files outside `%{_unitdir}`, marked `%config`, or not 0644; `BuildRequires: systemd` just for the macros | `%{_unitdir}`, plain file, 0644; `BuildRequires: systemd-rpm-macros` | MUST / required for macros (Systemd) |
| Users/groups via raw `useradd` in `%pre` | Ship a `sysusers.d` file (see UsersAndGroups and exemplars: `grep -l '%{_sysusersdir}' specs/*/*/*.spec`) | (UsersAndGroups) |
| Scriptlet can exit non-zero (last command may fail) | End with `\|\| :` / ensure exit 0 | MUST exit 0 (Scriptlets) |
| Hardcoded paths (`/usr/lib64`, `/etc`, `/usr/share`) | `%{_libdir}`, `%{_sysconfdir}`, `%{_datadir}` ... | SHOULD (RPMMacros) |
| Config file as plain `%config` (or under `/usr`) | `%config(noreplace)`; plain `%config` only with a comment why | SHOULD (Configuration Files) |
| Service enabled in a scriptlet (`systemctl enable/start`) | Presets decide; `%systemd_post` only | MUST NOT self-enable (Scriptlets § Systemd) |

Before writing a spec from scratch, check upstream first: `ls specs/*/<name>` (already in AZL?) and whether
Fedora packages it (an `azldev` upstream import beats a local spec; see the `azldev-add-component` skill).

## Inherited upstream problems

A Fedora-imported component's spec is Fedora's; every overlay is divergence we maintain. Don't "fix" inherited
non-idiomatic text just because you're nearby, and don't hold a PR to account for text it didn't change.

- **Idiom/style only** (legacy macros, globs, `%setup`, uncommented patches, obsolete tags): leave it. In a
  review, at most a suggestion labelled "inherited from Fedora". If worth it, fix it in Fedora (dist-git PR or
  bug) and inherit the fix.
- **Real defect that hurts AZL** (build break, wrong runtime behavior, security, broken upgrade path): a minimal
  overlay is justified. Record why with overlay metadata (see the `azldev-overlay-metadata` skill): an existing
  upstream fix → `upstream-backport` + `commits`; otherwise report it to Fedora/upstream and use
  `upstream-status = "upstreamable"` with the report in `bugs`, so the overlay is dropped when the fix lands.
- AZL-authored local specs have no upstream to defer to: all rules apply in full.
