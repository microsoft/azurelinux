#!/bin/bash

set -e

TOOLCHAIN_BUILD_FILE=$1
SPECS_DIR=$2
MANIFESTS_DIR=$3
DIST_TAG=$4
ARCH=$5

write_rpms_from_spec () {
    # $1 = spec file
    # $2 = file to save to

    exlusiveArch=$(rpmspec -q $1 --define="with_check 0" --define="dist $DIST_TAG" --qf="%{EXCLUSIVEARCH}" --srpm 2>/dev/null)
    if [ "$exlusiveArch" != "(none)" -a "$exlusiveArch" != "$ARCH" ]; then
        return 0
    fi

    version=$(rpmspec -q $1 --define="with_check 0" --define="dist $DIST_TAG" --qf="%{VERSION}" --srpm 2>/dev/null)
    rpmWithoutExtension=$(rpmspec -q $1 --define="with_check 0" --define="dist $DIST_TAG" --target=$ARCH 2>/dev/null)

    for rpm in $rpmWithoutExtension
    do
        echo "$rpm.rpm" >> $2

        # debuginfo packages are generated dynamically, and so will not be returned by rpmspec.
        # Create a superset manifest that assumes every package will have a debuginfo version.
        debuginfo_pkg=$(sed "0,/-$version/s//-debuginfo-$version/" <<< $rpm)
        echo "$debuginfo_pkg.rpm" >> $2
    done
}

write_rpms_from_toolchain () {
    # $1 = file to save to
    specs=$(sed -e '/^\s*build_rpm_in_chroot_no_install/!d; s/\s*build_rpm_in_chroot_no_install //; /^()/d' $TOOLCHAIN_BUILD_FILE)
    for specName in $specs
    do
        specFile=$(find $SPECS_DIR/**/$specName.spec)
        write_rpms_from_spec $specFile $1
    done
}

diff_manifest () {
    # $1 = superset file
    # $2 = subset file
    # $3 = diff file

    diff_formatting='mismatch line -> %<'
    diff --new-group-format='' --old-group-format='' --unchanged-group-format='' --changed-group-format="$diff_formatting" <(sort $2) <(sort $1) > $3 || true
}

# Generate a superset manifest that contains all possible toolchain packages (including all possible debuginfos).
# This manifest will be a superset of the toolchain manifests which will be a superset of the pkggen_core manifests.
generated_manifest=$(mktemp)
write_rpms_from_toolchain $generated_manifest
toolchain_file="$MANIFESTS_DIR/toolchain_$ARCH.txt"
pkggen_core_file="$MANIFESTS_DIR/pkggen_core_$ARCH.txt"

manifest_diff_file=$(mktemp)
diff_manifest $generated_manifest $toolchain_file $manifest_diff_file
if [[ -s $manifest_diff_file ]]; then
    echo ""
    echo "$(basename $toolchain_file)"
    echo "============================="
    echo "$(cat $manifest_diff_file)"
    echo ""
fi

pkggen_diff_file=$(mktemp)
diff_manifest $generated_manifest $pkggen_core_file $pkggen_diff_file
if [[ -s $pkggen_diff_file ]]; then
    echo ""
    echo "$(basename $pkggen_core_file)"
    echo "============================="
    echo "$(cat $pkggen_diff_file)"
    echo ""
fi

if [[ -s $manifest_diff_file || -s $pkggen_diff_file ]]; then
    echo "$ARCH manifests do not match toolchain specs!"
    exit 1
else
    echo "$ARCH manifests match"
    exit 0
fi