#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Best effort validation of the package cgmanifest. It will check, for each spec file passed, that:
#
#   - The registration for the package name/version is in the cgmanifest
#   - The source0 basename (not full URL) is a substring of the cgmanifest URL
#     - OR that a #source0 comment is a substring of the cgmanifest URL
#   - The URL listed in the cgmanifets is valid (can be downloaded)

# $1 - Path to worker chroot's archive
# $2+ - Paths to spec files to check

set -euo pipefail

# Specs, which contain multiple source files and are split into many entries inside 'cgmanifest.json'.
ignore_multiple_sources=" \
  xorg-x11-apps \
  xorg-x11-font-utils \
  xorg-x11-server-utils \
  xorg-x11-xkb-utils"

# List of ignored specs due to no source tarball to scan.
ignore_no_source_tarball=" \
  azurelinux-repos \
  azurelinux-rpm-macros \
  azurelinux-sysinfo \
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
  javapackages-tools-meta \
  kata-packages-uvm \
  kde-filesystem \
  kernel-uki \
  kf \
  livepatching \
  lua-rpm-macros \
  ocaml-srpm-macros \
  opencl-filesystem \
  patterns-ceph-containers \
  pyproject-rpm-macros \
  python-rpm-generators \
  qt-rpm-macros \
  sgx-backwards-compatibility \
  shim \
  web-assets \
  "

alt_source_tag="Source9999"

chroot_rpmspec() {
  local chroot_dir_path
  local sourcedir

  chroot_dir_path="$1"
  shift

  if [[ ! -d "$chroot_dir_path" ]]; then
    echo "Expected a chroot directory as first argument to 'chroot_rpmspec'. Got '$chroot_dir_path'." >&2
    return 1
  fi

  # Looking for spec path in the argument list to extract its directory.
  sourcedir=""
  for arg in "$@"; do
    if [[ "$arg" == *.spec && -f "$chroot_dir_path/$arg" ]]; then
      sourcedir="$(dirname "$arg")"
      break
    fi
  done

  if [[ -z $sourcedir ]]; then
    echo "Must pass valid spec path to 'chroot_rpmspec'!" >&2
    return 1
  fi

  sudo chroot "$chroot_dir_path" rpmspec -D "_sourcedir $sourcedir" "$@"
}

prepare_chroot_environment() {
  local chroot_archive
  local chroot_dir_path
  local chroot_rpm_macros_dir_path
  local dist_name
  local dist_number
  local dist_tag
  local rpm_macros_dir_path

  chroot_archive="$1"
  chroot_dir_path="$2"

  echo "Creating worker chroot under '$chroot_dir_path'."

  sudo tar -xf "$chroot_archive" -C "$chroot_dir_path"
  sudo chown -R "$(id -u):$(id -g)" "$chroot_dir_path"

  rpm_macros_dir_path="$(sudo chroot "$chroot_dir_path" rpm --eval '%{_rpmmacrodir}')"
  echo "Creating the RPM macros directory '$rpm_macros_dir_path' in the chroot."
  chroot_rpm_macros_dir_path="$chroot_dir_path/$rpm_macros_dir_path"
  mkdir -vp "$chroot_rpm_macros_dir_path"

  echo "Setting RPM's macros for the RPM queries inside the new chroot:"
  dist_tag=$(make -sC toolkit get-dist-tag)
  # Dist name is extracted from the dist tag by removing the leading dot and the number suffix.
  # Example: ".azl3" -> "azl"
  dist_name="$(sed -E 's/^\.(.*)[0-9]+$/\1/' <<<"$dist_tag")"
  # Dist number is the number suffix of the dist tag.
  # Example: ".azl3" -> "3"
  dist_number="$(grep -oP "\d+$" <<<"$dist_tag")"
  echo "%dist $dist_tag" | tee "$chroot_rpm_macros_dir_path/macros.dist"
  echo "%$dist_name $dist_number" | tee -a "$chroot_rpm_macros_dir_path/macros.dist"
  echo "%with_check 1" | tee -a "$chroot_rpm_macros_dir_path/macros.dist"
  for macro_file in SPECS/azurelinux-rpm-macros/macros* SPECS/pyproject-rpm-macros/macros.pyproject SPECS/perl/macros.perl; do
    sudo cp -v "$macro_file" "$chroot_rpm_macros_dir_path"
  done

  make -sC generate-versions-macros-file
  echo "Copying the version/release macros file to the chroot."
  sudo cp -v "build/pkg_artifacts/macros.releaseversions" "$chroot_rpm_macros_dir_path"

  echo
}

