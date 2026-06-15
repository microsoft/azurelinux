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

# Locate this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/security-config-dev.json"

# Function to get a secret from Azure Key Vault
get_azure_secret_value_from_keyvault() {
  local vault_name="$1"
  local secret_name="$2"
  local env_var_name="$3"
  
  echo "Retrieving secret $secret_name from key vault $vault_name"
  local secret_value
  secret_value=$(az keyvault secret show --vault-name "$vault_name" --name "$secret_name" --query "value" -o tsv)
  
  if [ -z "$secret_value" ]; then
    echo "Error: Failed to retrieve secret $secret_name from key vault $vault_name"
    return 1
  fi
  
  # Set the environment variable with the secret value
  declare -g "$env_var_name=$secret_value"
  echo "Successfully retrieved secret and set to environment variable $env_var_name"
}

# Parse the --openaiModel argument
CONFIG_OPENAI_MODEL=""
for arg in "$@"; do
  case $arg in
    --openaiModel=*) CONFIG_OPENAI_MODEL="${arg#*=}" ;;  # e.g. o3-mini
    *) ;;
  esac
done

# OPENAI settings
#---------------------------

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


# CBL-Mariner repo on github
#---------------------------
KV_NAME=$(jq -r '.aiCvePatching.cblMarinerRepo.keyvaultName' "$CONFIG_FILE")
PRPAT_NAME=$(jq -r '.aiCvePatching.cblMarinerRepo.secretNames.prPatName' "$CONFIG_FILE")

echo "Get CBL-Mariner github config"
echo "  - KV_NAME:        $KV_NAME"
echo "  - PRPAT_NAME:     $PRPAT_NAME"

# set PR config
get_azure_secret_value_from_keyvault "$KV_NAME" "$PRPAT_NAME" GITHUB_PRPAT
echo "##vso[task.setvariable variable=githubPrPat;issecret=true]$GITHUB_PRPAT"

# Also export the PAT so it's available to child processes
export GITHUB_TOKEN="$GITHUB_PRPAT"
echo "GitHub Token has been exported as GITHUB_TOKEN environment variable"