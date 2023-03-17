# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

TEMP_DIR=""

command_diff() {
    local input_command
    local first_file_path
    local second_file_path

    input_command="$1"
    first_file_path="$2"
    second_file_path="$3"

    if ! diff <(eval "$input_command" "$first_file_path") <(eval "$input_command" "$second_file_path"); then
        echo "ERROR: comparison for command ($input_command) failed! See lines above for details." >&2
        return 1
    fi
}

find_file_fullpath() {
    local file_pattern
    local input_path
    local output_path

    input_path="$1"
    file_pattern="$2"

    output_path="$input_path"
    if [[ ! -f "$input_path" ]]
    then
        output_path="$(find "$input_path" -name "$file_pattern" -type f -print -quit)"
    fi

    if [[ -f "$output_path" ]]
    then
        realpath "$output_path"
    fi
}

temp_dir_cleanup() {
    if [[ -d "$TEMP_DIR" ]]
    then
        echo "Cleaning up '$TEMP_DIR'."
        rm -rf "$TEMP_DIR"
    fi
}
