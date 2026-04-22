# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Math-BigInt
Epoch:          1
%global cpan_version 2.005003
# Keep 4-digit version to compete with perl.spec
Version:        %(echo %{cpan_version} | sed 's/\(\.....\)/\1./')
Release: 4%{?dist}
Summary:        Arbitrary-size integer and float mathematics
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Math-BigInt
Source0:        https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(Carp) >= 1.22
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(integer)
BuildRequires:  perl(Math::Complex) >= 1.39
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
# Module::Signature not used
# Socket not used
BuildRequires:  perl(Test::More) >= 0.94
Requires:       perl(Carp) >= 1.22
Requires:       perl(Math::Complex) >= 1.39
Conflicts:      perl < 4:5.22.0-347

Provides:       perl-Math-BigRat =  %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      perl-Math-BigRat < 0.2624-502

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Math::BigInt\\)\\s*$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Carp\\)\\s*$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(.::t/.*.inc\\)
%global __requires_exclude %{__requires_exclude}|perl\\(Math::BigFloat::(BareSubclass\|Subclass)\\)
%global __requires_exclude %{__requires_exclude}|perl\\(Math::BigInt::(BareCalc\|Scalar\|Subclass)\\)
%global __requires_exclude %{__requires_exclude}|perl\\(Math::BigInt::Lib::(Minimal\|TestUtil)\\)
%global __requires_exclude %{__requires_exclude}|perl\\(Math::BigRat::Subclass\\)

%description
This provides Perl modules for arbitrary-size integer and float mathematics.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Math-BigInt-%{cpan_version}

