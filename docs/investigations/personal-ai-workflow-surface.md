---
title: Personal Human-AI Workflow Surface
status: exploratory
source_of_truth: github
branch: sandbox
last_reviewed: 2026-04-24
drive_copy: https://docs.google.com/document/d/1jLs8O3OKgs8GWyw2sR1TvIf-Q3el_kGZcQSuUAn9MZg
source_inputs:
  - Google Drive: Personal Task Manager for Human-AI Workflows - Conversation Summary
---

# Personal Human-AI Workflow Surface

## Purpose

This document promotes a Drive-only idea into the repository so it can be evaluated as part of the ProtagonistOS project.

It is not a committed product plan. It is an exploratory note about a possible user-facing workflow surface for solo human-AI work.

## Core Observation

There is no obvious personal task manager designed for shared operation between one human and one or more AI assistants.

Current tools each solve part of the problem:

| Tool category | Strength | Limitation |
|---|---|---|
| Consumer reminders | fast capture | weak agent-readable structure |
| Enterprise PM tools | task state and reporting | too heavy for solo work |
| GitHub Issues | excellent for repo-bound engineering | awkward for personal or cross-domain work |
| Chat | easy interaction | poor durable source of truth |
| Spreadsheets | simple shared structure | no task-native semantics |

The gap is a personal operations surface where a human can remain in control while an AI can read context, propose updates, attach artifacts, manage subtasks, and execute bounded work.

## Relevance to ProtagonistOS

This idea matches the ProtagonistOS philosophy: the user remains the protagonist, and AI systems act as accountable tools inside user-controlled workflows.

For this repository, the immediate workflow equivalent is:

- GitHub Issues as task cards
- repository Markdown as durable context
- Calendar as time allocation
- Drive as archive/reference
- Codex as an execution and reconciliation agent

That is enough for the current project. A custom ProtagonistOS workflow application can wait.

## Possible Future Product Shape

A future personal human-AI task system could use a Kanban-like model:

- Inbox
- Next
- Waiting
- Scheduled
- Doing
- Review
- Done

Cards could include:

- title
- status
- owner
- context
- priority
- due date
- linked files
- acceptance criteria
- comments
- agent action log
- human approval state

## Trust Boundary

The hard problem is not the interface. The hard problem is the trust boundary.

Low-risk agent actions:

- summarize context
- suggest tags
- identify duplicate tasks
- draft subtasks
- prepare proposed issue text
- link related artifacts

Higher-risk actions:

- mark work complete
- delete tasks
- send messages
- create calendar commitments
- change deadlines
- modify project priorities

Higher-risk actions should require human approval unless the user explicitly delegates them.

## Current Recommendation

Do not build this as a ProtagonistOS app yet.

First, stabilize the project workflow using existing tools:

1. Repository Markdown for truth.
2. GitHub Issues for work.
3. Google Calendar for time.
4. Google Drive for archive.
5. Codex for execution and reconciliation.

After that workflow proves itself, revisit whether a native ProtagonistOS personal operations surface belongs on the roadmap.

