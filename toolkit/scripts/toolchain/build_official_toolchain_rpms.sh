#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Building the existing mariner toolchain SPEC files in built-from-scratch chroot environment
echo Building RPMs for toolchain
echo Parameters passed: $@

MARINER_DIST_TAG=$1
MARINER_BUILD_NUMBER=$2
MARINER_RELEASE_VERSION=$3
MARINER_BUILD_DIR=$4
SPECROOT=$5
RUN_CHECK=${6}
MARINER_TOOLCHAIN_MANIFESTS_DIR=$7
INCREMENTAL_TOOLCHAIN=${8:-n}
MARINER_INPUT_SRPMS_DIR=$9
MARINER_OUTPUT_SRPMS_DIR=${10}

MARINER_LOGS=$MARINER_BUILD_DIR/logs
TOOLCHAIN_LOGS=$MARINER_LOGS/toolchain
TOOLCHAIN_BUILD_LIST=$TOOLCHAIN_LOGS/build_list.txt
TOOLCHAIN_FAILURES=$TOOLCHAIN_LOGS/failures.txt
set -x

export LFS=$MARINER_BUILD_DIR/toolchain/populated_toolchain
TOPDIR=/usr/src/mariner
CHROOT_SOURCES_DIR=$LFS$TOPDIR/SOURCES
CHROOT_SPECS_DIR=$LFS$TOPDIR/SPECS
CHROOT_SRPMS_DIR=$LFS$TOPDIR/SRPMS
CHROOT_RPMS_DIR=$LFS$TOPDIR/RPMS
CHROOT_RPMS_DIR_ARCH=$CHROOT_RPMS_DIR/$(uname -m)
CHROOT_RPMS_DIR_NOARCH=$CHROOT_RPMS_DIR/noarch
CHROOT_INSTALL_RPM_DIR=$LFS$TOPDIR/PREBUILT_RPMS
CHROOT_INSTALL_RPM_DIR_IN_CHROOT=$TOPDIR/PREBUILT_RPMS
FINISHED_RPM_DIR=$MARINER_BUILD_DIR/toolchain/built_rpms
PARAM_DIST_TAG=$MARINER_DIST_TAG
PARAM_BUILD_NUM=$MARINER_BUILD_NUMBER
PARAM_RELEASE_VER=$MARINER_RELEASE_VERSION

# Assumption: pipeline has copied file: build/toolchain/toolchain_from_container.tar.gz
# Or, if toolchain-build-all was called, both of the following will exist:
#       build/toolchain/populated_toolchain
#       build/toolchain/toolchain_from_container.tar.gz
#
pushd $MARINER_BUILD_DIR/toolchain
if [[ ! -d "$LFS" ]]
then
    echo "$LFS not created yet, unpacking tarball"
    tar -xzf toolchain_from_container.tar.gz --checkpoint=100000 --checkpoint-action=echo="%T"
fi
popd

mkdir -pv $FINISHED_RPM_DIR
mkdir -pv $CHROOT_SPECS_DIR
mkdir -pv $CHROOT_SRPMS_DIR
mkdir -pv $CHROOT_SOURCES_DIR
mkdir -pv $CHROOT_INSTALL_RPM_DIR
mkdir -pv $TOOLCHAIN_LOGS
mkdir -pv $CHROOT_RPMS_DIR

sudo rm -f $TOOLCHAIN_BUILD_LIST
sudo rm -f $TOOLCHAIN_FAILURES
touch $TOOLCHAIN_FAILURES

chroot_mount () {
    trap chroot_unmount EXIT
    mount --bind /dev $LFS/dev
    mount -t devpts devpts $LFS/dev/pts -o gid=5,mode=620
    mount -t proc proc $LFS/proc
    mount -t sysfs sysfs $LFS/sys
    mount -t tmpfs tmpfs $LFS/run
}

blocking_unmount () {
    # $1 mountpoint
    umount -l $1
    while mountpoint -q $1; do
        echo $1 is still busy...
        sleep 1
        umount -l $1
    done
}

