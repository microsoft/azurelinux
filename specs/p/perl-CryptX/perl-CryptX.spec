# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enable JSON support
%bcond_without perl_CryptX_enables_json
# Run optional test
%bcond_without perl_CryptX_enables_optional_test

Name:           perl-CryptX
Version:        0.087
Release: 6%{?dist}
Summary:        Cryptographic toolkit
# src/ltc/*:    Unlicense
# src/ltm/*:    Unlicense
# Other files:  GPL-1.0-or-later OR Artistic-1.0-Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Unlicense
URL:            https://metacpan.org/release/CryptX
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MIK/CryptX-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(XSLoader)
# Optional run-time:
%if %{with perl_CryptX_enables_json}
BuildRequires:  perl(JSON)
%endif
# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
%if %{with perl_CryptX_enables_optional_test}
# Optional tests:
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::Complex)
BuildRequires:  perl(Storable) >= 2.0
BuildRequires:  perl(Test::Pod)
%endif

Provides:       bundled(libtomcrypt) = 1.18.2-1.20250506gitd448df17
Provides:       bundled(libtommath) = 1.2.0-1.20250611git839ae9ea

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Math::BigFloat|Math::BigInt|Storable)\\)$
# Remove private modules
%global __requires_exclude %{__requires_exclude}|^perl\\(\\.::

%description
This Perl library provides a cryptography based on LibTomCrypt library.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       perl-Test-Harness
%if %{with perl_CryptX_enables_json}
Requires:       perl(JSON)
%endif
%if %{with perl_CryptX_enables_optional_test}
Requires:       perl(File::Find)
Requires:       perl(Math::BigFloat)
Requires:       perl(Math::BigInt)
Requires:       perl(Math::Complex)
Requires:       perl(Storable) >= 2.0
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n CryptX-%{version}
# https://github.com/DCIT/perl-CryptX/issues/96
sed -i -e's/1\.999842/1.999840/g' t/mbi_ltm_since_1.999842.t
# Fix permissions
chmod -x t/data/openssl_rsa-x509.pem
# Remove unsed tests
%if !%{with perl_CryptX_enables_optional_test}
for F in t/002_all_pm.t t/003_all_pm_pod.t t/mbi_ltm_bigfltpm.t \
        t/mbi_ltm_bigintpm.t t/mbi_ltm_biglog.t t/mbi_ltm_bigroot.t \
        t/mbi_ltm/bigintpm.inc t/mbi_ltm/bigfltpm.inc t/mbi_ltm_storable.t; do
    rm "${F}"
    perl -i -ne 'print $_ unless m{\A\Q'"${F}"'\E}' MANIFEST
done
%endif
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done
# Handle license files for libtomcrypt and libtommath
cp -a src/ltc/LICENSE LICENSE.libtomcrypt
cp -a src/ltm/LICENSE LICENSE.libtommath

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -delete
%{_fixperms} $RPM_BUILD_ROOT/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
%if %{with perl_CryptX_enables_optional_test}
rm %{buildroot}%{_libexecdir}/%{name}/t/{002_all_pm,003_all_pm_pod}.t
%endif
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# t/crypt-misc.t writes into CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/t "$DIR"
pushd "$DIR"
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE LICENSE.libtomcrypt LICENSE.libtommath
%doc Changes README.md
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt
%{perl_vendorarch}/CryptX.pm
%{perl_vendorarch}/Math
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.087-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.087-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.087-3
- Perl 5.42 rebuild

* Thu Jun 12 2025 Xavier Bachelot <xavier@bachelot.org> - 0.087-2
- Use any version of Math::BigInt and Math::BigFloat
- Fix bundled Provides:

* Wed Jun 11 2025 Xavier Bachelot <xavier@bachelot.org> - 0.087-1
- Update to 0.087 (RHBZ#2372355,RHBZ#2372356,RHBZ#2372357,RHBZ#2372358)
  - Fix CVE-2025-40914

* Sat May 03 2025 Xavier Bachelot <xavier@bachelot.org> - 0.086-1
- Update to 0.086 (RHBZ#2363852, RHBZ#2354493)

* Tue Feb 11 2025 Xavier Bachelot <xavier@bachelot.org> - 0.085-1
- Update to 0.085 (RHBZ#2344451)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.084-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 16 2024 Xavier Bachelot <xavier@bachelot.org> - 0.084-1
- Update to 0.084 (RHBZ#2319152)

* Tue Oct 15 2024 Xavier Bachelot <xavier@bachelot.org> - 0.083-1
- Update to 0.083 (RHBZ#2310725)
- Drop EL7 support
- Fix Math::BigInt/BigFloat versions and conditionals

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.080-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.080-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.080-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.080-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Xavier Bachelot <xavier@bachelot.org> - 0.080-1
- Update to 0.080 (RHBZ#2242102)

* Mon Oct 02 2023 Xavier Bachelot <xavier@bachelot.org> - 0.079-1
- Update to 0.079 (RHBZ#2241629)
  - Fix CVE-2019-17362 in bundled libtomcrypt
- Add upstream patch to fix tests with Math::BigInt 1.999840+ (RHBZ#2240587)

* Fri Aug 25 2023 Xavier Bachelot <xavier@bachelot.org> - 0.078-4
- Don't Requires: perl(Math::BigFloat) for tests subpackage on EL7 (RHBZ#2234802)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.078-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.078-2
- Perl 5.38 rebuild

* Thu May 11 2023 Xavier Bachelot <xavier@bachelot.org> - 0.078-1
- Update to 0.078 (RHBZ#2120043)
- Convert license to SPDX

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.076-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.076-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.076-3
- Perl 5.36 rebuild

* Fri May 27 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.076-2
- Fix test issues with new version of Math::BigInt.

* Mon Feb 14 2022 Xavier Bachelot <xavier@bachelot.org> - 0.076-1
- Update to 0.076 (RHBZ#1549877)
- Use bundled libtomcrypt and libtommath to enable ECC support (RHBZ#1654710)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Petr Pisar <ppisar@redhat.com> - 0.053-24
- Hide internal functions (upstream bug #68)

* Wed Oct 06 2021 Petr Pisar <ppisar@redhat.com> - 0.053-23
- Adapt to changes in Math-BigInt-1.999825 (bug #2011184)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Petr Pisar <ppisar@redhat.com> - 0.053-21
- Do not disable LTO (upstream bug #70)

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.053-20
- Perl 5.34 rebuild

* Tue Mar 30 2021 Petr Pisar <ppisar@redhat.com> - 0.053-19
- Fix handling PEM decoding failures (upstream bug #67)
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.053-16
- Perl 5.32 rebuild

* Wed Jun 24 2020 Petr Pisar <ppisar@redhat.com> - 0.053-15
- Remove t/wycheproof.t test (bug #1850379)

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.053-14
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Petr Pisar <ppisar@redhat.com> - 0.053-12
- Adapt to changes in Math-BigInt 1.999817 (bug #1769850)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Petr Pisar <ppisar@redhat.com> - 0.053-10
- Require Math::Complex for running tests

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.053-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 29 2018 Petr Pisar <ppisar@redhat.com> - 0.053-7
- Adapt to changes in libtomcrypt-1.18.2 (bug #1605403)
- Adapt to changes in Math-BigInt-1.999815

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.053-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.053-5
- Perl 5.28 rebuild

* Thu May 03 2018 Petr Pisar <ppisar@redhat.com> - 0.053-4
- Adapt tests to changes in Math::BigInt 1.999813

* Thu Mar  1 2018 Florian Weimer <fweimer@redhat.com> - 0.053-3
- Rebuild with new redhat-rpm-config/perl build flags

* Wed Feb 28 2018 Petr Pisar <ppisar@redhat.com> - 0.053-2
- Validate decode_b58b input properly

* Thu Feb 15 2018 Petr Pisar <ppisar@redhat.com> 0.053-1
- Specfile autogenerated by cpanspec 1.78.
