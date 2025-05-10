#!/usr/bin/env bash
#
# run-pr-check.sh
# 1) Sources apply-security-config.sh
# 2) Installs Python deps
# 3) Runs Python checker which posts via GitHubClient
set -euo pipefail

################################################################################
# 1) Parse flags
################################################################################
FAIL_ON_WARNINGS=${FAIL_ON_WARNINGS:-false}
USE_EXIT_CODE_SEVERITY=${USE_EXIT_CODE_SEVERITY:-false}
POST_GITHUB_COMMENTS=${POST_GITHUB_COMMENTS:-false}
USE_GITHUB_CHECKS=${USE_GITHUB_CHECKS:-false}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fail-on-warnings)    FAIL_ON_WARNINGS=true ;;
    --exit-code-severity)  USE_EXIT_CODE_SEVERITY=true ;;
    --post-github-comments) POST_GITHUB_COMMENTS=true ;;
    --use-github-checks)   USE_GITHUB_CHECKS=true ;;
    *) echo "⚠️ Unknown parameter: $1" ;;
  esac
  shift
done

################################################################################
# 2) Apply OpenAI config (UMI login + vars)
################################################################################
echo "⚙️  Applying OpenAI config…"
source ./apply-security-config.sh --openaiModel=o3-mini

# Map to Azure OpenAI client vars
export AZURE_OPENAI_ENDPOINT="$OPENAI_API_BASE"
export AZURE_OPENAI_DEPLOYMENT_NAME="$OPENAI_DEPLOYMENT_NAME"
export AZURE_OPENAI_MODEL_NAME="$OPENAI_MODEL_NAME"
export AZURE_OPENAI_API_VERSION="$OPENAI_API_VERSION"

# Ensure BUILD_SOURCESDIRECTORY is set
if [ -z "${BUILD_SOURCESDIRECTORY:-}" ]; then
  export BUILD_SOURCESDIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
fi

################################################################################
# 3) Ensure we have a GitHub token (App or fallback)
################################################################################
if [ -z "${GITHUB_ACCESS_TOKEN:-}" ]; then
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    export GITHUB_ACCESS_TOKEN="$GITHUB_TOKEN"
    echo "🔑 Using GITHUB_TOKEN fallback"
  elif [ -n "${SYSTEM_ACCESSTOKEN:-}" ]; then
    export GITHUB_ACCESS_TOKEN="$SYSTEM_ACCESSTOKEN"
    echo "🔑 Using SYSTEM_ACCESSTOKEN fallback"
  else
    echo "⚠️ No GitHub token available; will skip comments/checks"
  fi
fi

################################################################################
# 4) Install Python dependencies
################################################################################
echo "📦 Installing Python dependencies…"
pip install --upgrade pip
pip install -r requirements.txt

################################################################################
# 5) Run the Python PR checker
################################################################################
echo "🔍 Running CVE Spec File PR check…"
python3 CveSpecFilePRCheck.py \
  ${FAIL_ON_WARNINGS:+--fail-on-warnings} \
  ${USE_EXIT_CODE_SEVERITY:+--exit-code-severity} \
  ${POST_GITHUB_COMMENTS:+--post-github-comments} \
  ${USE_GITHUB_CHECKS:+--use-github-checks}
