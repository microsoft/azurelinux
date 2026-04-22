# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optional tests
%{bcond_without perl_HTTP_Daemon_enables_optional_test}

Name:           perl-HTTP-Daemon
Version:        6.16
Release: 8%{?dist}
Summary:        Simple HTTP server class
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/HTTP-Daemon
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Daemon-%{version}.tar.gz
# Use Makefile.PL without unneeded dependencies
Patch0:         HTTP-Daemon-6.04-EU-MM-is-not-deprecated.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(HTTP::Request) >= 6
BuildRequires:  perl(HTTP::Response) >= 6
BuildRequires:  perl(HTTP::Status) >= 6
BuildRequires:  perl(IO::Socket::IP) >= 0.32
BuildRequires:  perl(LWP::MediaTypes) >= 6
BuildRequires:  perl(Socket)
BuildRequires:  perl(warnings)
# Tests only:
BuildRequires:  perl(lib)
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(URI)
# Optional tests:
%if %{with perl_HTTP_Daemon_enables_optional_test} && !%{defined %perl_bootstrap}
BuildRequires:  perl(LWP::RobotUA)
BuildRequires:  perl(LWP::UserAgent) >= 6.37
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful
%endif
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(HTTP::Request) >= 6
Requires:       perl(HTTP::Response) >= 6
Requires:       perl(HTTP::Status) >= 6
Requires:       perl(IO::Socket::IP) >= 0.32
Requires:       perl(LWP::MediaTypes) >= 6
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(HTTP::(Date|Request|Response|Status)|IO::Socket::IP|LWP::MediaTypes\\)$
# Remove private test modules
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(TestServer|TestServer::(BasicTests|Reflect)\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(TestServer|TestServer::(BasicTests|Reflect)\\)$

%description
Instances of the HTTP::Daemon class are HTTP/1.1 servers that listen on a
socket for incoming requests. The HTTP::Daemon is a subclass of
IO::Socket::IP, so you can perform socket operations directly on it too.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# perl-generators doesn't detect 'use Test::Needs 'LWP::RobotUA';'
Requires:       perl(LWP::RobotUA)
# perl-generators doesn't detect 'use Test::Needs 'LWP::UserAgent';'
Requires:       perl(LWP::UserAgent) >= 6.37

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n HTTP-Daemon-%{version}
%patch -P0 -p1
# Help generators to recognize Perl scripts
for F in $(find t/ -name '*.t'); do
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
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)" -r
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENCE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb 24 2023 Michal Josef Špaček <mspacek@redhat.com> - 6.16-1
- 6.16 bump
- Fix minimal version of IO::Socket::IP
- Fix requires/provided modules in *tests package

* Thu Feb 23 2023 Michal Josef Špaček <mspacek@redhat.com> - 6.15-1
- 6.15 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 25 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.14-8
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.14-6
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.14-5
- Perl 5.36 rebuild

* Mon Apr 25 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.14-4
- Remove dependency to Module::Build::Tiny (patched by patch0)

* Tue Mar 22 2022 Adam Williamson <awilliam@redhat.com> - 6.14-3
- Rebuild with no changes to fix update mess on F36

* Tue Mar 22 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.14-2
- Fix cycle dependencies (bug #2063824)

* Fri Mar 04 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.14-1
- 6.14 bump
- Package unit tests

* Thu Feb 10 2022 Michal Josef Špaček <mspacek@redhat.com> - 6.13-1
- 6.13 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 6.12-5
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.12-2
- Perl 5.32 rebuild

* Fri Jun 05 2020 Petr Pisar <ppisar@redhat.com> - 6.12-1
- 6.12 bump

* Wed May 27 2020 Petr Pisar <ppisar@redhat.com> - 6.10-1
- 6.10 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Petr Pisar <ppisar@redhat.com> - 6.06-1
- 6.06 bump

* Mon Jul 29 2019 Petr Pisar <ppisar@redhat.com> - 6.05-1
- 6.05 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-2
- Perl 5.30 rebuild

* Tue Apr 02 2019 Petr Pisar <ppisar@redhat.com> - 6.04-1
- 6.04 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-24
- Perl 5.28 rebuild

* Wed May 23 2018 Petr Pisar <ppisar@redhat.com> - 6.01-23
- Fix formatting numerical non-local specific IPv6 addresses (bug #1578026)

* Tue May 15 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-22
- Call "sockhostname" method on correct class object (bug #1578026)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Petr Pisar <ppisar@redhat.com> - 6.01-20
- Correct the package description

* Mon Sep 18 2017 Petr Pisar <ppisar@redhat.com> - 6.01-19
- Correct a typo in the undefined and empty-string LocalAddr patch
  (bug #1413065)

* Mon Sep 18 2017 Petr Pisar <ppisar@redhat.com> - 6.01-18
- Accept undefined and empty-string LocalAddr as IO::Socket::INET does
  (bug #1413065)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-16
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Petr Pisar <ppisar@redhat.com> - 6.01-14
- Support IPv6 (bug #1413065)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-13
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-10
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.01-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 6.01-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Petr Šabata <contyk@redhat.com> - 6.01-4
- Modernize the spec, fix dependencies, and drop command macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 6.01-2
- Perl 5.16 rebuild

* Mon Feb 20 2012 Petr Pisar <ppisar@redhat.com> - 6.01-1
- 6.01 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.00-3
- add new filter

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.00-2
- Perl mass rebuild

* Thu Mar 17 2011 Petr Pisar <ppisar@redhat.com> 6.00-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
- Conflicts with perl-libwww-perl-5* and older
