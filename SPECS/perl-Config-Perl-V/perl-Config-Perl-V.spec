# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Config-Perl-V
Version:        0.39
Release:        1%{?dist}
Summary:        Structured data retrieval of perl -V output
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Config-Perl-V
Source0:        https://cpan.metacpan.org/authors/id/H/HM/HMBRAND/Config-Perl-V-%{version}.tgz
# Correct example
Patch0:         Config-Perl-V-0.24-Remove-invalid-shellbang.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(warnings)
# Optional run-time:
BuildRequires:  perl(Digest::MD5)
# Tests:
BuildRequires:  perl(Test::More)
%if !%{defined perl_bootstrap}
# Building core modules must not require non-core modules when bootstrapping
BuildRequires:  perl(Test::NoWarnings)
%endif
Suggests:       perl(Digest::MD5)
Conflicts:      perl < 4:5.22.0-347

%description
The command "perl -V" will return you an excerpt from the %%Config::Config
hash combined with the output of "perl -V" that is not stored inside the hash,
but only available to the perl binary itself. This package provides Perl
module that will return you the output of "perl -V" in a structure.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if !%{defined perl_bootstrap}
Requires:       perl(Digest::MD5)
Requires:       perl(Test::NoWarnings)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Config-Perl-V-%{version}
%patch -P0 -p1
chmod -x examples/*

for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

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
# Building core modules must not require non-core modules when bootstrapping
make test PERL_CORE=%{defined perl_bootstrap}

%files
%doc Changelog CONTRIBUTING.md examples README
%dir %{perl_vendorlib}/Config
%{perl_vendorlib}/Config/Perl
%{_mandir}/man3/Config::Perl::V*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Jan 28 2026 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-1
- 0.39 bump (rhbz#2432655)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-1
- 0.38 bump (rhbz#2337314)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-499
- Increase release to favour standalone package

* Thu Mar 02 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-1
- 0.36 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-1
- 0.35 bump

* Wed Aug 24 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-1
- 0.34 bump
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-481
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-479
- Perl 5.34 re-rebuild of bootstrapped packages

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-1
- 0.33 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-456
- Increase release to favour standalone package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-442
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 27 2019 Petr Pisar <ppisar@redhat.com> - 0.32-441
- Indeed upgrade to 0.32

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-438
- Increase release to favour standalone package

* Fri May 03 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-1
- Upgrade to 0.32 as provided in perl-5.29.10

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 19 2018 Petr Pisar <ppisar@redhat.com> - 0.31-1
- 0.31 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Petr Pisar <ppisar@redhat.com> - 0.30-1
- 0.30 bump

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 16 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-1
- 0.29 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-393
- Perl 5.26 rebuild

* Fri May 12 2017 Petr Pisar <ppisar@redhat.com> - 0.28-2
- Building core modules must not require non-core modules when bootstrapping

* Thu May 11 2017 Petr Pisar <ppisar@redhat.com> - 0.28-1
- Upgrade to 0.28 as provided in perl-5.25.12

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-1
- 0.27 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.24 rebuild

* Wed May 11 2016 Petr Pisar <ppisar@redhat.com> - 0.26-1
- 0.26 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Petr Pisar <ppisar@redhat.com> - 0.25-1
- 0.25 bump

* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> 0.24-348
- Specfile autogenerated by cpanspec 1.78.
