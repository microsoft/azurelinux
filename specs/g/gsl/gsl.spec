# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: The GNU Scientific Library for numerical analysis
Name: gsl
Version: 2.8
Release: 2%{?dist}
URL: https://www.gnu.org/software/gsl/
VCS: git://git.savannah.gnu.org/gsl.git
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License: GPL-3.0-or-later
Source0: https://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
Source1: https://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz.sig
Source2: https://www.gnu.org/software/gsl/key/gsl_key.txt
Patch0: gsl-1.10-lib64.patch
# http://lists.gnu.org/archive/html/bug-gsl/2015-12/msg00012.html
Patch1: gsl-tol.patch
Patch2: gsl-test.patch

BuildRequires: gcc
BuildRequires: gnupg2
BuildRequires: pkgconfig
BuildRequires: make

%description
The GNU Scientific Library (GSL) is a collection of routines for
numerical analysis, written in C.

%package devel
Summary: Libraries and the header files for GSL development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The gsl-devel package contains the header files necessary for 
developing programs using the GSL (GNU Scientific Library).

%prep
%setup -q
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}
%patch -P0 -p1 -b .lib64
%patch -P1 -p1 -b .tol
%patch -P2 -p1 -b .test

%build
# disable FMA
%ifarch aarch64 ppc64 ppc64le s390 s390x x86_64 riscv64
export CFLAGS="%{optflags} -ffp-contract=off"
%endif
%configure --disable-silent-rules --disable-static
%make_build

%check
make check || ( cat */test-suite.log && exit 1 )

%install
%make_install
# remove unpackaged files from the buildroot
rm -rf %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/*.la

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%{_libdir}/libgsl.so.28*
%{_libdir}/libgslcblas.so.0*
%{_mandir}/man1/gsl-histogram.1*
%{_mandir}/man1/gsl-randist.1*

%files devel
%{_bindir}/gsl-config
%{_libdir}/libgsl.so
%{_libdir}/libgslcblas.so
%{_libdir}/pkgconfig/gsl.pc
%{_mandir}/man1/gsl-config.1*
%{_mandir}/man3/gsl.3*
%{_infodir}/gsl-ref.info*
%{_datadir}/aclocal/gsl.m4
%{_includedir}/gsl/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Feb 02 2025 Orion Poplawski <orion@nwra.com> - 2.8-1
- Update to 2.8

* Sat Feb  1 2025 Cristian Le <fedora@lecris.me> - 2.7.1-13
- Removed pkgconfig and automake requirements from gsl-devel

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug  8 2024 Jerry James <loganjerry@gmail.com> - 2.7.1-11
- Verify the source tarball
- Stop converting THANKS to UTF-8; it already is
- Minor spec file cleanups

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 2.7.1-10
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 26 2024 David Abdurachmanov <davidlt@rivosinc.com> - 2.7.1-8
- Disable FMA on riscv64

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Florian Weimer <fweimer@redhat.com> - 2.7.1-3
- Port configure script to C99

* Tue Aug 23 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.1-2
- Rebuild again for bodhi issue

* Thu Aug 11 2022 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.7.1-1
- Update to 2.7.1.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 20 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6-1
- Update to 2.6.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.5-1
- Update to 2.5.
- Updated license tag (the license that applies to the binaries) to GPLv3+.
- Bring spec file up to date by relying on recommended macros in build phase.
- Arched requires for base package in gsl-devel.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Christian Dersch <lupinix@mailbox.org> - 2.4-6
- Rebuilt, next try

* Wed Feb 28 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4-5
- Added gcc buildrequires.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Arthur Mello <amello@redhat.com> - 2.4-1
- Update to 2.4

* Tue Feb 14 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2.3-1
- rebase to 2.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 10 2016 Than Ngo <than@redhat.com> - 2.1-4
- fix build failure on powerpc

* Fri Feb 26 2016 Dan Horák <dan[at]danny.cz> - 2.1-3
- Disable FMA also on ppc64(le) and s390(x)

* Tue Feb 23 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.1-2
- Disable FMA on AArch64 to lower precision so tests do not fail.

* Sun Feb 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.1-1
- Update to 2.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 08 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.16-16
- Drop linkage patch: libgsl should not link to libgslcblas,
  so that more efficient libraries can be used (BZ #1007058).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.16-13
- Add upstream patch which fixes FTBFS on aarch64

* Sat Feb 15 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.16-12
- Drop ATLAS linkage patch: by design, the CBLAS library must be
  defined at link time to allow use of more optimized implementations.
  (BZ #1007058).

* Tue Oct 1 2013 Orion Poplawski <orion@cora.nwra.com> - 1.16-11
- Update to 1.16
- Rebase atlas patch
- Drop upstreamed ode patch

* Sat Sep 21 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-10
- linked against atlas 3.10

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jan 30 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-8
- self test moved to %%check section

* Tue Jan 29 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-7
- run self-tests after build
- updated ode-initval2 to upstream revision 4788

* Mon Nov 19 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-6
- minor cleanup of gsl.spec

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Peter Schiffer <pschiffe@redhat.com> - 1.15-3
- resolves: #741138
  removed unnecessary Requires: atlas

* Mon May  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.15-2
- resolves: #695148
  link gsl against atlas package for blas operations

* Mon May  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.15-1
- update to 1.15

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May  5 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.14-1
- update to 1.14
- Resolves: #560219
             Library not linked correctly

* Wed Mar  3 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.13-2
- remove the static subpackage

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 1.13-1
- update to 1.13

* Mon Aug 17 2009 Ivana Varekova <varekova@redhat.com> - 1.12-6
- fix preun and post scripts (#517568)

* Mon Aug 10 2009 Ivana Varekova <varekova@redhat.com> - 1.12-5
- fix installation with --excludedocs option (#515971)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 07 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.12-3
- Remove rpaths (fix BZ#487823).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Ivana Varekova <varekova@redhat.com> - 1.12-1
- update to 1.12

* Tue Sep 16 2008 Ivana Varekova <varekova@redhat.com> - 1.11-4
- Resolves: #462369 - remove %%{_datadir}/aclocal
- add automake dependency

* Mon Jul 28 2008 Ivana Varekova <varekova@redhat.com> - 1.11-3
- add -fgnu89-inline flag to solve gcc4.3 problem 
  remove gcc43 patch

* Wed Jun 18 2008 Ivana Varekova <varekova@redhat.com> - 1.11-2
- Resolves: #451006
  programs build with gcc 4.3 based on gsl require -fgnu89-inline 

* Mon Jun 16 2008 Ivana Varekova <varekova@redhat.com> - 1.11-1
- update to 1.11

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.10-10
- Autorebuild for GCC 4.3

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1.10-9
- source file change
- spec cleanup

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1.10-8
- fix man-pages directories

* Tue Oct 30 2007 Ivana Varekova <varekova@redhat.com> - 1.10-7
- add man pages

* Fri Oct 26 2007 Ivana Varekova <varekova@redhat.com> - 1.10-6
- minor spec changes

* Thu Oct 25 2007 Ivana Varekova <varekova@redhat.com> - 1.10-5
- minor spec changes

* Wed Oct 24 2007 Ivana Varekova <varekova@redhat.com> - 1.10-4
- add pkgconfig dependency
- separate static libraries to -static subpackage
- fix gsl-config script - thanks Patrice Dumas

