# Test catalogue & contributor guide

This document describes every test in [`../cases/`](../cases/) — what it
asserts, which markers and fixtures it uses, what its failure looks
like — and explains how to add a new one.

For the architecture and design of the framework itself, see
[`architecture.md`](architecture.md). For user-facing invocation,
see [`../README.md`](../README.md).

## Reading this catalogue

Each entry covers:

* **What it asserts** — the rule the test enforces.
* **Markers / fan-out** — which `(repo, arch)` pairs the test fans
  out across.
* **Fixtures used** — what data the test pulls from the framework.
* **Failure shape** — aggregate vs data-parametrized, what the failure
  message looks like.
* **Rules-as-code** — the constants at the top of the test file you
  edit to change behavior.

## Catalogue

### `test_no_srpms_in_binary.py`

* **Asserts:** Every package in a binary repo has a binary arch
  (i.e., not `src` and not `nosrc`).
* **Markers:** `@pytest.mark.repo_kind("binary")`.
* **Fan-out:** one test per binary repo per arch.
* **Fixtures:** `repo`, `arch`, `repo_packages`.
* **Failure:** aggregated — lists every offending NEVRA in one
  failure message per `(repo, arch)`.
* **Rules-as-code:** none — the rule is structural.

### `test_only_srpms_in_srpm_repo.py`

* **Asserts:** Every package in an SRPM repo has arch `src` or `nosrc`.
* **Markers:** `@pytest.mark.repo_kind("srpm")`.
* **Fan-out:** one test per srpm repo per arch.
* **Fixtures:** `repo`, `arch`, `repo_packages`.
* **Failure:** aggregated.
* **Rules-as-code:** `_SRPM_ARCHES = frozenset({"src", "nosrc"})`.

### `test_blocklist.py`

* **Asserts:** No package whose name (the *N* of *NEVR*) appears in
  the hard-coded `GLOBAL_BLOCKLIST` may exist in *any* provided
  repo, regardless of kind (`binary`, `srpm`, `debuginfo`) or arch.
* **Markers:** none — fans out over every provided `--repo` via the
  default `repo` parametrization.
* **Fan-out:** one collected test per `(repo, arch, blocked_name)`
  triple. Data-parametrized over `GLOBAL_BLOCKLIST` so each name
  shows up as its own pytest result.
* **Fixtures:** `repo`, `arch`, `repo_packages`.
* **Failure:** per `(repo, arch, blocked_name)`. The current
  `GLOBAL_BLOCKLIST` covers upstream packages that AZL replaces
  (`fedora-release`, `fedora-repos`, `fedora-logos`,
  `redhat-rpm-config`) and licensing-constrained packages
  (`ffmpeg`).
* **Rules-as-code:** `GLOBAL_BLOCKLIST = (...)` at the top of the
  file. If you ever need a *per-repo* blocklist, add it as a
  separate test alongside this one rather than overloading this
  function with two shapes.

### `test_vendor_tag.py`

* **Asserts:** Every non-source package in a binary repo has
  `Vendor == "Microsoft Corporation"` (the vendor is configurable via
  the `--expected-vendor` CLI option; default value shown).
* **Markers:** `@pytest.mark.repo_kind("binary")`.
* **Fan-out:** one test per binary repo per arch.
* **Fixtures:** `repo`, `arch`, `repo_packages`, `expected_vendor`.
* **Failure:** aggregated — lists each offending package and its
  observed vendor string.

### `test_release_suffix.py`

* **Asserts:** Every non-source package's `Release` tag matches the
  regex `\.azl4(?:\.\d+|~.*)?$` — i.e., ends with `.azl4`, optionally
  followed by either a numeric `.<N>` rebuild bump (`.azl4.4`) or a
  `~<arbitrary-suffix>` qualifier (used for pre-release / hotfix
  builds, e.g. `.azl4~rc1`). The pattern is configurable via the
  `--release-suffix` CLI option (default shown); set it to e.g.
  `\.azl3(?:\.\d+|~.*)?$` for AZL3 nightly verification.
