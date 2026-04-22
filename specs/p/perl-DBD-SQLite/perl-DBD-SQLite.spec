# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%bcond_without perl_DBD_SQLite_enables_optional_test

Name:           perl-DBD-SQLite
Version:        1.76
Release: 5%{?dist}
Summary:        SQLite DBI Driver
# lib/DBD/SQLite.pm:        GPL-1.0-or-later OR Artistic-1.0-Perl
# LICENSE:                  GPL-1.0-or-later OR Artistic-1.0-Perl
## unbundled
# inc/Test/FailWarnings.pm: Apache-2.0
# sqlite3.c:                Public Domain (copied from sqlite)
# sqlite3.h:                Public Domain (copied from sqlite)
# sqlite3ext.h:             Public Domain (copied from sqlite)
License:        ( GPL-1.0-or-later OR Artistic-1.0-Perl ) AND LicenseRef-Fedora-Public-Domain
URL:            https://metacpan.org/release/DBD-SQLite
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
# Use system sqlite if it is available
Patch0:         perl-DBD-SQLite-bz543982.patch
# Remove notes about bundled sqlite C source from man page and README
Patch1:         DBD-SQLite-1.62-Remove-bundled-source-extentions.patch
# Adapt tests to unbundled Test::FailWarnings
Patch2:         DBD-SQLite-1.64-Unbundle-Test-FailWarnings.patch
# if sqlite >= 3.6.0 then
#   perl-DBD-SQLite uses the external library
# else
#   perl-DBD-SQLite is self-contained (uses the sqlite local copy)
# But we always unbundle sqlite.
BuildRequires:  sqlite-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
# Prevent from bug #443495
BuildRequires:  perl(DBI) >= 1.607
BuildRequires:  perl(DBI::DBD)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(strict)
# Run-time:
# File::Basename not used
BuildRequires:  perl(locale)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Tests only
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
# POSIX not used
BuildRequires:  perl(Test::More)
# Test::FailWarnings not used
BuildRequires:  perl(Time::HiRes)
# Win32 not used
%if %{with perl_DBD_SQLite_enables_optional_test}
# Optional tests
BuildRequires:  perl(Unicode::UCD)
%endif

%{?perl_default_filter}

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(SQLiteTest\\)

%description
SQLite is a public domain, file-based, relational database engine that you can
find at <https://www.sqlite.org/>. This package provides a Perl DBI driver for
SQLite.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n DBD-SQLite-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
# Remove bundled sqlite libraries (BZ#1059154)
# System libraries will be used
rm sqlite*
perl -i -ne 'print $_ unless m{^sqlite}' MANIFEST
# Remove bundled modules
rm -rf inc
perl -i -ne 'print $_ unless m{^inc/}' MANIFEST
# Handle optional tests
%if !%{with perl_DBD_SQLite_enables_optional_test}
rm t/virtual_table/21_perldata_charinfo.t
perl -i -ne 'print $_ unless m{^t/virtual_table/21_perldata_charinfo\.t}' MANIFEST
%endif

# Help generators to recognize Perl scripts
for F in `find t -name *.t`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build} OPTIMIZE="%{optflags}"

