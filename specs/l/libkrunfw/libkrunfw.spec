# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This library just contains the guest payload to be injected by libkrun into
# the VM's memory, so no useful debug info can be generated from it.
%global debug_package %{nil}

%global kernel linux-6.12.68

Name:           libkrunfw
Version:        5.2.1
Release: 2%{?dist}
Summary:        A dynamic library bundling the guest payload consumed by libkrun
License:        LGPL-2.1-only AND GPL-2.0-only
URL:            https://github.com/containers/libkrunfw
Source0:        https://github.com/containers/libkrunfw/archive/refs/tags/v%{version}.tar.gz
# This package bundles a customized Linux kernel in a format that can only be
# consumed by libkrun, which will run it in an isolated context using KVM
# Virtualization. This kernel can't be used for booting a physical machine
# and, by being bundled in a dynamic library, it can not be mistaken as a
# regular kernel.
#
# The convenience of distributing a kernel this way and for this purpose was
# discussed here:
# https://lists.fedorahosted.org/archives/list/kernel@lists.fedoraproject.org/thread/2TMXPCE2VWF7USZA7OHQ3P2SBJAEGCSX/
Source1:        https://www.kernel.org/pub/linux/kernel/v6.x/%{kernel}.tar.xz

# libkrunfw only provides configs for x86_64 and aarch64 as libkrun (the only
# consumer of this library) only supports those architectures.
ExclusiveArch:  x86_64 aarch64 riscv64

# libkrunfw + packaging requirements
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  make
BuildRequires:  python3-pyelftools
BuildRequires:  openssl-devel

# kernel build requirements
BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  elfutils-devel
BuildRequires:  flex
%ifarch aarch64 riscv64
BuildRequires:  perl-interpreter
%endif

%description
%{summary}

%package devel
Summary: Header files and libraries for libkrunfw development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libkrunfw-devel package contains the libraries needed to develop
programs that consume the guest payload integrated in libkrunfw.

# SEV is a feature provided by AMD EPYC processors, so only it's only
# available on x86_64.
%ifarch x86_64
%package sev
Summary: A dynamic library bundling the guest payload consumed by libkrun-sev

%description sev
The libkrunfw-sev package contains the library bundling the guest
payload consumed by libkrun-sev.

%package sev-devel
Summary: Header files and libraries for libkrunfw-sev development
Requires: %{name}-sev%{?_isa} = %{version}-%{release}

%description sev-devel
The libkrunfw-sev-devel package contains the libraries needed to develop
programs that consume the guest payload integrated in libkrunfw-sev.
%endif

%prep
%autosetup -S git
mkdir tarballs
cp %{SOURCE1} tarballs/

%build
%{make_build}
%ifarch x86_64
    rm -fr %{kernel}
    rm kernel.c
    %{make_build} SEV=1
    pushd utils
    make
    popd
%endif

%install
%{make_install} PREFIX=%{_prefix}
%ifarch x86_64
    %{make_install} SEV=1 PREFIX=%{_prefix}
    install -D -p -m 0755 utils/krunfw_measurement %{buildroot}%{_bindir}/krunfw_measurement
%endif

%files
%{_libdir}/libkrunfw.so.5
%{_libdir}/libkrunfw.so.%{version}

%files devel
%{_libdir}/libkrunfw.so

%ifarch x86_64
%files sev
%{_libdir}/libkrunfw-sev.so.5
%{_libdir}/libkrunfw-sev.so.%{version}
%{_bindir}/krunfw_measurement

%files sev-devel
%{_libdir}/libkrunfw-sev.so
%endif

%changelog
* Tue Feb 17 2026 Sergio Lopez <slp@redhat.com> - 5.2.1-1
- Update to 5.2.1 with no kernel update

* Thu Feb 12 2026 David Abdurachmanov <davidlt@rivosinc.com> - 5.2.0-2
- Enable riscv64 arch

* Mon Feb 02 2026 Sergio Lopez <slp@redhat.com> - 5.2.0-1
- Update to 5.2.0 which bundles a 6.12.68 kernel

* Mon Jan 19 2026 Sergio Lopez <slp@redhat.com> - 5.1.0-2
- Rebuilt for new side tag

* Sat Jan 17 2026 Sergio Lopez <slp@redhat.com> - 5.1.0-1
- Update to 5.1.0 which bundles a 6.12.62 kernel

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 27 2025 Sergio Lopez <slp@redhat.com> - 4.10.0-1
- Update to 4.10.0 which bundles a 6.12.34 kernel

* Mon Mar 24 2025 Sergio Lopez <slp@redhat.com> - 4.9.0-1
- Update to 4.9.0 which bundles a 6.12.20 kernel

* Mon Jan 20 2025 Sergio Lopez <slp@redhat.com> - 4.7.1-1
- Update to 4.7.1 which bundles a 6.12.3 kernel

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Sergio Lopez <slp@redhat.com> - 4.5.1-1
- Update to 4.5.1 which bundles a 6.6.59 kernel

* Fri Sep 27 2024 Sergio Lopez <slp@redhat.com> - 4.4.1-1
- Update to 4.4.1 which bundles a 6.6.52 kernel

* Tue Sep 03 2024 Sergio Lopez <slp@redhat.com> - 4.3.0-1
- Update to 4.3.0 which bundles a 6.6.44 kernel

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 4.2.0-2
- convert license to SPDX

* Tue Jul 23 2024 Sergio Lopez <slp@redhat.com> - 4.2.0-1
- Update to 4.2.0 which bundles a 6.6.32 kernel

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 24 2023 Sergio Lopez <slp@redhat.com> - 4.0.0-1
- Update to 4.0.0 which bundles a 6.4.7 kernel

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 10 2023 Sergio Lopez <slp@redhat.com> - 3.12.0-1
- Update to 3.12.0 which bundles a 6.2.14 kernel

* Tue Apr 04 2023 Sergio Lopez <slp@redhat.com> - 3.11.0-1
- Update to 3.11.0 which bundles a 6.2.9 kernel

* Thu Feb 09 2023 Sergio Lopez <slp@redhat.com> - 3.9.0-1
- Update to 3.9.0 which bundles a 6.1.6 kernel

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Sergio Lopez <slp@redhat.com> - 3.8.1-1
- Update to 3.8.1 which bundles a 6.0.6 kernel

* Tue Oct 04 2022 Sergio Lopez <slp@redhat.com> - 3.7.0-1
- Update to 3.7.0 which bundles a 5.15.71 kernel

* Wed Aug 17 2022 Sergio Lopez <slp@redhat.com> - 3.6.3-1
- Update to 3.6.3 which bundles a 5.15.60 kernel
- Add the libkrunfw-sev and libkrunfw-sev-devel subpackages with the SEV
  variant of the library.

* Wed Jul 27 2022 Sergio Lopez <slp@redhat.com> - 3.2.0-1
- Update to 3.2.0 which bundles a 5.15.57 kernel

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Sergio Lopez <slp@redhat.com> - 3.1.0-1
- Update to 3.1.0 which bundles a 5.15.52 kernel

* Fri Jun 17 2022 Sergio Lopez <slp@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Jun 06 2022 Sergio Lopez <slp@redhat.com> - 2.1.1-1 
- Initial package
