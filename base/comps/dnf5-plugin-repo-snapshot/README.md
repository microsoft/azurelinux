# Filter repository RPMs by publication time

Install `dnf5-plugin-repo-snapshot` with its DNF5 post-setup hook, libdnf5
package-filetime accessor, and libsolv rpmmd-filetime dependencies. The CLI
module and compatible libdnf5 backend must both load for a constrained request;
the CLI checks the **actual loaded** backend after `Base::setup()` and fails
before the selected command configures repositories if it is absent, disabled,
redirected, or incompatible. The required backend identity is `repo_snapshot`,
plugin version `2.0.x` and libdnf5 plugin API `2.2` or later within major `2`.
The hook is a generic, optional DNF5 application-plugin entry point; older
application plugins continue to load without implementing it.

```sh
dnf5 --snapshot-time=1761696000 repoquery --available example
dnf5 --snapshot-time=1761696000 install example
dnf5 --snapshot-time=1761696000 upgrade
dnf5 --snapshot-time=1761696000 --snapshot-exclude-repos=breakglass install example
```

The cutoff is an inclusive, nonnegative decimal POSIX second. RPMs whose
primary metadata `<time file>` is later than the cutoff are excluded from
dependency resolution. An exact match remains eligible. Missing or invalid
time on an in-scope package fails the operation; RPM build time is not a
fallback. The `breakglass` repository **entirely bypasses** the cutoff,
not just selected packages; an unknown or disabled exemption is an error.
Existing package exclusions remain in effect, and installed packages are not
removed or automatically downgraded. No cutoff leaves ordinary DNF5 behavior
unchanged.

Snapshot exclusions apply to the in-memory package sack for that CLI invocation.
They do not rewrite cached repository metadata into a filtered view or persist
the cutoff: a later command without `--snapshot-time` sees ordinary candidates.
Normal DNF5 operations may still refresh/cache metadata, and transactions may
change the installed package state.

Constrained operations support standard repository `install`, `upgrade`, and
`repoquery`. Local/URL RPM inputs, history/replay/offline operations,
download-only transactions (including upgrade `--destdir`, even when configured
through `destdir` in the main config), and exclusion-bypassing options are not
supported with a cutoff and fail explicitly. Install/upgrade also reject
`--skip-broken` and `--skip-unavailable`: either could turn a filtered request
into a success-shaped no-op. Do not mix constrained operations with
unfiltered package sources. Installed-only repoquery modes such as `--installed`,
`--userinstalled`, `--leaves`, and `--duplicates` need no available-repository
metadata; `--available`, `--extras`, and `--upgrades` still require it.
DNF5 5.2.18.0 does not recognize `downloadonly` as a main configuration key;
use the supported `--downloadonly` flag instead (without a cutoff).
For available candidates, a disabled or unavailable required repository
primary metadata source is an error rather than an empty success-shaped
query (including a failed repository skipped by normal DNF5 policy).
All selected enabled available repositories must load: with a cutoff on an
available operation, `skip_if_unavailable=true` cannot turn a failed refresh
into success even when older primary metadata remains cached. Without a cutoff
or for installed-only queries, ordinary repository skip behavior is unchanged.
Refresh metadata with `--refresh` when a current publisher view is needed.
A cutoff does not attest that a publisher has retained old RPMs.

The C++ `libdnf5::rpm::Package::get_file_time()` returns an optional timestamp;
the unchanged SWIG bindings intentionally omit that method. The solv cache
format remains unchanged, so previously cached metadata lacking publication
times may require clearing and re-extracting. Snapshot variables imported
from `DNF_VAR_*` or vars directories are not accepted as implicit settings;
use the explicit options. This is a safeguard against accidentally unenforced
CLI requests, **not** a tamper-proof security boundary or a persistent or
historical repository snapshot service.

## Maintaining the plugin

The CLI validates the cutoff and query scope at parse time and hands the request
to the backend through private `azl_snapshot_*` Vars keys. These keys are not
persistent user settings or repository IDs. After `Base::setup()`, the CLI
attests the *loaded* `repo_snapshot` backend and effective configuration;
the backend then checks available metadata and adds cutoff exclusions without
removing existing exclusions. Installed-only queries need no available metadata.

Use the pinned DNF5 5.2.18.0 upstream `.clang-format` (C++20 Google-derived
style) from a local source checkout; the component does not ship a formatter
configuration. Set `style` to the file in your local checkout, then run these
commands from the repository root with clang-format 21.1.8:

```sh
style=/path/to/dnf5-5.2.18.0/.clang-format
clang-format --style="file:$style" -i base/comps/dnf5-plugin-repo-snapshot/*.{cpp,hpp}
clang-format --style="file:$style" --dry-run --Werror base/comps/dnf5-plugin-repo-snapshot/*.{cpp,hpp}
```