* **Markers:** `@pytest.mark.repo_kind("binary")`.
* **Fan-out:** one test per binary repo per arch.
* **Fixtures:** `repo`, `arch`, `repo_packages`, `release_suffix_pattern`.
* **Failure:** aggregated.

### `test_repoclosure_base.py`

* **Asserts:** The `base` repo is closed over its package universe's
  runtime dependencies (i.e., every `Requires:` resolves within the
  repo plus `noarch`).
* **Markers:** none — repos are hard-coded.
* **Fan-out:** one test per arch.
* **Fixtures:** `arch`, `require_named_repos`, `repoclosure`.
* **Fail behavior:** see `require_named_repos` semantics — any of
  `--repo name=base,...` not provided → fail loudly. Hard-coded
  closure tests are only meaningful with the full named set provided.
* **Failure:** per `(target-set, arch)`. The `RepoclosureResult.__str__`
  lists each unresolved package and its missing requires.

### `test_repoclosure_base_plus_sdk_full.py`

* **Asserts:** `base ∪ sdk ∪ base-srpms ∪ sdk-srpms` is closed over
  *both* runtime dependencies (binary RPMs on the test arch and
  `noarch`) and build-time dependencies (the source-arch view of
  every SRPM in `base-srpms ∪ sdk-srpms`). One walk satisfies both
  because the "buildtime" check kind covers arch ∈ {*arch*, `noarch`,
  `src`, `nosrc`}; the `repoclosure` runner deliberately does not
  filter findings to `target_repos` for `check_kind="buildtime"` so
  the same walk surfaces broken binary providers that would otherwise
  silently invalidate a daily build (see
  `utils.repoclosure.Repoclosure.run`). Findings are partitioned by
  consumer arch into runtime gaps (`arch ∉ {src, nosrc}`) and
  buildtime gaps (`arch ∈ {src, nosrc}`) and asserted independently
  against the matching `[runtime-missing]` / `[buildtime-missing]`
  section of the known-violations TOML.
* **Markers:** none — repos are hard-coded.
* **Fan-out:** one test per arch.
* **Fixtures:** `arch`, `require_named_repos`, `repoclosure` (used
  with `check_kind="buildtime"`), `subtests`, `known_violations`,
  `summary_recorder`.
* **Fail behavior:** all of `{base, sdk, base-srpms, sdk-srpms}`
  provided → run; any missing → fail.
* **Failure:** per `(target-set, arch, dep-kind)`. Each unresolved
  consumer becomes its own subtest (XFAIL when the deps are listed
  in the matching known-violations section, real fail otherwise),
  with stale-consumer / stale-dep rails on the allowlists themselves.
  Both the runtime and buildtime classifications also flow into the
  `--summary-json` output if that flag is set.

### `test_no_duplicate_subpackage_names.py`

* **Asserts:** Across all binary repos provided, no two distinct
  SRPMs (compared by SRPM *name*, parsed from `<rpm:sourcerpm>`) may
  produce a binary sub-package of the same name. Identical NEVRAs
  across repos are deduped before comparison.
* **Markers:** none — uses `binary_repos` directly.
* **Fan-out:** one test per arch.
* **Fixtures:** `arch`, `binary_repos`, `all_binary_packages`,
  `subtests`, `known_violations`, `summary_recorder`.
* **Failure shape:** subtests, one per offending binary name (or
  per stale allowlist entry). Real failures list the offending
  SRPMs with one example NEVRA per SRPM; XFAILs carry the same
  detail with a "tracked in <file> [<section>]" prefix.
