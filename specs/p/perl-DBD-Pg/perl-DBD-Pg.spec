# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optional tests
%bcond_without perl_DBD_Pg_enables_optional_test

Name:           perl-DBD-Pg
Summary:        A PostgreSQL interface for Perl
Version:        3.18.0
Release: 9%{?dist}
# Pg.pm, README:    Points to directory which contains GPL-2.0-or-later and Artistic-1.0-Perl
# other files:      Same as Perl (GPL-1.0-or-later OR Artistic-1.0-Perl)
License:        GPL-2.0-or-later OR Artistic-1.0-Perl
Source0:        https://cpan.metacpan.org/authors/id/T/TU/TURNSTEP/DBD-Pg-%{version}.tar.gz 
URL:            https://metacpan.org/release/DBD-Pg

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  libpq-devel
# Run-time:
BuildRequires:  perl(constant)
# Prevent bug #443495
BuildRequires:  perl(DBI) >= 1.614
BuildRequires:  perl(Exporter)
BuildRequires:  perl(if)
BuildRequires:  perl(version)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(charnames)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(open)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Simple)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(utf8)
BuildRequires:  postgresql-server
%if %{with perl_DBD_Pg_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Time::Piece)
%endif

Requires:       perl(DBI) >= 1.614

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DBD::Pg\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(DBI\\)$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(App::Info.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(dbdpg_test_setup.pl\\)

%description
DBD::Pg is a Perl module that works with the DBI module to provide access
to PostgreSQL databases.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Test::Simple)
Requires:       postgresql-server
%if %{with perl_DBD_Pg_enables_optional_test}
# Optional tests:
Requires:       perl(Time::Piece)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n DBD-Pg-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
unset AUTOMATED_TESTING DBDPG_GCCDEBUG PERL_MM_USE_DEFAULT \
    POSTGRES_HOME POSTGRES_INCLUDE POSTGRES_LIB
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags} -std=gnu17" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# If variables undefined, package test will create it's own database.
unset DBI_DSN DBI_USER DBI_PASS
unset DBDPG_DEBUG DBDPG_INITDB DBDPG_NOCLEANUP DBDPG_TEST_ALWAYS_ENV \
    DBDPG_TESTINITDB PGDATABASE PGINITDB POSTGRES_HOME POSTGRES_LIB \
    TEST_OUTPUT TEST_SIGNATURE
# The tests write to temporary database which is placed in $DIR
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
# When tests are run by root, 'postgres' is used as DBI_USER
# DBI_USER has to be able to write to the $DIR
if [ `id -u` -eq 0 ]; then
    chown -hR postgres:postgres $DIR
fi
# Jobs can't be run in parallel
prove -I .
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
# Full test coverage requires a live PostgreSQL database (see the README file)
#export DBI_DSN=dbi:Pg:dbname=<database>
#export DBI_USER=<username>
#export DBI_PASS=<password>
# If variables undefined, package test will create it's own database.
unset DBI_DSN DBI_USER DBI_PASS
unset DBDPG_DEBUG DBDPG_INITDB DBDPG_NOCLEANUP DBDPG_TEST_ALWAYS_ENV \
    DBDPG_TESTINITDB PGDATABASE PGINITDB POSTGRES_HOME POSTGRES_LIB \
    TEST_OUTPUT TEST_SIGNATURE
make test

