---
name: azldev-worktree-cleanup
description: "Read before removing an Azure Linux worktree, cleaning mock roots or caches, reclaiming build disk space, or investigating orphaned mock environments. Inventory worktree-associated resources, preserve diagnostics, obtain approval, and use targeted mock cleanup before worktree removal."
---

# Retire worktrees and their mock environments

Worktree removal does not remove mock roots or caches. Treat cleanup as
explicit, best-effort housekeeping, not automatic garbage collection.
Inventory first; obtain approval for the exact resources before deleting.
Do not run cleanup merely because this skill was loaded.

## While the worktree still exists

1. Identify the exact worktree with `git worktree list --porcelain` and check
   its `git status --short`. Confirm that commits are pushed, merged, or
   intentionally preserved elsewhere before proposing worktree removal.
   Do not discard uncommitted files, untracked outputs, or diagnostics.
2. Inspect its distro configuration and build logs to identify mock
   selections and overrides actually used. Account for prod (`4.0`), preview
   (`4.0-preview`), and each architecture: four current selections in
   `distro/mock/azl4/`. Check custom `basedir`, `rootdir`,
   root/cache overrides, unique extensions, and separately placed helper
   environments. Read the `azldev` skill before running azldev commands.
3. Resolve current selections with mock, not a caller-owned implementation
   of the naming algorithm. For example, with an absolute selected config:

   ```bash
   cfg=/absolute/worktree/distro/mock/azl4/azurelinux-4.0-preview-x86_64.cfg
   mock -r "$cfg" --configdir "$(dirname "$cfg")" \
     --disable-plugin=yum_cache --print-root-path
   ```

   Supply the same effective overrides as the original operation. The
   canonical directory containing the selected `.cfg` must match
   `--configdir`. Each architecture config applies `config-directory-root.tpl`
   after its channel templates. Preserve the complete configuration directory;
   moving a lone `.cfg` to a scratch directory loses required includes and
   does not resolve the original identity. Prod and preview share a directory
   label/digest but have distinct channel-specific roots and caches.
   Mock initializes plugins even for path/configuration queries. For the
   default Azure Linux plugin set, disabling `yum_cache` during discovery
   avoids creating empty caches and lock files. Use the same discovery-only
   option with `--debug-config` if unexpanded settings need inspection;
   avoid `--debug-config-expanded`. Custom plugins may have other side
   effects and need separate inspection. Do not carry the plugin-disable
   option into builds or cleanup commands.
4. Inventory the associated live root, bootstrap root, and cache directories.
   For the default layout, caches are under `/var/cache/mock/<root-name>`
   and `/var/cache/mock/<root-name>-bootstrap`; root placement is under
   `/var/lib/mock`. Confirm effective settings instead of assuming these
   paths for custom configurations. Separately placed helpers may still
   share caches. Include disk usage, missing resources, and uncertainties
   in the inventory.
5. Check logs and directory listings for previous naming schemes or paths.
   In particular, old stage1/stage2/stage2-prod environments are not selected
   by the current prod/preview configurations; retain their original
   configuration evidence for separately approved cleanup.
   Current configuration discovery does not identify roots left by older
   templates, a moved directory, or an earlier checkout at the same path.
   Readable labels are hints, not evidence that all matching resources
   belong to this worktree.
6. Confirm with the user that operations using the identity are stopped and
   no new build, render, query, or shell operation will start during cleanup.
   Check for active users as supporting evidence, not proof that a race
   cannot occur. Mock's locks do not cover the whole root/cache deletion
   transaction; if exclusive use cannot be established, defer cleanup.
7. Present exact resource paths, approximate disk savings, retained
   diagnostics/outputs, and targeted commands for approval. Ask whether
   failed environments must be preserved. Distinguish approval for mock
   cleanup from approval to remove the worktree.
8. After approval, use mock's supported cleanup with the still-loadable
   configuration and the matching overrides. For one default-layout
   stage/architecture selection:

   ```bash
   mock -r "$cfg" --configdir "$(dirname "$cfg")" --scrub all
   ```

   This is destructive: it removes the selected live root, bootstrap root,
   and their caches. It does not retire every channel/architecture at once.
   Do not use it if any targeted cache is shared with an identity that
   must remain. Cover approved helper placements separately.
9. Verify each inventoried resource is gone, or explicitly retained. Report
   failures and remaining paths; a successful command alone is not proof of
   complete reclamation. If cleanup is incomplete, keep the configuration
   available and stop before worktree removal unless the user explicitly
   approves deferral with a recovery plan. Remove the worktree only after
   its separate approval and preservation checks.

Ordinary successful-build cleanup uses `--scrub chroot` with azldev's
default preserve policy. It intentionally leaves bootstrap roots and caches;
it is not complete retirement. Do not change every build to `--scrub all`.

## If the worktree is already gone

There is no authoritative mock environment registry. `mock --list-chroots`
lists available configuration files, not instantiated environments. For
read-only discovery of default locations:

```bash
find /var/lib/mock /var/cache/mock \
  -mindepth 1 -maxdepth 1 -type d -printf '%p\n' | sort
```

Inspect both locations: a live root may be absent while bootstrap roots or
caches remain. Custom placement/cache overrides require separate discovery.
Report permission failures or inaccessible locations as incomplete inventory.

Use readable path labels to nominate candidates. Corroborate ownership with
surviving configurations, build logs, worktree records, or other explicit
evidence; absence of the apparent owner path is not sufficient. Labels are
sanitized and may be truncated, distinct paths can have the same label, and
path reuse can associate a name with a different checkout.

Report candidate paths, disk usage, ownership evidence, and uncertainties.
Do not delete ambiguous resources. A shared/external configuration may have
other callers even if the worktree that first used it is gone.

Recovery through a different loadable configuration plus a recorded root
override is a candidate approach, **not an end-to-end validated orphan
cleanup recipe**. It must reproduce placement, bootstrap, and cache settings
without loading includes from the deleted directory. Do not prescribe it as
routine cleanup until a disposable-environment test demonstrates complete
removal and leaves unrelated resources untouched. Escalate for a separately
reviewed recovery plan instead.

## Guardrails

- Never use wildcard/prefix deletion, broad recursive removal, or
  `mock --scrub-all-chroots` for this workflow. The latter guesses associations
  with installed configuration names and is not reliable for checkout-local
  roots.
- A readable-name match, an old timestamp, or an apparently idle lock is not
  authorization to delete. Do not infer ownership by recomputing a digest.
- Removing a caller of external/shared configuration does not authorize
  retiring that configuration's environments or caches.
- Preserve requested failed environments, caller `--resultdir` outputs,
  `chroot_scan` artifacts, and any diagnostics needed for inspection.
- Keep cleanup records or logs outside a worktree scheduled for removal
  when they are needed for deferred recovery. Do not claim a durable
  inventory exists unless one was actually saved.
