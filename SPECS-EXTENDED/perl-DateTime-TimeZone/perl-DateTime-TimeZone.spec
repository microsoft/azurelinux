# Run optional test
%bcond_without perl_DateTime_TimeZone_enables_optional_test

# Regenerate Perl library code from upstream Olson database of this date
%global tzversion 2020a

Name:           perl-DateTime-TimeZone
Version:        2.39
Release:        2%{?dist}
Summary:        Time zone object base class and factory
# tzdata%%{tzversion}.tar.gz archive:   Public Domain
# other files:                          GPL+ or Artistic
# Some other files are generated from tzdata%%{tzversion}.tar.gz content by
# upstream or locally:                  Public Domain
License:        (GPL+ or Artistic) and Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/DateTime-TimeZone
Source0:        https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-TimeZone-%{version}.tar.gz
%if %{defined tzversion}
Source1:        ftp://ftp.iana.org/tz/releases/tzdata%{tzversion}.tar.gz
%endif
# Parse local time zone definition from /etc/localtime as before giving up,
# bug #1135981, CPAN RT#55029
Patch0:         DateTime-TimeZone-2.04-Parse-etc-localtime-by-DateTime-TimeZone-Tzfile.patch
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%if !%{defined perl_bootstrap} && %{defined tzversion}
# Avoid circular dependencies - perl-DateTime strictly requires DateTime::TimeZone
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(integer)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Locale::Country) >= 3.11
BuildRequires:  perl(Parallel::ForkManager)
BuildRequires:  sed
%endif
# Runtime
BuildRequires:  perl(Class::Singleton) >= 1.03
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd) >= 3
%if !%{defined perl_bootstrap}
BuildRequires:  perl(DateTime::Duration)
%endif
# Unused BuildRequires:  perl(DateTime::TimeZone::Tzfile)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Params::ValidationCompiler) >= 0.13
BuildRequires:  perl(parent)
BuildRequires:  perl(Specio::Library::Builtins)
BuildRequires:  perl(Specio::Library::String)
BuildRequires:  perl(Try::Tiny)
# Tests only
BuildRequires:  perl(base)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(Test::Fatal)
# Test::Mojibake not used
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Requires)
%if %{with perl_DateTime_TimeZone_enables_optional_test}
# Optional tests
%if !%{defined perl_bootstrap}
BuildRequires:  perl(DateTime) >= 0.1501
%endif
BuildRequires:  perl(Test::Output)
BuildRequires:  perl(Test::Taint)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(File::Basename)
Requires:       perl(File::Compare)
Requires:       perl(File::Find)
# Require optional DateTime::TimeZone::Tzfile to work in mock after tzdata
# upgrade, bug #1135981
Requires:       perl(DateTime::TimeZone::Tzfile)
%if !%{defined perl_bootstrap} && %{defined tzversion}
Provides:       bundled(tzdata) = %{tzversion}
%else
Provides:       bundled(tzdata)
%endif

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Class::Singleton\\)$

