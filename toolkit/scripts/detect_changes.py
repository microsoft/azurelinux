#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import logging
import os
import subprocess
import sys

from typing import Sequence

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Detect changes in the repository")
parser.add_argument("--display-compare-ref", dest="display_compare_ref", action="store_true", help="Display the detected comparison ref and exit")
parser.add_argument("--since", dest="compare_ref", required=False, help="Identifies the git ref to compare against")
parser.add_argument("-t", "--target-ref", dest="target_ref", default="HEAD", help="Identifies the target git ref with changes")
parser.add_argument("-u", "--include-uncommitted", dest="include_uncommitted", action="store_true", help="Include uncommitted files from working tree")
parser.add_argument("--include-untracked", dest="include_untracked", action="store_true", help="Include untracked files in working tree")
parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Enable verbose output")

spec_options = parser.add_mutually_exclusive_group()
spec_options.add_argument("-s", "--spec-names", dest="spec_names_only", action="store_true", help="Only detect changes in SPECS .spec files and print out their base names")
spec_options.add_argument("-e", "--extended-spec-names", dest="extended_spec_names_only", action="store_true", help="Only detect changes in SPECS-EXTENDED .spec files and print out their base names")

args = parser.parse_args()

if args.verbose:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

def autodetect_compare_ref(target_ref: str) -> str:
    # Find the registered remotes
    result = subprocess.run(["git", "remote"], capture_output=True, check=True)
    remotes = result.stdout.decode("utf-8").splitlines()

    # Find all branches.
    git_args = ["git", "for-each-ref", "refs/heads/"]
    for remote in remotes:
        git_args.append(f"refs/remotes/{remote}/")
    git_args.append("--format=%(refname)")
    result = subprocess.run(git_args, capture_output=True, check=True)
    branch_refs = result.stdout.decode("utf-8").splitlines()    

    # Find the branches that look like official release or dev branches.
    well_known_refs = [branch_ref for branch_ref in branch_refs if is_well_known_azlinux_branch_ref(branch_ref)]

    # Figure out which of these branches is our closest ancestor.
    return get_closest_git_ancestor(target_ref, well_known_refs)

def is_well_known_azlinux_branch_ref(branch_ref: str) -> bool:
    branch_pieces = branch_ref.split("/")
    if not branch_pieces:
        return False

    if len(branch_pieces) < 3:
        return False

    # We only look at refs/heads/* and refs/remotes/*/*.
    if branch_pieces[0] != "refs":
        return False

    if branch_pieces[1] == "heads":
        # Look past ref/heads prefix.
        branch_name_pieces = branch_pieces[2:]
    elif branch_pieces[1] == "remotes":
        # Look past ref/remotes prefix as well as past the remote name.
        branch_name_pieces = branch_pieces[3:]

    # We only know about fasttrack/<ver>[-dev] and <ver>[-dev] named branches (and "main" as the legacy form of the 2.0 dev branch).
    if len(branch_name_pieces) == 2 and branch_name_pieces[0] == "fasttrack":
        name_to_check = branch_name_pieces[1]
    elif len(branch_name_pieces) == 1:
        name_to_check = branch_name_pieces[0]
    else:
        return False

    return name_to_check == "main" or name_to_check.endswith(".0") or name_to_check.endswith(".0-dev")

def get_closest_git_ancestor(target_ref: str, refs: Sequence[str]) -> str:
    # First filter down to fork points.
    fork_points = {}
    for ref in refs:
        result = subprocess.run(["git", "merge-base", "--fork-point", ref, target_ref], capture_output=True)
        if result.returncode == 0:
            fork_point_ref = result.stdout.decode("utf-8").strip()
            fork_points[ref] = fork_point_ref

    best_distance = None
    best_candidate_ref = None

    for candidate_ancestor, fork_point in fork_points.items():
        # Find the distance in the chain.
        result = subprocess.run(["git", "rev-list", "--count", f"{fork_point}..{target_ref}"], capture_output=True, check=True)
        distance = int(result.stdout.decode("utf-8").strip())

        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_candidate_ref = candidate_ancestor
        
    return best_candidate_ref

# If a comparison ref wasn't provided, then we go into auto-detect mode.
if not args.compare_ref:
    args.compare_ref = autodetect_compare_ref(args.target_ref)
    if not args.compare_ref:
        logger.error("could not autodetect comparison branch")
        sys.exit(1)

# If requested, display the comparison ref and then exit.
if args.display_compare_ref:
    print(args.compare_ref)
    sys.exit(0)

# Log output
logger.debug(f"comparing against ref: {args.compare_ref}")

# Try to find the files changed since the reference ref.
if args.include_uncommitted:
    if args.target_ref != "HEAD":
        logger.error("cannot include uncommitted files when target ref is not HEAD")
        sys.exit(1)

    git_cmd = ["git", "diff-index", "--name-only", args.compare_ref]
else:
    git_cmd = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", args.compare_ref, args.target_ref]

result = subprocess.run(git_cmd, capture_output=True, check=True)
changed_files = result.stdout.decode("utf-8").splitlines()

# If requested, look for untracked files.
if args.include_untracked:
    # This is not compatible with a target ref other than HEAD.
    if args.target_ref != "HEAD":
        logger.error("cannot include untracked files when target ref is not HEAD")
        sys.exit(1)

    result = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, check=True)
    changed_files.extend(result.stdout.decode("utf-8").splitlines())

# Identify any base dir filter.
if args.spec_names_only:
    base_dir = "SPECS/"
elif args.extended_spec_names_only:
    base_dir = "SPECS-EXTENDED/"
else:
    base_dir = None

for changed_file in changed_files:
    # If a base dir filter is provided, then apply it.
    if base_dir is not None and not changed_file.startswith(base_dir):
        continue

    # If requested, filter out non-spec files.
    if args.spec_names_only or args.extended_spec_names_only:
        if not changed_file.endswith(".spec"):
            continue

        filename = os.path.basename(changed_file)
        base_name = os.path.splitext(filename)[0]

        print(base_name)
    else:
        print(changed_file)

# Log output
if args.verbose:
    logger.debug(f"found {len(changed_files)} changed files")
