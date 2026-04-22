# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# TODO: libXmuu split and/or elf filter emulation

Summary: X.Org X11 libXmu/libXmuu runtime libraries
Name: libXmu
Version: 1.2.1
Release: 5%{?dist}
License: MIT-open-group AND SMLNJ AND X11 AND ISC
URL: http://www.x.org

Source0: https://www.x.org/pub/individual/lib/%{name}-%{version}.tar.xz

BuildRequires: make
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-util-macros
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: xmlto

%description
X.Org X11 libXmu/libXmuu runtime libraries

%package devel
Summary: X.Org X11 libXmu development package
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXmu development package

%prep
%setup -q

%build
autoreconf -v --install --force
%configure --disable-static
make  %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# fixup later
rm -rf $RPM_BUILD_ROOT%{_docdir}

%ldconfig_post
%ldconfig_postun

%files
%doc COPYING README.md ChangeLog
%{_libdir}/libXmu.so.6
%{_libdir}/libXmu.so.6.2.0
%{_libdir}/libXmuu.so.1
%{_libdir}/libXmuu.so.1.0.0

%files devel
%dir %{_includedir}/X11/Xmu
%{_includedir}/X11/Xmu/Atoms.h
%{_includedir}/X11/Xmu/CharSet.h
%{_includedir}/X11/Xmu/CloseHook.h
%{_includedir}/X11/Xmu/Converters.h
%{_includedir}/X11/Xmu/CurUtil.h
%{_includedir}/X11/Xmu/CvtCache.h
%{_includedir}/X11/Xmu/DisplayQue.h
%{_includedir}/X11/Xmu/Drawing.h
%{_includedir}/X11/Xmu/Editres.h
%{_includedir}/X11/Xmu/EditresP.h
%{_includedir}/X11/Xmu/Error.h
%{_includedir}/X11/Xmu/ExtAgent.h
%{_includedir}/X11/Xmu/Initer.h
%{_includedir}/X11/Xmu/Lookup.h
%{_includedir}/X11/Xmu/Misc.h
%{_includedir}/X11/Xmu/StdCmap.h
%{_includedir}/X11/Xmu/StdSel.h
%{_includedir}/X11/Xmu/SysUtil.h
%{_includedir}/X11/Xmu/WhitePoint.h
%{_includedir}/X11/Xmu/WidgetNode.h
%{_includedir}/X11/Xmu/WinUtil.h
%{_includedir}/X11/Xmu/Xct.h
%{_includedir}/X11/Xmu/Xmu.h
%{_libdir}/libXmu.so
%{_libdir}/libXmuu.so
%{_libdir}/pkgconfig/xmu.pc
%{_libdir}/pkgconfig/xmuu.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 17 2024 José Expósito <jexposit@redhat.com> - 1.2.1-1
- libXmu 1.2.1

* Mon Apr 01 2024 José Expósito <jexposit@redhat.com> - 1.2.0-1
- libXmu 1.2.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 06 2023 Benjamin Tissoires <benjamin.tissoires@redhat.com> - 1.1.4-4
- SPDX migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.1.4-1
- libXmu 1.1.4-1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 12:15:32 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.3-5
- Add BuildRequires for make

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Adam Jackson <ajax@redhat.com> - 1.1.3-1
- libXmu 1.1.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 14 2018 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.1.2-12
- Add upstream fixes detected by covscan

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 1.1.2-10
- Drop useless %%defattr

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 1.1.2-9
- Use ldconfig scriptlet macros

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.1.2-1
- libXmu 1.1.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.1-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Adam Jackson <ajax@redhat.com> 1.1.1-1
- libXmu 1.1.1
