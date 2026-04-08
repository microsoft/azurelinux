# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: The Reliable Event Logging Protocol library
Name: librelp
Version: 1.11.0
Release: 7%{?dist}
License: GPL-3.0-or-later
URL: http://www.rsyslog.com/
Source0: http://download.rsyslog.com/%{name}/%{name}-%{version}.tar.gz
# https://github.com/rsyslog/librelp/pull/266
Patch0: 0001-tcp-avoid-deprecated-ENGINE_cleanup.patch

%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%package devel
Summary: Development files for the %{name} package
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: make
BuildRequires: gnutls-devel >= 1.4.0
BuildRequires: openssl-devel

%description devel
Librelp is an easy to use library for the RELP protocol. The
librelp-devel package contains the header files and libraries needed
to develop applications using librelp.

%prep
%autosetup -p1

%build
autoreconf -ivf
%configure --disable-static --enable-tls --enable-tls-openssl
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{_libdir}/*.la

%ldconfig_scriptlets

%files
%doc AUTHORS COPYING NEWS README doc/*html
%{_libdir}/librelp.so.*

%files devel
%{_includedir}/*
%{_libdir}/librelp.so
%{_libdir}/pkgconfig/relp.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 20 2023 Attila Lakatos <alakatos@redhat.com> - 1.11.0-1
- rebase to 1.11.0
  resolves: rhbz#2159703
- enable openssl

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 08 2021 Attila Lakatos <alakatos@redhat.com> - 1.10.0-1
- rebase to 1.10.0
  resolves: rhbz#1929153

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 18 2020 Attila Lakatos <alakatos@redhat.com> - 1.9.0-1
- rebase to 1.9.0
  resolves: rhbz#1883471

* Tue Sep 08 2020 Attila Lakatos <alakatos@redhat.com> - 1.7.0-1
- rebase to 1.7.0
  resolves: rhbz#1826269

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 03 2020 Jiri Vymazal <jvymazal@redhat.com> - 1.5.0-1
- rebase to 1.5.0
  resolves: rhbz#1790820

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Jiri Vymazal <jvymazal@redhat.com> - 1.4.0-1
- rebase to 1.4.0
  resolves: rhbz#1425638

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Radovan Sroka <rsroka@redhat.com> - 1.2.16-1
- rebase to 1.2.16

* Mon Mar 26 2018 Radovan Sroka <rsroka@redhat.com> - 1.2.15-1
- rebase to 1.2.15
- fixed CVE-2018-1000140

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 02 2017 Radovan Sroka <rsroka@redhat.com> - 1.2.14-1
- rebase to 1.2.14

* Thu Feb 23 2017 Jiri Vymazal <jvymazal@redhat.com> - 1.2.13-1
- rebase to 1.2.13
  resolves: rhbz#1425638
- added patch for GnuTLS crypto-policy adherence
  resolves: rhbz#1179317
- added autoconf, automake and libtool because package
  has patches now

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 27 2016 Radovan Sroka <rsroka@redhat.com> 1.2.12-1
- rebase to 1.2.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Tomas Heinrich <theinric@redhat.com> - 1.2.7-1
- rebase to 1.2.7

* Thu Mar 27 2014 François Cami <fcami@fedoraproject.org> - 1.2.5-1
- rebase to 1.2.5

* Wed Jul 31 2013 Tomas Heinrich <theinric@redhat.com> - 1.2.0-1
- rebase to 1.2.0
- add gnutls-devel to BuildRequires

* Wed Apr 10 2013 Tomas Heinrich <theinric@redhat.com> - 1.0.3-1
- rebase to 1.0.3

* Thu Apr 04 2013 Tomas Heinrich <theinric@redhat.com> - 1.0.2-1
- rebase to 1.0.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Tomas Heinrich <theinric@redhat.com> - 1.0.1-1
- upgrade to upstream version 1.0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 15 2010 Tomas Heinrich <theinric@redhat.com> - 1.0.0-1
- upgrade to upstream version 1.0.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May  7 2008 Tomas Heinrich <theinric@redhat.com> 0.1.1-2
- removed "BuildRequires: autoconf automake"

* Tue Apr 29 2008 Tomas Heinrich <theinric@redhat.com> 0.1.1-1
- initial build
