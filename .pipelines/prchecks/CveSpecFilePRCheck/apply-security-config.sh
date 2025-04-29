#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/security-config-dev.json"

CONFIG_AI_CVE_PATCHING="false"
CONFIG_OPENAI_MODEL=""

for arg in "$@"; do
  case $arg in
    --aiCvePatching)    CONFIG_AI_CVE_PATCHING="true"    ;;
    --openaiModel=*)    CONFIG_OPENAI_MODEL="${arg#*=}"  ;;
  esac
done

if [[ "$CONFIG_AI_CVE_PATCHING" == "true" ]]; then
  echo "🔎 Applying AI CVE Patching with model: $CONFIG_OPENAI_MODEL"

  # 1) login via the UMI defined in JSON
  UMI_ID=$(jq -r '.umiId' "$CONFIG_FILE")
  echo "##vso[task.setvariable variable=umiId]$UMI_ID"
  az login --identity --client-id "$UMI_ID"

  # 2) pull out the OpenAI settings
  OPENAI_API_VERSION=$(jq -r \
    ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiApiVersion" \
    "$CONFIG_FILE")
  OPENAI_API_BASE=$(jq -r \
    ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiApiBase" \
    "$CONFIG_FILE")
  OPENAI_DEPLOYMENT_NAME=$(jq -r \
    ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiDeploymentName" \
    "$CONFIG_FILE")
  OPENAI_MODEL_NAME=$(jq -r \
    ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiModelName" \
    "$CONFIG_FILE")

  # 3) export them as pipeline variables
  echo "##vso[task.setvariable variable=openAiApiVersion]$OPENAI_API_VERSION"
  echo "##vso[task.setvariable variable=openAiApiBase]$OPENAI_API_BASE"
  echo "##vso[task.setvariable variable=openAiDeploymentName]$OPENAI_DEPLOYMENT_NAME"
  echo "##vso[task.setvariable variable=openAiModelName]$OPENAI_MODEL_NAME"
else
  echo "⚠️  AI CVE patching not enabled; skipping."
fi
