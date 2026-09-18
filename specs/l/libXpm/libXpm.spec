# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: X.Org X11 libXpm runtime library
Name: libXpm
Version: 3.5.17
Release: 6%{?dist}
License: MIT AND X11-distribute-modifications-variant
URL: http://www.x.org

Source0: https://www.x.org/pub/individual/lib/%{name}-%{version}.tar.xz

BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool make
BuildRequires: gettext
BuildRequires: pkgconfig(xext) pkgconfig(xt) pkgconfig(xau)
BuildRequires: ncompress gzip

%description
X.Org X11 libXpm runtime library

%package devel
Summary: X.Org X11 libXpm development package
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXpm development package

%prep
%setup -q

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_post
%ldconfig_postun

%files
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libXpm.so.4
%{_libdir}/libXpm.so.4.11.0

%files devel
%{_bindir}/cxpm
%{_bindir}/sxpm
%{_includedir}/X11/xpm.h
%{_libdir}/libXpm.so
%{_libdir}/pkgconfig/xpm.pc
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 Peter Hutterer <peter.hutterer@redhat.com> - 3.5.17-1
- libXpm 3.5.17

* Wed Sep 06 2023 Benjamin Tissoires <benjamin.tissoires@redhat.com> - 3.5.15-5
- SPDX migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Peter Hutterer <peter.hutterer@redhat.com> - 3.5.15-2
- Add missing BuildRequires

* Wed Jan 18 2023 Peter Hutterer <peter.hutterer@redhat.com> - 3.5.15-1
- libXpm 3.5.15, fixes CVE-2022-46285, CVE-2022-44617, CVE-2022-4883

* Wed Jan 11 2023 Peter Hutterer <peter.hutterer@redhat.com> - 3.5.14-1
- libXpm 3.5.14

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Peter Hutterer <peter.hutterer@redhat.com> 3.5.13-4
- Add make to BuildRequires

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 13 2019 Peter Hutterer <peter.hutterer@redhat.com> 3.5.13-1
- libXpm 3.5.13

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 3.5.12-7
- Drop useless %%defattr

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 3.5.12-6
- Use ldconfig scriptlet macros

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 3.5.12-1
- libXpm 3.5.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 3.5.11-1
- libXpm 3.5.11
- Drop pre-F18 changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 3.5.10-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 3.5.10-1
- libXpm 3.5.10
