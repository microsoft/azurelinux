## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
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
## START: Generated by rpmautospec
* Mon Apr 27 2026 azldev <azurelinux@microsoft.com> - 6.18.5-1
- Latest state for kernel-headers

* Fri Jan 02 2026 Justin M. Forbes <jforbes@fedoraproject.org> - 6.18.3-1
- Linux v6.18.3 rebase

* Sun Oct 19 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.4-1
- Linux v6.17.4

* Mon Sep 29 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-8
- Linux v6.17.0

* Mon Sep 22 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-7
- Linux v6.17-rc7

* Mon Sep 15 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-6
- Linux v6.17-rc6

* Mon Sep 08 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-5
- Linux v6.17-rc5

* Mon Sep 01 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-4
- Linux v6.16-rc4

* Mon Aug 25 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-3
- Linux v6.17-rc3

* Mon Aug 18 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-2
- Linux v6.17-rc2

* Mon Aug 11 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.17.0-1
- Linux v6.17-rc1

* Mon Jul 28 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-9
- Linux v6.16

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.16.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-7
- Linux v6.16-rc7

* Mon Jul 14 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-6
- Linux v6.16-rc6

* Mon Jul 07 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-5
- Linux v6.16-rc5

* Mon Jun 30 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-4
- Linux v6.16-rc4

* Mon Jun 23 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-3
- Linux v6.16-rc3

* Mon Jun 16 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-2
- Linux v6.16-rc2

* Tue Jun 10 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.16.0-1
- Linux v6.16-rc1

* Mon May 26 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.15.0-6
- Linux v6.15

* Mon May 19 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.15.0-5
- Linux v6.15-rc7

* Mon May 12 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.15.0-4
- Linux v6.15-rc6

* Mon May 05 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.15.0-3
- Linux v6.15-rc5

* Fri May 02 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.15.0-2
- Linux v6.15-rc4

* Mon Apr 14 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.15.0-1
- Linux v6.15-rc2

* Mon Mar 24 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-8
- Linux v6.14

* Mon Mar 17 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-7
- Linux v6.14-rc7

* Mon Mar 10 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-6
- Linux v6.14-rc6

* Mon Mar 03 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-5
- Linux v6.14-rc5

* Mon Feb 24 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-4
- Linux v6.14-rc4

* Mon Feb 17 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-3
- Linux v6.14-rc3

* Mon Feb 10 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-2
- Linux v6.14-rc2

* Mon Feb 03 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.14.0-1
- Linux v6.14-rc1

* Mon Jan 20 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.13.0-8
- Linux v6.13

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.13.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.13.0-6
- Linux v6.13-rc7

* Mon Jan 06 2025 Justin M. Forbes <jforbes@fedoraproject.org> - 6.13.0-5
- Linux v6.13-rc6

* Mon Dec 30 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.13.0-4
- Linux v6.13-rc5

* Mon Dec 23 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.13.0-3
- Linux v6.13-rc4

* Tue Dec 17 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.13.0-2
- Linux v6.13-rc3

* Mon Dec 02 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.13.0-1
- Linux v6.13-rc1

* Mon Nov 18 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.12.0-5
- Linux v6.12

* Mon Nov 11 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.12.0-4
- Linux v6.12-rc7

* Mon Nov 04 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.12.0-3
- Linux v6.12-rc6

* Mon Oct 28 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.12.0-2
- Linux v6.12-rc5

* Tue Oct 22 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.12.0-1
- Linux v6.12-rc4

* Sun Sep 15 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-8
- Linux v6.11

* Mon Sep 09 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-7
- Linux v6.11-rc7

* Mon Sep 02 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-6
- Linux v6.11-rc6

* Sun Aug 25 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-5
- Linux v6.11-rc5

* Mon Aug 19 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-4
- Linux v6.11-rc4

* Mon Aug 12 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-3
- Linux v6.11-rc3

* Mon Aug 05 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-2
- Linux v6.11-rc2

* Mon Jul 29 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.11.0-1
- Linux v6.11-rc1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-8
- Linux v6.10

* Mon Jul 08 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-7
- Linux v6.10-rc7

* Mon Jul 01 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-6
- Linux v6.10-rc5

* Mon Jun 24 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-5
- Linux v6.10-rc5

* Mon Jun 17 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-4
- Linux v6.10-rc4

* Mon Jun 10 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-3
- Linux v6.10-rc3

