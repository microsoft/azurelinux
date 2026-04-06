# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global name1 mpfr

Summary:        MinGW C library for multiple-precision floating-point computations
Name:           mingw-%{name1}
Version:        4.0.2
Release:        15%{?dist}
URL:            http://www.mpfr.org/
Source0:        http://www.mpfr.org/mpfr-%{version}/%{name1}-%{version}.tar.xz

# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13499&view=revision
# https://www.mpfr.org/mpfr-4.0.2/patch01
Patch0: %{name1}-include-float.patch

# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13828&view=revision
# https://www.mpfr.org/mpfr-4.0.2/patch02
Patch1: %{name1}-int-overflow.patch

# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13836&view=revision
# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13838&view=revision
# https://www.mpfr.org/mpfr-4.0.2/patch03
Patch2: %{name1}-set-int.patch

# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13697&view=revision
# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13837&view=revision
# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13841&view=revision
# https://www.mpfr.org/mpfr-4.0.2/patch04
Patch3: %{name1}-sub1-ubf.patch

# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13516&view=revision
# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13520&view=revision
# https://www.mpfr.org/mpfr-4.0.2/patch05
Patch4: %{name1}-const.patch

# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13518&view=revision
# https://www.mpfr.org/mpfr-4.0.2/patch06
Patch5: %{name1}-array-length.patch

# https://gforge.inria.fr/scm/viewvc.php/mpfr?revision=13869&view=revision
# https://www.mpfr.org/mpfr-4.0.2/patch07
Patch6: %{name1}-sub1-ubftest.patch

# GFDL  (mpfr.texi, mpfr.info and fdl.texi)
# Automatically converted from old format: LGPLv3+ and GPLv3+ and GFDL - review is highly recommended.
License:        LGPL-3.0-or-later AND GPL-3.0-or-later AND LicenseRef-Callaway-GFDL
BuildRequires: make
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-gmp
BuildRequires:  mingw64-gmp
BuildArch:      noarch

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

# Mingw32
%package -n mingw32-%{name1}
Summary:        %{summary}

%description -n mingw32-%{name1}
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

This package contains cross-compiled libraries and development tools
for Windows.

# Mingw64
%package -n mingw64-%{name1}
Summary:        %{summary}

%description -n mingw64-%{name1}
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

This package contains cross-compiled libraries and development tools
for Windows.

%{?mingw_debug_package}

%prep
%autosetup -p1 -n %{name1}-%{version}

%build
%mingw_configure --disable-assert --disable-static --enable-shared
%mingw_make %{?_smp_mflags}

%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}
rm -rf $RPM_BUILD_ROOT%{mingw32_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{mingw64_libdir}/*.la

%files -n mingw32-%{name1}
%doc COPYING COPYING.LESSER NEWS README
%{mingw32_bindir}/libmpfr-6.dll
%{mingw32_libdir}/libmpfr.dll.a
%{mingw32_includedir}/*.h
%{mingw32_libdir}/pkgconfig/mpfr.pc

%files -n mingw64-%{name1}
%doc COPYING COPYING.LESSER NEWS README
%{mingw64_bindir}/libmpfr-6.dll
%{mingw64_libdir}/libmpfr.dll.a
%{mingw64_includedir}/*.h
%{mingw64_libdir}/pkgconfig/mpfr.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 4.0.2-13
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 4.0.2-6
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 02 2020 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.0.2-1
- update to 4.0.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.6-1
- update to 3.1.6

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 01 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.5-1
- update to 3.1.5

* Mon Mar 07 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.4-1
- update to 3.1.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 02 2015 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.3-1
- update to 3.1.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 18 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.2-1
- update to 3.1.2

* Tue Sep 11 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.1-3
- remove requires

* Tue Sep  4 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.1-2
- change name macro name, changed group, removed sections not necessary for recent rpm

* Sat Aug 25 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.1.1-1
- create from native spec

