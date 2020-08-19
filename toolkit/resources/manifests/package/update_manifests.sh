#!/bin/bash

print_usage() {
    echo "Usage:"
    echo "update_manifests.sh x86_64|aarch64 ./toolchain_built_rpms_all.tar.gz"
    echo
    echo "Run this script to automatically update toolchain_*.txt and pkggen_core_*.txt based on the contents of toolchain_built_rpms_all.tar.gz"
    exit
}

TmpPkgGen=pkggen_core_temp.txt

if [ -z "$1" ] || [ -z "$2" ]; then
    print_usage
fi

if [[ "$1" == "x86_64" ]] || [[ "$1" == "aarch64" ]]; then
    Arch=$1
else
    echo "Invalid architecture: '$1'"
    print_usage
fi

if [ -f "$2" ]; then
    TOOLCHAIN_ARCHIVE=$2
else
    echo "Bad toolchain parameter: '$2' does not exist"
    print_usage
fi

echo Updating files...

generate_toolchain () {
    # First generate toolchain_*.txt from TOOLCHAIN_ARCHIVE (toolchain_built_rpms_all.tar.gz)
    # This file is a sorted list of all toolchain packages in the tarball.
    tar -ztf $TOOLCHAIN_ARCHIVE | sed 's+built_rpms_all/++g' | sed '/^$/d' > toolchain_$Arch.txt
    # Now sort the file in place
    sort -o toolchain_$Arch.txt toolchain_$Arch.txt
}

# Remove specific packages that are not needed in pkggen_core
remove_packages_for_pkggen_core () {
    sed -i '/alsa-lib-/d' $TmpPkgGen
    sed -i '/ca-certificates-[0-9]/d' $TmpPkgGen
    sed -i '/libtasn1-d/d' $TmpPkgGen
    sed -i '/libffi-d/d' $TmpPkgGen
    sed -i '/p11-kit-d/d' $TmpPkgGen
    sed -i '/p11-kit-server/d' $TmpPkgGen
    sed -i '/^check/d' $TmpPkgGen
    sed -i '/cmake/d' $TmpPkgGen
    sed -i '/cracklib/d' $TmpPkgGen
    sed -i '/createrepo_c-devel/d' $TmpPkgGen
    sed -i '/docbook-xml/d' $TmpPkgGen
    sed -i '/docbook-xsl/d' $TmpPkgGen
    sed -i '/e2fsprogs-[0-9]/d' $TmpPkgGen
    sed -i '/e2fsprogs-devel/d' $TmpPkgGen
    sed -i '/e2fsprogs-lang/d' $TmpPkgGen
    sed -i '/openj/d' $TmpPkgGen
    sed -i '/freetype2/d' $TmpPkgGen
    sed -i '/gfortran/d' $TmpPkgGen
    sed -i '/glib-devel/d' $TmpPkgGen
    sed -i '/glib-schemas/d' $TmpPkgGen
    sed -i '/gmock/d' $TmpPkgGen
    sed -i '/gperf/d' $TmpPkgGen
    sed -i '/gpgme-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/gtest/d' $TmpPkgGen
    sed -i '/kbd/d' $TmpPkgGen
    sed -i '/kmod/d' $TmpPkgGen
    sed -i '/krb5-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/libarchive/d' $TmpPkgGen
    sed -i '/libgpg-error-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/libsolv-tools/d' $TmpPkgGen
    sed -i '/libxml2-python/d' $TmpPkgGen
    sed -i '/libxslt/d' $TmpPkgGen
    sed -i '/Linux-PAM/d' $TmpPkgGen
    sed -i '/lua-devel/d' $TmpPkgGen
    sed -i '/npth-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/pcre-[0-9]/d' $TmpPkgGen
    sed -i '/pcre-devel/d' $TmpPkgGen
    sed -i '/perl-D/d' $TmpPkgGen
    sed -i '/perl-libintl/d' $TmpPkgGen
    sed -i '/perl-Object-Accessor/d' $TmpPkgGen
    sed -i '/perl-Test-Warnings/d' $TmpPkgGen
    sed -i '/perl-Text-Template/d' $TmpPkgGen
    sed -i '/python/d' $TmpPkgGen
    sed -i '/shadow/d' $TmpPkgGen
    sed -i '/unzip/d' $TmpPkgGen
    sed -i '/util-linux-lang/d' $TmpPkgGen
    sed -i '/wget/d' $TmpPkgGen
    sed -i '/which/d' $TmpPkgGen
    sed -i '/XML-Parser/d' $TmpPkgGen
    sed -i '/^zstd-doc/d' $TmpPkgGen
    sed -i '/^zip-/d' $TmpPkgGen
}

