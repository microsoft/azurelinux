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

# Ensure GITHUB_ACCESS_TOKEN picks up Azure DevOps System.AccessToken
# CRITICAL FIX: Manually setting GitHub access token if not already set
if [ -z "${GITHUB_ACCESS_TOKEN:-}" ]; then
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    export GITHUB_ACCESS_TOKEN="$GITHUB_TOKEN"
    echo "🔑 Using GITHUB_TOKEN as GITHUB_ACCESS_TOKEN"
  elif [ -n "${AZDO_GITHUB_TOKEN:-}" ]; then
    export GITHUB_ACCESS_TOKEN="$AZDO_GITHUB_TOKEN"
    echo "🔑 Using AZDO_GITHUB_TOKEN as GITHUB_ACCESS_TOKEN"
  fi
fi

# Also pick up Azure DevOps OAuth token if available
if [ -n "${SYSTEM_ACCESSTOKEN:-}" ]; then
  export GITHUB_ACCESS_TOKEN="$SYSTEM_ACCESSTOKEN"
  echo "🔑 Using SYSTEM_ACCESSTOKEN as GITHUB_ACCESS_TOKEN"
fi

# Simplify GitHub integration: enable comments if token present
# Check if GitHub PAT is available - needed for posting comments
if [ "$POST_GITHUB_COMMENTS" = "true" ] || [ "$USE_GITHUB_CHECKS" = "true" ]; then
  echo "🔍 GitHub Integration Enabled"
  echo "  - Repository: ${GITHUB_REPOSITORY:-NOT SET}"
  echo "  - PR Number: ${GITHUB_PR_NUMBER:-NOT SET}"
  if [ -n "${GITHUB_ACCESS_TOKEN:-}" ]; then
    echo "  ✅ GITHUB_ACCESS_TOKEN is set, comments/checks will be posted"
  else
    echo "  ⚠️ GITHUB_ACCESS_TOKEN not set, GitHub integration will be disabled"
    POST_GITHUB_COMMENTS=false
    USE_GITHUB_CHECKS=false
  fi
fi

echo "🔍 Ensuring GitHub repo and PR context..."
# Derive repository in 'owner/repo' format if missing, via git remote or BUILD_REPOSITORY_URI
if [ -z "${GITHUB_REPOSITORY:-}" ]; then
  # Try git remote origin first
  remote_url=$(git config --get remote.origin.url || echo "")
  if [[ $remote_url =~ github\.com[:/]+([^/]+/[^/]+)(\.git)?$ ]]; then
    export GITHUB_REPOSITORY="${BASH_REMATCH[1]}"
    echo "🔎 Derived GITHUB_REPOSITORY=$GITHUB_REPOSITORY from git remote"
  else
    # Fallback to BUILD_REPOSITORY_URI if remote origin not matching
    if [[ "${BUILD_REPOSITORY_URI:-}" =~ github\.com[:/]+([^/]+/[^/]+)(\.git)?$ ]]; then
      export GITHUB_REPOSITORY="${BASH_REMATCH[1]}"
      echo "🔎 Derived GITHUB_REPOSITORY=$GITHUB_REPOSITORY from BUILD_REPOSITORY_URI"
    else
      echo "⚠️ Could not derive GITHUB_REPOSITORY from remote or BUILD_REPOSITORY_URI"
    fi
  fi
fi

# Derive PR number if missing
if [ -z "${GITHUB_PR_NUMBER:-}" ]; then
  if [ -n "${SYSTEM_PULLREQUEST_PULLREQUESTNUMBER:-}" ]; then
    export GITHUB_PR_NUMBER="${SYSTEM_PULLREQUEST_PULLREQUESTNUMBER}"
    echo "🔎 Derived GITHUB_PR_NUMBER=$GITHUB_PR_NUMBER from SYSTEM_PULLREQUEST_PULLREQUESTNUMBER"
  elif [ -n "${SYSTEM_PULLREQUEST_PULLREQUESTID:-}" ]; then
    export GITHUB_PR_NUMBER="${SYSTEM_PULLREQUEST_PULLREQUESTID}"
    echo "🔎 Derived GITHUB_PR_NUMBER=$GITHUB_PR_NUMBER from SYSTEM_PULLREQUEST_PULLREQUESTID"
  else
    echo "⚠️ SYSTEM_PULLREQUEST_PULLREQUESTNUMBER or ID not set, comments may not post"
  fi
fi

export GITHUB_REPOSITORY
export GITHUB_PR_NUMBER

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
if [[ "${FAIL_ON_WARNINGS,,}" = "true" ]]; then
  CMD="$CMD --fail-on-warnings"
fi
if [[ "${USE_EXIT_CODE_SEVERITY,,}" = "true" ]]; then
  CMD="$CMD --exit-code-severity"
fi
if [[ "${POST_GITHUB_COMMENTS,,}" = "true" ]]; then
  CMD="$CMD --post-github-comments"
fi
if [[ "${USE_GITHUB_CHECKS,,}" = "true" ]]; then
  CMD="$CMD --use-github-checks"
fi

# 4) Execute the analysis
echo "🔍 Running CveSpecFilePRCheck with: $CMD"
eval $CMD
exit $?