* Mon Jun 03 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-2
- Linux v6.10-rc2

* Mon May 27 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.10.0-1
- Linux v6.10-rc1

* Mon May 13 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-8
- Linux v6.9.0

* Mon May 06 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-7
- Linux v6.9-rc7

* Mon Apr 29 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-6
- Linux v6.9-rc6

* Mon Apr 22 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-5
- Linux v6.9-rc5

* Mon Apr 15 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-4
- Linux v6.9-rc4

* Tue Apr 09 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-3
- Linux v6.9-rc3

* Tue Apr 02 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-2
- Linux v6.9-rc2

* Mon Mar 25 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.9.0-1
- Linux v6.9-rc1

* Wed Mar 20 2024 Augusto Caringi <acaringi@redhat.com> - 6.8.1-1
- Linux v6.8.1

* Mon Mar 04 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.8.0-7
- Linux v6.8=rc7

* Mon Feb 26 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.8.0-6
- Linux v6.8-rc6

* Mon Feb 19 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.8.0-5
- Linux v6.8-rc5

* Sun Feb 04 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.8.0-4
- Linux v6.8-rc3

* Mon Jan 29 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.8.0-3
- Linux v6.8-rc2

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.8.0-1
- Linux v6.8-rc1

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-9
- Linux v6.7

* Mon Jan 01 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-8
- Linux v6.7-rc8

* Sun Dec 24 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-7
- Linux v6.7-rc7

* Mon Dec 18 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-6
- Linux v6.7-rc6

* Mon Dec 11 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-5
- Linux v6.7-rc5

* Mon Dec 04 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-4
- Linux v6.7-rc4

* Mon Nov 27 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-3
- Linux v6.7-rc3

* Mon Nov 20 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-2
- Linux v6.7-rc2

* Mon Nov 13 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.7.0-1
- Linux v6.7-rc1

* Mon Oct 30 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-8
- Linux v6.6

* Mon Oct 16 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-7
- Linux v6.6-rc6

* Mon Oct 09 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-6
- Linux v6.6-rc5

* Mon Oct 02 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-5
- Linux v6.6-rc4

* Mon Sep 25 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-4
- Linux v6.6-rc3

* Mon Sep 18 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-3
- Linux v6.6-rc2

* Fri Sep 15 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-2
- Update License field for SPDX

* Mon Sep 11 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.6.0-1
- Linux v6.6-rc1

* Mon Aug 28 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.5.0-338
- Linux v6.5

* Mon Aug 14 2023 Justin M. Forbes <jforbes@fedoraproject.org> - 6.5.0-337
- Rename rpmversion since it is used internally now

* Mon Aug 14 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.5-rc6

* Mon Jul 17 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.5-rc2

* Mon Jun 26 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.4

* Tue Jun 20 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.4-rc7

* Mon Jun 12 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.4-rc6

* Mon Jun 05 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.4-rc5

* Mon May 22 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.4-rc3

* Mon May 15 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.4-r2

* Mon May 08 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.4-rc1

* Mon Apr 24 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3.0

* Mon Apr 17 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3-rc7

* Mon Apr 10 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3-rc6

* Mon Apr 03 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3-rc5

* Tue Mar 28 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3-rc4

* Mon Mar 20 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3-rc3

* Mon Mar 13 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3-rc2

* Mon Mar 06 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.3-rc1

* Mon Feb 20 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.2

* Mon Feb 13 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.2-rc8

* Mon Jan 30 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.2-rc6

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.2-rc4

* Mon Jan 02 2023 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.2-rc2

* Mon Dec 12 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1.0

* Mon Dec 05 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1-rc8

* Mon Nov 28 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1-rc7

* Mon Nov 21 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1-rc6

* Mon Nov 14 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1-rc5

* Mon Nov 07 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1-rc4

* Mon Oct 24 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1-rc2

* Mon Oct 17 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.1-rc1

* Mon Oct 03 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.0

* Mon Sep 26 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.0-rc7

* Mon Sep 19 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.0-rc6

* Mon Sep 05 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.0-rc4

* Mon Aug 29 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.0-rc3

* Mon Aug 22 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.0-rc2

* Mon Aug 15 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v6.0-rc1

* Mon Aug 01 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19.0

* Tue Jul 26 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc8

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc7

* Mon Jul 11 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc6

* Mon Jul 04 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc5

* Mon Jun 27 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc4

* Mon Jun 20 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc3