* **Rules-as-code:**
  * `ALLOWLIST: dict[str, frozenset[str]]` at the top of the test
    file — *intentional* multi-SRPM coexistence (e.g., compat
    shims). Silently skipped (no XFAIL noise) as long as the
    observed SRPM set is a subset of the listed set.
  * Known-violations TOML at
    [`cases/known-violations/test_no_duplicate_subpackage_names.toml`](../cases/known-violations/test_no_duplicate_subpackage_names.toml)
    under section `[duplicate-subpackages]` — *known violations we
    have not yet cleaned up*. Reported as XFAIL via the shared
    `classify_violations` engine; stale-consumer (binary no longer
    multi-SRPM) and stale-dep (a listed contributing SRPM no longer
    contributes) entries fail the run as a cleanup nudge.

### `test_file_conflicts_cross_repo.py`

> **Lives in `experimental-cases/`, not `cases/`.** This test downloads
> each candidate RPM (rather than just metadata) so it can compare
> per-file metadata, and the heuristic still has known limitations
> (see below). It is not collected by a default `pytest cases/` run;
> invoke it explicitly with `pytest experimental-cases/`.

* **Asserts:** Across all binary repos, distinct binary packages from
  *different SRPMs* that own the same file path are mutually marked
  with `Conflicts:` (either by literal name or via a `Provides:` /
  `Conflicts:` virtual-name pair). This is a heuristic check on top of
  repodata — not a perfect simulation of `rpm -i`'s install-time
  conflict resolution.
* **Heuristic limitations** (see also the module docstring):
  * **Name-only conflict matching.** `Provides:` and `Conflicts:` are
    treated as bare-name sets — version ranges (e.g.
    `Conflicts: foo >= 2.0`) are not modeled. A ranged `Conflicts:`
    that only covers some versions of the other side may produce a
    false positive here (we'll report it as unsatisfied even though
    the install-time resolver would accept the actually-published
    version), and conversely an effective conflict that only fires
    on a version *range* the published packages happen to fall outside
    of may pass here. Treat the test as high signal but not gospel.
  * **Single-arch perspective.** Each test instance compares only
    same-arch packages (the test fans out per-arch). Multilib
    (`glibc.i686` next to `glibc.x86_64` on an `x86_64` host) is out
    of scope.
* **Markers:** none — uses `binary_repos` directly.
* **Fan-out:** one test per arch.
* **Fixtures:** `arch`, `binary_repos`, `all_binary_packages`,
  `cross_repo_file_index`, `package_file_metadata`.
* **Filtering applied (in order):**
  * Directory entries — RPM permits shared directory ownership
    when modes/owner/group match (filtered by the metadata service
    as a cheap first pass; not re-validated, on the assumption that
    dirs are the overwhelming majority of legitimate sharing and
    re-validating each would mean downloading every RPM).
  * `%ghost` entries — RPM's canonical mechanism for non-conflicting
    shared "ownership" of a path (filtered by the metadata service).
  * Identical NEVRAs across repos are deduped (one owner per unique
    NEVRA).
  * Same-SRPM sibling pairs are exempted in this test — `rpmbuild`
    already prevents same-SRPM siblings from genuinely conflicting at
    install time; cross-SRPM pairs are the real signal here.
  * Pairs that mutually `Conflicts:` each other — RPM will refuse
    to coinstall them anyway, so file overlap is moot.
  * **`rpmfilesCompare`-equivalent refinement:** for every
    candidate `(pkg_a, pkg_b, path)` triple still surviving the
    filters above, both packages' RPMs are downloaded on demand
    (via `package_file_metadata(arch, nevra)`) and the per-file
    metadata is compared using the same rules `rpmfi.cc:898
    rpmfilesCompare` applies — modes (except both symlink), owner,
    group, plus type-specific checks (size+digest for regular
    files, linkto+size for symlinks, rdev for device nodes). Pairs
    that match across all those fields are silently dropped, which
    is what RPM does at install time.
* **Failure:** aggregated, **grouped by package pair** with sample
  paths per pair (5 by default). Sorted worst-offenders-first so a
  single high-volume issue (e.g., `mariadb-test` vs `mysql-test-data`
  sharing thousands of test fixtures) doesn't drown out the smaller
  ones.
