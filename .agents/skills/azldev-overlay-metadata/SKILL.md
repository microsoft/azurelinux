---
name: azldev-overlay-metadata
description: "Read this before adding or reviewing an overlay `metadata` table; do not guess the category or upstream status from memory. Explains the overlay metadata schema that documents why an overlay exists and when it can be dropped, covering the required category and upstream-status values, commit/bug URL references, and the per-file overlay metadata block. Triggers include overlay metadata, category, upstream-status, upstream-backport, azl-pruning, azl-branding-policy, needs-upstream-hook, why overlay."
---

# Overlay metadata — pick a category and annotate

Every overlay documents *why* it exists (`description`, **required**) and *what class
of change* it is (`metadata`). When a `[metadata]` block is present it **requires** both
a `category` and an `upstream-status`. This skill covers how to pick the right values,
attach provenance, and write the TOML at the moment you author or review an overlay.

Metadata is **pure documentation** — it never changes the rendered spec and is excluded
from component fingerprints, so adding or editing it never invalidates build caches or
locks. For overlay *types* and the render-and-inspect loop, read the `azldev-overlays`
skill; this skill is only about the `metadata` table.

## One `[metadata]` block = one logical change

A single logical change (a CVE backport, a feature disablement, a Fedora cherry-pick)
may need **several overlays** — e.g. remove a sub-package *and* drop the configure flags
that went with it. The per-file overlay format (`overlay-files`) captures exactly this:
one top-level `[metadata]` table and one or more `[[overlays]]` entries it applies to.
Per-overlay `metadata` inside an overlay file is **rejected** — the file-level block is
the single source of truth.

So: if you find yourself stamping the *same* metadata on several inline overlays, that is
a signal they are one logical change — move them into a single overlay file with one
`[metadata]` block.

## When to add metadata

- **New overlay** (any inline `[[components.<name>.overlays]]` block or `[[overlays]]`
  entry in an overlay file): add `metadata` with both a `category` and an `upstream-status`.
- **An overlay's intent changed** (e.g. a prune becomes a backport): update the `category`
  and `upstream-status` to match the new intent.

## Step 1 — Pick the category

Choose exactly one `category` from this closed set (authoritative — matches
`metadata.category` in the schema):

