# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}

Name:           sblim-testsuite
Version:        1.3.0
Release:        34%{?dist}
Summary:        SBLIM testsuite

License:        EPL-1.0
URL:            http://sblim.wiki.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
BuildArch:      noarch
BuildRequires: make
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
%autopatch -p1

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
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 29 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.0-29
- SPDX migration

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
