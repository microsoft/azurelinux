# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libaec
Version:        1.1.4
Release:        3%{?dist}
Summary:        Adaptive Entropy Coding library
License:        LicenseRef-Callaway-BSD
Url:            https://gitlab.dkrz.de/k202009/libaec
Source0:        https://gitlab.dkrz.de/k202009/libaec/-/archive/v%{version}/libaec-v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake >= 3.1

%description
Libaec provides fast loss-less compression of 1 up to 32 bit wide
signed or unsigned integers (samples). The library achieves best
results for low entropy data as often encountered in space imaging
instrument data or numerical model output from weather or climate
simulations. While floating point representations are not directly
supported, they can also be efficiently coded by grouping exponents
and mantissa.

Libaec implements Golomb Rice coding as defined in the Space Data
System Standard documents 121.0-B-2 and 120.0-G-2.

Libaec includes a free drop-in replacement for the SZIP
library (http://www.hdfgroup.org/doc_resource/SZIP).

%package devel
Summary:        Devel package for libaec (Adaptive Entropy Coding library)
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Devel files for libaec (Adaptive Entropy Coding library).

%package static
Summary:        Static variant of libaec (Adaptive Entropy Coding library)
Requires:       %{name}-devel = %{version}-%{release}

%description static
Static variant of libaec (Adaptive Entropy Coding library).

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%{cmake} -DBUILD_TESTING=ON -DBUILD_STATIC_LIBS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%doc README.md README.SZIP CHANGELOG.md
%license LICENSE.txt doc/patent.txt
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/cmake/%{name}

%files static
%{_libdir}/lib*.a

%changelog
* Wed Aug 20 2025 Christoph Junghans <junghans@votca.org> - 1.1.4-3
- Add static sub-package
- Fixes: rhbz#2387206

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jun 14 2025 Christoph Junghans <junghans@votca.org> - 1.1.4-1
- Version bump to v1.1.4
- Resolves: rhbz#2372454

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 03 2024 Christoph Junghans <junghans@votca.org> - 1.1.3-1
- Version bump to v1.1.3 (bug #2270651)

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1.2-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 05 2024 Orion Poplawski <orion@nwra.com> - 1.1.2-1
- Update to 1.1.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Christoph Junghans <junghans@votca.org> - 1.0.6-1
- Version bump to v1.0.6 (bug #2005324)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Christoph Junghans <junghans@votca.org> - 1.0.5-1
- Version bump to v1.0.5 (bug #1972635)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Christoph Junghans <junghans@votca.org> - 1.0.4-6
- Fix out-of-source build on F33 (bug #1863972)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Christoph Junghans <junghans@votca.org> - 1.0.4-1
- Version bump to 1.0.4

* Sat Feb 09 2019 Christoph Junghans <junghans@votca.org> - 1.0.3-3
- Include missing header

* Tue Feb 05 2019 Christoph Junghans <junghans@votca.org> - 1.0.3-2
- Enable all tests

* Mon Feb 04 2019 Christoph Junghans <junghans@votca.org> - 1.0.3-1
- Version bump to 1.0.3 (bug #1672326)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.2-2
- Switch to %%ldconfig_scriptlets

* Tue Oct 24 2017 Christoph Junghans <junghans@votca.org> - 1.0.2-1
- Version bump to 1.0.2 (#1504372)

* Sun Aug 13 2017  Christoph Junghans <junghans@votca.org>- 1.0.1-4
- Tweaks for EPEL7

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Christoph Junghans <junghans@votca.org> - 1.0.1-1
- version bump to 1.0.1 - bug #1471766

* Wed Jun 21 2017 Christoph Junghans <junghans@votca.org> - 1.0.0-2
- comments from review #1462443

* Sat Jun 17 2017 Christoph Junghans <junghans@votca.org> - 1.0.0-1
- initial import
