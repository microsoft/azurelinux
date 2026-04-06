#!/usr/bin/sh
# mingw-find-debuginfo.sh - automagically generate debug info and file list
# for inclusion in an rpm spec file for mingw-* packages.

if [ "$#" -lt 2 ] ; then
    echo "Usage: $0 <BUILDDIR> [TARGET]..."
    exit 1
fi

BUILDDIR=$1
shift

for f in `find $RPM_BUILD_ROOT -type f -name "*.exe" -or -name "*.dll" -or -name "*.pyd"`
do
	case $(mingw-objdump -h $f 2>/dev/null | grep -Eo '(debug[\.a-z_]*|gnu.version)') in
	    *debuglink*) continue ;;
	    *debug*) ;;
	    *gnu.version*)
		echo "WARNING: "`echo $f | sed -e "s,^$RPM_BUILD_ROOT/*,/,"`" is already stripped!"
		continue
		;;
	    *) continue ;;
	esac

	echo extracting debug info from $f
	dest=${RPM_BUILD_ROOT}/usr/lib/debug${f/$RPM_BUILD_ROOT/}.debug
	mkdir -p `dirname $dest`
	mingw-objcopy --only-keep-debug $f $dest || :
	pushd `dirname $dest`
	keep_symbols=`mktemp`
	mingw-nm $dest --format=sysv --defined-only | awk -F \| '{ if ($4 ~ "Function") print $1 }' | sort > "$keep_symbols"
	mingw-objcopy --add-gnu-debuglink=`basename $dest` --strip-unneeded $f --keep-symbols="$keep_symbols" || :
	rm -f "$keep_symbols"
	popd
done

for target in $@; do
	prefix=`rpm --eval "%{_prefix}/%{${target}_target}"`
	if [ ! -d ${RPM_BUILD_ROOT}/usr/lib/debug/$prefix ] ; then
		continue
	fi
	find ${RPM_BUILD_ROOT}/usr/lib/debug/$prefix -type f -name "*.exe.debug" -or -name "*.dll.debug" -or -name "*.pyd.debug" |
		sed -n -e "s#^$RPM_BUILD_ROOT##p" > $BUILDDIR/${target}-debugfiles.list
        find ${RPM_BUILD_ROOT}/usr/lib/debug/$prefix/* -type d |
		sed -n -e "s#^$RPM_BUILD_ROOT#%dir #p" >> $BUILDDIR/${target}-debugfiles.list
done
