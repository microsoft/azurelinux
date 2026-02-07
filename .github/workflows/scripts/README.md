# Spec Review: Local Developer Guide

Run the spec-review workflow locally via VS Code, shell scripts, or the Copilot CLI.

There are three major paths:

1. **[Use VS Code / Copilot Chat](#use-vs-code--copilot-chat)** (interactive, most flexible)
2. **[Run the shell scripts](#run-single-model-review-spec_reviewsh)** (single or multi-model, automated)
3. **[Use Copilot CLI manually](#use-copilot-cli-manually)** (interactive, most flexible, scriptable)

---

## Use VS Code / Copilot Chat

The easiest way to get quick, interactive feedback is with [GitHub Copilot](https://github.com/features/copilot) in VS Code (or via [Copilot CLI](#use-copilot-cli-manually)). The `spec-review` agent is designed to review spec files and provide feedback in a structured format the same way as the shell scripts, but with the added benefit of a conversational interface where you can ask follow-up questions, request clarifications, or dive deeper into specific issues.

1. Open this repo in VS Code with **GitHub Copilot Chat**.
2. In Copilot Chat, select the **`spec-review`** agent (bottom left corner of the chat window, "Agent", "Ask", "Edit", "Plan", etc.)
3. Prompt example:

   ```md
   Review the azl release spec please.
   ```

---

## Run single-model review (spec_review.sh)

`spec_review.sh` orchestrates the Copilot agent, writes report/log/kb, and validates JSON. This is a subset of the multi-model script (`spec_review_multi.sh`) which the pipeline uses, but is faster to run.

### Prerequisites

- **Python**: 3.11+ (CI uses 3.12)
- **Node.js + npm** (for `@github/copilot` CLI)
- **GitHub Copilot token**: export `GH_TOKEN` (scope: `copilot:org_member`) or run `gh auth login`
- Optional: `jq` (for JSON pretty-print)

```bash
cd ~/repos/azurelinux
python -m venv .venv && source .venv/bin/activate
pip install -r .github/workflows/scripts/requirements.txt
    gh copilot
    # OR
    npm install -g @github/copilot
copilot --version  # verify CLI
```

### Usage

```bash
# Defaults: reviews all *.spec in repo, writes to repo root
#   spec_review_report.json, copilot_log.md, spec_review_kb.md

./.github/workflows/scripts/spec_review.sh \
  --spec base/comps/azurelinux-release/azurelinux-release.spec \
  --spec base/comps/azurelinux-repos/azurelinux-repos.spec

# Validate / inspect
python .github/workflows/scripts/spec_review_schema.py /tmp/spec_review_report.json --all
python .github/workflows/scripts/spec_review_schema.py /tmp/spec_review_report.json --json | jq
```

The script supports additional options (like selecting a model, or using different URLs); run with `--help` for details.

```bash
./.github/workflows/scripts/spec_review.sh --help
```

## Run multi-model review (spec_review_multi.sh)

`spec_review_multi.sh` runs two different LLMs sequentially as independent reviewers, then
uses a third model pass to synthesize their findings into a single high-quality report. This is the flow used in the CI pipeline.

**Why multi-model?**

- Model diversity catches different issues (reduces false negatives)
- Synthesis pass deduplicates and resolves conflicts intelligently
- Higher confidence in findings that both models agree on

```bash
# Defaults: claude-opus-4.6 + gpt-5.2-codex reviewers, gpt-5.2-codex synthesizer
./.github/workflows/scripts/spec_review_multi.sh \
  --spec base/comps/azurelinux-release/azurelinux-release.spec

# Custom models
./.github/workflows/scripts/spec_review_multi.sh \
  --spec foo.spec \
  --model1 gpt-5.2-codex \
  --model2 claude-opus-4.6 \
  --synth-model gpt-5.2-codex \
  --output final_report.json

# View intermediate files for debugging
ls /tmp/spec_review_workdir/
#   report_a.json, report_b.json   - individual reviewer reports
#   kb_a.md, kb_b.md               - knowledge bases
#   kb_synth.md                    - synthesis notes
#   log_a.md, log_b.md, log_synth.md - copilot session logs
```

Run with `--help` for all options:

```bash
./.github/workflows/scripts/spec_review_multi.sh --help
```

---

## Use Copilot CLI manually (interactive, most flexible, scriptable)

```bash
# Expects the agent file to be in .github/agents/spec-review.agent.md. Can also be
# copied to the host global agents dir (~/.copilot/agents/).

# Interactive run
copilot --agent spec-review
```

```bash
# For semi-automated or fully automated runs, use -i or -p flags:
prompt="Review: base/comps/azurelinux-release/azurelinux-release.spec against packaging guidelines.\n"\
"Write JSON to spec_review_report.json and validate with: python .github/workflows/scripts/spec_review_schema.py spec_review_report.json"

# Semi-interactive (runs prompt, then waits for the user)
copilot --agent spec-review \
  --allow-all-tools \
  --add-dir "$PWD" \
  --allow-url https://docs.fedoraproject.org \
  --allow-url https://rpm-packaging-guide.github.io \
  --allow-url http://rpm.org \
  -i "$prompt"

# NOTE:
# --allow-all-urls can be used instead of individual --allow-url entries,
# but is less reliable since it may allow unwanted URLs.

# Fully automated (runs prompt directly, exits when done)
copilot --agent spec-review \
  --allow-all-tools \
  --add-dir "$PWD" \
  --allow-url https://docs.fedoraproject.org \
  --allow-url https://rpm-packaging-guide.github.io \
  --allow-url http://rpm.org \
  -p "$prompt"

# Review output
python .github/workflows/scripts/spec_review_schema.py spec_review_report.json --all
```

## Future work

- Support generated specfiles from overlays
- Add explicit instruction files for different files (e.g., packaging guidelines, best practices)
- Cache the knowledge base between runs to speed up subsequent reviews and reduce web requests
- De-prioritize upstream issues in the spec file, focus on local changes
  - Clearly indicate changes in the current PR
- More tools for the agent (e.g., diffing specs, rpmlint, etc.)
