# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Cache-Cache
Version:        1.08
Release:        32%{?dist}
Summary:        Generic cache interface and implementations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Cache-Cache
Source0:        https://cpan.metacpan.org/modules/by-module/Cache/Cache-Cache-%{version}.tar.gz
# Bug #112967 for Cache-Cache: Digest::SHA1 -> Digest::SHA - https://rt.cpan.org/Public/Bug/Display.html?id=112967
Patch0:         Cache-Cache-1.08-Rewrite_from_SHA1_to_SHA.patch
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Error)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IPC::ShareLite)
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
# (no additional dependencies)
# Dependencies
# (no additional dependencies)

%description
The Cache modules are designed to assist a developer in persisting data for a
specified period of time.  Often these modules are used in web applications to
store data locally to save repeated and redundant expensive calls to remote
machines or databases.  People have also been known to use Cache::Cache for
its straightforward interface in sharing data between runs of an application
or invocations of a CGI-style script or simply as an easy to use abstraction
of the filesystem or shared memory.

%prep
%setup -q -n Cache-Cache-%{version}
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
%license COPYING
%doc CHANGES CREDITS DISCLAIMER README STYLE
%{perl_vendorlib}/Cache/
%{_mandir}/man3/Cache::BaseCache.3*
%{_mandir}/man3/Cache::BaseCacheTester.3*
%{_mandir}/man3/Cache::Cache.3*
%{_mandir}/man3/Cache::CacheMetaData.3*
%{_mandir}/man3/Cache::CacheSizer.3*
%{_mandir}/man3/Cache::CacheTester.3*
%{_mandir}/man3/Cache::CacheUtils.3*
%{_mandir}/man3/Cache::FileBackend.3*
%{_mandir}/man3/Cache::FileCache.3*
%{_mandir}/man3/Cache::MemoryBackend.3*
%{_mandir}/man3/Cache::MemoryCache.3*
%{_mandir}/man3/Cache::NullCache.3*
%{_mandir}/man3/Cache::Object.3*
%{_mandir}/man3/Cache::SharedMemoryBackend.3*
%{_mandir}/man3/Cache::SharedMemoryCache.3*
%{_mandir}/man3/Cache::SizeAwareCache.3*
%{_mandir}/man3/Cache::SizeAwareCacheTester.3*
%{_mandir}/man3/Cache::SizeAwareFileCache.3*
%{_mandir}/man3/Cache::SizeAwareMemoryCache.3*
%{_mandir}/man3/Cache::SizeAwareSharedMemoryCache.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Michal Josef Špaček <mspacek@redhat.com> - 1.08-30
- Rewrite from Digest::SHA1 to SHA

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-23
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-20
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-17
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 15 2019 Paul Howarth <paul@city-fan.org> - 1.08-15
- Spec tidy-up
  - Use author-independent source URL
  - Simplify find command using -delete
  - Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-2
- Perl 5.22 rebuild

* Mon Jan 26 2015 Paul Howarth <paul@city-fan.org> - 1.08-1
- Update to 1.08
  - Try to avoid some race conditions
  - Typo fixes
- This release by RJBS → update source URL
- Use %%license
- Make %%files list more explicit

* Wed Nov 12 2014 Petr Šabata <contyk@redhat.com> - 1.07-1
- 1.07 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-19
- Perl 5.20 rebuild

* Wed Aug 13 2014 Petr Pisar <ppisar@redhat.com> - 1.06-18
- Fix race between adding two key sets in tests (bug #1128792)

* Wed Aug 13 2014 Petr Pisar <ppisar@redhat.com> - 1.06-17
- Fix other time race in tests (bug #1112553)

* Thu Jun 26 2014 Petr Pisar <ppisar@redhat.com> - 1.06-16
- Fix time races in tests (bug #1112553)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.06-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 1.06-10
- Perl 5.16 rebuild

* Thu Mar 22 2012 Tom Callaway <spot@fedoraproject.org> - 1.06-9
- fix BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.06-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-5
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.06-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 Steven Pritchard <steve@kspei.com> 1.06-1
- Update to 1.06.
- Reformat to match cpanspec output.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Drop explicit perl build dependency.
- Update Source0 URL.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-3
- Dist tag.

* Thu Dec 29 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.04-2
- rebuilt

* Fri Mar 18 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Mon Feb 28 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Bring up to date with current fedora.extras perl spec template.

* Tue Feb  1 2005 Matthias Saou <http://freshrpms.net/> 1.03-1
- Merge in changes from Jose Pedro Oliveira's fedora.us package : #146741.
- Update to 1.03.

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 1.02-4
- Bump release to provide Extras upgrade path.

* Wed May 26 2004 Matthias Saou <http://freshrpms.net/> 1.02-3
- Rebuilt for Fedora Core 2.

* Fri Apr  2 2004 Matthias Saou <http://freshrpms.net/> 1.02-2
- Change the explicit package deps to perl package style ones to fix the
  perl-Storable obsoletes problem.

* Fri Mar 19 2004 Matthias Saou <http://freshrpms.net/> 1.02-1
- Initial RPM release.

