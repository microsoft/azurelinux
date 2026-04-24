# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: C library for multiple-precision floating-point computations
Name: mpfr
Version: 4.2.2
Release: 3%{?dist}
URL: https://www.mpfr.org/
VCS: git:https://gitlab.inria.fr/mpfr/mpfr.git

License: LGPL-3.0-or-later
BuildRequires: gcc
BuildRequires: gmp-devel
BuildRequires: make
BuildRequires: texinfo

Source: https://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.xz

# Upstream post-release patches.  This currently contains:
#Patch0: https://www.mpfr.org/%%{name}-%%{version}/allpatches

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary: Development files for the MPFR library
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gmp-devel%{?_isa}

%description devel
Header files and documentation for using the MPFR
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package. You'll also need to
install the mpfr package.

%package doc
Summary: Documentation for the MPFR library
License: GFDL-1.2-no-invariants-or-later
BuildArch: noarch

%description doc
Documentation for the MPFR library.

%prep
%autosetup -p1

%build
%configure --disable-assert --disable-static

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build

%install
%make_install
cp -p ChangeLog PATCHES README %{buildroot}%{_pkgdocdir}
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

#these go into licenses, not doc
rm -f %{buildroot}%{_pkgdocdir}/COPYING{,.LESSER}

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%make_build check

%files
%license COPYING COPYING.LESSER
%dir %{_pkgdocdir}
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/README
%{_libdir}/libmpfr.so.6*

%files devel
%{_libdir}/libmpfr.so
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_libdir}/pkgconfig/mpfr.pc

%files doc
%license COPYING COPYING.LESSER
%dir %{_pkgdocdir}
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/BUGS
%{_pkgdocdir}/ChangeLog
%{_pkgdocdir}/FAQ.html
%{_pkgdocdir}/PATCHES
%{_pkgdocdir}/TODO
%{_pkgdocdir}/examples
%{_infodir}/mpfr.info*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 20 2025 Jerry James <loganjerry@gmail.com> - 4.2.2-1
- Update to MPFR 4.2.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May  9 2024 Jerry James <loganjerry@gmail.com> - 4.2.1-4
- Own the documentation directory (bz 2279758)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 4.2.1-1
- Update to MPFR 4.2.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Jerry James <loganjerry@gmail.com> - 4.2.0-2
- Update to MPFR 4.2.0-p12

* Wed Jul 12 2023 Jerry James <loganjerry@gmail.com> - 4.2.0-1
- Update to MPFR 4.2.0-p9

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Jerry James <loganjerry@gmail.com> - 4.1.1-2
- Update to MPFR 4.1.1-p1

* Thu Nov 17 2022 Jerry James <loganjerry@gmail.com> - 4.1.1-1
- Update to MPFR version 4.1.1
- Drop all patches
- Convert License tags to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Jerry James <loganjerry@gmail.com> - 4.1.0-8
- Remove old obsoletes used in the 3.x to 4.x transition

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jerry James <loganjerry@gmail.com> - 4.1.0-7
- Add upstream patches 12-13

* Tue Apr 13 2021 Jerry James <loganjerry@gmail.com> - 4.1.0-6
- Add upstream patches 10-11

* Tue Mar  9 2021 Jerry James <loganjerry@gmail.com> - 4.1.0-5
- Add upstream patches 8-9

* Wed Feb 17 2021 Jerry James <loganjerry@gmail.com> - 4.1.0-4
- Add upstream patches 1-7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jerry James <loganjerry@gmail.com> - 4.1.0-1
- Update to MPFR version 4.1.0
- Drop all patches

* Mon Jun 29 2020 Jerry James <loganjerry@gmail.com> - 4.0.2-5
- Add upstream patches 8 and 9

* Thu Apr 16 2020 Jerry James <loganjerry@gmail.com> - 4.0.2-4
- Add upstream patches 2 through 7

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Jerry James <loganjerry@gmail.com> - 4.0.2-2
- Drop the mpfr3 and mpfr3-devel subpackages

