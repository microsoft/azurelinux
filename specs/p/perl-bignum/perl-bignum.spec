# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-bignum
Version:        0.67
Release: 522%{?dist}
Summary:        Transparent big number support for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/bignum
Source0:        https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/bignum-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.10
BuildRequires:  perl(Carp) >= 1.22
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigInt) >= 1.999830
BuildRequires:  perl(Math::BigRat) >= 0.2623
BuildRequires:  perl(overload)
# Optional run-time:
# Math::BigInt::Lite not packaged
# Tests:
BuildRequires:  perl(Test::More) >= 0.88
# Optional tests:
%if !%{defined perl_bootstrap}
# Module::Signature not used and not helpful
BuildRequires:  perl(Math::BigInt::GMP)
# Math::BigInt::Pari not package yet
# Socket not used
%endif
Requires:       perl(Carp) >= 1.22
Requires:       perl(Math::BigInt) >= 1.999830
Requires:       perl(Math::BigRat) >= 0.2623
Conflicts:      perl < 4:5.22.0-348

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Math::BigInt\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Math::BigRat\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Carp\\)$

%description
This package attempts to make it easier to write scripts that use BigInts and
BigFloats in a transparent way.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if !%{defined perl_bootstrap}
Requires:       perl(Math::BigInt::GMP)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n bignum-%{version}

# Correct shebangs and permission
for F in lib/Math/BigInt/Trace.pm lib/Math/BigFloat/Trace.pm; do
    perl -MConfig -pi -e 's{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod -x "$F"
done

# Help generators to recognize Perl scripts
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
rm %{buildroot}%{_libexecdir}/%{name}/t/00sig.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/usr/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset TEST_SIGNATURE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc BUGS CHANGES README TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.67-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.67-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.67-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.67-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.67-1
- 0.67 bump (rhbz#2256265)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.66-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.66-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.66-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.66-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.66-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.66-4
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.66-3
- Perl 5.36 rebuild

* Mon May 23 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.66-2
- Don't run optional tests, if we're bootstrapping

* Mon May 16 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.66-1
- 0.66 bump

* Wed Apr 13 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.65-1
- 0.65 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.64-1
- 0.64 bump

* Sun Oct 10 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.63-1
- 0.63 bump

* Sun Oct 03 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.62-1
- 0.62 bump

* Thu Sep 30 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-1
- 0.60 bump

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.53-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.53-1
- 0.53 bump

* Mon Jul 12 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-2
- Fix permission of */Trace.pm

* Mon Jul 12 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-1
- 0.52 bump
- Package tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-1
- 0.51 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-2
- Perl 5.28 rebuild

* Wed Apr 18 2018 Petr Pisar <ppisar@redhat.com> - 0.50-1
- 0.50 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Petr Pisar <ppisar@redhat.com> - 0.49-1
- 0.49 bump

* Fri Feb 02 2018 Petr Pisar <ppisar@redhat.com> - 0.48-1
- 0.48 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Petr Pisar <ppisar@redhat.com> 0.47-1
- Specfile autogenerated by cpanspec 1.78.
