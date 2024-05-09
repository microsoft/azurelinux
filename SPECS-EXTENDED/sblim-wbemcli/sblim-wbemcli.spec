Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           sblim-wbemcli
Version:        1.6.3
Release:        18%{?dist}
Summary:        SBLIM WBEM Command Line Interface

License:        EPL-1.0
URL:            https://sourceforge.net/projects/sblim/
Source0:        https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
Patch0:         sblim-wbemcli-1.5.1-gcc43.patch
Patch1:         sblim-wbemcli-1.6.2-https-segfaults.patch
Patch2:         sblim-wbemcli-1.6.1-ssl-proto-option.patch
Patch3:         sblim-wbemcli-1.6.3-fix-exit-status.patch
Patch4:         sblim-wbemcli-1.6.3-covscan-fixes.patch

BuildRequires:  curl-devel >= 7.9.3
BuildRequires:  binutils-devel >= 2.17.50.0.3-4
BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  gcc-c++
Requires:       curl >= 7.9.3

%description
WBEM Command Line Interface is a standalone, command line WBEM client. It is
specially suited for basic systems management tasks as it can be used in
scripts.

%prep
%setup -q
autoreconf --install --force
%patch 0 -p1 -b .gcc43
%patch 1 -p1 -b .https-segfaults
%patch 2 -p1 -b .ssl-proto-option
%patch 3 -p1 -b .fix-exit-status
%patch 4 -p1 -b .covscan-fixes

%build
%configure CACERT=/etc/pki/Pegasus/client.pem
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}

%files
%license COPYING
%{_bindir}/wbem*
%{_mandir}/man1/*
%{_datadir}/%{name}

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.3-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 27 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.3-16
- Fix exit status (i. e. apply https://sourceforge.net/p/sblim/bugs/2761/)
- Fix issues found by static analysis

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.3-14
- Fix URL
- Use correct short name for Eclipse Public License 1.0
- Use %%license

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.3-11
- Add BuildRequires gcc-c++
- Remove Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 17 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.3-6
- Update default CA certificate file path due to recent changes in tog-pegasus
  Related: #1308809

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 10 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.3-4
- Backport configurable SSL version feature from upstream and update man
  page accordingly

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.6.3-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Oct 15 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.3-1
- Update to sblim-wbemcli-1.6.3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-11
- Use upstream accepted patch for fixing wbemcli issue with dot character

* Tue Feb 18 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-10
- Support aarch64
  Resolves: #926488

* Thu Jan 30 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-9
- Fix wbemcli doesn't accept dot (.) as password character on command line
  Resolves: #959885
- Fix bogus date in the %%changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-7
- Fix wrong usage of libcurl API, which caused segfaults when wbemcli was used
  with https scheme (patch by kdudka@redhat.com)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 10 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-5
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for c++ ABI breakage

* Thu Jan 05 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-2
- Fix gcc47 compile failure

* Tue Jul 19 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.2-1
- Update to sblim-wbemcli-1.6.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.1-1
- Update to sblim-wbemcli-1.6.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Feb 28 2009 Caolán McNamara - 1.6.0-4
- constify rets of strchr(const char *);

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.0-2
- Fix License
- Spec file cleanup, rpmlint check

* Fri Oct 24 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.0-1
- Update to 1.6.0
  Resolves: #468328

* Fri Jun 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5.1-7
- fix gcc43 compile failure

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.1-6
- Autorebuild for GCC 4.3

* Mon Nov 06 2006 Jindrich Novy <jnovy@redhat.com> - 1.5.1-5
- rebuild against new curl

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 1.5.1-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Nov 21 2005 Viktor Mihajlovski <mihajlov@de.ibm.com> - 1.5.1-1
- Upgrade to version 1.5.1 (SSL V3 enforced, default CACERT).
- Created Fedora/RH specific spec file.

* Fri Oct 28 2005 Viktor Mihajlovski <mihajlov@de.ibm.com> - 1.5.0-1
- Minor enhancements for Fedora compatibility, still not daring to
  nuke the build root though

* Thu Jul 28 2005 Viktor Mihajlovski <mihajlov@de.ibm.com> - 1.5.0-0
- Updates for rpmlint complaints
