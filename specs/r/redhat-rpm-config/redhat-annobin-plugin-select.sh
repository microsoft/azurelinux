#!/usr/bin/sh
# This is a script to select which GCC spec file fragment
# should be the destination of the redhat-annobin-cc1 symlink.

# Author: Nick Clifton  <nickc@redhat.com>
# Copyright (c) 2021 Red Hat.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2, or (at your
# option) any later version.

# It is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Usage:
#   redhat-annobin-plugin-select [script-dir]
#
# If script-dir is not provided then /usr/lib/rpm/redhat is used
# as the location where all of the annobin plugin selection files
# can be found.

if test "x$1" = "x" ;
then
    rrcdir=/usr/lib/rpm/redhat
else
    rrcdir=$1
fi

# Set this variable to non-zero to enable the generation of debugging
# messages.
debug=0

# Decide which version of the annobin plugin for gcc should be used.
# There are two possible versions, one created by the annobin package and one
# created by the gcc package.  The logic selects the gcc version unless both
# have been built by the same version of the compiler.  In that case the
# annobin version is selected instead.
#
# The point of all this is that the annobin plugin is very sensitive to
# mismatches with the version of gcc that built it.  If the plugin is built
# by version A of gcc, but then run on version B of gcc, it is possible for
# the plugin to misbehave, which then causes problems if gating tests examine
# the plugin's output.  (This has happened more than once in RHEL...).
#
# So the plugin is built both by gcc and by the annobin package.  This means
# that whenever gcc is updated a fresh plugin is built, and the logic below
# will select that version.  But in order to allow annobin development to
# proceed independtently of gcc, the annobin package can also update its
# version of the plugin, and the logic will select this new version.

# This is where the annobin package stores the information on the version
# of gcc that built the annobin plugin.
aver=`gcc --print-file-name=plugin`/annobin-plugin-version-info

# This is where the gcc package stores its version information.
gver=`gcc --print-file-name=rpmver`

aplugin=`gcc --print-file-name=plugin`/annobin.so.0.0.0
gplugin=`gcc --print-file-name=plugin`/gcc-annobin.so.0.0.0

# This is the file that needs to be updated when either of those version
# files changes.
rac1=redhat-annobin-cc1

# This is the GCC spec file fragment that selects the gcc-built version of
# the annobin plugin
select_gcc=redhat-annobin-select-gcc-built-plugin

# This is the GCC spec file fragment that selects the annobin-built version
# of the annobin plugin
select_annobin=redhat-annobin-select-annobin-built-plugin

install_annobin_version=0
install_gcc_version=0

if [ -f $aplugin ]
then
    if [ -f $gplugin ]
    then
	if [ $debug -eq 1 ]
	then
	    echo "  redhat-rpm-config: Both plugins exist, checking version information"
	fi

	if [ -f $gver ]
	then
	    if [ -f $aver ]
	    then
		if [ $debug -eq 1 ]
		then
		    echo "  redhat-rpm-config: Both plugin version files exist - comparing..."
		fi

		# Get the first line from the version info files.  This is just in
		# vase there are extra lines in the files.
		avers=`head --lines=1 $aver`
		gvers=`head --lines=1 $gver`

		if [ $debug -eq 1 ]
		then
		    echo "  redhat-rpm-config: Annobin plugin built by gcc $avers"
		    echo "  redhat-rpm-config: GCC     plugin built by gcc $gvers"
		fi

		# If both plugins were built by the same version of gcc then select
		# the one from the annobin package (in case it is built from newer
		# sources).  If the plugin builder versions differ, select the gcc
		# built version instead.  This assumes that the gcc built version
		# always matches the installed gcc, which should be true.
		if [ $avers = $gvers ]
		then
		    if [ $debug -eq 1 ]
		    then
			echo "  redhat-rpm-config: Both plugins built by the same compiler - using annobin-built plugin"
		    fi
		    install_annobin_version=1
		else
		    if [ $debug -eq 1 ]
		    then
			echo "  redhat-rpm-config: Versions differ - using gcc-built plugin"
		    fi
		    install_gcc_version=1
		fi
	    else
		if [ $debug -eq 1 ]
		then
		    echo "  redhat-rpm-config: Annobin version file does not exist, using gcc-built plugin"
		fi
		install_gcc_version=1
	    fi
	else
	    if [ -f $aver ]
	    then
		# FIXME: This is suspicious.  If the installed GCC does not supports plugins
		# then enabling the annobin plugin will not work.
		if [ $debug -eq 1 ]
		then
		    echo "  redhat-rpm-config: GCC plugin version file does not exist, using annobin-built plugin"
		fi
		install_annobin_version=1
	    else
		if [ $debug -eq 1 ]
		then
		    echo "  redhat-rpm-config: Neither version file exists - playing safe and using gcc-built plugin"
		    echo "  redhat-rpm-config: Note: expected to find $aver and/or $gver"
		fi
		install_gcc_version=1
	    fi
	fi
    else
	if [ $debug -eq 1 ]
	then
	    echo "  redhat-rpm-config: Only the annobin plugin exists - using that"
	fi
	install_annobin_version=1
    fi
else
    if [ -f $gplugin ]
    then
	if [ $debug -eq 1 ]
	then
	    echo "  redhat-rpm-config: Only the gcc plugin exists - using that"
	fi
    else
	if [ $debug -eq 1 ]
	then
	    echo "  redhat-rpm-config: Neither plugin exists - playing safe and using gcc-built plugin"
	    echo "  redhat-rpm-config: Note: expected to find $aplugin and/or $gplugin"
	fi
    fi
    install_gcc_version=1
fi

if [ $install_annobin_version -eq 1 ]
then
    if [ $debug -eq 1 ]
    then
	echo "  redhat-rpm-config: Installing annobin version of $rac1"
    fi
    pushd $rrcdir > /dev/null
    rm -f $rac1
    ln -s $select_annobin "$rac1"
    popd > /dev/null
    
else if [ $install_gcc_version -eq 1 ]
     then
	if [ $debug -eq 1 ]
	then
	    echo "  redhat-rpm-config: Installing gcc version of $rac1"
	fi
	pushd $rrcdir > /dev/null
	rm -f $rac1
	ln -s $select_gcc $rac1
	popd > /dev/null
     fi
fi