# create pkggen_core file in correct order
generate_pkggen_core () {
    # $1 = (pkggen_core_x86_64.txt or pkggen_core_aarch64.txt)
    cat $TmpPkgGen | grep "^filesystem-" > $1
    cat $TmpPkgGen | grep "^kernel-headers-" >> $1
    cat $TmpPkgGen | grep "^glibc-" >> $1
    cat $TmpPkgGen | grep "^zlib-" >> $1
    cat $TmpPkgGen | grep "^file-" >> $1
    cat $TmpPkgGen | grep "^binutils-" >> $1
    cat $TmpPkgGen | grep "^gmp-" >> $1
    cat $TmpPkgGen | grep "^mpfr-" >> $1
    cat $TmpPkgGen | grep "^libmpc-" >> $1
    cat $TmpPkgGen | grep "^libgcc-" >> $1
    cat $TmpPkgGen | grep "^libstdc++-" >> $1
    cat $TmpPkgGen | grep "^libgomp-" >> $1
    cat $TmpPkgGen | grep "^gcc-" >> $1
    cat $TmpPkgGen | grep "^pkg-config-" >> $1
    cat $TmpPkgGen | grep "^ncurses-" >> $1
    cat $TmpPkgGen | grep "^readline-" >> $1
    cat $TmpPkgGen | grep "^coreutils-" >> $1
    cat $TmpPkgGen | grep "^bash-" >> $1
    cat $TmpPkgGen | grep "^bzip2-" >> $1
    cat $TmpPkgGen | grep "^sed-" >> $1
    cat $TmpPkgGen | grep "^procps-ng-" >> $1
    cat $TmpPkgGen | grep "^m4-" >> $1
    cat $TmpPkgGen | grep "^grep-" >> $1
    cat $TmpPkgGen | grep "^diffutils-" >> $1
    cat $TmpPkgGen | grep "^gawk-" >> $1
    cat $TmpPkgGen | grep "^findutils-" >> $1
    cat $TmpPkgGen | grep "^gettext-" >> $1
    cat $TmpPkgGen | grep "^gzip-" >> $1
    cat $TmpPkgGen | grep "^make-" >> $1
    cat $TmpPkgGen | grep "^mariner-release-" >> $1
    cat $TmpPkgGen | grep "^patch-" >> $1
    cat $TmpPkgGen | grep "^util-linux-" >> $1
    cat $TmpPkgGen | grep "^tar-" >> $1
    cat $TmpPkgGen | grep "^xz-" >> $1
    cat $TmpPkgGen | grep "^zstd-" >> $1
    cat $TmpPkgGen | grep "^libtool-" >> $1
    cat $TmpPkgGen | grep "^flex-" >> $1
    cat $TmpPkgGen | grep "^bison-" >> $1
    cat $TmpPkgGen | grep "^popt-" >> $1
    cat $TmpPkgGen | grep "^nspr-" >> $1
    cat $TmpPkgGen | grep "^sqlite-" >> $1
    cat $TmpPkgGen | grep "^nss-" >> $1
    cat $TmpPkgGen | grep "^elfutils-" >> $1
    cat $TmpPkgGen | grep "^expat-" >> $1
    cat $TmpPkgGen | grep "^libpipeline-" >> $1
    cat $TmpPkgGen | grep "^gdbm-" >> $1
    cat $TmpPkgGen | grep "^perl-" >> $1
    cat $TmpPkgGen | grep "^texinfo-" >> $1
    cat $TmpPkgGen | grep "^autoconf-" >> $1
    cat $TmpPkgGen | grep "^automake-" >> $1
    cat $TmpPkgGen | grep "^openssl-" >> $1
    cat $TmpPkgGen | grep "^libcap-" >> $1
    cat $TmpPkgGen | grep "^libdb-" >> $1
    cat $TmpPkgGen | grep "^rpm-" >> $1
    cat $TmpPkgGen | grep "^cpio-" >> $1
    cat $TmpPkgGen | grep "^e2fsprogs-" >> $1
    cat $TmpPkgGen | grep "^libsolv-" >> $1
    cat $TmpPkgGen | grep "^libssh2-" >> $1
    cat $TmpPkgGen | grep "^curl-" >> $1
    cat $TmpPkgGen | grep "^tdnf-" >> $1
    cat $TmpPkgGen | grep "^createrepo_c-" >> $1
    cat $TmpPkgGen | grep "^libxml2-" >> $1
    cat $TmpPkgGen | grep "^glib-" >> $1
    cat $TmpPkgGen | grep "^libltdl-" >> $1
    cat $TmpPkgGen | grep "^pcre-" >> $1
    cat $TmpPkgGen | grep "^krb5-" >> $1
    cat $TmpPkgGen | grep "^lua-" >> $1
    cat $TmpPkgGen | grep "^mariner-rpm-macros-" >> $1
    cat $TmpPkgGen | grep "^mariner-check-" >> $1
    cat $TmpPkgGen | grep "^libassuan-" >> $1
    cat $TmpPkgGen | grep "^libgpg-error-" >> $1
    cat $TmpPkgGen | grep "^libgcrypt-" >> $1
    cat $TmpPkgGen | grep "^libksba-" >> $1
    cat $TmpPkgGen | grep "^npth-" >> $1
    cat $TmpPkgGen | grep "^pinentry-" >> $1
    cat $TmpPkgGen | grep "^gnupg2-" >> $1
    cat $TmpPkgGen | grep "^gpgme-" >> $1
    cat $TmpPkgGen | grep "^mariner-repos-" >> $1
    cat $TmpPkgGen | grep "^libffi-" >> $1
    cat $TmpPkgGen | grep "^libtasn1-" >> $1
    cat $TmpPkgGen | grep "^p11-kit-" >> $1
    cat $TmpPkgGen | grep "^ca-certificates-shared-" >> $1
    cat $TmpPkgGen | grep "^ca-certificates-tools-" >> $1
    cat $TmpPkgGen | grep "^ca-certificates-base-" >> $1
}

# Generate toolchain_*.txt based on the toolchain_built_rpms_all.tar.gz file contents
generate_toolchain

# Next, generate pkggen_core_*.txt
# Note that toolchain_*.txt is a superset of pkggen_core_*.txt
# Create a temp file that can be edited to remove the unnecessary files
cp toolchain_$Arch.txt $TmpPkgGen

# Remove all *-debuginfo except openssl
R=$(cat toolchain_$Arch.txt | grep openssl-debuginfo)
sed -i '/debuginfo/d' $TmpPkgGen
# Add the openssl-debuginfo file back
echo $R >> $TmpPkgGen

# Modify the temp file by removing other unneeded packages
remove_packages_for_pkggen_core

# Now create pkggen_core_*.txt file in correct order
# The packages are listed in the order they will be installed into the chroot
generate_pkggen_core pkggen_core_$Arch.txt

rm $TmpPkgGen
