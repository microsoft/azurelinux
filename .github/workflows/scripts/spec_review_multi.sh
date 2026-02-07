#!/bin/bash

# Multi-model spec review: runs two models sequentially, then synthesizes results.
# See .github/workflows/scripts/README.md for usage.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPEC_REVIEW="${SCRIPT_DIR}/spec_review.sh"

# Defaults
DEFAULT_MODEL1="claude-opus-4.6"
DEFAULT_MODEL2="gpt-5.2-codex"
DEFAULT_SYNTH_MODEL="gpt-5.2-codex"
DEFAULT_OUTPUT="${REPO_ROOT}/.spec_review/report.json"
DEFAULT_WORK_DIR="${REPO_ROOT}/.spec_review/workdir"

# Collected args
SPEC_FILES=()
URLS=()
GIT_SOURCES=()
MODEL1=""
MODEL2=""
SYNTH_MODEL=""
OUTPUT=""
WORK_DIR=""

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Multi-model spec review: runs two different models sequentially, then synthesizes
their findings into a single report using a third model pass.

Options:
    --spec <file>           SPEC file to review (can be specified multiple times)
                            Default: all *.spec files in the repo
    --url <url>             Guideline URL (can be specified multiple times)
    --git-source <url>      Git repository URL for guidelines (can be specified multiple times)
    --model1 <model>        First reviewer model (default: $DEFAULT_MODEL1)
    --model2 <model>        Second reviewer model (default: $DEFAULT_MODEL2)
    --synth-model <model>   Synthesis model (default: $DEFAULT_SYNTH_MODEL)
    --output <file>         Final merged report file
                            Default: \$REPO_ROOT/.spec_review/report.json
    --work-dir <dir>        Working directory for intermediate files
                            Default: \$REPO_ROOT/.spec_review/workdir
    -h, --help              Show this help message

Intermediate files (kept for debugging):
    <work-dir>/report_a.json    - Report from model1
    <work-dir>/report_b.json    - Report from model2
    <work-dir>/kb_a.md          - Knowledge base from model1
    <work-dir>/kb_b.md          - Knowledge base from model2
    <work-dir>/kb_synth.md      - Synthesis notes
    <work-dir>/log_a.md         - Copilot log from model1
    <work-dir>/log_b.md         - Copilot log from model2
    <work-dir>/log_synth.md     - Copilot log from synthesis

Examples:
    # Review with defaults (claude + gpt-5.2-codex reviewers, gpt-5.2-codex synthesizer)
    $(basename "$0") --spec path/to/foo.spec

    # Custom models
    $(basename "$0") --spec foo.spec --model1 gpt-5.2-codex --model2 claude-opus-4.6 --synth-model gpt-5.2-codex

    # Full custom invocation
    $(basename "$0") --spec foo.spec --spec bar.spec \\
        --model1 claude-opus-4.6 --model2 gpt-5.2-codex --synth-model gpt-5.2-codex \\
        --output final_report.json --work-dir /tmp/spec_review
EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --spec)
            [[ -z "${2:-}" ]] && { echo "Error: --spec requires an argument" >&2; exit 1; }
            if [[ ! -f "$2" ]]; then
                echo "Error: Spec file not found: $2" >&2
                exit 1
            fi
            SPEC_FILES+=("$2")
            shift 2
            ;;
        --url)
            [[ -z "${2:-}" ]] && { echo "Error: --url requires an argument" >&2; exit 1; }
            URLS+=("$2")
            shift 2
            ;;
        --git-source)
            [[ -z "${2:-}" ]] && { echo "Error: --git-source requires an argument" >&2; exit 1; }
            GIT_SOURCES+=("$2")
            shift 2
            ;;
        --model1)
            [[ -z "${2:-}" ]] && { echo "Error: --model1 requires an argument" >&2; exit 1; }
            MODEL1="$2"
            shift 2
            ;;
        --model2)
            [[ -z "${2:-}" ]] && { echo "Error: --model2 requires an argument" >&2; exit 1; }
            MODEL2="$2"
            shift 2
            ;;
        --synth-model)
            [[ -z "${2:-}" ]] && { echo "Error: --synth-model requires an argument" >&2; exit 1; }
            SYNTH_MODEL="$2"
            shift 2
            ;;
        --output)
            [[ -z "${2:-}" ]] && { echo "Error: --output requires an argument" >&2; exit 1; }
            OUTPUT="$2"
            shift 2
            ;;
        --work-dir)
            [[ -z "${2:-}" ]] && { echo "Error: --work-dir requires an argument" >&2; exit 1; }
            WORK_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Error: Unknown option: $1" >&2
            echo "Use --help for usage information" >&2
            exit 1
            ;;
    esac
