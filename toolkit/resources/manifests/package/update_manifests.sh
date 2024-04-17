#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

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
    ToolchainManifest=toolchain_"$1".txt
    PkggenManifest=pkggen_core_"$1".txt
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
    tar -tf "$TOOLCHAIN_ARCHIVE" | sed 's+built_rpms_all/++g' | sed '/^$/d' > "$ToolchainManifest"
    # Now sort the file in place
    LC_COLLATE=C sort -f -o "$ToolchainManifest" "$ToolchainManifest"
}

# Remove specific packages that are not needed in pkggen_core
remove_packages_for_pkggen_core () {
    sed -i '/audit-devel/d' $TmpPkgGen
    sed -i '/ca-certificates-legacy/d' $TmpPkgGen
    sed -i '/libtasn1-d/d' $TmpPkgGen
    sed -i '/libpkgconf-devel/d' $TmpPkgGen
    sed -i '/lua-static/d' $TmpPkgGen
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
    sed -i '/freetype2/d' $TmpPkgGen
    sed -i '/gfortran/d' $TmpPkgGen
    sed -i '/glib-devel/d' $TmpPkgGen
    sed -i '/glib-schemas/d' $TmpPkgGen
    sed -i '/glib-doc/d' $TmpPkgGen
    sed -i '/gperf/d' $TmpPkgGen
    sed -i '/gpgme-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/kbd/d' $TmpPkgGen
    sed -i '/kmod/d' $TmpPkgGen
    sed -i '/krb5-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/libarchive/d' $TmpPkgGen
    sed -i '/libbacktrace-static/d' $TmpPkgGen
    sed -i '/libgpg-error-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/libgcrypt-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/libselinux-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/libsepol-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/libsolv-tools/d' $TmpPkgGen
    sed -i '/libxslt/d' $TmpPkgGen
    sed -i '/Linux-PAM/d' $TmpPkgGen
    sed -i '/lua-devel/d' $TmpPkgGen
    sed -i '/lua-rpm/d' $TmpPkgGen
    sed -i '/lua-srpm/d' $TmpPkgGen
    sed -ri '/azurelinux-repos-(debug|extended|extras|microsoft)/d' $TmpPkgGen
    sed -i '/nghttp2-devel/d' $TmpPkgGen
    sed -i '/npth-[[:alpha:]]/d' $TmpPkgGen
    sed -i '/perl-5/d' $TmpPkgGen
    sed -i '/perl-A/d' $TmpPkgGen
    sed -i '/perl-a/d' $TmpPkgGen
    sed -i '/perl-Benchmark/d' $TmpPkgGen
    sed -i '/perl-bignum/d' $TmpPkgGen
    sed -i '/perl-blib/d' $TmpPkgGen
    sed -i '/perl-Compress/d' $TmpPkgGen
    sed -i '/perl-Config/d' $TmpPkgGen
    sed -i '/perl-CPAN/d' $TmpPkgGen
    sed -i '/perl-DB/d' $TmpPkgGen
    sed -i '/perl-Digest/d' $TmpPkgGen
    sed -i '/perl-Dir/d' $TmpPkgGen
    sed -i '/perl-Dump/d' $TmpPkgGen
    sed -i '/perl-de/d' $TmpPkgGen
    sed -i '/perl-Devel/d' $TmpPkgGen
    sed -i '/perl-diagnostics/d' $TmpPkgGen
    sed -i '/perl-doc/d' $TmpPkgGen
    sed -i '/perl-Encode-devel/d' $TmpPkgGen
    sed -i '/perl-encoding/d' $TmpPkgGen
    sed -i '/perl-English/d' $TmpPkgGen
    sed -i '/perl-Env/d' $TmpPkgGen
    sed -i '/perl-experimental/d' $TmpPkgGen
    sed -i '/perl-ExtUtils/d' $TmpPkgGen
    sed -i '/perl-Fedora-VSP/d' $TmpPkgGen
    sed -i '/perl-fields/d' $TmpPkgGen
    sed -i '/perl-File-Dos/d' $TmpPkgGen
    sed -i '/perl-File-Fetch/d' $TmpPkgGen
    sed -i '/perl-File-Find/d' $TmpPkgGen
    sed -i '/perl-FileCache/d' $TmpPkgGen
    sed -i '/perl-filetest/d' $TmpPkgGen
    sed -i '/perl-Filter/d' $TmpPkgGen
    sed -i '/perl-Find/d' $TmpPkgGen
    sed -i '/perl-GDBM_File/d' $TmpPkgGen
    sed -i '/perl-generators/d' $TmpPkgGen
    sed -i '/perl-Hash/d' $TmpPkgGen
    sed -i '/perl-I18N-Collate/d' $TmpPkgGen
    sed -i '/perl-I18N-LangTags/d' $TmpPkgGen
    sed -i '/perl-IO-Compress/d' $TmpPkgGen
    sed -i '/perl-IO-Socket/d' $TmpPkgGen
    sed -i '/perl-IO-Zlib/d' $TmpPkgGen
    sed -i '/perl-IPC-Cmd/d' $TmpPkgGen
    sed -i '/perl-IPC-SysV/d' $TmpPkgGen
    sed -i '/perl-JSON/d' $TmpPkgGen
    sed -i '/perl-less/d' $TmpPkgGen
    sed -i '/perl-lib-/d' $TmpPkgGen
    sed -i '/perl-libnet/d' $TmpPkgGen
    sed -i '/perl-libintl/d' $TmpPkgGen
    sed -i '/perl-Locale/d' $TmpPkgGen
    sed -i '/perl-Math/d' $TmpPkgGen
    sed -i '/perl-Memoize/d' $TmpPkgGen
    sed -i '/perl-meta/d' $TmpPkgGen
    sed -i '/perl-Module/d' $TmpPkgGen
    sed -i '/perl-mro/d' $TmpPkgGen
    sed -i '/perl-NDBM_File/d' $TmpPkgGen
    sed -i '/perl-Net/d' $TmpPkgGen
    sed -i '/perl-NEXT/d' $TmpPkgGen
    sed -i '/perl-ODBM_File/d' $TmpPkgGen
    sed -i '/perl-Opcode/d' $TmpPkgGen
    sed -i '/perl-open/d' $TmpPkgGen
    sed -i '/perl-Params/d' $TmpPkgGen
    sed -i '/perl-Perl/d' $TmpPkgGen
    sed -i '/perl-perlfaq/d' $TmpPkgGen
    sed -i '/perl-ph/d' $TmpPkgGen
    sed -i '/perl-Pod-Checker/d' $TmpPkgGen
    sed -i '/perl-Pod-Functions/d' $TmpPkgGen
    sed -i '/perl-Pod-Html/d' $TmpPkgGen
    sed -i '/perl-Pod-Safe/d' $TmpPkgGen
    sed -i '/perl-Pod-Search/d' $TmpPkgGen
    sed -i '/perl-Pod-SelfLoader/d' $TmpPkgGen
    sed -i '/perl-Pod-sigtrap/d' $TmpPkgGen
    sed -i '/perl-Pod-sort/d' $TmpPkgGen
    sed -i '/perl-Pod-subs/d' $TmpPkgGen
    sed -i '/perl-Pod-Sys/d' $TmpPkgGen
    sed -i '/perl-Pod-Term-Complete/d' $TmpPkgGen
    sed -i '/perl-Pod-Term-ReadLine/d' $TmpPkgGen
    sed -i '/perl-Safe/d' $TmpPkgGen
    sed -i '/perl-Search/d' $TmpPkgGen
    sed -i '/perl-SelfLoader/d' $TmpPkgGen
    sed -i '/perl-sigtrap/d' $TmpPkgGen
    sed -i '/perl-sort/d' $TmpPkgGen
    sed -i '/perl-Sys/d' $TmpPkgGen
    sed -i '/perl-Test/d' $TmpPkgGen
    sed -i '/perl-tests/d' $TmpPkgGen
    sed -i '/perl-Term-Complete/d' $TmpPkgGen
    sed -i '/perl-Term-ReadLine/d' $TmpPkgGen
    sed -i '/perl-Text-Abbrev/d' $TmpPkgGen
    sed -i '/perl-Text-Balanced/d' $TmpPkgGen
    sed -i '/perl-Thread-3/d' $TmpPkgGen
    sed -i '/perl-Thread-Semaphore/d' $TmpPkgGen
    sed -i '/perl-Tie/d' $TmpPkgGen
    sed -i '/perl-Time-1/d' $TmpPkgGen
    sed -i '/perl-Time-HiRes/d' $TmpPkgGen
    sed -i '/perl-Time-Piece/d' $TmpPkgGen
    sed -i '/perl-Unicode-Collate/d' $TmpPkgGen
    sed -i '/perl-Unicode-UCD/d' $TmpPkgGen
    sed -i '/perl-User/d' $TmpPkgGen
    sed -i '/perl-utils/d' $TmpPkgGen
    sed -i '/perl-version/d' $TmpPkgGen
    sed -i '/perl-vmsish/d' $TmpPkgGen
    sed -i '/perl-libintl/d' $TmpPkgGen
    sed -i '/perl-Test-Warnings/d' $TmpPkgGen
    sed -i '/perl-Text-Template/d' $TmpPkgGen
    sed -i '/python3-audit/d' $TmpPkgGen
    sed -i '/python3-curses/d' $TmpPkgGen
    sed -i '/python3-Cython/d' $TmpPkgGen
    sed -i '/python3-gpg/d' $TmpPkgGen
    sed -i '/python3-libxml2/d' $TmpPkgGen
    sed -i '/python3-lxml/d' $TmpPkgGen
    sed -i '/python3-magic/d' $TmpPkgGen
    sed -i '/python3-pip/d' $TmpPkgGen
    sed -i '/python3-rpm/d' $TmpPkgGen
    sed -i '/python3-test/d' $TmpPkgGen
    sed -i '/python3-tools/d' $TmpPkgGen
    sed -i '/tdnf-python/d' $TmpPkgGen
    sed -i '/util-linux-lang/d' $TmpPkgGen
    sed -i '/XML-Parser/d' $TmpPkgGen
    sed -i '/^zstd-doc/d' $TmpPkgGen
    sed -i '/^zip-/d' $TmpPkgGen
}

