# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-DBD-CSV
Version:        0.62
Release: 4%{?dist}
Summary:        DBI driver for CSV files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/DBD-CSV
Source0:        https://cpan.metacpan.org/modules/by-module/DBD/DBD-CSV-%{version}.tgz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
# Module Runtime
# The DBI and SQL::Statement are needed per DBD::CVS POD
BuildRequires:  perl(Carp)
BuildRequires:  perl(DBD::File) >= 0.44
BuildRequires:  perl(DBI) >= 1.628
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(SQL::Statement) >= 1.405
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::CSV_XS) >= 1.45
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(charnames)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Test::More) >= 0.90
# Dependencies
Requires:       perl(DBD::File) >= 0.44
Requires:       perl(DBI) >= 1.628
Requires:       perl(Exporter)
Requires:       perl(SQL::Statement) >= 1.405
Requires:       perl(Text::CSV_XS) >= 1.45

%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(DBD::File\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Text::CSV_XS\\)$

%description
The DBD::CSV module is yet another driver for the DBI (Database
independent interface for Perl). This one is based on the SQL
"engine" SQL::Statement and the abstract DBI driver DBD::File
and implements access to so-called CSV files (Comma separated
values). Such files are mostly used for exporting MS Access and
MS Excel data.

%prep
%setup -q -n DBD-CSV-%{version}
chmod -c a-x ChangeLog README lib/DBD/*.pm lib/Bundle/DBD/*.pm

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc ChangeLog CONTRIBUTING.md README SECURITY.md
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/DBD/
%{_mandir}/man3/Bundle::DBD::CSV.3*
%{_mandir}/man3/DBD::CSV.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Paul Howarth <paul@city-fan.org> - 0.62-1
- Update to 0.62 (rhbz#2337361)
  - It's 2025
  - Replace "use vars" with "our" (GH#9)
  - Specify recommended versions based on known CVE's
  - Update documentation for groff-1.24
  - Tested with perl-5.40.0
  - Add SECURITY.md

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan  6 2023 Paul Howarth <paul@city-fan.org> - 0.60-1
- Update to 0.60
  - It's 2023
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.59-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan  1 2022 Paul Howarth <paul@city-fan.org> - 0.59-1
- Update to 0.59
  - It's 2022

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.58-2
- Perl 5.34 rebuild

* Wed Feb 10 2021 Paul Howarth <paul@city-fan.org> - 0.58-1
- Update to 0.58
  - It's 2021
  - "class" is not a CSV attribute to pass on (GH#8)
- Use author-independent source URL

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Paul Howarth <paul@city-fan.org> - 0.57-1
- Update to 0.57
  - META fixes

* Sat Dec  5 2020 Paul Howarth <paul@city-fan.org> - 0.56-1
- Update to 0.56
  - Fix Changes (add missing entry for 0.54)
  - Bugtracker ⇒ GitHub Issues
  - f_dir should exist (CVE fix in DBI-1.644 / DBD::File-0.45)
  - TODO tests better skipped if failing

* Mon Jul 27 2020 Paul Howarth <paul@city-fan.org> - 0.55-1
- Update to 0.55
  - It's 2020
  - Provide cpanfile
  - Documentation enhancements
  - Make csv_ and f_ aliases more consistently available (GH#7)

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.54-7
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct  5 2019 Paul Howarth <paul@city-fan.org> - 0.54-5
- Modernize spec
  - Use author-independent source URL
  - Use %%{make_build} and %%{make_install}

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.54-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 29 2018 Paul Howarth <paul@city-fan.org> - 0.54-1
- Update to 0.54
  - Free unref scalar test fixed in Text::CSV_XS 1.35

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.53-2
- Perl 5.28 rebuild

* Mon May 21 2018 Paul Howarth <paul@city-fan.org> - 0.53-1
- Update to 0.53
  - No folder scanning during automated tests
  - Fix col_names set to empty [] incorrectly skipping first row (GH#6)
  - Small doc fix
  - Tested on FreeBSD
- Switch upstream from search.cpan.org to metacpan.org

* Thu Apr  5 2018 Paul Howarth <paul@city-fan.org> - 0.52-1
- Update to 0.52
  - More test fixes for Perl without dot in @INC

* Sun Mar 25 2018 Paul Howarth <paul@city-fan.org> - 0.51-1
- Update to 0.51
  - Fix tests for Perl without dot in @INC

* Thu Mar 22 2018 Paul Howarth <paul@city-fan.org> - 0.50-1
- Update to 0.50
  - Explain more about header folding
  - BOM handling
  - Some documentation enhancements
  - Ignore DBI_DSN if it is not CSV
  - It's 2018
  - Test with perl-5.26, DBI-1.641, SQL::Statement-1.412, and Text::CSV_XS-1.35
- Drop legacy Group: tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-2
- Perl 5.24 rebuild

* Thu May 12 2016 Paul Howarth <paul@city-fan.org> - 0.49-1
- Update to 0.49
  - Simplified test-table-name generation
  - Prefer quote_empty over quote_always for size (Text::CSV_XS => 1.18)
  - Add CONTRIBUTING.md
  - It's 2016
  - Added docs to warn for reserved words (CPAN RT#106529)
  - Minor spelling corrections
  - Test with perl 5.24.0, DBI 1.636, SQL::Statement 1.410, Text::CSV_XS 1.23
- Make %%files list more explicit

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-2
- Perl 5.22 rebuild

* Fri Feb 13 2015 Petr Šabata <contyk@redhat.com> - 0.48-1
- 0.48 bump

* Sun Nov 16 2014 Paul Howarth <paul@city-fan.org> - 0.46-1
- 0.46 bump

* Wed Oct 29 2014 Petr Šabata <contyk@redhat.com> - 0.45-1
- 0.45 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-2
- Perl 5.20 rebuild

* Fri Aug 08 2014 Petr Šabata <contyk@redhat.com> - 0.44-1
- 0.44 bump

* Tue Jul 01 2014 Petr Šabata <contyk@redhat.com> - 0.43-1
- 0.43 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 13 2013 Petr Šabata <contyk@redhat.com> - 0.41-1
- 0.41 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.40-1
- 0.40 bump

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.38-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Petr Šabata <contyk@redhat.com> - 0.38-1
- 0.38 bump
- Drop the rpm4.8 style filters

* Mon Nov 05 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-2
- Specify all dependencies

* Mon Aug 27 2012 Petr Šabata <contyk@redhat.com> - 0.36-1
- 0.36 bump, debugging enhancements

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 0.35-2
- Perl 5.16 rebuild

* Tue Jun 05 2012 Petr Šabata <contyk@redhat.com> - 0.35-1
- 0.35 bump (documentation changes)

* Tue May 15 2012 Petr Šabata <contyk@redhat.com> - 0.34-1
- 0.34 bump (no code changes)
- Drop commands macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Petr Sabata <contyk@redhat.com> - 0.33-1
- 0.33 bump
- Remove now obsolete BuildRoot and defattr

* Mon Jul 25 2011 Petr Pisar <ppisar@redhat.com> - 0.31-5
- RPM 4.9 dependency filtering added

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.31-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 22 2010 Petr Pisar <ppisar@redhat.com> - 0.31-1
- 0.31 bump
- Remove unversioned Requires

* Mon Jul 12 2010 Petr Pisar <ppisar@redhat.com> - 0.30-1
- 0.30 bump (bug #613251)

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 0.29-1
- 0.29 bump

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.27-2
- Mass rebuild with perl-5.12.0

* Thu Mar 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.27-1
- update
- replace DESTDIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-6
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-5
- Added perl(SQL::Statement) to requirements list (#208012).

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-4
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-3
- Rebuild for FC5 (perl 5.8.8).

* Sat Dec 17 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-2
- Missing build requirement: DBD::File >= 0.30.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- First build.
