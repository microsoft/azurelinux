#!/bin/bash

#$@ - Paths to spec files to check

#Ignore specs, mostly those with Source0 files that are not from an external source, or have very odd URLs
ignore_list=" \
  initramfs \
  kf5 \
  mariner-repos \
  mariner-rpm-macros \
  moby-buildx \
  moby-containerd \
  qt5-rpm-macros \
  runc \
  grub2-efi-binary-signed-aarch64 \
  grub2-efi-binary-signed-x64 \
  kernel-signed-aarch64 \
  kernel-signed-x64"

rm -f bad_registrations.txt

[[ -n "$@" ]] || echo "No specs passed to validate"

for spec in $@
do
  echo Checking "$spec"

  source0=$(rpmspec --srpm  --define "with_check 0" --qf "[%{SOURCE}\n]" -q $spec  2>/dev/null | tail -1)
  if [[ -z $source0 ]]
  then
    echo "    No source file listed for $name:$version, skipping"
    continue
  fi

  name=$(rpmspec --srpm  --define "with_check 0" --qf "%{NAME}" -q $spec 2>/dev/null )
  # Some specs don't make sense to add, ignore them
  if echo $ignore_list | grep -w "$name" > /dev/null
  then
    echo "    $name is being ignored, skipping"
    continue
  fi


  version=$(rpmspec --srpm  --define "with_check 0" --qf "%{VERSION}" -q $spec 2>/dev/null )
  #Some source files have been renamed, look for a comment and also try that (while manually substituting the name/version)
  source0alt=$(grep "^#[[:blank:]]*Source0:" $spec | awk '{print $NF}' | sed "s/%{name}/$name/g" | sed "s/%{version}/$version/g" )
  #Some packages define a %url as well
  #Use ' ' as delimiter to avoid conflict with URL characters
  specurl=$(rpmspec --srpm  --define "with_check 0" --qf "%{URL}" -q $spec 2>/dev/null )
  [[ -z specurl ]] || source0alt=$(echo $source0alt | sed "s %{url} $specurl g" )

  manifesturl=$(jq ".Registrations[].component.other | select(.name==\"$name\" and .version==\"$version\") | .downloadUrl" cgmanifest.json)
  if [[ -z $manifesturl ]]
  then
    echo "Registration for \"$name\":\"$version\" is missing" >> bad_registrations.txt
  else
    overlap=$(echo "$manifesturl" | grep "$source0")
    overlapalt=$(echo "$manifesturl" | grep "$source0alt")
    if [[ -z "$overlap$overlapalt" ]]
    then
      echo "Registration for \"$name\":\"$version\" does not seem to include a URL for \"$source0\" or \"$source0alt\" (Currently $manifesturl)"  >> bad_registrations.txt
    fi
  fi
done

if [[ -s bad_registrations.txt ]]
then
  echo "####"
  echo "cgmanifest.json may need to be updated..."
  echo "####"
  cat bad_registrations.txt
  exit 1
fi