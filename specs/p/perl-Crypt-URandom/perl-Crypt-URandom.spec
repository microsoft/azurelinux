# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optional tests
%bcond_without perl_Crypt_URandom_enables_optional_test

Name:           perl-Crypt-URandom
Version:        0.55
Release: 2%{?dist}
Summary:        Non-blocking randomness for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Crypt-URandom
Source0:        https://cpan.metacpan.org/authors/id/D/DD/DDICK/Crypt-URandom-%{version}.tar.gz
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
BuildRequires:  perl(Carp) >= 1.26
BuildRequires:  perl(constant)
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(FileHandle)
# Win32 not used
# Win32::API not used
# Win32::API::Type not used
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Encode)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More)
%if %{with perl_Crypt_URandom_enables_optional_test}
# Optional tests:
# Devel::Cover not helpful
BuildRequires:  perl(Test::Pod) >= 1.14
%endif
Requires:       perl(Carp) >= 1.26
Requires:       perl(FileHandle)

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Carp\\)$

%description
This Module is intended to provide an interface to the strongest available
source of non-blocking randomness on the current platform.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       gcc
Requires:       perl-Test-Harness
Requires:       perl(Carp) >= 1.26

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n Crypt-URandom-%{version}
%if !%{with perl_Crypt_URandom_enables_optional_test}
rm t/pod.t
perl -i -ne 'print $_ unless m{^t/pod.t}' MANIFEST
%endif
# Delete always skipped release tests
rm t/manifest.t
perl -i -ne 'print $_ unless m{^t/manifest.t}' MANIFEST
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
unset CRYPT_URANDOM_BUILD_DEBUG
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a check_random.inc t %{buildroot}%{_libexecdir}/%{name}
# t/boilerplate.t expects files in source archive locations.
rm %{buildroot}%{_libexecdir}/%{name}/t/boilerplate.t
%if %{with perl_Crypt_URandom_enables_optional_test}
rm %{buildroot}%{_libexecdir}/%{name}/t/pod.t
%endif
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
# check_random.inc and t/getrandom.t write into CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/* "$DIR"
# t/core_read.t etc. needs URandom.pm in ./blib without URandom.so
mkdir -p "$DIR/blib/lib/Crypt"
cp %{perl_vendorarch}/Crypt/URandom.pm "$DIR/blib/lib/Crypt"
pushd "$DIR"
unset CRYPT_URANDOM_BUILD_DEBUG
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset CRYPT_URANDOM_BUILD_DEBUG
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
# README.md is identical to README.
%doc Changes README SECURITY.md
%dir %{perl_vendorarch}/auto/Crypt
%{perl_vendorarch}/auto/Crypt/URandom
%dir %{perl_vendorarch}/Crypt
%{perl_vendorarch}/Crypt/URandom.pm
%{_mandir}/man3/Crypt::URandom.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Feb 23 2026 Petr Pisar <ppisar@redhat.com> - 0.55-1
- 0.55 bump (CVE-2026-2474, bug #2440313)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.54-2
- Perl 5.42 rebuild

* Mon Mar 17 2025 Petr Pisar <ppisar@redhat.com> - 0.54-1
- 0.54 bump

* Mon Feb 10 2025 Petr Pisar <ppisar@redhat.com> - 0.53-1
- 0.53 bump

* Thu Jan 23 2025 Petr Pisar <ppisar@redhat.com> - 0.52-1
- 0.52 bump

* Wed Jan 22 2025 Petr Pisar <ppisar@redhat.com> - 0.51-1
- 0.51 bump

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Petr Pisar <ppisar@redhat.com> - 0.50-1
- 0.50 bump

* Wed Jan 08 2025 Petr Pisar <ppisar@redhat.com> - 0.49-1
- 0.49 bump

* Tue Jan 07 2025 Petr Pisar <ppisar@redhat.com> - 0.48-1
- 0.48 bump

* Mon Jan 06 2025 Petr Pisar <ppisar@redhat.com> - 0.46-1
- 0.46 bump

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 26 2024 Petr Pisar <ppisar@redhat.com> - 0.40-1
- 0.40 bump

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 22 2023 Petr Pisar <ppisar@redhat.com> - 0.39-1
- 0.39 bump

* Thu May 11 2023 Petr Pisar <ppisar@redhat.com> - 0.38-1
- 0.38 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-23
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Petr Pisar <ppisar@redhat.com> - 0.36-21
- Modernize a spec file
- Package the tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-19
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-16
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-2
- Perl 5.22 rebuild

* Thu Jun 11 2015 Petr Pisar <ppisar@redhat.com> - 0.36-1
- 0.36 bump

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-2
- Perl 5.22 rebuild

* Fri Oct 10 2014 Petr Pisar <ppisar@redhat.com> 0.34-1
- Specfile autogenerated by cpanspec 1.78.
