# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:       mingw-gmp
Version:    6.3.0
Release:    4%{?dist}

Summary:    Cross-compiled GNU arbitrary precision library
# Automatically converted from old format: LGPLv3+ or GPLv2+ - review is highly recommended.
License:    LGPL-3.0-or-later OR GPL-2.0-or-later
URL:        http://gmplib.org/
Source0:    ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{version}.tar.xz
# https://gmplib.org/repo/gmp/rev/8e7bb4ae7a18
Patch0: gmp-6.3.0-c23.patch

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++

BuildRequires:  git
BuildRequires:  libtool


%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.


# Mingw32
%package -n mingw32-gmp
Summary: Cross-compiled GNU arbitrary precision library


%description -n mingw32-gmp
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.


# Mingw64
%package -n mingw64-gmp
Summary: Cross-compiled GNU arbitrary precision library


%description -n mingw64-gmp
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.


%?mingw_debug_package


%prep
%autosetup -S git -n gmp-%{version}


%build
autoreconf -ifv
%mingw_configure \
    --enable-shared \
    --disable-static \
    --enable-cxx \
    --enable-fat
export LD_LIBRARY_PATH=`pwd`/.libs
%mingw_make %{?_smp_mflags}


%install
export LD_LIBRARY_PATH=`pwd`/.libs
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/lib{gmp,mp,gmpxx}.la
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/lib{gmp,mp,gmpxx}.la

# Remove documentation which duplicates that found in the native package.
rm -r $RPM_BUILD_ROOT/%{mingw32_prefix}/share
rm -r $RPM_BUILD_ROOT/%{mingw64_prefix}/share


# Win32
%files -n mingw32-gmp
%license COPYING COPYING.LESSERv3 COPYINGv2 COPYINGv3
%doc NEWS README
%{mingw32_bindir}/libgmp-10.dll
%{mingw32_bindir}/libgmpxx-4.dll
%{mingw32_libdir}/libgmp.dll.a
%{mingw32_libdir}/libgmpxx.dll.a
%{mingw32_libdir}/pkgconfig/gmp.pc
%{mingw32_libdir}/pkgconfig/gmpxx.pc
%{mingw32_includedir}/gmp.h
%{mingw32_includedir}/gmpxx.h


# Win64
%files -n mingw64-gmp
%license COPYING COPYING.LESSERv3 COPYINGv2 COPYINGv3
%doc NEWS README
%{mingw64_bindir}/libgmp-10.dll
%{mingw64_bindir}/libgmpxx-4.dll
%{mingw64_libdir}/libgmp.dll.a
%{mingw64_libdir}/libgmpxx.dll.a
%{mingw64_libdir}/pkgconfig/gmp.pc
%{mingw64_libdir}/pkgconfig/gmpxx.pc
%{mingw64_includedir}/gmp.h
%{mingw64_includedir}/gmpxx.h


%changelog
* Thu Jul 31 2025 Michael Cronenworth <mike@cchtml.com> - 6.3.0-4
- Fix FTBFS (RHBZ#2385183)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Daniel P. Berrangé <berrange@redhat.com> - 6.3.0-1
- Rebase to 6.3.0, adding pkg-config files

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 6.1.2-20
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 6.1.2-13
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 6.1.2-7
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 Michael Cronenworth <mike@cchtml.com> - 6.1.2-1
- New upstream release.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 04 2016 Michael Cronenworth <mike@cchtml.com> - 6.1.1-1
- New upstream release.

* Tue Jun 07 2016 Michael Cronenworth <mike@cchtml.com> - 6.1.0-1
- New upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Michael Cronenworth <mike@cchtml.com> - 6.0.0-1
- New upstream release.

* Tue Jan 07 2014 Michael Cronenworth <mike@cchtml.com> - 5.1.3-1
- New upstream release.

* Sun Sep 22 2013 Michael Cronenworth <mike@cchtml.com> - 5.1.2-1
- New upstream release.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.1-2
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Thu May 09 2013 Michael Cronenworth <mike@cchtml.com> - 5.1.1-1
- New upstream release.

* Sun Jan 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.5-2
- Rebuild against mingw-gcc 4.8 (win64 uses SEH exceptions now)

* Mon Sep 03 2012 Michael Cronenworth <mike@cchtml.com> - 5.0.5-1
- New upstream release.

* Wed Aug 29 2012 Michael Cronenworth <mike@cchtml.com> - 5.0.2-4
- Don't ship include wrappers

* Wed Aug 29 2012 Michael Cronenworth <mike@cchtml.com> - 5.0.2-3
- Don't autoreconf

* Sun Aug 26 2012 Michael Cronenworth <mike@cchtml.com> - 5.0.2-2
- Add BR for mingw-gcc-c++
- Install gmp source headers

* Mon Jun 18 2012 Michael Cronenworth <mike@cchtml.com> - 5.0.2-1
- Initial RPM package
