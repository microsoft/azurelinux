Summary:        Adaptive Entropy Coding library
Name:           libaec
Version:        1.0.6
Release:        1%{?dist}
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.dkrz.de/k202009/libaec
Source0:        https://gitlab.dkrz.de/k202009/libaec/-/archive/v%{version}/libaec-v%{version}.tar.gz
BuildRequires:  cmake3 >= 3.1
BuildRequires:  gcc

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

%prep
%setup -q -n %{name}-v%{version}

%build
mkdir build
pushd build
%{cmake3} ..
%make_build
popd

%install
%make_install -C build
rm %{buildroot}/%{_libdir}/lib*.a
mv %{buildroot}/%{_prefix}/cmake %{buildroot}/%{_libdir}

%check
make -C build test CTEST_OUTPUT_ON_FAILURE=1

%ldconfig_scriptlets

%files
%doc README.md README.SZIP CHANGELOG.md
%license LICENSE.txt doc/patent.txt
%{_bindir}/aec
%{_libdir}/lib*.so.*
%{_mandir}/man1/aec.*

%files devel
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/cmake/%{name}-*.cmake

%changelog
* Mon Jan 22 2024 Sindhu Karri <lakarri@microsoft.com> - 1.0.6-1
- Version bump to 1.0.6
- Updated the name of license file
- Remove the static libraries and package the cmake files in the devel package

* Tue Nov 01 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.0.4-5
- Move to core
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
