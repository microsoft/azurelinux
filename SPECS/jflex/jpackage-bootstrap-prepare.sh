#!/bin/sh

# This script is based on libcdio_spec-prepare.sh (thanks to sbrabec@suse.cz)
# create a -bootstrap spec for majority of Java packages for bootstrapping
#
#Usage:
# 1.) add these two lines below into the spec file including hash sign (#)
#     behind the Name: tag
#   # This line is not a comment, please do not remove it!
#   #%(sh %{_sourcedir}/jpackage-bootstrap-prepare.sh %{_sourcedir} %{name})
# 2.) you need to define a with_bootstrap macro with value 1
#
# How it works:
# 1.) Was called by rpmbuild (or Re, or should be invoked manually from command line)
# 2.) Rename the package name to name-bootstrap
# 3.) Redefine the with_bootstrap macro to _without_bootstrap 1
# 4.) Define a real_name macro with real name (used in %install and %files)
# 5.) Copy the .changes to -boostrap.changes


ORIG_SPEC=${2%-bootstrap}
# Never update -bootstrap file when it is already opened. It will break advanced build scripts:
if [[ "${2}" != "${ORIG_SPEC}" ]]; then
    exit
fi

if [[ ! -f ${1}/${ORIG_SPEC}.spec ]] ; then
    exit
fi

EDIT_WARNING="##### WARNING: please do not edit this auto generated spec file. Use the ${ORIG_SPEC}.spec! #####\n"
sed "s/^%define _without_bootstrap.*$/${EDIT_WARNING}%define with_bootstrap 1/;
     s/^\(Name:.*\)$/\1-bootstrap/;
    " < ${1}/${ORIG_SPEC}.spec > ${1}/${ORIG_SPEC}-bootstrap.spec

cp -a ${1}/${ORIG_SPEC}.changes ${1}/${ORIG_SPEC}-bootstrap.changes