* Mon Jun 13 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc2

* Mon Jun 06 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.19-rc1

* Mon May 23 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18.0

* Mon May 16 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18-rc6

* Mon May 09 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18-rc6

* Mon May 02 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18-rc5

* Mon Apr 25 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18-rc4

* Mon Apr 18 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Helps if I add the spec

* Mon Apr 18 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18-rc3

* Mon Apr 11 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18-rc2

* Mon Apr 04 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.18-rc1

* Mon Mar 21 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17.0

* Mon Mar 14 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc8

* Mon Mar 07 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc7

* Mon Feb 28 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc6

* Mon Feb 21 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc5

* Mon Feb 14 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc4

* Mon Feb 07 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc3

* Sun Jan 30 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc2

* Mon Jan 24 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.17-rc1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.16

* Mon Jan 03 2022 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.16-rc8

* Mon Dec 27 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.16-rc7

* Mon Dec 20 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.16-rc6

* Mon Dec 13 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.16-rc5

* Mon Dec 06 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.16-rc4

* Mon Nov 15 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.16-rc1

* Mon Nov 01 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.15.0

* Tue Oct 26 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.15-rc7

* Mon Oct 18 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.15-rc6

* Mon Oct 11 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.15-rc5

* Mon Oct 04 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.15-rc4

* Mon Sep 20 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.15-rc2

* Mon Sep 13 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.15-rc1

* Mon Aug 30 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14.0

* Mon Aug 23 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14-rc7

* Mon Aug 16 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14-rc6

* Mon Aug 09 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14-rc5

* Mon Aug 02 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14-rc4

* Mon Jul 26 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14-rc3

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14-rc2

* Mon Jul 12 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.14-rc1

* Mon Jun 28 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13

* Mon Jun 21 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc7

* Tue Jun 15 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc6

* Mon Jun 07 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc5 again, the spec helps

* Mon Jun 07 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc5

* Tue Jun 01 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc4

* Mon May 24 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc3

* Mon May 17 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc2

* Mon May 10 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.13-rc1

* Mon Apr 26 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12.0

* Mon Apr 19 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc8

* Mon Apr 12 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc7

* Mon Apr 05 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc6

* Mon Mar 29 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc5

* Mon Mar 22 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc4

* Mon Mar 15 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc3

* Sat Mar 06 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc2

* Mon Mar 01 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.12-rc1

* Mon Feb 15 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.11.0

* Mon Feb 08 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.11-rc7

* Mon Feb 01 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.11-rc6

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.11-rc5

* Mon Jan 18 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.11-rc4

* Mon Jan 04 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.11-rc2

* Mon Dec 14 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10

* Mon Dec 07 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc7

* Mon Nov 30 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc6

* Mon Nov 23 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc5

* Mon Nov 16 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc4

* Mon Nov 09 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc3

* Tue Nov 03 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc2 spec

* Tue Nov 03 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc2

* Mon Oct 26 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.10-rc1

* Mon Oct 12 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9.0

* Mon Oct 05 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9-rc8

* Mon Sep 28 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9-rc7

* Mon Sep 21 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9-rc6

* Tue Sep 15 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9-rc5

* Mon Aug 31 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9-rc3

* Tue Aug 25 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9-rc2

* Mon Aug 17 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.9-rc1

* Mon Aug 03 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.8.0

* Mon Jul 27 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.8-rc7

* Mon Jul 13 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.8-rc5

* Mon Jul 06 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.8-rc4

* Mon Jun 29 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.8-rc3

* Mon Jun 15 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.8-rc1

* Mon Jun 01 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.7.0

* Tue May 26 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Add support for riscv64 headers

* Mon May 25 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.7-rc7

* Mon May 11 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.7-rc5

* Wed May 06 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.7-rc4

* Mon Apr 27 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux 5.7-rc3

* Mon Apr 13 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Turn off released_kernel

* Mon Apr 13 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.7-rc1

* Mon Mar 30 2020 Jeremy Cline <jcline@redhat.com>
- Turn on released_kernel

* Mon Mar 30 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6

* Mon Mar 23 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc7

* Tue Mar 17 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc6

* Mon Mar 09 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc5

* Mon Mar 02 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc4

* Mon Feb 24 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc3

* Wed Feb 19 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc2.git2

* Mon Feb 17 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc2

* Tue Feb 11 2020 Jeremy Cline <jcline@redhat.com>
- Linux v5.6-rc1.git0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.5

