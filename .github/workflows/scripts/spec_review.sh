#!/bin/bash

# See .github/workflows/scripts/README.md for local usage and troubleshooting.
#
# Args: --spec <spec_file1> --spec <spec_file2> ... --url <guideline_url1> --url <guideline_url2> --output <output_file> --log <log_file> --knowledge-base <knowledge_base_file>

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"

# Defaults
DEFAULT_URLS=(
    "https://docs.fedoraproject.org/en-US/packaging-guidelines/"
    "https://rpm-packaging-guide.github.io/"
    "http://rpm.org/documentation"
    "https://spdx.org/licenses/"
    "https://rpm-software-management.github.io"
    "https://pagure.io/packaging-committee"
)

DEFAULT_GIT_SOURCES=(
    "https://pagure.io/packaging-committee.git"
)

TOOLS=(
    --allow-tool "view" \
    --allow-tool "grep" \
    --allow-tool "glob" \
    --allow-tool "lsp" \
    --allow-tool "read" \
    --allow-tool "search" \
    --allow-tool "write" \
    --allow-tool "edit" \
    --allow-tool "create" \
    --allow-tool "shell(git:log)" \
    --allow-tool "shell(git:show)" \
    --allow-tool "shell(git:diff)" \
    --allow-tool "shell(find:*)" \
    --allow-tool "shell(cat:*)" \
    --allow-tool "shell(head:*)" \
    --allow-tool "shell(tail:*)" \
    --allow-tool "shell(wc:*)" \
    --allow-tool "shell(diff:*)" \
    --allow-tool "shell(test:*)" \
)

DEFAULT_OUTPUT="${REPO_ROOT}/.spec_review/report.json"
DEFAULT_LOG="${REPO_ROOT}/.spec_review/copilot_log.md"
DEFAULT_KNOWLEDGE_BASE="${REPO_ROOT}/.spec_review/kb.md"
DEFAULT_MODEL="claude-opus-4.6"
# Arrays for collected args
SPEC_FILES=()
URLS=()
OUTPUT=""
LOG=""
KNOWLEDGE_BASE=""
GIT_SOURCES=()
MODEL=""

# Synthesis mode args
SYNTHESIZE=false
REPORT_A=""
REPORT_B=""
KB_A=""
KB_B=""

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Review SPEC files for compliance with RPM packaging guidelines.

Options:
    --spec <file>           SPEC file to review (can be specified multiple times)
                            Default: all *.spec files in the repo
    --url <url>             Guideline URL to check against (can be specified multiple times)
                            Default: Fedora packaging guidelines, RPM guide, rpm.org docs
    --git-source <url>      Git repository URL to use as source for guidelines (can be specified multiple times)
                            Default: Fedora packaging guidelines repo
    --model <model>         Language model to use (e.g., gpt-5.2-codex, claude-opus-4.6)
                            Default: $DEFAULT_MODEL
    --output <file>         Output JSON report file
                            Default: \$REPO_ROOT/.spec_review/report.json
    --log <file>            Copilot session log file
                            Default: \$REPO_ROOT/.spec_review/copilot_log.md
    --knowledge-base <file> Knowledge base file for diagnostics
                            Default: \$REPO_ROOT/.spec_review/kb.md

Synthesis Mode (merge two reports):
    --synthesize            Enable synthesis mode to merge two existing reports
    --report-a <file>       First report JSON to merge (required with --synthesize)
    --report-b <file>       Second report JSON to merge (required with --synthesize)
    --kb-a <file>           Knowledge base from first review (optional)
    --kb-b <file>           Knowledge base from second review (optional)

    -h, --help              Show this help message

Examples:
    # Review all spec files with defaults
    $(basename "$0")

    # Review specific spec files
    $(basename "$0") --spec path/to/foo.spec --spec path/to/bar.spec

    # Use custom guideline URLs
    $(basename "$0") --url https://example.com/guidelines

    # Full custom invocation
    $(basename "$0") --spec foo.spec --url https://example.com --output report.json --log session.md --model claude-opus-4.6

    # Synthesis mode: merge two reports
    $(basename "$0") --synthesize --report-a report_a.json --report-b report_b.json \\
        --kb-a kb_a.md --kb-b kb_b.md --spec foo.spec --output final.json --model gpt-5.2-codex
EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --spec)
            [[ -z "${2:-}" ]] && { echo "Error: --spec requires an argument" >&2; exit 1; }
            # Check if file exists
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
        --output)
            [[ -z "${2:-}" ]] && { echo "Error: --output requires an argument" >&2; exit 1; }
            OUTPUT="$2"
            shift 2
            ;;
        --log)
            [[ -z "${2:-}" ]] && { echo "Error: --log requires an argument" >&2; exit 1; }
            LOG="$2"
            shift 2
            ;;
        --knowledge-base)
            [[ -z "${2:-}" ]] && { echo "Error: --knowledge-base requires an argument" >&2; exit 1; }
            KNOWLEDGE_BASE="$2"
            shift 2
            ;;
        --model)
            [[ -z "${2:-}" ]] && { echo "Error: --model requires an argument" >&2; exit 1; }
            MODEL="$2"
            shift 2
            ;;
        --synthesize)
            SYNTHESIZE=true
            shift
            ;;
        --report-a)
            [[ -z "${2:-}" ]] && { echo "Error: --report-a requires an argument" >&2; exit 1; }
            if [[ ! -f "$2" ]]; then
                echo "Error: Report file not found: $2" >&2
                exit 1
            fi
            REPORT_A="$2"
            shift 2
            ;;
        --report-b)
            [[ -z "${2:-}" ]] && { echo "Error: --report-b requires an argument" >&2; exit 1; }
            if [[ ! -f "$2" ]]; then
                echo "Error: Report file not found: $2" >&2
                exit 1
            fi
            REPORT_B="$2"
            shift 2
            ;;
        --kb-a)
            [[ -z "${2:-}" ]] && { echo "Error: --kb-a requires an argument" >&2; exit 1; }
            if [[ ! -f "$2" ]]; then
                echo "Error: Knowledge base file not found: $2" >&2
                exit 1
            fi
            KB_A="$2"
            shift 2
            ;;
        --kb-b)
            [[ -z "${2:-}" ]] && { echo "Error: --kb-b requires an argument" >&2; exit 1; }
            if [[ ! -f "$2" ]]; then
                echo "Error: Knowledge base file not found: $2" >&2
                exit 1
            fi
            KB_B="$2"
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

