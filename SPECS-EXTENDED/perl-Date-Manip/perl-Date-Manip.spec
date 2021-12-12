Name:           perl-Date-Manip
Version:        6.82
Release:        2%{?dist}
Summary:        Date manipulation routines
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Date-Manip
Source0:        https://cpan.metacpan.org/authors/id/S/SB/SBECK/Date-Manip-%{version}.tar.gz#/perl-Date-Manip-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
# XXX: BuildRequires:  perl(Cwd)
# XXX: BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
# XXX: BuildRequires:  perl(File::Find)
# XXX: BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Storable)
BuildRequires:  perl(utf8)
# Tests only
BuildRequires:  perl(Test::Inter) >= 1.09
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Cwd)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)

# This package was formerly known as perl-DateManip
Provides: perl-DateManip = %{version}-%{release}
Obsoletes: perl-DateManip < 5.48-1

%{?perl_default_filter}

%description
Date::Manip is a series of modules designed to make any common date/time
operation easy to do. Operations such as comparing two times, determining a
data a given amount of time from another, or parsing international times
are all easily done. It deals with time as it is used in the Gregorian
calendar (the one currently in use) with full support for time changes due
to daylight saving time.

%prep
%setup -q -n Date-Manip-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc README README.first
%{perl_vendorlib}/Date/
%{_mandir}/man[13]/*.[13]*
%{_bindir}/dm_*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.82-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
