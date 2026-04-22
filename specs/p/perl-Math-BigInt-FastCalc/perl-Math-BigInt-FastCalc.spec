# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Math-BigInt-FastCalc
%global cpan_version 0.5020
Version:        0.502.000
Release: 521%{?dist}
Summary:        Math::BigInt::Calc with some XS for more speed
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Math-BigInt-FastCalc
Source0:        https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-FastCalc-%{cpan_version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.6.1
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Math::BigInt::Calc) >= 2.005001
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigInt) >= 2.003001
BuildRequires:  perl(Test::More) >= 0.88
Conflicts:      perl < 4:5.22.0-348
Requires:       perl(Math::BigInt) >= 2.005001

# Filter modules bundled for tests
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(.::t/.*.inc\\)
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
This Perl module provides support for fast big integer calculations.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Math::BigInt) >= 2.005001

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Math-BigInt-FastCalc-%{cpan_version}

# Remove bundled libraries
rm -r inc
perl -i -ne 'print $_ unless m{^inc/}' MANIFEST
find -type f -exec chmod -x {} +

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
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
%doc CHANGES CREDITS README TODO
%{perl_vendorarch}/auto/Math*
%{perl_vendorarch}/Math*
%{_mandir}/man3/Math::BigInt::FastCalc*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.502.000-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.502.000-519
- Increase release to favour standalone package

* Fri Mar 28 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.502.000-1
- 0.5020 bump (rhbz#2355196)

* Mon Mar 03 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.900-1
- 0.5019 bump (rhbz#2349246)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.800-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.800-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.800-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.800-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.800-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.800-1
- 0.5018 bump (rhbz#2257058)

* Fri Jan 05 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.700-1
- 0.5017 bump (rhbz#2256784)

* Tue Jan 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.600-1
- 0.5016 bump (rhbz#2255963)

* Thu Sep 21 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.500-1
- 0.5015 bump (rhbz#2239928)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.400-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.400-2
- Perl 5.38 rebuild

* Mon Apr 03 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.400-1
- 0.5014 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.300-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.300-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.300-2
- Perl 5.36 rebuild

* Tue May 17 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.300-1
- 0.5013 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 30 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.200-1
- 0.5012 bump

* Thu Sep 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.100-1
- 0.5011 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.501.000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.501.000-1
- 0.5010 bump
- Package tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.500.900-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.900-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.900-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.500.900-456
- Increase release to favour standalone package

* Wed Feb 05 2020 Tom Stellard <tstellar@redhat.com> - 0.500.900-3
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.900-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 14 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.500.900-1
- 0.5009 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.800-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.500.800-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.800-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.500.800-1
- 0.5008 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.700-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.500.700-2
- Perl 5.28 rebuild

* Wed Apr 18 2018 Petr Pisar <ppisar@redhat.com> - 0.500.700-1
- 0.5007 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.600-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.600-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.600-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.500.600-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.500.600-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Petr Pisar <ppisar@redhat.com> - 0.500.600-1
- 0.5006 bump

* Fri Dec 23 2016 Petr Pisar <ppisar@redhat.com> 0.500.500-1
- Specfile autogenerated by cpanspec 1.78.
