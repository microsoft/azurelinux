# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

function command_diff {
    local input_command
    local first_file_path
    local second_file_path

    input_command="$1"
    first_file_path="$2"
    second_file_path="$3"

    if ! diff <(eval "$input_command" "$first_file_path") <(eval "$input_command" "$second_file_path"); then
        echo "Comparison for command ($input_command) failed! See lines above for details." >&2
        return 1
    fi
}