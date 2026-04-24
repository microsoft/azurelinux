# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global tarball libX11
#global gitdate 20130524
#global gitversion a3bdd2b09

Summary: Core X11 protocol client library
Name: libX11
Version: 1.8.12
Release: 4%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
License: MIT AND X11
URL: http://www.x.org

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0: https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.xz
%endif


Patch2: dont-forward-keycode-0.patch

BuildRequires: libtool
BuildRequires: make
BuildRequires: xorg-x11-util-macros >= 1.11
BuildRequires: pkgconfig(xproto) >= 7.0.15
BuildRequires: xorg-x11-xtrans-devel >= 1.0.3-4
BuildRequires: libxcb-devel >= 1.2
BuildRequires: pkgconfig(xau) pkgconfig(xdmcp)
BuildRequires: perl(Pod::Usage)

Requires: %{name}-common >= %{version}-%{release}

%description
Core X11 protocol client library.

%package common
Summary: Common data for libX11
BuildArch: noarch

%description common
libX11 common data

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-xcb = %{version}-%{release}

%description devel
X.Org X11 libX11 development package

%package xcb
Summary: XCB interop for libX11
Conflicts: %{name} < %{version}-%{release}

%description xcb
libX11/libxcb interoperability library

%prep
%autosetup -p1 -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install --force
%configure --disable-silent-rules --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# create/own compose cache dir
mkdir -p $RPM_BUILD_ROOT/var/cache/libX11/compose

# We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# FIXME: Don't install Xcms.txt - find out why upstream still ships this.
find $RPM_BUILD_ROOT -name 'Xcms.txt' -delete

# FIXME package these properly
rm -rf $RPM_BUILD_ROOT%{_docdir}

%check
make %{?_smp_mflags} check

%ldconfig_post
%ldconfig_postun

%files
%{_libdir}/libX11.so.6
%{_libdir}/libX11.so.6.4.0

%files xcb
%{_libdir}/libX11-xcb.so.1
%{_libdir}/libX11-xcb.so.1.0.0

%files common
%doc AUTHORS COPYING README.md
%{_datadir}/X11/locale/
%{_datadir}/X11/XErrorDB
%dir /var/cache/libX11
%dir /var/cache/libX11/compose

