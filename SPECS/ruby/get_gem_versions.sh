#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e
set -o pipefail

# A helpful one-liner script to check the current default versions
if [[ -z "$RUBY_VER" ]]; then
  echo "Need to run with RUBY_VER=?.?" 1>&2
  echo "    RUBY_VER=3.1 get_gem_versions.sh > versions.txt"
  exit 1
fi

# -get .json data
# - query each entry for its gem + version matchign $RUBY_VER
# - Print each array entry
# - put two per line using paste
# - add '_version' to each pkg
# - calc tab spacing
# - add %global to each line

curl https://stdgems.org/default_gems.json 2>/dev/null                | \
jq  '.gems[] | [.gem, .versions["'$RUBY_VER'"]] | select(.[1]!=null)' | \
jq -r '.[0], .[1]'                                                    | \
tr '-' '_'                                                            | \
paste -d " " - -                                                      | \
xargs printf '%s_version %s\n'                                        | \
column -t -n                                                          | \
awk '{print "%global " $0}'
