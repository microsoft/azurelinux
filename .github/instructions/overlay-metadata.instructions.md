---
applyTo: "**/*.comp.toml, **/*.overlay.toml"
description: How to pick a `category` and attach `metadata` when you add or modify an overlay while working on a component. Read this whenever you write a new `[[...overlays]]` entry or `.overlay.toml` file.
---

# Overlay Metadata — Category Selection & Annotation

Every overlay in Azure Linux documents *why* it exists (`description`, **required**)
and *what class of change* it is (`metadata.category`, **required** when a
`[metadata]` block is present, alongside `metadata.upstream-status`). This file
tells you how to pick the right category and stamp the metadata **at the moment you
write the overlay**.

## The unit of intent: one overlay file = one logical change

An overlay file (`.overlay.toml`) is the **unit of intentional change** — it says
"these edits go together." A single logical change may require **several
overlays** (e.g. remove a subpackage *and* drop the `--disable-<thing>` configure
flags that went with it, or a backport that touches the spec and adds a patch).
That is why the per-file format has exactly **one** top-level `[metadata]` block
and a list of one or more `[[overlays]]` entries it applies to. Per-overlay
`metadata` inside an overlay file is **rejected** — the file-level block is the
single source of truth.

So: **one `[metadata]` block = one logical change.** If you find yourself giving
several inline overlays the *same* metadata, that is a signal they are one logical
change — `azldev` does not currently reject duplicated inline metadata, but you
**should** move them into a single `.overlay.toml` file with one `[metadata]`
block.

## When to add metadata

- **New overlay** (any `[[components.<name>.overlays]]` block or `[[overlays]]`
  entry in a `.overlay.toml`): add `metadata` with both a `category` and an
  `upstream-status`.
- **Modifying an existing overlay's intent** (e.g. a prune becomes a backport):
  update the `category` (and `upstream-status`) to match the new intent.

Metadata is excluded from component fingerprints, so adding or editing it never
invalidates build caches or locks.

## Step 1 — Pick the category

Choose exactly one `category` from this closed set (these ten values are
authoritative — they match `metadata.category` in the schema):

| `category` | Use when the overlay… | Extra required/expected fields |
|------------|-----------------------|--------------------------------|
| `upstream-backport` | Backports a fix from an upstream source (Fedora dist-git or the component's OSS project) that AZL will inherit once it bumps past the fix. Self-resolves on version bump. | `commits` (≥1 upstream commit URL) — **required**. `upstream-status` must be `upstreamed` or `upstreamable`. |
| `azl-pruning` | Removes content for AZL: unshipped deps, unneeded features, subpackages, or files. | — |
| `azl-compatibility` | Adapts a component to *how Azure Linux is built and shipped* — build tooling, buildroot, infrastructure, runtime ecosystem — when upstream builds/behaves incorrectly for AZL-specific reasons that are **not** branding, a missing dependency, architecture, or tests (e.g. `azldev` downloader quirks, `rpmdiff` reproducibility, buildroot gaps, Fedora version-skew). | — |
| `azl-temp-workaround` | Temporary workaround explicitly intended to be dropped once an upstream or environmental fix lands. Covers a dependency not yet imported into AZL (or unavailable on a target) **and** any other transient workaround waiting on an external change. | — |
| `azl-branding-policy` | Fedora→Azure Linux identity differences: intentional name/path/vendor conventions **and** spec fixes for upstream code that hard-codes Fedora identity strings (e.g. `_vendor=redhat`, `<cpu>-redhat-linux[-gnu]` triples, `redhat-linux-build` dirs). | — |
| `azl-disable-flaky-tests` | Skips tests that fail intermittently / due to environmental flakiness, not a real component bug. | — |
| `azl-disable-unsupported-tests` | Skips tests that can't meaningfully run in AZL's build/runtime env (need network, root, or unavailable hardware in mock). | — |
| `azl-security-compliance` | Makes FIPS or crypto-policy changes. | — |
| `azl-release-management` | Adjusts release-tag / changelog mechanics. | — |
| `azl-platform-adaptation` | Makes architecture-specific adjustments. | — |

### Disambiguation tips

- **Backport vs. compatibility/pruning:** if the exact change exists as a commit
  in Fedora dist-git or the upstream project, it's `upstream-backport` (and you
  must supply `commits`, with `upstream-status` of `upstreamed` or `upstreamable`).
  Only use an `azl-*` category when the change is AZL-specific with no upstream
  equivalent.
