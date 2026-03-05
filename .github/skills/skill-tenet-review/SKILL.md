---
name: skill-tenet-review
description: "[Skill] Request a tenet review for proposed changes. Use when changes could affect Azure Linux design goals, anti-goals, or policies. Triggers: tenet review, check tenets, design review, anti-goal check, policy compliance, package change, package addition/removal."
user-invocable: false
disable-model-invocation: false
---

# Tenet Review

Use this skill when your changes could affect Azure Linux design decisions. The tenets define what Azure Linux **must do** (goals), **may do** (non-goals), and **must not do** (anti-goals).

## When to Request a Tenet Review

Request a review when changes touch any of (but not limited to):
- Package additions/removals
- Configuration changes (kernel, toml, package, image, etc.)
- Image/VM/WSL/container composition changes
- Changes that could impact security, performance, reliability, or maintainability
- Design decisions that could affect user experience or compatibility
- Licensing changes
- Engineering tools/process changes that could affect how the team works

If unsure, request a review — false positives are cheap, missed anti-goal violations are not.

## How to Request a Review

Delegate the review to a sub-agent to avoid loading all of the tenet documents into your own context. There are two approaches depending on your capabilities.

### Path A: Named Agent (preferred)

If you can pass `agentName` to `runSubagent` (requires the user to have enabled custom agent invocation in VS Code settings), use the dedicated tenet reviewer agent. It has built-in review instructions.

```
runSubagent(
  agentName: "azl-tenet-reviewer",
  description: "Tenet review for <topic>",
  prompt: "Review the following changes against Azure Linux tenets. Read ALL tenet files in ./docs/tenets/tenets.*.md before reviewing.\n\n## Changes\n<describe changes in detail along with any pertinent background>\n\n## Context\n<why these changes are being made>\n\nReturn your review using the structured output format (Verdict, Anti-Goal Violations, Goal Alignment, Non-Goal Notes, Recommendations)."
)
```

### Path B: Generic Sub-Agent (fallback)

If `agentName` is not available, call `runSubagent` without it and embed the review instructions directly in the prompt. The sub-agent will have a fresh context window — plenty of room for tenets + the review guide + the change description.

```
runSubagent(
  description: "Tenet review for <topic>",
  prompt: "You are a tenet reviewer for Azure Linux. Follow the review guide in ./.github/skills/skill-tenet-review/REVIEW-GUIDE.md — read that file first, then read ALL tenet files listed in it, then review the changes below.\n\n## Changes\n<describe changes in detail along with any pertinent background>\n\n## Context\n<why these changes are being made>\n\nReturn your review using the structured output format from the guide."
)
```

The review guide ([REVIEW-GUIDE.md](REVIEW-GUIDE.md)) contains the complete self-contained procedure: which files to read, how to classify findings, and the output format. A vanilla sub-agent reading that file has everything it needs. You do not need to read the guide yourself — just make sure it is included in the prompt for the sub-agent.

### Path C: Inline Review (last resort)

If `runSubagent` is not available at all (e.g., you are already a sub-agent), you can perform the review inline by reading [REVIEW-GUIDE.md](REVIEW-GUIDE.md) and following its procedure directly. Only do this as a last resort as it will consume a lot of context and may be less efficient than delegating to a dedicated reviewer agent.

## Interpreting Results

The reviewer returns a structured report with a verdict:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **PASS** | Change aligns with all applicable tenets | Proceed |
| **WARN** | Partial misalignment or risky implications | Review recommendations, address if feasible, and call out residual risk |
| **FAIL** | Anti-goal violation detected | Pause implementation/build/testing and ask the user for direction (drop, redesign, or explicit exception). Do not continue without explicit confirmation |

For agent workflows, **FAIL is a hard decision gate**: report the violating tenet(s), summarize options, and wait for user direction before making further changes.

## What NOT to Send for Review

- Pure formatting/comment changes
- Moving component definitions between files (no functional change)
- Build log analysis or triage (not a design decision)
