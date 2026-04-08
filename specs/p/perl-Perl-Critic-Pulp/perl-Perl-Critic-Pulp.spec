# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Perl-Critic-Pulp
Version:        100
Release:        1%{?dist}
Summary:        Some add-on perlcritic policies
License:        GPL-3.0-or-later
URL:            https://metacpan.org/release/Perl-Critic-Pulp
Source0:        https://cpan.metacpan.org/authors/id/K/KR/KRYDE/Perl-Critic-Pulp-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
# Scripts in ./devel and ./xtools are not executed.
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::String) >= 1.02
BuildRequires:  perl(List::MoreUtils) >= 0.24
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Perl::Critic) >= 1.084
BuildRequires:  perl(Perl::Critic::Policy) >= 1.084
BuildRequires:  perl(Perl::Critic::Utils) >= 1.100
BuildRequires:  perl(Perl::Critic::Utils::PPI)
BuildRequires:  perl(Perl::Critic::Violation)
BuildRequires:  perl(Pod::Escapes)
BuildRequires:  perl(Pod::MinimumVersion) >= 50
BuildRequires:  perl(Pod::ParseLink)
BuildRequires:  perl(Pod::Parser)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(PPI) >= 1.220
BuildRequires:  perl(PPI::Document)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
# Tests only:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(lib)
BuildRequires:  perl(PPI::Dumper)
BuildRequires:  perl(Test::More)
# Optional tests only:
# Devel::FindRef not needed
# Devel::StackTrace not needed
BuildRequires:  perl(Perl::MinimumVersion)
Requires:       perl(IO::String) >= 1.02
Requires:       perl(List::MoreUtils) >= 0.24
Requires:       perl(Perl::Critic) >= 1.084
Requires:       perl(Pod::MinimumVersion) >= 50
Requires:       perl(PPI::Document)
# This is plug-in into Test::More. Depend on it even if not mentioned in the
# code.
Requires:       perl(Test::More)

# Filter underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(List::MoreUtils\\)\\s*$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::Policy\\)\\s*$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::Utils\\)\\s*$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::Utils\\) >= 0\\.21$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::PodParser::ProhibitVerbatimMarkup\\)\\s*$
# Filter private redefinitions
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Perl::MinimumVersion\\)\\s*$
# Filter private parsers 
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::PodParser::ProhibitVerbatimMarkup\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Policy::Documentation::ProhibitAdjacentLinks::Parser\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodMinimumVersionViolation\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitBadAproposMarkup\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitLinkToSelf\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitParagraphTwoDots\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitUnbalancedParens\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::RequireLinkedURLs\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::ProhibitDuplicateHashKeys::Qword\\)\\s*$
# Filter parsed, but never executed code in the tests
%global __requires_exclude %__requires_exclude|perl\\(constant\\) >= 1\.
%global __requires_exclude %__requires_exclude|perl\\(:VERSION\\) >= 5\.10\.0$
# Filter private modules in the tests
%global __requires_exclude %__requires_exclude|perl\\(MyTestHelpers\\)
%global __provides_exclude %__provides_exclude|perl\\(MyTestHelpers\\)

