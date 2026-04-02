# This spec file has been modified by azldev to include build configuration overlays. Version: v0.1.1-0.20260402002340-3dc8b8a0f4b6
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/kernel-headers.azl.macros}

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

# define buildid .local
%define specversion 6.18.5
%define tarfile_release 6.18.5
# This is needed to do merge window version magic
# This allows pkg_release to have configurable %%{?dist} tag
%define specrelease %{kextraversion}.2%{?dist}

# This package doesn't contain any binary, thus no debuginfo package is needed
%global debug_package %{nil}

Name: kernel-headers
Summary: Header files for the Linux kernel for use by glibc
License: ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-2-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR CDDL-1.0) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND ((GPL-2.0-only WITH Linux-syscall-note) OR MIT) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR MIT) AND BSD-3-Clause AND (GPL-1.0-or-later WITH Linux-syscall-note) AND GPL-2.0-only AND (GPL-2.0-only WITH Linux-syscall-note) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND (LGPL-2.1-only WITH Linux-syscall-note) AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND MIT
URL: http://www.kernel.org/
Version: %{specversion}
Release: %{specrelease}
# This is a tarball with headers from the kernel, which should be created
# using create_headers_tarball.sh provided in the kernel source package.
# To create the tarball, you should go into a prepared/patched kernel sources
# directory, or git kernel source repository, and do eg.:
# For a RHEL package: (...)/create_headers_tarball.sh -m RHEL_RELEASE
# For a Fedora package: kernel/scripts/create_headers_tarball.sh -r <release number>
Source0: https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-%{azurelinux_version}/%{specversion}.%{kextraversion}.tar.gz#/kernel-%{specversion}.%{kextraversion}.tar.gz
Source9999: kernel-headers.azl.macros
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if "0%{?variant}"
Obsoletes: kernel-headers < %{specversion}-%{specrelease}
Provides: kernel-headers = %{specversion}-%{specrelease}
%endif

BuildRequires: make
BuildRequires: gcc
BuildRequires: perl
BuildRequires: rsync
%description
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package -n kernel-cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc

%description -n kernel-cross-headers
Kernel-cross-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
cross-glibc package.

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{azurelinux_version}-%{specversion}.%{kextraversion}

%build

make mrproper
make headers_install INSTALL_HDR_PATH=headers-native

# Determine native kernel arch and cross-compile for the other
native_karch=$(uname -m | sed 's/x86_64/x86/;s/aarch64/arm64/')
for cross_arch in arm64 x86; do
    [ "$cross_arch" = "$native_karch" ] && continue
    make ARCH=$cross_arch headers_install INSTALL_HDR_PATH=headers-$cross_arch
done
%install
native_karch=$(uname -m | sed 's/x86_64/x86/;s/aarch64/arm64/')

mkdir -p $RPM_BUILD_ROOT%{_includedir}
cp -rv headers-native/include/* $RPM_BUILD_ROOT%{_includedir}

for cross_arch in arm64 x86; do
    [ "$cross_arch" = "$native_karch" ] && continue
    cross_arch_includedir=$RPM_BUILD_ROOT%{_prefix}/${cross_arch}-linux-gnu/include
    mkdir -p $cross_arch_includedir
    cp -rv headers-$cross_arch/include/* $cross_arch_includedir
done

exit 0
# List of architectures we support and want to copy their headers
ARCH_LIST="arm arm64 loongarch powerpc riscv s390 x86"

ARCH=%_target_cpu
case $ARCH in
	armv7hl)
		ARCH=arm
		;;
	aarch64)
		ARCH=arm64
		;;
	loongarch64*)
		ARCH=loongarch
		;;
	ppc64*)
		ARCH=powerpc
		;;
	riscv64)
		ARCH=riscv
		;;
	s390x)
		ARCH=s390
		;;
	x86_64|i*86)
		ARCH=x86
		;;
esac

cd arch-$ARCH/include
mkdir -p $RPM_BUILD_ROOT%{_includedir}
cp -a asm-generic $RPM_BUILD_ROOT%{_includedir}

# Copy all the architectures we care about to their respective asm directories
for arch in $ARCH_LIST; do
	mkdir -p $RPM_BUILD_ROOT%{_prefix}/${arch}-linux-gnu/include
	cp -a asm-generic $RPM_BUILD_ROOT%{_prefix}/${arch}-linux-gnu/include/
done

# Remove what we copied already
rm -rf asm-generic

# Copy the rest of the headers over
cp -a * $RPM_BUILD_ROOT%{_includedir}/
for arch in $ARCH_LIST; do
cp -a * $RPM_BUILD_ROOT%{_prefix}/${arch}-linux-gnu/include/
done

%files
%defattr(-,root,root)
%{_includedir}/*

%files -n kernel-cross-headers
%defattr(-,root,root)
%{_prefix}/*-linux-gnu/*

%changelog
%autochangelog
