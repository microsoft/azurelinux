#!/bin/bash -e
#
#  See https://github.com/cyrusimap/cyrus-sasl/releases for unmodified sources.
#

tmppath=`mktemp -d ${TMPDIR:-/tmp}/make-no-dlcompat-tarball-XXXXXX`
if test -z "$tmppath" ; then
	echo Error creating temporary directory.
	exit 1
fi
trap "rm -fr $tmppath" EXIT

initialdir=`pwd`

for tarball in ${initialdir}/cyrus-sasl-*.tar.{gz,bz2} ; do
	if ! test -s "$tarball" ; then
		continue
	fi
	rm -fr $tmppath/*
	pushd $tmppath > /dev/null
	case "$tarball" in
	*nodlcompat*)
		: Do nothing.
		;;
	*.gz)
		gzip  -dc "$tarball" | tar xf -
		rm -fr cyrus-sasl-*/dlcompat*
		rm -fr cyrus-sasl-*/plugins/srp*
		tar cf - * | gzip  -9c > \
		$initialdir/`basename $tarball .tar.gz`-nodlcompatorsrp.tar.gz
		;;
	*.bz2)
		bzip2 -dc "$tarball" | tar xf -
		rm -fr cyrus-sasl-*/dlcompat*
		rm -fr cyrus-sasl-*/plugins/srp*
		tar cf - * | bzip2 -9c > \
		$initialdir/`basename $tarball .tar.bz2`-nodlcompatorsrp.tar.bz2
		;;
	esac
	popd > /dev/null
done
