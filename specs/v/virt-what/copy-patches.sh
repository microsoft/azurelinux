#!/bin/bash -

set -e

# Maintainer script to copy patches from the git repo to the current
# directory.  It's normally only used downstream (ie. in RHEL).  Use
# it like this:
#   ./copy-patches.sh

project=virt-what
rhel_version=10.0

# Check we're in the right directory.
if [ ! -f $project.spec ]; then
    echo "$0: run this from the directory containing '$project.spec'"
    exit 1
fi

case `id -un` in
    rjones) git_checkout=$HOME/d/$project-rhel-$rhel_version ;;
    lacos)  git_checkout=$HOME/src/v2v/$project ;;
    *)      git_checkout=$HOME/d/$project-rhel-$rhel_version ;;
esac
if [ ! -d $git_checkout ]; then
    echo "$0: $git_checkout does not exist"
    echo "This script is only for use by the maintainer when preparing a"
    echo "$project release on RHEL."
    exit 1
fi

# Get the base version of the project.
version=`grep '^Version:' $project.spec | awk '{print $2}'`
tag="v$version"

# Remove any existing patches.
git rm -f [0-9]*.patch ||:
rm -f [0-9]*.patch

# Get the patches.
(cd $git_checkout; rm -f [0-9]*.patch; git -c core.abbrev=9 format-patch -O/dev/null -N --submodule=diff $tag)
mv $git_checkout/[0-9]*.patch .

# Remove any not to be applied.
rm -f *NOT-FOR-RPM*.patch

# Add the patches.
git add [0-9]*.patch

# Print out the patch lines.
echo
echo "--- Copy the following text into $project.spec file"
echo

echo "# Patches."
for f in [0-9]*.patch; do
    n=`echo $f | awk -F- '{print $1}'`
    echo "Patch$n:     $f"
done

echo
echo "--- End of text"
