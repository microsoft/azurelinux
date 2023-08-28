#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

function help {
    echo "Cherry-pick commit to a specific branch and create Github PR"
    echo "Usage:"
    echo "-b TARGET_BRANCH -> target branch to cherry pick commit to"
    echo "-c COMMIT_HASH"
    echo "-l LOG_FILE -> log file to output conflicts in case cherry-pick fails, or to output URL to new PR"
    echo "-o ORIGINAL_PR_URL -> original PR that triggers this script"
    echo "-r REPOSITORY -> name of the repository"
    echo "-t TITLE -> title of the original PR"
}

function cherry_pick {
    commit_hash=$1
    target_branch=$2
    log_file=$3
    pr_title=$4
    original_pr_url=$5
    repo=$6
    tmp_branch="cherry-pick-$target_branch-$commit_hash"

    echo "Commit hash = $commit_hash"
    echo "Target branch = $target_branch"

    git fetch --all
    git checkout -b "$tmp_branch" origin/"$target_branch"

    git cherry-pick -x "$commit_hash" || rc=$?
    if [ ${rc:-0} -ne 0 ]; then
        echo "Cherry pick failed. Displaying conflicts below"
        git diff --diff-filter=U
        exit 1
    else
        echo "pushing to remote"
        git push -u origin "$tmp_branch"
        echo "done pushing to remote"
        gh pr create \
            -B "$target_branch" \
            -H "$tmp_branch" \
            --repo $repo \
            --title "[AUTO-CHERRY-PICK] $pr_title - branch $target_branch" \
            --body "This is an auto-generated pull request to cherry pick commit $commit_hash to $target_branch. Original PR: $original_pr_url" \
            > $log_file
    fi
}

commit_hash=
target_branch=
original_pr_url=
log_file=
repo=
pr_title=

while getopts "b:c:l:o:r:t:" opt; do
    case ${opt} in
    b ) target_branch="$OPTARG" ;;
    c ) commit_hash="$OPTARG" ;;
    l ) log_file="$OPTARG" ;;
    o ) original_pr_url="$OPTARG" ;;
    r ) repo="$OPTARG" ;;
    t ) pr_title="${OPTARG,,}" ;;
    ? ) echo -e "ERROR: Invalid option.\n\n"; help; exit 1 ;;
    esac
done

if [[ -z "$commit_hash" ]] || [[ -z "$target_branch" ]]; then
    echo -e "Error: arguments -c and -b are required"
    help
    exit 1
fi

cherry_pick "$commit_hash" "$target_branch" "$log_file" "$pr_title" "$original_pr_url" "$repo"
