---
name: skill-annotate-overlays
description: "[Skill] Suggest a metadata `category` and annotate overlays in the Azure Linux repo — either new overlays you are adding or a specific set of existing overlays a user points you at. Uses an LLM to classify the change, hunt for the originating upstream commit(s) and bug(s), and judge upstream status, then writes the metadata per the overlay-metadata instructions. Triggers: annotate overlay, add overlay metadata, classify overlay, pick overlay category, suggest category, upstream-status, overlay commits/bugs."
---

# Suggest Category & Annotate Overlays

This skill helps you attach `metadata` (at minimum a `category`) to overlays in
the Azure Linux repo. It is **targeted**, not a bulk sweep — use it for:

- **New overlays** you (or the user) are adding to a component, or
- **A specific set of existing overlays** the user points you at (one component,
  one overlay file, or a named list).

It is **not** for mass-annotating or migrating every overlay in the tree.

For each overlay in scope the skill:

1. Reads the overlay's actual change and **suggests a `category`** (with reasoning).
2. **Hunts for the originating upstream commit(s) and bug(s)** so `commits` /
   `bugs` are grounded in real provenance, not guesses.
3. **Judges `upstream-status`** (`upstreamed` / `upstreamable` /
   `needs-upstream-hook` / `inapplicable` / `unknown`).
4. **Writes the metadata** following
   [`overlay-metadata.instructions.md`](../../instructions/overlay-metadata.instructions.md)
   — that file is the source of truth for the category set, the field semantics,
   the per-file vs. inline TOML forms, and file layout/naming. Re-read it at the
   start of every run; the guidance below only adds the *classification workflow*.

Annotation is **pure documentation** — it must not change the rendered spec. The
overlay's behavior, order, and count stay identical; only `metadata` is added or
edited.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Scope | **Yes** | The overlay(s) to annotate: a component name, an overlay file, or an explicit list. For new overlays, the ones you just wrote. |
| User-supplied provenance | No | Any commit/PR/bug URLs the user already knows. Prefer these over rediscovery. |

If the scope is ambiguous (e.g. "annotate the qemu overlays" when only some are
new), ask the user which overlays they mean before editing.

## Step 1 — Read each overlay's change

For every overlay in scope, understand *what it actually does* before classifying:

```bash
# Read the defining file(s)
find base/comps/<name>/ -type f \( -name '*.comp.toml' -o -name '*.overlay.toml' \) | sort
```

Note the overlay `type`, target `section`/`package`, the `description`, any
top-of-file comments, and — for `patch-add` — the patch header and body. These are
your primary classification signals.

## Step 2 — Suggest a category (LLM classification)

