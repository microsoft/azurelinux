# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 2.75
# Perform optional tests
%bcond_without perl_Net_Ping_enables_optional_test

Name:           perl-Net-Ping
Version:        2.76
Release:        520%{?dist}
Summary:        Check a remote host for reachability
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Net-Ping/
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Net-Ping-%{base_version}.tar.gz
# Unbundled from perl 5.37.11
Patch0:         Net-Ping-2.75-Upgrade-to-2.76.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.2
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(IO::Socket::INET)
# Net::Ping::External not used at tests
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket) >= 2.007
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(vars)
# Win32 not used on Linux
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
# sudo not used
%if %{with perl_Net_Ping_enables_optional_test}
# Optional tests:
BuildRequires:  perl(:VERSION) >= 5.6
# Class::XSAccessor not used
BuildRequires:  perl(IO::Socket)
# List::MoreUtils not used
# Module::CPANTS::Kwalitee::Uses not used
# Text::CSV_XS not used
# Test::CPAN::Meta not used
# Test::Kwalitee not used
BuildRequires:  perl(Test::Pod) >= 1.22
# Test::Pod::Coverage not used
%endif
Requires:       perl(IO::Socket::INET)
# Keep Net::Ping::External optional
Suggests:       perl(Net::Ping::External)
Conflicts:      perl < 4:5.22.0-350

%description
Net::Ping module contains methods to test the reachability of remote hosts on
a network.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Socket)
Requires:       perl(IO::Socket)
Requires:       perl(IO::Socket::INET)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Net-Ping-%{base_version}
%patch -P0 -p1
# Remove author tests
rm t/6*.t
# Remove appveyor script
rm t/appveyor-test.bat
# Remove removed files from MANIFEST file
perl -i -ne 'print $_ unless m{^(?:t/6.*\.t|appveyor-test\.bat)}' MANIFEST
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
unset PERL_CORE
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset AUTHOR_TESTING IS_MAINTAINER NET_PING_FAIL_IP PERL_TEST_Net_Ping \
    TEST_PING_HOST TEST_PING6_HOST
export NO_NETWORK_TESTING=1
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
unset AUTHOR_TESTING IS_MAINTAINER NET_PING_FAIL_IP PERL_TEST_Net_Ping \
    TEST_PING_HOST TEST_PING6_HOST
export NO_NETWORK_TESTING=1
make test

%files
%doc Changes README TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.76-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.76-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.76-499
- Increase release to favour standalone package

* Thu May 18 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.76-1
- Upgrade to 2.76 as provided in perl-5.37.11

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 02 2022 Michal Josef Špaček <mspacek@redhat.com> - 2.75-2
- Package tests
- Unify to use macros
- Update license to SPDX format

* Tue Sep 06 2022 Michal Josef Špaček <mspacek@redhat.com> - 2.75-1
- Bump 2.75

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.74-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.74-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.74-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.74-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.74-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.74-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 03 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.74-2
- Disable network tests in 200_tcp_ping

* Mon Nov 16 2020 Petr Pisar <ppisar@redhat.com> 2.74-1
- Specfile autogenerated by cpanspec 1.78.