%install
%{make_install}
find %{buildroot} -type f  -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*.3pm*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.76-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.76-3
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.76-1
- 1.76 bump (rhbz#2319885)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.74-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.74-1
- 1.74 bump (rhbz#2239708)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.72-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.72-3
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.72-1
- 1.72 bump
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.70-4
- Perl 5.36 rebuild

* Fri Mar 18 2022 Petr Pisar <ppisar@redhat.com> - 1.70-3
- Adapt to SQLite-3.38.0 (bug #2065567)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.70-1
- 1.70 bump

* Thu Jul 29 2021 Adam Williamson <awilliam@redhat.com> - 1.68-2
- (backport) disable sqlite_unicode deprecation warning as it's widely used

* Thu Jul 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.68-1
- 1.68 bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.66-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.66-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 08 2020 Petr Pisar <ppisar@redhat.com> - 1.66-2
- Update DBD-SQLite-1.60-Unbundle-Test-NoWarnings.patch
- Do not build-require unused Test::FailWarnings
- Update the description

* Mon Aug 31 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.66-1
- 1.66 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.64-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.64-5
- Perl 5.32 rebuild

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 1.64-4
- Spec file cleanups: Use make_build and make_install macros
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMaker
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.64-2
- Initialize filename variable in sqlite_db_filename()

* Tue Aug 13 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.64-1
- 1.64 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.62-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.62-1
- 1.62 bump

* Mon Dec 03 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-1
- 1.60 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.58-2
- Perl 5.28 rebuild

* Thu Mar 29 2018 Petr Pisar <ppisar@redhat.com> - 1.58-1
- 1.58 bump

* Thu Mar  1 2018 Florian Weimer <fweimer@redhat.com> - 1.56-2
- Rebuild with new redhat-rpm-config/perl build flags

* Thu Mar 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.56-1
- 1.56 bump

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.54-7
- Add build-require gcc

* Thu Feb 08 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.54-6
- Adjust to sqlite-3.22.0 (bug #1543286)
- Add new index constraint ops introduced in SQLite 3.21.0 to PerlData

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.54-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.54-1
- 1.54 bump

* Wed Nov 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-1
- 1.52 bump

* Sun Jul 24 2016 Petr Pisar <ppisar@redhat.com> - 1.50-4
- Enable perl FTS3 tokenizer with sqlite older than 3.11.0 (CPAN RT#112474)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-3
- Perl 5.24 rebuild

* Thu Feb 18 2016 Petr Pisar <ppisar@redhat.com> - 1.50-2
- Adjust to sqlite-3.11.0 (bug #1309675)
- Rebase Remove-bundled-source-extentions.patch to prevent from packing backup
  files

* Thu Feb 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-1
- 1.50 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Petr Pisar <ppisar@redhat.com> - 1.48-3
- Adapt to sqlite-3.10.0 by adding DBD::SQLite::strlike() (bug #1298628)

* Fri Jun 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.48-2
- Updated patch

* Thu Jun 18 2015 Tom Callaway <spot@fedoraproject.org> - 1.48-1
- update to 1.48

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-3
- Perl 5.22 rebuild

* Fri Mar 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-2
- Correct license from (GPL+ or Artistic) to ((GPL+ or Artistic) and
  Public Domain)

* Wed Dec 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-1
- 1.46 bump

* Wed Oct 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-1
- 1.44 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-3
- Removed bundled sqlite library and updated man page (BZ#1059154)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-1
- 1.42 bump

* Wed Jan 29 2014 Petr Pisar <ppisar@redhat.com> - 1.40-3
- Fix tests with sqlite >= 3.8.2 (bug #1058709)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-1
- 1.40 bump

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.39-2
- Perl 5.18 rebuild

* Mon Jun 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.39-1
- 1.39 bump
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Update source URL

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.37-2
- Perl 5.16 rebuild

* Tue Jun 12 2012 Petr Šabata <contyk@redhat.com> - 1.37-1
- 1.37 bump (sqlite3.7.11 and various bugfixes)
- Drop command macros
- Fix dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Petr Šabata <contyk@redhat.com> - 1.35-1
- 1.35 bump

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-2
- Perl mass rebuild

* Mon May 30 2011 Petr Sabata <contyk@redhat.com> - 1.33-1
- 1.33 bump
- BuildRoot and defattr cleanup
- Dropping the FTS3 tests patch; included upstream

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.31-2
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Petr Sabata <psabata@redhat.com> - 1.31-1
- New release, v1.31
- Significant FTS3 changes -- might break compatibility with pre-1.30 applications using FTS3
- New FTS3 tests patch by Paul Howarth

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 1.29-4
- fix testsuite to run with the latest sqlite (bugs.debian.org/591111)

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 1.29-3
- rebuild

* Mon Jun 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.29-2
- fix description/summary

* Thu Jun 10 2010 Petr Sabata <psabata@redhat.com> - 1.29-1
- Update to the latest release

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-4
- Mass rebuild with perl-5.12.0

* Mon Jan 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.27-3
- 543982 change Makefile.PL to compile with system sqlite

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.27-2
- rebuild against perl 5.10.1

* Wed Nov 25 2009 Stepan Kasal <skasal@redhat.com> 1.27-1
- new upstream version

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.25-4
- Filtering errant private provides

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> 1.25-2
- rebuild against DBI 1.609

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.25-1
- 1.25 needed for DBIx::Class 0.08103
- auto-update to 1.25 (by cpan-spec-update 0.01)
- added a new br on perl(File::Spec) (version 0.82)
- altered br on perl(Test::More) (0 => 0.42)
- added a new br on perl(DBI) (version 1.57)

* Mon Apr 20 2009 Marcela Maslanova <mmaslano@redhat.com> 1.23-1
- update to the latest version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun  2 2008 Marcela Maslanova <mmaslano@redhat.com> 1.14-8

* Wed Mar 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.14-7
- reenable tests

* Tue Mar 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.14-6
- apply sanity patches derived from RT#32100

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-5.1
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.14-4.1
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14-3.1
- tests disabled, due to x86_64 failures

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14-3
- rebuild for new perl

* Wed Dec 19 2007 Steven Pritchard <steve@kspei.com> 1.14-2
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.

* Mon Dec 10 2007 Robin Norwood <rnorwood@redhat.com> - 1.14-1
- Update to latest upstream version: 1.14
- Remove patch - no longer needed.

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-2
- Rebuild for FC6.

* Tue Apr 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Wed Apr  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-4
- Patch to build with system sqlite 3.3.x (#183530).
- Patch to avoid type information segv (#187873).

* Thu Mar  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-3
- DBD::SQLite fails to build with the current FC-5 sqlite version (3.3.3);
  see bugzilla entry #183530.
  Forcing package rebuild with the included version of sqlite (3.2.7).

* Sat Feb 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-2
- Rebuild for FC5 (perl 5.8.8).

* Fri Dec  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Fri Dec  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Fri Jul 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-2
- Build requirement added: sqlite-devel.
- Doc file added: Changes.

* Fri Jul 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.
- This new version can use an external SQLite library (>= 3.1.3).

* Sun Jun 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-2
- temporary maintainership.

* Sat Jun 11 2005 Michael A. Peters <mpeters@mac.com> 1.08-1.1
- minor changes for initial cvs checkin (removed tabs, better url in
- url tag and description tag)

* Tue Apr 12 2005 Michael A. Peters <mpeters@mac.com> 1.08-1
- created initial spec file from Fedora spectemplate-perl.spec
