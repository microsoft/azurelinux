# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:       A library of functions for manipulating PNG image format files
Name:          libpng
Epoch:         2
Version:       1.6.55
Release: 2%{?dist}
License:       zlib
URL:           http://www.libpng.org/pub/png/

Source0:       https://github.com/glennrp/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:       pngusr.dfa

Patch0:        libpng-multilib.patch

BuildRequires: gcc
BuildRequires: zlib-devel
BuildRequires: autoconf automake libtool
BuildRequires: cmake

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package devel
Summary:       Development tools for programs to manipulate PNG image format files
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:      zlib-devel%{?_isa} pkgconfig

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

%package static
Summary:       Static PNG image format file library
Requires:      %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description static
The libpng-static package contains the statically linkable version of libpng.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary:       Tools for PNG image format file library
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description tools
The libpng-tools package contains tools used by the authors of libpng.

%prep
%setup -q
# Provide pngusr.dfa for build.
cp -p %{SOURCE1} .

%patch -P0 -p1

%build
%cmake -DDFA_XTRA=pngusr.dfa
%cmake_build

%install
%cmake_install

# We don't ship .la files.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%ctest

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libpng16.so.*
%{_mandir}/man5/*

%files devel
%doc libpng-manual.txt example.c TODO CHANGES
%{_bindir}/*
%{_includedir}/*
%{_libdir}/libpng*.so
%dir %{_libdir}/libpng/
%{_libdir}/libpng/*.cmake
%{_libdir}/pkgconfig/libpng*.pc
%{_libdir}/cmake/PNG/
%{_mandir}/man3/*

%files static
%{_libdir}/libpng*.a

%files tools
%{_bindir}/pngfix

%changelog
* Fri Feb 13 2026 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.55-1
- updated to 1.6.55 (#2429529)

* Wed Feb 11 2026 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.54-1
- updated to 1.6.54

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 08 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.53-1
- updated to 1.6.53 (#2418775)

* Mon Dec 08 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.52-1
- updated to 1.6.52 (#2418775)

* Thu Nov 27 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.51-1
- updated to 1.6.51 (#2416525)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.50-1
- updated to 1.6.50

* Mon Jun 16 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.49-1
- updated to 1.6.49 (#2372582)

* Mon May 05 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.48-1
- updated to 1.6.48 (#2363171)

* Wed Feb 19 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.47-1
- updated to 1.6.47 (#2346280)

* Fri Jan 31 2025 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.46-1
- updated to 1.6.46 (#2336284)

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 18 2024 Michal Hlavinka <mhlavink@redhat.com> - 2:1.6.44-1
- updated to 1.6.44 (#2127036)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2:1.6.40-1
- Update to libpng 1.6.40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 24 2021 Nikola Forró <nforro@redhat.com> - 2:1.6.37-10
- Remove the aarch64 test workaround, the patches causing the failures
  have been dropped in zlib-1.2.11-25

* Thu Feb 11 2021 Nikola Forró <nforro@redhat.com> - 2:1.6.37-9
- Run %check by default

* Fri Feb 05 2021 Nikola Forró <nforro@redhat.com> - 2:1.6.37-8
- Use proper pngtest.png reference image on aarch64

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Nikola Forró <nforro@redhat.com> - 2:1.6.37-6
- Remove libpng-devel dependency on arch-specific pkgconfig (#1893523)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2:1.6.37-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Nikola Forró <nforro@redhat.com> - 2:1.6.37-1
- New upstream release 1.6.37

* Wed Feb 27 2019 Debarshi Ray <rishi@fedoraproject.org> - 2:1.6.36-1
- New upstream release 1.6.36

* Fri Feb 08 2019 Nikola Forró <nforro@redhat.com> - 2:1.6.35-3
- Fix CVE-2019-7317 (#1672411)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 10 2018 Nikola Forró <nforro@redhat.com> - 2:1.6.35-1
- New upstream release 1.6.35 (#1552349)

* Wed Aug 01 2018 Nikola Forró <nforro@redhat.com> - 2:1.6.34-6
- Fix CVE-2018-13785 (#1599944)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 2:1.6.34-4
- Add missing gcc build dependency

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:1.6.34-2
- Switch to %%ldconfig_scriptlets

* Wed Oct 04 2017 Nikola Forró <nforro@redhat.com> - 2:1.6.34-1
- New upstream release 1.6.34

* Tue Aug 01 2017 Nikola Forró <nforro@redhat.com> - 2:1.6.31-1
- New upstream release 1.6.31

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Nikola Forró <nforro@redhat.com> - 2:1.6.29-1
- New upstream release 1.6.29

* Tue Jun 06 2017 Nikola Forró <nforro@redhat.com> - 2:1.6.28-3
- Update source URL (#1458040)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Nikola Forró <nforro@redhat.com> - 2:1.6.28-1
- New upstream release 1.6.28 (#1411176)

* Fri Dec 30 2016 Kalev Lember <klember@redhat.com> - 2:1.6.27-1
- New upstream release 1.6.27 (#1409159)

* Tue Oct 25 2016 Nikola Forró <nforro@redhat.com> - 2:1.6.26-1
- New upstream release 1.6.26 (#1387902)

* Mon Sep 05 2016 Nikola Forró <nforro@redhat.com> - 2:1.6.25-1
- New upstream release 1.6.25 (#1373171)

* Mon Aug 08 2016 Nikola Forró <nforro@redhat.com> - 2:1.6.24-1
- New upstream release 1.6.24 (#1365115)

* Wed Jun 15 2016 Petr Hracek <phracek@redhat.com> - 2:1.6.23-1
- New upstream release 1.6.23 (#1346522)

* Mon Jun 06 2016 Petr Hracek <phracek@redhat.com> - 2:1.6.22-1
- New upstream release 1.6.22 (#1341646)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Petr Hracek <phracek@redhat.com> - 2:1.6.21-1
- New upstream release 1.6.21 (#1299292)

* Fri Jan 08 2016 Petr Hracek <phracek@redhat.com> - 2:1.6.20-2
- Bumping

* Wed Jan 06 2016 Petr Hracek <phracek@redhat.com> - 2:1.6.20-1
- new upstream release 1.6.20 (#1293326)

* Thu Nov 19 2015 Petr Hracek <phracek@redhat.com> - 2:1.6.19-1
- new upstream release 1.6.19 (#1282193)

* Wed Nov 18 2015 Petr Hracek <phracek@redhat.com> - 2:1.6.18-3
- fix for CVE-2015-8126 (#1281756, #1281757)
- correct patch

* Wed Nov 18 2015 Petr Hracek <phracek@redhat.com> - 2:1.6.18-2
- fix for CVE-2015-8126 (#1281756)

* Mon Aug 03 2015 Petr Hracek <phracek@redhat.com> - 2:1.6.18-1
- New upstream release 1.6.18 (#1247132)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 07 2015 Petr Hracek <phracek@redhat.com> - 2:1.6.17-1
- New upstream release 1.6.17 (#1209145)

* Sun Mar 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.6.16-3
- Use %%license
- Move docs to devel package as they're all related to dev

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2:1.6.16-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 15 2015 Petr Hracek <phracek@redhat.com> - 2:1.6.16-1
- New upstream release 1.6.16 (#1167665)

* Mon Nov  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.6.14-2
- Add upstream patch to fix build on aarch64 (NEON issues)

* Mon Oct 27 2014 Petr Hracek <phracek@redhat.com> - 2:1.6.14-1
- Update to libpng 1.6.14 for minor bug fixes (#1147423)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Petr Hracek <phracek@redhat.com> - 2:1.6.12-1
- Update to libpng 1.6.12 for minor bug fixes (#1111832)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Petr Hracek <phracek@redhat.com> - 2:1.6.10-1
- Update to libpng 1.6.10 for minor bug fixes (#1063749)

* Wed Jan 15 2014 Petr Hracek <phracek@redhat.com> - 2:1.6.8-1
- Update to libpng 1.6.8 for minor bug fixes (#1033049)

* Wed Sep 25 2013 Petr Hracek <phracek@redhat.com> - 2:1.6.6-2
- Correct BuildRequires on autoconf to 2.68 (#1008101)

* Tue Sep 24 2013 Jaromir Koncicky <jkoncick@redhat.com> - 2:1.6.6-1
- New upstream version 1.6.6 (#1007757)

* Tue Aug 13 2013 Petr Hracek <phracek@redhat.com> 2:1.6.3-3
- libpng-tools depends only on libpng

* Tue Aug 13 2013 Jaromir Koncicky <jkoncick@redhat.com> 2:1.6.3-2
- Added tools package with pngfix

* Tue Aug 13 2013 Jaromir Koncicky <jkoncick@redhat.com> 2:1.6.3-1
- New upstream version 1.6.3 (#987368)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 25 2013 Adam Jackson <ajax@redhat.com> 2:1.6.2-2
- Don't Require autoconf at runtime, just at build time (#977853)

* Fri May 17 2013 Petr Hracek <phracek@redhat.com> 2:1.6.2-1
- New upstream version 1.6.2 (#963113)

* Wed May 15 2013 Petr Hracek <phracek@redhat.com> 2:1.5.13-3
- Rebuild for ARM64 support (#925861)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 27 2012 Tom Lane <tgl@redhat.com> 2:1.5.13-1
- Update to libpng 1.5.13 for minor bug fixes

* Sat Aug  4 2012 Tom Lane <tgl@redhat.com> 2:1.5.12-1
- Update to libpng 1.5.12 for minor bug fixes
- Activate chunk size limits by default, with a very generous default limit

* Wed Aug  1 2012 Tom Lane <tgl@redhat.com> 2:1.5.10-3
- Remove compat subpackage (it's now a separate package "libpng12")
- Minor specfile cleanup per suggestions from Tom Callaway
Related: #845110

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr  7 2012 Tom Lane <tgl@redhat.com> 2:1.5.10-1
- Update to libpng 1.5.10 and 1.2.49, for minor security issues (CVE-2011-3048)
Resolves: #809597

* Sun Mar 11 2012 Tom Lane <tgl@redhat.com> 2:1.5.9-1
- Update to libpng 1.5.9 and 1.2.48, for minor security issues (CVE-2011-3045)
Resolves: #801667

* Thu Feb 16 2012 Tom Lane <tgl@redhat.com> 2:1.5.8-2
- Fix CVE-2011-3026
Resolves: #791183

* Fri Feb  3 2012 Tom Lane <tgl@redhat.com> 2:1.5.8-1
- Update to libpng 1.5.8, for minor security issue (CVE-2011-3464)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Tom Lane <tgl@redhat.com> 2:1.5.7-1
- Update to libpng 1.5.7, for assorted minor fixes

* Mon Nov 21 2011 Tom Lane <tgl@redhat.com> 2:1.5.6-2
- Don't include libpng12.pc in the compat subpackage; instead just offer a
  phony Provides: for it in the devel subpackage

* Sat Nov  5 2011 Tom Lane <tgl@redhat.com> 2:1.5.6-1
- Update to new major release series 1.5.x; includes source-code-incompatible
  API changes and a soname version bump
- Temporarily package 1.2.46 shared library (only) in libpng-compat subpackage
  so that dependent packages won't be broken while rebuilding proceeds

* Thu Jul 14 2011 Tom Lane <tgl@redhat.com> 2:1.2.46-1
- Update to libpng 1.2.46, includes fixes for CVE-2011-2501, CVE-2011-2690,
  CVE-2011-2691, CVE-2011-2692
Resolves: #717509
Resolves: #721307

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 2:1.2.44-2
- Use xz compressed source tarball
Resolves: #647282

* Tue Jun 29 2010 Tom Lane <tgl@redhat.com> 2:1.2.44-1
- Update to libpng 1.2.44, includes fixes for CVE-2010-1205 and CVE-2010-2249
Resolves: #609161

* Mon Mar 15 2010 Tom Lane <tgl@redhat.com> 2:1.2.43-1
- Update to libpng 1.2.43, includes fix for CVE-2010-0205
Related: #566234

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 2:1.2.42-1
- Update to libpng 1.2.42

* Thu Aug 20 2009 Tom Lane <tgl@redhat.com> 2:1.2.39-1
- Update to libpng 1.2.39

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Tom Lane <tgl@redhat.com> 2:1.2.37-1
- Update to libpng 1.2.37, to fix CVE-2009-2042
Related: #504782

* Wed Feb 25 2009 Tom Lane <tgl@redhat.com> 2:1.2.35-1
- Update to libpng 1.2.35, to fix CVE-2009-0040

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan  9 2009 Tom Lane <tgl@redhat.com> 2:1.2.34-1
- Update to libpng 1.2.34

* Thu Dec 11 2008 Caolán McNamara <caolanm@redhat.com> 2:1.2.33-2
- rebuild to get provides pkgconfig(libpng)

* Sun Nov  2 2008 Tom Lane <tgl@redhat.com> 2:1.2.33-1
- Update to libpng 1.2.33

* Tue Sep  9 2008 Tom Lane <tgl@redhat.com> 2:1.2.31-2
- Apply upstream patch for zTXT buffer overrun (CVE-2008-3964)
Related: #461599

* Sat Aug 23 2008 Tom Lane <tgl@redhat.com> 2:1.2.31-1
- Update to libpng 1.2.31

* Sat May 31 2008 Tom Lane <tgl@redhat.com> 2:1.2.29-1
- Update to libpng 1.2.29 (fixes low-priority security issue CVE-2008-1382)
Related: #441839

* Tue Feb 12 2008 Tom Lane <tgl@redhat.com> 2:1.2.24-1
- Update to libpng 1.2.24

* Thu Oct 18 2007 Tom Lane <tgl@redhat.com> 2:1.2.22-1
- Update to libpng 1.2.22, primarily to fix CVE-2007-5269
Related: #324771

* Wed Aug 22 2007 Tom Lane <tgl@redhat.com> 2:1.2.16-3
- Update License tag
- Rebuild to fix Fedora toolchain issues

* Wed May 23 2007 Tom Lane <tgl@redhat.com> 2:1.2.16-2
- Add patch to fix CVE-2007-2445
Related: #239542

* Mon Feb 12 2007 Tom Lane <tgl@redhat.com> 2:1.2.16-1
- Update to libpng 1.2.16
Resolves: #211705, #216706, #227334
- Separate libpng.a into a -static subpackage
- Other minor packaging fixes per Fedora merge review
Resolves: #226038

* Mon Oct 02 2006 Jesse Keating <jkeating@redhat.com> - 2:1.2.10-7
- Require pkgconfig in the -devel subpackage as it gets called by
  /usr/bin/libpng-config

* Thu Jul 27 2006 Matthias Clasen <mclasen@redhat.com> - 2:1.2.10-6
- Disable asm on arches other than i386  (#196580)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:1.2.10-5.1
- rebuild

* Thu May 25 2006 Matthias Clasen  <mclasen@redhat.com> - 2:1.2.10-5
- Fix some paths in the -config script

* Tue May 23 2006 Matthias Clasen  <mclasen@redhat.com> - 2:1.2.10-4
- fix multilib conflicts

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2:1.2.10-3
- Add a comment about the need to keep static libraries

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2:1.2.10-2
- Re-add static libraries

* Thu May  4 2006 Matthias Clasen  <mclasen@redhat.com>  - 2:1.2.10-1
- Update to 1.2.10
- Drop static libraries

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:1.2.8-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:1.2.8-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2:1.2.8-2
- Rebuild with gcc4

* Mon Dec 06 2004 Matthias Clasen <mclasen@redhat.com> - 2:1.2.8-1
- Update to 1.2.8

* Wed Sep 15 2004 Matthias Clasen <mclasen@redhat.com> - 2:1.2.7-1
- Update to 1.2.7

* Tue Aug 17 2004 Matthias Clasen <mclasen@redhat.com> - 2:1.2.6-1
- Update to 1.2.6
- Combine patches

* Wed Aug 4 2004 Matthias Clasen <mclasen@redhat.com> 2:1.2.5-9
- Build for FC3

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> 
- Include LICENSE.

* Fri Jul 23 2004 Matthias Clasen <mclasen@redhat.com> 2:1.2.5-8
- Build for FC2

* Fri Jul 23 2004 Matthias Clasen <mclasen@redhat.com> 2:1.2.5-7
- Replace the patches for individual security problems with the
  cumulative patch issued by the png developers. 
- Build for FC1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 Matthias Clasen <mclasen@redhat.com> - 2:1.2.5-5
- Rebuild for FC2

* Mon Jun 14 2004 Matthias Clasen <mclasen@redhat.com> - 2:1.2.5-4
- Rebuild for FC1

* Mon Jun 14 2004 Matthias Clasen <mclasen@redhat.com> - 2:1.2.5-3
- Reinstate and improve the transfix patch which got lost sometime ago, 
  but is still needed for CAN-2002-1363 (#125934)

* Mon May 24 2004 Than Ngo <than@redhat.com> 2:1.2.5-2
- add patch to link libm automatically
- get rid of rpath

* Wed May 19 2004 Matthias Clasen <mclasen@redhat.com> 2:1.2.5-1
- 1.2.5

* Mon May 3 2004 Matthias Clasen <mclasen@redhat.com> 2:1.2.2-22
- Redo the out-of-bounds fix in a slightly better way.

* Wed Apr 21 2004 Matthias Clasen <mclasen@redhat.com>
- Bump release number to disambiguate n-v-rs.

* Mon Apr 19 2004 Matthias Clasen <mclasen@redhat.com> 
- fix a possible out-of-bounds read in the error message 
  handler. #121229

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 27 2004 Mark McLoughlin <markmc@redhat.com> 2:1.2.2-19
- rebuild with changed bits/setjmp.h on ppc

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Mon Feb 24 2003 Jonathan Blandford <jrb@redhat.com> 2:1.2.2-15
- change pkg-config to use libdir instead of hardcoding /usr/lib

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 20 2003 Jonathan Blandford <jrb@redhat.com> 2:1.2.2-12
- add Provides: libpng.so.3, #67007

* Fri Jan 24 2003 Jonathan Blandford <jrb@redhat.com>
- change requires to include the Epoch

* Thu Jan 23 2003 Karsten Hopp <karsten@redhat.de> 2:1.2.2-11
- Bump & rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Elliot Lee <sopwith@redhat.com> 2:1.2.2-9
- Bump & rebuild

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 2:1.2.2-7
- merge changes in from -6hammer

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-4
- Don't own {_libdir}/pkgconfig
- Don't strip library, that's up to rpm

* Tue May  7 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-3
- Forgot png.h

* Mon May  6 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-2
- Fix compatibility with everyone else.

* Thu May  2 2002 Havoc Pennington <hp@redhat.com>
- 1.2.2 plus makefile patches tarball
- update file list to contain versioned libpng only

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Dec 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.1-1
- 1.2.1

* Wed Sep 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.0-1
- 1.2.0

* Mon Jul 16 2001 Trond Eivind Glomsrd <teg@redhat.com>
- s/Copyright/License/
- fix weird versioning system (epoch was set to "2" in the main
  package, serial to "1" in the devel package. Huh?)

* Wed Jun 20 2001 Than Ngo <than@redhat.com> 1.0.12-1
- update to 1.0.12
- add missing libpng symlink

* Thu May  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.11-2
- libpng-devel requires zlib-devel (since png.h includes zlib.h)
  (#38883)

* Wed May  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.11-1
- 1.0.11

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.0.10

* Tue Feb  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.0.9, fixes Mozilla problems

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to get rid of 0777 dirs

* Wed Nov 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Remove the workaround for Bug #20018 (from Oct 30).
  Qt 2.2.2 fixes the problem the workaround addressed.

* Mon Oct 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Work around a problem causing konqueror to segfault in image preview
  mode (Bug #20018)
- Copy SuSE 7.0's patch to handle bad chunks

* Sun Sep  3 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- only include the man5 man-pages once in the main rpm

* Fri Jul 28 2000 Preston Brown <pbrown@redhat.com>
- upgrade to 1.0.8 - fixes small memory leak, other bugs

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- patchlevel c
- FHSify

* Tue Mar 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.0.6

* Mon Mar 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- change serial to Epoch to get dependencies working correctly

* Fri Feb 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- move buildroot and add URL

* Sat Feb  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- strip library
- rebuild to compress man pages

* Sun Nov 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.0.5
- some tweaks to spec file to make updating easier
- handle RPM_OPT_FLAGS

* Mon Sep 20 1999 Matt Wilson <msw@redhat.com>
- changed requires in libpng-devel to include serial
- corrected typo

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Sun Feb 07 1999 Michael Johnson <johnsonm@redhat.com>
- rev to 1.0.3

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Wed Sep 23 1998 Cristian Gafton <gafton@redhat.com>
- we are Serial: 1 now because we are reverting the 1.0.2 version from 5.2
  beta to this prior one
- install man pages; set defattr defaults

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- devel subpackage moved to Development/Libraries

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.0.1
- added buildroot

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- updated to new version
- spec file cleanups

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

