#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# test-pr-check-local.sh
#   Local test runner for CVE Spec File PR Check
#   
#   Usage:
#     ./test-pr-check-local.sh
#     SOURCE_COMMIT=abc123 TARGET_COMMIT=def456 ./test-pr-check-local.sh
#     TARGET_COMMIT=HEAD~5 ./test-pr-check-local.sh
#     
#   Environment Variables (optional):
#     SOURCE_COMMIT       - Source commit hash (default: HEAD)
#     TARGET_COMMIT       - Target commit hash (default: auto-detected)
#     GITHUB_TOKEN        - GitHub PAT for API access (optional for local testing)
#     PR_NUMBER           - PR number to analyze (optional, will use branch)
#     ENABLE_OPENAI_ANALYSIS - Set to 'true' to enable AI analysis (default: false)
# -----------------------------------------------------------------------------

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  CVE Spec File PR Check - Local Test Runner${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

echo -e "${BLUE}📁 Repository root:${NC} ${REPO_ROOT}"
echo -e "${BLUE}📁 Script directory:${NC} ${SCRIPT_DIR}"
echo ""

# Set default environment variables for local testing
export BUILD_REPOSITORY_LOCALPATH="${REPO_ROOT}"
export BUILD_SOURCESDIRECTORY="${REPO_ROOT}"
export SYSTEM_PULLREQUEST_SOURCEBRANCH="${SYSTEM_PULLREQUEST_SOURCEBRANCH:-$(git rev-parse --abbrev-ref HEAD)}"
export GITHUB_REPOSITORY="${GITHUB_REPOSITORY:-microsoft/azurelinux}"
export ENABLE_OPENAI_ANALYSIS="${ENABLE_OPENAI_ANALYSIS:-false}"

# Get current branch and set up commit IDs for local testing
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Allow manual override of source/target commits
# Usage: SOURCE_COMMIT=abc123 TARGET_COMMIT=def456 ./test-pr-check-local.sh
if [ -z "${SOURCE_COMMIT:-}" ]; then
    SOURCE_COMMIT=$(git rev-parse HEAD)
    echo -e "${GREEN}✓${NC} Using current HEAD as source commit"
else
    echo -e "${BLUE}ℹ${NC}  Using provided source commit: ${SOURCE_COMMIT:0:8}"
fi

if [ -z "${TARGET_COMMIT:-}" ]; then
    # Try to get the target branch (main/2.0/3.0)
    TARGET_BRANCH="${SYSTEM_PULLREQUEST_TARGETBRANCH:-main}"
    
    # Try merge-base first
    if git rev-parse "origin/${TARGET_BRANCH}" >/dev/null 2>&1; then
        MERGE_BASE=$(git merge-base HEAD "origin/${TARGET_BRANCH}" 2>&1)
        if [ $? -eq 0 ] && [ -n "$MERGE_BASE" ]; then
            TARGET_COMMIT="$MERGE_BASE"
            echo -e "${GREEN}✓${NC} Found merge-base with origin/${TARGET_BRANCH}"
        else
            # Fallback to HEAD~1 if merge-base fails (e.g., grafted commits)
            TARGET_COMMIT=$(git rev-parse HEAD~1 2>/dev/null || git rev-parse HEAD)
            echo -e "${YELLOW}⚠️${NC}  merge-base failed (grafted branch?), using HEAD~1 as target"
        fi
    else
        # Fallback: use HEAD~1 if we can't find the target branch
        TARGET_COMMIT=$(git rev-parse HEAD~1 2>/dev/null || git rev-parse HEAD)
        echo -e "${YELLOW}⚠️${NC}  Could not find origin/${TARGET_BRANCH}, using HEAD~1 as target"
    fi
else
    TARGET_BRANCH="${SYSTEM_PULLREQUEST_TARGETBRANCH:-main}"
    echo -e "${BLUE}ℹ${NC}  Using provided target commit: ${TARGET_COMMIT:0:8}"
fi

export SYSTEM_PULLREQUEST_SOURCECOMMITID="${SOURCE_COMMIT}"
export SYSTEM_PULLREQUEST_TARGETCOMMITID="${TARGET_COMMIT}"

# GitHub integration (disabled by default for local testing)
export POST_GITHUB_COMMENTS="${POST_GITHUB_COMMENTS:-false}"
export USE_GITHUB_CHECKS="${USE_GITHUB_CHECKS:-false}"

echo -e "${GREEN}✓${NC} Current branch: ${SYSTEM_PULLREQUEST_SOURCEBRANCH}"
echo -e "${GREEN}✓${NC} Target branch: ${TARGET_BRANCH}"
echo -e "${GREEN}✓${NC} Source commit: ${SOURCE_COMMIT:0:8}"
echo -e "${GREEN}✓${NC} Target commit: ${TARGET_COMMIT:0:8}"
echo -e "${GREEN}✓${NC} Repository: ${GITHUB_REPOSITORY}"
echo -e "${GREEN}✓${NC} OpenAI Analysis: ${ENABLE_OPENAI_ANALYSIS}"
echo -e "${GREEN}✓${NC} Post GitHub Comments: ${POST_GITHUB_COMMENTS}"
echo ""

# Check if Python virtual environment exists
if [ ! -d "${SCRIPT_DIR}/.venv" ]; then
    echo -e "${YELLOW}⚠️  No virtual environment found. Creating one...${NC}"
    python3 -m venv "${SCRIPT_DIR}/.venv"
    source "${SCRIPT_DIR}/.venv/bin/activate"
    
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    pip install -q --upgrade pip
    pip install -q -r "${SCRIPT_DIR}/requirements.txt"
else
    source "${SCRIPT_DIR}/.venv/bin/activate"
    echo -e "${GREEN}✓${NC} Using existing virtual environment"
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Running PR Check${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Change to script directory
cd "${SCRIPT_DIR}"

# Run the Python checker
python CveSpecFilePRCheck.py "$@"

# Capture exit code
EXIT_CODE=$?

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Test Complete${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Interpret exit code
case $EXIT_CODE in
    0)
        echo -e "${GREEN}✅ SUCCESS:${NC} No critical issues found"
        ;;
    1)
        echo -e "${RED}❌ FAILURE:${NC} Critical issues found"
        ;;
    2)
        echo -e "${RED}💥 ERROR:${NC} Check encountered an error"
        ;;
    3)
        echo -e "${YELLOW}⚠️  WARNING:${NC} Non-critical issues found"
        ;;
    *)
        echo -e "${RED}❓ UNKNOWN:${NC} Unexpected exit code: $EXIT_CODE"
        ;;
esac

echo ""
echo -e "${BLUE}📄 Report files:${NC}"
if [ -f "${SCRIPT_DIR}/pr_check_report.txt" ]; then
    echo -e "  ${GREEN}✓${NC} pr_check_report.txt"
fi
if [ -f "${SCRIPT_DIR}/pr_check_results.json" ]; then
    echo -e "  ${GREEN}✓${NC} pr_check_results.json"
fi

echo ""
echo -e "${BLUE}💡 Tips:${NC}"
echo -e "  • View full report: ${YELLOW}cat pr_check_report.txt${NC}"
echo -e "  • View JSON results: ${YELLOW}cat pr_check_results.json | jq${NC}"
echo -e "  • Enable AI analysis: ${YELLOW}ENABLE_OPENAI_ANALYSIS=true ./test-pr-check-local.sh${NC}"
echo -e "  • Test specific spec: ${YELLOW}./test-pr-check-local.sh --spec-file SPECS/package/package.spec${NC}"
echo ""

exit $EXIT_CODE
