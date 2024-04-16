#!/bin/bash
set -o pipefail

# Setup RPM tools
source "$(git rev-parse --show-toplevel)"/toolkit/scripts/rpmops.sh

# Define directories to watch
SPEC_DIRS=("SPECS" "SPECS-EXTENDED")

# Initialize the variable to false
multi_package_add_remove_detected=false

# Fetch the latest state of the base branch
git fetch origin $GITHUB_BASE_REF

# Function to check for duplicate package names in a directory
check_multi_package_add_remove() {
    local DIR=$1
    echo "Checking directory: $DIR for duplicates..."
    # Array to hold package names
    declare -A package_counts
    # Loop through .spec files in the directory
    for spec_file in "$DIR"/*.spec; do
        if [ -e "$spec_file" ]; then # Check if the spec file exists
            # Extract package name from the spec file
            package_name=$(mariner_rpmspec -q --qf "%{NAME}\n" "$spec_file" 2>/dev/null)
            # Increment package name count
            ((package_counts[$package_name]++))
        fi
    done
    # Check for duplicates
    for package in "${!package_counts[@]}"; do
        if [ "${package_counts[$package]}" -gt 1 ]; then
            echo "Multi-package add/remove of .spec file detected: $package in $DIR"
            multi_package_add_remove_detected=true
        fi
    done
}

# Loop through directories
for spec_dir in "${SPEC_DIRS[@]}"; do
    # List of added or removed spec files in PR
    CHANGED_FILES=$(git diff --name-only --diff-filter=AD "origin/$GITHUB_BASE_REF" "HEAD" -- "$GITHUB_WORKSPACE/$spec_dir" | grep '.spec$')

    for file in $CHANGED_FILES; do
        dir_path=$(dirname "$file")
        # Check for duplicates in the directory
        check_multi_package_add_remove "$dir_path"
    done
done

# Print true or false based on detection of duplicates
echo $multi_package_add_remove_detected
