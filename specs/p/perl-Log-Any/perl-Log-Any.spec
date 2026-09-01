# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Log-Any
Version:        1.718
Release:        1%{?dist}
Summary:        Bringing loggers and listeners together
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Log-Any
Source0:        https://cpan.metacpan.org/authors/id/P/PR/PREACTION/Log-Any-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Devel::StackTrace)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sys::Syslog)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Unix::Syslog)
# Tests only
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Mojo::Exception)
BuildRequires:  perl(Moose::Exception)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Throwable::Error)
Requires:       perl(B)
Requires:       perl(Data::Dumper)

# Log::Any::Adapter* merged into Log::Any in 1.00
Obsoletes:      perl-Log-Any-Adapter < 0.11-7
Provides:       perl-Log-Any-Adapter = %{version}-%{release}%{?dist}

%description
Log::Any allows CPAN modules to safely and efficiently log messages, while
letting the application choose (or decline to choose) a logging mechanism
such as Log::Dispatch or Log::Log4perl.

%prep
%setup -q -n Log-Any-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Log/
%{_mandir}/man3/Log::Any*.3pm*

%changelog
* Mon Jul 28 2025 Xavier Bachelot <xavier@bachelot.org> - 1.718-1
- Update to 1.718 (RHBZ#2371156)
- Clean up specfile

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.717-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.717-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.717-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.717-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.717-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Aug 20 2023 Xavier Bachelot <xavier@bachelot.org> - 1.717-1
- Update to 1.717 (RHBZ#2232636)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.716-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Xavier Bachelot <xavier@bachelot.org> - 1.716-1
- Update to 1.716 (RHBZ#2217660)

* Mon Jun 26 2023 Xavier Bachelot <xavier@bachelot.org> - 1.715-1
- Update to 1.715 (RHBZ#2203876)

* Wed Mar 22 2023 Tim Orling <ticotimo@gmail.com> - 1.714-1
- Update to 1.714 (rhbz 2180101)

* Mon Feb 27 2023 Tim Orling <ticotimo@gmail.com> - 1.713-2
- migrated to SPDX license

* Fri Feb 24 2023 Tim Orling <ticotimo@gmail.com> - 1.713-1
- Update to 1.713 (rhbz 2144909)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.710-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.710-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.710-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.710-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 Tim Orling <ticotimo@gmail.com> - 1.710-1
- Update to 1.710 (rhbz 1989200)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.709-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.709-2
- Perl 5.34 rebuild

* Tue Feb 23 2021 Xavier Bachelot <xavier@bachelot.org> - 1.709-1
- Update to 1.709 (RHBZ#1929916)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.708-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.708-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.708-4
- Perl 5.32 rebuild

* Thu Mar 19 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.708-3
- Specify all dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.708-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Tim Orling <ticotimo@gmail.com> - 1.708-1
- Update to 1.708 (rhbz 1790306)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.707-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.707-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.707-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Aug 04 2018 Tim Orling <ticotimo@gmail.com> - 1.707-1
- Update to 1.707

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.706-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Tim Orling <ticotimo@gmail.com> - 1.706-1
- Update to 1.706

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.705-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.705-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Tim Orling <ticotimo@gmail.com> - 1.705-1
- Update to 1.705

* Tue Dec 19 2017 Tim Orling <ticotimo@gmail.com> - 1.704-1
- Update to 1.704

* Wed Oct 04 2017 Tim Orling <ticotimo@gmail.com> - 1.701-1
- Update to 1.701

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.049-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.049-3
- Perl 5.26 rebuild

* Thu Mar 30 2017 Tim Orling <ticotimo@gmail.com> - 1.049-2
- delete version-control-internal-file caught by rpmlint

* Wed Mar 29 2017 Tim Orling <ticotimo@gmail.com> - 1.049-1
- 1.049 bump (bug #1436460)
- BR perl(Sys::Syslog)
- Tests only BR perl(IPC::Open3) perl(IO::Handle)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.045-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Tim Orling <ticotimo@gmail.com> - 1.045-1
- 1.045 bump, update Source0 URI (author now PREACTION rather than DAGOLDEN)

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.040-2
- Perl 5.24 rebuild

* Thu Feb 25 2016 Petr Šabata <contyk@redhat.com> - 1.040-1
- 1.040 bump, documentation fixes

* Thu Feb 11 2016 Petr Šabata <contyk@redhat.com> - 1.038-4
- 1.038 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.032-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.032-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.032-2
- Perl 5.22 rebuild

* Tue May 26 2015 Petr Šabata <contyk@redhat.com> - 1.032-1
- 1.032 bump

* Mon Jan 05 2015 Petr Šabata <contyk@redhat.com> - 1.03-2
- Obsolete/provide Log::Any::Adapter as it is included in
  this distribution now

* Fri Jan 02 2015 Petr Šabata <contyk@redhat.com> - 1.03-1
- 1.03 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-6
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 17 2014 Paul Howarth <paul@city-fan.org> - 0.15-3
- Bootstrap of EPEL-7 done

* Sun Feb 16 2014 Paul Howarth <paul@city-fan.org> - 0.15-2
- Bootstrap EPEL-7 build

* Mon Oct  7 2013 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Migrate to Dist::Zilla
  - Return false from null adapter is_xxx methods (CPAN RT#64164)
  - Eliminate 'subroutine redefined' warning in case Log::Any::Adapter loaded
    before Log::Any::Test
  - Fix typo in lib/Log/Any/Adapter/Test.pm (CPAN RT#69850)
  - Fix version number in Log/Any.pm
  - Hide 'package Log::Any::Adapter' from PAUSE/Module::Metadata
- If we're not bootstrapping, run the release tests too
- Specify all dependencies
- Package upstream LICENSE file
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands
- Drop redundant provides filter

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.11-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.11-8
- Perl 5.16 rebuild

* Sat Apr 21 2012 Paul Howarth <paul@city-fan.org> - 0.11-7
- BR: perl(base), perl(Data::Dumper), perl(Test::Builder)

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> - 0.11-6
- Add __provides_exclude macro for rpm 4.9

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-5
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-4
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.11-2
- Add %%perl_default_filter.
- Filter out bogus Provides: perl(Log::Any::Adapter).

* Sat Feb 13 2010 Steven Pritchard <steve@kspei.com> 0.11-1
- Specfile autogenerated by cpanspec 1.79.
- Add --skipdeps to Makefile.PL to avoid attempting to download dependencies.
