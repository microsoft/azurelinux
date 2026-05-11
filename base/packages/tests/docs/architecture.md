# Architecture

This document describes the design of the Azure Linux RPM repo
validation tests. It targets contributors who are adding new tests,
debugging existing ones, or extending the framework.

For *user-facing* documentation (how to run the tests, CLI options,
examples), see [`../README.md`](../README.md). For the catalogue of
existing tests and the recipe for adding new ones, see
[`tests.md`](tests.md).

## Goals

1. **Tests are declarative.** A test reads as a clear assertion about
   a published repo. It does not shell out to `dnf`, parse XML, or
   manage caches.
2. **Tests fan out cleanly.** A single test definition becomes one
   pytest result per `(repo, arch)` pair it applies to, with stable
   `repo-arch` ids so failures are easy to triage.
3. **Tests apply to the right repos.** Markers
   (`@pytest.mark.repo_kind(...)` / `@pytest.mark.repo_name(...)`)
   declare what the test is about; non-matching repos do not generate
   test instances at all.
4. **Backends are pluggable but narrow.** The only operation that
   meaningfully needs `dnf5` is `repoclosure`. Everything else is
   metadata-only and is implemented by parsing repodata directly,
   which keeps tests fast and decouples them from `dnf` version
   quirks.

## Layered design

```
                    ┌─────────────────────────────────────────────┐
   tests in cases/  │  test functions (pytest fixtures only)      │
                    └────────────────────────┬────────────────────┘
                                             │ uses
                    ┌────────────────────────▼────────────────────┐
   conftest.py      │  fixtures (repo, arch, repo_packages, ...)  │
                    └────────────────────────┬────────────────────┘
                                             │ calls into
                    ┌────────────────────────▼────────────────────┐
   utils/           │  MetadataService           Repoclosure      │
   (service)        │  (cache + parse)           (in-process)     │
                    └────────────┬───────────────────┬────────────┘
                                 │                   │
                    ┌────────────▼─────────┐  ┌──────▼─────────────┐
   utils/           │  repodata.py         │  │  repoclosure.py    │
   (implementation) │  librepo + createrepo│  │  libdnf5 (libsolv) │
                    └──────────────────────┘  └────────────────────┘
```

**Tests never reach below the fixture layer.** If you find yourself
wanting to import `utils.repodata` or `utils.repoclosure` from a test
file, that's a signal to extend `MetadataService` (or add a fixture)
instead.

The implementation layer is intentionally a thin shim over the
canonical dnf-stack libraries:

* **`librepo`** (`python3-librepo`) — fetches `repomd.xml`, primary,
  and filelists into a per-repo cache directory, plus per-package
  RPMs on demand; verifies checksums; decompresses zchunk / zstd /
  xz / gz transparently; substitutes `$basearch` / `$releasever` in
  URLs.
* **`createrepo_c`** (PyPI; pure-C bindings) — parses primary and
  filelists into typed `Package` objects via libxml2 (streaming).
* **`libdnf5`** (`python3-libdnf5`, libsolv bindings) — loads the
  fetched metadata into a Base/repo_sack and evaluates rich-dep
  requirements via `pool_satisfieddep_map` (the same call
  `dnf5 repoclosure` makes). Rich expressions like `(foo if bar)`,
  `(foo with bar)`, `(foo unless bar)` are evaluated as boolean
  conditionals over the available providers — no special handling
  in our code.
* **`rpm`** (`python3-rpm`, librpm bindings) — reads per-file
  metadata (mode, owner, group, size, digest, linkto) out of
  downloaded RPM headers. Used by the cross-repo file-conflicts
  test to mirror RPM's own `rpmfilesCompare` rules; the createrepo
  XML schema and libdnf5's `Package.get_files` only carry the
  path / type / digest subset.

All four are the same libraries `dnf` itself uses internally, so
the suite's metadata interpretation is guaranteed to match dnf's
without any subprocess shell-out.

## The CLI surface

Defined entirely in [`utils/pytest_plugin.py`](../utils/pytest_plugin.py).
The plugin is registered as a `pytest11` entry point in
[`pyproject.toml`](../pyproject.toml) so its options are known to
pytest *before* it parses argv. This matters because:

* `--workdir` takes a path; without early registration, pytest's
  rootdir logic could mistake the value for a positional test path.
* `--repo` values are arbitrary strings (URLs, names with hyphens, ...).

