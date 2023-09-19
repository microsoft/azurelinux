## 1.11 currently disables tests with BUILD_SHARED_LIBS=ON
#bcond_without tests
#bcond_without doc
%global apidocdir __api-doc_fedora
Summary:        Audio Meta-Data Library
Name:           taglib
Version:        1.13.1
Release:        1%{?dist}
License:        LGPLv2 OR MPLv1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://taglib.github.io/
# The snapshot tarballs generated with the following script:
Source1:        taglib-snapshot.sh
# http://bugzilla.redhat.com/343241
Patch102:       taglib-1.13.1-multilib.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel
%if 0%{?snap:1}
Source0:        taglib-%{version}-%{snap}.tar.gz
%else
Source0:        http://taglib.github.io/releases/taglib-%{version}%{?beta}.tar.gz
%endif
%if %{with tests}
BuildRequires:  cppunit-devel
%endif
%if %{with doc}
BuildRequires:  doxygen
BuildRequires:  graphviz
%endif

%description
TagLib is a library for reading and editing the meta-data of several
popular audio formats. Currently it supports both ID3v1 and ID3v2 for MP3
files, Ogg Vorbis comments and ID3 tags and Vorbis comments in FLAC, MPC,
Speex, WavPack, TrueAudio files, as well as APE Tags.

%package doc
Summary:        API Documentation for %{name}
BuildArch:      noarch

%description doc
This is API documentation generated from the TagLib source code.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if ! %{with doc}
Obsoletes:      %{name}-doc
%endif

%description devel
Files needed when building software with %{name}.

%prep
%autosetup -n taglib-%{version}%{?beta} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. \
%if %{with tests}
  -DBUILD_TESTS:BOOL=ON \
%endif
  -DCMAKE_BUILD_TYPE:STRING="Release"
popd

%make_build -C %{_target_platform}

%if %{with doc}
make docs -C %{_target_platform}
%endif


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%if %{with doc}
rm -fr %{apidocdir} ; mkdir %{apidocdir}
cp -a %{_target_platform}/doc/html/ %{apidocdir}/
ln -s html/index.html %{apidocdir}
find %{apidocdir} -name '*.md5' | xargs rm -fv
%endif


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion taglib)" = "%{version}"
test "$(pkg-config --modversion taglib_c)" = "%{version}"
%if %{with tests}
#ln -s ../../tests/data %{_target_platform}/tests/
#LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH \
make check -C %{_target_platform}
%endif

%ldconfig_scriptlets

%files
%doc AUTHORS NEWS
%license COPYING.LGPL COPYING.MPL
%{_libdir}/libtag.so.1*
%{_libdir}/libtag_c.so.0*

%files devel
%doc examples
%{_bindir}/taglib-config
%{_includedir}/taglib/
%{_libdir}/libtag.so
%{_libdir}/libtag_c.so
%{_libdir}/pkgconfig/taglib.pc
%{_libdir}/pkgconfig/taglib_c.pc

