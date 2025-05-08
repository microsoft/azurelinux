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
    # Try to fetch the target branch if it exists
    echo "🔄 Trying to fetch target branch: ${SYSTEM_PULLREQUEST_TARGETBRANCH}"
    git fetch origin "${SYSTEM_PULLREQUEST_TARGETBRANCH}" --depth=1 || true
    
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

# For GitHub integration
if [ -z "${GITHUB_REPOSITORY:-}" ] || [ -z "${GITHUB_PR_NUMBER:-}" ]; then
  # Extract from ADO variables if possible
  if [ -n "${SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI:-}" ]; then
    # Extract repo from URI (e.g. https://github.com/owner/repo.git -> owner/repo)
    export GITHUB_REPOSITORY=$(echo $SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI | sed -E 's/.*github.com\/([^.]+)(\.git)?/\1/')
    echo "📂 Setting GITHUB_REPOSITORY to $GITHUB_REPOSITORY"
  fi
  
  if [ -n "${SYSTEM_PULLREQUEST_PULLREQUESTID:-}" ]; then
    export GITHUB_PR_NUMBER=$SYSTEM_PULLREQUEST_PULLREQUESTID
    echo "📊 Setting GITHUB_PR_NUMBER to $GITHUB_PR_NUMBER"
  fi
fi

echo "🔍 Using commits for diff:"
echo "  - Source: ${SYSTEM_PULLREQUEST_SOURCECOMMITID}"
echo "  - Target: ${SYSTEM_PULLREQUEST_TARGETCOMMITID}"

if [ "$POST_GITHUB_COMMENTS" = "true" ] || [ "$USE_GITHUB_CHECKS" = "true" ]; then
  echo "🔍 GitHub Integration Details:"
  echo "  - Repository: ${GITHUB_REPOSITORY:-NOT SET}"
  echo "  - PR Number: ${GITHUB_PR_NUMBER:-NOT SET}"
  echo "  - GitHub Token: ${GITHUB_ACCESS_TOKEN:+SET}"
  
  if [ -z "${GITHUB_ACCESS_TOKEN:-}" ]; then
    echo "⚠️ GITHUB_ACCESS_TOKEN not set, GitHub integration will be disabled"
    POST_GITHUB_COMMENTS=false
    USE_GITHUB_CHECKS=false
  fi
fi

# 2) Install Python dependencies into your active environment
echo "📦 Installing Python dependencies…"
pip install --upgrade pip

# Install all dependencies from requirements.txt (including azure-identity and azure-ai-openai)
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 3) Run the CVE spec file checker
echo "🔍 Running CveSpecFilePRCheck.py…"

# Build command with arguments
CMD="python CveSpecFilePRCheck.py"
if [ "$FAIL_ON_WARNINGS" = "true" ]; then
  CMD="$CMD --fail-on-warnings"
fi
if [ "$USE_EXIT_CODE_SEVERITY" = "true" ]; then
  CMD="$CMD --exit-code-severity" 
fi
if [ "$POST_GITHUB_COMMENTS" = "true" ]; then
  CMD="$CMD --post-github-comments"
fi
if [ "$USE_GITHUB_CHECKS" = "true" ]; then
  CMD="$CMD --use-github-checks"
fi

# Run the command and capture exit code
echo "🚀 Running command: $CMD"
eval $CMD
PR_CHECK_EXIT_CODE=$?

# Process the exit code appropriately 
if [ $PR_CHECK_EXIT_CODE -eq $EXIT_SUCCESS ]; then
  echo "✅ PR check completed successfully"
  echo "=================================================="
  echo "No critical issues found in spec files"
  echo "=================================================="
elif [ $PR_CHECK_EXIT_CODE -eq $EXIT_WARNING ]; then
  if [ "$FAIL_ON_WARNINGS" = "true" ]; then
    echo "❌ PR check failed with warnings (exit code $PR_CHECK_EXIT_CODE)"
    echo "=================================================="
    echo "⚠️  WARNINGS DETECTED - PLEASE REVIEW THE ISSUES"
    echo "=================================================="
    # Only propagate failure if FAIL_ON_WARNINGS is true
    exit $EXIT_CRITICAL
  else
    echo "⚠️ PR check completed with warnings (exit code $PR_CHECK_EXIT_CODE)"
    echo "=================================================="
    echo "⚠️  WARNINGS DETECTED BUT PIPELINE CONTINUES"
    echo "=================================================="
    # Don't fail the pipeline for warnings by default
    exit $EXIT_SUCCESS
  fi
elif [ $PR_CHECK_EXIT_CODE -eq $EXIT_ERROR ]; then
  echo "❌ PR check failed with errors (exit code $PR_CHECK_EXIT_CODE)"
  echo "=================================================="
  echo "❌  ERRORS DETECTED - PLEASE FIX THE ISSUES"
  echo "=================================================="
  # Propagate the exit code to fail the pipeline
  exit $EXIT_CRITICAL
elif [ $PR_CHECK_EXIT_CODE -eq $EXIT_CRITICAL ]; then
  echo "❌ PR check failed with critical issues (exit code $PR_CHECK_EXIT_CODE)"
  echo "=================================================="
  echo "🚨  CRITICAL ISSUES DETECTED - PLEASE FIX IMMEDIATELY"
  echo "=================================================="
  # Propagate the exit code to fail the pipeline
  exit $EXIT_CRITICAL
else
  echo "❌ PR check encountered an unexpected error (exit code $PR_CHECK_EXIT_CODE)"
  echo "=================================================="
  echo "⚠️  UNEXPECTED ERROR - CHECK THE LOGS"
  echo "=================================================="
  # Propagate the exit code to fail the pipeline
  exit $PR_CHECK_EXIT_CODE
fi
