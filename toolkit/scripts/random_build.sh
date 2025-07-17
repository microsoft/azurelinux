#!/bin/bash

# Random build script for Azure Linux
# This script runs the build command a specified number of times with random package lists

set -e

# Predefined package lists
PACKAGE_LISTS=(
    "words vim emacs"
    "git dbus gh dnf emacs"
    "future python-zipp tcsh vim"
    "words vim librelp"
)

# Base build command
BASE_COMMAND='make build-packages REBUILD_TOOLS=y DAILY_BUILD_ID=lkg ENABLE_TELEMETRY=y OTEL_EXPORTER_OTLP_ENDPOINT="localhost:4317"'

# Function to display usage
usage() {
    echo "Usage: $0 <number_of_runs>"
    echo "  number_of_runs: Number of times to run the build with random package lists"
    echo ""
    echo "Available package lists:"
    for i in "${!PACKAGE_LISTS[@]}"; do
        echo "  $((i+1)): ${PACKAGE_LISTS[i]}"
    done
    echo ""
    echo "Example: $0 5"
    exit 1
}

# Function to get a random package list
get_random_package_list() {
    local num_lists=${#PACKAGE_LISTS[@]}
    local random_index=$((RANDOM % num_lists))
    echo "${PACKAGE_LISTS[random_index]}"
}

# Function to run a single build
run_build() {
    local run_number=$1
    local package_list=$2
    
    echo "=================================================="
    echo "Run #${run_number}"
    echo "Package list: ${package_list}"
    echo "=================================================="
    
    # Clean before building
    echo "Running 'make clean'..."
    make clean
    local clean_exit_code=$?
    if [ $clean_exit_code -ne 0 ]; then
        echo "Warning: 'make clean' failed with exit code: ${clean_exit_code}"
        echo "Continuing with build anyway..."
    fi
    echo ""
    
    # Execute the build command with the selected package list
    echo "Starting build..."
    eval "${BASE_COMMAND} SRPM_PACK_LIST=\"${package_list}\""
    
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "Run #${run_number} completed successfully"
    else
        echo "Run #${run_number} failed with exit code: ${exit_code}"
        return $exit_code
    fi
    
    echo ""
}

# Main script logic
main() {
    # Check if argument is provided
    if [ $# -ne 1 ]; then
        echo "Error: Number of runs not specified"
        usage
    fi
    
    # Validate the argument is a positive integer
    if ! [[ "$1" =~ ^[1-9][0-9]*$ ]]; then
        echo "Error: Number of runs must be a positive integer"
        usage
    fi
    
    local num_runs=$1
    local failed_runs=0
    
    echo "Starting random build script"
    echo "Number of runs: ${num_runs}"
    echo "Available package lists: ${#PACKAGE_LISTS[@]}"
    echo ""
    
    # Run the builds
    for ((i=1; i<=num_runs; i++)); do
        local selected_package_list=$(get_random_package_list)
        
        if ! run_build "$i" "$selected_package_list"; then
            ((failed_runs++))
            echo "Warning: Run #${i} failed, continuing with remaining runs..."
            echo ""
        fi
        
        # Add a small delay between runs
        if [ $i -lt $num_runs ]; then
            echo "Waiting 2 seconds before next run..."
            sleep 2
        fi
    done
    
    # Summary
    echo "=================================================="
    echo "Build Summary"
    echo "=================================================="
    echo "Total runs: ${num_runs}"
    echo "Successful runs: $((num_runs - failed_runs))"
    echo "Failed runs: ${failed_runs}"
    
    if [ $failed_runs -gt 0 ]; then
        echo ""
        echo "Warning: ${failed_runs} out of ${num_runs} runs failed"
        exit 1
    else
        echo ""
        echo "All runs completed successfully!"
        exit 0
    fi
}

# Run the main function with all arguments
main "$@"
