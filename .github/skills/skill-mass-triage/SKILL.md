````skill
---
name: skill-mass-triage
description: "[Skill] Batch-triage build failures from a JSON results file — diagnose with parallel sub-agents, bucketize by root cause, and produce a consolidated summary. Use when asked to triage a Koji results file. Triggers: batch triage, mass triage, triage results file, bucketize failures."
user-invocable: false
disable-model-invocation: false
---

# Batch Build Triage

Triage failed builds from a JSON results file. Diagnose each failure using sub-agents, bucketize by root cause, and produce a consolidated summary. This workflow handles any number of failures — from 1 to hundreds — using the same sub-agent dispatch pattern throughout.

## Input Format

The input results file is a JSON object with this structure:

```json
{
    "numKojiJobs": 9876,
    "numKojiJobsClosed": 9870,
    "numKojiJobsFailed": 6,
    "buildTasks": [
    {
      "taskStatus": "Failed",
      "kojiInfo": {
        "kojiTaskNumber": 12345,
        "componentName": "my-package",
        "kojiTaskStatus": "Failed"
      }
    }
  ]
}
```

Key fields:
- `buildTasks[].taskStatus` — `"Failed"` or `"Completed"`
  - NOTE: Some builds may have overall status "Completed" while individual tasks failed, or vice versa. Use the OR of both `taskStatus` and `kojiTaskStatus` to catch all failure modes.
- `buildTasks[].kojiInfo.kojiTaskStatus` — more detailed status. Filter to `"Failed"` for triage.
- `buildTasks[].kojiInfo.kojiTaskNumber` — the Koji task ID (use with the Koji base URL to construct URLs)
- `buildTasks[].kojiInfo.componentName` — package name

## Workflow

### Phase 1 — Diagnose (parallel sub-agents)

> **STOP — READ THIS FIRST.** You are the **orchestrator**. Your ONLY job in this phase is to:
> 1. Parse the results file to extract failed task IDs and package names
> 2. Configure Koji and create the output directory
> 3. Partition failures into batches and write batch files
> 4. Generate the sub-agent prompt `.md` file
> 5. Spawn sub-agents to do the actual diagnosis
>
> **Do NOT fetch Koji logs, read build output, investigate failures, or do any diagnostic work yourself.** That is the sub-agents' job. If you catch yourself calling `koji_fetch`, reading a skill file about *how to triage*, or analyzing build errors — you have gone off-script. Stop and spawn a sub-agent instead.

> **IMPORTANT:** Always save diagnostic instructions as a `.md` file in the working directory and reference it by path when spawning sub-agents — do NOT pass full prompt text inline in `runSubagent` calls. This ensures sub-agents can read instructions with file tools, avoids context window bloat in the orchestrator, and persists the instructions for debugging.

1. Read the results file and filter `buildTasks` to only entries with `kojiInfo.kojiTaskStatus` of `"Failed"` or `taskStatus` of `"Failed"` (some failed builds may still have overall status "Completed"). Extract the `kojiTaskNumber` and `componentName` for each failed task.
2. Configure the koji MCP tool:
  - If the user/prompt has provided a Koji base URL, use that.
  - Otherwise, check if the MCP tool is already configured with a base URL (the tool may have been pre-configured by the user or the orchestrator). If it is configured, use that URL.
  - Also check the environment variable `KOJI_BASE_URL` for a URL to use. If it is set, use that.
  - If no URL is available, prompt the user to provide a Koji base URL before proceeding.
3. Create the triage output directory: `base/build/work/scratch/triage/`.
  - Ensure there are no existing JSON files in the triage directory from previous runs, to avoid confusion. If there are, prompt the user to confirm deletion before proceeding.
4. Use cmdline tools (jq, python, etc.) to partition the failed builds into batches of **~6 builds each**, writing a JSON file per batch to the triage directory (e.g., `base/build/work/scratch/triage/batch-1.json`, `batch-2.json`, etc.) with this structure:

> **All temporary and intermediate files** (jq output, working files, batch files, etc.) MUST go in `base/build/work/scratch/triage/` — do NOT use `/tmp` or bare `mktemp -d`.

```json
{
  "tasks": [
    { "taskID": 12345, "package": "my-package" },
    ...
  ]
}
```

Use your best judgement on how many builds to put in each batch, but ~6 should be the maximum to keep the sub-agent workload manageable. Try to maximize parallelism (i.e., more smaller batches rather than fewer larger batches) while keeping the batch size reasonable for a single sub-agent to handle in a timely manner.

> For example, if there are 20 failed builds, it would be better to create 10 batches of 2 builds each, rather than 2 batches of 10 builds each, to enable more parallel sub-agents and faster overall completion.

5. Configure the koji MCP tools for the sub-agents (e.g., set base URL, allow insecure if needed) - do this once in the orchestrator before spawning sub-agents, and they will inherit the configuration.

6. For each batch, spawn a sub-agent using `runSubagent`. **Launch sub-agents in parallel if the platform supports it, BUT limit to 10 parallel sub-agents per wave to avoid rate limiting** (i.e., put multiple `runSubagent` calls in the same tool-call block; if there are more than 10 batches, launch them in successive waves of 10). Each sub-agent receives:
   - The Koji base URL
   - The path to its batch file
   - The output directory path
   - The path to the `.md` prompt file (do NOT inline the prompt content — reference by file path only)

> **IMPORTANT:** Always use a sub-agent — even for a single build. Do NOT diagnose failures inline in the orchestrator. Sub-agents stay scoped to categorization because they follow the prompt `.md` file; the orchestrator tends to over-investigate when it handles diagnosis directly. The orchestrator's job is strictly orchestration: partition, dispatch, collect, bucketize.

