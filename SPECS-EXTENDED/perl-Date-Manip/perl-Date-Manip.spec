Name:           perl-Date-Manip
Version:        6.95
Release:        3%{?dist}
Summary:        Date manipulation routines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Date-Manip
Source0:        https://cpan.metacpan.org/authors/id/S/SB/SBECK/Date-Manip-%{version}.tar.gz#/perl-Date-Manip-%{version}.tar.gz

BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(:VERSION) >= 5.10.0
BuildRequires:  perl(Carp)
# Cwd not used at tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
# File::Find not used at tests
# File::Spec not used at tests
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Storable)
BuildRequires:  perl(utf8)
# Win32::TieRegistry not used
# Tests only
# File::Basename not used
# File::Find::Rule not used
# lib not used
BuildRequires:  perl(Test::Inter) >= 1.09
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
# Test::Pod 1.00 not used
# Test::Pod::Coverage 1.00 not used
Requires:       perl(Cwd)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)

# This package was formerly known as perl-DateManip
Provides: perl-DateManip = %{version}-%{release}
Obsoletes: perl-DateManip < 5.48-1

%{?perl_default_filter}

# Filter modules bundled for tests
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(tests.pl\\)

%description
Date::Manip is a series of modules designed to make any common date/time
operation easy to do. Operations such as comparing two times, determining
a data a given amount of time from another, or parsing international times
are all easily done. It deals with time as it is used in the Gregorian
calendar (the one currently in use) with full support for time changes due
to daylight saving time.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Date-Manip-%{version}

