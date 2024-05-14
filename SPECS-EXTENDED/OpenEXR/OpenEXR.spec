Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global project openexr

Name:	 OpenEXR
Summary: A high dynamic-range (HDR) image file format
Version: 2.3.0
Release: 6%{?dist}

License: BSD
URL:	 https://www.openexr.com/
Source0: https://github.com/%{project}/%{project}/releases/download/v%{version}/%{name}-%{version}.tar.gz

# fix tests for big endian arches
# https://github.com/openexr/openexr/issues/81
# https://github.com/openexr/openexr/commit/5350d10ffc03c774e5cd574062297fc91001064d
# https://github.com/openexr/openexr/commit/225ddb8777e75978b88c2d6311bb0cf94c0b6f22
Patch0:  openexr-2.3.0-bigendian.patch
# https://github.com/openexr/openexr/issues/377
# https://github.com/openexr/openexr/pull/443
Patch1: openexr-2.3.0-tests.patch

Obsoletes: openexr < %{version}-%{release}
Provides:  openexr = %{version}-%{release}

# https://github.com/openexr/openexr/issues/130
BuildConflicts: OpenEXR-devel < 2.2.0

BuildRequires: gcc-c++
BuildRequires: ilmbase-devel >= %{version}
BuildRequires: zlib-devel
BuildRequires: pkgconfig

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial
Light & Magic for use in computer imaging applications. This package contains
libraries and sample applications for handling the format.

%package devel
Summary: Headers and libraries for building apps that use %{name}
Obsoletes: openexr-devel < %{version}-%{release}
Provides:  openexr-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ilmbase-devel%{?_isa}
%description devel
%{summary}.

%package libs
Summary: %{name} runtime libraries
%description libs
%{summary}.

%package doc
Summary: Documentation and examples for building app that use %{name}

%description doc
%{summary}.


%prep
%setup -q -n openexr-%{version}
%patch 0 -p2 -b .bigendian
%patch 1 -p2 -b .tests


%build
%configure --disable-static

# hack to omit unused-direct-shlib-dependencies
#sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build


%install
%make_install

#unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}

# Move documentation to use the same name as the package.
mv %{buildroot}%{_docdir}/openexr %{buildroot}%{_docdir}/%{name}


%check
export PKG_CONFIG_PATH="%{buildroot}%{_libdir}/pkgconfig${PKG_CONFIG_PATH:+:}${PKG_CONFIG_PATH}"
test "$(pkg-config --modversion OpenEXR)" = "%{version}"
make %{?_smp_mflags} check || { cat IlmImfTest/test-suite.log; /bin/true; }


%files
%{_bindir}/exr*

%ldconfig_scriptlets libs

%files libs
%doc AUTHORS ChangeLog NEWS IlmImfUtil/README
%license LICENSE
%{_libdir}/libIlmImf-2_3.so.24*
%{_libdir}/libIlmImfUtil-2_3.so.24*

%files devel
#omit for now, they're mostly useless, and include multilib conflicts (#342781)
#doc rpmdocs/examples
%{_datadir}/aclocal/openexr.m4
%{_includedir}/OpenEXR/*
%{_libdir}/libIlmImf*.so
%{_libdir}/pkgconfig/OpenEXR.pc

%files doc
%{_docdir}/%{name}/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.0-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Dan Horák <dan[at]danny.cz> - 2.3.2-3
- fix some tests

* Sat Jul 13 2019 Dan Horák <dan[at]danny.cz> - 2.3.2-2
- switch to upstream fix for big endians

* Tue Apr 02 2019 Richard Shaw <hobbes1069@gmail.com> - 2.3.0-1
- Update to 2.3.0.
- Move large documentation to a doc subpackage.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct  1 2018 Owen Taylor <otaylor@redhat.com> - 2.2.0-15
- In %%check, augment PKG_CONFIG_PATH, not replace it

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.2.0-13
- use %%make_build %%make_install %%ldconfig_scriptlets %%license

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.2.0-12
- BR: gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 12 2016 Björn Esser <fedora@besser82.io> - 2.2.0-7
- rebuild (GCC 6.2)
- whitespace clean-up

* Tue Oct 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.2.0-6
- -devel: make ilmbase-devel dep arch'd

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 16 2015 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-3
- rebuild (gcc5)

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-2
- rebuild (gcc5)

* Thu Nov 20 2014 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-1
- 2.2.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 31 2014 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-3
- respin headers patch (to match upstream fix)

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-2
- install ImfDeepImageStateAttribute.h header too

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-1
- 2.1.0

* Wed Nov 20 2013 Dan Horák <dan[at]danny.cz>  2.0.1-3
- remove testing residue from optflags

* Wed Nov 20 2013 Dan Horák <dan[at]danny.cz>  2.0.1-2
- fix tests for big endian arches

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org>  2.0.1-1
- openexr-2.0.1

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.7.1-5
- Back to upstream ABI (f19+, el7+)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.7.1-3
- Bump to hide revertion

* Fri Aug 31 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.1-2
- rebuild

* Thu Aug 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.7.1-1
- Update to 1.7.1

-* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-5
-- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-4
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 Rex Dieter <rdieter@fedoraproject.org> 1.7.0-1
- openexr-1.7.0

* Wed Jul 29 2009 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-8
- CVE-2009-1720 OpenEXR: Multiple integer overflows (#513995)
- CVE-2009-1721 OpenEXR: Invalid pointer free by image decompression (#514003)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Caolán McNamara <caolanm@redhat.com> 1.6.1-5
- rebuild to get provides pkgconfig(OpenEXR)

* Fri May 09 2008 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-4
- drop: Obsoletes: OpenEXR-utils (see OpenEXR_Viewers review, bug #428228c3)

* Fri Feb 01 2008 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-3
- gcc43 patch
- purge rpaths

* Wed Jan 09 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.1-2
- hack to omit unused-direct-shlib-dependencies
- conditionalize -libs (f8+)

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.1-1
- openexr-1.6.1

* Tue Oct 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-5
- multiarch conflicts in OpenEXR (#342781)
- don't own %%_includedir/OpenEXR (leave that to ilmbase)

* Mon Oct 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-4
- -libs: %%post/%%postun -p /sbin/ldconfig

* Fri Oct 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-2
- openexr-1.6.0

* Mon Sep 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.0a-6
- libs: -Requires: %%name

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.0a-5
- -libs: new subpkg to be multilib friendly
- -utils: package exrdisplay separately (separate fltk dep)

* Sat Oct 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-4
- Obsoletes/Provides: openexr(-devel) (rpmforge compatibility)

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-3
- pkgconfig patch to use Libs.private

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-2
- -devel: +Requires: pkgconfig

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-1
- openexr-1.4.0a

* Sat Feb 18 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-7
- Further zlib fixes (#165729)

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-6
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-5
- Remove *.a from %%files devel

* Tue Aug 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-4
- Removed -devel dep on zlib-devel (#165729)
- Added --disable-static to %%configure
- Fixed build with GCC 4.0.1
- Added .so links to -devel

* Wed May 18 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-3
- Add zlib-devel to BR
- Delete all .la files (#157652)

* Mon May  9 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Add disttag

* Sun May  8 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Fix BuildRequires
- Fix Requires on -devel
- Add %%post[un] scriptlets
- Fix ownership in -devel
- Don't have .deps files in %%doc

* Wed Mar 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-1
- Initial RPM release
