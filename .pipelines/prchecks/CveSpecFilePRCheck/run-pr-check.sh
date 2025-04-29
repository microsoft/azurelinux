#!/usr/bin/env bash
set -euo pipefail

# 1) Render the real JSON from your template
echo "📋 Rendering security-config-dev.json…"
envsubst < scripts/security-config-dev.template.json \
  > scripts/security-config-dev.json

# 2) Ensure jq is available for parsing
if ! command -v jq &>/dev/null; then
  echo "🔧 Installing jq…"
  apt-get update && apt-get install -y jq
fi

# 3) Call your config script (it will do UMI login + set pipeline vars)
echo "⚙️  Applying OpenAI config via apply-security-config.sh…"
bash scripts/apply-security-config.sh \
  --aiCvePatching \
  --openaiModel=o3-mini

# 4) Pull the same values into THIS shell so Python can see them
CONFIG_FILE="scripts/security-config-dev.json"
OPENAI_API_VERSION=$(jq -r ".aiCvePatching.models.\"o3-mini\".openaiApiVersion"  "$CONFIG_FILE")
OPENAI_API_BASE=$(jq -r      ".aiCvePatching.models.\"o3-mini\".openaiApiBase"     "$CONFIG_FILE")
OPENAI_DEPLOYMENT_NAME=$(jq -r".aiCvePatching.models.\"o3-mini\".openaiDeploymentName" "$CONFIG_FILE")
OPENAI_MODEL_NAME=$(jq -r     ".aiCvePatching.models.\"o3-mini\".openaiModelName"      "$CONFIG_FILE")

export OPENAI_API_VERSION OPENAI_API_BASE OPENAI_DEPLOYMENT_NAME OPENAI_MODEL_NAME

echo "🔗 Exported:"
echo "  OPENAI_API_VERSION=$OPENAI_API_VERSION"
echo "  OPENAI_API_BASE=$OPENAI_API_BASE"
echo "  OPENAI_DEPLOYMENT_NAME=$OPENAI_DEPLOYMENT_NAME"
echo "  OPENAI_MODEL_NAME=$OPENAI_MODEL_NAME"

# 5) Install Python deps
echo "📦 Installing Python dependencies…"
pip install --upgrade pip
pip install -r requirements.txt

# 6) Run the PR-check
echo "🔍 Running run_pr_checks.py…"
python run_pr_checks.py
