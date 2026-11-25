---
applyTo: "**/*.patch"
---

# Review newly added patches

- Check only `.patch` files newly added by the change, including at the repository
  root. Skip files under the top-level `specs/` directory at any depth: they are
  generated output. Do not flag pre-existing patches under this rule.
- Require a Git email-format patch, as produced by `git format-patch`, not a raw
  `git diff`. Check for the opening `From <commit-id>` line, a `From:` header
  with the original author's name and email address, a `Date:` header with the
  original author date and time zone, a descriptive `Subject:`, and a Git diff.
  The commit message body should explain what the patch changes and why.
- For an upstream patch or backport, require a traceable source, such as a link
  to the original upstream commit or review. Preserve the original author and
  date, and document any downstream adaptations. For a locally authored patch,
  identify it as downstream-only if it has no upstream source. Do not invent
  missing provenance.
- In a PR review, report missing or malformed metadata in an inline comment on
  the added patch. Name what is missing and, for raw diffs, recommend exporting
  the source commit with `git format-patch -1 <commit>`.
