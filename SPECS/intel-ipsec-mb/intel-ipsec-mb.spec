%global major        1
%global minor        5
%global patch        0
%global fullversion  %{major}.%{minor}.%patch
# GitHub properties
%global githubname   intel-ipsec-mb
%global githubver    %{major}.%{minor}
%global githubfull   %{githubname}-%{githubver}
# disable producing debuginfo for this package
%global debug_package %{nil}
Summary:        IPSEC cryptography library optimized for Intel Architecture
Name:           %{githubname}
Version:        %{fullversion}
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/intel/%{githubname}
Source0:        https://github.com/intel/%{githubname}/archive/v%{githubver}/%{githubfull}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc >= 4.8.3
BuildRequires:  gcc-c++
BuildRequires:  nasm >= 2.14
ExclusiveArch:  x86_64

%description
IPSEC cryptography library optimized for Intel Architecture

%package -n %{name}-devel
Summary:        IPSEC cryptography library optimized for Intel Architecture
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
ExclusiveArch:  x86_64

%description -n intel-ipsec-mb-devel
IPSEC cryptography library optimized for Intel Architecture

For additional information please refer to:
https://github.com/intel/%{githubname}

%prep
%autosetup -n %{githubfull}
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
%{_libdir}/libIPSec_MB.so.%{fullversion}
%{_libdir}/libIPSec_MB.so.%{major}
%{_mandir}/man7/libipsec-mb.*

%files -n %{name}-devel
%{_includedir}/intel-ipsec-mb.h
%{_libdir}/libIPSec_MB.so
%{_mandir}/man7/libipsec-mb-dev.*

%changelog
* Thu Feb 01 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.5.0-1
- Upgrade to version 1.5

* Mon Jul 04 2022 Sriram Nambakam <snambakam@microsoft.com> - 1.2.0-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- Verified license

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
