# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enable PPIx::Regexp optional feature
%bcond_without perl_PPIx_QuoteLike_enables_PPIx_Regexp

Name:           perl-PPIx-QuoteLike
Version:        0.023
Release: 10%{?dist}
Summary:        Parse Perl string literals and string-literal-like things
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/PPIx-QuoteLike
Source0:        https://cpan.metacpan.org/authors/id/W/WY/WYANT/PPIx-QuoteLike-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# Build.PL and inc/My/Module/Build.pm not used
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
# Test::Without::Module not helpful
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Encode)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(PPI::Document) >= 1.238
BuildRequires:  perl(PPI::Dumper) >= 1.238
BuildRequires:  perl(re)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(Scalar::Util)
%if %{with perl_PPIx_QuoteLike_enables_PPIx_Regexp}
# Optional run-time:
# Author states there is a build-cycle with PPIx::Regexp, but I cannot see
# any.
BuildRequires:  perl(PPIx::Regexp)
%endif
# Tests:
BuildRequires:  perl(charnames)
BuildRequires:  perl(open)
BuildRequires:  perl(Test::More) >= 0.88
Requires:       perl(PPI::Document) >= 1.238
Requires:       perl(PPI::Dumper) >= 1.238
%if %{with perl_PPIx_QuoteLike_enables_PPIx_Regexp}
Recommends:     perl(PPIx::Regexp)
%endif

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((PPI::Document|PPI::Dumper)\\)$

%description
This Perl class parses Perl string literals and things that are reasonably
like string literals. Its real reason for being is to find interpolated
variables for Perl::Critic policies and similar code.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(open)
Requires:       perl(PPI::Document) >= 1.238

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n PPIx-QuoteLike-%{version}
# Fix shell bang and permissions
for F in eg/{pqldump,variables}; do
    perl -MConfig -p -i -e 's{\A#!/usr/bin/env perl\b}{$Config{startperl}}' \
        "$F"
    chmod -x "$F"
done
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

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
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSES/*
%doc Changes CONTRIBUTING eg README
%{perl_vendorlib}/PPIx/
%{_mandir}/man3/PPIx::QuoteLike*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Sep 17 2022 Paul Howarth <paul@city-fan.org> - 0.023-2
- Use SPDX-format license tag

* Fri Sep 16 2022 Paul Howarth <paul@city-fan.org> - 0.023-1
- Update to 0.023 (rhbz#2127475)
  - Update discouragement notice for variables(), and add a TODO in
    t/variables.t for why
  - Correct normalization of ${^FOO} for PPI: if the caret is present the
    braces are not removed

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.022-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-2
- Perl 5.36 rebuild

* Sat Apr 16 2022 Paul Howarth <paul@city-fan.org> - 0.022-1
- Update to 0.022
  - Remove 'postderef' argument to new(); postfix dereference is always
    recognized

* Sun Apr  3 2022 Paul Howarth <paul@city-fan.org> - 0.021-1
- Update to 0.021
  - Recognize postfix deref in '@{[ ... ]}' for determining minimum Perl
    version; this recognizes all forms of postfix dereference, including ->%%*,
    ->&*, and ->** (NOTE: for now, this remains a
    PPIx::QuoteLike::Token::Interpolation)
  - Require PPI 1.238 for postfix deref support, and prune code that dealt with
    PPI's old behavior
  - Postfix %%*, &*, and ** do not interpolate
  - Correct perl_version_introduced() for interpolated postfix scalar deref

* Tue Mar 22 2022 Adam Williamson <awilliam@redhat.com> - 0.020-2
- Rebuild with no changes to fix update mess on F36

* Thu Mar 17 2022 Paul Howarth <paul@city-fan.org> - 0.020-1
- Update to 0.020
  - Correct and optimize the computation of logical column position (the one
    that takes account of tabs)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Paul Howarth <paul@city-fan.org> - 0.019-1
- Update to 0.019
  - Add CONTRIBUTING file
  - Try to quell weird Win32 test failures that seem to occur only in tests
    where I am using 'use open' to put the standard handles into UTF-8 mode;
    the fix (hopefully) is to do this to the Test::Harness handles at run time
    instead of to the standard handles at compile time

* Fri Oct 22 2021 Paul Howarth <paul@city-fan.org> - 0.018-1
- Update to 0.018
  - Argument postderef is now fatal
  - Correct generation of 'provides' metadata

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.017-2
- Perl 5.34 rebuild

* Fri Apr 16 2021 Paul Howarth <paul@city-fan.org> - 0.017-1
- Update to 0.017
  - All uses of the postderef argument to new() now warn
- Fix permissions verbosely
- Make %%files list more explicit

* Fri Mar 26 2021 Petr Pisar <ppisar@redhat.com> - 0.016-1
- 0.016 bump
- Package tests

* Fri Feb 05 2021 Petr Pisar <ppisar@redhat.com> - 0.015-1
- 0.015 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Petr Pisar <ppisar@redhat.com> - 0.014-1
- 0.014 bump

* Fri Oct 09 2020 Petr Pisar <ppisar@redhat.com> - 0.013-1
- 0.013 bump

* Tue Jul 28 2020 Petr Pisar <ppisar@redhat.com> - 0.012-1
- 0.012 bump

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-2
- Perl 5.32 rebuild

* Tue Mar 31 2020 Petr Pisar <ppisar@redhat.com> - 0.011-1
- 0.011 bump

* Mon Mar 09 2020 Petr Pisar <ppisar@redhat.com> - 0.010-1
- 0.010 bump

* Fri Feb 28 2020 Petr Pisar <ppisar@redhat.com> - 0.009-1
- 0.009 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Petr Pisar <ppisar@redhat.com> - 0.008-1
- 0.008 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Petr Pisar <ppisar@redhat.com> - 0.007-1
- 0.007 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.006-4
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Petr Pisar <ppisar@redhat.com> - 0.006-1
- 0.006 bump

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-2
- Perl 5.28 rebuild

* Mon Jun 04 2018 Petr Pisar <ppisar@redhat.com> 0.005-1
- Specfile autogenerated by cpanspec 1.78.