# Help generators to recognize Perl scripts
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove release tests
rm -f %{buildroot}%{_libexecdir}/%{name}/t/_pod*
rm -f %{buildroot}%{_libexecdir}/%{name}/t/_version.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset DATE_MANIP DATE_MANIP_DEBUG DATE_MANIP_DEBUG_ABBREVS \
    DATE_MANIP_DEBUG_ZONES Date_Manip_RELEASE_TESTING DATE_MANIP_TEST_DM5 \
    OS MULTINET_TIMEZONE 'SYS$TIMEZONE_DIFFERENTIAL' 'SYS$TIMEZONE_NAME' \
    'SYS$TIMEZONE_RULE' 'TCPIP$TZ' 'UCX$TZ'
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset DATE_MANIP DATE_MANIP_DEBUG DATE_MANIP_DEBUG_ABBREVS \
    DATE_MANIP_DEBUG_ZONES Date_Manip_RELEASE_TESTING DATE_MANIP_TEST_DM5 \
    OS MULTINET_TIMEZONE 'SYS$TIMEZONE_DIFFERENTIAL' 'SYS$TIMEZONE_NAME' \
    'SYS$TIMEZONE_RULE' 'TCPIP$TZ' 'UCX$TZ'
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc README README.first
%dir %{perl_vendorlib}/Date
%{perl_vendorlib}/Date/Manip
%{perl_vendorlib}/Date/Manip.{pm,pod}
%{_mandir}/man1/dm_*.1*
%{_mandir}/man3/Date::Manip.3*
%{_mandir}/man3/Date::Manip::*.3*
%{_bindir}/dm_*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Dec 18 2024 Jyoti kanase <v-jykanase@microsoft.com> -  6.95 -3
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 01 2024 Packit <hello@packit.dev> - 6.95-1
- Release: v6.95 (Sullivan Beck)
- Checkpoint: v6.95 (Sullivan Beck)
- Added POSIX handling (Sullivan Beck)
- Initial checkin of next release cycle: 6.95 (Sullivan Beck)
- Resolves rhbz#2267329

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 6.94-1
- 6.94 bump (rhbz#2257491)
- Package tests

* Wed Jan 03 2024 Petr Pisar <ppisar@redhat.com> - 6.93-2
- Adapt test envinronment guard to changes in 6.93
- List files explicitly
- Run tests in parallel

* Sun Dec 03 2023 Packit <hello@packit.dev> - 6.93-1
- Release: v6.93 (Sullivan Beck)
- Checkpoint: v6.93 (Sullivan Beck)
- Remove Travis (Sullivan Beck)
- Initial checkin of next release cycle: 6.93 (Sullivan Beck)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Jan Pazdziora <jpazdziora@redhat.com> - 6.92-1
- 2213282 - Rebase to upstream version 6.92.

* Wed Mar 08 2023 Jan Pazdziora <jpazdziora@redhat.com> - 6.91-1
- 2174484 - Rebase to upstream version 6.91.

* Fri Mar 03 2023 Michal Josef Špaček <mspacek@redhat.com> - 6.90-3
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 10 2022 Jan Pazdziora <jpazdziora@redhat.com> - 6.90-1
- 2150409 - Rebase to upstream version 6.90.

* Wed Sep 21 2022 Jan Pazdziora <jpazdziora@redhat.com> - 6.89-1
- 2123418 - Rebase to upstream version 6.89.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.88-2
- Perl 5.36 re-rebuild updated packages

* Mon Jun 06 2022 Jan Pazdziora <jpazdziora@redhat.com> - 6.88-1
- 2093024 - Rebase to upstream version 6.88.

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.86-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 23 2021 Jan Pazdziora <jpazdziora@redhat.com> - 6.86-1
- 2023516 - Rebase to upstream version 6.86.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 6.85-2
- Perl 5.34 rebuild

* Wed Mar 03 2021 Jan Pazdziora <jpazdziora@redhat.com> - 6.85-1
- 1933868 - Rebase to upstream version 6.85.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.83-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Petr Pisar <ppisar@redhat.com> - 6.83-2
- Specify all dependendencies

* Tue Dec 15 2020 Jan Pazdziora <jpazdziora@redhat.com> - 6.83-1
- 1902872 - Rebase to upstream version 6.83.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.82-2
- Perl 5.32 rebuild

* Mon Jun 08 2020 Jan Pazdziora <jpazdziora@redhat.com> - 6.82-1
- 1842524 - Rebase to upstream version 6.82.

* Mon Apr 27 2020 Jan Pazdziora <jpazdziora@redhat.com> - 6.81-1
- 1827253 - Rebase to upstream version 6.81.

* Tue Mar 03 2020 Jan Pazdziora <jpazdziora@redhat.com> - 6.80-1
- 1809202 - Rebase to upstream version 6.80.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.79-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Pazdziora <jpazdziora@redhat.com> - 6.79-1
- 1778849 - Rebase to upstream version 6.79.

* Mon Sep 02 2019 Jan Pazdziora <jpazdziora@redhat.com> - 6.78-1
- 1747170 - Rebase to upstream version 6.78.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 06 2019 Jan Pazdziora <jpazdziora@redhat.com> - 6.77-1
- 1716417 - Rebase to upstream version 6.77.

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.76-2
- Perl 5.30 rebuild

* Mon Mar 04 2019 Jan Pazdziora <jpazdziora@redhat.com> - 6.76-1
- 1684273 - Rebase to upstream version 6.76.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Jan Pazdziora <jpazdziora@redhat.com> - 6.75-1
- 1656324 - Rebase to upstream version 6.75.

* Mon Sep 10 2018 Jan Pazdziora <jpazdziora@redhat.com> - 6.73-1
- 1624940 - Rebase to upstream version 6.73.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.72-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.72-2
- Perl 5.28 rebuild

* Thu Jun 07 2018 Jan Pazdziora <jpazdziora@redhat.com> - 6.72-1
- 1585345 - Rebase to upstream version 6.72.

* Fri Mar 02 2018 Jan Pazdziora <jpazdziora@redhat.com> - 6.70-1
- 1550748 - Rebase to upstream version 6.70.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 04 2017 Jan Pazdziora <jpazdziora@redhat.com> - 6.60-1
- 1487801 - Rebase to upstream version 6.60.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.59-2
- Perl 5.26 rebuild

* Sat Jun 03 2017 Jan Pazdziora <jpazdziora@redhat.com> - 6.59-1
- 1458071 - Rebase to upstream version 6.59.

* Thu Mar 02 2017 Jan Pazdziora <jpazdziora@redhat.com> - 6.58-1
- 1428184 - Rebase to upstream version 6.58.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Jan Pazdziora <jpazdziora@redhat.com> - 6.57-1
- 1400728 - Rebase to upstream version 6.57.

* Sat Sep 10 2016 Jan Pazdziora <jpazdziora@redhat.com> - 6.56-1
- 1372494 - Rebase to upstream version 6.56.
- 1372494 - Rebase to upstream version 6.55, build failed due to
  https://rt.cpan.org/Public/Bug/Display.html?id=117404.

* Wed Jun 01 2016 Jan Pazdziora <jpazdziora@redhat.com> - 6.54-1
- 1341373 - Rebase to upstream version 6.54.

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.53-2
- Perl 5.24 rebuild

* Thu Mar 03 2016 Petr Šabata <contyk@redhat.com> - 6.53-1
- 6.53 bump
- Various bugfixes
- Timezone data updated

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Petr Šabata <contyk@redhat.com> - 6.52-1
- 6.52 bump
- Holidays reworked slightly
- Timezone data updated

* Wed Sep 02 2015 Petr Šabata <contyk@redhat.com> - 6.51-1
- 6.51 bump, bugfixes and tzdata updates
- This release changes the behavior of Date::Manip::Delta::value which
  now returns an empty string rather than undef, where applicable

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.50-2
- Perl 5.22 rebuild

* Tue Jun 02 2015 Petr Šabata <contyk@redhat.com> - 6.50-1
- 6.50 bump, bugfixes and new tzdata

* Tue Mar 03 2015 Petr Šabata <contyk@redhat.com> - 6.49-1
- 6.49 bugfix bump

* Fri Dec 05 2014 Petr Šabata <contyk@redhat.com> - 6.48-1
- 6.48 bump
- various bugfixes and tzdata updates

* Wed Sep 10 2014 Petr Šabata <contyk@redhat.com> - 6.47-1
- Update timezone data

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.46-2
- Perl 5.20 rebuild

* Fri Jul 11 2014 Petr Pisar <ppisar@redhat.com> - 6.46-1
- 6.46 bump

* Tue Jun 17 2014 Petr Šabata <contyk@redhat.com> - 6.45-1
- 6.45 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Petr Šabata <contyk@redhat.com> - 6.44-1
- 6.44 bump, Unicode support enhancements

* Fri Mar 28 2014 Petr Šabata <contyk@redhat.com> - 6.43-1
- 6.43 bump, no code changes

* Tue Dec 03 2013 Petr Pisar <ppisar@redhat.com> - 6.42-1
- 6.42 bump

* Tue Sep 10 2013 Petr Šabata <contyk@redhat.com> - 6.41-1
- 6.41 bump
- Various bugfixes, new tzdata

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 6.40-3
- Perl 5.18 rebuild

* Tue Jun 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 6.40-2
- Specify all dependencies

* Mon Jun 10 2013 Petr Šabata <contyk@redhat.com> - 6.40-1
- 6.40 bump, TZ updates

* Fri Mar 01 2013 Petr Pisar <ppisar@redhat.com> - 6.39-1
- 6.39 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 6.38-1
- 6.38 bump

* Mon Dec 03 2012 Petr Pisar <ppisar@redhat.com> - 6.37-1
- 6.37 bump

* Thu Nov 01 2012 Petr Šabata <contyk@redhat.com> - 6.36-1
- 6.36 bump

* Wed Sep 12 2012 Jitka Plesnikova <jplesnik@redhat.com> - 6.34-1
- 6.34 bump
- examples are included in man pages and bin directory. Remove them from doc.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 6.32-2
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Šabata <contyk@redhat.com> - 6.32-1
- 6.32 bump
- Remove command macros
- Don't require a specific version of Module::Build

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 6.31-2
- Round Module::Build version to 2 digits

* Wed Mar 14 2012 Marcela Mašláňová <mmaslano@redhat.com> - 6.31-1
- bump to 6.31

* Fri Jan 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 6.30-1
- bump to 6.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 01 2011 Petr Pisar <ppisar@redhat.com> - 6.25-1
- 6.25 bump
- Package examples

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.24-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 6.24-2
- Perl mass rebuild

* Tue Jun 14 2011 Petr Sabata <contyk@redhat.com> - 6.24-1
- 6.24 bump
- defattr removed

* Mon Apr 18 2011 Petr Sabata <psabata@redhat.com> - 6.23-1
- 6.23 bump
- IO::File added to BR
- Buildroot stuff removed

* Tue Mar  8 2011 Petr Sabata <psabata@redhat.com> - 6.22-1
- 6.22 bump, new timezone data

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.21-1
- update to 6.21

* Fri Dec  3 2010 Petr Sabata <psabata@redhat.com> - 6.20-1
- 6.20 bump, internal resources might be incompatible with previous versions

* Wed Oct 27 2010 Petr Pisar <ppisar@redhat.com> - 6.14-1
- 6.14 bump
- Remove double-required perl(YAML::Syck)

* Mon Oct 18 2010 Petr Sabata <psabata@redhat.com> - 6.13-1
- 6.13 bump

* Mon Oct  4 2010 Petr Sabata <psabata@redhat.com> - 6.12-1
- 6.12 bump

* Tue Sep 14 2010 Petr Pisar <ppisar@redhat.com> - 6.11-1
- 6.11 bump

* Tue Apr 27 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.07-3
- Mass rebuild with perl-5.12.0

* Fri Apr 16 2010 Marcela Mašláňová <mmaslano@redhat.com> - 6.07-1
- update

* Mon Feb  1 2010 Marcela Mašláňová <mmaslano@redhat.com> - 6.05-1
- update, remove patch (tested functionality without it)

* Wed Jan 13 2010 Marcela Mašláňová <mmaslano@redhat.com> - 5.54-5
- add license into doc and fix rpmlint warnings

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.54-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Stepan Kasal <skasal@redhat.com> - 5.54-1
- new upstream version
- add BuildRequires so that testsuite can be fully executed

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.48-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.48-2
- rebuild for new perl

* Thu Jan  3 2008 Ed Avis <eda@waniasset.com> - 5.48-1
- Update to 5.48.
- rhbz#214709 Krasnoyarsk patch now upstream.
- Changed name to Date-Manip as now used on CPAN.

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 5.44-4
- Apply patch to use date +%%z as possible source for timezone data
- Fix license tag
- Add TODO and HISTORY to %%doc list

* Tue Mar 20 2007 Robin Norwood <rnorwood@redhat.com> - 5.44-3
- Fix minor issues in spec file for package review
- Bump release
- Resolves: rhbz#226250

* Fri Nov 10 2006 Robin Norwood <rnorwood@redhat.com> - 5.44-2
- Add support for KRAT and KRAST timezones
- Include magic dist tag in release
- Resolves: rhbz#214709
- Related: rhbz#100786

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.44-1.3
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.44-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.44-1
- Update to 5.44.

* Mon Apr 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.42a-4
- Bring up to date with current Fedora.Extras perl spec template. (#155913)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 5.42a-2
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 5.42a-1
- update to 5.42a

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated.
