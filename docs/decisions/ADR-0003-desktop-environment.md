---
title: "ADR-0003: Canonical Desktop Environment"
status: active
source_of_truth: github
branch: dev
last_reviewed: 2026-04-27
drive_copy: none
source_inputs:
  - GitHub Issue #4
  - docs/decisions/ADR-0001-project-workflow-source-of-truth.md
  - docs/decisions/ADR-0002-branching-upstream-sync-and-access-policy.md
  - docs/reports/protagonistos-technical-status.md
---

# ADR-0003: Canonical Desktop Environment

## Status

Accepted.

## Context

ProtagonistOS documentation currently mixes multiple desktop directions:

- COSMIC as the first desktop target in top-level project docs
- KDE and minimal Wayland listed as unresolved alternatives in current status docs

This ambiguity blocks consistent package planning, issue scoping, and image composition work.

The project needs one canonical desktop environment so that all downstream package, integration, and validation work follows a single direction.

## Decision

KDE is the canonical desktop environment for ProtagonistOS.

Decision details:

- KDE is the default and primary desktop target for roadmap, packaging, and image composition.
- Minimal Wayland compositor setups may be used as temporary bring-up/testing steps only.
- COSMIC research remains useful historical analysis, but it is not current product direction unless superseded by a future ADR.

## Consequences

### Packaging and dependency scope

- Prioritize KDE stack planning and packaging instead of COSMIC-first package sequencing.
- Desktop prerequisite work remains Mesa-first (hardware acceleration before shell polish).
- Future desktop gap matrices, acceptance criteria, and work estimates should reference KDE requirements.

### Session and integration surface

- Desktop login/session design should align with KDE session expectations.
- Desktop portal and desktop-service integration should target KDE-compatible defaults.
- Desktop image definitions should be designed around a KDE-first user experience.

### Documentation and workflow

- Active docs must present KDE as a single unambiguous direction.
- Legacy COSMIC-heavy analyses should be explicitly marked as historical where they remain in-repo.
- New desktop execution issues should align to KDE-first milestones after this ADR.

## Migration Guidance

When updating existing docs:

1. Treat this ADR as authoritative for desktop direction.
2. Replace active "COSMIC-first" language with KDE-first guidance.
3. If older COSMIC analysis is retained for reference, mark it as historical/superseded context.
4. Preserve technical findings that remain valid regardless of DE choice (for example, Mesa hardware acceleration requirements and Linux-host build constraints).

## Review Trigger

Revisit this ADR only if one of the following occurs:

- KDE packaging/integration proves infeasible within project constraints,
- project goals change materially, or
- a new desktop strategy is formally proposed and accepted through a follow-up ADR.