%files devel
%{_includedir}/X11/ImUtil.h
%{_includedir}/X11/XKBlib.h
%{_includedir}/X11/Xcms.h
%{_includedir}/X11/Xlib.h
%{_includedir}/X11/XlibConf.h
%{_includedir}/X11/Xlibint.h
%{_includedir}/X11/Xlib-xcb.h
%{_includedir}/X11/Xlocale.h
%{_includedir}/X11/Xregion.h
%{_includedir}/X11/Xresource.h
%{_includedir}/X11/Xutil.h
%{_includedir}/X11/cursorfont.h
%{_includedir}/X11/extensions/XKBgeom.h
%{_libdir}/libX11.so
%{_libdir}/libX11-xcb.so
%{_libdir}/pkgconfig/x11.pc
%{_libdir}/pkgconfig/x11-xcb.pc
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 22 2025 Peter Hutterer <peter.hutterer@redhat.com> - 1.8.12-2
- Rebuild to pick up latest xorg proto keysyms (#2413818)

* Thu Jul 24 2025 Olivier Fourdan <ofourdan@redhat.com> - 1.8.12-1
- libX11 1.8.12

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Feb 03 2025 José Expósito <jexposit@redhat.com> - 1.8.11-1
- libX11 1.8.11

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 22 2024 Florian Müllner <fmuellner@redhat.com> - 1.8.10-2
- Fix spurious Xerror when running synchronized

* Wed Jul 31 2024 José Expósito <jexposit@redhat.com> - 1.8.10-1
- libX11 1.8.10

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 08 2024 José Expósito <jexposit@redhat.com> - 1.8.9-1
- libX11 1.8.9

* Mon Apr 01 2024 José Expósito <jexposit@redhat.com> - 1.8.8-1
- libX11 1.8.8

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.8.7-1
- libX11 1.8.7
  - CVE-2023-43785 libX11: out-of-bounds memory access in _XkbReadKeySyms()
  - CVE-2023-43786 libX11: stack exhaustion from infinite recursion in
    PutSubImage()
  - CVE-2023-43787 libX11: integer overflow in XCreateImage() leading to
   a heap overflow
  - CVE-2023-43788 libXpm: out of bounds read in XpmCreateXpmImageFromBuffer()
  - CVE-2023-43789 libXpm: out of bounds read on XPM with corrupted colormap

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com> - 1.8.6-3
- SPDX Migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.8.6-1
- libX11 1.8.6 (CVE-2023-3138)

* Mon Jun 05 2023 Peter Hutterer <peter.hutterer@redhat.com> 1.8.5-1
- libX11 1.8.5

* Wed Feb 08 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.8.4-1
- libX11 1.8.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.8.3-2
- Fix XPutBackEvent() issues (#2161020)

* Fri Jan 06 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.8.3-1
- libX11 1.8.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.8.1-1
- libX11 1.8.1

* Mon Apr 04 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.5-1
- libX11 1.7.5

* Thu Mar 31 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.4-1
- libX11 1.7.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.3.1-1
- libX11 1.7.3.1

* Tue Dec 07 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.3-1
- libX11 1.7.3
- manually add ax_gcc_builtin, it's missing from the tarball

* Tue Jul 27 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.2-3
- Parse the new _EVDEVK symbols

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 09 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.7.2-1
- libX11 1.7.2

* Tue May 18 2021 Adam Jackson <ajax@redhat.com> - 1.7.1-1
- libX11 1.7.1 (CVE-2021-31535)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.7.0-2
- libX11 1.7.0 (with the tarball this time)

* Tue Dec 01 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.7.0-1
- libX11 1.7.0
- switch to using the autosetup rpm macro

* Mon Nov 09 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.6.12-3
- Fix a race-condition in poll_for_response (#1758384)

* Thu Nov  5 11:12:56 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.12-2
- Add BuildRequires for make

* Wed Aug 26 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.6.12-1
- libX11 1.6.12 (CVE-2020-14363, CVE 2020-14344)

* Fri Jul 31 2020 Adam Jackson <ajax@redhat.com> - 1.6.9-5
- Fix server reply validation issue in XIM (CVE 2020-14344)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.6.9-2
- handle ssharp in XConvertCase

* Wed Oct 09 2019 Adam Jackson <ajax@redhat.com> - 1.6.9-1
- libX11 1.6.9

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 20 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.6.8-2
- rebuild to pick up the new xorgproto keysyms

* Thu Jun 20 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.6.8-1
- libX11 1.6.8

* Thu Mar 21 2019 Adam Jackson <ajax@redhat.com> - 1.6.7-3
- Rebuild for xtrans 1.4.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 09 2018 Adam Jackson <ajax@redhat.com> - 1.6.7-1
- libX11 1.6.7

* Tue Aug 21 2018 Adam Jackson <ajax@redhat.com> - 1.6.6-1
- libX11 1.6.6

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 1.6.5-8
- Use ldconfig scriptlet macros

* Fri Mar 23 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.6.5-7
- Fix FTBS caused by fake size in the XimCacheStruct (#1556616)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 17 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.5-5
- run make check as part of the build (#1502658)

* Tue Aug 01 2017 Adam Jackson <ajax@redhat.com> - 1.6.5-4
- Split libX11-xcb to its own subpackage. This doesn't have much effect at
  the moment because x11-xcb.pc still lists both libX11 and libxcb in
  Requires, but once that's fixed eg. libEGL should be able to be installed
  without libX11.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Hans de Goede <hdegoede@redhat.com> - 1.6.5-2
- Rebuild against new xproto to pick up support for new keysyms

* Wed Apr 26 2017 Adam Jackson <ajax@redhat.com> - 1.6.5-1
- libX11 1.6.5

* Thu Feb 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.6.4-6
- create/own /var/cache/libx11/compose (#962764)
- %%build: --disable-silent-rules

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.4-4
- Actually apply the patch from 1.6.4-3

* Mon Jan 09 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.4-3
- Fix a bug in the memory leak fix from 1.6.4-2

* Thu Jan 05 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.4-2
- Plug a memory leak in XListFonts()

* Wed Oct 05 2016 Adam Jackson <ajax@redhat.com> - 1.6.4-1
- libX11 1.6.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Peter Hutterer <peter.hutterer@redhat.com>
- Remove unnecessary defattr

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 1.6.3-1
- libX11 1.6.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Adam Jackson <ajax@redhat.com> 1.6.2-1
- libX11 1.6.2 plus a fix for interleaved xcb/xlib usage
- Use >= for the -common Requires

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jul 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.6.1-1
- libX11 1.6.1

* Tue Jun 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-1
- libX11 1.6.0
