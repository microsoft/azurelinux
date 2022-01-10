#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Best effort validation of the package cgmanifest. It will check, for each spec file passed, that:
#
#   - The registration for the package name/version is in the cgmanifest
#   - The source0 basename (not full url) is a substring of the cgmanifest url
#     - OR that a #source0 comment is a substring of the cgmanifest url
#   - The URL listed in the cgmanifets is valid (can be downloaded)

# $@ - Paths to spec files to check

# Ignore some specs, mostly those with Source0 files that are not from an external source, or have very odd URLs
ignore_list=" \
  appstream-data \
  byacc \
  ca-certificates \
  Cython \
  dbus-x11 \
  grub2-efi-binary-signed-aarch64 \
  grub2-efi-binary-signed-x86_64 \
  initramfs \
  installkernel \
  kde-filesystem \
  kernel-signed-aarch64 \
  kernel-signed-x86_64 \
  kf5 \
  lcms2 \
  mariner-repos \
  mariner-rpm-macros \
  moby-buildx \
  moby-containerd \
  multilib-rpm-config \
  opencl-filesystem \
  openjdk8 \
  patterns-ceph-containers \
  python-markupsafe \
  python-nocasedict \
  python-pywbem \
  python-repoze-lru \
  python-requests \
  python-sphinxcontrib-websupport \
  python-yamlloader \
  python-zope-interface \
  qt5-rpm-macros \
  runc \
  sgabios \
  shim \
  verity-read-only-root \
  web-assets \
  xmvn \
  xorg-x11-apps \
  xorg-x11-font-utils \
  xorg-x11-server-utils \
  xorg-x11-xkb-utils"

rm -f bad_registrations.txt
rm -rf ./cgmanifest_test_dir/

[[ $# -eq 0 ]] && echo "No specs passed to validate"

for spec in "$@"
do
  echo Checking "$spec"

  # Additional macros required to parse some spec files.
  spec_dir="$(dirname "$spec")"
  defines=(-D "forgemeta %{nil}" -D "py3_dist X" -D "with_check 0" -D "dist .cm2" -D "__python3 python3" -D "_sourcedir $spec_dir" -D "fillup_prereq fillup")

  name=$(rpmspec --srpm  "${defines[@]}" --qf "%{NAME}" -q "$spec" 2>/dev/null)
  if [[ -z $name ]]
  then
    echo "Failed to get name from '$spec'. Please update the spec or the macros from the 'defines' variable in this script. Error:" >> bad_registrations.txt
    rpmspec --srpm  "${defines[@]}" --qf "%{NAME}" -q "$spec" &>> bad_registrations.txt
    continue
  fi

  # Some specs don't make sense to add, ignore them
  if echo "$ignore_list" | grep -w "$name" > /dev/null
  then
    echo "    $name is being ignored, skipping"
    continue
  fi

  version=$(rpmspec --srpm  "${defines[@]}" --qf "%{VERSION}" -q "$spec" 2>/dev/null )

  # Get the source0 for the package, it apears to always occur last in the list of sources
  source0=$(rpmspec --srpm  "${defines[@]}" --qf "[%{SOURCE}\n]" -q "$spec"  2>/dev/null | tail -1)
  if [[ -z $source0 ]]
  then
    echo "    No source file listed for $name:$version, skipping"
    continue
  fi

  # Some source files have been renamed, look for a comment and also try that (while manually substituting the name/version)
  source0alt=$(grep "^#[[:blank:]]*Source0:" "$spec" | awk '{print $NF}' | sed "s/%\?%{name}/$name/g" | sed "s/%\?%{version}/$version/g" )
  # Some packages define a %url as well
  # Use ' ' as delimiter to avoid conflict with URL characters
  specurl=$(rpmspec --srpm  "${defines[@]}" --qf "%{URL}" -q "$spec" 2>/dev/null )
  [[ -z $specurl ]] || source0alt=$(echo $source0alt | sed "s %\?%{url} $specurl g" )

  # Pull the current registration from the cgmanifest file. Every registration should have a url, so if we don't find one
  # that implies the registration is missing.
  manifesturl=$(jq --raw-output ".Registrations[].component.other | select(.name==\"$name\" and .version==\"$version\") | .downloadUrl" cgmanifest.json)
  if [[ -z $manifesturl ]]
  then
    echo "Registration for \"$name\":\"$version\" is missing" >> bad_registrations.txt
  else
    # Check if either attempt at the source url is a substring of the full download path, if so assume the full url is correct.
    overlap=$(echo "$manifesturl" | grep "$source0")
    overlapalt=$(echo "$manifesturl" | grep "$source0alt")
    if [[ -z "$overlap$overlapalt" ]]
    then
      echo "Registration for \"$name\":\"$version\" does not seem to include a URL for \"$source0\" or \"$source0alt\" (Currently $manifesturl)"  >> bad_registrations.txt
    else
      # Try a few times to download the source listed in the manifest
      mkdir -p ./cgmanifest_test_dir
      for _ in {1..10}
      do
        wget --quiet -P ./cgmanifest_test_dir "$manifesturl" && touch ./cgmanifest_test_dir/WORKED && break
        sleep 30
      done
      [[ -f ./cgmanifest_test_dir/WORKED ]] || echo "Registration for \"$name\":\"$version\" has invalid URL '$manifesturl' (could not download)"  >> bad_registrations.txt
      rm -rf ./cgmanifest_test_dir/
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
