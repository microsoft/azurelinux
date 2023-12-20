#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Best effort validation of the package cgmanifest. It will check, for each spec file passed, that:
#
#   - The registration for the package name/version is in the cgmanifest
#   - The source0 basename (not full URL) is a substring of the cgmanifest URL
#     - OR that a #source0 comment is a substring of the cgmanifest URL
#   - The URL listed in the cgmanifets is valid (can be downloaded)

# $@ - Paths to spec files to check

# shellcheck source=../../toolkit/scripts/rpmops.sh
source "$(git rev-parse --show-toplevel)"/toolkit/scripts/rpmops.sh

# Specs, which contain multiple source files and are split into many entries inside 'cgmanifest.json'.
ignore_multiple_sources=" \
  xorg-x11-apps \
  xorg-x11-font-utils \
  xorg-x11-server-utils \
  xorg-x11-xkb-utils"

# List of ignored specs due to no source tarball to scan.
ignore_no_source_tarball=" \
  ca-certificates \
  check-restart \
  core-packages \
  dbus-x11 \
  ghc-srpm-macros \
  hunspell-nl \
  hunspell-ru \
  hyphen-grc \
  hyphen-hsb \
  hyphen-lt \
  hyphen-mn \
  initramfs \
  installkernel \
  javapackages-tools-meta \
  kata-packages-uvm \
  kde-filesystem \
  kf5 \
  livepatching \
  lua-rpm-macros \
  mariner-repos \
  mariner-rpm-macros \
  multilib-rpm-config \
  opencl-filesystem \
  patterns-ceph-containers \
  pyproject-rpm-macros \
  qt5-rpm-macros \
  verity-read-only-root \
  web-assets \
  sgx-backwards-compatability \
  "

# Specs where cgmanifest validation has known issues checking URLs.
ignore_known_issues=" \
  virglrenderer \
  libesmtp"

alt_source_tag="Source9999"

function prepare_lua {
  local -a dirs_to_check
  local lua_common_file_name
  local lua_forge_file_name
  local mariner_lua_dir
  local mariner_srpm_lua_dir
  local rpm_lua_dir
  local rpm_macros_dir

  rpm_macros_dir="$1"

  lua_common_file_name="common.lua"
  lua_forge_file_name="forge.lua"
  rpm_lua_dir="$(rpm --eval "%_rpmluadir")"
  mariner_lua_dir="$rpm_lua_dir/mariner"
  mariner_srpm_lua_dir="$mariner_lua_dir/srpm"

  if [[ -z "$rpm_lua_dir" ]]
  then
    echo "ERROR: no RPM LUA directory set, can't update with Mariner's LUA modules!" >&2
    exit 1
  fi

  # We only want to clean-up directories, which were absent from the system.
  dirs_to_check=("$rpm_lua_dir" "$mariner_lua_dir" "$mariner_srpm_lua_dir")
  for dir_path in "${dirs_to_check[@]}"
  do
    if [[ ! -d "$dir_path" ]]
    then
      FILES_TO_CLEAN_UP+=("$dir_path")
      break
    fi
  done
  sudo mkdir -p "$mariner_srpm_lua_dir"

  if [[ ! -f "$mariner_lua_dir/$lua_common_file_name" ]]
  then
    sudo cp "$rpm_macros_dir/$lua_common_file_name" "$mariner_lua_dir/$lua_common_file_name"
    FILES_TO_CLEAN_UP+=("$mariner_lua_dir/$lua_common_file_name")
  fi

  if [[ ! -f "$mariner_srpm_lua_dir/$lua_forge_file_name" ]]
  then
    sudo cp "$rpm_macros_dir/$lua_forge_file_name" "$mariner_srpm_lua_dir/$lua_forge_file_name"
    FILES_TO_CLEAN_UP+=("$mariner_srpm_lua_dir/$lua_forge_file_name")
  fi
}

function specs_dir_from_spec_path {
  # Assuming we always check specs inside CBL-Mariner's core GitHub repository.
  # If that's the case, the spec paths will always have the following form:
  #     [repo_directory_path]/[specs_directory]/[package_name]/[package_spec_files]
  echo "$(realpath "$(dirname "$1")/../../SPECS")/mariner-rpm-macros"
}

rm -f bad_registrations.txt
rm -rf ./cgmanifest_test_dir/

