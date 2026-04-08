# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Versions numbers
%global major 2
%global minor 0
%global patch 1

%global desc %{expand: \
Intel Multi-Buffer Crypto for IPsec Library is highly-optimized software
implementations of the core cryptographic processing for IPsec, which provides
industry-leading performance on a range of Intel Processors.}

Name:               intel-ipsec-mb
Version:            2.0.1
Release:            2%{?dist}
Summary:            IPsec cryptography library optimized for Intel Architecture

License:            BSD-3-Clause
URL:                https://github.com/intel/intel-ipsec-mb
Source0:            %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

ExclusiveArch:      x86_64

BuildRequires:      cmake
BuildRequires:      gcc
BuildRequires:      gcc-c++
BuildRequires:      nasm >= 2.14

%description
%{desc}

%package -n intel-ipsec-mb-devel
Summary:            Development files for %{name}
Requires:           %{name}%{?_isa} = %{version}-%{release}

%description devel %{desc}

Development files.

%prep
%autosetup -p1 -n %{name}-%{version}
sed -i 's|man/man7|share/man/man7|g' lib/cmake/unix.cmake

%build
%cmake
%cmake_build

%install
%cmake_install

%check
%ctest

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md ReleaseNotes.txt
%{_libdir}/libIPSec_MB.so.%{major}
%{_libdir}/libIPSec_MB.so.%{major}.%{minor}.%{patch}
%{_mandir}/man7/libipsec-mb.*

%files -n %{name}-devel
%{_includedir}/intel-ipsec-mb.h
%{_libdir}/libIPSec_MB.so
%{_mandir}/man7/libipsec-mb-dev.*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Marcel Cornu <marcel.d.cornu@intel.com> - 2.0.1-1
- Update to 2.0.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 06 2024 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> 2.0-1
- Update to 2.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> 1.5-1
- Update to 1.5

* Wed Aug 16 2023 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> 1.4-3
- Packaging optimization to prevent AVX512 based gcc compilation errors

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Marcel Cornu <marcel.d.cornu@intel.com> 1.4.0-1
- Update for release package v1.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Marcel Cornu <marcel.d.cornu@intel.com> 1.3.0-2
- Add patch to fix multi-threaded performance scaling issue

* Wed Sep 28 2022 Marcel Cornu <marcel.d.cornu@intel.com> 1.3.0-1
- Update for release package v1.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 02 2022 Marcel Cornu <marcel.d.cornu@intel.com> 1.2.0-2
- Correct spelling of IPsec in package description

* Fri Feb 25 2022 Marcel Cornu <marcel.d.cornu@intel.com> 1.2.0-1
- Update for release package v1.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 29 2021 Marcel Cornu <marcel.d.cornu@intel.com> 1.1.0-1
- Update for release package v1.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 13 2021 Marcel Cornu <marcel.d.cornu@intel.com> 1.0.0-1
- Update for release package v1.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.55.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 29 2020 Marcel Cornu <marcel.d.cornu@intel.com> 0.55.0-1
- Update for release package v0.55

* Tue Sep 08 2020 Marcel Cornu <marcel.d.cornu@intel.com> 0.54.0-2
- Updated to improve compliance with packaging guidelines
- Added patch to fix executable stack issue

* Thu May 14 2020 Marcel Cornu <marcel.d.cornu@intel.com> 0.54.0-1
- Update for release package v0.54.0

* Thu Sep 13 2018 Marcel Cornu <marcel.d.cornu@intel.com> 0.51-1
- Update for release package v0.51

* Mon Apr 16 2018 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.49-1
- update for release package v0.49
- 01org replaced with intel in URL's
- use of new makefile 'install' target with some workarounds

* Fri Aug 11 2017 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.46-1
- initial version of the package
