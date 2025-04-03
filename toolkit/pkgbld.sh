#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Dev script to build packages for 3.0 locally. There is no compatibility warranty and it is subject to change.
# For internal dev use only.

TOBUILD=
BID=lkg
RC=n
WCREFRESH=y
SDIR=../SPECS
USEPKGBLDCACHE=y
USECCACHE=y
helpFuncion () {
	echo ""
	echo "Build a package(s) for 3.0 locally:"
	echo "  -h  : Print detailed usage"
        echo "  -s  : Spec Dir [Default SPECS] [Possible values: ../SPECS-EXTENDED, ../SPECS]"
        echo "  -b  : DAILY_BUILD_ID of the format of 3-0-YYYYMMDD [Default 'lkg']"
        echo "  -c  : Run with check disabled/enabled [Default disabled]"
	echo "  -p  : Package(s) to build/rebuild [Default all] (space seperated list)"
        echo "  -r  : Refresh worker chroot [Default true]"
        echo "  -f  : Force a Rebuild"
        echo "  -n  : Cleanup input-srpms expand-srpms"
        echo "  -d  : [DryRun] Show the command to be executed"
	echo "  -x  : Disable build using ccache (Default USE_CCACHE=y)"
	echo ""
	echo "Examples:"
	echo "[inside the toolkit dir]"
	echo ""
	echo "Build vim & golang-1.18 locally:"
	echo "  $0 -p \"vim golang-1.18\""
	echo ""
	echo "Build vim & golang-1.18 locally with check enabled:"
	echo "  $0 -c -p \"vim golang-1.18\""
	echo ""
	echo "Build cpptest from extended:"
	echo "  $0 -s ../SPECS-EXTENDED -p cpptest"
	echo ""
	echo "Extra build options can be supplied at the end of all the defined options"
	echo "Ignore tests of packages among the build"
	echo "  $0 -c -p \"pkg1 pkg2 pkg3\"  -- 'TEST_IGNORE_LIST=\"pkg1 pkg3\"' "
}


while getopts "hs:b:cp:rfndx" opt
do
	case "$opt" in
		h ) helpVar=y;;
		s ) specsVar="$OPTARG" ;;
		b ) buildidVar="$OPTARG";;
		c ) checkVar=y;;
		p ) packageVar="$OPTARG";;
		r ) refreshVar=n;;
		f ) forceVar=y;;
		n ) nukeVar=y;;
		d ) dryrunVar=y;;
		x ) cacheVar=y;;
	esac
done
shift $((OPTIND - 1))

if [ -n "$helpVar" ]
then
	helpFuncion
	exit 0
fi

if [ -n "$specsVar" ]
then
	SDIR=$specsVar
fi

if [ -n "$buildidVar" ]
then
	BID="$buildidVar"
fi

if [ -n "$checkVar" ]
then
	RC=y
fi

if [ -z "$packageVar" ]
then
	echo "Package to build needs to be set:";
	helpFuncion
	exit 1
fi

if [ -n "$packageVar" ]
then
	TOBUILD="$packageVar"
fi


if [ -n "$refreshVar" ]
then
	WCREFRESH=n
fi

if [ -n "$forceVar" ]
then
	USEPKGBLDCACHE=n
fi

if [ -n "$cacheVar" ]
then
	USECCACHE=n
fi

if [ -n "$nukeVar" ]
then
	echo "Cleaning up expanded specs and input srpms"
	sudo make clean-expand-specs clean-input-srpms
fi

if [ -n "$dryrunVar" ]
then
	echo "sudo make build-packages \ "
	echo "     REBUILD_TOOLS=y \ "
	echo "     QUICK_REBUILD_PACKAGES=y \ "
	echo "     USE_CCACHE=${USECCACHE} \ "
	echo "     PACKAGE_REBUILD_LIST="${TOBUILD}" \ ";
	echo "     SRPM_PACK_LIST="${TOBUILD}" \ ";
	echo "     RUN_CHECK=$RC \ ";
	echo "     SRPM_FILE_SIGNATURE_HANDLING=update \ ";
	echo "     DAILY_BUILD_ID=$BID \ ";
	echo "     REFRESH_WORKER_CHROOT=$WCREFRESH \ ";
	echo "     USE_PACKAGE_BUILD_CACHE=$USEPKGBLDCACHE \ ";
	echo "     SPECS_DIR=$SDIR \ ";
	echo "     -j $(nproc) \ ";
	echo "     $@ ";
	exit 0
fi




sudo make build-packages \
	REBUILD_TOOLS=y \
	QUICK_REBUILD_PACKAGES=y \
	USE_CCACHE=${USECCACHE} \
	PACKAGE_REBUILD_LIST="${TOBUILD}" \
	SRPM_PACK_LIST="${TOBUILD}" \
	RUN_CHECK=$RC \
	SRPM_FILE_SIGNATURE_HANDLING=update \
	DAILY_BUILD_ID=$BID \
	REFRESH_WORKER_CHROOT=$WCREFRESH \
	USE_PACKAGE_BUILD_CACHE=$USEPKGBLDCACHE \
	REPO_LIST=$REPOLIST \
	SPECS_DIR=$SDIR \
	-j $(nproc) \
	$@