# Avoid circular dependencies - perl-DateTime strictly requires DateTime::TimeZone
%if 0%{?perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(DateTime::Duration\\)
%endif

%description
This class is the base class for all time zone objects. A time zone is
represented internally as a set of observances, each of which describes the
offset from GMT for a given time period.

%prep
%if !%{defined perl_bootstrap} && %{defined tzversion}
%setup -q -T -a 1 -c -n tzdata-%{tzversion}
%endif
%setup -q -T -b 0 -n DateTime-TimeZone-%{version}
%patch0 -p1

%build
%if !%{defined perl_bootstrap} && %{defined tzversion}
JOBS=$(printf '%%s' "%{?_smp_mflags}" | sed 's/.*-j\([0-9][0-9]*\).*/\1/')
perl tools/parse_olson --dir ../tzdata-%{tzversion} --version %{tzversion} \
    --jobs $JOBS --clean
%endif
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.39-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Apr 27 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.39-1
- 2.39 bump (2020a Olson database)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-1
- 2.38 bump

* Thu Sep 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.37-1
- 2.37 bump (2019c Olson database)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-1
- 2.36 bump

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.35-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.35-2
- Perl 5.30 rebuild

* Tue Apr 23 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.35-1
- 2.35 bump

* Wed Mar 27 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-1
- 2.34 bump (2019a Olson database)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-1
- 2.23 bump (2018i Olson database)

* Mon Oct 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.21-1
- 2.21 bump (2018g Olson database)

* Fri Oct 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-1
- 2.20 bump (2018f Olson database)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.19-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.19-2
- Perl 5.28 rebuild

* Mon May 14 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.19-1
- 2.19 bump (2018e Olson database)

* Mon Mar 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-1
- 2.18 bump (2018d Olson database)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.17-1
- 2.17 bump (2018c Olson database)

* Mon Jan 22 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-1
- 2.16 bump (2018b Olson database)

* Mon Nov 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.15-1
- 2.15 bump

* Mon Oct 30 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.14-1
- 2.14 bump (2017c Olson database)

* Mon Aug 14 2017 Petr Pisar <ppisar@redhat.com> - 2.13-6
- Adjust to rpm-build-4.13.90

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Petr Pisar <ppisar@redhat.com> - 2.13-4
- Specify all dependencies
- Regenerate Perl code from timezone sources (bug #1101251)

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.13-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.13-2
- Perl 5.26 rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.13-1
- 2.13 bump

* Wed Mar 22 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-1
- 2.11 bump (2017b Olson database)

* Thu Mar 02 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-1
- 2.10 bump (2017a Olson database)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-1
- 2.09 bump

* Mon Nov 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.08-1
- 2.08 bump

* Thu Nov 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.07-1
- 2.07 bump (2016i Olson database)

* Fri Oct 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.06-1
- 2.06 bump (2016h Olson database)

* Thu Oct 06 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-2
- Add BR perl(DateTime) to run more tests

* Fri Sep 30 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-1
- 2.05 bump (2016g Olson database)

* Tue Sep 27 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-1
- 2.04 bump

* Mon Jul 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.01-1
- 2.01 bump (2016f Olson database)

* Thu Jun 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-1
- 2.00 bump

* Tue Jun 07 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.99-1
- 1.99 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.98-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.98-2
- Perl 5.24 rebuild

* Fri Apr 22 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.98-1
- 1.98 bump (2016d Olson database)

* Thu Mar 24 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.97-1
- 1.97 bump (2016c Olson database)

* Wed Mar 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.96-1
- 1.96 bump (2016b Olson database)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Petr Šabata <contyk@redhat.com> - 1.95-1
- 1.95 bump (2016a Olson database)

* Thu Oct 22 2015 Petr Pisar <ppisar@redhat.com> - 1.94-1
- 1.94 bump (2015g Olson database)

* Wed Aug 12 2015 Petr Šabata <contyk@redhat.com> - 1.93-1
- 1.93 bump, tzdata updated

* Tue Jun 23 2015 Petr Šabata <contyk@redhat.com> - 1.92-1
- 1.92 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Petr Šabata <contyk@redhat.com> - 1.91-1
- 1,91 bump, tzdata updated

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.90-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.90-2
- Perl 5.22 rebuild

* Fri May 15 2015 Petr Šabata <contyk@redhat.com> - 1.90-1
- 1.90 bump
- The `compile-all' test is now author-only, cutting the dep list somewhat
- Drop the old filters; I don't think we need them anymore

* Mon Apr 27 2015 Petr Šabata <contyk@redhat.com> - 1.88-1
- 1.88 bump, timezone data updated

* Tue Apr 21 2015 Petr Šabata <contyk@redhat.com> - 1.87-1
- 1.87 bump, timezone data updated

* Mon Mar 23 2015 Petr Šabata <contyk@redhat.com> - 1.86-1
- 1.86 bump, timezone data updated

* Tue Feb 03 2015 Petr Pisar <ppisar@redhat.com> - 1.85-1
- 1.85 bump

* Thu Jan 29 2015 Petr Pisar <ppisar@redhat.com> - 1.83-3
- Rebase patch to remove a spurious back-up file

* Fri Jan 16 2015 Petr Pisar <ppisar@redhat.com> - 1.83-2
- Fix dependency filtering

* Wed Jan 07 2015 Petr Šabata <contyk@redhat.com> - 1.83-1
- 1.83 bump, tests enhanced for 5.21
- Dropping F16-era conflicts

* Tue Nov 25 2014 Petr Šabata <contyk@redhat.com> - 1.81-1
- 1.81 bump, only removes Win32 tests

* Tue Nov 18 2014 Petr Šabata <contyk@redhat.com> - 1.80-1
- 1.80 bump, based on version 2014j of the Olson database

* Mon Nov 03 2014 Petr Pisar <ppisar@redhat.com> - 1.76-1
- 1.76 bump

* Wed Oct 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.75-1
- 1.75 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.74-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.74-3
- Perl 5.20 rebuild

* Tue Sep 02 2014 Petr Pisar <ppisar@redhat.com> - 1.74-2
- Parse local time zone definition from /etc/localtime (bug #1135981)

* Tue Sep 02 2014 Petr Pisar <ppisar@redhat.com> - 1.74-1
- 1.74 bump (updates to 2014g Olson database)

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.73-2
- Perl 5.20 rebuild

* Thu Aug 07 2014 Petr Pisar <ppisar@redhat.com> - 1.73-1
- 1.73 bump

* Mon Jun 30 2014 Petr Pisar <ppisar@redhat.com> - 1.71-1
- update to latest upstream version - Olson 2014e

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Petr Pisar <ppisar@redhat.com> - 1.69-1
- update to latest upstream version - IANA 2014c database

* Mon Feb 10 2014 Paul Howarth <paul@city-fan.org> - 1.64-1
- Update to 1.64
  - Under taint mode, DateTime::TimeZone->new( name => 'local' ) could die
    depending on the method used to find the local time zone name, and the
    resulting variable would often be tainted; we now untaint all names before
    attempting to load them (CPAN RT#92631)

* Tue Oct 29 2013 Petr Pisar <ppisar@redhat.com> - 1.63-1
- update to latest upstream version - Olson 2013h

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-2
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 10 2013 Iain Arnell <iarnell@gmail.com> 1.60-1
- update to latest upstream version - Olson 2013d

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.59-3
- Perl 5.18 rebuild

* Wed Jun 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.59-2
- Specify all dependencies

* Mon Apr 22 2013 Iain Arnell <iarnell@gmail.com> 1.59-1
- update to latest upstream version - Olson 2013c

* Wed Mar 20 2013 Iain Arnell <iarnell@gmail.com> 1.58-1
- update to latest upstream version - Olson 2013b

* Sun Mar 03 2013 Iain Arnell <iarnell@gmail.com> 1.57-1
- update to latest upstream version - Olson 2013a

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Iain Arnell <iarnell@gmail.com> 1.56-1
- update to latest upstream version - still Olson 2012j

* Thu Nov 15 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.54-2
- add BR, filter duplicated requires

* Tue Nov 13 2012 Petr Pisar <ppisar@redhat.com> - 1.54-1
- update to latest upstream version - Olson 2012j

* Fri Nov 02 2012 Iain Arnell <iarnell@gmail.com> 1.52-1
- update to latest upstream version - Olson 2012h

* Thu Oct 18 2012 Petr Pisar <ppisar@redhat.com> - 1.51-1
- update to latest upstream version - Olson 2012g

* Sat Sep 15 2012 Iain Arnell <iarnell@gmail.com> 1.49-1
- update to latest upstream version - Olson 2012f

* Fri Aug 03 2012 Iain Arnell <iarnell@gmail.com> 1.48-1
- update to latest upstream version - Olson 2012e

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 1.47-1
- update to latest upstream version - Olson 2012d

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.46-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.46-2
- Perl 5.16 rebuild

* Tue Apr 03 2012 Iain Arnell <iarnell@gmail.com> 1.46-1
- update to latest upstream - Olson 2012c

* Sun Mar 04 2012 Iain Arnell <iarnell@gmail.com> 1.45-1
- update to latest upstream version

* Fri Mar 02 2012 Iain Arnell <iarnell@gmail.com> 1.44-1
- update to latest upstream version - Olson 2012b

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Iain Arnell <iarnell@gmail.com> 1.42-1
- update to latest upstream - Olson 2011n

* Tue Oct 25 2011 Iain Arnell <iarnell@gmail.com> 1.41-1
- update to latest upstream - Olson 2011m

* Tue Oct 11 2011 Iain Arnell <iarnell@gmail.com> 1.40-1
- update to latest upstream - Olson 2011l

* Tue Sep 27 2011 Iain Arnell <iarnell@gmail.com> 1.39-1
- update to latest upstream - Olson 2011k

* Wed Sep 14 2011 Iain Arnell <iarnell@gmail.com> 1.37-1
- update to latest upstream - Olson 2011j

* Tue Aug 30 2011 Iain Arnell <iarnell@gmail.com> 1.36-1
- update to latest upstream - Olson 2011i

* Thu Aug 18 2011 Iain Arnell <iarnell@gmail.com> 1.35-3
- rebuild against unbunled perl-DateTime

* Mon Aug 15 2011 Iain Arnell <iarnell@gmail.com> 1.35-2
- additional explicit (build)requires for core modules

* Mon Aug 15 2011 Iain Arnell <iarnell@gmail.com> 1.35-1
- Specfile autogenerated by cpanspec 1.78.
- Add bootstrapping logic
