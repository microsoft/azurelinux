---
name: skill-fedora-mirror-injections
description: "[Skill] Diagnose Azure Linux Stage 1 (bootstrap-mirror) BuildRequires resolution failures and backfill missing RPMs into the prod Fedora updates mirror via the azl-infra injections file. Use when triaging stage-1 / azl4-bootstrap-mirror build failures, finding dependency gaps in the Fedora mirror, deciding whether a failure is a real mirror gap vs a transient timeout or a spec bug, adding entries to azl4-stage1-injections.yaml, or opening a PR with mirror injections. Triggers: bootstrap-mirror, stage 1 build failure, fedora mirror gap, missing BuildRequires, nothing provides crate, no match for argument, injections file, azl4-stage1-injections, mirror injection."
---

# Fedora Mirror Injections (AzL4 Stage 1 dependency gaps)

Diagnose `BuildRequires` resolution failures in AzL4 Stage 1
(`*-bootstrap-mirror`) builds, decide which are real prod-mirror gaps, and
backfill the missing RPMs via `azl4-stage1-injections.yaml` in `azl-infra`.

Validated on the `mirror_bootstrap0623` round (draft PR #27888; 34-package
retest all passed).

## Repos You Need

- **`azl-infra`** — holds the injections file and mirror tooling. Clone from:
  `https://dev.azure.com/mariner-org/polar/_git/azl-infra`
  (Azure DevOps org `mariner-org`, project `polar`). The relevant tree is
  `scripts/fedora_mirror/`.
- **`azurelinux`** — the package specs (for spec-fix cases). Clone from:
  `https://github.com/microsoft/azurelinux.git` (branch `4.0`).

## When to Use This Skill

Use when the user asks to:
- Triage a stage-1 / `azl4-bootstrap` build failure or triage summary.
- Find what RPMs are missing from the prod Fedora updates mirror.
- Add / verify entries in the injections file.
- Decide if a failure needs a mirror injection, a retest, or a spec fix.
- Open a PR adding entries to the injections file.

## Mental Model — a resolution failure IS a mirror gap

Stage 1 (`azl4-bootstrap-mirror`) builds resolve **all** `BuildRequires`
from the prod Fedora mirror alone (`kojifedoramirror.blob.core.windows.net`).
Koji-built RPMs from the same build set are **not** used as build deps, so
**build ordering is irrelevant** — a resolution failure means the mirror
lacks that exact NVR/crate version, even if the provider built fine in the
same run. Do not dismiss these as build-order races.

Repo split: `fedora-43-everything` (base release) is frozen and consumed
**live** from upstream; `fedora-43-updates` **drifts** and is what gets
mirrored into blob snapshots — so it is what needs injections.

## The Eviction Pattern (root cause)

