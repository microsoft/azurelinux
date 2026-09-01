# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Azure Linux local kernel-headers spec.
#
# This is a maintained local spec (migrated from the previous azldev TOML
# overlay approach). Edit this file directly. Azure Linux customizations are
# marked with "AZL:" comments throughout.
#
# The build tracks kernel.spec: same source tarball, same version scheme
# (%{specversion}.%{kextraversion}), same manual release bump discipline.
# When rebuilding without a version change, bump azl_pkgrelease.

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

# AZL: our kernel source comes to us with a non-standard 4-digit version
# number (e.g. A.B.C.D), so we remove the 4th number (e.g. D) and use the
# standard 3-digit version (e.g. A.B.C), and place the 4th number into the
# leading (dot-separated) position of our release value, in the %{specrelease}
# macro below. For example, if the kernel source is version "A.B.C.D", our rpm
# V-R would start with "A.B.C-D." plus the remaining release macro/arch values.
%define kextraversion 1
# AZL: RPM release counter. Bump for rebuilds without a version change. This
# corresponds to upstream Fedora's %{pkgrelease} macro; we use it in the
# %{specrelease} macro below instead of a hardcoded value.
%define azl_pkgrelease 1

# define buildid .local
%define specversion 6.18.45
%define tarfile_release 6.18.45
# This is needed to do merge window version magic
# This allows pkg_release to have configurable %%{?dist} tag
%define specrelease %{kextraversion}.%{azl_pkgrelease}%{?buildid}%{?dist}

# This package doesn't contain any binary, thus no debuginfo package is needed
%global debug_package %{nil}

Name: kernel-headers
Summary: Header files for the Linux kernel for use by glibc
License: ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-2-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR CDDL-1.0) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND ((GPL-2.0-only WITH Linux-syscall-note) OR MIT) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR MIT) AND BSD-3-Clause AND (GPL-1.0-or-later WITH Linux-syscall-note) AND GPL-2.0-only AND (GPL-2.0-only WITH Linux-syscall-note) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND (LGPL-2.1-only WITH Linux-syscall-note) AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND MIT
URL: http://www.kernel.org/
Version: %{specversion}
Release: %{specrelease}
# AZL: Source0 points at the Azure Linux kernel tarball
# (rolling-lts/azl4/%{specversion}.%{kextraversion}); upstream Fedora ships a
# pre-built headers tarball, we generate headers from source instead (%build
# below).
Source0: kernel-%{specversion}.%{kextraversion}.tar.gz
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if "0%{?variant}"
Obsoletes: kernel-headers < %{specversion}-%{specrelease}
Provides: kernel-headers = %{specversion}-%{specrelease}
%endif

# AZL: `make headers_install` is invoked directly, so a small build toolchain
# (make/gcc/perl/rsync) is enough — no full kernel build deps.
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
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-azl4-%{specversion}.%{kextraversion}

# AZL: generate headers from the kernel source tree for both native and the
# opposite architecture (for kernel-cross-headers). Upstream Fedora consumes a
# pre-built headers tarball; we build them here instead.
%build

make mrproper
make headers_install INSTALL_HDR_PATH=headers-native

# Determine native kernel arch and cross-compile for the other
native_karch=$(uname -m | sed 's/x86_64/x86/;s/aarch64/arm64/')
for cross_arch in arm64 x86; do
    [ "$cross_arch" = "$native_karch" ] && continue
    make ARCH=$cross_arch headers_install INSTALL_HDR_PATH=headers-$cross_arch
done

# AZL: install natively-generated headers under %{_includedir}; cross-arch
# headers land under %{_prefix}/<arch>-linux-gnu/include for the
# kernel-cross-headers subpackage.
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

%files
%defattr(-,root,root)
%{_includedir}/*

%files -n kernel-cross-headers
%defattr(-,root,root)
%{_prefix}/*-linux-gnu/*

%changelog
* Tue Sep 01 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.18.45-1.1
- feat(kernel): update kernel and kernel-headers to 6.18.45.1

* Mon Aug 24 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.18.39-1.3
- chore(kernel-headers): tidy release macros

* Wed Aug 19 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.18.39-1.2
- chore(kernel-headers): bump release to stay aligned with kernel spec

* Wed Aug 19 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.18.39-1.1
- feat(kernel): update kernel and kernel-headers to 6.18.39.1

* Mon May 18 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.18.31-1.1
- feat(kernel): update kernel and kernel-headers to 6.18.31.1

* Thu May 14 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.18.3-4
- feat(kernel-headers): update source to 6.18.29.1

* Wed May 13 2026 Daniel McIlvaney <damcilva@microsoft.com> - 6.18.3-3
- chore(locks): update kernel locks to work with azldev 9696597 (allow file replacement)

* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 6.18.3-2
- feat: introduce deterministic commit resolution via Azure Linux lock file
