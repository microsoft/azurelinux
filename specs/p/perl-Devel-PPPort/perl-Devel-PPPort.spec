# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 3.68

# Perform optional tests
%bcond_without perl_Devel_PPPort_enables_optional_test

Name:           perl-Devel-PPPort
Version:        3.73
Release: 522%{?dist}
Summary:        Perl Pollution Portability header generator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Devel-PPPort
Source0:        https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Devel-PPPort-%{base_version}.tar.gz
# Upgrade to 3.71 based on perl-5.37.11
Patch0:         Devel-PPPort-3.68-Upgrade-to-3.71.patch
Patch1:         Devel-PPPort-3.68-Add-shebang-to-tests.patch
# Upgrade to 3.72 based on perl-5.40.0-RC1
Patch2:         Devel-PPPort-3.71-Upgrade-to-3.72.patch
# Upgrade to 3.73 based on perl-5.42.0
Patch3:         Devel-PPPort-3.72-Upgrade-to-3.73.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.3
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Run-time:
# warnings in PPPort.pm not used
# Tests:
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(less)
BuildRequires:  perl(lib)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
%if %{with perl_Devel_PPPort_enables_optional_test} && !%{defined %perl_bootstrap}
# Optional tests:
# File::Spec not helpful
BuildRequires:  perl(Test::Pod) >= 0.95
%endif

# Filter modules bundled for tests
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(.::parts/.*\\)

%description
Perl's API has changed over time, gaining new features, new functions,
increasing its flexibility, and reducing the impact on the C name space
environment (reduced pollution). The header file written by this module,
typically ppport.h, attempts to bring some of the newer Perl API features
to older versions of Perl, so that you can worry less about keeping track
of old releases, but users can still reap the benefit.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(File::Spec)
Requires:       perl(less)
Requires:       perl(utf8)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%{?perl_default_filter}

%prep
%autosetup -p1 -n Devel-PPPort-%{base_version}

# Help generators to recognize Perl scripts
for F in t/*.pl parts/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t parts %{buildroot}%{_libexecdir}/%{name}
chmod +x %{buildroot}%{_libexecdir}/%{name}/t/*.t
perl -i -pe 's{(ppptmp)}{/tmp/$1}' %{buildroot}%{_libexecdir}/%{name}/t/ppphtest.t
rm %{buildroot}%{_libexecdir}/%{name}/t/podtest.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset PERL_CORE SKIP_SLOW_TESTS
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make regen_tests
make test

%files
# README.md is useless
%doc Changes HACKERS README soak TODO
%{perl_vendorarch}/auto/Devel*
%{perl_vendorarch}/Devel*
%{_mandir}/man3/Devel::PPPort*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.73-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.73-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.73-519
- Upgrade to 3.73 based on perl-5.42.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.72-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-510
- Increase release to favour standalone package

* Mon Jun 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.72-504
- Upgrade to 3.72 based on perl-5.40.0-RC1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.71-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.71-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.71-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-499
- Increase release to favour standalone package

* Tue May 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.71-1
- Upgrade to 3.71 based on perl-5.37.11

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.68-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.68-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.68-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.68-488
- Increase release to favour standalone package

* Thu Mar 24 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.68-1
- 3.68 bump

* Thu Mar 10 2022 Michal Josef Špaček <mspacek@redhat.com> - 3.67-1
- 3.67 bump

* Thu Mar 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.66-1
- 3.66 bump

* Wed Feb 02 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.64-1
- 3.64 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-1
- 3.63 bump
- Package tests

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.62-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.62-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 19 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.62-1
- 3.62 bump

* Thu Aug 13 2020 Petr Pisar <ppisar@redhat.com> - 3.60-1
- 3.60 bump

* Tue Aug 11 2020 Petr Pisar <ppisar@redhat.com> - 3.59-1
- 3.59 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.58-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.58-2
- Perl 5.32 rebuild

* Tue Mar 10 2020 Petr Pisar <ppisar@redhat.com> - 3.58-1
- 3.58 bump

* Mon Feb 03 2020 Petr Pisar <ppisar@redhat.com> - 3.57-1
- 3.57 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Petr Pisar <ppisar@redhat.com> - 3.56-1
- 3.56 bump

* Mon Nov 11 2019 Petr Pisar <ppisar@redhat.com> - 3.55-1
- 3.55 bump

* Mon Sep 30 2019 Petr Pisar <ppisar@redhat.com> - 3.54-1
- 3.54 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.52-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.52-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.52-438
- Increase release to favour standalone package

* Wed May 15 2019 Petr Pisar <ppisar@redhat.com> - 3.52-1
- 3.52 bump

* Thu May 02 2019 Petr Pisar <ppisar@redhat.com> - 3.51-1
- 3.51 bump

* Tue Apr 30 2019 Petr Pisar <ppisar@redhat.com> - 3.49-1
- 3.49 bump

* Mon Apr 29 2019 Petr Pisar <ppisar@redhat.com> - 3.48.again-1
- 3.48-again bump

* Fri Apr 05 2019 Petr Pisar <ppisar@redhat.com> - 3.45-2
- Fix a leak in tests

* Wed Mar 20 2019 Petr Pisar <ppisar@redhat.com> - 3.45-1
- 3.45 bump

* Thu Feb 21 2019 Petr Pisar <ppisar@redhat.com> - 3.44-1
- 3.44 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.43-1
- 3.43 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.42-2
- Perl 5.28 rebuild

* Mon Apr 23 2018 Petr Pisar <ppisar@redhat.com> - 3.42-1
- 3.42 bump

* Tue Mar 06 2018 Petr Pisar <ppisar@redhat.com> - 3.36-6
- Modernize spec file

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.36-2
- Perl 5.26 rebuild

* Mon May 15 2017 Petr Pisar <ppisar@redhat.com> - 3.36-1
- 3.36 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 3.35-1
- 3.35 bump

* Wed Jun 15 2016 Petr Pisar <ppisar@redhat.com> - 3.34-1
- 3.34 bump

* Mon Jun 06 2016 Petr Pisar <ppisar@redhat.com> - 3.33-1
- 3.33 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.32-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 01 2015 Petr Pisar <ppisar@redhat.com> - 3.32-1
- 3.32 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.31-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.31-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.31-2
- Perl 5.22 rebuild

* Fri Mar 13 2015 Petr Pisar <ppisar@redhat.com> - 3.31-1
- 3.31 bump

* Fri Mar 06 2015 Petr Pisar <ppisar@redhat.com> - 3.30-1
- 3.30 bump

* Mon Jan 19 2015 Petr Pisar <ppisar@redhat.com> - 3.28-1
- 3.28 bump

* Fri Jan 09 2015 Petr Pisar <ppisar@redhat.com> - 3.25-2
- Do not export private library

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 3.25-1
- 3.25 bump

* Thu Sep 18 2014 Petr Pisar <ppisar@redhat.com> 3.24-1
- Specfile autogenerated by cpanspec 1.78.
