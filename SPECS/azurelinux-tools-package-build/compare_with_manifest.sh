#!/bin/bash
#
# Run with $1 == "added" to see added packages. By default lists removed packages.
#

root=$(git rev-parse --show-toplevel)

spec_path=${root}/SPECS/azurelinux-tools-package-build/azurelinux-tools-package-build.spec
manifest_path=${root}/toolkit/resources/manifests/package/pkggen_core_x86_64.txt

function expand_packages_from_spec() {
    spec_reqs=$(rpmspec -q $1 --requires)

    dnf repoquery -y ${spec_reqs[@]} --latest-limit=1 --quiet --qf '%{name}'
    dnf repoquery -y ${spec_reqs[@]} --latest-limit=1 --quiet --recursive --resolve --requires --qf '%{name}'
}

function get_packages_from_manifest() {
    sed -e 's/-[\.0-9]\+-[0-9]\+\(\.azl3\)\?\.\(x86_64\|noarch\)\.rpm\s*$//' $1
}

args=(--unchanged-line-format='')
if [[ "$1" == "added" ]]; then
    args+=(--old-line-format='' --new-line-format='%L')
else
    args+=(--old-line-format='%L' --new-line-format='')
fi

# Look for *removed* packages.
diff ${args[@]} \
  <(get_packages_from_manifest ${manifest_path} | sort | uniq) \
  <(expand_packages_from_spec ${spec_path} | sort | uniq) 