%files
%license LICENSES/*
%doc Changes README README.dev TODO
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/Bundle/DBD/Pg.pm
%{_mandir}/man3/*DBD*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.18.0-7
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.18.0-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.18.0-1
- 3.18.0 bump (rhbz#2253383)

* Wed Oct 25 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.17.0-2
- Package tests

* Thu Aug 24 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.17.0-1
- 3.17.0 bump (rhbz#2234337)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.16.3-2
- Perl 5.38 rebuild

* Wed Apr 05 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.16.3-1
- 3.16.3 bump

* Mon Mar 06 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.16.1-1
- 3.16.1 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Ondřej Sloup <osloup@redhat.com> - 3.16.0-2
- Rebuild for new PostgreSQL 15

* Mon Aug 08 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.16.0-1
- 3.16.0 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.15.1-2
- Perl 5.36 rebuild

* Mon Feb 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.15.1-1
- 3.15.1 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.15.0-1
- 3.15.0 bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.14.2-4
- Perl 5.34 rebuild

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 3.14.2-3
- rebuild for libpq ABI fix rhbz#1908268

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 Petr Pisar <ppisar@redhat.com> - 3.14.2-1
- 3.14.2 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Petr Pisar <ppisar@redhat.com> - 3.14.0-1
- 3.14.0 bump

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.13.0-2
- Perl 5.32 rebuild

* Thu Jun 18 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.13.0-1
- 3.13.0 bump

* Mon Jun 08 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.12.3-1
- 3.12.3 bump

* Fri Jun 05 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.12.2-1
- 3.12.2 bump

* Wed Jun 03 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.12.1-1
- 3.12.1 bump

* Mon May 11 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.12.0-1
- 3.12.0 bump

* Wed Apr 29 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.11.1-1
- 3.11.1 bump

* Fri Apr 24 2020 Petr Pisar <ppisar@redhat.com> - 3.11.0-1
- 3.11.0 bump

* Tue Mar 24 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.10.5-1
- 3.10.5 bump

* Tue Feb 04 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.10.4-1
- 3.10.4 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.10.3-1
- 3.10.3 bump

* Mon Jan 20 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.10.2-1
- 3.10.2 bump

* Tue Jan 14 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.10.1-1
- 3.10.1 bump

* Wed Sep 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.10.0-1
- 3.10.0 bump

* Mon Aug 19 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.9.1-1
- 3.9.1 bump

* Wed Aug 14 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.9.0-1
- 3.9.0 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.8.1-1
- 3.8.1 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.8.0-2
- Perl 5.30 rebuild

* Fri Apr 26 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.8.0-1
- 3.8.0 bump

* Fri Mar 22 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-6
- Fix failing test (bug #1679574)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-3
- Perl 5.28 rebuild

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-2
- Add build-require gcc

* Tue Feb 13 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-1
- 3.7.4 bump

* Mon Feb 12 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.1-1
- 3.7.1 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 25 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.0-1
- 3.7.0 bump
- Remove explicit Provides: perl(DBD::Pg) = %%{version}

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.6.2-2
- Perl 5.26 rebuild

* Wed May 24 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.6.2-1
- 3.6.2 bump

* Tue Apr 18 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.6.0-1
- 3.6.0 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.3-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.3-1
- 3.5.3 bump

* Wed Sep 30 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.2-1
- 3.5.2 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.1-2
- Perl 5.22 rebuild

* Wed Feb 18 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.1-1
- 3.5.1 bump

* Wed Feb 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.0-1
- 3.5.0 bump
- Remove tests sub-package, tests don't work without Makefile

* Mon Sep 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.2-1
- 3.4.2 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-2
- Perl 5.20 rebuild

* Fri Aug 22 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-1
- 3.4.1 bump

* Tue Aug 19 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.0-1
- 3.4.0 bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.3.0-1
- 3.3.0 bump

* Mon May 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.2.1-1
- 3.2.1 bump

* Mon Apr 14 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.1.1-1
- 3.1.1 bump

* Wed Feb 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.0-1
- 3.0.0 bump

* Wed Jan 29 2014 Petr Pisar <ppisar@redhat.com> - 2.19.3-6
- Adapt to changes in Postgres 9.3 (bug #1058723)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.19.3-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 2.19.3-2
- Specify all dependencies
- Move testme.tmp.pl to tests sub-package

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 2.19.3-1
- 2.19.3 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 2.19.2-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Marcela Mašláňová <mmaslano@redhat.com> 2.19.2-1
- bump to 2.19.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-3
- Perl mass rebuild

* Mon Apr  4 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-2
- add requirement for test file

* Tue Mar 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-1
- update to 2.18.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.17.2-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.17.2)

* Thu Sep 30 2010 Petr Sabata <psabata@redhat.com> - 2.17.1-3
- Fixing BuildRequires (perl-version, Test::More)
- Re-enabling tests
- Resolves: rhbz#633108

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.17.1-2
- Mass rebuild with perl-5.12.0

* Tue Apr 27 2010 Petr Pisar <ppisar@redhat.com> - 2.17.1-1
- upstream released 2.17.1
- GPL+ license corrected to GPLv2+
- enable and run %%check in C locale

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 2.15.1-3
- drop patch that was upstreamed long ago (<=2.8.7)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.15.1-2
- rebuild against perl 5.10.1

* Thu Sep 24 2009 Stepan Kasal <skasal@redhat.com> - 2.15.1-1
- new upstream version
- add versioned provide (#525502)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 2.13.1-2
- rebuild against perl-DBI-1.609

* Mon May  4 2009 Stepan Kasal <skasal@redhat.com> - 2.13.1-1
- new upstream release, also fixes #498899

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Stepan Kasal <skasal@redhat.com> - 2.11.6-2
- fix the source URL

* Fri Dec  5 2008 Marcela Mašláňová <mmaslano@redhat.com> - 2.11.6-1
- update

* Fri Oct 31 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.11.2-1
- update to 2.11.2

* Fri Aug 29 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.10.0-1
- update to 2.10.0

* Mon Aug 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.9.2-1
- update to 2.9.2

* Mon Jul 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.8.7-1
- new version has Pg.pm twice in two locations
- update

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-9
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.49-8
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-7
- rebuild for new perl

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-6
- Apply changes from package review.
- Resolves: bz#226252

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-5.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-5
- Fix license tag
- Add %%doc
- Remove explicit Provides: perl(DBD::Pg) = %%{version}
- Other cleanups

* Tue Jul 17 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-4
- Fix summary

* Tue Dec 05 2006 Robin Norwood <rnorwood@redhat.com> - 1.49-3
- rebuild for new version of postgres.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.49-2
- rebuild

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 1.49-1
- Upgrade to upstream version 1.49

* Wed Apr 12 2006 Jason Vas Dias <jvdias@redhat.com> - 1.48-1
- Upgrade to upstream version 1.48

* Wed Mar 22 2006 Jason Vas Dias <jvdias@redhat.com> - 1.47-1
- Upgrade to upstream version 1.47

* Wed Mar 08 2006 Jason Vas Dias <jvdias@redhat.com> - 1.45-1
- Upgrade to upstream version 1.45

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.43-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.43-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.43-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Nov 03 2005 Florian La Roche <laroche@redhat.com>
- make sure correct Provides: are generated for this module

* Tue Jun 28 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.43-1
- Update to 1.43 (corrects #156840).

* Thu May 19 2005 Warren Togami <wtogami@redhat.com> - 1.41-2
- Disable gcc optimization to workaround broken placeholders (#156840)

* Wed  Apr 13 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.41-1
- Update to 1.41.
- Updated the requirements versions.
- Specfile cleanup. (#154203)

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 1.40-2
- rebuild for new libpq soname

* Thu Mar 31 2005 Warren Togami <wtogami@redhat.com> 1.40-1
- 1.40

* Tue Oct 12 2004 Chip Turner <cturner@redhat.com> 1.32-1
- bugzilla: 127755, update to 1.32

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.31-2
- rebuild

* Thu Dec 11 2003 Chip Turner <cturner@redhat.com> 1.31-1
- update to 1.31

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 1.22-1
- move to upstream 1.22

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Mon Jan 13 2003 Chip Turner <cturner@redhat.com>
- update to 1.21

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use internal rpm dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-5
- Rebuild

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-4
- Rebuild, to fix #66304

* Wed Jun  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-3
- Integrate with newer perl

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-1
- 1.13

* Fri Feb 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-8
- Rebuild

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-7
- Rebuild

* Thu Jan 31 2002 Tim Powers <timp@redhat.com>
- rebuild to solve more deps

* Tue Jan 29 2002 Bill Nottingham <notting@redhat.com> 1.01-5
- rebuild (dependencies)

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-2
- Rebuild

* Sun Jul  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.01 bugfix release ("bytea" coredumped with values outside 0...127)
- Add perl-DBI and perl to BuildRequires (they were just in Requires: previously)

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.00
- change group to Applications/Databases from Applications/CPAN

* Tue May  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.98, for postgresql-7.1
- add doc files
- cleanups

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- First cut
