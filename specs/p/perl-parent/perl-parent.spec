# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-parent
Epoch:		1
Version:	0.244
Release:	520%{?dist}
Summary:	Establish an ISA relationship with base classes at compile time
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/parent
Source0:	https://cpan.metacpan.org/authors/id/C/CO/CORION/parent-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:	perl(strict)
# Test Suite
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.40
# Dependencies
# (none)

%description
Allows you to both load one or more modules, while setting up inheritance
from those modules at the same time. Mostly similar in effect to:

	package Baz;

	BEGIN {
		require Foo;
		require Bar;

		push @ISA, qw(Foo Bar);
	}

%prep
%setup -q -n parent-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes
%{perl_vendorlib}/parent.pm
%{_mandir}/man3/parent.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.244-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.244-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.244-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 13 2024 Paul Howarth <paul@city-fan.org> - 1:0.244-1
- Update to 0.244
  - Update (commented) comparison with $] to use quotes

* Fri Nov 29 2024 Paul Howarth <paul@city-fan.org> - 1:0.243-1
- Update to 0.243
  - Reinstate test for apostrophe as package separator, as that package
    separator is allowed again (no code change, only tests have been amended)
- Use %%{make_build} and %%{make_install}

* Wed Aug 14 2024 Paul Howarth <paul@city-fan.org> - 1:0.242-1
- Update to 0.242
  - Don't test for apostrophe as package separator on Perl versions after 5.41
  - Protect against modules changing @_

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.241-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.241-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.241-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.241-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.241-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.241-499
- Increase release to favour standalone package

* Wed Feb 15 2023 Paul Howarth <paul@city-fan.org> - 1:0.241-1
- Update to 0.241
  - Actually include the changes documented for version 0.240

* Tue Feb 14 2023 Paul Howarth <paul@city-fan.org> - 1:0.240-1
- Update to 0.240
  - Use Test::More::isnt() instead of Test::More::isn't in tests, which is
    deprecated, as ' isn't allowed as package separator in an upcoming version
    of Perl (GH#13)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.239-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec  7 2022 Paul Howarth <paul@city-fan.org> - 1:0.239-1
- Update to 0.239
  - Harden against changes to require error messages: the '@INC contains' may
    change in a future release of perl; this hardens the test to be insensitive
    to the exact words chosen (https://github.com/Perl/perl5/pull/20547)
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.238-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.238-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.238-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.238-478
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.238-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.238-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.238-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.238-456
- Increase release to favour standalone package

* Fri Feb  7 2020 Paul Howarth <paul@city-fan.org> - 1:0.238-1
- Update to 0.238
  - Move the prerequisite Test::More from being a runtime prerequisite to a
    test time / build time prerequisite (GH#11)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.237-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.237-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.237-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.237-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.237-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul  7 2018 Paul Howarth <paul@city-fan.org> - 1:0.237-1
- Update to 0.237
  - Don't load vars.pm (Perl RT#132077)
- Drop legacy Group: tag
- Drop buildroot cleaning in %%install section

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.236-416
- Increase release to favour standalone package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.236-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.236-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.236-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.236-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Paul Howarth <paul@city-fan.org> - 1:0.236-1
- Update to 0.236
  - Add Travis test configuration
  - Make test for PMC availability more reliable
  - Disable benchmark test rt62341.t as it runs out of memory on many smoker
    systems (CPAN RT#118310)
- Simplify find command using -delete

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.234-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.234-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.234-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.234-2
- Perl 5.22 rebuild

* Thu May 28 2015 Paul Howarth <paul@city-fan.org> - 1:0.234-1
- Update to 0.234
  - Fix the test for PMC loading to work on versions on Perl that don't have
    Config::non_bincompat_options (CPAN RT#102626)

* Tue May 26 2015 Paul Howarth <paul@city-fan.org> - 1:0.233-1
- Update to 0.233
  - The diagnostic about inheriting from ourselves was removed; it served no
    purpose as Perl already warns if we try to inherit in a circular way

* Fri Mar 20 2015 Paul Howarth <paul@city-fan.org> - 1:0.232-1
- Update to 0.232
  - Change line-endings in parent-pmc.t to unix EOLs so that bleadperl is happy

* Tue Mar 10 2015 Paul Howarth <paul@city-fan.org> - 1:0.231-1
- Update to 0.231
  - Restore test compatibility where Perl does not provide
    &Config::non_bincompat_options (CPAN RT#102626)

* Sat Mar  7 2015 Paul Howarth <paul@city-fan.org> - 1:0.229-1
- Update to 0.229
  - Add link to (Github) repository
  - Guard tests against PERL_DISABLE_PMC

* Tue Jan 13 2015 Petr Pisar <ppisar@redhat.com> - 1:0.228-311
- Specify all dependencies

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.228-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.228-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.228-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 17 2013 Paul Howarth <paul@city-fan.org> - 1:0.228-1
- Update to 0.228
  - Install in site/ by default for 5.12+ (CPAN RT#88450)

* Sun Sep  1 2013 Paul Howarth <paul@city-fan.org> - 1:0.227-1
- Update to 0.227
  - Restore tests passing for 5.17.5+ (CPAN RT#88320)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.226-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Paul Howarth <paul@city-fan.org> - 1:0.226-1
- Update to 0.226
  - Fix tests for Perl 5.18 (CPAN RT#86890)

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:0.225-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:0.225-245
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:0.225-244
- Adjust tests to perl-5.18 (CPAN RT#86890)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.225-243
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 1:0.225-242
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 1:0.225-241
- Specify all dependencies

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-240
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.225-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1:0.225-7
- Perl 5.16 rebuild

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 1:0.225-6
- Reinstate compatibility with old distributions like EL-5
  - Add back buildroot definition and cleaning
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit
- Drop redundant %%{?perl_default_filter}
- Don't use macros for commands
- Use tabs

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.225-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-4
- Install to vendor directories rather than perl core directories so as to
  avoid conflicts between our debuginfo and the main perl-debuginfo package

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-3
- Perl mass rebuild

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-2
- Perl mass rebuild

* Sat May 07 2011 Iain Arnell <iarnell@gmail.com> - 1:0.225-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> - 1:0.224-1
- Update to latest upstream version

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.223-4
- Mass rebuild with perl-5.12.0

* Sat Mar 27 2010 Iain Arnell <iarnell@gmail.com> - 1:0.223-3
- Dual-life module
- Add epoch to match that of parent in core
- Use core macros, not vendor

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.223-2
- Rebuild against perl 5.10.1

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.223-1
- Update filtering
- Auto-update to 0.223 (by cpan-spec-update 0.01)
- Altered br on perl(Test::More) (0 => 0.4)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.221-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.221-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 19 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.221-2
- Bump

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.221-1
- Specfile autogenerated by cpanspec 1.75
