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

# Define exit code meanings
EXIT_SUCCESS=0
EXIT_CRITICAL=1
EXIT_ERROR=2
EXIT_WARNING=3
EXIT_FATAL=10

# Flag to control whether warnings should fail the pipeline
FAIL_ON_WARNINGS=${FAIL_ON_WARNINGS:-false}

# Flag to control whether to use different exit codes for different severities
USE_EXIT_CODE_SEVERITY=${USE_EXIT_CODE_SEVERITY:-false}

# GitHub integration options
POST_GITHUB_COMMENTS=${POST_GITHUB_COMMENTS:-false}
USE_GITHUB_CHECKS=${USE_GITHUB_CHECKS:-false}

# Initialize CMD to avoid unbound variable errors
CMD=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --fail-on-warnings)
      FAIL_ON_WARNINGS=true
      shift
      ;;
    --exit-code-severity)
      USE_EXIT_CODE_SEVERITY=true
      shift
      ;;
    --post-github-comments)
      POST_GITHUB_COMMENTS=true
      shift
      ;;
    --use-github-checks)
      USE_GITHUB_CHECKS=true
      shift
      ;;
    *)
      echo "⚠️ Unknown parameter: $1"
      shift
      ;;
  esac
done

# 1) Source the config script to login and export OPENAI_* variables
echo "⚙️  Applying OpenAI config…"
# Use path relative to current directory instead of 'scripts/'
source ./apply-security-config.sh --openaiModel=o3-mini

# Map environment variables for Azure OpenAI client
echo "🔄 Mapping environment variables to expected format..."
export AZURE_OPENAI_ENDPOINT="$OPENAI_API_BASE"
export AZURE_OPENAI_DEPLOYMENT_NAME="$OPENAI_DEPLOYMENT_NAME"
export AZURE_OPENAI_MODEL_NAME="$OPENAI_MODEL_NAME"
export AZURE_OPENAI_API_VERSION="$OPENAI_API_VERSION"

# Set BUILD_SOURCESDIRECTORY if not already set
if [ -z "${BUILD_SOURCESDIRECTORY:-}" ]; then
  export BUILD_SOURCESDIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
  echo "📂 Setting BUILD_SOURCESDIRECTORY to $BUILD_SOURCESDIRECTORY"
fi

# Verify the environment variables are set
echo "✅ Verifying environment variables:"
echo "  - AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT:-NOT SET}"
echo "  - AZURE_OPENAI_DEPLOYMENT_NAME: ${AZURE_OPENAI_DEPLOYMENT_NAME:-NOT SET}"
echo "  - AZURE_OPENAI_MODEL_NAME: ${AZURE_OPENAI_MODEL_NAME:-NOT SET}"
echo "  - AZURE_OPENAI_API_VERSION: ${AZURE_OPENAI_API_VERSION:-NOT SET}"
echo "  - BUILD_SOURCESDIRECTORY: ${BUILD_SOURCESDIRECTORY:-NOT SET}"
echo "  - FAIL_ON_WARNINGS: ${FAIL_ON_WARNINGS}"
echo "  - USE_EXIT_CODE_SEVERITY: ${USE_EXIT_CODE_SEVERITY}"
echo "  - POST_GITHUB_COMMENTS: ${POST_GITHUB_COMMENTS}"
echo "  - USE_GITHUB_CHECKS: ${USE_GITHUB_CHECKS}"

# For local testing - if PR commit IDs are not set, use HEAD and HEAD~1
if [ -z "${SYSTEM_PULLREQUEST_SOURCECOMMITID:-}" ] || [ -z "${SYSTEM_PULLREQUEST_TARGETCOMMITID:-}" ]; then
  echo "⚠️ PR commit IDs not found, trying to determine from git..."
  export SYSTEM_PULLREQUEST_SOURCECOMMITID=$(git rev-parse HEAD)
  
  # Try to find the target branch more robustly
  if [ -n "${SYSTEM_PULLREQUEST_TARGETBRANCH:-}" ]; then
    # Try to fetch the target branch if it exists - quote branch name to handle slashes properly
    echo "🔄 Trying to fetch target branch: ${SYSTEM_PULLREQUEST_TARGETBRANCH}"
    git fetch --depth=1 origin "${SYSTEM_PULLREQUEST_TARGETBRANCH}" || true
    
    # Double-quote branch names to handle branches with slashes
    if git rev-parse "origin/${SYSTEM_PULLREQUEST_TARGETBRANCH}" >/dev/null 2>&1; then
      export SYSTEM_PULLREQUEST_TARGETCOMMITID=$(git rev-parse "origin/${SYSTEM_PULLREQUEST_TARGETBRANCH}")
      echo "✅ Found target commit from branch: ${SYSTEM_PULLREQUEST_TARGETBRANCH}"
    else
      # If we can't find the branch, use HEAD~1 as fallback
      export SYSTEM_PULLREQUEST_TARGETCOMMITID=$(git rev-parse HEAD~1)
      echo "⚠️ Could not find target branch, using previous commit as fallback"
    fi
  else
    # No target branch info, use HEAD~1
    export SYSTEM_PULLREQUEST_TARGETCOMMITID=$(git rev-parse HEAD~1)
    echo "⚠️ No target branch specified, using previous commit as fallback"
  fi