* Tue Oct  8 2019 Jerry James <loganjerry@gmail.com> - 4.0.2-1
- Update to MPFR version 4.0.2 plus patch01
- Make mpfr3 and mpfr3-devel subpackages for version 3.1.6
- Add a -doc subpackage to hold the GFDL-licensed content
- The main package license is LGPLv3+; the GPLv3+ content is not packaged
- Drop unnecessary autoconf and libtool BRs
- Drop explicit R on gmp; it is autogenerated
- Drop info scriptlets; this version can never appear in Fedora < 32 or RHEL < 9
- Drop ldconfig_scriptlets for the same reason
- Make sure there are no rpaths and that -Wl,--as-needed takes effect
- Do not use the %%doc macro; the files have already been copied

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Rex Dieter <rdieter@fedoraproject.org> - 3.1.6-3
- update scriptlets (#1644106)
- use %%make_build %%make_install

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 25 2018 James Paul Turner <jamesturner246@fedoraproject.org> - 3.1.6-1
- Update to MPFR version 3.1.6
- Use autosetup specfile macro for applying patches (patches 1 and 2 applied)
- Removed iconv calls, as they were breaking .info files, which are now unicode
  resolves #1299649
- Other minor cleanups
- BuildRequire gcc per https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar  4 2017 Peter Robinson <pbrobinson@fedoraproject.org> 3.1.5-3
- Examples should be in devel
- Minor cleanups

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 3.1.5-2
- Add missing %%license macro

* Tue Sep 27 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.1.5-1
- rebase

* Tue Mar 08 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.1.4-1
- Rebase

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Dan Horák <dan[at]danny.cz> - 3.1.3-3
- drop support for F<20

* Fri Oct 23 2015 David Sommerseth <davids@redhat.com> - 3.1.3-2
- Fixed missing packaging of doc files

* Tue Jun 23 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.1.3-1
- rebase to 3.1.3
- limboverflow.patch already in tarball, dropped

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 12 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.1.2-8
- added limboverflow.patch, rhbz#1171701, rhbz#1171710, there was one less limb allocated in strtofr

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.1.2-4
- Install docs into unversioned docdir (Fix FTBFS RHBZ#992296).
- Append --disable-static to %%configure.
- Fix broken %%changelog date.
- Remove stray cd ..

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Karsten Hopp <karsten@redhat.com> 3.1.2-2
- bump release and rebuild to fix dependencies on PPC

* Fri Mar 22 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.1.2-1
- Rebase to 3.1.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 26 2012 Peter Schiffer <pschiffe@redhat.com> - 3.1.1-1
- resolves: #837563
  update to 3.1.1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Peter Schiffer <pschiffe@redhat.com> - 3.1.0-1
- resolves: #743237
  update to 3.1.0
- removed compatibility symlinks and provides

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.0.0-4.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 3.0.0-4.1
- rebuild with new gmp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec  7 2010 Dan Horák <dan[at]danny.cz> 3.0.0-3
- update the compat Provides for non-x86 arches

* Wed Dec  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> 3.0.0-2
- fix -devel description (see 603021#c3)

* Tue Nov 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> 3.0.0-1
- update to 3.0.0
- created links and provides to .1

* Fri Dec 18 2009 Ivana Hutarova Varekova <varekova@redhat.com> 2.4.2-1
- update to 2.4.2

* Fri Nov 13 2009 Ivana Varekova <varekova@redhat.com> 2.4.1-5
- fix 537328 - mpfr-devel should "Requires: gmp-devel"

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.4.1-4
- Use lzma compressed upstream tarball.

* Mon Aug 10 2009 Ivana Varekova <varekova redhat com> 2.4.1-3
- fix installation with --excludedocs option (#515958)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Ivana Varekova <varekova@redhat.com> - 2.4.1-1
- update to 2.4.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Ivana Varekova <varekova@redhat.com> - 2.4.0-1
- update to 2.4.0

* Wed Oct 15 2008 Ivana Varekova <varekova@redhat.com> - 2.3.2-1
- update to 2.3.2

* Mon Jul 21 2008 Ivana Varekova <varekova@redhat.com> - 2.3.1-1
- update to 2.3.1

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.0-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Ivana Varekova <varekova@redhat.com> 2.3.0-2
- rebuilt

* Thu Sep 20 2007 Ivana Varekova <varekova@redhat.com> 2.3.0-1
- update to 2.3.0
- fix license flag

* Mon Aug 20 2007 Ivana Varekova <varekova@redhat.com> 2.2.1-2
- spec file cleanup (#253440)

* Tue Jan 16 2007 Ivana Varekova <varekova@redhat.com> 2.2.1-1
- started

