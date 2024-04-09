# This module usually ships with version numbers having two digits after the decimal point
%global cpanversion 1.443

Summary:        Test file attributes through Test::Builder
Name:           perl-Test-File
Version:        1.44.3
Release:        12%{?dist}
License:        Artistic-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Test-File
Source0:        https://cpan.metacpan.org/authors/id/B/BD/BDFOY/Test-File-%{cpanversion}.tar.gz#/perl-Test-File-%{cpanversion}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::Manifest) >= 1.21
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::Builder) >= 1.001006
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More) >= 0.95
BuildRequires:  perl(Test::utf8)
BuildRequires:  perl(utf8)
# Optional Tests
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides a collection of test utilities for file attributes.

Some file attributes depend on the owner of the process testing the file
in the same way the file test operators do.

%prep
%setup -q -n Test-File-%{cpanversion}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README.pod
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::File.3*

%changelog
* Thu Mar 28 2024 Andrew Phelps <anphel@microsoft.com> - 1.44.3-12
- Remove `rpmversion` global definition due to macro conflict with rpm-4.18.2
- Update license to Artistic-2.0
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.44.3-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.44.3-8
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.44.3-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.44.3-2
- Perl 5.26 rebuild

* Mon Apr 17 2017 Paul Howarth <paul@city-fan.org> - 1.44.3-1
- Update to 1.443
  - Found another relative path require issue:
    http://blogs.perl.org/users/ryan_voots/2017/04/trials-and-troubles-with-changing-inc.html
  - This is another attempt at avoiding failures from the v5.26 removal of . from @INC
- Drop redundant Group: tag

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Paul Howarth <paul@city-fan.org> - 1.44.2-1
- Update to 1.442
  - Fix for missing . in @INC; this relates to CVE-2016-1238
    (https://github.com/briandfoy/test-file/issues/14)
- Split rpm and upstream versioning
- Use features from recent EUMM to simplify %%install section

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul  6 2015 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  - Fix problem with META* specifying requirements (CPAN RT#105210)
  - Don't install README.pod
  - check file_mode_has tests for Windows
  - Fix file_has_* tests to work on Windows (GH#13)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.41-2
- Perl 5.22 rebuild

* Wed Sep 24 2014 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - Uncomment accidentally commented symlink_target_is_absolute_ok
  - Add mtime test functions (GH#8)
  - Allow tests to run in parallel (CPAN RT#89908, CPAN RT#91862)
  - Fix up tests for UTF-8 checks
- This release by BDFOY → update source URL
- Classify buildreqs by usage
- Use %%license

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan  2 2014 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36
  - Fix bad line counts on latest dev version of Perl (CPAN RT#89849)

* Thu Oct 10 2013 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35
  - Don't distribute MYMETA.* (CPAN RT#89175)
  - Add dir_exists_ok and dir_contains_ok
  - Add file_contains_* functions
- Specify all dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.34-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 1.34-1
- Update to 1.34
  - Added dir_exists_ok and dir_contains_ok
  - Added file_contains_like and file_contains_unlike
  - Fixed a few grammatical errors in POD
  - Added some SKIP blocks to avoid test failures when running as root
  - Fixed qr//mx patterns to work with older Perls (CPAN RT#74365)
  - Fixed incorrect spelling of "privileges" in SKIP blocks (CPAN RT#74483)
  - Skip testing of symlinks on Windows (CPAN RT#57682)
  - Fixed automatically generated test name for owner_isnt (CPAN RT#37676)
  - Fixed problem in MANIFEST file (CPAN RT#37676)
  - Fixed problem in links.t (CPAN RT#76853)
- This release by BAREFOOT -> update source URL
- BR: perl(base), perl(Exporter) and perl(File::Spec)
- Bump perl(Test::Manifest) version requirement to 1.21
- Bump perl(Test::More) version requirement to 0.88
- Drop perl(ExtUtils::MakeMaker) version requirement
- BR: at least version 1.00 of perl(Test::Pod)
- Drop buildreq perl(Test::Prereq) since t/prereq.t isn't in the test_manifest
- Package LICENSE file
- Expand %%summary and %%description
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Make %%files list more explicit
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.29-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.29-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Jun 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.29-1
- update to 1.29

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.25-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.25-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.25-1
- Upstream update.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-3
- helps if you upload new source

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-1
- bump to 1.22
- fix license tag

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Fri May 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.

* Wed May 03 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- First build.
