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
# Use path relative to current directory instead of 'scripts/'
source ./apply-security-config.sh --openaiModel=o3-mini

# Map environment variables for Azure OpenAI client
echo "🔄 Mapping environment variables to expected format..."
export AZURE_OPENAI_ENDPOINT="$OPENAI_API_BASE"
export AZURE_OPENAI_DEPLOYMENT_NAME="$OPENAI_DEPLOYMENT_NAME"

# Set BUILD_SOURCESDIRECTORY if not already set
if [ -z "${BUILD_SOURCESDIRECTORY:-}" ]; then
  export BUILD_SOURCESDIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
  echo "📂 Setting BUILD_SOURCESDIRECTORY to $BUILD_SOURCESDIRECTORY"
fi

# Verify the environment variables are set
echo "✅ Verifying environment variables:"
echo "  - AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT:-NOT SET}"
echo "  - AZURE_OPENAI_DEPLOYMENT_NAME: ${AZURE_OPENAI_DEPLOYMENT_NAME:-NOT SET}"
echo "  - BUILD_SOURCESDIRECTORY: ${BUILD_SOURCESDIRECTORY:-NOT SET}"

# For local testing - if PR commit IDs are not set, use HEAD and HEAD~1
if [ -z "${SYSTEM_PULLREQUEST_SOURCECOMMITID:-}" ] || [ -z "${SYSTEM_PULLREQUEST_TARGETCOMMITID:-}" ]; then
  echo "⚠️ PR commit IDs not found, using local git commits for testing"
  export SYSTEM_PULLREQUEST_SOURCECOMMITID=$(git rev-parse HEAD)
  export SYSTEM_PULLREQUEST_TARGETCOMMITID=$(git rev-parse HEAD~1)
fi

echo "🔍 Using commits for diff:"
echo "  - Source: ${SYSTEM_PULLREQUEST_SOURCECOMMITID}"
echo "  - Target: ${SYSTEM_PULLREQUEST_TARGETCOMMITID}"

# 2) Install Python dependencies into your active environment
echo "📦 Installing Python dependencies…"
pip install --upgrade pip

# Install all dependencies from requirements.txt (including azure-identity and azure-ai-openai)
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 3) Run the CVE spec file recommender
echo "🔍 Running CveSpecFileRecommenderClass.py…"
python CveSpecFileRecommenderClass.py