* Mon Jan 20 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.5-rc7

* Mon Jan 13 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.5-rc6

* Mon Jan 06 2020 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.5-rc5.git0

* Mon Dec 30 2019 Peter Robinson <pbrobinson@gmail.com>
- v5.5-rc4.git0

* Mon Dec 23 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.5-rc3

* Mon Dec 16 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.5-rc2

* Tue Dec 10 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.5-rc1

* Wed Dec 04 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.4

* Mon Nov 04 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.4-rc6

* Mon Oct 28 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.4-rc5

* Thu Oct 03 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.4-rc1

* Mon Sep 16 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3.0

* Tue Sep 10 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc8.git0

* Tue Sep 03 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc7.git0

* Mon Aug 26 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc6.git0

* Mon Aug 19 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc5.git0

* Tue Aug 13 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc4.git0

* Mon Aug 05 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc3.git0

* Mon Jul 29 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc2.git0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc1.git0

* Thu Jul 18 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc0.git7

* Thu Jul 18 2019 Laura Abbott <labbott@redhat.com>
- Tweak how the headers are (correctly) generated

* Tue Jul 16 2019 Laura Abbott <labbott@redhat.com>
- Remove some dead header targets

* Tue Jul 16 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.3-rc0.git5

* Mon Jul 08 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2.0

* Mon Jul 01 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2-rc7.git0

* Mon Jun 24 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2-rc6.git0

* Mon Jun 17 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2-rc5.git0

* Mon Jun 10 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2-rc4

* Mon Jun 03 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2-rc3.git0

* Mon May 27 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2-rc2

* Mon May 20 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Forgot to set prerelease

* Mon May 20 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v5.2-rc1

* Mon May 06 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1.0

* Fri May 03 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc7.git4

* Thu May 02 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc7.git3

* Wed May 01 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc7.git2

* Tue Apr 30 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc7.git1

* Mon Apr 29 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc7

* Fri Apr 26 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc6.git4

* Thu Apr 25 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc6.git3

* Wed Apr 24 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc6.git2

* Tue Apr 23 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc6.git1

* Mon Apr 22 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc6

* Wed Apr 17 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc5.git2

* Tue Apr 16 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc5.git1

* Mon Apr 15 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc5

* Fri Apr 12 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc4.git4

* Thu Apr 11 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc4.git3

* Wed Apr 10 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc4.git2

* Tue Apr 09 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc4.git1

* Mon Apr 08 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc4

* Fri Apr 05 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc3.git3

* Wed Apr 03 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc3.git2

* Tue Apr 02 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc3.git1

* Mon Apr 01 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc3

* Fri Mar 29 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc2.git4

* Thu Mar 28 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc2.git3

* Thu Mar 28 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc2.git2

* Tue Mar 26 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc2.git1

* Mon Mar 25 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc2

* Sat Mar 23 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc1.git2

* Wed Mar 20 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc1.git1

* Mon Mar 18 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc1

* Fri Mar 15 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git9

* Thu Mar 14 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git8

* Wed Mar 13 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git7

* Tue Mar 12 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git6

* Mon Mar 11 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git5

* Fri Mar 08 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git4

* Thu Mar 07 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git3

* Wed Mar 06 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git2

* Tue Mar 05 2019 Jeremy Cline <jcline@redhat.com>
- Linux v5.1-rc0.git1

* Mon Mar 04 2019 Laura Abbott <labbott@redhat.com>
- Revert "Bump to -300"

* Mon Mar 04 2019 Laura Abbott <labbott@redhat.com>
- Bump to -300

* Mon Mar 04 2019 Laura Abbott <labbott@redhat.com>
- Forgot to mark as released

* Mon Mar 04 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0.0

* Mon Feb 25 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc8.git0

* Fri Feb 22 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc7.git3

* Wed Feb 20 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc7.git2

* Tue Feb 19 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc7.git1

* Mon Feb 18 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc7.git0

* Wed Feb 13 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc6.git1

* Mon Feb 11 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc6.git0

* Mon Feb 04 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc5.git0

* Fri Feb 01 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc4.git3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc4.git2

* Tue Jan 29 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc4.git1

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Remove obsolete Group tag

* Mon Jan 28 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc4.git0

* Mon Jan 21 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc3.git0

* Fri Jan 18 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc2.git4

* Thu Jan 17 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc2.git3

