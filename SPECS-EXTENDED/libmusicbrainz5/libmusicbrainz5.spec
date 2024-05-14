Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# Fedora package review: https://bugzilla.redhat.com/718395

Summary: Library for accessing MusicBrainz servers
Name: libmusicbrainz5
Version: 5.1.0
Release: 15%{?dist}
License: LGPLv2
URL: https://www.musicbrainz.org/
Source0: https://github.com/metabrainz/libmusicbrainz/releases/download/release-5.1.0/libmusicbrainz-%{version}.tar.gz
# Filed upstream as https://tickets.musicbrainz.org/browse/LMB-41
Patch0: doxygen.patch
Patch1: 0001-Don-t-emit-errors-unless-compiled-for-debug.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: pkgconfig(neon)
BuildRequires: pkgconfig(libxml-2.0)
Obsoletes: libmusicbrainz4 < 4.0.3-5

%description
The MusicBrainz client library allows applications to make metadata
lookup to a MusicBrainz server, generate signatures from WAV data and
create CD Index Disk ids from audio CD roms.

%package devel
Summary: Headers for developing programs that will use %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: libmusicbrainz4-devel < 4.0.3-5

%description devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.


%prep
%setup -q -n libmusicbrainz-%{version}
%patch 0 -p1 -b .doxygen
%patch 1 -p1 -b .silence-warnings

# omit "Generated on ..." timestamps that induce multilib conflicts
# this is *supposed* to be the doxygen default in fedora these days, but
# it seems there's still a bug or 2 there -- Rex
echo "HTML_TIMESTAMP      = NO" >> Doxyfile.cmake


%build
%{cmake} .

make %{?_smp_mflags} V=1
make %{?_smp_mflags} docs


%install

make install/fast DESTDIR=%{buildroot}

rm -f docs/installdox


%ldconfig_scriptlets


%files
%doc AUTHORS.txt COPYING.txt NEWS.txt README.md
%{_libdir}/libmusicbrainz5.so.1*

