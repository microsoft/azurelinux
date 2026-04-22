# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Getopt-Long-Descriptive
Summary:        Getopt::Long with usage text
Version:        0.116
Release: 4%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Getopt-Long-Descriptive
Source0:        https://cpan.metacpan.org/modules/by-module/Getopt/Getopt-Long-Descriptive-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.12
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Getopt::Long) >= 2.55
BuildRequires:  perl(List::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(Params::Validate) >= 0.97
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Exporter) >= 0.972
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(CPAN::Meta::Check) >= 0.011
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Warnings) >= 0.005
# Optional tests:
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(Moose::Conflicts)
# Dependencies
# (none)

%description
Convenient wrapper for Getopt::Long and program usage output.

%prep
%setup -q -n Getopt-Long-Descriptive-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes eg/ README
%{perl_vendorlib}/Getopt/
%{_mandir}/man3/Getopt::Long::Descriptive.3*
%{_mandir}/man3/Getopt::Long::Descriptive::Opts.3*
%{_mandir}/man3/Getopt::Long::Descriptive::Usage.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.116-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 31 2024 Paul Howarth <paul@city-fan.org> - 0.116-1
- Update to 0.116 (rhbz#2335016)
  - Do not leave Getopt::Long configuration in an altered state after getting
    options

* Fri Nov  8 2024 Paul Howarth <paul@city-fan.org> - 0.115-1
- Update to 0.115 (rhbz#2324463)
  - Cope with the user forgetting the first argument, generally "%%c %%o", to
    'describe_options', by assuming they meant that value exactly

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Paul Howarth <paul@city-fan.org> - 0.114-1
- Update to 0.114 (rhbz#2259379)
  - A switch with (required => 0) is no longer treated as required!

* Sun Dec 17 2023 Paul Howarth <paul@city-fan.org> - 0.113-1
- Update to 0.113 (rhbz#2254783)
  - Improve line wrapping so spacers (non-option text lines) can use more
    horizontal characters
  - Replace tabs (generally 8 space) indents in output with four spaces
- Package examples as documentation

* Tue Nov 21 2023 Paul Howarth <paul@city-fan.org> - 0.112-1
- Update to 0.112 (rhbz#2250751)
  - This version removes the redundant option warning, which is now provided by
    Getopt::Long v2.55 and later (which is now required); as before, this will
    someday become fatal

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.111-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.111-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  1 2023 Paul Howarth <paul@city-fan.org> - 0.111-1
- Update to 0.111
  - Clean up the required perl version in the code
  - Update author contact info
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 31 2021 Paul Howarth <paul@city-fan.org> - 0.110-1
- Update to 0.110
  - Just small packaging updates
  - ...and bumped the minimum perl to v5.12 (inadvertently)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.109-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.109-2
- Perl 5.34 rebuild

* Wed Mar 17 2021 Paul Howarth <paul@city-fan.org> - 0.109-1
- Update to 0.109
  - Eliminate warnings-count failure by requiring an ExtUtils::MakeMaker from
    late 2013 or later; without this, very old EUMM could pass -w to the tests,
    enabling more warnings than we wanted
- Use %%{make_build} and %%{make_install}

* Tue Mar 16 2021 Paul Howarth <paul@city-fan.org> - 0.108-1
- Update to 0.108
  - Provide diagnostics in tests when more warnings arrive than are expected

* Mon Mar 15 2021 Paul Howarth <paul@city-fan.org> - 0.107-1
- Update to 0.107
  - Term::ReadKey has been dropped; caused too many problems
  - Minimum version is now v5.10.1, not v5.10.0
- Don't need to use expect for the test suite any longer

* Sat Mar 13 2021 Paul Howarth <paul@city-fan.org> - 0.106-1
- Update to 0.106
  - Improved formatting of switches
  - When available, use Term::ReadKey to get terminal width
  - When an option name is defined twice, warn about it (this will become fatal
    in a future version)
- Run the test suite using expect so as to make a pty available

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.105-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.105-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.105-2
- Perl 5.32 rebuild

* Wed Feb 26 2020 Paul Howarth <paul@city-fan.org> - 0.105-1
- Update to 0.105
  - one_of sub-options now get accessors

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.104-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.104-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.104-2
- Perl 5.30 rebuild

* Sun Apr 28 2019 Paul Howarth <paul@city-fan.org> - 0.104-1
- Update to 0.104
  - Allow for verbatim text in description options

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.103-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.103-1
- Update to 0.103
  - Show --[no-]option for boolean toggle options

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.102-2
- Perl 5.28 rebuild

* Wed Feb 21 2018 Paul Howarth <paul@city-fan.org> - 0.102-1
- Update to 0.102
  - Long spacer lines are now line broken
  - "Empty" spacer lines no longer have leading whitespace
  - Option specifications ":+" and ":5" (etc.) now get better presentation in
    the usage description

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Paul Howarth <paul@city-fan.org> - 0.101-1
- Update to 0.101
  - Escape some unescaped braces in regex
- Drop legacy Group: tag

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.100-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Paul Howarth <paul@city-fan.org> - 0.100-1
- Update to 0.100
  - Show off "shortcircuit" in synopsis
  - Fix rendering of complex types ('i@' → 'INT...', etc.)
- Simplify find command using -delete
- Make %%files list more explicit
- Drop redundant %%{?perl_default_filter}

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.099-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.099-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.099-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.099-2
- Perl 5.22 rebuild

* Tue Feb 03 2015 Petr Pisar <ppisar@redhat.com> - 0.099-1
- 0.099 bump

* Thu Dec 04 2014 Petr Pisar <ppisar@redhat.com> - 0.098-1
- 0.098 bump
- Stop providing dummy tests sub-package symbol

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.093-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.093-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.093-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.093-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.093-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Iain Arnell <iarnell@gmail.com> 0.093-1
- update to latest upstream version

* Fri Aug 03 2012 Iain Arnell <iarnell@gmail.com> 0.092-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.091-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.091-2
- Perl 5.16 rebuild

* Thu Feb 23 2012 Iain Arnell <iarnell@gmail.com> 0.091-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.090-4
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.090-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.090-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.090-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.087-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 0.087-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.084-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.084-2
- Mass rebuild with perl-5.12.0

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.084-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(Getopt::Long) (version 2.33)
- dropped old BR on perl(IO::Scalar)
- dropped old BR on perl(Test::Pod::Coverage)
- added a new req on perl(Getopt::Long) (version 2.33)
- dropped old requires on perl(IO::Scalar)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.077-2
- rebuild against perl 5.10.1

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.077-1
- auto-update to 0.077 (by cpan-spec-update 0.01)
- added a new br on perl(List::Util) (version 0)
- added a new br on perl(Sub::Exporter) (version 0)
- added a new req on perl(List::Util) (version 0)
- added a new req on perl(Params::Validate) (version 0.74)
- added a new req on perl(Sub::Exporter) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.074-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.074-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.074-2
- bump

* Tue Jul 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.074-1
- Specfile autogenerated by cpanspec 1.74.
