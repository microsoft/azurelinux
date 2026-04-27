---
title: "ADR-0001: Project Workflow and Source of Truth"
status: active
source_of_truth: github
branch: dev
last_reviewed: 2026-04-27
drive_copy: none
source_inputs:
  - docs/README.md
  - Google Drive: ProtagonistOS Drive Organization Instructions
  - Google Drive: Personal Task Manager for Human-AI Workflows - Conversation Summary
---

# ADR-0001: Project Workflow and Source of Truth

## Status

Accepted.

## Context

ProtagonistOS is a solo-developer operating system project with multiple knowledge surfaces:

- this Git repository
- Google Drive documents
- Google Calendar
- GitHub Issues
- Codex sessions and, later, Codex automations

The project needs one authoritative technical record. Without that, planning notes, chat summaries, Drive documents, and repository files can drift apart.

## Decision

The Git repository is the source of truth for ProtagonistOS technical state.

Google Drive is a secondary archive and reference layer. It may contain planning notes, readable exports, summaries, historical artifacts, and documents intended for human review, but it is not authoritative unless the content has been promoted back into the repository.

GitHub Issues are the primary workflow surface for concrete project work. Issues should track tasks, investigations, blockers, acceptance criteria, and follow-up work.

Google Calendar is the primary time-allocation surface. It should be used for focus blocks, build windows, testing sessions, review time, and scheduled operational work.

Codex is allowed to operate across these surfaces, but repository content wins when surfaces disagree.

## Workflow Model

Use the surfaces this way:

| Surface | Role |
|---|---|
| Git repository | Authoritative technical documentation, source code, specs, image configs, ADRs, reports |
| GitHub Issues | Task queue, active workflow, blockers, acceptance criteria, project execution state |
| Google Calendar | Time blocking and scheduling for actual work sessions |
| Google Drive | Archive, readable copies, planning notes, historical context, exported summaries |
| Codex sessions | Execution, reconciliation, drafting, implementation, summarization |
| Codex automations | Later workflow automation after the manual model is stable |

## Documentation Rules

- Technical facts belong in Markdown in this repository first.
- Drive-originated technical material must be reconciled into the repository before it is treated as current truth.
- Drive copies should be marked as non-authoritative when they mirror repository docs.
- GitHub Issues should link to repository documents rather than duplicating long technical explanations.
- Calendar events should link to the issue or repo document they are meant to advance.
- Codex should prefer updating repository docs and issues over creating new isolated Drive documents.

## Current Drive Reconciliation Rules

The existing Drive folder should be treated as an archive/reference area, not the project operating center.

Useful Drive documents should be promoted into this repository when they answer one of these questions:

- What is currently true?
- What did we decide?
- How do we reproduce this?
- What did we test?
- What failed, and why?
- What task or decision should become a GitHub Issue or ADR?

Drive documents that are historical, exploratory, or stale may remain in Drive, but the repository should say whether they are active, archived, or superseded.

## Consequences

This keeps ProtagonistOS from becoming split across chat, Drive, and local memory.

The repository becomes the durable project brain. GitHub Issues become the operating board. Calendar becomes the time budget. Drive becomes the attic: useful, searchable, but not where active truth lives.
