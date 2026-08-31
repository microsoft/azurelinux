# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       perl-Text-CSV
Version:    2.06
Release:    1%{?dist}
Summary:    Comma-separated values manipulator
License:    GPL-1.0-or-later OR Artistic-1.0-Perl
URL:        https://metacpan.org/release/Text-CSV
Source0:    https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/Text-CSV-%{version}.tar.gz
BuildArch:  noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(lib)
# Run-time:
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
# Encode not used
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test:
BuildRequires:  perl(base)
BuildRequires:  perl(charnames)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(warnings)
# Text::CSV_XS not used
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(IO::Handle)
Suggests:       perl(Text::CSV_XS) >= 1.59

%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values.  An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

The module accepts either strings or files as input and can utilize any
user-specified characters as delimiters, separators, and escapes so it is
perhaps better called ASV (anything separated values) rather than just CSV.

%prep
%setup -q -n Text-CSV-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%check
make test TEST_VERBOSE=1

%install
%{make_install}
%{_fixperms} %{buildroot}

%files
%doc Changes README.md
%{perl_vendorlib}/Text*
%{_mandir}/man3/Text::CSV*.3*

%changelog
* Wed Aug 20 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.06-1
- 2.06 bump (rhbz#2349284)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 20 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-1
- 2.04 bump (rhbz#2252556)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.03-1
- 2.03 bump (rhbz#2231263)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-1
- 2.02 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.01-4
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.01-1
- 2.01 bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-4
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 06 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-1
- 2.00 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.99-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.99-1
- 1.99 bump

* Wed Aug 22 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.97-1
- 1.97 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.95-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.95-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.95-2
- Perl 5.26 rebuild

* Wed May 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.95-1
- 1.95 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.91-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Johan Vromans <jvromans@squirrel.nl> - 1.91-4
- Upgrade to upstream 1.91.

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 24 2015 Petr Pisar <ppisar@redhat.com> - 1.33-1
- 1.33 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-6
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.30-2
- Perl 5.18 rebuild

* Tue Jun 11 2013 Johan Vromans <jvromans@squirrel.nl> 1.30-1
- Upgrade to upstream 1.30.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 08 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-6
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.21-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.21-2
- Perl mass rebuild

* Tue Apr 05 2011 Johan Vromans <jvromans@squirrel.nl> 1.21-1
- Upgrade to upstream 1.21.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.18-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul  1 2010 Johan Vromans - 1.18-1
- Upgrade to upstream 1.18.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.16-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.16-1
- PERL_INSTALL_ROOT => DESTDIR, add perl_default_filter
- auto-update to 1.16 (by cpan-spec-update 0.01) (for DBIx::Class)
- added a new br on perl(Test::Harness) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.10-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jan 31 2009 Johan Vromans <jvromans@squirrel.nl> 1.10-1
- Initial Fedora RPM version
