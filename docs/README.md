# ProtagonistOS Documentation Index

Authoritative technical documentation for ProtagonistOS lives in this repository. The active integration branch is `dev`; stable project state lives on `main`; the `3.0` branch is reserved as a pristine Azure Linux upstream mirror.

Google Drive is a secondary archive/reference layer. GitHub Issues are the active workflow surface. Google Calendar is the time-planning surface. If GitHub and Google Drive disagree, the GitHub version wins.

## Documentation Rules

- Write technical documentation in Markdown inside this repository first.
- Use GitHub Issues for active tasks, blockers, acceptance criteria, and follow-up work.
- Use Google Calendar for focus blocks, build windows, review sessions, and scheduled testing.
- Use Google Drive for archived notes, readable summaries, review copies, and historical context.
- Mark all Drive copies as non-authoritative unless they are later promoted back into this repository.
- Keep stale experiments in `docs/archive/` rather than deleting useful history.
- Follow the branch and upstream synchronization rules in [ADR-0002](decisions/ADR-0002-branching-upstream-sync-and-access-policy.md).
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
- [Environment setup](current-state/environment-setup.md)

## Decisions

Use this section for Architecture Decision Records and other durable project decisions.

- [ADR-0001: Project workflow and source of truth](decisions/ADR-0001-project-workflow-source-of-truth.md)
- [ADR-0002: Branching, upstream sync, contribution, and access policy](decisions/ADR-0002-branching-upstream-sync-and-access-policy.md)

## Investigations

Use this section for research notes, technical evaluations, unresolved questions, and exploratory reports.

- [Azure Linux desktop gaps](investigations/azure-linux-desktop-gaps.md)
- [Personal human-AI workflow surface](investigations/personal-ai-workflow-surface.md)

## Reports

Use this section for synthesized project reports and state-of-the-project summaries.

- [ProtagonistOS technical status](reports/protagonistos-technical-status.md)

## Archive

Use `docs/archive/` for stale or superseded work that is worth preserving but should not be treated as current guidance.

## Google Drive Synchronization Policy

The repository is the source of truth. Google Drive is an archive/reference layer.

When a Google Doc is created from a repository document, include this header at the top of the Google Doc:

```text
Status: Convenience copy
Source of truth: GitHub
Repo: jajunk/azurelinux-protagonist
Branch: dev
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
branch: dev
last_reviewed: YYYY-MM-DD
drive_copy: none
---
```

If a Drive copy exists, replace `drive_copy: none` with the Google Doc URL.