%description
This is a collection of add-on policies for Perl::Critic.  They're under
a "pulp" theme plus other themes according to their purpose (see "POLICY
THEMES" in Perl::Critic).

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Data::Dumper)
Requires:       perl(PPI::Dumper)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Perl-Critic-Pulp-%{version}
chmod +x t/*.t t/ProhibitModuleShebang/Script.pl

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license COPYING
%doc Changes README
%{perl_vendorlib}/Perl/
%{_mandir}/man3/Perl::Critic::Policy::CodeLayout::ProhibitFatCommaNewline.3*
%{_mandir}/man3/Perl::Critic::Policy::CodeLayout::ProhibitIfIfSameLine.3*
%{_mandir}/man3/Perl::Critic::Policy::CodeLayout::RequireFinalSemicolon.3*
%{_mandir}/man3/Perl::Critic::Policy::CodeLayout::RequireTrailingCommaAtNewline.3*
%{_mandir}/man3/Perl::Critic::Policy::Compatibility::ConstantLeadingUnderscore.3*
%{_mandir}/man3/Perl::Critic::Policy::Compatibility::ConstantPragmaHash.3*
%{_mandir}/man3/Perl::Critic::Policy::Compatibility::Gtk2Constants.3*
%{_mandir}/man3/Perl::Critic::Policy::Compatibility::PerlMinimumVersionAndWhy.3*
%{_mandir}/man3/Perl::Critic::Policy::Compatibility::PodMinimumVersion.3*
%{_mandir}/man3/Perl::Critic::Policy::Compatibility::ProhibitUnixDevNull.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitAdjacentLinks.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitBadAproposMarkup.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitDuplicateHeadings.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitDuplicateSeeAlso.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitLinkToSelf.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitParagraphEndComma.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitParagraphTwoDots.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitUnbalancedParens.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::ProhibitVerbatimMarkup.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::RequireEndBeforeLastPod.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::RequireFilenameMarkup.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::RequireFinalCut.3*
%{_mandir}/man3/Perl::Critic::Policy::Documentation::RequireLinkedURLs.3*
%{_mandir}/man3/Perl::Critic::Policy::Miscellanea::TextDomainPlaceholders.3*
%{_mandir}/man3/Perl::Critic::Policy::Miscellanea::TextDomainUnused.3*
%{_mandir}/man3/Perl::Critic::Policy::Modules::ProhibitModuleShebang.3*
%{_mandir}/man3/Perl::Critic::Policy::Modules::ProhibitPOSIXimport.3*
%{_mandir}/man3/Perl::Critic::Policy::Modules::ProhibitUseQuotedVersion.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ConstantBeforeLt.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::NotWithCompare.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ProhibitArrayAssignAref.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ProhibitBarewordDoubleColon.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ProhibitDuplicateHashKeys.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ProhibitEmptyCommas.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ProhibitFiletest_f.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ProhibitNullStatements.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::ProhibitUnknownBackslash.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::RequireNumericVersion.3*
%{_mandir}/man3/Perl::Critic::Policy::ValuesAndExpressions::UnexpandedSpecialLiteral.3*
%{_mandir}/man3/Perl::Critic::Pulp.3*
%{_mandir}/man3/Perl::Critic::Pulp::PodParser.3*
%{_mandir}/man3/Perl::Critic::Pulp::Utils.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Oct 13 2025 Paul Howarth <paul@city-fan.org> - 100-1
- Update to 100 (rhbz#2403443)
  - ProhibitUnknownBackslash allow \F new in Perl 5.16
- Install to vendor directories
- Fix permissions verbosely
- Make %%files list more explicit

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 99-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 99-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 99-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 99-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 99-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 99-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 99-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 99-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 99-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 99-2
- Perl 5.34 rebuild

* Mon Mar 01 2021 Petr Pisar <ppisar@redhat.com> - 99-1
- 99 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 97-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 97-4
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 04 2019 Petr Pisar <ppisar@redhat.com> - 97-2
- Modernize a spec file

* Mon Oct 21 2019 Jitka Plesnikova <jplesnik@redhat.com> - 97-1
- 97 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 96-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 96-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 96-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 96-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 Petr Pisar <ppisar@redhat.com> - 96-1
- 96 bump

* Thu Oct 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 95-1
- 95 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Petr Pisar <ppisar@redhat.com> - 94-1
- 94 bump

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 93-2
- Perl 5.26 rebuild

* Tue Apr 18 2017 Petr Pisar <ppisar@redhat.com> - 93-1
- 93 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Petr Pisar <ppisar@redhat.com> - 92-1
- 92 bump

* Fri Nov 25 2016 Petr Pisar <ppisar@redhat.com> - 91-1
- 91 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 90-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 90-2
- Perl 5.22 rebuild

* Mon Mar 09 2015 Petr Pisar <ppisar@redhat.com> - 90-1
- 90 version bump

* Mon Jan 05 2015 Petr Pisar <ppisar@redhat.com> - 89-1
- 89 version bump

* Tue Nov 25 2014 Petr Pisar <ppisar@redhat.com> - 88-1
- 88 version bump

* Fri Nov 21 2014 Petr Pisar <ppisar@redhat.com> - 87-1
- 87 version bump

* Tue Nov 18 2014 Petr Pisar <ppisar@redhat.com> - 86-1
- 86 version bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 85-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Petr Pisar <ppisar@redhat.com> - 85-1
- 85 version bump

* Wed May 07 2014 Petr Pisar <ppisar@redhat.com> - 84-1
- 84 version bump

* Wed May 07 2014 Petr Pisar <ppisar@redhat.com> - 83-1
- 83 version bump

* Mon Apr 28 2014 Petr Pisar <ppisar@redhat.com> - 82-1
- 82 version bump

* Fri Apr 04 2014 Petr Pisar <ppisar@redhat.com> - 81-1
- 81 version bump

* Thu Apr 03 2014 Petr Pisar <ppisar@redhat.com> - 80-2
- Restore compatibility with version-0.9907 (#1083991)

* Tue Aug 06 2013 Petr Pisar <ppisar@redhat.com> - 80-1
- 80 version bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 79-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 79-2
- Perl 5.18 rebuild

* Wed Mar 20 2013 Petr Pisar <ppisar@redhat.com> - 79-1
- 79 bump

* Mon Mar 18 2013 Petr Pisar <ppisar@redhat.com> - 78-1
- 78 bump

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 77-1
- 77 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Petr Pisar <ppisar@redhat.com> - 76-1
- 76 bump

* Mon Nov 26 2012 Petr Pisar <ppisar@redhat.com> - 75-1
- 75 bump

* Mon Oct 29 2012 Petr Pisar <ppisar@redhat.com> - 74-1
- 74 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Petr Pisar <ppisar@redhat.com> - 73-2
- Perl 5.16 rebuild

* Mon Jul 02 2012 Petr Pisar <ppisar@redhat.com> - 73-1
- 73 bump

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 72-2
- Perl 5.16 rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 72-1
- 72 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 71-1
- 71 bump

* Fri May 18 2012 Petr Pisar <ppisar@redhat.com> - 70-1
- 70 bump

* Mon Jan 30 2012 Petr Pisar <ppisar@redhat.com> - 69-1
- 69 bump

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 68-1
- 68 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Petr Pisar <ppisar@redhat.com> - 67-1
- 67 bump

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 66-1
- 66 bump

* Mon Sep 19 2011 Petr Pisar <ppisar@redhat.com> - 65-1
- 65 bump

* Mon Aug 22 2011 Petr Pisar <ppisar@redhat.com> - 64-1
- 64 bump

* Tue Jul 26 2011 Petr Pisar <ppisar@redhat.com> - 62-1
- 62 bump
- Remove RPM 4.8 filters

* Tue Jul 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 61-3
- add RPM4.9 macro filter

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 61-2
- Perl mass rebuild

* Mon Jun 06 2011 Petr Pisar <ppisar@redhat.com> - 61-1
- Version 61 bump

* Mon May 23 2011 Petr Pisar <ppisar@redhat.com> - 60-2
- Remove explicit defattr

* Mon May 23 2011 Petr Pisar <ppisar@redhat.com> - 60-1
- Version 60 bump

* Tue May 10 2011 Petr Pisar <ppisar@redhat.com> - 59-1
- Version 59 bump

* Tue May 10 2011 Petr Pisar <ppisar@redhat.com> - 58-1
- Version 58 bump

* Fri May 06 2011 Petr Pisar <ppisar@redhat.com> - 57-1
- Version 57 bump

* Thu Apr 28 2011 Petr Pisar <ppisar@redhat.com> - 56-1
- Version 56 bump
- Do not provide private parsers

* Tue Apr 26 2011 Petr Pisar <ppisar@redhat.com> - 55-1
- Version 55 bump

* Thu Apr 21 2011 Petr Pisar <ppisar@redhat.com> - 54-1
- 54 bump

* Thu Apr 21 2011 Petr Pisar <ppisar@redhat.com> - 51-1
- Version 51 bump

* Thu Apr 21 2011 Petr Pisar <ppisar@redhat.com> - 46-2
- Do not provide Perl::MinimumVersion

* Tue Jan 25 2011 Petr Pisar <ppisar@redhat.com> 46-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuidRoot stuff
- Install into perl core direcotory
- Make the package no-architecture depndend (the XS compilation is test-time)
