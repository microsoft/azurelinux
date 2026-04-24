# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Algorithm-C3
Version:	0.11
Release: 17%{?dist}
Summary:	Module for merging hierarchies using the C3 algorithm
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Algorithm-C3
Source0:	https://cpan.metacpan.org/modules/by-module/Algorithm/Algorithm-C3-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp) >= 0.01
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test
BuildRequires:	perl(Test::More) >= 0.47
# Runtime

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Test::More)\\)$

%description
This module implements the C3 algorithm.  Most of the uses I have for C3
revolve around class building and metamodels but it could also be used for
things like dependency resolution as well since it tends to do such a nice
job of preserving local precedence orderings.

%package tests
Summary:	Tests for %{name}
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	perl-Test-Harness
Requires:	perl(Test::More) >= 0.47

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Algorithm-C3-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -r -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Algorithm/
%{_mandir}/man3/Algorithm::C3.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 02 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.11-10
- Update license to SPDX format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 Michal Josef Špaček <mspacek@redhat.com> - 0.11-5
- Package tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Set metadata for static dependency list and install
  - Move repository to GitHub
  - Minor test clean-ups
  - Fix Makefile.PL to work for authors in perl 5.26+
- Package new LICENSE file

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-18
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 15 2019 Paul Howarth <paul@city-fan.org> - 0.10-16
- Spec tidy-up
  - Use author-independent source URL
  - Specify all build dependencies
  - Drop redundant buildroot cleaning in %%install section
  - Simplify find command using -delete
  - Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-11
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-3
- Perl 5.22 rebuild

* Thu Sep 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-2
- Perl 5.20 rebuild

* Thu Sep  4 2014 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - Declare minimum version of perl as 5.6 in metadata

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar  3 2014 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Convert to use ExtUtils::MakeMaker using distar
  - Include repo and bugtracker metadata
- This release by HAARG -> update source URL
- Switch to ExtUtils::MakeMaker flow

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 0.08-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.08-10
- Perl 5.16 rebuild

* Mon Jan 16 2012 Paul Howarth <paul@city-fan.org> - 0.08-9
- Spec clean-up:
  - Make %%files list more explicit
  - Categorize build requirements for build/module/test
  - Don't use macros for commands
  - Use tabs
  - Fix typo in %%description

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.08-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-3
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-1
- Auto-update to 0.08 (by cpan-spec-update 0.01)
- Altered br on perl(Test::More) (0 => 0.47)
- Added a new br on perl(Carp) (version 0.01)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.07-2
- Rebuild for new perl

* Thu May 31 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.07-1
- Update to 0.07
- Include t/ in doc
- Minor spec reworkage to deal with the once and future perl split

* Tue Nov 21 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.06-1
- Update to 0.06

* Wed Sep 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-2
- Bump

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-1
- Specfile autogenerated by cpanspec 1.69.1
