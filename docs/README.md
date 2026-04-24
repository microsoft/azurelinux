# ProtagonistOS Documentation Index

Authoritative technical documentation for ProtagonistOS lives in this repository, on the `sandbox` branch unless otherwise noted.

Google Drive documents are convenience copies, planning notes, review drafts, or human-readable summaries. If GitHub and Google Drive disagree, the GitHub version wins.

## Documentation Rules

- Write technical documentation in Markdown inside this repository first.
- Use Google Drive for readable summaries, planning notes, review copies, and shareable documents.
- Mark all Drive copies as non-authoritative unless they are later promoted back into this repository.
- Keep stale experiments in `docs/archive/` rather than deleting useful history.
- Every document should answer at least one concrete question:
  - What is currently true?
  - What did we decide?
  - How do we reproduce this?
  - What did we test?
  - What failed, and why?

## Current State

Use this section for documents that describe the current technical reality of ProtagonistOS.

- [Azure Linux baseline](current-state/azure-linux-baseline.md)
- [Desktop performance reality](current-state/desktop-performance-reality.md)
- [Packaging and build system](current-state/packaging-and-build-system.md)
- [Installer and ISO path](current-state/installer-and-iso-path.md)

## Decisions

Use this section for Architecture Decision Records and other durable project decisions.

- [ADR-0001: Documentation source of truth](decisions/ADR-0001-documentation-source-of-truth.md)
- [ADR-0002: Base system selection](decisions/ADR-0002-base-system-selection.md)
- [ADR-0003: Desktop environment](decisions/ADR-0003-desktop-environment.md)
- [ADR-0004: Build strategy](decisions/ADR-0004-build-strategy.md)

## Investigations

Use this section for research notes, technical evaluations, unresolved questions, and exploratory reports.

- [Azure Linux desktop gaps](investigations/azure-linux-desktop-gaps.md)
- [KDE on Azure Linux](investigations/kde-on-azure-linux.md)
- [RPM repository strategy](investigations/rpm-repository-strategy.md)

## Reports

Use this section for synthesized project reports and state-of-the-project summaries.

- [ProtagonistOS technical status](reports/protagonistos-technical-status.md)
- [Path to minimal ISO](reports/path-to-minimal-iso.md)

## Archive

Use `docs/archive/` for stale or superseded work that is worth preserving but should not be treated as current guidance.

## Google Drive Synchronization Policy

The repository is the source of truth. Google Drive is a convenience layer.

When a Google Doc is created from a repository document, include this header at the top of the Google Doc:

```text
Status: Convenience copy
Source of truth: GitHub
Repo: jajunk/azurelinux-protagonist
Branch: sandbox
Path: docs/<path-to-source-file>.md
Exported: YYYY-MM-DD

If this document conflicts with the GitHub version, the GitHub version is authoritative.
```

When a Google Doc starts as a draft and becomes technically important, convert it into Markdown and commit it to this repository before treating it as authoritative.

## Recommended Markdown Front Matter

Use this front matter for major technical documents:

```yaml
---
title: Document Title
status: active
source_of_truth: github
branch: sandbox
last_reviewed: YYYY-MM-DD
drive_copy: none
---
```

If a Drive copy exists, replace `drive_copy: none` with the Google Doc URL.