if [[ $# -eq 0 ]]
then
  echo "No specs passed to validate."
  exit
fi

WORK_DIR=$(mktemp -d -t)
FILES_TO_CLEAN_UP=("$WORK_DIR")
function clean_up {
    echo "Cleaning up..."
    for file_path in "${FILES_TO_CLEAN_UP[@]}"
    do
      echo "   Removing ($file_path)."
      sudo rm -rf "$file_path"
    done
}
trap clean_up EXIT SIGINT SIGTERM


mariner_macros_dir="$(specs_dir_from_spec_path "$1")"
prepare_lua "$mariner_macros_dir"

echo "Checking $# specs."

i=0
for original_spec in "$@"
do
  i=$((i+1))
  echo "[$i/$#] Checking $original_spec"

  # Using a copy of the spec file, because parsing requires some pre-processing.
  original_spec_dir_path="$(dirname "$original_spec")"
  cp -r "$original_spec_dir_path" "$WORK_DIR"

  original_spec_dir_name="$(basename "$original_spec_dir_path")"
  spec="$WORK_DIR/$original_spec_dir_name/$(basename "$original_spec")"

  # Skipping specs for signed packages. Their unsigned versions should already be included in the manifest.
  if echo "$original_spec" | grep -q "SPECS-SIGNED"
  then
    echo "    $spec is being ignored (reason: signed package), skipping"
    continue
  fi

  # Pre-processing alternate sources (commented-out "Source" lines with full URLs), if present. Currently we only care about the first source.
  # First, we replace "%%" with "%" in the alternate source's line.
  sed -Ei "/^#\s*Source0?:.*%%.*/s/%%/%/g" "$spec"
  # Then we uncomment it.
  sed -Ei "s/^#\s*Source0?:/$alt_source_tag:/" "$spec"

  # Removing trailing comments from "Source" tags.
  sed -Ei "s/^(\s*Source[0-9]*:.*)#.*/\1/" "$spec"

  name=$(mariner_rpmspec --srpm --qf "%{NAME}" -q "$spec" 2>/dev/null)
  if [[ -z $name ]]
  then
    echo "Failed to get name from '$original_spec'. Please update the spec or the macros from the 'defines' variable in this script. Error:" >> bad_registrations.txt
    mariner_rpmspec --srpm --qf "%{NAME}" -q "$spec" &>> bad_registrations.txt
    continue
  fi

  # Skipping specs from the ignore lists.
  if echo "$ignore_multiple_sources $ignore_no_source_tarball $ignore_known_issues" | grep -qP "(^|\s)$name($|\s)"
  then
    echo "    $name is being ignored (reason: explicitly ignored package), skipping"
    continue
  fi

  version=$(mariner_rpmspec --srpm --qf "%{VERSION}" -q "$spec" 2>/dev/null )
  if [[ -z $version ]]
  then
    echo "Failed to get version from '$original_spec'. Please update the spec or the macros from the 'defines' variable in this script. Error:" >> bad_registrations.txt
    mariner_rpmspec --srpm --qf "%{VERSION}" -q "$spec" &>> bad_registrations.txt
    continue
  fi

  parsed_spec="$(mariner_rpmspec --parse "$spec" 2>/dev/null)"

  # Reading the source0 file/URL.
  source0=$(echo "$parsed_spec" | grep -P "^\s*Source0?:" | cut -d: -f2- | xargs)
  if [[ -z $source0 ]]
  then
    echo "    No source file listed for $name:$version, skipping"
    continue
  fi

  # Reading the alternate source URL.
  source0alt=$(echo "$parsed_spec" | grep -P "^\s*$alt_source_tag:" | cut -d: -f2- | xargs)

  # Pull the current registration from the cgmanifest file. Every registration should have a URL, so if we don't find one
  # that implies the registration is missing.
  manifesturl=$(jq --raw-output ".Registrations[].component.other | select(.name==\"$name\" and .version==\"$version\") | .downloadUrl" cgmanifest.json)
  if [[ -z $manifesturl ]]
  then
    echo "Registration for $name:$version is missing" >> bad_registrations.txt
  else
    if [[ "$manifesturl" != "$source0" && "$manifesturl" != "$source0alt" ]]
    then
      {
        echo "Registration URL for $name:$version ($manifesturl) matches neither the first \"Source\" tag nor the alternate source URL."
        printf '\tFirst "Source" tag:\t%s\n' "$source0"
        printf '\tAlternate source URL:\t%s\n' "$source0alt"
      } >> bad_registrations.txt
    else
      # Try a few times to download the source listed in the manifest
      # Parsing output instead of using error codes because 'wget' returns code 8 for FTP, even if the file exists.
      # Sample HTTP(S) output:  Remote file exists.
      # Sample FTP output:      File ‘time-1.9.tar.gz’ exists.
      if ! wget --secure-protocol=TLSv1_2 --spider --timeout=2 --tries=10 "${manifesturl}" 2>&1 | grep -qP "^(Remote file|File ‘.*’) exists.*"
      then
        echo "Registration for $name:$version has invalid URL '$manifesturl' (could not download)"  >> bad_registrations.txt
      fi
    fi
  fi
done

if [[ -s bad_registrations.txt ]]
then
  echo "####"
  echo "Found errors while analyzing modified spec files, cgmanifest.json may need to be updated."
  echo "####"
  cat bad_registrations.txt
  exit 1
fi
