#!/bin/bash -

set -e

# Maintainer script to copy patches from the git repo to the current
# directory.  Use it like this:
#   ./copy-patches.sh

rhel_version=8.3

# Check we're in the right directory.
if [ ! -f libnbd.spec ]; then
    echo "$0: run this from the directory containing 'libnbd.spec'"
    exit 1
fi

git_checkout=$HOME/d/libnbd-rhel-$rhel_version
if [ ! -d $git_checkout ]; then
    echo "$0: $git_checkout does not exist"
    echo "This script is only for use by the maintainer when preparing a"
    echo "libnbd release on RHEL."
    exit 1
fi

# Get the base version of libnbd.
version=`grep '^Version:' libnbd.spec | awk '{print $2}'`
tag="v$version"

# Remove any existing patches.
git rm -f [0-9]*.patch ||:
rm -f [0-9]*.patch

# Get the patches.
(cd $git_checkout; rm -f [0-9]*.patch; git format-patch -N $tag)
mv $git_checkout/[0-9]*.patch .

# Remove any not to be applied.
rm -f *NOT-FOR-RPM*.patch

# Add the patches.
git add [0-9]*.patch

# Print out the patch lines.
echo
echo "--- Copy the following text into libnbd.spec file"
echo

echo "# Patches."
for f in [0-9]*.patch; do
    n=`echo $f | awk -F- '{print $1}'`
    echo "Patch$n:     $f"
done

echo
echo "--- End of text"
