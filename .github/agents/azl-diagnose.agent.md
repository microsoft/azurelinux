---
name: azl-diagnose
description: Diagnose build failures — fetch Koji task info/logs, investigate upstream sources, identify root cause, and suggest fixes. Accepts task IDs, URLs, package names, or general queries.
argument-hint: Ask a question about a package (e.g., `kernel`) or give a task ID/URL (e.g., `1234`, `https://koji.example.com/koji/taskinfo?taskID=1234`).
agents: ["*"]
user-invokable: true
disable-model-invocation: false
handoffs:
  - label: Attempt to diagnose and fix the issue
    agent: azl-diagnose
    prompt: Follow the directions in [the debug workflow](../prompts/azl-debug-component.prompt.md) to fix the issue. Ensure a review agent runs before declaring the fix ready, to ensure it follows best practices and won't cause future maintenance issues. If the review agent raises concerns, address them, and then re-run the review (repeate as needed).
    send: true
  - label: Ask follow-up questions
    agent: azl-diagnose
    prompt: Briefly summarize the findings in one paragraph or less, then help the user with any follow-up questions.
    send: true
  - label: Write a summary to a markdown file
    agent: azl-diagnose
    prompt: Write a report summarizing the investigation, findings, and next steps into a markdown file in the current directory.
    send: true
  - label: Make a commit with the fix
    agent: azl-diagnose
    prompt: If the changes are made **AND READY**, commit them with a clear message describing the fix. The commit message should follow the conventional commit format (e.g., `fix(pkg): fix build failure due to missing dependency\n\nDetailed explanation of the fix with references to relevant sources and excerpts from upstream bug reports, changelogs, or commits that informed the fix.\nTested by doing thing.`). Do not reference internal-only koji in the PR message (upstream is fine). Ensure only the changes related to the fix are included in the commit (Do not remove unrelated changes, offer to stash or unstage them instead). Propose a commit message (in markdown code block) to the user, and ask for confirmation before commiting. If no fix has been made yet, respond with "No fix identified yet, so no commit made." If a fix has been made but is not ready, respond with "A fix has been identified but is not ready to be committed yet."
    send: true
---
# Build Failure Diagnosis

This agent diagnoses build failures — Koji triage, upstream investigation, root cause analysis, and fix recommendations. Follow the [skill-koji-triage skill](../skills/skill-koji-triage/SKILL.md) for the full investigation workflow, including discovery, log analysis, and failure categorization.

## Workflow

1. Determine the Koji base URL (from env `KOJI_BASE_URL` or ask the user)
2. If the user provides a **task ID or URL** → go directly to the investigation workflow in the skill
3. If the user provides a **package name** → follow the discovery workflow in the skill (both Path A and Path B)
4. Identify the root cause using the failure categories in the skill
5. Investigate upstream sources (Fedora dist-git, bug tracker, mailing list, etc.) for relevant information and potential fixes (the `fedora-distgit` tool may be helpful here, or re-use the koji MCP for pulling from upstream Fedora's public koji instance at "https://koji.fedoraproject.org")
6. Present a clear summary: what failed, why, and what to do next
