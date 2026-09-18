# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libcerf
Version:        3.1
%global         sover 3
Release:        2%{?dist}
Summary:        A library that provides complex error functions

License:        MIT
URL:            https://jugit.fz-juelich.de/mlz/libcerf
Source0:        https://jugit.fz-juelich.de/mlz/libcerf/-/archive/v%{version}/%{name}-v%{version}.tar.gz

%if (0%{?rhel} || (0%{?fedora} && 0%{?fedora} < 33))
%undefine __cmake_in_source_build
%endif

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  cmake
# Required to build the documentation
BuildRequires:  perl-podlators
BuildRequires:  perl-Pod-Html

%description
libcerf is a self-contained numeric library that provides an efficient
and accurate implementation of complex error functions, along with
Dawson, Faddeeva, and Voigt functions.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-v%{version}

%build
# avoid non-portable default build flags (-march=native -O3), by setting overwrite
# CERF_COMPILE_OPTIONS to a harmless flags like -Wall and let cmake do its thing
%cmake -DCERF_COMPILE_OPTIONS='-Wall' \
%ifarch s390x
    -DCERF_IEEE754=OFF
%else
    %{nil}
%endif
%cmake_build


%install
%cmake_install
# Move the documentation to the devel package
mv $RPM_BUILD_ROOT/%{_datadir}/doc/cerf/html $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-devel


%check
%ctest


%files
%license LICENSE
%doc README.md
%{_libdir}/*.so.%{sover}*

%files devel
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/doc/%{name}-devel/
%{_libdir}/cmake/cerf


%changelog
* Tue Aug 12 2025 Dan Horák <dan[at]danny.cz> - 3.1-2
- fix build on s390x

* Sun Aug 10 2025 Christoph Junghans <junghans@votca.org> - 3.1-1
- Version bump to v3.1
- Fixes: rhbz#2362012

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Apr 16 2025 Christoph Junghans <junghans@votca.org> - 2.4-1
- Version bump v2.4 (bug #228557)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 14 2023 Christoph Junghans <junghans@votca.org> - 2.3-1
- Version bump to v2.3 (bug #2140587)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 10 2022 Christoph Junghans <junghans@lanl.gov> - 2.1-1
- Version bump to v2.1 (bug #2073559)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Christoph Junghans <junghans@lanl.gov> - 1.17-1
- Version bump to v1.17

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan  4 2021 José Matos <jamatos@fedoraproject.org> - 1.14-1
- update to 1.14 (version 2.0 has been withdrawn) so this is the latest

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
- Fix cmake changes

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 17 2019 José Matos <jamatos@fedoraproject.org> - 1.13-1
- update to 1.13
- update homepage and source urls

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 José Matos <jamatos@fedoraproject.org> - 1.11-1
- update to 1.11
- adds html documentation to the devel subpackage
- adds a pkgconfig .pc file

* Fri Nov  2 2018 José Matos <jamatos@fedoraproject.org> - 1.9-3
- build for all available fedora releases

* Fri Nov  2 2018 José Matos <jamatos@fedoraproject.org> - 1.9-2
- rebuild for all the supported releases

* Fri Oct 19 2018 José Matos <jamatos@fedoraproject.org> - 1.9-1
- update to 1.9

* Mon Oct 15 2018 José Matos <jamatos@fedoraproject.org> - 1.8-2
- add tests

* Sun Oct 14 2018 José Abílio Matos <jamatos@fedoraproject.org> - 1.8-1
- initial package
