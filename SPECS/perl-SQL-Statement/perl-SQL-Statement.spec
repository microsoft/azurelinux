# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-SQL-Statement
Version:        1.414
Release:        16%{?dist}
Summary:        SQL parsing and processing engine
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/SQL-Statement
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/SQL-Statement-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone) >= 0.30
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI) >= 1.616
BuildRequires:  perl(Encode)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Math::Base::Convert)
BuildRequires:  perl(Math::Trig)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Params::Util) >= 1.00
BuildRequires:  perl(Scalar::Util) >= 1.0
# XXX: BuildRequires:  perl(SQL::UserDefs)
BuildRequires:  perl(sort)
BuildRequires:  perl(Text::Balanced)
BuildRequires:  perl(Text::Soundex)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(vars)
# Tests only
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More)
# Optional tests only
# DBD::CSV buildrequires SQL::Statement
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(DBD::CSV) >= 0.30
%endif
BuildRequires:  perl(DBD::DBM) >= 0.06
BuildRequires:  perl(DBD::File) >= 0.40
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(MLDBM)
Requires:       perl(Clone) >= 0.30
Requires:       perl(DBI) >= 1.616
Requires:       perl(Math::Base::Convert)
Requires:       perl(Params::Util) >= 1.00
Requires:       perl(Scalar::Util) >= 1.0
# This module doesn't seem to exist...
# XXX: Requires:       perl(SQL::UserDefs)
Requires:       perl(Text::Soundex)

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Clone|Params::Util|Scalar::Util)\\)$

%description
The SQL::Statement module implements a pure Perl SQL parsing and execution
engine.  While it by no means implements full ANSI standard, it does support
many features including column and table aliases, built-in and user-defined
functions, implicit and explicit joins, complexly nested search conditions, and
other features.

%prep
%setup -q -n SQL-Statement-%{version}
find -type f -exec chmod a-x {} +
perl -pi -e 's/\r//go' README

%build
export SQL_STATEMENT_WARN_UPDATE=sure
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license ARTISTIC-1.0 GPL-1 GPL-2.0 LICENSE
%doc Changes README README.md
%{perl_vendorlib}/SQL/
%{_mandir}/man3/*.3pm*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.414-8
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.414-7
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.414-4
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.414-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.414-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.414-1
- 1.414 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.412-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-15
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-14
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.412-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.412-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-11
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.412-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.412-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-7
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.412-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.412-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-2
- Perl 5.26 rebuild

* Fri Apr 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.412-1
- 1.412 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.410-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 05 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.410-1
- 1.410 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.409-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.409-2
- Perl 5.24 rebuild

* Mon Apr 11 2016 Petr Pisar <ppisar@redhat.com> - 1.409-1
- 1.409 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.407-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.407-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.407-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.407-2
- Perl 5.22 rebuild

* Tue May 26 2015 Petr Šabata <contyk@redhat.com> - 1.407-1
- 1.407 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.405-9
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.405-8
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.405-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 29 2014 Paul Howarth <paul@city-fan.org> - 1.405-6
- Bootstrap build for epel7 done

* Wed Jan 29 2014 Paul Howarth <paul@city-fan.org> - 1.405-5
- Bootstrap epel7 build

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.405-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.405-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.405-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Petr Šabata <contyk@redhat.com> - 1.405-1
- 1.405 enhancement bump

* Fri May 24 2013 Petr Šabata <contyk@redhat.com> - 1.404-1
- 1.404 bump, Soundex is now optional

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.402-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Petr Šabata <contyk@redhat.com> - 1.402-1
- 1.402 bump

* Fri Nov 02 2012 Petr Pisar <ppisar@redhat.com> - 1.401-3
- Correct dependencies

* Thu Nov 01 2012 Petr Pisar <ppisar@redhat.com> - 1.401-2
- Specify all dependencies

* Wed Oct 31 2012 Petr Šabata <contyk@redhat.com> - 1.401-1
- 1.401 bump (upstream switches to 3-digit minor version)
- Drop command macros and modernize spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.33-8
- Perl 5.16 re-rebuild of bootstrapped packages

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 1.33-7
- Perl 5.16 rebuild

* Tue Apr 10 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-6
- remove DBD::AnyData which were removed by upstream for now 810377

* Fri Apr  6 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-5
- apply Paul's bootstrap macro 810377

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.33-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Petr Sabata <psabata@redhat.com> - 1.33-1
- 1.33 bump

* Mon Jan 24 2011 Petr Pisar <ppisar@redhat.com> - 1.32-1
- 1.32 bump
- Update build time dependencies

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.31-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 07 2010 Petr Pisar <ppisar@redhat.com> - 1.31-1
- 1.31 bump (incompatible with perl(DBI) <= 1.611) (bug #631306)

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 1.27-1
- 1.27 bump (do not backport, 1.22 lower-cases unqouted identifiers)
- Make tests fatal again

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.20-2
- rebuild against perl 5.10.1

* Wed Sep 23 2009 Stepan Kasal <skasal@redhat.com> - 1.20-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-4
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-2.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-2
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-2
- Rebuild for FC5 (perl 5.8.8).

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- First build.
