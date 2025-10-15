# Local Testing Guide for CVE Spec File PR Check

This guide explains how to run the CVE Spec File PR Check locally without pushing to Azure DevOps pipelines.

## Quick Start

```bash
cd /path/to/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck
./test-pr-check-local.sh
```

## Prerequisites

- Git repository cloned
- Python 3.10+ installed
- Bash shell

The script will automatically:
- Create a Python virtual environment (`.venv/`)
- Install required dependencies from `requirements.txt`
- Detect source and target commits
- Run the PR check

## Usage Examples

### Auto-detect commits (default)
```bash
./test-pr-check-local.sh
```
This will:
- Use current HEAD as source commit
- Try to find merge-base with `origin/main` as target
- Fall back to `HEAD~1` if merge-base fails (e.g., grafted branches)

### Specify target commit explicitly
```bash
TARGET_COMMIT=HEAD~5 ./test-pr-check-local.sh
```

### Specify both source and target commits
```bash
SOURCE_COMMIT=abc123def TARGET_COMMIT=456789abc ./test-pr-check-local.sh
```

### Compare against a specific commit hash
```bash
TARGET_COMMIT=6c6441460 ./test-pr-check-local.sh
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SOURCE_COMMIT` | Source commit hash | Current HEAD |
| `TARGET_COMMIT` | Target commit hash | Auto-detected (merge-base or HEAD~1) |
| `SYSTEM_PULLREQUEST_TARGETBRANCH` | Target branch name | `main` |
| `ENABLE_OPENAI_ANALYSIS` | Enable AI analysis | `false` |
| `POST_GITHUB_COMMENTS` | Post comments to GitHub | `false` |
| `USE_GITHUB_CHECKS` | Use GitHub check API | `false` |

## Output Files

After running, you'll find:
- `pr_check_report.txt` - Human-readable report
- `pr_check_results.json` - Machine-readable JSON results

**Note:** Both files are validated to exist after the check runs. If either is missing, the script will exit with an error code (10), matching the behavior of the ADO pipeline.

View them with:
```bash
cat pr_check_report.txt
cat pr_check_results.json | jq
```

## Running Unit Tests

```bash
cd /path/to/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck
source .venv/bin/activate
python -m unittest discover -s tests -v
```

All 29 unit tests should pass.

## Troubleshooting

### "Source or target commit ID not found"
Make sure you're in a git repository and the commits exist:
```bash
git rev-parse HEAD
git rev-parse HEAD~1
```

### Grafted branches (no shared history)
If your branch is grafted and has no shared history with origin/main, the script will automatically fall back to using `HEAD~1` as the target. You can also specify commits explicitly:
```bash
SOURCE_COMMIT=$(git rev-parse HEAD) TARGET_COMMIT=$(git rev-parse HEAD~1) ./test-pr-check-local.sh
```

### Unicode errors in git diff
This has been fixed in the code. If you still see issues, ensure your git config is set to UTF-8:
```bash
git config --global core.quotepath false
```

## What Gets Checked

The PR check analyzes changed `.spec` files for:
- **Critical Issues** (block the PR):
  - Missing CVE patches
  - CVE patch/changelog mismatches
  - Missing or incorrect Release number bumps
  
- **Info/Warnings**:
  - Unused patch files
  - Changelog formatting issues
  - Future-dated CVE entries

## Integration with Azure DevOps

When you're ready to test in the actual ADO pipeline, just push your changes. The same code runs in both environments, so if it works locally, it should work in ADO.

## Tips

- Start with local testing to iterate quickly
- Use `tail -f pr_check_report.txt` to watch progress
- Set `ENABLE_OPENAI_ANALYSIS=true` only when you have Azure credentials configured
- The script respects `.gitignore` patterns for spec files