7. Each sub-agent writes one JSON file per build to the triage directory: `base/build/work/scratch/triage/<taskID>.json`
8. After all sub-agents complete, verify that a JSON file exists for each failed build. Re-run any missing ones.

### Phase 2 — Bucketize & Summarize (single pass)

1. Read all `*.json` files from `base/build/work/scratch/triage/`.
2. Collect the free-form `failureCategory` values assigned by sub-agents.
3. Normalize similar categories into canonical buckets (e.g., "implicit-int error", "C99 compliance", "GCC 14 implicit int" → **"gcc-implicit-int"**). Use your judgment — the goal is <= ~15 distinct buckets, not one per build. Use your best judgment to assign bucket names that are concise, descriptive, and offer a balance between specificity and generality.
4. Write the consolidated summary to `./triage-summary.json` with this structure:

```json
{
  "generated": "2026-02-23T...",
  "inputFile": "<results file name>",
  "totalBuilds": 150,
  "failedBuilds": 42,
  "buckets": [
    {
      "name": "gcc-implicit-int",
      "description": "C code uses K&R-style implicit int declarations that are errors in GCC 14+",
      "count": 12,
      "tasks": [
        { "taskID": 12345, "package": "gt", "arch": "aarch64", "shortSummary": "dim.c uses old-style function defs" },
        ...
      ]
    },
    ...
  ],
  "undiagnosed": []
}
```

5. Clean up triage scratch files with `koji_cleanup` (but only after the summary is written, in case you need to re-run any sub-agents).
6. Present a human-readable summary to the user: bucket name, count, and representative example for each.

---

## Sub-Agent Prompt Template

Use this as the prompt template when spawning diagnostic sub-agents. Save a single copy of this prompt as a `.md` file into the working directory (e.g., `base/build/work/scratch/triage/diagnose-prompt.md`) and reference it in the `runSubagent` calls, passing the variables during the call to runSubagent.

```
You are diagnosing Koji build failures for Azure Linux. For each task below, investigate the failure and write a JSON summary file.

## Inputs from the orchestrator
- Koji base URL: {{KOJI_BASE_URL}}
- Batch file path: {{BATCH_FILE}} (contains a JSON array of `{ "taskID": <number>, "package": "<name>" }` objects)
- Output directory: {{OUTPUT_DIR}}

## Investigation procedure
Read the skill file at `.github/skills/skill-koji-triage/SKILL.md` for the full investigation
workflow — including how to use MCP tools, fetch logs, and categorize failures. Follow it exactly.

## Setup
1. Read `.github/skills/skill-koji-triage/SKILL.md` (MUST do this first).
2. The orchestrator has already configured the default Koji base URL and SSL settings. **Do NOT call `set_koji_url`** — changing the default would affect other parallel sub-agents sharing the same MCP server.
   - If you need to fetch from a different Koji instance for some reason, pass `override_base_url` directly to `koji_fetch` or `koji_allow_insecure` instead.
3. If the koji tools do not work as-is, inform the orchestrator of the issue — do not attempt to reconfigure them yourself, as that may cause issues for other parallel sub-agents.

## Tasks to diagnose
Read the batch file at: {{BATCH_FILE}}
It contains a JSON array of `{ "taskID": <number>, "package": "<name>" }` objects.
Construct the Koji URL tail for each task as: /koji/taskinfo?taskID=<ID>

## For each task
Follow the "Investigation Workflow" section from the skill file. Then:
1. Identify the failure category. Use a short kebab-case string (e.g., "missing-build-dependency", "gcc-implicit-int", "test-failure", "mock-infra", "source-prep-plugin"). Be specific but consistent.
  - Note: Your job is JUST to categorize the failure, not to propose a fix or root cause analysis. The category should be based on the observed symptoms and error messages, not assumptions about the underlying issue.
2. Write a JSON file to: {{OUTPUT_DIR}}/<taskID>.json
  - The orchestrator will read these files later for bucketization and summary. Follow the schema below exactly.

## Output JSON schema (one file per task)
{
  "taskID": <number>,
  "url": "<full task URL>",
  "package": "<package name>",
  "failureCategory": "<short-kebab-case-category>",
  "failurePhase": "<prep|build|install|check|dependency|infra|source-prep>",
  "shortSummary": "<1-2 sentence human-readable summary>"
}

## Rules
- Do NOT call `set_koji_url` — the orchestrator has already set the default. Use `override_base_url` on `koji_fetch` if you need to target a different URL.
- Do NOT call `koji_cleanup` — there may be multiple sub-agents working in parallel, and they should not delete each other's files. The orchestrator will handle cleanup after all sub-agents complete.
- Do NOT call `koji_allow_insecure` — the orchestrator has already configured SSL settings.
- If a task has no downloadable logs (e.g., plugin error in Result field only), note that in shortSummary.
- If you can't determine the failure, set failureCategory to "unknown" and explain in shortSummary.
- Return a brief summary of findings when done (which tasks succeeded/failed diagnosis).
- Do not edit or modify any files outside of your assigned output JSON file. If you need additional files or configuration, inform the orchestrator.
```

---

## Notes

- The orchestrator handles partitioning, sub-agent dispatch, result collection, bucketization, and cleanup.
- Sub-agents handle only Koji fetching / log analysis / JSON writing — they don't need workspace context.
- If a sub-agent fails or hangs, note the affected task IDs and retry them individually.
- Clean up triage scratch files with `koji_cleanup` only after the final summary is written.

````