* Wed Jan 16 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc2.git2

* Tue Jan 15 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc2.git1

* Mon Jan 14 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc2.git0

* Thu Jan 10 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc1.git3

* Wed Jan 09 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc1.git2

* Tue Jan 08 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc1.git1

* Mon Jan 07 2019 Laura Abbott <labbott@redhat.com>
- Linux v5.0-rc1.git0

* Fri Jan 04 2019 Laura Abbott <labbott@redhat.com>
- Linux v4.21-rc0.git7

* Thu Jan 03 2019 Laura Abbott <labbott@redhat.com>
- Linux v4.21-rc0.git6

* Wed Jan 02 2019 Laura Abbott <labbott@redhat.com>
- Linux v4.21-rc0.git5

* Mon Dec 31 2018 Laura Abbott <labbott@redhat.com>
- Linux v4.21-rc0.git4

* Sun Dec 30 2018 Laura Abbott <labbott@redhat.com>
- Linux v4.21-rc0.git3

* Fri Dec 28 2018 Laura Abbott <labbott@redhat.com>
- Correct the sources

* Fri Dec 28 2018 Laura Abbott <labbott@redhat.com>
- Linux v4.21-rc0.git2

* Mon Dec 24 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20.0

* Mon Dec 17 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc7

* Mon Dec 10 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc6.git0

* Mon Dec 03 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc5.git0

* Mon Nov 26 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc4.git0

* Tue Nov 20 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.20-rc3.git1

* Mon Nov 19 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.20-rc3

* Mon Nov 12 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Add sources

* Mon Nov 12 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc2.git0

* Mon Nov 05 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc1.git0

* Fri Nov 02 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git9

* Thu Nov 01 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git8

* Wed Oct 31 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git7

* Tue Oct 30 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git6

* Mon Oct 29 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Forgot sources

* Mon Oct 29 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git5

* Fri Oct 26 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git4

* Thu Oct 25 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git3

* Wed Oct 24 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git2

* Tue Oct 23 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.20-rc0.git1

* Mon Oct 22 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19

* Fri Oct 19 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc8.git4

* Thu Oct 18 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc8.git3

* Wed Oct 17 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc8.git2

* Tue Oct 16 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc8.git1

* Mon Oct 15 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc8

* Fri Oct 12 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc7.git4

* Thu Oct 11 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc7.git3

* Wed Oct 10 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc7.git2

* Tue Oct 09 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc7.git1

* Mon Oct 08 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc7

* Fri Oct 05 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc6.git4

* Thu Oct 04 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc6.git3

* Wed Oct 03 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc6.git2

* Tue Oct 02 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc6.git1

* Mon Oct 01 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc6

* Fri Sep 28 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc5.git3

* Wed Sep 26 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc5.git2

* Tue Sep 25 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc5.git1

* Mon Sep 24 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc5

* Fri Sep 21 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc4.git4

* Thu Sep 20 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc4.git3

* Wed Sep 19 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc4.git2

* Tue Sep 18 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc4.git1

* Mon Sep 17 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc4

* Fri Sep 14 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc3.git3

* Thu Sep 13 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc3.git2

* Wed Sep 12 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc3.git1

* Mon Sep 10 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc3.git0

* Fri Sep 07 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc2.git3

* Thu Sep 06 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc2.git2

* Wed Sep 05 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc2.git1

* Mon Sep 03 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc2.git0

* Fri Aug 31 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc1.git4

* Thu Aug 30 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc1.git3

* Wed Aug 29 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc1.git2

* Tue Aug 28 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc1.git1

* Mon Aug 27 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.19-rc1

* Fri Aug 24 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-12721-g33e17876ea4e

* Thu Aug 23 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-11682-g815f0ddb346c

* Wed Aug 22 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-11219-gad1d69735878

* Tue Aug 21 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-10986-g778a33959a8a

* Mon Aug 20 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-10721-g2ad0d5269970

* Sun Aug 19 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-10568-g08b5fa819970

* Sat Aug 18 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-8895-g1f7a4c73a739

* Fri Aug 17 2018 Jeremy Cline <jcline@redhat.com>
- Linux v4.18-8108-g5c60a7389d79

* Tue Aug 14 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.18

* Tue Jul 31 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Linux v4.18-rc7

* Fri Jul 27 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- kernel-headers-4.18.0-0.rc6.git3.1
## END: Generated by rpmautospec