%files devel
%doc docs/*
%{_includedir}/musicbrainz5/
%{_libdir}/libmusicbrainz5.so
%{_libdir}/pkgconfig/libmusicbrainz5.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.1.0-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Christophe Fergeau <cfergeau@redhat.com> - 5.1.0-9
- Add upstream patch silencing some debug runtime warnings
  Resolves: rhbz#1450556

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Rex Dieter <rdieter@fedoraproject.org> 5.1.0-3
- rebuild (gcc5)

* Wed Feb 25 2015 Than Ngo <than@redhat.com> - 5.1.0-2
- rebuilt against new gcc5

* Sat Nov 15 2014 David King <amigadave@amigadave.com> 5.1.0-1
- Update to 5.1.0 (#1164434)
- Drop libxml2 patch (fixed upstream)
- Use pkgconfig for BuildRequires

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Christophe Fergeau <cfergeau@redhat.com> 5.0.1-10
- Fix documentation build with doxygen 1.8.7
  Resolves: rhbz#1106042

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Kalev Lember <kalevlember@gmail.com> - 5.0.1-7
- Fix the libmusicbrainz4 obsoletes version

* Tue Jun 11 2013 Christophe Fergeau <cfergeau@redhat.com> 5.0.1-6
- Obsoletes libmusicbrainz4, fixes rhbz#967322

* Wed Apr 03 2013 Christophe Fergeau <cfergeau@redhat.com> - 5.0.1-5
- Fix Patch1 which is causing rhbz#845846

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Tom Callaway <spot@fedoraproject.org> - 5.0.1-3
- remove non-free xmlParser.cpp

* Mon Aug 27 2012 Christophe Fergeau <cfergeau@redhat.com> - 5.0.1-2
- Address review comments (rhbz#832670)
    fix licence (LGPLv2+ -> LGPLv2)
    fix tarball URL
    remove obsolete use of RPM_BUILD_ROOT
    remove BuildRequires on pkg-config
    remove use of %%defattr

* Sat Jun 16 2012 Christophe Fergeau <cfergeau@redhat.com> - 5.0.1-1
- Package libmusicbrainz5, apart from the name/version it's identical to
  libmusicbrainz4 so this .spec is based on it.

* Wed May 16 2012 Christophe Fergeau <cfergeau@redhat.com> - 4.0.3-1
- New upstream 4.0.3 release, should fix a bug breaking metadata fetching
  from musicbrainz servers

* Fri Apr 20 2012 Christophe Fergeau <cfergeau@redhat.com> - 4.0.1-1
- New upstream 4.0.1 release, drop patch that has been merged upstream

* Sun Mar 04 2012 Christophe Fergeau <cfergeau@redhat.com> - 4.0.0-1
- First pass at a libmusicbrainz4 package, heavily based on the
  libmusicbrainz3 package

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Rex Dieter <rdieter@fedoraproject.rog> 3.0.3-2
- libmusicbrainz3-devel multilib conflict (#480378)
- drop extraneous pkgconfig dep baggage

* Mon Oct 18 2010 Bastien Nocera <bnocera@redhat.com> 3.0.3-1
- Update to 3.0.3 (#643789)

* Tue May 25 2010 Bastien Nocera <bnocera@redhat.com> 3.0.2-7
- Remove script from devel docs

* Tue Nov 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.0.2-7
- fix/enable unit tests

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.0.2-5
- fix doxygen-induced multilib conflicts (#480378)
- add %%check section (disabled by default, pending cppunit detection issues)

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.0.2-4
- work harder to omit extraneous pkgconfig deps
- gcc44 patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.2-2
- rebuild for pkgconfig deps

* Tue Sep 16 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.2-1
- libmusicbrainz3-3.0.2

* Fri Sep 05 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-4
- Build docs (#461238)
- -devel: drop extraneous Requires

* Fri Jul 25 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-3
- fix recursive linking against libdiscid neon

* Thu Jul 24 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-2
- BR: libdiscid-devel
- -devel: Requires: libdiscid-devel neon-devel

* Mon Jun 16 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-1
- libmusicbrainz3-3.0.1

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 2.1.5-7
- Provides: libmusicbrainz2(-devel), prepare for libmusicbrainz3

* Fri Feb 22 2008 Rex Dieter <rdieter@fedoraproject.org> 2.1.5-6
- gcc43 patch (#434127)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.5-5
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.1.5-4
- specfile cosmetics

* Thu Nov 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 2.1.5-3
- use versioned Obsoletes
- drop (Build)Requires: libstdc++-devel
- License: LGPLv2+

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 2.1.5-2
- Rebuild for PPC toolchain bug

* Thu Jun 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.1.5-1
- Update to 2.1.5

* Mon Oct 23 2006 Matthias Clasen <mclasen@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-4.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 2.1.1-4
- rebuild for -devel deps

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.1.1-3
- apply .spec file cleanups from Matthias Saou (#172926)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-2.1
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Christopher Aillon <caillon@redhat.com> - 2.1.1-2
- Stop shipping the .a file in the main package

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 23 2005 John (J5) Palmieri <johnp@redhat.com> 2.1.1-1
- Update to upstream version 2.1.1
- Removed libmusicbrainz-2.0.2-missing-return.patch
- Removed libmusicbrainz-2.0.2-conf.patch

* Thu Mar 03 2005 John (J5) Palmieri <johnp@redhat.com> 2.0.2-14
- Add patch to fix percision cast error to compile correctly on s390x
 
* Thu Mar 03 2005 John (J5) Palmieri <johnp@redhat.com> 2.0.2-13
- rebuild with gcc 4.0

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 2.0.2-12
- Add libmusicbrainz-2.0.2-missing-return.patch (bug #137289)

* Thu Oct 07 2004 Colin Walters <walters@redhat.com> 2.0.2-11
- BuildRequire expat-devel

* Tue Sep 28 2004 Colin Walters <walters@redhat.com> 2.0.2-10
- Move .so symlink to -devel package

* Tue Aug 31 2004 Colin Walters <walters@redhat.com> 2.0.2-9
- Add ldconfig calls (bz #131281)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 18 2003 Brent Fox <bfox@redhat.com> 2.0.2-6
- add a BuildPreReq for libstdc++-devel and gcc-c++ (bug #106556)
- add a Requires for libstdc++-devel for libmusicbrainz-devel

* Mon Sep  1 2003 Bill Nottingham <notting@redhat.com>
- Obsoletes musicbrainz-devel too

* Mon Sep  1 2003 Jonathan Blandford <jrb@redhat.com>
- Obsoletes musicbrainz

* Fri Aug 22 2003 Bill Nottingham <notting@redhat.com> 2.0.2-5
- fix autoconf/libtool weirdness, remove exclusivearch

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-4
- add ExcludeArch for s390x (something is really broken)

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-3
- add ExcludeArch for ppc64

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-2
- add ExcludeArch for x86_64 for now

* Thu Aug 21 2003 Brent Fox <bfox@redhat.com> 
- Initial build.