if [[ $# -lt 2 ]]; then
  echo "No specs passed to validate."
  exit 1
fi

if [[ ! -f "$1" ]]; then
  echo "First argument is not a valid file. Please pass the path to the worker chroot's archive."
  exit 1
fi

rm -f bad_registrations.txt

WORK_DIR=$(mktemp -d -t)
function clean_up {
  echo "Removing the temporary directory '$WORK_DIR'."
  rm -rf "$WORK_DIR"
}
trap clean_up EXIT SIGINT SIGTERM

prepare_chroot_environment "$1" "$WORK_DIR"

shift # Remove the first argument (the chroot archive) from the list of specs to check.
echo "Checking $# specs."

i=0
for original_spec in "$@"; do
  i=$((i + 1))
  echo "[$i/$#] Checking $original_spec."
  # Using a copy of the spec file, because parsing requires some pre-processing.
  original_spec_dir_path="$(dirname "$original_spec")"
  cp -r "$original_spec_dir_path" "$WORK_DIR"

  original_spec_dir_name="$(basename "$original_spec_dir_path")"
  chroot_spec="$original_spec_dir_name/$(basename "$original_spec")"
  host_spec="$WORK_DIR/$chroot_spec"

  # Skipping specs for signed packages. Their unsigned versions should already be included in the manifest.
  if echo "$original_spec" | grep -q "SPECS-SIGNED"; then
    echo "    $host_spec is being ignored (reason: signed package), skipping."
    continue
  fi

  # Pre-processing alternate sources (commented-out "Source" lines with full URLs), if present. Currently we only care about the first source.
  # First, we replace "%%" with "%" in the alternate source's line.
  sed -Ei "/^#\s*Source0?:.*%%.*/s/%%/%/g" "$host_spec"
  # Then we uncomment it.
  sed -Ei "s/^#\s*Source0?:/$alt_source_tag:/" "$host_spec"

  # Removing trailing comments from "Source" tags.
  sed -Ei "s/^(\s*Source[0-9]*:.*)#.*/\1/" "$host_spec"

  name=$(chroot_rpmspec "$WORK_DIR" --srpm --qf "%{NAME}" -q "$chroot_spec" 2>/dev/null)
  if [[ -z $name ]]; then
    echo "Failed to get name from '$original_spec'. Please update the spec or the chroot macros configuration in this script. Error:" >>bad_registrations.txt
    chroot_rpmspec "$WORK_DIR" --srpm --qf "%{NAME}" -q "$chroot_spec" &>>bad_registrations.txt
    continue
  fi

  # Skipping specs from the ignore lists.
  if echo "$ignore_multiple_sources $ignore_no_source_tarball" | grep -qP "(^|\s)$name($|\s)"; then
    echo "    $name is being ignored (reason: explicitly ignored package), skipping."
    continue
  fi

  version=$(chroot_rpmspec "$WORK_DIR" --srpm --qf "%{VERSION}" -q "$chroot_spec" 2>/dev/null)
  if [[ -z $version ]]; then
    echo "Failed to get version from '$original_spec'. Please update the spec or the chroot macros configuration in this script. Error:" >>bad_registrations.txt
    chroot_rpmspec "$WORK_DIR" --srpm --qf "%{VERSION}" -q "$chroot_spec" &>>bad_registrations.txt
    continue
  fi

  parsed_spec="$WORK_DIR/parsed.spec"
  chroot_rpmspec "$WORK_DIR" --parse "$chroot_spec" 2>/dev/null > "$parsed_spec"

  # Reading the source0 file/URL.
  if ! grep -qP "^\s*Source0?:" "$parsed_spec"; then
    echo "    No source file listed for $name-$version, skipping."
    continue
  fi

  source0=$(grep -P "^\s*Source0?:"  "$parsed_spec" | cut -d: -f2- | xargs)
  echo "    Source0: $source0."

  # Reading the alternate source URL.
  source0_alt=""
  if grep -qP "^\s*$alt_source_tag:"  "$parsed_spec"; then
    source0_alt=$(grep -P "^\s*$alt_source_tag:"  "$parsed_spec" | cut -d: -f2- | xargs)
    echo "    Source0Alt: $source0_alt."
  fi

  # Pull the current registration from the cgmanifest file. Every registration should have a URL, so if we don't find one
  # that implies the registration is missing.
  manifest_url=$(jq --raw-output ".Registrations[].component.other | select(.name==\"$name\" and .version==\"$version\") | .downloadUrl" cgmanifest.json)
  if [[ -z $manifest_url ]]; then
    echo "Registration for $name-$version is missing" >>bad_registrations.txt
  else
    echo "    Registration URL: $manifest_url."

    if [[ "$manifest_url" != "$source0" && "$manifest_url" != "$source0_alt" ]]; then
      {
        echo "Registration URL for $name-$version ($manifest_url) matches neither the first \"Source\" tag nor the alternate source URL."
        printf '\tFirst "Source" tag:\t%s\n' "$source0"
        printf '\tAlternate source URL:\t%s\n' "$source0_alt"
      } >>bad_registrations.txt
    else
      # Try a few times to download the source listed in the manifest
      # Parsing output instead of using error codes because 'wget' returns code 8 for FTP, even if the file exists.
      # Sample HTTP(S) output:  Remote file exists.
      # Sample FTP output:      File ‘time-1.9.tar.gz’ exists.
      if ! wget --secure-protocol=TLSv1_2 --spider --timeout=30 --tries=10 "${manifest_url}" 2>&1 | grep -qP "^(Remote file|File ‘.*’) exists.*"; then
        echo "Registration for $name-$version has invalid URL '$manifest_url' (could not download)" >>bad_registrations.txt
      fi
    fi
  fi
done

if [[ -s bad_registrations.txt ]]; then
  echo "####"
  echo "Found errors while analyzing modified spec files, cgmanifest.json may need to be updated."
  echo "####"
  cat bad_registrations.txt
  exit 1
fi
