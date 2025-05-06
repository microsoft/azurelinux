# scripts/apply-security-config.sh
#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# apply-security-config.sh
#   1) Reads security-config-dev.json
#   2) Logs in using the user-assigned managed identity (UMI)
#   3) Extracts Azure OpenAI settings
#   4) Emits Azure Pipelines logging commands
#   5) Exports OPENAI_* variables into the current shell
# -----------------------------------------------------------------------------

# Locate this script’s directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/security-config-dev.json"

# Parse the --openaiModel argument
CONFIG_OPENAI_MODEL=""
for arg in "$@"; do
  case $arg in
    --openaiModel=*) CONFIG_OPENAI_MODEL="${arg#*=}" ;;  # e.g. o3-mini
    *) ;;
  esac
done

# 1) Login via the user-assigned managed identity
UMI_ID=$(jq -r '.umiId' "$CONFIG_FILE")   # Extract umiId
# Emit pipeline var for UMI (for other tasks if needed)
echo "##vso[task.setvariable variable=umiId]$UMI_ID"
az login --identity --client-id "$UMI_ID"

# 2) Read the OpenAI deployment details from JSON
OPENAI_API_VERSION=$(jq -r ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiApiVersion"      "$CONFIG_FILE")
OPENAI_API_BASE=$(jq -r      ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiApiBase"         "$CONFIG_FILE")
OPENAI_DEPLOYMENT_NAME=$(jq -r ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiDeploymentName" "$CONFIG_FILE")
OPENAI_MODEL_NAME=$(jq -r     ".aiCvePatching.models.\"$CONFIG_OPENAI_MODEL\".openaiModelName"      "$CONFIG_FILE")

# 3) Emit them as pipeline variables
echo "##vso[task.setvariable variable=openAiApiVersion]$OPENAI_API_VERSION"
echo "##vso[task.setvariable variable=openAiApiBase]$OPENAI_API_BASE"
echo "##vso[task.setvariable variable=openAiDeploymentName]$OPENAI_DEPLOYMENT_NAME"
echo "##vso[task.setvariable variable=openAiModelName]$OPENAI_MODEL_NAME"

# 4) Export for local/bash use
#    So that sourcing this script populates these in the shell environment
export OPENAI_API_VERSION
export OPENAI_API_BASE
export OPENAI_DEPLOYMENT_NAME
export OPENAI_MODEL_NAME