* **Rules-as-code:** `PATH_ALLOWLIST: dict[str, str]` for legitimate
  shared-ownership cases (e.g., `alternatives`-managed slots that
  somehow escape the ghost-filter). `_SAMPLE_PATHS_PER_PAIR` controls
  how many sample paths show up per group in the failure message.

## How to add a new test

The framework is shaped so most new tests are short — five to twenty
lines.

### 1. Decide the scope

Pick the markers / fixtures that match the assertion:

| Assertion is about... | Use |
| --- | --- |
| Every package in a single binary repo | `@pytest.mark.repo_kind("binary")` + `repo`, `arch`, `repo_packages` |
| Every package in a single SRPM repo | `@pytest.mark.repo_kind("srpm")` + same fixtures |
| One specific named repo | `@pytest.mark.repo_name("base")` + same fixtures |
| All binary repos at once | no marker, `binary_repos` fixture |
| Cross-repo file overlaps | `cross_repo_file_index(arch)` |
| Solver-level closure | `repoclosure(target_repos, arch)` |

### 2. Decide the failure-reporting style

Three patterns are used in this suite; pick the one that fits:

| Style | When | How |
| --- | --- | --- |
| **Aggregated** | Rule has at most one failure per `(test, arch)`, or violations are tightly related and reading them together is more useful than splitting | Collect violations into a list, then `pytest.fail("\n".join(...))` once at the end |
| **Data-parametrized** | Rule applies to a small *fixed* list of inputs known at collection time (e.g., a hard-coded `BLOCKLIST`) | `@pytest.mark.parametrize("input", LIST)`; each input becomes its own collected test case |
| **Subtests** | Rule produces a *dynamic* list of violations discovered at run time, and each one deserves its own report entry (e.g., per-package repoclosure failures, per-pair file conflicts) | Take a `subtests` fixture (provided by `pytest-subtests`) and wrap each violation in `with subtests.test(...)`; each surfaces as its own `SUBFAILED` entry without inflating the collected test count |

In the current suite:

* Aggregated: `test_no_srpms_in_binary`, `test_only_srpms_in_srpm_repo`,
  `test_vendor_tag`, `test_release_suffix`.
* Data-parametrized: `test_blocklist`.
* Subtests: `test_no_duplicate_subpackage_names`,
  `test_file_conflicts_cross_repo`, `test_repoclosure_*`.

### 3. Decide where the rules live

* If the rule is a small set of literals (a regex, a vendor string,
  a tuple of names, a dict allowlist), put them at the top of the test
  file as `UPPER_CASE` constants under a `# rules-as-code:` comment.
* If the rule needs new data from the repos (e.g., a new tag from
  RPM headers), extend `Package` in
  [`../utils/types.py`](../utils/types.py) and add the parsing in
  [`../utils/repodata.py`](../utils/repodata.py). The fixture
  surface should not need to change.

### 4. Write the test

Template:

```python
# SPDX-License-Identifier: MIT
"""<one-line summary>."""

from __future__ import annotations

import pytest

from utils.repos import Repo


# rules-as-code: edit me to ...
SOME_RULE = ...


@pytest.mark.repo_kind("binary")
def test_<rule_name>(repo: Repo, arch: str, repo_packages) -> None:
    packages = repo_packages(repo, arch)
    offenders = [p for p in packages if not _passes(p)]
    if offenders:
        listing = "\n".join(f"  - {p.nevra}" for p in offenders)
        pytest.fail(
            f"binary repo {repo.name!r} (arch {arch}) has "
            f"{len(offenders)} offending package(s):\n{listing}"
        )
```

### 5. Run it

```bash
.venv/bin/pytest cases/test_<your_test>.py -v --repo ...
```

If it doesn't apply to the repo set you have, it'll skip cleanly.
If it does apply but doesn't have the data it needs from the
fixtures, it should fail loudly — not silently — at the point where
the data is requested.

### 6. Update this catalogue

Add an entry under "Catalogue" so future contributors don't have to
read the test file to understand its scope.
