# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gettext_package FontForge

Name:           fontforge
Version:        20230101
Release: 20%{?dist}
Summary:        Outline and bitmap font editor

License:        GPL-3.0-or-later
URL:            http://fontforge.github.io/
Source0:        https://github.com/fontforge/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Fix translations with gettext-0.22, https://github.com/fontforge/fontforge/pull/5257
Patch0:         0001-Fix-errors-in-French-and-Italian-translations.patch
# https://github.com/fontforge/fontforge/pull/5367
# Fixes CVE-2024-25081 and CVE-2024-25082
Patch1:         https://patch-diff.githubusercontent.com/raw/fontforge/fontforge/pull/5367.patch#/Fix_Splinefont_shell_invocation.patch
Patch2:         pyconfig.patch
# https://github.com/fontforge/fontforge/pull/5491
Patch3:         fix_memleak_in_function_DlgCreate8-5491.patch
# CVE-2025-15279 https://github.com/fontforge/fontforge/pull/5720
# https://sourceforge.net/p/fontforge/patches/32/
Patch4:         https://patch-diff.githubusercontent.com/raw/fontforge/fontforge/pull/5720.patch
# CVE-2025-15275 https://github.com/fontforge/fontforge/pull/5721
# https://sourceforge.net/p/fontforge/patches/37/
Patch5:          https://patch-diff.githubusercontent.com/raw/fontforge/fontforge/pull/5721.patch
# CVE-2025-15269 https://github.com/fontforge/fontforge/pull/5722
# https://sourceforge.net/p/fontforge/patches/40/
Patch6:         https://patch-diff.githubusercontent.com/raw/fontforge/fontforge/pull/5722.patch
# CVE-2025-15279 https://github.com/fontforge/fontforge/pull/5723
# https://sourceforge.net/p/fontforge/patches/32/
Patch7:         https://patch-diff.githubusercontent.com/raw/fontforge/fontforge/pull/5723.patch


Requires:       xdg-utils
Requires:       (autotrace or potrace)
Requires:       hicolor-icon-theme

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  giflib-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  gettext
BuildRequires:  pango-devel
BuildRequires:  cairo-devel
BuildRequires:  libspiro-devel
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  libappstream-glib
BuildRequires:  woff2-devel
# F25 build is failing add following to fix
BuildRequires:  shared-mime-info
# F33 onward need now
BuildRequires:  gtk3-devel
BuildRequires:  python3-sphinx
BuildRequires: make

%py_provides python3-fontforge
%py_provides python3-psMat

%description
FontForge (former PfaEdit) is a font editor for outline and bitmap
fonts. It supports a range of font formats, including PostScript
(ASCII and binary Type 1, some Type 3 and Type 0), TrueType, OpenType
(Type2) and CID-keyed fonts.

%package devel
Summary: Development files for fontforge
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}

%description devel
This package includes the library files you will need to compile
applications against fontforge.

%package doc
Summary: Documentation files for %{name}
BuildArch: noarch

%description doc
This package contains documentation files for %{name}.


%prep
%autosetup -p1

# Remove tests that requires Internet access
sed -i '45d;82d;101d;127d' tests/CMakeLists.txt


%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%cmake -DCMAKE_BUILD_TYPE=Release \
          -DENABLE_WOFF2=ON \
          -DPYHOOK_INSTALL_DIR=%{python3_sitearch}
%cmake_build

%install
%cmake_install

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications            \
  --add-category X-Fedora                                  \
  desktop/org.fontforge.FontForge.desktop

# remove unneeded .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

rm -f %{buildroot}%{_datadir}/doc/fontforge/{.buildinfo,.nojekyll}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Find translations
%find_lang %{gettext_package}

%check
%ctest

