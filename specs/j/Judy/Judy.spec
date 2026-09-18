# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		Judy
Version:	1.0.5
Release:	42%{?dist}
Summary:	General purpose dynamic array
License:	LGPL-2.0-or-later
URL:		http://sourceforge.net/projects/judy/
Source0:	http://downloads.sf.net/judy/Judy-%{version}.tar.gz
Source1:	README.Fedora
Patch0:		Judy-1.0.4-test-shared.patch
Patch1:		Judy-1.0.4-fix-Judy1-mans.patch
Patch2:		04_fix_undefined_behavior_during_aggressive_loop_optimizations.patch
BuildRequires:	coreutils
BuildRequires:	gawk
BuildRequires:	gcc >= 4.1
BuildRequires:	hardlink
BuildRequires:	make
BuildRequires:	sed

%description
Judy is a C library that provides a state-of-the-art core technology that
implements a sparse dynamic array. Judy arrays are declared simply with a null
pointer. A Judy array consumes memory only when it is populated, yet can grow
to take advantage of all available memory if desired. Judy's key benefits are
scalability, high performance, and memory efficiency. A Judy array is
extensible and can scale up to a very large number of elements, bounded only by
machine memory. Since Judy is designed as an unbounded array, the size of a
Judy array is not pre-allocated but grows and shrinks dynamically with the
array population.

%package devel
Summary:	Development libraries and headers for Judy
Requires:	%{name} = %{version}-%{release}
# Provide also the lower-case name to be coherent with other RPM based distributions
Provides:	judy-devel = %{version}-%{release}

%description devel
This package contains the development libraries and header files
for developing applications that use the Judy library.

%prep
%setup -q -n judy-%{version}

# Make tests use shared instead of static libJudy
%patch -P 0 -p1 -b .test-shared

# The J1* man pages were incorrectly being symlinked to Judy, rather than Judy1
# This patch corrects that; submitted upstream 2008/11/27
%patch -P 1 -p1 -b .fix-Judy1-mans

# Fix some code with undefined behavior, commented on and removed by gcc
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=782841
%patch -P 2 -p1 -b .behavior

# README.Fedora
cp -p %{SOURCE1} .

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure --disable-static
make
#%{?_smp_mflags}
# fails to compile properly with parallel make:
# https://sourceforge.net/p/judy/bugs/22/

%install
%make_install

# get rid of static libs and libtool archives
rm -f %{buildroot}%{_libdir}/*.{a,la}

# clean out zero length and generated files from doc tree
rm -rf doc/man
rm -f doc/Makefile* doc/ext/README_deliver
[ -s doc/ext/COPYRIGHT ] || rm -f doc/ext/COPYRIGHT
[ -s doc/ext/LICENSE ] || rm -f doc/ext/LICENSE

# hardlink identical manpages together
hardlink -cv %{buildroot}%{_mandir}/man3/J*.3*

%check
cd test
./Checkit
cd -

%files
%license COPYING README.Fedora
%doc AUTHORS ChangeLog README examples/
%{_libdir}/libJudy.so.1
%{_libdir}/libJudy.so.1.*

%files devel
%doc doc
%{_includedir}/Judy.h
%{_libdir}/libJudy.so
%{_mandir}/man3/J*.3*

%changelog
* Fri Jan 30 2026 Michal Schorm <mschorm@redhat.com> - 1.0.5-42
- Start providing the lower-case 'judy-devel' name for compatibility with
  other RPM based distributions (rhbz#2435466)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Paul Howarth <paul@city-fan.org> - 1.0.5-36
- Hard link manpages to avoid duplication

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Paul Howarth <paul@city-fan.org> - 1.0.5-31
- Use SPDX-format license tag

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun  4 2021 Paul Howarth <paul@city-fan.org> - 1.0.5-26
- Replace undefined behaviour patch with one from upstream author, as used
  in debian since 2015
  (https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=782841)
- Drop gcc optimization flags as we can now use the distribution default
  flags again

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 25 2020 Paul Howarth <paul@city-fan.org> - 1.0.5-23
- Don't pass gcc-only compiler flags to other compilers, e.g. clang
  (based on https://src.fedoraproject.org/rpms/Judy/pull-request/3 from
  Timm Baeder)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Paul Howarth <paul@city-fan.org> - 1.0.5-20
- Modernize spec
  - Use %%make_install
  - Use %%set_build_flags
  - Drop conditionals for building with old distributions
  - Re-format %%description to 80 columns
  - Comment patch applications in %%prep section

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb  8 2018 Paul Howarth <paul@city-fan.org> - 1.0.5-17
- ldconfig scriptlets replaced by RPM File Triggers from Fedora 28
- Drop legacy BuildRoot: and Group: tags
- Drop redundant explicit buildroot cleaning
- Specify all explicitly-used build requirements
- Use %%license where possible
- Drop %%defattr, redundant since rpm 4.4

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Paul Howarth <paul@city-fan.org> - 1.0.5-8
- Fix some code with undefined behavior
- Build with -fno-strict-aliasing
- Disable various compiler tree optimizations that trigger reproducible
  crashes in gtkwave without generating compiler warnings (#1064090)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> - 1.0.5-3
- Rebuilt for gcc 4.7

* Mon Feb  7 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 18 2010 Paul Howarth <paul@city-fan.org> - 1.0.5-1
- Update to 1.0.5
  - Added proper clean targets to enable multiple builds
  - Added examples directory
  - Correctly detects 32/64-bit build environment
  - Allow explicit configure for 32/64-bit environment
- Cosmetic spec file clean-ups

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-4
- For Judy1 man page fix, patch Makefile.{am,in} instead of
  relying on autotools to regenerate the latter
- Add README.Fedora with upstream's license explanation

* Sun Nov 30 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-3
- Fix Judy1 man page symlinks
- Use valid tag License: LGPLv2+ confirmed with upstream
- Use version macro in Source0
- Remove Makefiles from installed doc tree

* Thu Nov 27 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-2
- Patch tests to run with shared library
- Run tests in check section

* Sun Oct 05 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-1
- Initial package for Fedora