# Apply defaults if not specified
if [[ ${#URLS[@]} -eq 0 ]]; then
    URLS=("${DEFAULT_URLS[@]}")
fi

if [[ ${#GIT_SOURCES[@]} -eq 0 ]]; then
    GIT_SOURCES=("${DEFAULT_GIT_SOURCES[@]}")
fi

if [[ ${#SPEC_FILES[@]} -eq 0 ]]; then
    mapfile -t SPEC_FILES < <(find "$REPO_ROOT" -type f -name "*.spec")
fi

OUTPUT="${OUTPUT:-$DEFAULT_OUTPUT}"
LOG="${LOG:-$DEFAULT_LOG}"
KNOWLEDGE_BASE="${KNOWLEDGE_BASE:-$DEFAULT_KNOWLEDGE_BASE}"
MODEL="${MODEL:-$DEFAULT_MODEL}"

# Validate synthesis mode requirements
if [[ "$SYNTHESIZE" == true ]]; then
    if [[ -z "$REPORT_A" || -z "$REPORT_B" ]]; then
        echo "Error: --synthesize requires both --report-a and --report-b" >&2
        exit 1
    fi
fi

# Validate we have spec files
if [[ ${#SPEC_FILES[@]} -eq 0 ]]; then
    echo "Error: No SPEC files found or specified" >&2
    exit 1
fi

echo "=== Spec Review Configuration ==="
echo "Mode:           $(if [[ "$SYNTHESIZE" == true ]]; then echo "Synthesis"; else echo "Review"; fi)"
echo "Output:         $OUTPUT"
echo "Log:            $LOG"
echo "Knowledge Base: $KNOWLEDGE_BASE"
echo "SPEC files:     ${#SPEC_FILES[@]}"
echo "URLs:           ${#URLS[@]}"
echo "Git Sources:    ${#GIT_SOURCES[@]}"
echo "Model:          $MODEL"
if [[ "$SYNTHESIZE" == true ]]; then
    echo "Report A:       $REPORT_A"
    echo "Report B:       $REPORT_B"
    [[ -n "$KB_A" ]] && echo "KB A:           $KB_A"
    [[ -n "$KB_B" ]] && echo "KB B:           $KB_B"
fi
echo ""

echo "Reviewing SPEC files for compliance with packaging guidelines..."
for SPEC_FILE in "${SPEC_FILES[@]}"; do
    echo "  - $SPEC_FILE"
done

echo ""
echo "Using guidelines from:"
allow_url_args=()
for URL in "${URLS[@]}"; do
    echo "  - $URL"
    # Extract protocol://domain (e.g., https://docs.fedoraproject.org)
    base=$(echo "$URL" | sed -E 's|(https?://[^/]+).*|\1|')
    allow_url_args+=("--allow-url" "$base")
done
for GIT_SOURCE in "${GIT_SOURCES[@]}"; do
    echo "  - $GIT_SOURCE"
done

echo ""
echo "Starting copilot review..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/spec_review_schema.py"

# Add validator tool to allowed tools
TOOLS+=("--allow-tool" "shell(${VALIDATOR}:*)")

# Prepare git sources in a temporary directory to allow copilot access
temp_sources_dir="$(mktemp -d -t spec_review_git_sources_XXXXXX)"
trap 'rm -rf "$temp_sources_dir"' EXIT SIGHUP SIGINT SIGTERM

git_folders=()
for GIT_SOURCE in "${GIT_SOURCES[@]}"; do
    git clone --depth 1 --single-branch "$GIT_SOURCE" "$temp_sources_dir/$(basename "$GIT_SOURCE" .git)"
    git_folders+=("$temp_sources_dir/$(basename "$GIT_SOURCE" .git)")
done
# Add git source folders to allow list
for folder in "${git_folders[@]}"; do
    allow_url_args+=("--add-dir" "$folder")
done
# Create key-value pairs of git URL to local folder for prompt
git_prompt=()
for i in "${!GIT_SOURCES[@]}"; do
    git_prompt+=("- ${GIT_SOURCES[i]} => ${git_folders[i]}")
done

allow_folders=("--add-dir" "$temp_sources_dir" "--add-dir" "$REPO_ROOT")
# For the kb and output, allow the parent folder as well
allow_folders+=("--add-dir" "$(dirname "$KNOWLEDGE_BASE")" "--add-dir" "$(dirname "$OUTPUT")")
mkdir -p "$(dirname "$KNOWLEDGE_BASE")" && mkdir -p "$(dirname "$OUTPUT")"

# In synthesis mode, allow access to input reports and KBs
if [[ "$SYNTHESIZE" == true ]]; then
    allow_folders+=("--add-dir" "$(dirname "$REPORT_A")" "--add-dir" "$(dirname "$REPORT_B")")
    [[ -n "$KB_A" ]] && allow_folders+=("--add-dir" "$(dirname "$KB_A")")
    [[ -n "$KB_B" ]] && allow_folders+=("--add-dir" "$(dirname "$KB_B")")
fi

# Ensure log file directory exists
mkdir -p "$(dirname "$LOG")"

# Build prompt based on mode
if [[ "$SYNTHESIZE" == true ]]; then
    # Synthesis mode: merge two reports
    kb_context=""
    if [[ -n "$KB_A" && -n "$KB_B" ]]; then
        kb_context="Reference knowledge bases ${KB_A} and ${KB_B} for guideline context."
    elif [[ -n "$KB_A" ]]; then
        kb_context="Reference knowledge base ${KB_A} for guideline context."
    elif [[ -n "$KB_B" ]]; then
        kb_context="Reference knowledge base ${KB_B} for guideline context."
    fi

    prompt="
SYNTHESIS MODE: Merge two spec review reports into a single consolidated report.

Input reports:
- Report A: ${REPORT_A}
- Report B: ${REPORT_B}

${kb_context}

Spec files for verification: ${SPEC_FILES[*]}
Guideline URLs (for reference): ${URLS[*]}
Guideline repos (cloned locally): ${git_prompt[*]}

Instructions:
1. Read both input reports and understand the findings from each reviewer.
2. Deduplicate findings semantically (e.g., 'missing BuildRequires' and 'BuildRequires is absent' are the same).
3. For conflicting severities (one says error, other says warning), use your judgment:
   - If the guideline clearly indicates it's blocking, promote to error.
   - If uncertain, keep as error (err on the side of caution).
4. Preserve the best/most specific citation for each finding.
5. Re-validate *EVERY* finding against the cited sources to ensure accuracy, fix any mistakes. Check the web sources again to confirm accuracy.
6. Write the merged report to ${OUTPUT}.
7. Store synthesis notes in ${KNOWLEDGE_BASE} for diagnostics.
8. Validate the final report by running: '${VALIDATOR} ${OUTPUT}' (Call verbatim, other commands will be blocked).

Model: ${MODEL}
"
else
    # Standard review mode
    prompt="
Review: ${SPEC_FILES[*]} against packaging guidelines from: ${URLS[*]} and ${git_prompt[*]}, place results in ${OUTPUT}.
Knowledge base: ${KNOWLEDGE_BASE}
Model: ${MODEL}
After writing the JSON report, validate it by running: '${VALIDATOR} ${OUTPUT}' (Call verbatim, other commands will be blocked).
"
fi
# Clean up any stale output file from a previous run to avoid file-creation conflicts
if [[ -f "$OUTPUT" ]]; then
    echo "Removing stale output file: $OUTPUT"
    rm -f "$OUTPUT"
fi

validation_output=""

# Create hint about available tools (just make a list without the --allow-tool prefix)
tool_hint=$(printf "%s\n" "${TOOLS[@]}" | grep -v '^--allow-tool$' | tr '\n' ',' | sed 's/,$//')
prompt+="
Tools that are pre-approved: ${tool_hint}
"

# Run the copilot agent — 4 total attempts (1 initial + 3 retries) if output validation fails
for run in {1..4}; do
    if [[ $run -gt 1 ]]; then
        echo "Retrying copilot review (attempt $run)..."
        # Use --continue to resume the previous session with additional guidance
        retry_prompt=""
        if [[ ! -f "$OUTPUT" ]]; then
            retry_prompt="The output file ${OUTPUT} was not created. You MUST complete ALL steps and write the JSON report to ${OUTPUT}, then validate with: ${VALIDATOR} ${OUTPUT}"
        else
            printf -v retry_prompt "The output file %s failed validation:\n%s\n\nPlease fix the issues and re-validate." "$OUTPUT" "$validation_output"
        fi

        copilot --agent "spec-review" \
            --model "$MODEL" \
            --continue \
            "${TOOLS[@]}" \
            "${allow_folders[@]}" \
            --share "$LOG" \
            "${allow_url_args[@]}" \
            -p "$retry_prompt"
    else
        copilot --agent "spec-review" \
            --model "$MODEL" \
            "${TOOLS[@]}" \
            "${allow_folders[@]}" \
            --share "$LOG" \
            "${allow_url_args[@]}" \
            -p "$prompt"
    fi

    # Validate the output report
    if [[ ! -f "$OUTPUT" ]]; then
        echo "Error: Spec review report not found at ${OUTPUT}" >&2
        continue
    fi

    validation_exit_code=0
    validation_output=$(python3 "${VALIDATOR}" "${OUTPUT}" 2>&1) || validation_exit_code=$?
    if [[ $validation_exit_code -ne 0 ]]; then
        echo "Spec review report validation failed:"
        echo "$validation_output"
        if [[ $run -eq 4 ]]; then
            echo "Error: All 4 attempts exhausted, spec review report validation still failing" >&2
            exit 1
        fi
    else
        echo "Spec review report validation succeeded."
        break
    fi
done

echo ""
echo "Spec review completed successfully. Report written to ${OUTPUT}"
echo "Knowledge base notes (for diagnostics) written to ${KNOWLEDGE_BASE}"
echo "Copilot session log written to ${LOG}"
echo ""
echo "To view/format results, use:"
echo "   jq . ${OUTPUT}"
echo "or"
echo "   python3 ${VALIDATOR} --all ${OUTPUT}"