1. A build pulled NVR `X` from `fedora-43-updates`.
2. Fedora bumped to a newer major/minor `Y`; `X` demoted from `updates` repodata.
3. `X` never entered the frozen `releases/43/Everything`.
4. `X` is still recoverable from **kojipkgs** (Fedora's build archive).

The spec's `BuildRequires` upper bound (`>= X < next~`) can't accept `Y` →
inject `X` back from kojipkgs.

## Procedure

### 1. Scan the triage summary for resolution signatures
```python
import json, re
d = json.load(open('triage-summary-*.json'))
pat = re.compile(r'nothing provides|No match for argument|Could NOT find|missing:', re.I)
for b in d['buckets']:
    for t in b['tasks']:
        if pat.search(t['shortSummary']):
            print(b['name'], t['taskID'], t['package'])
```
Check **all** buckets — gaps hide outside the obvious one.

### 2. Get EXACT pins from koji root.log (never trust summary ranges)
```bash
curl -sk "https://<koji-host>/koji/getfile?taskID=<childID>&name=root.log&offset=0" \
  | grep -iE "nothing provides|No match for argument|conflicting requests"
```
`crate(icu_collections) >= 2.1.1 < 2.2.0~` proves the mirror has the name at
2.2.0 but not the needed version (the eviction signature).

### 3. Classify (not everything is injectable)
| Signature | Class | Action |
|---|---|---|
| `nothing provides ... < X~` / `No match for argument: crate = X` | Real mirror gap | Inject `X` from kojipkgs |
| `Curl error (28): Timeout` from the blob mirror | Transient infra | Retest, don't inject |
| `Could NOT find <LIB>` at `%build`, lib IS in mirror | Spec bug | Fix the azurelinux spec (`BuildRequires`) |
| Needs version requiring a whole-stack realignment | Version skew | Upstream owner fix |

0623 exclusions: **grpc** (`libpfm-devel` current, just add
`BuildRequires: libpfm-devel`), **qt6-qthttpserver** (`qt6-qtbase-private-devel
= 6.10.2` vs mirror qtbase 6.9.2 → qt6 stack realignment).

### 4. Find the NVR + full subpackage fan-out on kojipkgs
Rust: SRPM is `rust-<crate>`; binaries are `rust-<crate>-devel`,
`rust-<crate>+<feature>-devel` — all **noarch**, one shared NVR. Inject
**every** subpackage of the NVR.
```bash
# versions
curl -s "https://kojipkgs.fedoraproject.org/packages/<name>/" | grep -oE '>[0-9][^<]*/<' | sed -E 's/>//;s/\/<//' | sort -V
# releases for a version
curl -s "https://kojipkgs.fedoraproject.org/packages/<name>/<ver>/" | grep -oE '>[0-9][^<]*\.fc[0-9]+/<' | sed -E 's/>//;s/\/<//'
# noarch subpackages for the NVR
curl -s "https://kojipkgs.fedoraproject.org/packages/<name>/<ver>/<rel>/noarch/" | grep -oE 'href="[^"]+\.noarch\.rpm"' | sed -E 's/href="//;s/"//' | sort
```

### 5. Verify the transitive closure (avoid peeling the onion)
```bash
rpm -qp --requires <rpm> | grep -E 'crate\(' | grep '<'   # upper-bounded deps
rpm -qp --provides <rpm> | grep -E '^crate\('
```
Confirm each `< X~` dep is satisfied by the injected set or current mirror
(e.g. siblings bounded `< 3.0.0~` are fine against a 2.2.0 mirror; only
`< 2.2.0~` pins need injecting). Iterate to a fixpoint. For masked gaps
(downstream packages that never reached builddep), run a full-set offline
depsolve against `mirror + injections` before rerunning. Note Rust
`%generate_buildrequires` produces BRs at build time — a static depsolve
misses them.

### 6. Add entries to the injections file
File: `azl-infra/scripts/fedora_mirror/injections/azl4-stage1-injections.yaml`
```yaml
- {source: rust-icu_collections, name: rust-icu_collections-devel, version: 2.1.1, release: 5.fc43, arch: noarch}
```
- `source` = SRPM, `name` = binary RPM (set `source` whenever they differ —
  always for rust crates; binaries live under the SRPM dir on kojipkgs).
- `noarch` fans out to x86_64 + aarch64; arch-specific binaries get one entry per arch.
- File is sorted by `(source, name, arch)`, `+feature-devel` before bare
  `-devel`. Insert in place; **do not append**. Keep entries **comment-free**
  (rationale goes in the PR/commit).

### 7. Pre-flight validation (offline, no Azure)
No standalone `--dry-run`; reuse the script's own functions:
```python
import yaml, inject_packages as ip, logging
logging.disable(logging.CRITICAL)
inj = yaml.safe_load(open('injections/azl4-stage1-injections.yaml'))
repos = yaml.safe_load(open('repos.yaml'))
new = [p for p in ip.expand_packages(inj, repos) if p['source_name'] in {'rust-...'}]
print('HEAD failures:', sum(0 if ip.head_check(p['url'])[0] else 1 for p in new))  # want 0
```

### 8. Know how the run behaves
`inject_packages.py` is **add-only + idempotent** (dedup by dest path,
SKIPs existing). **No delete path.** Storage: account `kojifedoramirrorsa`,
container `fedora-mirror`; blob path
`snapshots/<snap>/<repo>/<arch>/Packages/<first-letter>/<file>.rpm`.
**Snapshot caveat:** the injection only helps if it lands in the snapshot the
target consumes — confirm the file's `snapshot:` matches before running.

### 9. Open the PR
Commit the injection entries on a branch off `azl-infra` `main` and open the
PR — this is the deliverable.
- **Branch:** `<user>/<task>-<date>` off latest `origin/main`.
- **Diff:** additions-only to `azl4-stage1-injections.yaml` (no existing lines
  touched), entries comment-free and in the correct alphabetical slot.
- **PR description** carries the rationale: the eviction pattern, exact NVRs,
  which failing package(s) each entry unblocks, closure notes, the target
  `snapshot:`, and any packages deliberately **excluded** (spec bugs / version
  skew) with why.
- **Evidence:** paste the Step 7 offline HEAD-check result (want 0 failures).
- Open as **draft** first if you want review before it's merge-ready.

> **After merge (optional):** once the injection lands in the prod snapshot,
> retest the affected packages (include the transient-timeout ones; exclude
> spec/version-skew) with a body like:
> ```json
> {
>   "repoUri": "https://github.com/microsoft/azurelinux.git",
>   "branch": "4.0",
>   "commitSha": "",
>   "packageTarget": "azl4-bootstrap-mirror",
>   "packages": ["rust-icu_normalizer", "rust-rkyv", "..."],
>   "isScratchBuild": true
> }
> ```

## Transient timeout vs. real gap

A burst of `Curl error (28): Timeout` is usually a time-windowed blob outage,
not a bad package. Confirm: (1) same RPM failing across many packages →
systemic; (2) failures pack into a short window (0623: 29 in ~78 min) →
transient; (3) most other builds in that window succeeded (0623: 97%) →
mirror was up. If all three hold, **retest** — do not inject.

## Gotcha — version float (pin the spec, don't delete)

When old + new both exist (old in frozen base, new in updates/mirror), dnf
picks the highest and an old-API spec fails (e.g. `rust-uucore` 0.0.27 vs
0.7.0). Deleting from the mirror is the wrong lever (sync re-adds it, no
delete tooling, diverges from upstream). **Fix:** pin the spec's
`crate(uucore) = 0.0.27` (+ lockstep siblings `uucore_procs`,
`uuhelp_parser`). Since 0.0.27 lives in the frozen live base repo, the pin
needs zero mirror changes.

## Reference

- Repo `azl-infra`: `https://dev.azure.com/mariner-org/polar/_git/azl-infra`
- Injections file: `azl-infra/scripts/fedora_mirror/injections/azl4-stage1-injections.yaml`
- Schema/template: `.../injections/example.yaml`
- Tooling: `.../fedora_mirror/{inject_packages,snapshot_repos}.py`, `repos.yaml`, `_common.py`
- kojipkgs archive: `https://kojipkgs.fedoraproject.org/packages/`
- Prod mirror: `https://kojifedoramirrorsa.blob.core.windows.net/fedora-mirror/`
- Worked example: draft PR #27888 in `azl-infra`
