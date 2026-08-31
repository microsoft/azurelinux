# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_IO_Socket_IP_enables_optional_test
%else
%bcond_with perl_IO_Socket_IP_enables_optional_test
%endif

Name:           perl-IO-Socket-IP
Version:        0.43
Release:        521%{?dist}
Summary:        Drop-in replacement for IO::Socket::INET supporting both IPv4 and IPv6
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-Socket-IP
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/IO-Socket-IP-%{version}.tar.gz
# IO-Socket-IP-0.41 moved from ExtUtils::MakeMaker to Module::Build.
# It will make problems, because IO::Socket::IP is a dual-lived package and
# needs to be built very early on Perl bootstrap, but Module::Build is not
# a core package and thus not available in the early stage of bootstrapping.
# For this reason, we create Makefile.PL and use it instead of Build.PL.
Source1:        Makefile.PL
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Errno)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket) >= 1.97
BuildRequires:  perl(strict)
buildrequires:  perl(warnings)
# Tests only
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Test2::V0)
%if %{with perl_IO_Socket_IP_enables_optional_test} && !%{defined perl_bootstrap}
# Optional tests only
BuildRequires:  perl(Test::Pod) >= 1.00
%endif

%{?perl_default_filter}

%description
This module provides a protocol-independent way to use IPv4 and IPv6
sockets, intended as a replacement for IO::Socket::INET. Most constructor
arguments and methods are provided in a backward-compatible way.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n IO-Socket-IP-%{version}
cp %{SOURCE1} .
chmod -x lib/IO/Socket/IP.pm
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
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm -f %{buildroot}%{_libexecdir}/%{name}/t/99pod.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes examples README
%{perl_vendorlib}/IO/*
%{_mandir}/man3/IO::Socket::IP*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 28 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-1
- 0.43 bump (rhbz#2328740)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-1
- 0.42 bump (rhbz#2225678)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-499
- Increase release to favour standalone package

* Mon Mar 27 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.41-493
- Package tests

* Fri Mar 24 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.41-492
- Remove not needed Socket6 package in build

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 17 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-2
- Create Makefile.PL, use ExtUtils::MakeMaker instead of Module::Build

* Wed Sep 16 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-1
- 0.41 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-2
- Perl 5.26 rebuild

* Tue Mar 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-1
- 0.39 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-1
- 0.38 bump

* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 0.37-367
- Migrate from Module::Build to ExtUtils::MakeMaker
- Correct IO/Socket/IP.pm file mode

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-345
- Increase release to favour standalone package

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-2
- Perl 5.22 rebuild

* Fri Mar 13 2015 Petr Šabata <contyk@redhat.com> - 0.37-1
- 0.37 bump

* Fri Jan 30 2015 Petr Šabata <contyk@redhat.com> - 0.36-1
- 0.36 bump
- Win32 changes only

* Mon Jan 05 2015 Petr Šabata <contyk@redhat.com> - 0.35-1
- 0.35 bugfix bump

* Fri Dec 12 2014 Petr Pisar <ppisar@redhat.com> - 0.34-2
- Do not build-require non-core Socket6 module when bootstrapping this core
  module

* Fri Dec 05 2014 Petr Šabata <contyk@redhat.com> - 0.34-1
- 0.34 bump, VMS bugfixes

* Tue Nov 25 2014 Petr Šabata <contyk@redhat.com> - 0.33-1
- 0.33 bump

* Thu Sep 18 2014 Petr Šabata <contyk@redhat.com> - 0.32-1
- 0.32 bump, implement connect timeout

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-2
- Perl 5.20 rebuild

* Wed Jul 16 2014 Petr Šabata <contyk@redhat.com> - 0.31-1
- 0.31 bump

* Wed Jul 09 2014 Petr Pisar <ppisar@redhat.com> - 0.30-2
- Fix multihomed SSL (bug #1116600)

* Mon Jul 07 2014 Petr Pisar <ppisar@redhat.com> - 0.30-1
- 0.30 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Petr Šabata <contyk@redhat.com> - 0.29-1
- 0.29 bump

* Wed Feb 12 2014 Petr Šabata <contyk@redhat.com> - 0.28-1
- 0.28 bump

* Tue Jan 21 2014 Petr Šabata <contyk@redhat.com> - 0.27-1
- 0.27 bump, test suite enhancements only

* Fri Jan 17 2014 Petr Šabata <contyk@redhat.com> - 0.26-1
- 0.26 bump

* Fri Sep 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-1
- 0.24 bump

* Mon Sep 16 2013 Petr Šabata <contyk@redhat.com> - 0.23-1
- 0.23 bump; smarter SO_REUSEPORT tests

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Šabata <contyk@redhat.com> - 0.22-1
- 0.22 bump
- Test suite bugfix release

* Thu Jul 18 2013 Petr Šabata <contyk@redhat.com> - 0.21-3
- Disable the SO_REUSEPORT test; koji builders don't support this feature yet

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.21-2
- Perl 5.18 rebuild

* Mon Apr 29 2013 Petr Šabata <contyk@redhat.com> - 0.21-1
- 0.21 bump

* Wed Apr 17 2013 Petr Šabata <contyk@redhat.com> - 0.20-1
- 0.20 bump

* Tue Mar 12 2013 Petr Šabata <contyk@redhat.com> - 0.19-1
- 0.19 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Petr Šabata <contyk@redhat.com> - 0.18-1
- 0.18 bump

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 0.17-2
- Fix a typo, sort the deps

* Wed Aug 22 2012 Petr Šabata <contyk@redhat.com> - 0.17-1
- 0.17 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.16-2
- Perl 5.16 rebuild

* Mon Jun 25 2012 Petr Šabata <contyk@redhat.com> - 0.16-1
- 0.16 (IO::Socket::INET compatibility enhancement)

* Thu Jun 21 2012 Petr Šabata <contyk@redhat.com> - 0.15-1
- 0.15 bump

* Tue Jun 19 2012 Petr Šabata <contyk@redhat.com> - 0.14-1
- 0.14 bump

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.11-2
- Perl 5.16 rebuild

* Wed Jun 06 2012 Petr Šabata <contyk@redhat.com> - 0.11-1
- 0.11 bump

* Fri May 11 2012 Petr Šabata <contyk@redhat.com> - 0.10-1
- 0.10 bump

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 0.09-1
- 0.09 bump

* Fri Jan 27 2012 Petr Šabata <contyk@redhat.com> 0.08-1
- Specfile autogenerated by cpanspec 1.78.
