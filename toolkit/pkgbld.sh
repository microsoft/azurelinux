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

helpFuncion () {
	echo ""
	echo "-h  : Print detailed usage"
        echo "-s  : Spec Dir [Default SPECS] [Possible values: ../SPECS-EXTENDED, ../SPECS]"
        echo "-b  : DAILY_BUILD_ID of the format of 3-0-YYYYMMDD [Default 'lkg']"
        echo "-c  : Run with check distabled/enabled [Default RUN_CHECK=n]"
        echo "-p  : Package to build/rebuild [Default all]"
        echo "-r  : Refresh worker chroot [Default true]"
        echo "-f  : Force a Rebuild"
        echo "-n  : Cleanup input-srpms expand-srpms"
        echo "-d  : Show the command to be executed."
	echo ""
	echo ""
	echo "Examples:"
	echo "[inside the toolkit dir]"
	echo "Build vim & golang locally:"
	echo "./build.sh -p \"vim golang\""
	echo ""
	echo "Build cpptest from extended:"
	echo "./build.sh -s=../SPECS-EXTENDED -p cpptest"
	echo ""
}


while getopts "hs:b:cp:rfnd" opt
do
	case "$opt" in
		h ) helpVar=y;;
		s ) specsVar="$OPTARG";;
		b ) buildidVar="$OPTARG";;
		c ) checkVar=y;;
		p ) packageVar="$OPTARG";;
		r ) refreshVar=n;;
		f ) forceVar=y;;
		n ) nukeVar=y;;
		d ) dryrunVar=y;;
	esac
done

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
	echo "Package var needs to be set:";
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

if [ -n "$nukeVar" ]
then
	echo "Cleaning up expanded specs and input srpms"
	sudo make clean-expand-specs clean-input-srpms
fi

if [ -n "$dryrunVar" ]
then
	echo "sudo make build-packages \ "
	echo "     REBUILD_TOOLS=y \ "
	echo "     PACKAGE_REBUILD_LIST="${TOBUILD}" \ ";
	echo "     SRPM_PACK_LIST="${TOBUILD}" \ ";
	echo "     RUN_CHECK=$RC \ ";
	echo "     SRPM_FILE_SIGNATURE_HANDLING=update \ ";
	echo "     DAILY_BUILD_ID=$BID \ ";
	echo "     REFRESH_WORKER_CHROOT=$WCREFRESH \ ";
	echo "     USE_PACKAGE_BUILD_CACHE=$USEPKGBLDCACHE \ ";
	echo "     SPECS_DIR=$SDIR \ ";
	echo "     -j $(nproc)";
	exit 0
fi




sudo make build-packages \
	REBUILD_TOOLS=y \
	PACKAGE_REBUILD_LIST="${TOBUILD}" \
	SRPM_PACK_LIST="${TOBUILD}" \
	RUN_CHECK=$RC \
	SRPM_FILE_SIGNATURE_HANDLING=update \
	DAILY_BUILD_ID=$BID \
	REFRESH_WORKER_CHROOT=$WCREFRESH \
	USE_PACKAGE_BUILD_CACHE=$USEPKGBLDCACHE \
	REPO_LIST=$REPOLIST \
	SPECS_DIR=$SDIR \
	-j $(nproc)
