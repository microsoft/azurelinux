#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

shell_link_path="/bin/sh"

if [[ -f "$shell_link_path" ]]
then
  original_rpm_shell="$(readlink $shell_link_path)"
fi

if [[ "$original_rpm_shell" != "bash" ]]
then
  echo "Host system's '/bin/sh' links to '$RPM_SHELL'. Mariner specs require 'bash' - updating."

  rm -f $shell_link_path
  ln -s bash "$shell_link_path"
fi