| `category` | Use when the overlay… | Extra required/expected fields |
|------------|-----------------------|--------------------------------|
| `upstream-backport` | Backports a fix from an upstream source (Fedora dist-git or the component's OSS project) that AZL will inherit once it bumps past the fix. Self-resolves on version bump. | `commits` (≥1 upstream commit URL) — **required**. `upstream-status` must be `upstreamed` or `upstreamable`. |
| `azl-pruning` | Removes content for AZL: unshipped deps, unneeded features, sub-packages, or files. | — |
| `azl-compatibility` | Adapts a component to *how Azure Linux is built and shipped* — build tooling, buildroot, infrastructure, runtime ecosystem — when upstream builds/behaves incorrectly for AZL-specific reasons that are **not** branding, a missing dependency, architecture, or tests (e.g. `azldev` downloader quirks, `rpmdiff` reproducibility, buildroot gaps, Fedora version-skew). | — |
| `azl-temp-workaround` | Temporary workaround explicitly intended to be dropped once an upstream or environmental fix lands. Covers a dependency not yet imported into AZL (or unavailable on a target) **and** any other transient workaround waiting on an external change. | — |
| `azl-branding-policy` | Fedora→Azure Linux identity differences: intentional name/path/vendor conventions **and** spec fixes for upstream code that hard-codes Fedora identity strings (e.g. `_vendor=redhat`, `<cpu>-redhat-linux[-gnu]` triples, `redhat-linux-build` dirs). Also covers repointing a `Source`/`URL` tag from a Fedora mirror to an Azure Linux one (e.g. `azurelinux-rpm-config`, `golang`). | — |
| `azl-disable-flaky-tests` | Skips tests that fail intermittently / due to environmental flakiness, not a real component bug. | — |
| `azl-disable-unsupported-tests` | Skips tests that cannot meaningfully run in AZL's build/runtime env (need network, root, or unavailable hardware in mock). | — |
| `azl-security-compliance` | Makes FIPS or crypto-policy changes. | — |
| `azl-release-management` | Adjusts release-tag / changelog mechanics. | — |
| `azl-platform-adaptation` | Makes architecture-specific adjustments. | — |

### Disambiguation tips

- **Backport vs. compatibility/pruning:** if the exact change exists as a commit in Fedora
  dist-git or the upstream project, it is `upstream-backport` (supply `commits`, with
  `upstream-status` of `upstreamed` or `upstreamable`). Use an `azl-*` category only when
  the change is AZL-specific with no upstream equivalent.
- **Pruning vs. temp-workaround:** removing a dependency we deliberately don't ship is
  `azl-pruning`; temporarily working around a dep that *should* exist but hasn't been
  imported yet (or any transient workaround waiting on an external fix) is
  `azl-temp-workaround`.
- **Flaky vs. unsupported tests:** flaky = the test *could* pass but is intermittent;
  unsupported = the test *cannot* run in mock (network/root/hardware). Require evidence of
  the limitation before choosing `azl-disable-unsupported-tests`; investigate or ask when
  the failure mode is unclear.
- **Compatibility vs. platform-adaptation:** reserve `azl-platform-adaptation` for
  architecture-specific (`%ifarch`-style) changes; general toolchain/mock/build-env fixes
  are `azl-compatibility`.

## Step 2 — Set `upstream-status`

Required whenever `[metadata]` is present. It classifies the overlay's relationship to
upstream — "why are we carrying this?" and "what would it take to drop it?" Pick exactly one:

| Value | Meaning |
|-------|---------|
| `upstreamed` | Already in Fedora; carried only until AZL bumps past it. |
| `upstreamable` | The patch we carry is itself upstream-shaped (or already in the OSS project but not in Fedora yet); the same diff could be sent upstream and plausibly accepted. Link the upstream PR when you can. |
| `needs-upstream-hook` | AZL-specific change that upstream wouldn't take as-is, but upstream could add a `bcond`/`%if`/config knob so we could drop the overlay. |
| `inapplicable` | Permanent AZL-only deviation with no upstream story (branding, deliberate pruning, enterprise policy). |
| `unknown` | Not yet assessed. Prefer a definite value; reviewers should push back on `unknown` before approving. |

On an `upstream-backport` overlay only `upstreamed` and `upstreamable` are allowed — any
other value is a validation error.

**`upstreamable` vs. `needs-upstream-hook`:** `upstreamable` means the patch we carry is
itself upstream-shaped (send the same diff upstream); `needs-upstream-hook` means the
change is AZL-specific and would *not* be accepted as-is, but upstream could add a hook
that makes patching unnecessary.

## Step 3 — Add provenance (`commits`, `bugs`)

- `commits` — list of `{ url = "..." }` tables pointing at upstream commits (absolute
  http(s) URLs). **Required for `upstream-backport`**; optional elsewhere but valuable
  whenever a change traces to a specific commit. For one logical change spanning several
  commits, list them all. Verify each SHA actually exists upstream before recording it — a
  discovered-and-verified URL is not "inventing" metadata; an unverified guess is.
- `bugs` — list of `{ url = "..." }` tables referencing tracker entries. Never fabricate one.

## Step 4 — Write the metadata (TOML forms)

**Prefer the per-file layout (an overlay file loaded via `overlay-files`) for all new
work — even a component with a single overlay.** It keeps `category`/`commits`/`bugs` on
their own lines (no inline-table one-line limit) and means a change never has to be
reshuffled when it grows a second overlay. One top-level `[metadata]` table applies to
every `[[overlays]]` entry in the file.

Multi-overlay change (one logical change, several overlays):

```toml
# One logical change: drop the devel sub-package AZL does not ship.
[metadata]
category = "azl-pruning"
upstream-status = "inapplicable"

[[overlays]]
description = "Remove the devel sub-package — AZL ships no -devel for this component"
type = "spec-remove-subpackage"
package = "devel"

[[overlays]]
description = "Drop the BuildRequires only the devel sub-package needed"
type = "spec-remove-tag"
tag = "BuildRequires"
value = "some-devel-only-dep"
```

### Inline forms

Use inline `metadata` only when the component is already inline and you are not
restructuring it. A single-line inline table must fit on one line (no lists), so it is
limited to one or two scalar fields:

```toml
[[components.rpm.overlays]]
description = "Customize RPM vendor to Azure Linux"
type = "spec-search-replace"
regex = "RPM_VENDOR=redhat"
replacement = "RPM_VENDOR=azurelinux"
metadata = { category = "azl-branding-policy", upstream-status = "inapplicable" }
```

Use the sub-table form whenever you need a list (`commits`, `bugs`) or more than a couple
of fields:

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

Adding or editing metadata must be a no-op on the rendered spec. Re-render and confirm
there is no diff:

```sh
azldev comp render -p <name>
git diff specs/
```

If you also moved overlays into files, prove the apply order was preserved with
`azldev comp diff-sources -p <name>` before and after — any difference means an overlay
changed or the sequence shifted. Metadata-only edits need no rebuild or lock refresh; if
you also changed an overlay's behavior, finalize with the `azldev-update-component` skill.

Generated by `azldev docs agent`; do not hand-edit. Generated for azldev version `v0.4.0`.