- **Pruning vs. temp-workaround:** removing a dependency we deliberately
  don't ship is `azl-pruning`; temporarily working around a dep that *should*
  exist but hasn't been imported yet (or any transient workaround waiting on an
  external fix) is `azl-temp-workaround`.
- **Flaky vs. unsupported tests:** flaky = the test *could* pass but is
  intermittent; unsupported = the test *cannot* run in mock (network/root/hardware).
- **Compatibility vs. platform-adaptation:** reserve `azl-platform-adaptation`
  for architecture-specific (`%ifarch`-style) changes; general
  toolchain/mock/build-env fixes are `azl-compatibility`.

## Step 2 — Set `upstream-status` (required when `metadata` is present)

A string classifying the overlay's relationship to upstream — "why are we
carrying this?" and "what would it take to drop it?" Pick exactly one:

| Value | Meaning |
|-------|---------|
| `upstreamed` | Already in Fedora; carried only until AZL bumps past it. |
| `upstreamable` | Local fix and/or already in OSS project but not in Fedora yet. Could be sent upstream as-is. Link the upstream PR when you can. |
| `needs-upstream-hook` | AZL-specific change that today needs invasive spec edits; upstream could add a `bcond`/`%if`/config knob so we could drop the overlay. |
| `inapplicable` | Permanent AZL-only deviation with no upstream story. |
| `unknown` | Not yet assessed. Reviewers should push for a definite value before approving. |

`upstream-status` is **required** whenever `[metadata]` is present. On an
`upstream-backport` overlay only `upstreamed` and `upstreamable` are allowed — any
other value is a validation error.

**`upstreamable` vs. `needs-upstream-hook`:** `upstreamable` means the patch we
carry is itself upstream-shaped (send the same diff upstream); `needs-upstream-hook`
means the change is AZL-specific and would *not* be accepted as-is, but upstream
could add a hook that makes patching unnecessary.

## Step 3 — Add provenance (`commits`, `bugs`)

- `commits` — list of `{ url = "…" }` tables pointing at upstream commits
  (absolute http(s) URLs). **Required for `upstream-backport`**; optional elsewhere
  but valuable whenever a change traces to a specific commit. For a single logical
  change that spans several commits, list them all. Verify each SHA actually exists
  before recording it.
- `bugs` — list of `{ url = "…" }` tables referencing tracker entries.

## Step 4 — Write the metadata (TOML forms)

**Prefer the per-file layout (`.overlay.toml`) for all new work — even a component
with a single overlay.** It keeps `category`/`commits`/`bugs` on their own lines
(no inline-table one-line limit) and means a change never has to be reshuffled when
it grows a second overlay. Reach for inline `metadata` only when editing a
component that is already inline and you don't want to restructure it.

**Per-file layout** — one top-level `[metadata]` table applies to every
`[[overlays]]` entry in the file.

Single-overlay change:

```toml
# One logical change: rebrand the RPM vendor for Azure Linux.
[metadata]
category = "azl-branding-policy"
upstream-status = "inapplicable"

[[overlays]]
description = "Customize RPM vendor to Azure Linux"
type = "spec-search-replace"
regex = "RPM_VENDOR=redhat"
replacement = "RPM_VENDOR=azurelinux"
```

Multi-overlay change:

