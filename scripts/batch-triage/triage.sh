#!/bin/bash
# Batch triage tool — runs the azl-diagnose agent in a containerized environment
# to triage build failures from a JSON results file.
set -euo pipefail

IMAGE_NAME="localhost/azurelinux/batch-triage"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Parse args: [--results /path/to/file.json] [extra prompt text]
RESULTS_FILE="./results.json"
if [[ "${1:-}" == "--results" ]]; then
    if [[ -z "${2:-}" ]]; then
        echo "Error: --results requires a file path argument" >&2
        exit 1
    fi
    RESULTS_FILE="$2"
    shift 2
fi
EXTRA_PROMPT="${*:-}"

# Resolve to absolute path and validate
RESULTS_FILE="$(realpath -m "$RESULTS_FILE")"
if [[ ! -f "$RESULTS_FILE" ]]; then
    echo "Error: Results file not found: $RESULTS_FILE" >&2
    echo "Usage: $0 [--results /path/to/file.json] [extra prompt text]" >&2
    exit 1
fi
RESULTS_BASENAME="$(basename "$RESULTS_FILE")"

# Always build — layer caching makes this fast when nothing changed
# Use buildx if available, otherwise fall back to legacy builder
echo "Building triage image..." >&2
if docker buildx version &>/dev/null; then
    docker buildx build -q -t "$IMAGE_NAME" "$SCRIPT_DIR" >&2
else
    echo "Warning: docker-buildx not found, using legacy builder. Install docker-buildx to remove warning." >&2
    docker build -t "$IMAGE_NAME" "$SCRIPT_DIR" >&2
fi

echo "Running triage agent..." >&2
DOCKER_ARGS=( --rm )

# Run as the calling user so output files have the right ownership
DOCKER_ARGS+=( -u "$(id -u):$(id -g)" )

# Mount the repo root read-only, with a writable output dir.
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"

# Require a .env file for MCP server config (Koji URL, auth, etc.)
ENV_FILE=""
if [[ -f "${REPO_ROOT}/.vscode/mcps/.env" ]]; then
    ENV_FILE="${REPO_ROOT}/.vscode/mcps/.env"
elif [[ -f "${REPO_ROOT}/.env" ]]; then
    ENV_FILE="${REPO_ROOT}/.env"
else
    echo "Error: No .env file found. Create one at .env in the repo root or .vscode/mcps/.env" >&2
    echo "See .vscode/mcps/.env.example for required variables." >&2
    echo "Koji MCP will not auto-configure without this file." >&2
    exit 1
fi

# Ensure a clean output dir
OUTPUT_DIR="${REPO_ROOT}/out/triage"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Configure mounts and working dir
DOCKER_ARGS+=( -v "${REPO_ROOT}:/workspace:ro" )
DOCKER_ARGS+=( -v "${OUTPUT_DIR}:/workspace/out/triage" )
DOCKER_ARGS+=( --tmpfs "/workspace/base/build:rw,uid=$(id -u),gid=$(id -g),mode=775" )
DOCKER_ARGS+=( -v "${RESULTS_FILE}:/triage-input/${RESULTS_BASENAME}:ro" )
DOCKER_ARGS+=( -w /workspace )

# Load MCP server config from .env
DOCKER_ARGS+=( --env-file "$ENV_FILE" )

# Forward any auth env vars that are set
for var in COPILOT_GITHUB_TOKEN GH_TOKEN GITHUB_TOKEN; do
    [[ -n "${!var:-}" ]] && DOCKER_ARGS+=( -e "$var=${!var}" )
done

# Mount any auth config dirs that exist (ro, mapped ${HOME} passed to the container)
[[ -d "${HOME}/.copilot" ]]    && DOCKER_ARGS+=( -v "${HOME}/.copilot:/home/copilot/.copilot:ro"  )
[[ -d "${HOME}/.config/gh" ]]  && DOCKER_ARGS+=( -v "${HOME}/.config/gh:/home/copilot/.config/gh:ro" )

DOCKER_ARGS+=( -e "HOME=/home/copilot" )

# Task prompt:
PROMPT="Follow the instructions in .github/prompts/azl-mass-triage.prompt.md to triage /triage-input/${RESULTS_BASENAME}.
The repo is mounted read-only! Write output to /workspace/out/triage/ (final output only). The base/build dirs are a writable tmpfs for intermediate files.
Place ONLY the final report .md and .json files in the output dir, no other files should be written there. Use the mounted tmpfs for ALL other files.
Once complete, write a report summarizing the investigation, findings, and next steps into a markdown file in the output dir."

if [[ -n "$EXTRA_PROMPT" ]]; then
    PROMPT+=$'\n\nAdditional instructions from the user:\n'
    PROMPT+="$EXTRA_PROMPT"
fi

# Security: --allow-all-* is safe here — the repo is mounted read-only, output is
# restricted to out/triage/, and the container provides process isolation.
COPILOT_ARGS=(--allow-all-tools --allow-all-paths --allow-all-urls --agent azl-diagnose -p "$PROMPT")

exec docker run "${DOCKER_ARGS[@]}" -- "$IMAGE_NAME" "${COPILOT_ARGS[@]}"
