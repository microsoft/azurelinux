# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Perl-Critic-Lax
Version:        0.014
Release:        8%{?dist}
Summary:        Policies that let you slide on common exceptions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Perl-Critic-Lax
Source0:        https://cpan.metacpan.org/modules/by-module/Perl/Perl-Critic-Lax-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.12
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(parent)
# This is plug-in into Perl::Critic
BuildRequires:  perl(Perl::Critic) >= 1.088
BuildRequires:  perl(Perl::Critic::Policy)
BuildRequires:  perl(Perl::Critic::Policy::ValuesAndExpressions::ProhibitLeadingZeros)
BuildRequires:  perl(Perl::Critic::Utils)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(utf8)
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Perl::Critic::TestUtils)
BuildRequires:  perl(Test::More)
# This is plug-in into Perl::Critic
Requires:       perl(Perl::Critic) >= 1.088
Requires:       perl(Perl::Critic::Policy)

%description
The Perl-Critic-Lax distribution includes versions of core Perl::Critic
modules with built-in exceptions. If you really like a Perl::Critic policy,
but find that you often violate it in a specific way that seems pretty darn
reasonable, maybe there's a Lax policy. If there isn't, send one in!

%prep
%setup -q -n Perl-Critic-Lax-%{version}

%build
perl Makefile.PL INSTALLDIRS=perl
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_privlib}/Perl/
%{_mandir}/man3/Perl::Critic::Lax.3*
%{_mandir}/man3/Perl::Critic::Policy::Lax::ProhibitComplexMappings::LinesNotStatements.3*
%{_mandir}/man3/Perl::Critic::Policy::Lax::ProhibitEmptyQuotes::ExceptAsFallback.3*
%{_mandir}/man3/Perl::Critic::Policy::Lax::ProhibitLeadingZeros::ExceptChmod.3*
%{_mandir}/man3/Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire.3*
%{_mandir}/man3/Perl::Critic::Policy::Lax::RequireConstantOnLeftSideOfEquality::ExceptEq.3*
%{_mandir}/man3/Perl::Critic::Policy::Lax::RequireEndWithTrueConst.3*
%{_mandir}/man3/Perl::Critic::Policy::Lax::RequireExplicitPackage::ExceptForPragmata.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  1 2023 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014 (rhbz#2157212)
  - Update packaging and metadata
  - Minimum required Perl is now v5.12
- Use SPDX-format license tag
- Use author-independent source URL
- Fix permissions verbosely
- Make %%files list more explicit

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-17
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-14
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-11
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-2
- Perl 5.26 rebuild

* Tue Mar 14 2017 Petr Pisar <ppisar@redhat.com> - 0.013-1
- 0.013 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 02 2016 Petr Pisar <ppisar@redhat.com> - 0.012-1
- 0.012 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.011-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-2
- Perl 5.20 rebuild

* Fri Jul 11 2014 Petr Pisar <ppisar@redhat.com> - 0.011-1
- 0.011 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 10 2013 Petr Pisar <ppisar@redhat.com> - 0.010-1
- 0.010 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.009-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 0.009-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 13 2012 Petr Pisar <ppisar@redhat.com> - 0.009-1
- 0.009 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.008-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.008-2
- Perl mass rebuild

* Thu Jan 27 2011 Petr Pisar <ppisar@redhat.com> 0.008-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
- Install into perl core directory