```toml
# One logical change: drop the maven-local-openjdk21 subpackage.
[metadata]
category = "azl-pruning"
upstream-status = "inapplicable"

[[overlays]]
description = "Remove maven-local-openjdk21 %package section — AZL ships no java-21-openjdk"
type = "spec-remove-subpackage"
package = "maven-local-openjdk21"

[[overlays]]
description = "Remove maven-local-openjdk21 %files section — subpackage above is gone"
type = "spec-remove-subpackage"
package = "javapackages-local-openjdk21"
```

### File layout & naming

Set `overlay-files` on the component to one or more globs (resolved relative to the
component config) and put one overlay file per logical change into a directory. The
conventional layout is a sibling `overlays/` directory with a `*.overlay.toml`
suffix — neither is strictly required (`overlay-files` is just a glob), but follow
the convention unless you have a reason not to:

```
base/comps/mypackage/
├── mypackage.comp.toml
└── overlays/
    ├── 0001-cve-2024-1234.overlay.toml
    ├── 0002-disable-broken-tests.overlay.toml
    └── 0003-azl-branding.overlay.toml
```

```toml
# mypackage.comp.toml
[components.mypackage]
overlay-files = ["overlays/*.overlay.toml"]
```

`overlay-files` can also be set on `default-component-config` at the project,
distro, or component-group level, so you don't have to repeat the same pattern in
every component's TOML. Inherited relative patterns are resolved per concrete
component (from its config file, or the matched spec's directory), making a default
like `overlay-files = ["overlays/*.overlay.toml"]` a convenient
component-local discovery rule. A component that sets its own `overlay-files`
**replaces** the inherited list; use `overlay-files = []` to opt out, or list both
the inherited and component-specific patterns to keep default discovery and add
more.

Naming and ordering rules:

- **Prefix every file with a numeric ordinal** (`0001-`, `0002-`, …). Files load in
  **filename (lexicographic) order** within each glob, and globs concatenate in
  declaration order, so the ordinal makes the apply order obvious and stable.
- **Give the file a short, descriptive slug** after the ordinal that names the
  logical change (`0001-cve-2024-1234`, `0002-disable-broken-tests`,
  `0003-drop-openjdk21`). One file = one logical change, so the slug should read
  like a one-line summary of that change.
- Overlays loaded via `overlay-files` are **appended after** any inline overlays
  still declared on the component. To avoid surprising apply order, move **all** of
  a component's overlays into files rather than mixing inline + file overlays.
- Relative `source` paths inside an overlay file resolve against the **overlay
  file's own directory**, not the component config — a sibling patch in the
  component root becomes `source = "../my.patch"`.

### Inline forms (not recommended, the support will be removed in the future)

**Single-line inline table** — one or two scalar fields, ≤ ~80 chars. Must fit on
one line (no lists):

```toml
[[components.rpm.overlays]]
description = "Customize RPM vendor to Azure Linux"
type = "spec-search-replace"
regex = "RPM_VENDOR=redhat"
replacement = "RPM_VENDOR=azurelinux"
metadata = { category = "azl-branding-policy", upstream-status = "inapplicable" }
```

**Sub-table form** — required whenever you need a list (`commits`, `bugs`) or more
than a couple of fields:

```toml
[[components.xclock.overlays]]
description = "Pass --force to autoreconf so the build survives newer autotools"
type = "spec-search-replace"
regex = "autoreconf -i"
replacement = "autoreconf -fi"

[components.xclock.overlays.metadata]
category = "upstream-backport"
upstream-status = "upstreamed"
commits = [{ url = "https://src.fedoraproject.org/rpms/xclock/c/1e407488" }]
```

## Step 5 — Verify

After editing, confirm the metadata parses and is attached where you expect. This
is a no-op on the rendered spec:

```bash
# Rendered spec must be unchanged by the metadata itself
azldev comp render -p <name>
git diff specs/
```

If you added or modified the overlay's actual behavior (not just metadata),
follow the normal build + smoke-test protocol in
[`AGENTS.md`](../../AGENTS.md) and re-run `azldev comp update -p <name>` before
opening a PR. Metadata-only edits need neither a rebuild nor a lock refresh.
