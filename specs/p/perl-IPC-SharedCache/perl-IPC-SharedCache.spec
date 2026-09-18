# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-IPC-SharedCache
Version:        1.3
Release:        57%{?dist}
Summary:        Perl module to manage a cache in SysV IPC shared memory
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://metacpan.org/release/IPC-SharedCache
Source0:        https://cpan.metacpan.org/modules/by-module/IPC/IPC-SharedCache-%{version}.tar.gz
Patch0:         IPC-SharedCache-1.3-test.patch
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module
BuildRequires:  perl(Carp)
BuildRequires:  perl(integer)
BuildRequires:  perl(IPC::ShareLite) >= 0.06
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
# (no additional dependencies)
# Dependencies
Requires:       perl(IPC::ShareLite) >= 0.06

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(IPC::ShareLite\\)$

%description
This module provides a shared memory cache accessed as a tied hash.
Shared memory is an area of memory that is available to all processes.
It is accessed by choosing a key, the ipc_key argument to tie.  Every
process that accesses shared memory with the same key gets access to
the same region of memory.  In some ways it resembles a file system,
but it is not hierarchical and it is resident in memory.  This makes
it harder to use than a filesystem but much faster.  The data in
shared memory persists until the machine is rebooted or it is
explicitly deleted.


%prep
%setup -q -n IPC-SharedCache-%{version}

# Debian patch for tests, which fixes problem of HTML::Template
%patch -P0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}


%check
make test



%files
%license LICENSE
%doc ANNOUNCE Changes README
%{perl_vendorlib}/IPC/
%{_mandir}/man3/IPC::SharedCache.3*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.3-55
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-48
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-45
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-42
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Paul Howarth <paul@city-fan.org> - 1.3-40
- Spec clean-up
  - Use author-independent source URL
  - Classify buildreqs by usage
  - Drop redundant buildroot cleaning in %%install section
  - Simplify find command using -delete
  - Don't need to remove empty directories from the buildroot
  - Fix permissions verbosely
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-38
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-35
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-32
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-30
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 Petr Šabata <contyk@redhat.com> - 1.3-28
- Prevent FTBFS by correcting the build time dependency list
- Package the LICENSE text with %%license

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-26
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-25
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.3-22
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 1.3-19
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-17
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-15
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 17 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-14
- apply Debian patch for tests, which fix problem of HTML::Template

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-13
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.3-12
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-8
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-7.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3-7
- Rebuild for FC6.

* Thu Feb 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3-6
- Rebuild for FC5 (perl 5.8.8).
- Dist tag and specfile cleanups.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.3-5
- rebuilt

* Sat Jun 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.4
- Fix license (bug 1783).
- BuildReq perl(Storable) (bug 1783).

* Fri Jun 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.3
- Bring up to date with current fedora.us perl spec template.

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.2
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).
- BuildArch: noarch.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.1
- First build.
