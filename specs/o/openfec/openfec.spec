# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		openfec
Version:	1.4.2.6
Release:	7%{?dist}
Summary:	Application-Level Forward Erasure Correction codes
License:	CeCILL-C and GPLv2+ and BSD
# GPLv2+:
#   tools/descr_stats_v1.2/descr_stats.c
# BSD:
#   src/lib_stable/reed-solomon_gf_2_8/of_reed-solomon_gf_2_8.c
#   src/lib_stable/reed-solomon_gf_2_m/galois_field_codes_utils/algebra_2_4.c
#   src/lib_stable/reed-solomon_gf_2_m/galois_field_codes_utils/algebra_2_4.h
#   src/lib_stable/reed-solomon_gf_2_m/galois_field_codes_utils/algebra_2_8.c
#   src/lib_stable/reed-solomon_gf_2_m/galois_field_codes_utils/algebra_2_8.h
URL:		https://github.com/roc-streaming/openfec
Source0:	%{URL}/archive/v%{version}/%{name}_%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	coreutils
BuildRequires:	findutils

%description
Application-Level Forward Erasure Correction codes, or AL-FEC (also called
UL-FEC, for Upper-Layers FEC). The idea, in one line, is to add redundancy
in order to be able to recover from erasures. Because of their position in
the communication stack, these codes are implemented as software codecs,
and they find many applications in robust transmission and distrituted
storage systems.

%package devel
Summary: Development libraries for openfec
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The openfec-devel package contains header files necessary for
developing programs using openfec.

%package utils
Summary: Utilities for openfec
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities for openfec.

%prep
%autosetup -p1

%build
%cmake -DOPTIMIZE=DEFAULT -DINSTALL_DEVTOOLS=ON
%cmake_build

%install
%cmake_install

# Install headers
mkdir -p %{buildroot}%{_includedir}/%{name}
pushd src
find -name '*.h' -type f -exec install -pDm 0644 '{}' %{buildroot}%{_includedir}/%{name}/'{}' \;
popd

%check
cd %{_vpath_builddir}
make test

%files
%license LICENCE_CeCILL-C_V1-en.txt Licence_CeCILL_V2-en.txt
%doc README CHANGELOG
%{_libdir}/libopenfec.so.1*

%files devel
%{_includedir}/%{name}
%{_libdir}/libopenfec.so
%{_datadir}/pkgconfig/openfec.pc

%files utils
%{_bindir}/eperftool
%{_bindir}/simple_client
%{_bindir}/simple_server

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 26 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.2.6-1
- New version
  Resolves: rhbz#2164074

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep  5 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.2.4-3
- Updated license according to the review
  Related: rhbz#2121558

* Tue Aug 30 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.2.4-2
- Fixed tests on s390x

* Mon Aug 29 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.2.4-1
- New version
- Switched to roc-streaming fork

* Tue Aug 23 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.2-1
- Initial version