Map the change to exactly one `category` from the closed set in
[`overlay-metadata.instructions.md`](../../instructions/overlay-metadata.instructions.md#step-1--pick-the-category).
Do **not** restate the table here — read it there. Apply its disambiguation tips
(backport vs. compat/pruning, pruning vs. temp-workaround, flaky vs. unsupported
tests, compatibility vs. platform-adaptation).

Classification heuristics from the overlay itself:

- `spec-remove-*`, `patch-remove`, `file-remove`, dropping a `BuildRequires`/
  subpackage we don't ship → usually `azl-pruning`.
- `spec-remove-tag` on a dep that *should* exist but isn't imported yet →
  `azl-temp-workaround`.
- A `patch-add` whose header matches a real upstream/dist-git commit, or a spec
  edit that mirrors a dist-git change → `upstream-backport` (**requires**
  `commits`).
- Skipping tests → `azl-disable-flaky-tests` (intermittent) vs.
  `azl-disable-unsupported-tests` (can't run in mock: network/root/hardware).
  Grep the overlay's `description`, surrounding comp.toml comments, and the
  component's git history for the word **`flaky`** — if it appears, the intent is
  intermittent failure, so classify as `azl-disable-flaky-tests`:

  ```bash
  # Comments / descriptions in the component config
  grep -niE 'flaky|flake|intermittent|racy|race' base/comps/<name>/*.toml base/comps/<name>/**/*.toml
  # Commit messages touching the component (same keyword set)
  git log -i -E --grep='flaky|flake|intermittent|racy|race' --oneline -- base/comps/<name>/
  ```

  For a component defined inside a **component-group** file (its overlays live in
  a shared `base/comps/component-*.toml` under
  `[component-groups.<group>.overlays]` rather than a dedicated comp dir), the
  history above won't isolate it. `git blame` the specific line(s) that define the
  component / its overlay and inspect the originating commit message for the same
  keywords:

  ```bash
  # Find the line range for the component/overlay, then blame it
  grep -n '<name>' base/comps/component-<group>.toml
  git blame -L <start>,<end> base/comps/component-<group>.toml
  # Inspect the commit(s) the blame points at
  git show -s --format='%h %s%n%b' <blame-sha> | grep -iE 'flaky|flake|intermittent|racy|race'
  ```

  If any of these turns up the keywords, classify as `azl-disable-flaky-tests`;
  otherwise treat the skipped test as `azl-disable-unsupported-tests`.
- Fedora→AZL name/path or RHEL-alignment edits → `azl-branding-policy`.
- Toolchain/mock/build-env fixes with no upstream equivalent → `azl-compatibility`.
- `%ifarch`-style arch-specific tweaks → `azl-platform-adaptation`.
- FIPS / crypto-policy → `azl-security-compliance`.
- Release-tag / changelog mechanics → `azl-release-management`.

State your suggested category **and a one-line rationale** for each overlay so the
user can sanity-check. When two categories are plausible, say so and pick the
higher one in the instructions' priority order (first match wins).

## Step 3 — Hunt for commits & bugs (provenance)

Grounded `commits` are the most valuable field for `upstream-backport` (and are
**required** there), and useful for any category that traces to a specific fix.
Prefer provenance the user supplied; otherwise actively look for it. **A commit
URL you discovered and verified is not "inventing" metadata; an unverified guess
is.** Never fabricate a `bugs` entry.

Search in this order, stopping at the first that yields a **verifiable** commit:

1. **The overlay's own comments / `description`** — reuse any `# Backport from …/c/<sha>`, `(upstream <sha>)`, PR, or bug link already present.
2. **`patch-add` patch headers** — `git format-patch` output starts with
   `From <40-hex-sha> …`; that SHA is the upstream commit. Also scan the body for
   `Ref:`, `Closes:`, `Resolves:`, `(cherry picked from commit <sha>)`, or
   `owner/repo#<n>` / PR / issue URLs.

   ```bash
   sed -n '1,40p' base/comps/<name>/<patch>.patch
   grep -nE '^From [0-9a-f]{7,40}|cherry picked from|Ref:|Closes:|Resolves:|#[0-9]+|/(pull|commit|issues)/' \
     base/comps/<name>/<patch>.patch
   ```
3. **Fedora dist-git / upstream `git log`** — for spec edits that mirror an
   upstream change, find the commit in
   `https://src.fedoraproject.org/rpms/<name>` or the project's repo.

Always confirm a candidate SHA exists upstream before recording it, and resolve
PR/issue references to the concrete commit:

```bash
gh api repos/<owner>/<repo>/commits/<sha> -q '.html_url'
gh api repos/<owner>/<repo>/pulls/<n>/commits -q '.[].sha'
gh api repos/<owner>/<repo>/pulls/<n> -q '.merge_commit_sha'
gh api repos/<owner>/<repo>/issues/<n>/timeline \
  -q '.[] | select(.event=="cross-referenced" or .event=="closed")'
```

Record canonical URLs in `commits` (upstream-project repo for project patches,
Fedora dist-git for dist-git backports) as `{ url = "…" }` tables. List all commits
of one logical change: `commits = [{ url = url1 }, { url = url2 }, …]`. Add
`bugs = [{ url = "…" }]` for any tracker entry the overlay or a resolved reference
points to. If no commit can be found **and** verified for an `upstream-backport`
overlay, note the gap in your summary and flag it for the user rather than guessing.

## Step 4 — Judge `upstream-status`

Pick exactly one value per the instructions ([Step 2](../../instructions/overlay-metadata.instructions.md#step-2--set-upstream-status-required-when-metadata-is-present)).
It is **required** whenever `[metadata]` is present:

- `upstreamed` — already in Fedora; carried only until AZL
  bumps past it.
- `upstreamable` — the patch we carry is itself upstream-shaped or already in the OSS project but not in Fedora yet; the same diff could be sent upstream and plausibly accepted (most backports, portable fixes).
- `needs-upstream-hook` — AZL-specific change that upstream wouldn't take as-is,
  but upstream could add a `bcond`/`%if`/config knob so we could drop the overlay.
- `inapplicable` — permanent AZL-only deviation with no upstream story (branding,
  deliberate pruning, enterprise policy).
- `unknown` — genuinely not yet assessed. Prefer a definite value; reviewers push
  back on `unknown`.

On an `upstream-backport` overlay only `upstreamed` and `upstreamable` are valid —
any other value is a validation error.

## Step 5 — Write the metadata

Apply the metadata using the exact TOML forms and layout/naming rules in
[`overlay-metadata.instructions.md` → Step 4](../../instructions/overlay-metadata.instructions.md#step-4--write-the-metadata-toml-forms):

- **Prefer the per-file `.overlay.toml` layout** for new work — even single-overlay
  changes — with one top-level `[metadata]` block per logical change.
- Overlays that share the same intent are **one logical change** → one
  `.overlay.toml` file with one `[metadata]`. Don't stamp identical inline metadata
  on several overlays.
- Inside a `.overlay.toml`, per-overlay `metadata` is **rejected** — the file-level
  block is the single source of truth.
- Use inline `metadata` only when the component is already inline and you're not
  restructuring it (single-line form for one or two scalar fields; sub-table form
  when you need `commits`/`bugs` or more fields).

### Preserve apply order when moving overlays into files

Overlay apply order is **significant** — later overlays operate on the spec text
produced by earlier ones, so reordering can silently change (or break) the render.
When you migrate inline overlays into `.overlay.toml` files you **must** reproduce
the exact original sequence:

- **Files apply in filename (lexicographic) order**, and globs concatenate in
  declaration order. Prefix every file with a zero-padded ordinal (`0001-`,
  `0002-`, …) so the file order matches the original inline order top-to-bottom.
- **Within a file, `[[overlays]]` apply in declaration order.** Keep overlays in
  the same relative order they had inline; don't sort or regroup them in a way
  that moves an overlay across another it depended on.
- **Split on real boundaries only.** A group of inline overlays may become one
  file only if they were contiguous in the original array (or their reordering is
  provably irrelevant). If two logical groups were interleaved inline, either keep
  that interleaving via ordinals or confirm with the Step 6 diff that pulling them
  apart is a no-op.
- **Move *all* of a component's overlays into files.** Overlays loaded via
  `overlay-files` are **appended after** any inline overlays left on the
  component, so a partial migration silently moves the file-loaded overlays to the
  end of the sequence. Leave no inline `[[overlays]]` behind (or preserve the
  exact global order via ordinals across both).

The Step 6 diff is the enforcement mechanism: if the order changed, the rendered
spec (or `diff-sources` output) will differ.

Preserve any explanatory top-of-file comments and the existing `description` text
verbatim; if a `description` is missing, leave it absent unless the user asks you
to write one.

## Step 6 — Validate (mandatory)

Annotation **and** the file migration must be a no-op on the applied overlays. The
rendered spec, the overlay set, and — critically — the overlay **apply order** must
be identical before and after.

```bash
# Baseline before editing
azldev comp render -p <name>
cp specs/<first-char>/<name>/<name>.spec ./base/build/work/scratch/overlay-annotate-<name>-before.spec

# … make the metadata edits …

# After editing — expect NO diff
azldev comp render -p <name>
diff -u ./base/build/work/scratch/overlay-annotate-<name>-before.spec specs/<first-char>/<name>/<name>.spec
```

**Order check without a full render.** If `render` is unavailable (e.g. the mock
build root is locked in a shared environment), use `diff-sources`, which applies
the overlays in order and shows the resulting patch. Capture it before and after
the migration and confirm they are byte-identical — this directly proves the apply
order was preserved:

```bash
azldev component diff-sources -p <name> -q > ./base/build/work/scratch/<name>-diff-before.txt   # before edits
# … move overlays into files / add metadata …
azldev component diff-sources -p <name> -q > ./base/build/work/scratch/<name>-diff-after.txt    # after edits
diff -u ./base/build/work/scratch/<name>-diff-before.txt ./base/build/work/scratch/<name>-diff-after.txt \
  && echo "IDENTICAL — order and content preserved"
```

Any diff means an overlay changed **or** the apply order shifted (a common symptom
of a partial migration, a mis-ordered file ordinal, or overlays regrouped across a
dependency). Fix the ordinals/grouping until the diff is empty.

- Every in-scope overlay carries the expected `category`.
- `upstream-status` is set to one of the five valid values (never omitted when
  `[metadata]` is present).
- `upstream-backport` overlays carry `commits` and use `upstreamed`/`upstreamable`.
- The overlay **order and count** are unchanged (the before/after diff is empty).

If `render` fails, re-check the per-file rules in the instructions — common
mistakes: per-overlay `metadata` in a `.overlay.toml`; a file-level `[metadata]`
missing `category`; an `overlay-files` glob that matches no files; leftover inline
`[[overlays]]` blocks after moving them into a file (these append **after** the
file overlays and reorder the sequence).

## Step 7 — Finalize for PR

Metadata is excluded from component fingerprints, so annotation alone does not
invalidate locks and needs **no build or smoke-test** (the rendered spec is
identical). Still, run `update` to capture any incidental drift and follow the
standard finalize flow:

```bash
azldev comp update -p <name>
git status base/comps/<name>/ locks/<name>.lock specs/
```

If `update` or `render` touched anything, include it in the same commit, then
re-render and amend so `%changelog` / `Release:` track the commit (see
[`skill-update-component`](../skill-update-component/SKILL.md)).

## Common pitfalls

- **Discover provenance, don't invent it.** `commits` may be added only when you
  **verified** the SHA exists upstream; `bugs`/PR links must come from the overlay,
  a resolved reference, or the user — never a guess.
- **`upstream-status` is required and enumerated.** One of `upstreamed`,
  `upstreamable`, `needs-upstream-hook`, `inapplicable`, `unknown` — never a
  boolean or free-form string.
- **Don't change overlay order, count, or behavior.** This skill only adds
  `metadata` (and optionally regroups overlays into files). The apply order must be
  **identical** before and after — later overlays depend on earlier ones' output,
  so a reorder can change or break the render. Use zero-padded file ordinals
  (`0001-`, …) and declaration order within each file to reproduce the original
  sequence exactly, and prove it with the Step 6 before/after diff.
- **Move all overlays into files, or none.** A partial migration appends the
  file-loaded overlays **after** any remaining inline ones, silently reordering the
  sequence.
- **Don't merge or split the overlays' *behavior*.** Grouping into one
  `.overlay.toml` for annotation is fine; altering what the overlays *do* is not.
- **Ambiguous scope → ask.** Don't guess which overlays the user meant.