%files -f %{gettext_package}.lang
%doc AUTHORS
%license LICENSE COPYING.gplv3
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_datadir}/applications/*FontForge.desktop
%{_datadir}/fontforge
%{_datadir}/icons/hicolor/*/apps/org.fontforge.FontForge*
%{_mandir}/man1/*.1*
%{_datadir}/mime/packages/fontforge.xml
%{_metainfodir}/org.fontforge.FontForge.appdata.xml
%{python3_sitearch}/fontforge.so
%{python3_sitearch}/psMat.so

%files devel
%{_libdir}/lib*.so

%files doc
%doc %{_pkgdocdir}

%changelog
* Fri Jan 23 2026 Parag Nemade <pnemade AT redhat DOT com> - 20230101-19
- Resolves: CVE-2025-15279
- Resolves: CVE-2025-15275
- Resolves: CVE-2025-15269

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20230101-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Parag Nemade <pnemade AT redhat DOT com> - 20230101-17
- Update for https://fedoraproject.org/wiki/Changes/CMake_ninja_default (rh#2381004)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 20230101-16
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20230101-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230101-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 20230101-13
- Patch for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 20230101-12
- Rebuilt for Python 3.13

* Wed Feb 28 2024 Parag Nemade <pnemade AT redhat DOT com> - 20230101-11
- Resolves: CVE-2024-25081 and CVE-2024-25082

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230101-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230101-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 20230101-8
- Drop unused libuninameslist dependency

* Tue Aug 08 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 20230101-7
- Allow potrace as an alternative to autotrace

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230101-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Parag Nemade <pnemade AT redhat DOT com> - 20230101-5
- Fix fr.po and it.po translations issue

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 20230101-4
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Parag Nemade <pnemade AT redhat DOT com> - 20230101-2
- Update license tag to SPDX format
- Fix test failure

* Mon Jan 02 2023 Parag Nemade <pnemade AT redhat DOT com> - 20230101-1
- Update to 20230101 version (#2157290)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220308-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 20220308-2
- Rebuilt for Python 3.11

* Thu Mar 10 2022 Parag Nemade <pnemade AT redhat DOT com> - 20220308-1
- Update to 20220308 version (#2062047)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20201107-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201107-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 20201107-4
- Rebuilt for Python 3.10

* Mon Feb 01 2021 Parag Nemade <pnemade AT redhat DOT com> - 20201107-3
- The %%find_lang should run as part of %%install only

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Parag Nemade <pnemade AT redhat DOT com> - 20201107-1
- Update to 20201107 version (#1895648)
- removed %%gittag0 macro, as it cause problem to automated package update script

* Sun Nov 22 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 20200314-10
- Add py_provides macros to provide python3-fontforge, python3-psMat, etc.

* Wed Aug 05 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200314-9
- Fix FTBFS bug by fixing glossary.rst and using new CMake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200314-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200314-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 20200314-6
- Rebuilt for Python 3.9

* Sat May 02 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200314-5
- Resolves:rhbz#1830502 - Add missing WOFF2 support

* Wed Apr 15 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200314-4
- Resolves:rhbz#1823525 - fontforge fails to build with Sphinx 3.0.0

* Thu Apr 02 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200314-3
- Fix the GDK backend UI issues
- Move back to using GDK backend

* Fri Mar 27 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200314-2
- Enabled X11 and 2012 theme

* Wed Mar 25 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200314-1
- Update to 20200314 version (#1813578)

* Sun Feb 16 2020 Parag Nemade <pnemade AT redhat DOT com> - 20190801-6
- another fix for rh#1790042 - CVE-2020-5395:out-of-bounds write in sfd.c

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190801-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Parag Nemade <pnemade AT redhat DOT com> - 20190801-4
- Resolves:rh#1790042 - CVE-2020-5395:out-of-bounds write in sfd.c

* Tue Aug 27 2019 Kevin Fenzi <kevin@scrye.com> - 20190801-3
- Rebuild for new libspiro

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 20190801-2
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Parag Nemade <pnemade AT redhat DOT com> - 20190801-1
- Update to 20190801 version (#1739819)
- Upstream moved to use Glib's GHashTable over uthash
- Upstream dropped requiring bundling copy of gnulib

* Fri Aug 02 2019 Parag Nemade <pnemade AT redhat DOT com> - 20190413-4
- Fix the conditional for rh#1728058

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190413-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 20190413-2
- make the code compatible with python-3.8 (rh#1728058)

* Sat Apr 13 2019 Parag Nemade <pnemade AT redhat DOT com> - 20190413-1
- Update to 20190413 version (#1689629)

* Mon Mar 25 2019 Parag Nemade <pnemade AT redhat DOT com> - 20190317-1
- Update to 20190317 release (#1689629)

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 20170731-12
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20170731-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Miro Hrončok <mhroncok@redhat.com> - 20170731-10
- Rebuilt for #1595421

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170731-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Kevin Fenzi <kevin@scrye.com> - -8
- Update bundled gnulib. Fixes bug #1596037

* Thu Jun 28 2018 Miro Hrončok <mhroncok@redhat.com> - 20170731-7
- Rebuilt for Python 3.7.0 final (#1595421)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 20170731-6
- Rebuilt for Python 3.7

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 20170731-5
- Rebuild (giflib)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170731-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 20170731-3
- Remove obsolete scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170731-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Parag Nemade <pnemade AT redhat DOT com> - 20170731-1
- Update to 20170731

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161012-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 09 2017 Parag Nemade <pnemade AT redhat DOT com> - 20161012-6
- Resolves:rh#1429574 - [abrt] fontforge: PyFF_OpenFont(): fontforge killed by signal 6
- Added patch to fix python module for python3.6

* Sat Feb 18 2017 Parag Nemade <pnemade AT redhat DOT com> - 20161012-5
- Add missing BR: git

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 20161012-3
- Rebuild for readline 7.x

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 20161012-2
- Rebuild for Python 3.6

* Thu Oct 13 2016 Parag Nemade <pnemade AT redhat DOT com> - 20161012-1
- Update to 20161012

* Thu Oct 06 2016 Parag Nemade <pnemade AT redhat DOT com> - 20161005-1
- Update to 20161005

* Wed Oct 05 2016 Parag Nemade <pnemade AT redhat DOT com> - 20161004-1
- Update to 20161004

* Mon Oct 03 2016 Parag Nemade <pnemade AT redhat DOT com> - 20161001-1
- Update to 20161001

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20160404-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 07 2016 Parag Nemade <pnemade AT redhat DOT com> - 20160404-3
- Rebuild for new libuninameslist-20160701 build
- Add BuildRequires: shared-mime-info
- Add BuildRequires: gcc

* Wed Apr 06 2016 Parag Nemade <pnemade AT redhat DOT com> - 20160404-2
- Move from python2 to python3 support

* Tue Apr 05 2016 Parag Nemade <pnemade AT redhat DOT com> - 20160404-1
- Update to 20160404

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20150824-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 26 2015 Parag Nemade <pnemade AT redhat DOT com> - 20150824-1
- Update to 20150824
- Follow https://fedoraproject.org/wiki/Packaging:SourceURL#Git_Tags

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150612-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 13 2015 Parag Nemade <pnemade AT redhat DOT com> - 20150612-1
- Update to 20150612

* Fri May 01 2015 Parag Nemade <pnemade AT redhat DOT com> - 20150430-1
- Update to 20150430

* Mon Mar 30 2015 Parag Nemade <pnemade AT redhat DOT com> - 20150330-1
- Update to 20150330
- use %%license macro for LICENSE file

* Thu Mar 12 2015 Parag Nemade <pnemade AT redhat DOT com> - 20150228-1
- Update to 20150228

* Sun Feb 01 2015 Kevin Fenzi <kevin@scrye.com> 20141230-2
- Rebuild for new libspiro

* Sun Jan 04 2015 Kevin Fenzi <kevin@scrye.com> 20141230-1
- Update to 20141230

* Tue Sep 09 2014 Parag Nemade <pnemade AT redhat DOT com> - 20140813-3
- drop BR: python-ipython for aarch64 builds (rh#1139508)

* Mon Sep 08 2014 Parag Nemade <pnemade AT redhat DOT com> - 20140813-2
- Add gnulib source for bootstrap as koji don't have network
- Patch Makefile.am to use system uthash-devel
- We also need gnulib-devel

* Mon Sep 08 2014 Parag Nemade <pnemade AT redhat DOT com> - 20140813-1
- Update to fontforge 2.0 snapshot 20140813
- corrected some scriptlets as per packaging guidelines
- Added new subpackage -doc

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120731b-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Rex Dieter <rdieter@fedoraproject.org> 20120731b-12
- update mime scriptlet

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120731b-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 02 2013 Parag Nemade <pnemade AT redhat DOT com> - 20120731b-10
- Revert previously added -Wstrict-aliasing cflags
- We actaully need -fno-strict-aliasing (rh#903288)
- Remove %%defattr() (rh#1003518)
- fontforge.xml should not be executable (rh#1003518)

* Thu Aug 22 2013 Parag Nemade <pnemade AT redhat DOT com> - 20120731b-9
- Added cflags -Wstrict-aliasing
- Fixed some compile-time errors from invalid Makefile rules
- Fixed bogus date in changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120731b-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Paul Flo Williams <paul@frixxon.co.uk> - 20120731b-7
- Don't crash on PDFs with filters we can't understand. Fixes bug #906492

* Sat Mar 23 2013 Kevin Fenzi <kevin@scrye.com> 20120731b-6
- Add fix for aarch64 support. Fixes bug #925354

* Mon Feb 11 2013 Paul Flo Williams <paul@frixxon.co.uk> - 20120731b-5
- De-vendorize desktop installation

* Thu Feb 07 2013 Paul Flo Williams <paul@frixxon.co.uk> - 20120731b-4
- Patch for bug #902089, out-of-bounds errors while reading PDFs

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 20120731b-3
- rebuild due to "jpeg8-ABI" feature drop

* Tue Nov 27 2012 Kevin Fenzi <kevin@scrye.com> 20120731b-2
- Cosmetic cleanups for bug 880472

* Thu Aug 02 2012 Paul Flo Williams <paul@frixxon.co.uk> - 20120731b-1
- Update to 20120731b (problem with 64-bit builds in first release)

* Thu Aug 02 2012 Paul Flo Williams <paul@frixxon.co.uk> - 20120731-1
- Update to 20120731

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110222-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Kevin Fenzi <kevin@scrye.com> - 20110222-8
- Rebuild for new libtiff. 

* Sat Jan 28 2012 Parag Nemade <paragn AT fedoraproject.org> - 2011022-7
- Add patch for libpng15

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110222-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 20110222-5
- Rebuild for new libpng

* Thu Apr 07 2011 Parag Nemade <paragn AT fedoraproject.org> - 2011022-4
- Add patch for multilib. Fixes bug #694409

* Thu Mar 31 2011 Paul Flo Williams <paul@frixxon.co.uk> - 20110222-3
- Add patch for charview crash. Fixes bug #660376

* Thu Mar 17 2011 Kevin Fenzi <kevin@tummy.com> - 20110222-2
- Drop sources that are now upstream. Fixes bug #688470

* Tue Feb 22 2011 Kevin Fenzi <kevin@tummy.com> - 20110222-1
- Update to 20110222

* Wed Feb 16 2011 Kevin Fenzi <kevin@tummy.com> - 20100501-7
- Fix patch for python. Fixes bug #677917
- Add patch for unicode glyph crash. Fixes bug #631172

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100501-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 04 2010 Kevin Fenzi <kevin@tummy.com> - 20100501-5
- Add patch for CVE-2010-4259

* Wed Jul 28 2010 Kevin Fenzi <kevin@tummy.com> - 20100501-4
- Add patch to build with python 2.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 20100501-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 Kevin Fenzi <kevin@tummy.com> - 20100501-2
- Add patch for bug 536920

* Wed May 19 2010 Kevin Fenzi <kevin@tummy.com> - 20100501-1
- Update to 20100501

* Fri Apr 30 2010 Kevin Fenzi <kevin@tummy.com> - 20100429-1
- Update to 20100429

* Sat Mar 20 2010 Kevin Fenzi <kevin@tummy.com> - 20090923-3
- Fix patch to fix python module (fixes #560277)

* Wed Dec 30 2009 Kevin Fenzi <kevin@tummy.com> - 20090923-2
- Add patch to fix relative paths for fontlint (fixes #530760)

* Sun Nov 01 2009 Kevin Fenzi <kevin@tummy.com> - 20090923-1
- Upgrade to 20090923

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090622-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Kevin Fenzi <kevin@tummy.com> - 20090622-1
- Upgrade to 20090622

* Thu Apr 16 2009 Kevin Fenzi <kevin@tummy.com> - 20090408-1
- Upgrade to 20090408

* Thu Apr 02 2009 Kevin Fenzi <kevin@tummy.com> - 20090224-2
- Apply patch for python modules loading (fixes #489109)
- use install -p to fix multiarch issue (fixes #480685)

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 20090224-1
- Upgrade to 20090224

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081224-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 20081224-2
— global-ization

* Fri Feb 20 2009 Kevin Fenzi <kevin@tummy.com> - 20081224-1
- Upgrade to 20081224
- Enable python bindings

* Wed Jan 21 2009 Kevin Fenzi <kevin@tummy.com> - 20081215-4
- Add python-devel to BuildRequires

* Tue Dec 23 2008 Kevin Fenzi <kevin@tummy.com> - 20081215-3
- Add patch to fix buffer overflow. Fixes 471538

* Wed Dec 17 2008 Kevin Fenzi <kevin@tummy.com> - 20081215-2
- Add libspiro-devel to build with spiro

* Tue Dec 16 2008 Kevin Fenzi <kevin@tummy.com> - 20081215-1
- Upgrade to 20081215
- Build with cairo and pango

* Mon Dec 01 2008 Kevin Fenzi <kevin@tummy.com> - 20081117-1
- Upgrade to 20081117

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 20080927-2
- Rebuild for Python 2.6

* Sat Nov 08 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 20080927-1
☢ quick & dirty version bump to start working on F11 font packages
⟲ time to forget about pfaedit
⤑ take care of rpmlint warnings

* Wed Sep 03 2008 Kevin Fenzi <kevin@tummy.com> - 20080828-1
- Upgrade to 20080828
- Add Requires on autotrace. Fixes 460668
- Confirm patch from 459451 is upstream here.

* Fri May 16 2008 Kevin Fenzi <kevin@tummy.com> - 20080429-1
- Upgrade to 20080429

* Mon Mar 24 2008 Kevin Fenzi <kevin@tummy.com> - 20080309-2
- Add mime info for .sfd files. Fixes 240669

* Mon Mar 17 2008 Kevin Fenzi <kevin@tummy.com> - 20080309-1
- Upgrade to 20080309
- Fixes bug 437833

* Mon Mar 03 2008 Kevin Fenzi <kevin@tummy.com> - 20080302-2
- Commit new sources

* Mon Mar 03 2008 Kevin Fenzi <kevin@tummy.com> - 20080302-1
- Update to upstream 20080302

* Sun Mar 02 2008 Kevin Fenzi <kevin@tummy.com> - 20080203-2
- Change Requires from htmlview to xdg-utils (bz 312691)

* Sat Mar 01 2008 Kevin Fenzi <kevin@tummy.com> - 20080203-1
- Update to upstream 20080203
- Add new devel subpackage

* Sun Dec 02 2007 Roozbeh Pournader <roozbeh@farsiweb.info> - 20071110-1
- Update to upstream 20071110

* Sun Oct 21 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☢ 20071002-1
⚠ quick & dirty version bump to start working on F9 font packages

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 20070511-2
- Rebuild for BuildID

* Thu Jun  7 2007 Kevin Fenzi <kevin@tummy.com> - 20070511-1
- Update to upstream 20070511
- Remove some leftover CVS bits
- Remove useless .pc file.

* Fri Dec 22 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20061220-1
- Update to upstream 20061220

* Sat Dec 09 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20061025-2
- Add patch to fix fsSelection problem with DejaVu ExtraLight

* Sat Nov 25 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20061025-1
- Update to 20061025
- Patch to correct usFirstCharIndex (George Williams)

* Fri Oct 20 2006 Kevin Fenzi <kevin@tummy.com> - 20061019-1
- Update to 20061019

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 20060822-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Kevin Fenzi <kevin@tummy.com> - 20060822-1
- Update to 20060822
- Remove unneeded patch
- Add flag to compile right with giflib

* Sun Jun 18 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-7
- Add BuildRequires on gettext, to make sure the package builds in minimal
  mock environments

* Mon Feb 13 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-6
- Rebuild for Fedora Extras 5

* Sun Feb 12 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-5
- Add patch to fix crash (#181052, George Williams)

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-4
- Add "BuildRequires:" on libXt-devel and xorg-x11-proto-devel

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-3
- Really remove XFree86-devel BuildReq

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-2
- Remove XFree86-devel BuildReq

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-1
- Update to 20060125 (bug #170177)
- Update docs to 20060114
- Change versioning to reflect upstream and follow packaging guidelines
- Provide pfaedit (bug #176548)
- Use %%{?dist} tag (bug #176472)
- Add localizations
- No need to remove CVS subdir: fixed upstream
- No need to covert man pages to UTF-8: fixed upstream
- Fixed DOS line terminators
- Use parallel build

* Sat Jul 30 2005 Owen Taylor <otaylor@redhat.com> - 0.0-2.20050729.fc4
- Update to 20050729
- Remove .docview patch, looking for HTMLview is upstream so no longer needed

* Tue May 10 2005 Owen Taylor <otaylor@redhat.com> - 0.0-2.20050502.fc4
- Update to 20050502
- Fix the build to look for the docs where we install them

* Sat Mar 19 2005 Owen Taylor <otaylor@redhat.com> - 0.0-2.20050310
- Update to 20050310

* Sat Jan 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.0-2.20041231
- Avoid RPATH.
- Convert man pages to UTF-8.
- Fix pkgconfig and doc file permissions.
- Use updated upstream icon.
- Don't include installation documentation.

* Mon Jan 17 2005 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-1.20041231
- Updated to 20041231.

* Thu Oct 28 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20041014
- Updated to 20041014.

* Sun Sep 19 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040824
- Updated to 20040824.

* Wed Jun 30 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040618
- Updated to 20040618.

* Wed Jun  2 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040601
- Updated to 20040601.

* Tue May 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040509
- Updated to 20040509.

* Thu Apr 15 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040410
- Updated to 20040410.

* Sun Mar 28 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040321
- Updated to 20040321.
- Changed package name from pfaedit to fontforge.
- Added Obsoletes: pfaedit.

* Mon Mar 15 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.8.040310
- Updated to 040310.

* Sat Feb  7 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.8.040204
- Updated to 040204.
- Removed some unnecessary directory ownerships (bug 1061).

* Sun Jan 25 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.8.040111
- Updated documentation to 040111.

* Sun Jan 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.040111
- Updated to 040111.
- Converted spec file to UTF-8.

* Wed Jan  7 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.040102
- Updated to 040102.

* Sat Dec 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.031210
- Updated to 031210.

* Sat Dec 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.031205
- Updated to 031205.

* Fri Nov 28 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.031123
- Updated to 031123.

* Wed Nov 12 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.6.031110
- Updated to 031110.
- Eliminated build patch; incorporated in upstream tarball.
- Re-added documentation tarball since no longer included in source tarball.
- Added pfaicon.gif as Packaging directory disappeared from tarball.

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.5.031012
- Refetched sources since upstream suddenly decided to change them (bug 497).

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.4.031012
- Build req libuninameslist-devel instead of libuninameslist.

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.3.031012
- Fixed non-standard value in desktop file (bug 497).
- Added libuninameslist support.
- Removed separate documentation tarball; mostly identical to those in source (bug 497).

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.2.031012
- Patched to use dynamic linking instead of dlopen'ing (bug 497).
- Patched to use htmlview and use installed documentation (bug 497).
- Added build req libxml2-devel (bug 497).
- Disabled parallell make (bug 497).
- Added desktop entry (bug 497).

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.031012
- Updated to 031012.
- Removed .so links.
- Removed empty AUTHORS file.
- Removed the samples subpackage.

* Mon Sep 22 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030904
- Updated to 030904.

* Wed Sep  3 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030831
- Updated to 030831.

* Tue Aug 12 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030803
- Updated to 030803.

* Mon Jul 21 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.3.030702
- Added font samples.
- Added ldconfig to post and postun.
- Added samples subpackage.

* Sun Jul  6 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.2.030702
- Removed README-MS and README-MacOSX from documentation.

* Thu Jul  3 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030512
- Initial RPM release based on Mandrake's PfaEdit-030512 RPM.
