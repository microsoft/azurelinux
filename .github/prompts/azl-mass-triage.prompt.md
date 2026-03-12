---
description: "Triage a batch of build failures from a JSON results file or control tower job id guid — diagnose, bucketize, and summarize"
agent: azl-diagnose
argument-hint: Path to a JSON file containing build results (e.g., results.json) or control tower job id guid.
---

# Batch Build Triage

- **Results file/guid**: `${input:results_file:path to results JSON file or control tower job id guid}`
- **Koji base URL**: `${input:koji_url:Koji base URL (e.g. https://koji.example.com)}`

Follow the [skill-mass-triage skill](../skills/skill-mass-triage/SKILL.md) to triage all failed builds in `${input:results_file}`.

Pass the Koji base URL (`${input:koji_url}`) and the results file path to the skill workflow. You will be acting as an orchestrator here, so even though you have the skills to diagnose build failures directly you should NOT do that work yourself. Instead, follow the instructions in the skill file on how to coordinate other agents.