%if %{with doc}
%files doc
%doc %{apidocdir}/*
%endif


%changelog
* Mon Sep 18 2023 Archana Choudhary <archana1@microsoft.com> - 1.13.1-1
- Upgrade to 1.13.1 - CVE-2018-11439, CVE-2017-12678
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.1-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.11.1-8
- use %%make_build

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.11.1-6
- Switch to %%ldconfig_scriptlets

* Tue Aug 22 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.11.1-5
-  CVE-2017-12678 taglib: Incorrect cast in rebuildAggregateFrames function (#1483960,#1483959)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.11.1-1
- taglib-1.11.1

* Fri Apr 29 2016 Rex Dieter <rdieter@fedoraproject.org> 1.11-1
- taglib-1.11

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 1.11-0.3.beta2
- taglib-1.11beta2

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-0.2.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Rex Dieter <rdieter@fedoraproject.org> 1.11-0.1.beta
- taglib-1.11beta

* Sat Jan 30 2016 Rex Dieter <rdieter@fedoraproject.org> 1.10-2
- disable regression tests on rawhide (FTBFS)

* Sat Jan 30 2016 Rex Dieter <rdieter@fedoraproject.org> 1.10-1
- taglib-1.10 (#1301895)

* Tue Aug 25 2015 Rex Dieter <rdieter@fedoraproject.org> 1.10-0.1.beta
- taglib-1.10beta

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.9.1-9
- Rebuilt for GCC 5 C++11 ABI change

* Sat Mar 21 2015 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-8
- gcc5 rebuild (#1204372)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Dan Horák <dan[at]danny.cz> 1.9.1-5
- big endian fixes (#1097109)

* Tue May 06 2014 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-4
- enable tests (#1094759)

* Fri Apr 25 2014 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-3
- License: GPLv2 or MPLv1.1 (#1091089)

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-2
- backport fixes for ABI breakage (wrt taglib-1.8) (#1026080, #1027164)

* Tue Oct 08 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-1
- taglib-1.9.1

* Tue Oct 08 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9-2
- License: +MPL

* Sun Oct 06 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9-1
- taglib-1.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-6.20130218git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Rex Dieter <rdieter@fedoraproject.org> 1.8-5.20130218git
- 20120218git snapshot

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-4.20121215git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8-3.20121215git
- 20121215git snapshot
- .spec cleanup

* Thu Sep 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8-2
- taglib.h: fix TAGLIB_MINOR_VERSION

* Thu Sep 06 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8-1
- taglib-1.8
-* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-2
-- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.2-1
- taglib-1.7.2

* Mon Mar 19 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.1-1
- taglib-1.7.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4
- Rebuilt for c++ ABI breakage

* Sat Feb 04 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.7-3
- Backported fix for a crash in .ape file parsing RHBZ#700727

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1.7-1
- taglib-1.7 (final)

* Sat Feb 19 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.7-0.1.rc1
- taglib-1.7rc1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 20 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.6.3-1
- taglib-1.6.3

* Mon Apr 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.6.2-3
- cosmetics, tighten %%files

* Mon Apr 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.6.2-2
- fix version in taglib-config, taglib.pc

* Fri Apr 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.6.2-1
- taglib-1.6.2

* Tue Jan 26 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-3
- Update with four post-1.6.1 fixes from 20100126
  (r1056922, r1062026, r1062426, r1078611).

* Fri Nov  6 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-2
- Update with two post-1.6.1 changes from 20091103.

* Sat Oct 31 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1 (bug-fixes, of which one is considered a fix for
  a serious bug: saving of Ogg FLAC comments).

* Thu Sep 17 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6-2
- Include the new NEWS file as %%doc.

* Mon Sep 14 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6-1
- Add patch to fix MP4 test on ppc/ppc64.
- Update to 1.6 final.

* Sun Sep  6 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6-0.1.rc1
- Update to 1.6rc1 (further bug-fixes and support for AIFF and WAV).
- Build optional support for MP4 and ASF/WMA files.

* Fri Sep  4 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.5-8
- Merge another bug-fix from 1.6rc1 (this adds 3 symbols) and
  really add tstring bug-fix:
  * Split Ogg packets larger than 64k into multiple pages. (BUG:171957)
  * Fixed a possible crash in the non-const version of String::operator[]
    and in String::operator+=. (BUG:169389)

* Sun Aug 23 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.5-7
- Build API documentation into -doc package.

* Sat Aug 22 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.5-6
- Add %%check section and conditionally build with tests.
- Update descriptions (and mention the additional file formats).
- Cherry-pick bug-fix patches from 1.6 development (also replaces the
  old taglib-1.5-kde#161721.patch):
  * Fixed crash when saving a Locator APEv2 tag. (BUG:169810)
  * TagLib can now use FLAC padding block. (BUG:107659)
  * Fixed overflow while calculating bitrate of FLAC files with a very
    high bitrate.
  * XiphComment::year() now falls back to YEAR if DATE doesn't exist
    and XiphComment::year() falls back to TRACKNUM if TRACKNUMBER doesn't
    exist. (BUG:144396)
  * Fixed a bug in ByteVectorList::split().
  * Fixed a possible crash in the non-const version of String::operator[]
    and in String::operator+=. (BUG:169389)
  * ID3v2.2 frames are now not incorrectly saved. (BUG:176373)
  * Support for ID3v2.2 PIC frames. (BUG:167786)
  * Improved ID3v2.3 genre parsing. (BUG:188578)
  * Better checking of corrupted ID3v2 APIC data. (BUG:168382)
  * Bitrate calculating using the Xing header now uses floating point
    numbers. (BUG:172556)
  * Added support for PRIV ID3v2 frames.
  * Empty ID3v2 genres are no longer treated as numeric ID3v1 genres.
  * Added support for the POPM (rating/playcount) ID3v2 frame.
  * Fixed crash on handling unsupported ID3v2 frames, e.g. on encrypted
    frames. (BUG:161721)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-3
- rebuild for pkgconfig deps

* Mon Oct 06 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-2
- Encrypted frames taglib/Amarok crash (kde#161721)

* Wed Feb 20 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-1
- taglib-1.5

* Wed Feb 13 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-0.9.rc1
- taglib-1.5rc1
- omit taglib-1.4_wchar.diff (for now)

* Mon Feb 04 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-0.8.b1
- taglib-1.5b1

* Wed Jan 16 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.7.20080116svn
- svn20080116 snapshot
- multiarch conflicts (#343241)

* Sun Nov 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.6.20071111svn
- svn20071111 snapshot (#376241)

* Thu Sep 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.5.20070924svn
- -BR: automake 
- +BR: zlib-devel

* Thu Sep 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.4.20070924svn
- use cmake, fixes "taglib_export.h not included" (#272361#c7)

* Mon Sep 24 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.5-0.3.20070924svn
- rebuild

* Mon Sep 24 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.5-0.2.20070924svn
- BR: automake

* Mon Sep 24 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.5-0.1.20070924svn
- update to svn version

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.4-6
- fix license tag
- rebuild for BuildID

* Thu Dec 14 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4-5
- add patch for multi-language support

* Thu Sep 14 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4-4
- have the devel package require pkgconfig (#206443)

* Thu Aug 31 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4-3
- rebuild

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-2
- rebuild for FC5

* Mon Aug 01 2005 Aurelien Bompard <gauret[AT]free.fr> 1.4-1
- version 1.4

* Fri Mar 25 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.3.1-2
- rebuild with g++4

* Mon Jan 10 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.3.1-1
- version 1.3.1
- drop patch0
- don't nuke every .la files, only the useless ones
- spec improvements thanks to Rex Dieter

* Thu Nov 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.3-0.fdr.2
- add apeitem.h to the include files in -devel

* Mon Oct 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.3-0.fdr.1
- version 1.3

* Sun Jun 06 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.5
- Changed license to LGPL
- include examples only in -devel
- remove Makefile* from examples
- remove *.la files

* Fri Jun 04 2004 Mihai Maties <mihai[AT]xcyb.org> 0:1.1-0.fdr.4
- included .la files as well
- compiled doc and included in -devel
- included examples in -devel

* Thu Jun 03 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.3
- provide the libtool files in the -devel subpackage
- include exemples in doc

* Thu Jun 03 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.2
- remove empty README
- add Requires(post,postun): /sbin/ldconfig
- remove --disable-static, it was useless anyway

* Tue Jun 01 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.1
- Fedora submission (shamelessly borrowed from Rex -- kde-redhat.sf.net)

* Sun Apr 04 2004 Rex Dieter <rexdieter at sf.net> 0:1.1-0.fdr.1
- 1.1

* Thu Feb 12 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.1
- fix for rh73

* Fri Feb 06 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.0
- first try