done

# Apply defaults
MODEL1="${MODEL1:-$DEFAULT_MODEL1}"
MODEL2="${MODEL2:-$DEFAULT_MODEL2}"
SYNTH_MODEL="${SYNTH_MODEL:-$DEFAULT_SYNTH_MODEL}"
OUTPUT="${OUTPUT:-$DEFAULT_OUTPUT}"
WORK_DIR="${WORK_DIR:-$DEFAULT_WORK_DIR}"

# If no spec files specified, let spec_review.sh find them
if [[ ${#SPEC_FILES[@]} -eq 0 ]]; then
    mapfile -t SPEC_FILES < <(find "$REPO_ROOT" -type f -name "*.spec")
fi

if [[ ${#SPEC_FILES[@]} -eq 0 ]]; then
    echo "Error: No SPEC files found or specified" >&2
    exit 1
fi

# Create work directory
mkdir -p "$WORK_DIR"

# Define intermediate file paths
REPORT_A="${WORK_DIR}/report_a.json"
REPORT_B="${WORK_DIR}/report_b.json"
KB_A="${WORK_DIR}/kb_a.md"
KB_B="${WORK_DIR}/kb_b.md"
KB_SYNTH="${WORK_DIR}/kb_synth.md"
LOG_A="${WORK_DIR}/log_a.md"
LOG_B="${WORK_DIR}/log_b.md"
LOG_SYNTH="${WORK_DIR}/log_synth.md"

echo "=== Multi-Model Spec Review Configuration ==="
echo "Model 1 (Reviewer A): $MODEL1"
echo "Model 2 (Reviewer B): $MODEL2"
echo "Synthesis Model:      $SYNTH_MODEL"
echo "Output:               $OUTPUT"
echo "Work Directory:       $WORK_DIR"
echo "SPEC files:           ${#SPEC_FILES[@]}"
echo ""

# Build common args for spec_review.sh
common_args=()
for spec in "${SPEC_FILES[@]}"; do
    common_args+=("--spec" "$spec")
done
for url in "${URLS[@]}"; do
    common_args+=("--url" "$url")
done
for git_source in "${GIT_SOURCES[@]}"; do
    common_args+=("--git-source" "$git_source")
done

echo "=== Phase 1: Review ==="
echo ""

echo "[Reviewer A] Starting with model: $MODEL1"
"$SPEC_REVIEW" "${common_args[@]}" \
    --model "$MODEL1" \
    --output "$REPORT_A" \
    --knowledge-base "$KB_A" \
    --log "$LOG_A"
echo "[Reviewer A] Completed successfully"
echo ""

echo "[Reviewer B] Starting with model: $MODEL2"
"$SPEC_REVIEW" "${common_args[@]}" \
    --model "$MODEL2" \
    --output "$REPORT_B" \
    --knowledge-base "$KB_B" \
    --log "$LOG_B"
echo "[Reviewer B] Completed successfully"

echo ""
echo "Both reviewers completed successfully."
echo "  Report A: $REPORT_A"
echo "  Report B: $REPORT_B"
echo ""

echo "=== Phase 2: Synthesis ==="
echo "Starting synthesis with model: $SYNTH_MODEL"
echo ""

# Run synthesis pass
"$SPEC_REVIEW" "${common_args[@]}" \
    --synthesize \
    --report-a "$REPORT_A" \
    --report-b "$REPORT_B" \
    --kb-a "$KB_A" \
    --kb-b "$KB_B" \
    --model "$SYNTH_MODEL" \
    --output "$OUTPUT" \
    --knowledge-base "$KB_SYNTH" \
    --log "$LOG_SYNTH"

echo ""
echo "=== Multi-Model Spec Review Complete ==="
echo ""
echo "Final report:     $OUTPUT"
echo ""
echo "Intermediate files (for debugging):"
echo "  Report A ($MODEL1): $REPORT_A"
echo "  Report B ($MODEL2): $REPORT_B"
echo "  KB A:           $KB_A"
echo "  KB B:           $KB_B"
echo "  KB Synth:       $KB_SYNTH"
echo "  Log A:          $LOG_A"
echo "  Log B:          $LOG_B"
echo "  Log Synth:      $LOG_SYNTH"
echo ""

echo "=== Model Comparison ==="
echo ""
python3 "${SCRIPT_DIR}/spec_review_schema.py" compare \
    "$REPORT_A" "$REPORT_B" "$OUTPUT" \
    --label-a "Reviewer A ($MODEL1)" \
    --label-b "Reviewer B ($MODEL2)" \
    --label-final "Synthesized ($SYNTH_MODEL)"
echo ""
echo "To view/format results:"
echo "   jq . $OUTPUT"
