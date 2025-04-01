%if 0%{?rhel} >= 9
%bcond_with perl_DateTime_Format_Builder_enable_optional_tests
%else
%bcond_without perl_DateTime_Format_Builder_enable_optional_tests
%endif

%global real_version   0.83

Name:           perl-DateTime-Format-Builder
# 0.83 in reality, but rpm can't get it
Version:        0.8300
Release:        14%{?dist}
Summary:        Create DateTime parser classes and objects        
# examples/W3CDTF.pm:               GPL-1.0-or-later OR Artistic-1.0-Perl
# examples/MySQL.pm:                GPL-1.0-or-later OR Artistic-1.0-Perl
# lib/DateTime/Format/Builder.pm:   Artistic-2.0
# LICENSE:                          Artistic-2.0 text
License:        Artistic-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/release/DateTime-Format-Builder            
Source0:        https://cpan.metacpan.org/modules/by-module/DateTime/DateTime-Format-Builder-%{real_version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  sed
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(DateTime) >= 1.00
BuildRequires:  perl(DateTime::Format::Strptime) >= 1.04
BuildRequires:  perl(Params::Validate) >= 0.72
BuildRequires:  perl(parent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
# Optional Tests
%if %{with perl_DateTime_Format_Builder_enable_optional_tests}
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(DateTime::Format::HTTP)
BuildRequires:  perl(DateTime::Format::Mail)
BuildRequires:  perl(DateTime::Format::IBeat)
BuildRequires:  perl(Devel::Cycle) >= 1.07
BuildRequires:  perl(Test::Memory::Cycle)
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
# Dependencies
Provides:       perl(DateTime::Format::Builder) = %{version}

# Avoid doc-file dependencies from tests
%{?perl_default_filter}

%description
DateTime::Format::Builder creates DateTime parsers. Many string formats of
dates and times are simple and just require a basic regular expression to
extract the relevant information. Builder provides a simple way to do this
without writing reams of structural code.

Builder provides a number of methods, most of which you'll never need, or at
least rarely need. They're provided more for exposing of the module's innards
to any sub-classes, or for when you need to do something slightly beyond what
is expected.

%prep
%setup -q -n DateTime-Format-Builder-%{real_version}

# POD doesn't like E<copy> very much...
perl -pi -e 's/E<copy>/(C)/' `find lib/ -type f`

# Silence rpmlint
sed -i '1s~^#!.*perl~#!%{__perl}~' t/*.t

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CODE_OF_CONDUCT.md CONTRIBUTING.md README.md examples/ t/
%{perl_vendorlib}/DateTime/
%{_mandir}/man3/DateTime::Format::Builder.3*
%{_mandir}/man3/DateTime::Format::Builder::Parser.3*
%{_mandir}/man3/DateTime::Format::Builder::Parser::Dispatch.3*
%{_mandir}/man3/DateTime::Format::Builder::Parser::Quick.3*
%{_mandir}/man3/DateTime::Format::Builder::Parser::Regex.3*
%{_mandir}/man3/DateTime::Format::Builder::Parser::Strptime.3*
%{_mandir}/man3/DateTime::Format::Builder::Parser::generic.3*
%{_mandir}/man3/DateTime::Format::Builder::Tutorial.3*

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Paul Howarth <paul@city-fan.org> - 0.8300-9
- Use SPDX-format license tag
- Use %%license unconditionally

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.8300-7
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.8300-4
- Perl 5.34 rebuild

* Thu Mar 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.8300-3
- Disable optional tests on ELN

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8300-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 10 2020 Paul Howarth <paul@city-fan.org> - 0.8300-1
- Update to 0.83
  - Switched to GitHub issues

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8200-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.8200-6
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8200-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov  1 2019 Paul Howarth <paul@city-fan.org> - 0.8200-4
- Fix License: tag to reflect content of actual shipped files, not just what
  the LICENSE file says (#1600504, CPAN RT#125832)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.8200-2
- Perl 5.30 rebuild

* Mon Mar  4 2019 Paul Howarth <paul@city-fan.org> - 0.8200-1
- Update to 0.82
  - Removed use of Class::Factory::Util, which isn't really needed
- Package new upstream CODE_OF_CONDUCT.md and CONTRIBUTING.md
- Use %%license where possible
- Make %%files list more explicit
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Simplify find command using -delete

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-15
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8100-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-7
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8100-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.8100-3
- Perl 5.18 rebuild

* Fri Apr 05 2013 Iain Arnell <iarnell@gmail.com> 0.8100-2
- license change from "same as perl" to Artistic 2.0

* Fri Apr 05 2013 Iain Arnell <iarnell@gmail.com> 0.8100-1
- update to latest upstream version
- drop dependency filtering

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.8000-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.8000-7
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.8000-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Dec 12 2010 Iain Arnell <iarnell@gmail.com> 0.8000-3
- use perl_default_filter
- clean up spec for modern rpmbuild

* Fri May 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-2
- add provides with rpm version for other packages

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-1
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.7901-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7901-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7901-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.7901-2
- rebuild for new perl

* Sat Jan 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.7901-1
- update to 0.7901
- additional docs
- some spec rework

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-4
- bump for mass rebuild

* Tue Aug 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-3
- bump for release & build, not in that order

* Tue Aug 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-2
- additional br's

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-1
- Initial spec file for F-E