# Help generators to recognize Perl scripts
for F in t/*.t t/alias.inc; do
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
rm %{buildroot}%{_libexecdir}/%{name}/t/00sig.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset TEST_SIGNATURE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
# NEW file is useless
%doc BUGS CHANGES CREDITS examples GOALS HISTORY README TODO
%{perl_vendorlib}/Math*
%{_mandir}/man3/Math::Big*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0050.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0050.03-2
- Perl 5.42 rebuild

* Mon Apr 14 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0050.03-1
- 2.005003 bump (rhbz#2359305)

* Mon Mar 31 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0050.02-1
- 2.005002 bump (rhbz#2355802)

* Fri Mar 28 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0050.01-1
- 2.005001 bump (rhbz#2355194)

* Mon Mar 03 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0040.01-1
- 2.004001 bump (rhbz#2349247)

* Fri Jan 24 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0030.04-1
- 2.003004 bump (rhbz#2341776)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0030.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0030.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0030.03-2
- Perl 5.40 rebuild

* Tue May 28 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0030.03-1
- 2.003003 bump (rhbz#2283507)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0030.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0030.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0030.02-1
- 2.003002 bump (rhbz#2257059)

* Tue Jan 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0030.01-1
- 2.003001 bump (rhbz#2255925)

* Mon Dec 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0020.01-1
- 2.002001 bump (rhbz#2253770)

* Mon Dec 04 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0020.00-1
- 2.002000 bump (rhbz#2252546)

* Wed Nov 22 2023 Petr Pisar <ppisar@redhat.com> - 1:2.0010.01-1
- 2.001001 bump

* Tue Nov 14 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0010.00-1
- 2.001000 bump (rhbz#2249534)

* Wed Nov 01 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0000.00-1
- 2.000000 bump (rhbz#2247279)
  Merge the Math-BigRat distribution into the Math-BigInt distribution

* Mon Oct 02 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.42-1
- 1.999842 bump (rhbz#2241058)

* Fri Sep 22 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.41-1
- 1.999841 bump (rhbz#2240164)

* Wed Sep 20 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.40-1
- 1.999840 bump (rhbz#2239487)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.39-1
- 1.999839 bump (rhbz#2222961)

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.38-3
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.38-2
- Perl 5.38 rebuild

* Sun Apr 02 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.38-1
- 1.999838 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.37-1
- 1.999837 bump

* Mon Jun 27 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.36-1
- 1.999836 bump

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.35-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.35-2
- Perl 5.36 rebuild

* Tue May 24 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.35-1
- 1.999835 bump

* Mon May 23 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.33-1
- 1.999833 bump

* Sun May 22 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.32-1
- 1.999832 bump

* Mon May 16 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.31-1
- 1.999831 bump

* Wed Apr 13 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.30-1
- 1.999830 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.29-1
- 1.999829 bump

* Mon Dec 20 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.28-1
- 1.999828 bump

* Sun Oct 03 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.27-1
- 1.999827 bump

* Wed Sep 29 2021 Michal Josef Špaček <mspacek@redhat.com> - 1:1.9998.25-1
- 1.999825 bump

* Wed Sep 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.24-1
- 1.999824 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.23-1
- 1.999823 bump

* Mon Jul 12 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.22-1
- 1.999822 bump

* Wed Jul 07 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.21-1
- 1.999821 bump
- Package tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.18-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.18-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.18-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.18-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.18-1
- 1.999818 bump

* Mon Oct 14 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.17-1
- 1.999817 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.16-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.16-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 31 2018 Petr Pisar <ppisar@redhat.com> - 1:1.9998.16-1
- 1.999816 bump

* Tue Oct 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.15-1
- 1.999815 bump

* Fri Oct 12 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.14-1
- 1.999814 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.13-2
- Perl 5.28 rebuild

* Wed Apr 18 2018 Petr Pisar <ppisar@redhat.com> - 1:1.9998.13-1
- 1.999813 bump

* Wed Apr 18 2018 Petr Pisar <ppisar@redhat.com> - 1:1.9998.12-1
- 1.999812 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9998.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.11-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9998.11-2
- Perl 5.26 rebuild

* Fri Mar 17 2017 Petr Pisar <ppisar@redhat.com> - 1.9998.11-1
- 1.999811 bump

* Thu Mar 02 2017 Petr Pisar <ppisar@redhat.com> - 1.9998.10-1
- 1.999810 bump

* Mon Feb 13 2017 Petr Pisar <ppisar@redhat.com> - 1.9998.09-1
- 1.999809 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9998.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Paul Howarth <paul@city-fan.org> - 1.9998.08-1
- 1.999808 bump

* Mon Jan 02 2017 Petr Pisar <ppisar@redhat.com> - 1.9998.07-1
- 1.999807 bump

* Wed Dec 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9998.06-1
- 1.999806 bump

* Mon Dec 12 2016 Petr Pisar <ppisar@redhat.com> - 1.9998.05-1
- 1.999805 bump

* Fri Dec 09 2016 Petr Pisar <ppisar@redhat.com> - 1.9998.04-1
- 1.999804 bump

* Mon Dec 05 2016 Petr Pisar <ppisar@redhat.com> - 1.9998.03-1
- 1.999803 bump

* Thu Dec 01 2016 Petr Pisar <ppisar@redhat.com> - 1.9998.02-1
- 1.999802 bump

* Fri Nov 25 2016 Petr Pisar <ppisar@redhat.com> - 1.9998.01-1
- 1.999801 bump

* Fri Nov 18 2016 Petr Pisar <ppisar@redhat.com> - 1.9998.00-1
- 1.999800 bump

* Tue Nov 08 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.27-1
- 1.999727 bump

* Mon Jul 18 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.26-1
- 1.999726 bump

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.24-1
- 1.999724 bump

* Wed Jun 15 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.23-1
- 1.999723 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9997.22-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9997.22-2
- Perl 5.24 rebuild

* Wed Apr 27 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.22-1
- 1.999722 bump

* Tue Apr 26 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.20-1
- 1.999720 bump

* Mon Apr 18 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.17-1
- 1.999717 bump

* Tue Apr 05 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.16-1
- 1.999716 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9997.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.15-1
- 1.999715 bump

* Mon Jan 04 2016 Petr Pisar <ppisar@redhat.com> - 1.9997.14-1
- 1.999714 bump

* Mon Nov 16 2015 Petr Pisar <ppisar@redhat.com> - 1.9997.10-1
- 1.999710 bump

* Tue Nov 10 2015 Petr Pisar <ppisar@redhat.com> - 1.9997.09-1
- 1.999709 bump

* Thu Nov 05 2015 Petr Pisar <ppisar@redhat.com> - 1.9997.08-1
- 1.999708 bump

* Mon Nov 02 2015 Petr Pisar <ppisar@redhat.com> 1.9997.07-354
- Specfile autogenerated by cpanspec 1.78.
- Use bundled modules when bootstrapping
