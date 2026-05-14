---
name: skill-modify-source
description: "[Skill] Author `modify_source.sh` scripts that byte-deterministically repack a locally-modified Source0 tarball for use with a `replace-upstream` source override in `comp.toml`. Use when stripping subtrees from an upstream tarball under the same filename so that re-runs and rebuilds across machines produce identical SHA-512 hashes. Triggers: modify_source.sh, replace-upstream, deterministic tarball repack, locally-modified Source0, reproducible build inputs, lookaside hash drift, tarball repack."
---

# Reproducible Source-Tarball Modification (`modify_source.sh`)

## Why this matters

`replace-upstream` source overrides in `*.comp.toml` (see [`comp-toml.instructions.md`](../../instructions/comp-toml.instructions.md#replace-upstream-source-override)) serve a locally-modified tarball from a lookaside URL whose path **embeds the SHA-512 of the served file**:

```
https://azltempstaginglookaside.blob.core.windows.net/repo/pkgs_modified/$pkg/$filename/sha512/$hash/$filename
```

If the repack script is not byte-deterministic, every re-run produces a new hash. The `hash` field in `comp.toml` and the `$hash` segment in `origin.uri` drift apart, the lookaside URL fails to resolve, and `Check Rendered Specs` / build CI break. The whole pattern hinges on reproducibility: **same upstream input → same byte-identical output → same SHA-512**, across machines and across time.

## (a) Anatomy of `modify_source.sh`

- **Lives at** `base/comps/<name>/modify_source.sh`, alongside its `<name>.comp.toml`.
- **Locates the repo root from its own location** using `BASH_SOURCE[0]`, so it can be invoked from any working directory as `bash base/comps/<name>/modify_source.sh` (or just `bash modify_source.sh` from the component directory).
- **Writes all intermediates and the output tarball** under `base/build/work/scratch/<name>/`. Never use `/tmp` or a bare `mktemp -d` (see [`AGENTS.md`](../../../AGENTS.md#conventions)).
- **Caches the verified upstream tarball** in that scratch directory so re-runs skip the download (the determinism self-test relies on the cache being preserved while the modified output is removed).
- **Starts with `set -euo pipefail`** for fail-fast semantics — any unset variable, failed command, or broken pipe aborts immediately.

## (b) The byte-deterministic repack contract

"Deterministic" here means: **same upstream input ⇒ same byte-identical output ⇒ same SHA-512**, across machines and across re-runs. Zero variation from host time, uid/gid, locale, thread scheduling, or filesystem iteration order.

### Required `tar` flags

| Flag | Why |
|------|-----|
| `--sort=name` | Stable entry order regardless of filesystem iteration order |
| `--owner=0 --group=0` | No host uid/gid leakage |
| `--numeric-owner` | Force numeric ids, ignore `/etc/passwd` mapping differences |
| `--mtime='@1577836800'` | Fixed UTC epoch for every entry. Convention: `@1577836800` (2020-01-01 UTC). Any fixed epoch works, but pick one and document it. |
| `--format=gnu` | Deterministic long-path handling; pax format adds variable-length headers |

Always export `LC_ALL=C` before invoking `tar` so `--sort=name` uses locale-independent collation.

### Required `xz` flags

| Flag | Why |
|------|-----|
| `-T 1` | **Single-threaded only.** Multi-threaded xz splits the stream into non-reproducible blocks unless `--block-size` is also pinned. For tarballs of typical source-package size the throughput gain is marginal — not worth the determinism risk. |
| `-9` | Pin the compression level so re-runs produce identical compressed bytes (default level may vary across xz versions). |

### Forbidden

- `tar --gzip` / `tar -cz` — gzip embeds the mtime in its header unless you also pass `-n` to gzip explicitly; cleaner to drive `xz` ourselves through a pipe.
- `xz -T 0` or `xz -T <n>` without a pinned `--block-size`.
- `mktemp` (or any `$$`, `$RANDOM`, or `date`-derived filename) for the **output** tarball or any intermediate that ends up inside it. The whole scratch dir is ephemeral; the output filename must be fixed.
- `find ... -newer ...` for selection — host clock leaks into what gets packed.
- Any direct call to `gzip` without `-n`.

## (c) Verify the upstream tarball before extracting

Always SHA-512-check the upstream tarball before extracting and re-packing:

```bash
echo "${UPSTREAM_SHA512}  ${UPSTREAM_PATH}" | sha512sum --check --status \
  || { echo "ERROR: upstream SHA-512 mismatch — upstream may have re-tagged" >&2; exit 1; }
```

Upstream re-tagging (publishing different bytes under the same version) is rare but real. The script must fail loudly rather than silently re-pack different content under the same filename.

## (d) Strip-list vs keep-list — pick the one that audits better

Both strategies are equally valid. Use the one whose list is shorter and easier to review.

### Strip-list (deletion-based)

Extract the full tarball, then `rm -rf` the offending subtrees. Best when the bad content is a small fraction of the tarball.

```bash
STRIP_PATHS=(
  docs
  tests/network
  third_party/vendored-bigblob
)

for p in "${STRIP_PATHS[@]}"; do
  rm -rf -- "${EXTRACT_DIR}/${p}"
done
```

### Keep-list (allowlist-based)

Extract everything, then delete everything except an explicit list of paths to keep. Best when the bad content is most of the tarball, or when the keep-list is easier to audit. Canonical example: a vendored JS engine that lives inside a much larger browser monorepo, where keeping only `js/src/` plus a handful of build-tooling paths is dramatically easier to review than enumerating everything to strip.

```bash
KEEP_PATHS=(
  js/src
  build
  config
  python
  taskcluster
)

# Move keep paths into a staging dir, wipe the rest, move them back.
mkdir -p "${EXTRACT_DIR}.keep"
for p in "${KEEP_PATHS[@]}"; do
  src="${EXTRACT_DIR}/${p}"
  [[ -e "${src}" ]] || { echo "ERROR: keep-path missing: ${p}" >&2; exit 1; }
  mkdir -p "$(dirname "${EXTRACT_DIR}.keep/${p}")"
  mv "${src}" "${EXTRACT_DIR}.keep/${p}"
done
rm -rf "${EXTRACT_DIR}"
mv "${EXTRACT_DIR}.keep" "${EXTRACT_DIR}"
```

### List discipline (both strategies)

- Lists live in the script as **data**, not as code: a bash array (one item per line, trailing comma optional) or a here-doc that's read into an array. Keep the list dense and auditable.
- **No inline commentary** mid-list. If a single entry needs context, put a one-line comment immediately above it, not on the same line.
- Sort the list. Sorted lists are easier to diff and to review.
- Validate that each keep-path actually exists in the extracted tree. If a keep-path is missing, abort — upstream restructured and the list is stale.

## (e) Output and reporting

On success the script prints, in order:

1. The absolute path to the modified tarball under `base/build/work/scratch/<name>/`.
2. The SHA-512 of that file.
3. A ready-to-paste `az storage blob upload` command targeting the lookaside path `pkgs_modified/$pkg/$filename/sha512/$hash/$filename`.
4. A short reminder that **both** the `hash` field **and** the `$hash` segment of `origin.uri` in `<name>.comp.toml` must be updated to the new SHA-512.

Example tail of `modify_source.sh`:

```bash
out_hash=$(sha512sum "${OUTPUT_TARBALL}" | awk '{print $1}')

cat <<EOF
Modified tarball : ${OUTPUT_TARBALL}
SHA-512          : ${out_hash}

Upload command:
  az storage blob upload \\
    --account-name azltempstaginglookaside \\
    --container-name repo \\
    --name "pkgs_modified/${PKG}/${OUTPUT_FILENAME}/sha512/${out_hash}/${OUTPUT_FILENAME}" \\
    --file "${OUTPUT_TARBALL}"

Remember to update BOTH 'hash' AND the '\$hash' segment of 'origin.uri'
in base/comps/${PKG}/${PKG}.comp.toml to:
  ${out_hash}
EOF
```

## (f) Determinism self-test

Before merging, verify locally that the script is reproducible:

```bash
bash base/comps/<name>/modify_source.sh
sha512sum base/build/work/scratch/<name>/<filename>

# Remove the OUTPUT only — keep the upstream cache so the second run
# exercises the same extract+repack path.
rm base/build/work/scratch/<name>/<filename>

bash base/comps/<name>/modify_source.sh
sha512sum base/build/work/scratch/<name>/<filename>   # MUST match the first sum
```

If the two hashes don't match, the script has a determinism bug — diagnose and fix before merging. Common culprits:

- Multi-threaded `xz` without a pinned block size.
- A `tar` flag missing from the required set in (b).
- `LC_ALL=C` not exported in the shell that invokes `tar`.
- A leftover `mktemp`, `$RANDOM`, `$$`, or `$(date ...)` somewhere in the pipeline.
- Host-time leak via `find -newer`, `touch`, or implicit mtime preservation during the strip step.

## (g) Anti-patterns

- ❌ `mktemp` for the output filename. The output filename is fixed; only the scratch dir is ephemeral.
- ❌ `$$` or `$RANDOM` anywhere in an intermediate path that ends up inside the tarball.
- ❌ `$(date ...)` in any filename or as a tar `--mtime` value.
- ❌ `gzip` without `-n`, or `tar --gzip` / `tar -cz`. Use `xz` driven through a pipe.
- ❌ `xz -T 0` (or any `-T N` > 1) without `--block-size` pinned.
- ❌ `find ... -newer ...` to select what to pack — host clock leaks in.
- ❌ Tar without `--sort=name`, `--owner=0 --group=0 --numeric-owner`, `--mtime`, or `--format=gnu`.
- ❌ Forgetting `LC_ALL=C` — sort collation becomes locale-dependent and the same input produces different orderings on different hosts.

## (h) Canonical skeleton

The full pattern, end-to-end, using the strip-list strategy. The keep-list variant swaps only the strip section (see (d)); everything else is identical.

```bash
#!/usr/bin/env bash
# Repack upstream Source0 with local modifications under the same filename.
# Produces a byte-deterministic tarball; SHA-512 is stable across machines and re-runs.
set -euo pipefail

# Resolve repo root from the script's own location: base/comps/<name>/modify_source.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

PKG="examplepkg"
UPSTREAM_FILENAME="examplepkg-1.2.3.tar.xz"
UPSTREAM_URL="https://upstream.example.org/${UPSTREAM_FILENAME}"
UPSTREAM_SHA512="<paste-upstream-sha512-here>"

OUTPUT_FILENAME="${UPSTREAM_FILENAME}"  # same name as upstream; replace-upstream swaps in place
SCRATCH_DIR="${REPO_ROOT}/base/build/work/scratch/${PKG}"
UPSTREAM_PATH="${SCRATCH_DIR}/${UPSTREAM_FILENAME}"
EXTRACT_DIR="${SCRATCH_DIR}/extract"
OUTPUT_TARBALL="${SCRATCH_DIR}/${OUTPUT_FILENAME}"

STRIP_PATHS=(
  docs
  tests
  third_party/vendored-bigblob
)

mkdir -p "${SCRATCH_DIR}"

# 1. Fetch (cache across runs) and verify upstream.
[[ -f "${UPSTREAM_PATH}" ]] || curl -fSL -o "${UPSTREAM_PATH}" "${UPSTREAM_URL}"
echo "${UPSTREAM_SHA512}  ${UPSTREAM_PATH}" | sha512sum --check --status \
  || { echo "ERROR: upstream SHA-512 mismatch — upstream may have re-tagged" >&2; exit 1; }

# 2. Extract fresh.
rm -rf "${EXTRACT_DIR}"
mkdir -p "${EXTRACT_DIR}"
tar -xf "${UPSTREAM_PATH}" -C "${EXTRACT_DIR}"

# 3. Strip.
for p in "${STRIP_PATHS[@]}"; do
  rm -rf -- "${EXTRACT_DIR:?}/${p}"
done

# 4. Repack deterministically.
rm -f "${OUTPUT_TARBALL}"
( cd "${EXTRACT_DIR}" && LC_ALL=C tar \
    --sort=name \
    --owner=0 --group=0 --numeric-owner \
    --mtime='@1577836800' \
    --format=gnu \
    -cf - . \
  | xz -T 1 -9 ) > "${OUTPUT_TARBALL}"

# 5. Report.
out_hash=$(sha512sum "${OUTPUT_TARBALL}" | awk '{print $1}')
cat <<EOF
Modified tarball : ${OUTPUT_TARBALL}
SHA-512          : ${out_hash}

Upload command:
  az storage blob upload \\
    --account-name azltempstaginglookaside \\
    --container-name repo \\
    --name "pkgs_modified/${PKG}/${OUTPUT_FILENAME}/sha512/${out_hash}/${OUTPUT_FILENAME}" \\
    --file "${OUTPUT_TARBALL}"

Remember to update BOTH 'hash' AND the '\$hash' segment of 'origin.uri'
in base/comps/${PKG}/${PKG}.comp.toml to:
  ${out_hash}
EOF
```

## Related

- [`comp-toml.instructions.md` — `replace-upstream` source override](../../instructions/comp-toml.instructions.md#replace-upstream-source-override) — how the modified tarball is plumbed into the component definition.
- [`skill-fix-overlay`](../skill-fix-overlay/SKILL.md) — when an overlay would have been enough and a tarball repack is overkill.
- [`skill-update-component`](../skill-update-component/SKILL.md) — finalizing the comp.toml change (`update` → commit → `render` → amend) once the new hash is uploaded.
