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
    echo "[MANDATORY] -w WORKFLOW_RUN_URL -> URL of the workflow run that triggers this script"
}

function cherry_pick_from_pull_request {
    repo=$1
    pr_number=$2
    target_branch=$3
    workflow_run_url=$4

    # Collect merge commit hash and title from the original PR
    commit_hash=$(gh pr view $pr_number --repo $repo --json mergeCommit --jq '.mergeCommit.oid')
    original_pr_title=$(gh pr view $pr_number --repo $repo --json title --jq '.title')
    tmp_branch="cherry-pick-$target_branch-$commit_hash"

    echo "Cherry picking commit ($commit_hash) to target branch ($target_branch)"

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
            --body "Cherry-pick failed for branch \`$target_branch\`. See run logs for more details: $workflow_run_url"
        exit 1
    fi

    echo "Pushing to remote"
    git push -u origin "$tmp_branch"
    echo "Done pushing to remote"
    new_pr=$(gh pr create \
        -B "$target_branch" \
        -H "$tmp_branch" \
        --repo "$repo" \
        --title "[AUTO-CHERRY-PICK] $original_pr_title - branch $target_branch" \
        --body "This is an auto-generated pull request to cherry pick commit $commit_hash to $target_branch. Original PR: #$pr_number")
    gh pr comment "$pr_number" \
        --repo "$repo" \
        --body "Cherry-pick succeeded for branch \`$target_branch\`. See pull request #$new_pr"
    gh pr edit "$pr_number" \
        --repo "$repo" \
        --add-label "cherry_pick-$target_branch"
}

repo=
pr_number=
target_branch=
workflow_run_url=

while getopts "r:p:t:w:" opt; do
    case ${opt} in
    r ) repo="$OPTARG" ;;
    p ) pr_number="$OPTARG" ;;
    t ) target_branch="$OPTARG" ;;
    w ) workflow_run_url="${OPTARG,,}" ;;
    ? ) echo -e "ERROR: Invalid option.\n\n"; help; exit 1 ;;
    esac
done

if [[ -z "$repo" ]] || [[ -z "$pr_number" ]] || [[ -z "$target_branch" ]] || [[ -z "$workflow_run_url" ]] ; then
    echo "Error: missing required arguments"
    help
    exit 1
fi

cherry_pick_from_pull_request "$repo" "$pr_number" "$target_branch" "$workflow_run_url"
