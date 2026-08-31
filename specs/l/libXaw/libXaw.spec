# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary: X Athena Widget Set
Name: libXaw
Version: 1.0.16
Release: 4%{?dist}
License: MIT-open-group AND X11 AND HPND AND HPND-sell-variant AND SMLNJ AND NTP
URL: http://www.x.org

Source0: https://www.x.org/pub/individual/lib/%{name}-%{version}.tar.xz

BuildRequires: make
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(xproto) pkgconfig(x11) pkgconfig(xt)
BuildRequires: pkgconfig(xmu) pkgconfig(xpm) pkgconfig(xext)
BuildRequires: xorg-x11-util-macros xmlto lynx

%description
Xaw is a widget set based on the X Toolkit Intrinsics (Xt) Library.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: pkgconfig(xproto) pkgconfig(xmu) pkgconfig(xt) pkgconfig(xpm)

%description devel
X.Org X11 libXaw development package

%prep
%setup -q

%build
autoreconf -v --install --force
export CFLAGS="$RPM_OPT_FLAGS -Os"
%configure \
	    --docdir=%{_pkgdocdir} \
	    --disable-xaw8 --disable-static \
	    --disable-xaw6 \
	    --without-fop --without-xmlto
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
install -pm 644 COPYING README.md ChangeLog $RPM_BUILD_ROOT%{_pkgdocdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_post
%ldconfig_postun

%files
%dir %{_pkgdocdir}
%{_pkgdocdir}/ChangeLog
%{_pkgdocdir}/COPYING
%{_pkgdocdir}/README.md
%{_libdir}/libXaw.so.7
%{_libdir}/libXaw7.so.7
%{_libdir}/libXaw7.so.7.0.0

%files devel
%dir %{_includedir}/X11/Xaw
%{_includedir}/X11/Xaw/*.h
# FIXME:  Is this C file really supposed to be here?
%{_includedir}/X11/Xaw/Template.c
%{_libdir}/libXaw.so
%{_libdir}/libXaw7.so
%{_libdir}/pkgconfig/xaw7.pc
%{_mandir}/man3/*.3*
%{_pkgdocdir}/*.xml
#{_pkgdocdir}/%{name}.html
#{_pkgdocdir}/%{name}.txt

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 13 2024 José Expósito <jexposit@redhat.com> - 1.0.16-1
- libXaw 1.0.16

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 José Expósito <jexposit@redhat.com> - 1.0.15-1
- libXaw 1.0.15

* Wed Sep 06 2023 Benjamin Tissoires <benjamin.tissoires@redhat.com> - 1.0.14-6
- SPDX migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 21 2021 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.0.14-1
- libXaw 1.0.14

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 11:13:57 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.13-16
- Add BuildRequires for make

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 1.0.13-10
- Drop useless %%defattr

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 1.0.13-9
- Use ldconfig scriptlet macros

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 25 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.0.13-4
- Force disable documentation generation

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Adam Jackson <ajax@redhat.com> 1.0.13-1
- libXaw 1.0.13

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Jaromir Capik <jcapik@redhat.com> - 1.0.12-2
- Fixing format-security flaws (#1037174)

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 1.0.12-1
- libXaw 1.0.12
- Drop pre-F18 changelog

* Sat Nov  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.0.11-7
- Install docs to %%{_pkgdocdir} where available (#993836).
- Fix bogus date in %%changelog.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.0.11-5
- Drop ed from BR, see upstream 0b6058db1ce

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.11-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Adam Jackson <ajax@redhat.com> 1.0.11-1
- libXaw 1.0.11
