# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with static_libs # don't build static libraries

Summary:        Library providing a collection of special mathematical functions
Name:           openspecfun
Version:        0.5.3
Release: 25%{?dist}
# Automatically converted from old format: MIT and Public Domain - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND LicenseRef-Callaway-Public-Domain
Source0:        https://github.com/JuliaLang/openspecfun/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
URL:            https://github.com/JuliaLang/openspecfun
BuildRequires: make
BuildRequires:  gcc-gfortran

%description
Currently provides AMOS and Faddeeva. AMOS (from Netlib) is a
portable package for Bessel Functions of a Complex Argument and
Nonnegative Order; it contains subroutines for computing Bessel
functions and Airy functions. Faddeeva allows computing the
various error functions of arbitrary complex arguments (Faddeeva
function, error function, complementary error function, scaled
complementary error function, imaginary error function, and Dawson function);
given these, one can also easily compute Voigt functions, Fresnel integrals,
and similar related functions as well.

%package devel
Summary:    Library providing a collection of special mathematical functions
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Contains header files for developing applications that use the %{name}
library.

%package static
Summary:    Library providing a collection of special mathematical functions
Requires:   %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static %{name} library.

%prep
%setup -q %{name}-%{version}

%build
make %{?_smp_mflags} \
      FFLAGS="%{optflags}" \
      CFLAGS="%{optflags}" \
      USE_OPENLIBM=0 \
      includedir=%{_includedir}

%install
make install prefix=%{_prefix} \
             libdir=%{_libdir} \
             includedir=%{_includedir} \
             DESTDIR=%{buildroot}

%if ! %{with static_libs}
rm %{buildroot}/%{_libdir}/libopenspecfun.a
%endif

%ldconfig_scriptlets

%files
%doc LICENSE.md README.md
%{_libdir}/libopenspecfun.so.1*

%files devel
%{_libdir}/libopenspecfun.so
%{_includedir}/Faddeeva.h

%if %{with static_libs}
%files static
%{_libdir}/libopenspecfun.a
%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.5.3-22
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 4 2018 Milan Bouchet-Valat <nalimilan@club.fr> - 0.5.3-6
- Rebuilt for libgfortran.so.4.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Milan Bouchet-Valat <nalimilan@club.fr> - 0.5.3-2
- Rebuild for gfortran 7.

* Wed Jul 27 2016 Milan Bouchet-Valat <nalimilan@club.fr> - 0.5.3-1
- New upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 27 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 0.4-1
- New upstream release.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 1 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 0.3-1
- New upstream release.
- Use Group System Environment/Libraries for base package.

* Fri Feb 14 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 0.2-2
- Don't build static libraries package by default.

* Sat Feb 8 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 0.2-1
- Initial version.
