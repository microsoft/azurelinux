#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# It will check, for each spec file passed, that either the version or the release or both have been updated

# $1 - Branch to diff against
# $@:2 - Paths to spec files to check

[[ $# -eq 1 ]] && echo "No specs passed to validate"
git fetch origin $1

for spec in "${@:2}"
do
  echo Checking "$spec"

  # Ensure spec can be parsed
  name=$(rpmspec --srpm  --define "with_check 0" --qf "%{NAME}" -q $spec 2>/dev/null )
  if [[ -z $name ]]
  then
    echo "Not able to parse $spec, with_check 0, skipping" >> bad_specs.txt
    continue
  fi
  name=$(rpmspec --srpm  --define "with_check 1" --qf "%{NAME}" -q $spec 2>/dev/null )
  if [[ -z $name ]]
  then
    echo "Not able to parse $spec, with_check 1, skipping" >> bad_specs.txt
    continue
  fi

  git diff origin/$1 -- $spec > diff_content
  version_change="+Version"
  release_change="+Release"
  if grep -q $version_change diff_content || grep -q $release_change diff_content
  then
    echo "$spec: version and/or release changed"
  else
    echo "$spec was changed but neither version nor release changed" >> bad_specs.txt
  fi
done
rm -f diff_content

if [[ -s bad_specs.txt ]]
then
  echo "####"
  echo "Some spec file(s) may need to be updated..."
  echo "####"
  cat bad_specs.txt
  exit 1
fi