fi

# Enhanced GitHub integration settings
echo "🔍 Setting up GitHub API access..."

# IMPORTANT: Prefer CBL-Mariner bot token from keyvault over SYSTEM_ACCESSTOKEN
# Check if the GITHUB_TOKEN is available (from apply-security-config.sh)
if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "✅ CBL-Mariner bot token is available for GitHub authentication (from keyvault)"
  # Log the token prefix (first few chars) for debugging
  echo "🔑 CBL-Mariner bot token prefix: ${GITHUB_TOKEN:0:4}..."
# Fall back to SYSTEM_ACCESSTOKEN if no CBL-Mariner bot token is available
elif [ -n "${SYSTEM_ACCESSTOKEN:-}" ]; then
  echo "✅ SYSTEM_ACCESSTOKEN is available for GitHub OAuth authentication"
  echo "🔄 Setting GITHUB_TOKEN to SYSTEM_ACCESSTOKEN for compatibility"
  export GITHUB_TOKEN="${SYSTEM_ACCESSTOKEN}"
  # Log the token prefix (first few chars) for debugging
  echo "🔑 Token prefix: ${SYSTEM_ACCESSTOKEN:0:4}..."
else
  echo "❌ No GitHub token found - GitHub integration will be disabled"
  # Disable GitHub integration features if no token is available
  POST_GITHUB_COMMENTS=false
  USE_GITHUB_CHECKS=false
fi

# Double-check token availability and export explicitly
if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "✅ Final validation: GITHUB_TOKEN is set (prefix: ${GITHUB_TOKEN:0:4}...)"
  # Make sure we pass and expose this to the Python script
  export GITHUB_TOKEN
else
  echo "❌ GITHUB_TOKEN is not set after authentication setup - will not be able to post comments!"
fi

# Verify GitHub integration settings
if [ "$POST_GITHUB_COMMENTS" = "true" ] || [ "$USE_GITHUB_CHECKS" = "true" ]; then
  echo "🔍 GitHub Integration Enabled"
  echo "  - Repository: ${GITHUB_REPOSITORY:-NOT SET}"
  echo "  - PR Number: ${GITHUB_PR_NUMBER:-NOT SET}"
  
  # Verify required variables
  if [ -z "${GITHUB_REPOSITORY:-}" ]; then
    echo "⚠️ GITHUB_REPOSITORY not set, GitHub integration may fail"
  fi
  
  if [ -z "${GITHUB_PR_NUMBER:-}" ]; then
    echo "⚠️ GITHUB_PR_NUMBER not set, GitHub integration may fail"
  fi
fi

echo "🔍 Using commits for diff:"
echo "  - Source: ${SYSTEM_PULLREQUEST_SOURCECOMMITID}"
echo "  - Target: ${SYSTEM_PULLREQUEST_TARGETCOMMITID}"

# 2) Install Python dependencies into your active environment
echo "📦 Installing Python dependencies…"
pip install --upgrade pip
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 3) Build the Python invocation command with flags
echo "⚙️  Building Python command for CveSpecFilePRCheck.py"
CMD="python3 CveSpecFilePRCheck.py"

# Explicitly set flags based on environment variables
echo "🔧 Configuring PR check settings:"
if [[ "${FAIL_ON_WARNINGS,,}" = "true" ]]; then
  CMD="$CMD --fail-on-warnings"
  echo "  - Will fail on warnings: YES"
else
  echo "  - Will fail on warnings: NO"
fi

if [[ "${USE_EXIT_CODE_SEVERITY,,}" = "true" ]]; then
  CMD="$CMD --exit-code-severity"
  echo "  - Using exit code severity: YES"
else
  echo "  - Using exit code severity: NO"
fi

# Add GitHub integration flags to the command based on settings
if [[ "${POST_GITHUB_COMMENTS,,}" = "true" ]]; then
  CMD="$CMD --post-github-comments"
  echo "  - GitHub comments: ENABLED (integrated)"
else
  echo "  - GitHub comments: DISABLED (not requested)"
fi

if [[ "${USE_GITHUB_CHECKS,,}" = "true" ]]; then
  CMD="$CMD --use-github-checks"
  echo "  - GitHub checks: ENABLED (integrated)"
else
  echo "  - GitHub checks: DISABLED"
fi

# 4) Execute the analysis
echo "🔍 Running CveSpecFilePRCheck with: $CMD"
echo ""
echo "============================================================"
echo "ENVIRONMENT VARIABLES FOR GITHUB INTEGRATION:"
echo "  - GITHUB_REPOSITORY: ${GITHUB_REPOSITORY:-NOT SET}"
echo "  - GITHUB_PR_NUMBER: ${GITHUB_PR_NUMBER:-NOT SET}"
echo "  - GITHUB_TOKEN: ${GITHUB_TOKEN:+SET (not showing value)}"
echo "  - POST_GITHUB_COMMENTS: $POST_GITHUB_COMMENTS"
echo "============================================================"
echo ""

# Run the command with all environment variables visible
eval $CMD
exit $?