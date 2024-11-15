Summary:        Metapackage of tools required to build Azure Linux packages
Name:           azurelinux-tools-packagebuild
Version:        %{azl}.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/mariner

# Start with bases
Requires: build-essential
Requires: core-packages-container

# Additional core requirements
Requires: audit
Requires: azurelinux-check-macros
Requires: ca-certificates
Requires: createrepo_c
Requires: dwz
Requires: flex
Requires: glib
Requires: glibc-iconv
Requires: glibc-locales-all
Requires: glibc-nscd
Requires: glibc-tools
Requires: libltdl
Requires: libmetalink
Requires: libpipeline
Requires: msopenjdk-17
Requires: ncurses-compat
Requires: ncurses-term
Requires: ocaml-srpm-macros
Requires: openssl-perl
Requires: openssl-static
Requires: perl
Requires: procps-ng
Requires: pyproject-rpm-macros
Requires: python3-rpm-generators
Requires: python3-setuptools
Requires: rpm-build
Requires: sqlite
Requires: util-linux
Requires: texinfo
Requires: which

# -lang requirements
Requires: bash-lang
Requires: chkconfig-lang
Requires: coreutils-lang
Requires: cpio-lang
Requires: elfutils-libelf-lang
Requires: findutils-lang
Requires: gdbm-lang
Requires: glibc-lang
Requires: gnupg2-lang
Requires: grep-lang
Requires: newt-lang
Requires: popt-lang
Requires: procps-ng-lang
Requires: rpm-lang
Requires: sed-lang
Requires: xz-lang

# -devel requirements
Requires: bash-devel
Requires: binutils-devel
Requires: bzip2-devel
Requires: curl-devel
Requires: elfutils-devel
Requires: elfutils-devel-static
Requires: elfutils-libelf-devel
Requires: elfutils-libelf-devel-static
Requires: expat-devel
Requires: file-devel
Requires: flex-devel
Requires: gdbm-devel
Requires: glibc-devel
Requires: gmp-devel
Requires: libarchive-devel
Requires: libassuan-devel
Requires: libcap-devel
Requires: libcap-ng-devel
Requires: libffi-devel
Requires: libgcc-devel
Requires: libgomp-devel
Requires: libksba-devel
Requires: libltdl-devel
Requires: libpipeline-devel
Requires: libsolv-devel
Requires: libssh2-devel
Requires: libstdc++-devel
Requires: libxcrypt-devel
Requires: libxml2-devel
Requires: mpfr-devel
Requires: ncurses-devel
Requires: openssl-devel
Requires: popt-devel
Requires: procps-ng-devel
Requires: python3-devel
Requires: readline-devel
Requires: rpm-devel
Requires: sqlite-devel
Requires: tdnf-devel
Requires: util-linux-devel
Requires: xz-devel
Requires: zlib-devel
Requires: zstd-devel

%description
Metapackage of tools required to build Azure Linux packages

%prep

%build

%files

%changelog
* Thu Oct 17 2024 Reuben Olinsky <reubeno@microsoft.com> - 3.0-1
- Initial version of package.
