Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global debug_package %{nil}

Name:           sblim-testsuite
Version:        1.3.0
Release:        23%{?dist}
Summary:        SBLIM testsuite

License:        EPL
URL:            https://sblim.wiki.sourceforge.net/
Source0:        https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
BuildArch:      noarch
BuildRequires:      perl-generators

Requires:       perl-interpreter >= 5.6
Requires:       sblim-wbemcli >= 1.5

Patch0:         sblim-testsuite-1.3.0-perl-errors.patch
# Patch1: removes version from docdir
Patch1:         sblim-testsuite-1.3.0-docdir.patch
# Patch2: fixes unescaped left brace perl warning
Patch2:         sblim-testsuite-1.3.0-unescaped-left-brace-warning-fix.patch

%description
SBLIM automated testsuite scripts.

%prep
%setup -q
%patch 0 -p1 -b .perl-errors
%patch 1 -p1 -b .docdir
%patch 2 -p1 -b .unescaped-left-brace-warning-fix

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING README
%{_datadir}/%{name}
%{_localstatedir}/lib/%{name}

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.3.0-16
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 26 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-14
- Fix unescaped left brace perl warning

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 28 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-10
- Fix for unversioned docdir change
  Resolves: #994088
- Fix bogus date in %%changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.3.0-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 10 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-6
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 09 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-3
- Fix perl errors

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-1
- Update to sblim-testsuite-1.3.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.5-2
- Remove debug package, fix URL, make setup quiet
- Spec file cleanup, rpmlint check

* Fri Oct 24 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.5-1
- Update to 1.2.5
  Resolves: #468327

* Fri Oct 28 2005 Viktor Mihajlovski <mihajlov@de.ibm.com> - 1.2.4-1
- New release

* Thu Jul 28 2005 Viktor Mihajlovski <mihajlov@de.ibm.com> - 1.2.3-0
- Updates for rpmlint complaints
