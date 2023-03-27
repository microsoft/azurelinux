# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Extracts files from the specified RPM file.
# If no pattern is specified, all files are extracted.
#
# Arguments:
#
#  -f -> flatten the extracted files into the output directory
#        WARNING: this will overwrite files with the same name.
#  -i -> input RPM file.
#  -o -> output directory.
#  -p -> files pattern.
#        Default: '*'.
#  -w -> temporary work directory.
rpm_extract_file() {
    local files_pattern="*"
    local flatten
    local output_dir
    local rpm_name
    local rpm_path
    local work_dir

    local OPTIND
    while getopts "fi:o:p:w:" OPTIONS
    do
        case "${OPTIONS}" in
            f ) flatten=true ;;
            i ) rpm_path="$OPTARG" ;;
            o ) output_dir="$OPTARG" ;;
            p ) files_pattern="$OPTARG" ;;
            w ) work_dir="$OPTARG" ;;

            \? )
                echo "ERROR: Invalid Option: -$OPTARG" 1>&2
                exit 1
                ;;
            : )
                echo "ERROR: Invalid Option: -$OPTARG requires an argument" 1>&2
                exit 1
                ;;
        esac
    done

    if [[ ! -f "$rpm_path" ]]
    then
        echo "ERROR: RPM file ($rpm_path) not found." >&2
        return 1
    fi

    if [[ -z "$output_dir" ]]
    then
        echo "ERROR: output path not specified." >&2
        return 1
    fi

    if [[ -f "$output_dir" ]]
    then
        echo "ERROR: output path ($output_dir) is a file. Expected a directory or a non-existing path." >&2
        return 1
    fi

    rpm_name="$(basename "$rpm_path" .rpm)"

    if [[ ! -d "$work_dir" ]]
    then
        work_dir="$(mktemp -d)"
    fi
    work_dir="$work_dir/$rpm_name"
    mkdir -p "$work_dir"

    mkdir -p "$output_dir"

    echo "Extracting ($files_pattern) from ($rpm_path) into ($output_dir)."

    rpm2cpio "$rpm_path" | cpio --quiet -D "$work_dir" -idmv "$files_pattern"
    if $flatten
    then
        find "$work_dir" -name "$files_pattern" -exec mv -v {} "$output_dir" \;
    else
        mv "$work_dir" "$output_dir"
    fi
}

# Extracts files from the specified directory or RPM file.
# If no pattern is specified, all files are extracted.
# Arguments:
#  -f -> flatten the extracted files into the output directory
#        WARNING: this will overwrite files with the same name.
#  -i -> input directory or RPM file.
#  -o -> output directory.
#  -p -> files pattern.
#        Default: '*'.
#  -w -> temporary work directory.
rpm_extract_files() {
    local files_pattern="*"
    local flatten_arg
    local input
    local output_dir
    local output_subdir
    local rpm_name
    local rpm_path
    local work_dir

    local OPTIND
    while getopts "fi:o:p:w:" OPTIONS
    do
        case "${OPTIONS}" in
            f ) flatten_arg="-f" ;;
            i ) input="$OPTARG" ;;
            o ) output_dir="$OPTARG" ;;
            p ) files_pattern="$OPTARG" ;;
            w ) work_dir="$OPTARG" ;;

            \? )
                echo "ERROR: Invalid Option: -$OPTARG" 1>&2
                exit 1
                ;;
            : )
                echo "ERROR: Invalid Option: -$OPTARG requires an argument" 1>&2
                exit 1
                ;;
        esac
    done

    if [[ ! -d "$input" && ! -f "$input" ]]
    then
        echo "ERROR: input ($input) not found." >&2
        return 1
    fi

    if ! find "$input" -name "*.rpm" -type f -print0 | grep -q .
    then
        echo "ERROR: input ($input) is neither an RPM file nor a directory containing RPM files." >&2
        return 1
    fi

    while IFS= read -r -d '' rpm_path
    do
        rpm_name="$(basename "$rpm_path" .rpm)"
        output_subdir="$output_dir/$rpm_name"
        rpm_extract_file -i "$rpm_path" -p "$files_pattern" -w "$work_dir" -o "$output_subdir" $flatten_arg
    done < <(find "$input" -name "*.rpm" -type f -print0)
}
