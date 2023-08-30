#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

function help {
    echo "Cherry-pick commit to a specific branch and create Github PR"
    echo "Usage:"
    echo "[MANDATORY] -r REPOSITORY -> name of the repository in the format <owner>/<repo-name>"
    echo "[MANDATORY] -p PR_NUMBER -> number of the PR to cherry-pick commit from"
    echo "[MANDATORY] -t TARGET_BRANCH -> target branch to cherry-pick commit to"
}

function collect_pr_info {
    repo=$1
    pr_number=$2

    commit_hash=$(gh pr view $pr_number --repo $repo --json mergeCommit --jq '.mergeCommit.oid')
    original_pr_title=$(gh pr view $pr_number --repo $repo --json title --jq '.title')
}

function cherry_pick {
    commit_hash=$1
    target_branch=$2
    repo=$3
    pr_number=$4
    original_pr_title=$5

    tmp_branch="cherry-pick-$target_branch-$commit_hash"

    echo "Cherry picking commit ($commit_hash) to target branch $target_branch"

    # reset the current working tree to clean state
    git reset --hard
    git clean -df
    git checkout -- .

    # create a temporary branch from target branch to perform cherry pick
    git fetch --all
    git checkout -b "$tmp_branch" origin/"$target_branch"

    if ! git cherry-pick -x "$commit_hash"; then
        echo "Cherry pick failed. Displaying conflicts below"
        git diff --diff-filter=U
        gh pr comment "$pr_number" \
            --repo "$repo" \
            --body "Cherry-pick failed for branch \`$target_branch\`. See run logs for more details: $RUN_URL"
        exit 1
    else
        echo "pushing to remote"
        git push -u origin "$tmp_branch"
        echo "done pushing to remote"
        new_pr=$(gh pr create \
            -B "$target_branch" \
            -H "$tmp_branch" \
            --repo "$repo" \
            --title "[AUTO-CHERRY-PICK] $pr_title - branch $target_branch" \
            --body "This is an auto-generated pull request to cherry pick commit $commit_hash to $target_branch. Original PR: #$pr_number")
        gh pr comment "$pr_number" \
            --repo "$repo" \
            --body "Cherry-pick succeeded for branch \`$target_branch\`. See pull request #$new_pr"
    fi
}

repo=
pr_number=
target_branch=

while getopts "r:p:t:d:" opt; do
    case ${opt} in
    r ) repo="$OPTARG" ;;
    p ) pr_number="$OPTARG" ;;
    t ) target_branch="$OPTARG" ;;
    ? ) echo -e "ERROR: Invalid option.\n\n"; help; exit 1 ;;
    esac
done

if [[ -z "$repo" ]] || [[ -z "$pr_number" ]] || [[ -z "$target_branch" ]]; then
    echo -e "Error: missing required arguments"
    help
    exit 1
fi

collect_pr_info "$repo" "$pr_number"
cherry_pick "$commit_hash" "$target_branch" "$repo" "$pr_number" "$original_pr_title"
echo "================================================================================"
echo "================================================================================"