chroot_unmount () {
    echo "Unmounting chroot"
    blocking_unmount $LFS/dev/pts
    blocking_unmount $LFS/dev
    blocking_unmount $LFS/run
    blocking_unmount $LFS/proc
    blocking_unmount $LFS/sys
    trap - EXIT
}

chroot_and_print_installed_rpms () {
    chroot_mount

    echo "List of packages installed in chroot:"

    chroot "$LFS" /usr/bin/env -i  \
        HOME=/root                         \
        TERM="$TERM"                       \
        PS1='\u:\w\$ '                     \
        PATH=/bin:/usr/bin:/sbin:/usr/sbin \
        rpm -qa
    echo ""

    chroot_unmount
}

chroot_and_install_rpms () {
    # $1 = package name
    # Clean and then copy the RPM into the chroot directory for installation below
    rm -v $CHROOT_INSTALL_RPM_DIR/*
    cp -v $CHROOT_RPMS_DIR_ARCH/$1-* $CHROOT_INSTALL_RPM_DIR
    cp -v $CHROOT_RPMS_DIR_NOARCH/$1-* $CHROOT_INSTALL_RPM_DIR

    chroot_mount

    echo "RPM files to be installed..."
    chroot "$LFS" ls -la $CHROOT_INSTALL_RPM_DIR_IN_CHROOT
    echo "Installing the rpms..."
    chroot "$LFS" /usr/bin/env -i  \
        HOME=/root                         \
        TERM="$TERM"                       \
        PS1='\u:\w\$ '                     \
        PATH=/bin:/usr/bin:/sbin:/usr/sbin \
        rpm -i -vh --force --nodeps $CHROOT_INSTALL_RPM_DIR_IN_CHROOT/*

    chroot_unmount
}

chroot_and_run_rpmbuild () {
    # $1 = package name
    echo "Will build spec for $1 in chroot"
    chroot_mount

    if [ "$RUN_CHECK" = "y" ]; then
        export CHECK_SETTING=" "
    else
        export CHECK_SETTING="--nocheck"
    fi

    chroot "$LFS" /usr/bin/env -i          \
        HOME=/root                         \
        TERM="$TERM"                       \
        PS1='\u:\w\$ '                     \
        PATH=/bin:/usr/bin:/sbin:/usr/sbin \
        SHELL=/bin/bash                    \
        rpmbuild --nodeps --rebuild --clean     \
            $CHECK_SETTING                 \
            --define "with_check 1" --define "dist $PARAM_DIST_TAG" --define "mariner_build_number $PARAM_BUILD_NUM" \
            --define "mariner_release_version $PARAM_RELEASE_VER" $TOPDIR/SRPMS/$1 \
            || echo "$1" >> "$TOOLCHAIN_FAILURES"

    chroot_unmount
}

build_rpm_in_chroot_no_install () {
    # $1 = package name
    # $2 = qualified package name
    if [ -n "$2" ]; then
        rpmPath=$(find $CHROOT_RPMS_DIR -name "$2-*" -print -quit)
    else
        rpmPath=$(find $CHROOT_RPMS_DIR -name "$1-*" -print -quit)
    fi
    if [ "$INCREMENTAL_TOOLCHAIN" = "y" ] && [ -n "$rpmPath" ]; then
        echo found $rpmPath for $1
        find $CHROOT_RPMS_DIR -name "$1*" -exec cp {} $FINISHED_RPM_DIR ';'
    else
        echo only building RPM $1 within the chroot
        specPath=$(find $SPECROOT -name "$1.spec" -print -quit)
        srpmName=$(rpmspec -q $specPath --srpm --define="with_check 1" --define="dist $PARAM_DIST_TAG" --queryformat %{NAME}-%{VERSION}-%{RELEASE}.src.rpm)
        srpmPath=$MARINER_INPUT_SRPMS_DIR/$srpmName
        cp $srpmPath $CHROOT_SRPMS_DIR
        chroot_and_run_rpmbuild $srpmName 2>&1 | awk '{ print strftime("time=\"%Y-%m-%dT%T%Z\""), $0; fflush(); }' | tee $TOOLCHAIN_LOGS/$srpmName.log
        cp $CHROOT_RPMS_DIR_ARCH/$1* $FINISHED_RPM_DIR
        cp $CHROOT_RPMS_DIR_NOARCH/$1* $FINISHED_RPM_DIR
        cp $srpmPath $MARINER_OUTPUT_SRPMS_DIR
        echo NOT installing the package $srpmName
    fi
    echo "$1" >> $TOOLCHAIN_BUILD_LIST
}

# Copy RPM subpackages that have a different prefix
copy_rpm_subpackage () {
    echo cache $1 RPMS
    cp $CHROOT_RPMS_DIR_ARCH/$1* $FINISHED_RPM_DIR
    cp $CHROOT_RPMS_DIR_NOARCH/$1* $FINISHED_RPM_DIR
}

echo Setting up initial chroot to build pass1 toolchain RPMs from SPECs

# Configure rpm macros
mkdir -pv $LFS/usr/etc/rpm
cp -v $SPECROOT/mariner-rpm-macros/macros $LFS/usr/etc/rpm/macros
cp -v $SPECROOT/rpm/brp* $LFS/usr/lib/rpm
mkdir -pv $LFS/usr/lib/rpm/macros.d
cp -v $MARINER_TOOLCHAIN_MANIFESTS_DIR/macros.override $LFS/usr/lib/rpm/macros.d/macros.override
chmod +x $LFS/usr/lib/rpm/brp*
cp /etc/resolv.conf $LFS/etc/

chroot_and_print_installed_rpms

echo Building final list of toolchain RPMs
build_rpm_in_chroot_no_install mariner-rpm-macros
copy_rpm_subpackage mariner-check-macros
chroot_and_install_rpms mariner-rpm-macros
chroot_and_install_rpms mariner-check-macros
build_rpm_in_chroot_no_install filesystem
build_rpm_in_chroot_no_install kernel-headers
build_rpm_in_chroot_no_install glibc
build_rpm_in_chroot_no_install zlib
build_rpm_in_chroot_no_install file
build_rpm_in_chroot_no_install binutils
build_rpm_in_chroot_no_install gmp
build_rpm_in_chroot_no_install mpfr
build_rpm_in_chroot_no_install libmpc
build_rpm_in_chroot_no_install gcc
build_rpm_in_chroot_no_install pkg-config
build_rpm_in_chroot_no_install ncurses
build_rpm_in_chroot_no_install readline
build_rpm_in_chroot_no_install bash
build_rpm_in_chroot_no_install bzip2
build_rpm_in_chroot_no_install gdbm
build_rpm_in_chroot_no_install coreutils
build_rpm_in_chroot_no_install gettext
build_rpm_in_chroot_no_install sqlite
build_rpm_in_chroot_no_install nspr
build_rpm_in_chroot_no_install expat
build_rpm_in_chroot_no_install libffi
build_rpm_in_chroot_no_install xz
build_rpm_in_chroot_no_install zstd
build_rpm_in_chroot_no_install lz4
build_rpm_in_chroot_no_install m4
build_rpm_in_chroot_no_install libdb
build_rpm_in_chroot_no_install libcap
build_rpm_in_chroot_no_install popt
build_rpm_in_chroot_no_install findutils
build_rpm_in_chroot_no_install tar
build_rpm_in_chroot_no_install gawk
build_rpm_in_chroot_no_install gzip
build_rpm_in_chroot_no_install libpipeline
build_rpm_in_chroot_no_install libtool
build_rpm_in_chroot_no_install make
build_rpm_in_chroot_no_install patch
build_rpm_in_chroot_no_install procps-ng
build_rpm_in_chroot_no_install sed
build_rpm_in_chroot_no_install perl
build_rpm_in_chroot_no_install nss
build_rpm_in_chroot_no_install flex
build_rpm_in_chroot_no_install libarchive
build_rpm_in_chroot_no_install diffutils
build_rpm_in_chroot_no_install mariner-release

# Need to install perl-DBI in order for perl-DBD-SQLite to build
build_rpm_in_chroot_no_install perl-DBI
chroot_and_install_rpms perl-DBI

build_rpm_in_chroot_no_install perl-Object-Accessor
build_rpm_in_chroot_no_install bison
build_rpm_in_chroot_no_install autoconf
build_rpm_in_chroot_no_install texinfo
build_rpm_in_chroot_no_install perl-DBD-SQLite
build_rpm_in_chroot_no_install perl-DBIx-Simple
build_rpm_in_chroot_no_install elfutils
build_rpm_in_chroot_no_install automake

# Need to install perl-Text-Template and perl-Test-Warnings
# to build openssl
build_rpm_in_chroot_no_install perl-Test-Warnings
chroot_and_install_rpms perl-Test-Warnings
build_rpm_in_chroot_no_install perl-Text-Template
chroot_and_install_rpms perl-Text-Template
build_rpm_in_chroot_no_install openssl

build_rpm_in_chroot_no_install wget
build_rpm_in_chroot_no_install freetype

# build and install additional openjdk build dependencies
build_rpm_in_chroot_no_install pcre
chroot_and_install_rpms pcre
build_rpm_in_chroot_no_install which
chroot_and_install_rpms which
build_rpm_in_chroot_no_install zip
chroot_and_install_rpms zip
build_rpm_in_chroot_no_install unzip
chroot_and_install_rpms unzip
build_rpm_in_chroot_no_install alsa-lib
chroot_and_install_rpms alsa-lib

# Build OpenJDK and OpenJRE
echo Java bootstrap version:
case $(uname -m) in
    x86_64)
        echo $($LFS/usr/lib/jvm/OpenJDK-212-b04-bootstrap/bin/java -version)
        build_rpm_in_chroot_no_install openjdk8
    ;;
    aarch64)
        echo $($LFS/usr/lib/jvm/OpenJDK-1.8.0.181-bootstrap/bin/java -version)
        build_rpm_in_chroot_no_install openjdk8_aarch64
    ;;
esac

# Install OpenJDK and OpenJRE
chroot_and_install_rpms openjdk8
# Copy OpenJRE
cp -v $CHROOT_RPMS_DIR_ARCH/openjre8* $FINISHED_RPM_DIR
chroot_and_install_rpms openjre8

# PCRE needs to be installed (above) for grep to build with perl regexp support
build_rpm_in_chroot_no_install grep

# Python2 needs to be installed for RPM to build
build_rpm_in_chroot_no_install python2
rm -vf $FINISHED_RPM_DIR/python2*debuginfo*.rpm
chroot_and_install_rpms python2

# Lua needs to be installed for RPM to build
build_rpm_in_chroot_no_install lua
chroot_and_install_rpms lua

build_rpm_in_chroot_no_install cpio

# Build tdnf-2.1.0
build_rpm_in_chroot_no_install kmod
build_rpm_in_chroot_no_install perl-XML-Parser
build_rpm_in_chroot_no_install libssh2
build_rpm_in_chroot_no_install perl-libintl-perl
build_rpm_in_chroot_no_install gperf
build_rpm_in_chroot_no_install python-setuptools
build_rpm_in_chroot_no_install libgpg-error

# intltool needs perl-XML-Parser
chroot_and_install_rpms perl-XML-Parser
build_rpm_in_chroot_no_install intltool
build_rpm_in_chroot_no_install check
build_rpm_in_chroot_no_install e2fsprogs

# libgcrypt needs libgpg-error
chroot_and_install_rpms libgpg-error
build_rpm_in_chroot_no_install libgcrypt
build_rpm_in_chroot_no_install kbd

# krb5 needs e2fsprogs
chroot_and_install_rpms e2fsprogs
build_rpm_in_chroot_no_install krb5

# curl needs libssh2
chroot_and_install_rpms libssh2
build_rpm_in_chroot_no_install curl
build_rpm_in_chroot_no_install libxml2

# python-setuptools needs python-xml
# python-xml is built by building python2
chroot_and_install_rpms python-xml

# cracklib needs python-setuptools
chroot_and_install_rpms python-setuptools
build_rpm_in_chroot_no_install cracklib

# pam needs cracklib
chroot_and_install_rpms cracklib

build_rpm_in_chroot_no_install cmake
build_rpm_in_chroot_no_install pam
build_rpm_in_chroot_no_install docbook-dtd-xml

# libxslt needs libxml2, libgcrypt
chroot_and_install_rpms libxml2
chroot_and_install_rpms libgcrypt
build_rpm_in_chroot_no_install libxslt

# docbook-style-xsl needs pam
chroot_and_install_rpms pam
build_rpm_in_chroot_no_install docbook-style-xsl

# gtest needs cmake
chroot_and_install_rpms cmake
build_rpm_in_chroot_no_install gtest

build_rpm_in_chroot_no_install libsolv

# glib needs perl-XML-Parser, python-xml
chroot_and_install_rpms perl-XML-Parser

build_rpm_in_chroot_no_install glib
build_rpm_in_chroot_no_install libassuan
build_rpm_in_chroot_no_install npth
build_rpm_in_chroot_no_install libksba

# gnupg2 requires zlib, bzip2, readline, npth, libassuan, libksba
chroot_and_install_rpms zlib
chroot_and_install_rpms bzip2
chroot_and_install_rpms readline
chroot_and_install_rpms npth
chroot_and_install_rpms libassuan
chroot_and_install_rpms libksba
build_rpm_in_chroot_no_install gnupg2
build_rpm_in_chroot_no_install swig

# gpgme needs swig, gnupg2 and python3
chroot_and_install_rpms swig
chroot_and_install_rpms gnupg2
chroot_and_install_rpms python3
build_rpm_in_chroot_no_install gpgme

# tdnf needs python3, gpgme, curl and libsolv
chroot_and_install_rpms libsolv
chroot_and_install_rpms curl

chroot_and_install_rpms gpgme
build_rpm_in_chroot_no_install pinentry

build_rpm_in_chroot_no_install tdnf

# Build createrepo_c-0.11.1
# createrepo_c needs glib
chroot_and_install_rpms glib
build_rpm_in_chroot_no_install createrepo_c

# ca-certificates requires libxslt
chroot_and_install_rpms docbook-dtd-xml
chroot_and_install_rpms docbook-style-xsl
chroot_and_install_rpms libxslt
build_rpm_in_chroot_no_install itstool

# gtk-doc needs itstool
chroot_and_install_rpms itstool
build_rpm_in_chroot_no_install gtk-doc

# p11-kit and libtasn1 needs gtk-doc
chroot_and_install_rpms gtk-doc
build_rpm_in_chroot_no_install libtasn1

# ninja-build requires gtest
chroot_and_install_rpms gtest
build_rpm_in_chroot_no_install ninja-build

# meson requires ninja-build, gettext
chroot_and_install_rpms ninja-build
chroot_and_install_rpms gettext
build_rpm_in_chroot_no_install meson

build_rpm_in_chroot_no_install libpwquality
build_rpm_in_chroot_no_install json-c
build_rpm_in_chroot_no_install libsepol

# libselinux requires libsepol
chroot_and_install_rpms libsepol
build_rpm_in_chroot_no_install libselinux

# util-linux, rpm, libsemanage and shadow-utils require libselinux
chroot_and_install_rpms libselinux
build_rpm_in_chroot_no_install util-linux
build_rpm_in_chroot_no_install rpm

build_rpm_in_chroot_no_install pam

# systemd-bootstrap requires libcap, xz, kbd, kmod, util-linux, meson
chroot_and_install_rpms libcap
chroot_and_install_rpms lz4
chroot_and_install_rpms xz
chroot_and_install_rpms kbd
chroot_and_install_rpms kmod
chroot_and_install_rpms util-linux
chroot_and_install_rpms meson
build_rpm_in_chroot_no_install systemd-bootstrap
build_rpm_in_chroot_no_install libaio

# lvm2 requires libselinux, libsepol, ncurses, systemd-bootstrap, libaio,
chroot_and_install_rpms libselinux
chroot_and_install_rpms libsepol
chroot_and_install_rpms ncurses
chroot_and_install_rpms systemd-bootstrap
chroot_and_install_rpms libaio

# lvm2 provides device-mapper package
build_rpm_in_chroot_no_install lvm2

# cryptsetup requires popt, device-mapper, libpwquality, json-c
chroot_and_install_rpms popt
chroot_and_install_rpms device-mapper
chroot_and_install_rpms libpwquality
chroot_and_install_rpms json-c
build_rpm_in_chroot_no_install cryptsetup

# systemd needs intltool, gperf, util-linux
chroot_and_install_rpms intltool
chroot_and_install_rpms gperf
chroot_and_install_rpms cryptsetup
build_rpm_in_chroot_no_install systemd

build_rpm_in_chroot_no_install golang-1.15
build_rpm_in_chroot_no_install groff

# libtiprc needs krb5
chroot_and_install_rpms krb5
build_rpm_in_chroot_no_install libtirpc
build_rpm_in_chroot_no_install rpcsvc-proto

# libnsl2 needs libtirpc and rpcsvc-proto
chroot_and_install_rpms libtirpc
chroot_and_install_rpms rpcsvc-proto
build_rpm_in_chroot_no_install libnsl2

build_rpm_in_chroot_no_install finger

# tcp_wrappers needs libnsl2, finger
chroot_and_install_rpms libnsl2
chroot_and_install_rpms finger
build_rpm_in_chroot_no_install tcp_wrappers

build_rpm_in_chroot_no_install cyrus-sasl

# openldap needs groff, cyrus-sasl
chroot_and_install_rpms groff
chroot_and_install_rpms cyrus-sasl
build_rpm_in_chroot_no_install openldap

build_rpm_in_chroot_no_install libcap-ng

# audit needs systemd, golang, openldap, tcp_wrappers and libcap-ng
chroot_and_install_rpms systemd
chroot_and_install_rpms golang
chroot_and_install_rpms openldap
chroot_and_install_rpms tcp_wrappers
chroot_and_install_rpms libcap-ng
build_rpm_in_chroot_no_install audit

# libsemanage requires libaudit
chroot_and_install_rpms audit
build_rpm_in_chroot_no_install libsemanage

# shadow-utils requires libsemanage
chroot_and_install_rpms libsemanage
# shadow-utils needs the pam.d sources in the root of SOURCES_DIR
cp $SPECROOT/shadow-utils/pam.d/* $CHROOT_SOURCES_DIR
build_rpm_in_chroot_no_install shadow-utils

# p11-kit needs libtasn1
chroot_and_install_rpms libtasn1
build_rpm_in_chroot_no_install p11-kit

# asciidoc needs python-xml
build_rpm_in_chroot_no_install asciidoc

# ca-certificates needs p11-kit and asciidoc
chroot_and_install_rpms p11-kit
chroot_and_install_rpms asciidoc
build_rpm_in_chroot_no_install ca-certificates

build_rpm_in_chroot_no_install mariner-repos

chroot_and_print_installed_rpms

# Ensure all RPMS are copied out of the chroot
echo Copying all built RPMS from chroot
cp -v $CHROOT_RPMS_DIR_ARCH/* $FINISHED_RPM_DIR
cp -v $CHROOT_RPMS_DIR_NOARCH/* $FINISHED_RPM_DIR

echo Finished building final list of toolchain RPMs
chroot_unmount
ls -la $FINISHED_RPM_DIR
ls -la $FINISHED_RPM_DIR | wc