The plugin parses every `--repo` flag at `pytest_configure` time into
a list of [`Repo`](../utils/repos.py) dataclasses. Validation errors
become a single `pytest.UsageError` with a helpful message; we never
let pytest get to test collection with bad config.

### `--repo` / `--repos-file` syntax

Two equivalent input forms:

```
--repo name=...,kind=...,url=...
```

Strict `key=value` segments separated by commas. The first `=` in each
segment separates key from value, so values containing `=` are
tolerated. Values containing commas are not supported — if a real-world
URL ever needs commas, swap to a URL-encoded form or use the file form
below. URL placeholders like `$basearch` and `$releasever` are
substituted by `librepo` at fetch time.

```
--repos-file path.repo
```

A standard yum/dnf-style ini file, parsed with stdlib `configparser`.
Each section is one repo; the section name is the repo name, `baseurl=`
is the URL, and a custom `kind=` key (`binary` / `srpm` / `debuginfo`)
is required (since the dnf format has no equivalent). May be repeated;
freely combinable with `--repo`. Repo names must be globally unique
across all inputs.

### Other CLI options

The complete option list -- `--arch`, `--releasever`, `--workdir`,
`--expected-vendor`, `--release-suffix`, `--known-violations-dir`,
`--summary-json`, plus the three repo flags above -- is documented
with full semantics and defaults in
[`../README.md`](../README.md#cli-options). The two known-violations
flags are also covered in detail in the [Known-violations
engine](#known-violations-engine) section below.

## Test fan-out

Implemented in `pytest_generate_tests` in
[`utils/pytest_plugin.py`](../utils/pytest_plugin.py). The rules:

* If a test has both `repo` and `arch` parameters, parametrize over
  every matching `(repo, arch)` pair (cross product), with ids like
  `base-x86_64`.
* If a test has only `repo`, parametrize over matching repos.
* If a test has only `arch`, parametrize over arches.
* If `repo_kind` / `repo_name` markers eliminate every candidate
  repo, the test is parametrized with a single skipped entry whose
  reason names the missing kind/name. The test does *not* silently
  disappear; it shows up as a skip in pytest output, which is loud
  enough to spot in CI but doesn't break "validate only my SRPM repo"
  workflows.

## Fixture surface

Defined in [`../conftest.py`](../conftest.py). This is what tests
actually consume:

| Fixture | Scope | Returns | Used by |
| --- | --- | --- | --- |
| `repo` | function (parametrized) | one `Repo` after marker filtering | per-repo tests |
| `arch` | function (parametrized) | `str` | every repo-touching test |
| `binary_repos`, `srpm_repos`, `debuginfo_repos` | session | `list[Repo]` | cross-repo tests |
| `releasever` | session | `str | None` | rarely used directly |
| `all_repos` | session | `list[Repo]` | rarely used directly |
| `repo_packages(repo, arch)` | function | `list[Package]` | metadata-only per-repo tests |
| `all_binary_packages(arch)` | function | `dict[Repo, list[Package]]` | cross-repo metadata tests |
| `cross_repo_file_index(arch)` | function | `dict[path, list[FileOwner]]` | the file-conflicts test (first-pass overlap discovery) |
| `package_file_metadata(arch, nevra)` | function | `dict[path, FileMeta]` | the file-conflicts test (second-pass `rpmfilesCompare`) |
| `repoclosure(target_repos, arch)` | function | `RepoclosureResult` | the repoclosure tests |
| `require_named_repos(names, kind=...)` | function | `list[Repo]` | tests with hard-coded repo expectations |
| `known_violations` | function | `KnownViolationsFile` | tests that maintain a known-violations allowlist |
| `summary_recorder` | function | callable | tests that classify violations and want the verdicts in `--summary-json` |

> **`require_named_repos` semantics.** Tests that use this fixture
> declare "I cannot pass without all of these specific repos."
> Behavior:
>
> * **All names present** — returns the matching `Repo` list in input
>   order.
> * **Any names missing** (including the all-missing case) — calls
>   `pytest.fail(...)` with a clear "misconfigured run" message.
>   Hard-coded closure tests are release-gating invariants that are
>   only meaningful with the full named set provided; silently
>   skipping such a check is worse than failing loudly. Use
>   `pytest -k` / `--ignore` to deselect a hard-coded test if you
>   intentionally don't want to run it.
>
> Use the looser `binary_repos` / `srpm_repos` / `debuginfo_repos`
> fixtures when partial coverage should be tolerated.

`repo_packages`, `all_binary_packages`, and `cross_repo_file_index`
are returned as *callables* (not direct values) so each test can
invoke them with the test-time `arch` (and `repo`) instead of having
the fixture know which arch to pre-compute. The underlying
`MetadataService` memoizes results, so calling them many times is
cheap.

## The service layer

### `MetadataService` (`utils/metadata.py`)

Wraps the raw `repodata.py` loader with caching keyed by `(repo
fingerprint, arch)`. Translates loader errors into `pytest.fail` so
tests don't see noisy tracebacks from below the abstraction. Provides
the high-level operations the fixtures need:

* `list_packages(repo, arch) -> list[Package]`
* `build_file_index(repos, arch) -> dict[path, list[FileOwner]]` —
  first-pass path-overlap candidates (skips dirs and ghosts).
* `fetch_package_files(repo, package, arch) -> dict[path, FileMeta]` —
  on-demand RPM download (via librepo) plus per-file metadata
  extraction (mode/owner/group/size/digest/linkto via python3-rpm).
  Memoized per NEVRA. The file-conflicts test calls this only for
  the small set of packages involved in candidate overlaps, then
  applies `rpmfilesCompare`-equivalent rules.
* `fetch(repo, arch) -> RepoLayout` — exposes the on-disk paths of
  the librepo-fetched repomd/primary/filelists for the metadata-only
  tests. `Repoclosure` does **not** reuse this cache — see below.

### `Repoclosure` (`utils/repoclosure.py`)

In-process repoclosure runner. Builds a `libdnf5.base.Base`, hands
each universe repo's URL to libdnf5's own internal librepo (which
fetches a fresh copy of repomd/primary/filelists into a separate
per-arch / per-xdist-worker cache directory under the session
workdir), and for each checked package walks every `Requires` entry
through `PackageQuery.is_dep_satisfied` (libsolv's native rich-dep
evaluator). Reports each requirement that has no provider in the
universe.

The libdnf5-side cache is **not** shared with `MetadataService`'s
cache. An earlier revision tried to point libdnf5 at the
`MetadataService` destdir via a `file://` baseurl, but libdnf5's
internal librepo treats `file://` baseurls as remote mirrors:
(a) it demands every record listed in `repomd.xml` (e.g.
`other.xml.zst`, `updateinfo.xml.zst`), which `MetadataService`
deliberately does not download, and (b) it refuses to start when the
destdir is already populated. The duplicate fetch is roughly 10MB
per repo, paid once per session, in exchange for two layers that
each own their own cache cleanly.

```python
def run(
    self,
    *,
    target_repos: list[Repo],
    arch: str,
    universe_repos: list[Repo] | None = None,
    check_kind: str = "binary",  # "binary" | "buildtime" | "all"
) -> RepoclosureResult: ...
```

`target_repos` are the repos whose packages we expect to close;
`universe_repos` (when wider than `target_repos`) are the repos that
contribute providers. `check_kind` selects which package arches the
*checker* examines:

* `"binary"` — `[arch, noarch]` — pure runtime closure of binary
  packages.
* `"buildtime"` — `[arch, noarch, src, nosrc]` — used by the
  combined runtime + build-time closure test
  (`test_repoclosure_base_plus_sdk_full`). Catches BOTH unresolved
  BuildRequires (because src/nosrc are checked) AND runtime breakage
  in the binary packages that provide those BuildRequires (because
  arch/noarch are also checked). For `"buildtime"` we also disable
  the per-target-repo filter on findings: a binary provider from
  `base ∪ sdk` whose own runtime deps are broken is exactly the kind
  of cross-repo failure this kind exists to catch, so it must be
  surfaced even though its source repo is not in `target_repos`. The
  test partitions findings by consumer arch into the runtime and
  buildtime gap classes for assertion against parallel
  known-violations sections.
* `"all"` — no arch filter on the checker.

`libdnf5` is the libsolv binding `dnf5 repoclosure` itself uses, so
the rich-dep semantics match exactly: every `Requires` must have a
provider in the universe filtered to latest EVR per name (the
`best=1` model dnf uses at install time). Rich/boolean dependencies
(`if`, `unless`, `with`, `or`, `and`, `else`) are evaluated
correctly without any special handling in our code —
`pool_satisfieddep_map` treats them as boolean conditionals over
the available providers, so a `(foo if bar)` whose trigger has no
provider is correctly reported as satisfied.

We deliberately deviate from `dnf5 repoclosure` in **one** place:
the *to-check* set is also filtered to latest EVR per name. Stock
`dnf5 repoclosure` walks every NEVRA in the target repo, which
means a snapshot that publishes both N-1 and N of a tightly-pinned
package family (e.g. all of `azurelinux-release-*` carried at both
`-12.azl4` and `-13.azl4` mid-rebuild) reports the older `-12.azl4`
set as broken — its peers were filtered out by the latest-EVR
filter on the available side. That signal is technically true ("you
can no longer downgrade to `-12.azl4`") but not actionable: the
repo's *latest installable* state is the only thing closure is
meant to validate. Filtering the to-check side too means we
effectively ask *"would `dnf install <pkg>` actually pick a
closeable set?"* This still catches kernel/anaconda-style
version-pinning bugs (those have a *single* EVR pinning a
*missing* peer, not an *older* EVR pinning an older but present
peer), so no real signal is lost.

There is no subprocess shell-out; no JSON-vs-text output
schema-drift handling; no `--json` capability probe; no
host-vs-container backend split. The previous abstraction existed
only because older host `dnf5` builds lacked `--json`, which is
irrelevant when we drive the solver in-process.

## Known-violations engine

A handful of tests carry a per-test allowlist of *known violations* --
gaps that are real, tracked, and intentionally tolerated for now (so
the overall test stays green and a single new regression stands out)
while still being reported as `XFAIL` subtests so they remain visible
in pytest output and JUnit XML.

The allowlists are TOML files at
[`../cases/known-violations/<test-stem>.toml`](../cases/known-violations/),
validated against
[`../cases/known-violations.schema.json`](../cases/known-violations.schema.json)
at load time so authoring mistakes (typo'd section, wrong shape,
empty values) surface with a clear message rather than a confusing
`KeyError` deep in the test. Both flat (`[<section>]`) and arch-gated
(`[<section>-arch-gated."<name>"]`) entries are supported in parallel;
they merge back into one in-memory mapping per section.

Each entry can be written in either of two equivalent forms. The
short form is a bare array of strings -- the curator default for the
common case where a one-line allowlist is enough:

```toml
[runtime-missing]
cinnamon = [ "libgcr-base-3.so.1()(64bit)" ]
```

The long form is an inline table that carries the same `deps` array
plus optional metadata: `reason` (free-text rationale) and `issue`
(a tracking URL or shorthand). Both fields are surfaced in the
subtest output and the `--summary-json` records, so CI consumers and
human triage can see *why* a violation is tolerated without grepping
git blame:

```toml
[runtime-missing]
cinnamon = { deps = [ "libgcr-base-3.so.1()(64bit)" ], reason = "gcr3 deprecated upstream; needs port to gcr4", issue = "AB#123456" }
```

Both forms desugar to the same internal representation. There is no
schema-version bump -- bare arrays remain valid v1.

A single shared engine in
[`../utils/known_violations.py`](../utils/known_violations.py)
classifies every observed violation against the allowlist into one of
four buckets:

| Verdict | Meaning | Subtest result |
| --- | --- | --- |
| `real-fail` | consumer not in allowlist, OR observed values exceed listed values | fail |
| `xfail` (known-violation) | consumer in allowlist and observed ⊆ listed | xfail |
| `stale-consumer` | consumer is listed but no finding aggregates to it on this arch | fail (cleanup nudge) |
| `stale-dep` | consumer is listed and observed, but a listed value was not observed | fail (cleanup nudge) |

The classifier is generic on the finding key type so the same engine
drives both the repoclosure tests (per-NEVRA findings, consumer =
`NEVRA.name`) and the duplicate-subpackage test (per-binary-name
findings, consumer = the binary name itself). Per-test message
rendering and subtest-key shape stay in the calling test; the engine
returns three independent buckets (`real_fails`, `known_violations`,
`stale`) and the test wraps each entry in its own `subtests.test(...)`
context with test-appropriate keys.

The loader and engine are accompanied by:

* **`--known-violations-dir DIR`** -- override the in-repo default
  location so CI can point at an alternative allowlist tree without
  editing the defaults.
* **`summary_recorder` fixture** -- session-wide JSON-summary
  accumulator. When `--summary-json=PATH` is set, every classified
  result is written out at session end as a JSON file with a
  `schema_version` wrapper and one record per `(test_nodeid, arch,
  source_label)`. CI can gate on `real_fails` and surface stale drift
  without re-parsing pytest output. The on-disk shape is pinned by
  [`../cases/summary-json.schema.json`](../cases/summary-json.schema.json)
  (JSON Schema 2020-12) and validated structurally by the unit
  tests, so any future drift in the writer's payload that the
  schema doesn't allow fails CI loudly. Stock `--junitxml` continues
  to emit per-subtest pass/fail/xfail records for human triage; the
  two flags compose orthogonally.

### Allowlist mechanism taxonomy

Three different allowlist-shaped mechanisms coexist in this suite,
because they are answers to three different questions. Tracking them
here so future contributors don't accidentally collapse them into
one implementation:

| Kind | Polarity | Where it lives | Example | Cleanup intent? |
| --- | --- | --- | --- | --- |
| **(a) Hard-coded blocklist** | inverse: things that must *never* appear | in-code (per-test) | `GLOBAL_BLOCKLIST` in [`../cases/test_blocklist.py`](../cases/test_blocklist.py) | none -- this *is* the policy |
| **(b) Intentional silent allowlist** | by-design coexistence | in-code (per-test) | `ALLOWLIST` in [`../cases/test_no_duplicate_subpackage_names.py`](../cases/test_no_duplicate_subpackage_names.py); `PATH_ALLOWLIST` in [`../experimental-cases/test_file_conflicts_cross_repo.py`](../experimental-cases/test_file_conflicts_cross_repo.py) | none -- the listed entries are *correct* and the allowlist filters them out before classification, with no XFAIL noise |
| **(c) Tracked-but-tolerated allowlist** | XFAIL-track for cleanup | TOML files under [`../cases/known-violations/`](../cases/known-violations/), validated against `known-violations.schema.json` | `[runtime-missing] cinnamon = [ "libgcr-base-3.so.1()(64bit)" ]` | yes -- every entry is supposed to shrink and eventually disappear; stale-consumer / stale-dep rails fail the run as cleanup nudges |

Why the carve-up:

* Policy (a) is small, slow-changing, and lives in the repo as the
  test's own definition. Pulling it into TOML would split the policy
  across two files for no benefit.
* Intentional coexistence (b) is per-test, *narrow*, and not subject
  to the cleanup-pressure rails. Routing it through the
  known-violations engine would give it XFAIL noise it does not
  deserve and stale-rails that would force-fail the run when the
  intentional shim was ever rebuilt with a different SRPM
  combination. (b) is also genuinely additive policy: a one-time
  decision that two binaries with the same name are fine, captured
  next to the test that enforces "binaries with the same name are
  *usually* a bug".
* Tracked tolerance (c) is the *opposite*: every entry is technically
  wrong and is meant to be cleaned up. Externalising it into TOML
  files keeps the diff churn out of the test code, makes the entries
  greppable across tests, and lets the loader / classifier surface
  metadata (reason, issue) and run the stale-cleanup rails uniformly.

The test docstrings (most importantly
[`../cases/test_no_duplicate_subpackage_names.py`](../cases/test_no_duplicate_subpackage_names.py))
cite this section so a reader who lands there understands why two
parallel allowlist mechanisms coexist in the same test.

## Implementation layer

### `utils/repodata.py`

A thin wrapper over `librepo` (fetch + verify + decompress) and
`createrepo_c` (parse). librepo writes `repomd.xml` and the
`primary` + `filelists` records into a per-repo cache directory,
verifying SHA checksums against repomd and decompressing zchunk /
zstd / xz / gz transparently. `createrepo_c.xml_parse_primary` and
`xml_parse_filelists` then stream the underlying file via libxml2 —
memory stays bounded for very large filelists (tens to hundreds of
MB uncompressed).

The previous implementation hand-rolled HTTP fetch with retries,
checksum verification, multi-format decompression (gz/xz/zstd via
`zstandard`), and `defusedxml.iterparse` of primary + filelists —
~700 lines that did exactly what librepo+createrepo_c already do.
The dnf stack uses these same libraries internally, so the two
codepaths are now guaranteed to interpret repodata identically.

### `utils/repoclosure.py`

A thin wrapper over `libdnf5`. `Repoclosure.run` builds a
`libdnf5.base.Base`, hands each universe repo's URL to libdnf5's
own internal librepo (which writes a fresh copy of repomd/primary/
filelists into a separate per-arch / per-xdist-worker cache
directory under the session workdir -- see the `Repoclosure`
service-layer section above for why this cache is intentionally
*not* shared with `MetadataService`'s cache), filters BOTH the
available-providers query and the to-check query to latest EVR per
name (see semantics discussion above), and walks every checked
package's `Requires` looking for entries that
`PackageQuery.is_dep_satisfied` reports as unsatisfied.
`rpmlib(...)` and `solvable:prereqmarker` synthetic deps are
already filtered by libdnf5 (matching `dnf5 repoclosure`'s own
behaviour).

The previous implementation shelled out to `dnf5 repoclosure` and
parsed its output (JSON when available, falling back to a
line-oriented text parser); it shipped two backends (host and
container) plus an output-format-capability probe and per-finding
NEVRA reparser. All of that is gone — we just call libsolv via
libdnf5, in-process, with a few dozen lines.

An earlier in-process revision used `hawkey.Query.filter(provides=)`
on each Requires entry. That looked correct but actually treated
rich expressions as literal Provides strings (libsolv was being
asked "does any Solvable literally Provides the string
`(foo if bar)`?", which is never true), so every rich dep was
reported as unresolved. `libdnf5.rpm.PackageQuery.is_dep_satisfied`
is the call `dnf5 repoclosure` itself uses; it routes through
`pool_satisfieddep_map`, which evaluates the full rich grammar.

## Caching strategy

The session workdir defaults to a fresh `tempfile.mkdtemp(...)` and
is removed at session end. With `--workdir` set, it is reused as-is
and never cleaned (post-mortem friendly).

`MetadataService` writes repomd, primary, and filelists artifacts
under
`<workdir>/repodata/rv-<releasever-or-none>/<xdist-worker>/<arch>/<reponame>-<fingerprint>/`
where `fingerprint` is a stable short hash over `(name, kind, url)`.
The xdist-worker scope keeps two parallel pytest workers from racing
each other on the same destdir (librepo writes the same filenames
each run, so without per-worker scope two simultaneous fetches of
the same repo would clobber each other's `repomd.xml`).

This means **a reused workdir cannot serve stale metadata** if any of
url, arch, or releasever changes between runs. The repoclosure
runner does *not* reuse this cache — it maintains its own per-arch /
per-xdist-worker libdnf5 cache subdirectory under the same workdir
(see the `Repoclosure` section above for the rationale).

## URL placeholders

`librepo` substitutes `$basearch`, `$arch`, and `$releasever` directly
when fetching. We pass the chosen arch and releasever to librepo via
`Handle.varsub`; the URL stored in the `Repo` dataclass keeps the
placeholders verbatim so the same `Repo` object can be reused across
arches without mutation.

If a URL contains `$releasever` and `--releasever` was not provided,
the plugin raises `pytest.UsageError` at `pytest_configure` time so
the user gets a single clean message before any test starts.

## Why these libraries (and not stdlib + dnf5 shell-out)?

The previous design parsed repodata directly with stdlib XML to
avoid pulling in dnf — but that re-implemented exactly what
`createrepo_c` and `librepo` already do, including some sharp edges
(zchunk handling, atomic write semantics for parallel xdist runs,
zstd decompression on Python <3.14). Adopting the canonical
libraries:

* **Eliminates the host-vs-container backend split.** The split
  existed only because older host `dnf5` builds lacked
  `repoclosure --json`. Driving libsolv in-process via libdnf5 makes
  output parsing irrelevant — there is no output.
* **Removes ~1300 lines of infra code** (XML iterparse, HTTP retry
  loop, checksum verify, decompression fallbacks, JSON-vs-text
  parsers, NEVRA regex, JSON capability probe, `.repo` file
  rendering, subprocess plumbing, container bind-mount logic).
* **Aligns metadata interpretation with dnf** — when dnf changes
  its parsing of a quirky tag, we change with it for free.
* **Speeds up runs** — no subprocess fork per repoclosure
  invocation; metadata is parsed once per session and reused by
  every dependent test.

The new requirements are system packages (`python3-librepo`,
`python3-libdnf5`, `python3-rpm`), not pip-installable wheels.
This is consistent with the previous host-backend requirement on
the `dnf5` binary; users running the suite in a Fedora/AZL/RHEL
container or on those distros already have them. See
[`../README.md`](../README.md) for installation guidance.

## Adding a new test

See [`tests.md`](tests.md) — the section "How to add a new test"
walks through marker selection, fixture choice, and the
aggregate-vs-data-parametrize decision.