# create pkggen_core file in correct order
generate_pkggen_core () {
    # $1 = (pkggen_core_x86_64.txt or pkggen_core_aarch64.txt)
    {
        grep "^filesystem-" $TmpPkgGen
        grep "^kernel-headers-" $TmpPkgGen
        grep "^glibc-" $TmpPkgGen
        grep "^zlib-" $TmpPkgGen
        grep "^file-" $TmpPkgGen
        grep "^binutils-" $TmpPkgGen
        grep "^gmp-" $TmpPkgGen
        grep "^mpfr-" $TmpPkgGen
        grep "^libmetalink-[0-9]" $TmpPkgGen
        grep "^libmpc-" $TmpPkgGen
        grep "^libgcc-" $TmpPkgGen
        grep "^libstdc++-" $TmpPkgGen
        grep "^libgomp-" $TmpPkgGen
        grep "^gcc-" $TmpPkgGen
        grep "^libpkgconf-" $TmpPkgGen
        grep "^pkgconf-" $TmpPkgGen
        grep "^ncurses-" $TmpPkgGen
        grep "^readline-" $TmpPkgGen
        grep "^coreutils-" $TmpPkgGen
        grep "^bash-" $TmpPkgGen
        grep "^bzip2-" $TmpPkgGen
        grep "^sed-" $TmpPkgGen
        grep "^procps-ng-" $TmpPkgGen
        grep "^m4-" $TmpPkgGen
        grep "^grep-" $TmpPkgGen
        grep "^diffutils-" $TmpPkgGen
        grep "^gawk-" $TmpPkgGen
        grep "^findutils-" $TmpPkgGen
        grep "^gettext-" $TmpPkgGen
        grep "^gzip-" $TmpPkgGen
        grep "^make-" $TmpPkgGen
        grep "^patch-" $TmpPkgGen
        grep "^libcap-ng-" $TmpPkgGen
        grep "^util-linux-" $TmpPkgGen
        grep "^tar-" $TmpPkgGen
        grep "^xz-" $TmpPkgGen
        grep "^zstd-" $TmpPkgGen
        grep "^libtool-" $TmpPkgGen
        grep "^flex-" $TmpPkgGen
        grep "^bison-" $TmpPkgGen
        grep "^popt-" $TmpPkgGen
        grep "^sqlite-" $TmpPkgGen
        grep "^elfutils-" $TmpPkgGen
        grep "^expat-" $TmpPkgGen
        grep "^libpipeline-" $TmpPkgGen
        grep "^gdbm-" $TmpPkgGen
        grep "^perl-" $TmpPkgGen
        grep "^texinfo-" $TmpPkgGen
        grep "^gtk-doc-" $TmpPkgGen
        grep "^autoconf-" $TmpPkgGen
        grep "^automake-" $TmpPkgGen
        grep "^openssl-" $TmpPkgGen
        grep "^libcap-" $TmpPkgGen
        grep "^debugedit-" $TmpPkgGen
        grep "^rpm-" $TmpPkgGen
        grep "^cpio-" $TmpPkgGen
        grep "^e2fsprogs-" $TmpPkgGen
        grep "^libsolv-" $TmpPkgGen
        grep "^libssh2-" $TmpPkgGen
        grep "^krb5-" $TmpPkgGen
        grep "^nghttp2-" $TmpPkgGen
        grep "^curl-" $TmpPkgGen
        grep "^tdnf-" $TmpPkgGen
        grep "^createrepo_c-" $TmpPkgGen
        grep "^libxml2-" $TmpPkgGen
        grep "^libsepol-" $TmpPkgGen
        grep "^glib-" $TmpPkgGen
        grep "^libltdl-" $TmpPkgGen
        grep "^lua-" $TmpPkgGen
        grep "^azurelinux-rpm-macros-" $TmpPkgGen
        grep "^mariner-check-" $TmpPkgGen
        grep "^libassuan-" $TmpPkgGen
        grep "^libgpg-error-" $TmpPkgGen
        grep "^libgcrypt-" $TmpPkgGen
        grep "^libksba-" $TmpPkgGen
        grep "^npth-" $TmpPkgGen
        grep "^pinentry-" $TmpPkgGen
        grep "^gnupg2-" $TmpPkgGen
        grep "^gpgme-" $TmpPkgGen
        grep "^azurelinux-repos-shared" $TmpPkgGen
        grep "^azurelinux-repos" $TmpPkgGen
        grep "^libffi-" $TmpPkgGen
        grep "^libtasn1-" $TmpPkgGen
        grep "^p11-kit-" $TmpPkgGen
        grep "^ca-certificates-shared-" $TmpPkgGen
        grep "^ca-certificates-tools-" $TmpPkgGen
        grep "^ca-certificates-base-" $TmpPkgGen
        grep "^ca-certificates-[0-9]" $TmpPkgGen
        grep "^dwz-" $TmpPkgGen
        grep "^unzip-" $TmpPkgGen
        grep "^python3-" $TmpPkgGen
        grep "^which-" $TmpPkgGen
        grep "^libselinux-" $TmpPkgGen
        grep "^slang-[0-9]" $TmpPkgGen
        grep "^newt-[0-9]" $TmpPkgGen
        grep "^newt-lang-[0-9]" $TmpPkgGen
        grep "^chkconfig-[0-9]" $TmpPkgGen
        grep "^chkconfig-lang-[0-9]" $TmpPkgGen
        grep "^msopenjdk-" $TmpPkgGen
        grep "^pyproject-" $TmpPkgGen
        grep "^audit-" $TmpPkgGen
    } > "$1"
}

# Generate toolchain_*.txt based on the toolchain_built_rpms_all.tar.gz file contents
generate_toolchain

# Next, generate pkggen_core_*.txt
# Note that toolchain_*.txt is a superset of pkggen_core_*.txt
# Create a temp file that can be edited to remove the unnecessary files
cp "$ToolchainManifest" $TmpPkgGen

# Remove all *-debuginfo subpackages
sed -i '/debuginfo/d' $TmpPkgGen

# Modify the temp file by removing other unneeded packages
remove_packages_for_pkggen_core

# Now create pkggen_core_*.txt file in correct order
# The packages are listed in the order they will be installed into the chroot
generate_pkggen_core "$PkggenManifest"

rm $TmpPkgGen
