# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

rpm_extract_files() {
    local files_pattern
    local rpm_name
    local rpm_path
    local workspace_dir

    rpm_path="$1"
    files_pattern="$2"
    workspace_dir="$3"

    rpm_name="$(basename "$rpm_path" .rpm)"

    if [[ ! -f "$rpm_path" ]]; then
        echo "ERROR: package RPMs ($rpm_path) not found." >&2
        return 1
    fi

    if [[ ! -d "$workspace_dir" ]]; then
        workspace_dir="$(mktemp -d)"
    fi

    workspace_dir="$workspace_dir/$rpm_name"
    mkdir -p "$workspace_dir"

    echo "Extracting ($files_pattern) from ($rpm_path) inside ($workspace_dir)."

    rpm2cpio "$rpm_path" | cpio --quiet -D "$workspace_dir" -idmv "$files_pattern"
    find "$workspace_dir" -name "$files_pattern" -exec mv -v {} . \;
}
