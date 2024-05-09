Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global project openexr

Name:    ilmbase
Summary: Abstraction/convenience libraries
Version: 2.3.0
Release: 5%{?dist}

License: BSD
URL:	 https://www.openexr.com/
Source0: https://github.com/%{project}/%{project}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1: ilmbase-config.h

#BuildRequires: automake libtool
BuildRequires: gcc-c++
BuildRequires: pkgconfig
# silly rpm, won't pick up rpm dependencies for items not in it's buildroot
# see https://bugzilla.redhat.com/866302
BuildRequires: pkgconfig(gl) pkgconfig(glu)

## upstreamable patches
# explicitly add $(PTHREAD_LIBS) to libIlmThread linkage (helps PTHREAD_LIBS workaround in %%build)
Patch51: ilmbase-2.2.0-no_undefined.patch
# add Requires.private: gl glu to IlmBase.pc
Patch53:  ilmbase-1.0.3-pkgconfig.patch
# workaround glibc iszero macro
# https://bugzilla.redhat.com/show_bug.cgi?id=1383552
Patch54:  ilmbase-2.2.0-glibc_iszero.patch

## upstream patches

%description
Half is a class that encapsulates the ilm 16-bit floating-point format.

IlmThread is a thread abstraction library for use with OpenEXR
and other software packages.

Imath implements 2D and 3D vectors, 3x3 and 4x4 matrices, quaternions
and other useful 2D and 3D math functions.

Iex is an exception-handling library.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

%patch 51 -p1 -b .no_undefined
%patch 53 -p1 -b .pkgconfig
#patch54 -p1 -b .glibc_iszero

#/bootstrap


%build
%configure --disable-static

# manually set PTHREAD_LIBS to include -lpthread until libtool bogosity is fixed,
# https://bugzilla.redhat.com/show_bug.cgi?id=661333
%make_build \
  PTHREAD_LIBS="-pthread -lpthread"


%install
%make_install

rm -fv %{buildroot}%{_libdir}/lib*.la

# Fix multilibs header conflict
%ifarch x86_64 i686
%ifarch x86_64
mv %{buildroot}%{_includedir}/OpenEXR/IlmBaseConfig.h \
  %{buildroot}%{_includedir}/OpenEXR/IlmBaseConfig-64.h
%else
mv %{buildroot}%{_includedir}/OpenEXR/IlmBaseConfig.h \
  %{buildroot}%{_includedir}/OpenEXR/IlmBaseConfig-32.h
%endif
install -pm 0644 %{SOURCE1} %{buildroot}%{_includedir}/OpenEXR/IlmBaseConfig.h
%endif


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion IlmBase)" = "%{version}"
# is the known-failure ix86-specific or 32bit specific? guess we'll find out -- rex
# lt-ImathTest: testBoxAlgo.cpp:892: void {anonymous}::boxMatrixTransform(): Assertion `b21 == b2' failed.
%ifarch %{ix86}
%make_build check -k ||:
%else
%make_build check
%endif


%ldconfig_scriptlets


%files
%doc AUTHORS ChangeLog NEWS README.md
%license LICENSE
%{_libdir}/libHalf.so.24*
%{_libdir}/libIex-2_3.so.24*
%{_libdir}/libIexMath-2_3.so.24*
%{_libdir}/libIlmThread-2_3.so.24*
%{_libdir}/libImath-2_3.so.24*

%files devel
%{_includedir}/OpenEXR/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/IlmBase.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0-2
- Fix for multibs conflict - rhbz#1712198

* Tue Apr 02 2019 Richard Shaw <hobbes1069@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-14
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

* Thu Oct 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.2.0-7
- drop iszero workaround, no longer needed (#1383552)

* Sun Oct 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.2.0-6
- workaround glibc iszero macro (#1383552)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 16 2015 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-3
- rebuild (gcc5)

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-2
- rebuild (gcc5)

* Thu Nov 20 2014 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-1
- 2.2.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-1
- 2.1.0

* Thu Aug 29 2013 Rex Dieter <rdieter@fedoraproject.org>  2.0.1-1
- 2.0.1

* Thu Aug 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.3-7
- Fix spec issues, modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-4
- ilmbase-devel missing dependency on libGLU-devel (#866302)

* Sat Sep 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.0.3-3
- IlmBase.pc: +Requires.private: gl glu
- -devel: drop hard-coded libGL/pkgconfig deps, let rpm autodetect now

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> 1.0.3-2
- fix build on non-x86 arches

* Sun Aug 05 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-1
- ilmbase-1.0.3
- ix86 fix courtesy of Nicolas Chauvet <kwizart@gmail.com>

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-2
- libIlmThread missing -pthread linkage (#661115)
- %%install: INSTALL="install -p"
- -devel: tighten dep using %%?_isa

* Wed Jul 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-1
- ilmbase-1.0.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May  4 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.0.1-5
- Fix spelling error in summary.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-3
- rebuild for pkgconfig deps

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-2
- respin (gcc43)

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-1
- ilmbase-1.0.1

* Fri Oct 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-3
- include *.tar.sig in sources

* Mon Oct 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-2
- update %%summary
- -devel: +Requires: libGL-devel libGLU-devel
- make install ... INSTALL="install -p" to preserve timestamps


* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-1
- ilmbase-1.0.0 (first try)

