# scripts/run-pr-check.sh
#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# run-pr-check.sh
#   Entry point for PR checks:
#   1) Sources apply-security-config.sh to login and export vars
#   2) Installs Python dependencies
#   3) Runs the Python PR-checker
# -----------------------------------------------------------------------------

# 1) Source the config script to login and export OPENAI_* variables
echo "⚙️  Applying OpenAI config…"
source scripts/apply-security-config.sh --openaiModel=o3-mini

# 2) Install Python dependencies into your active environment
echo "📦 Installing Python dependencies…"
pip install --upgrade pip
pip install -r requirements.txt

# 3) Run the PR-check Python script
echo "🔍 Running run_pr_checks.py…"
python run_pr_checks.py
