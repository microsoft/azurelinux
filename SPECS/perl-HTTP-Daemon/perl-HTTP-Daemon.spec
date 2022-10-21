Name:           perl-HTTP-Daemon
Version:        6.06
Release:        4%{?dist}
Summary:        Simple HTTP server class
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/HTTP-Daemon
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Daemon-%{version}.tar.gz#/perl-HTTP-Daemon-%{version}.tar.gz
# Use Makefile.PL without unneeded dependencies
Patch0:         HTTP-Daemon-6.04-EU-MM-is-not-deprecated.patch
BuildArch:      noarch
BuildRequires:  make
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
BuildRequires:  perl(IO::Socket::IP)
BuildRequires:  perl(LWP::MediaTypes) >= 6
BuildRequires:  perl(Socket)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(warnings)
# Tests only:
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Spec)
# LWP::UserAgent not used
BuildRequires:  perl(Module::Metadata)
# Test not used if LWP::UserAgent is not installed
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Needs)
# URI not used
# Optional tests:
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful
# LWP::RobotUA not used
# LWP::UserAgent not used
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(HTTP::Request) >= 6
Requires:       perl(HTTP::Response) >= 6
Requires:       perl(HTTP::Status) >= 6
Requires:       perl(LWP::MediaTypes) >= 6
Requires:       perl(Sys::Hostname)
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(HTTP::(Date|Request|Response|Status)|LWP::MediaTypes\\)$

%description
Instances of the HTTP::Daemon class are HTTP/1.1 servers that listen on a
socket for incoming requests. The HTTP::Daemon is a subclass of
IO::Socket::IP, so you can perform socket operations directly on it too.

%prep
%setup -q -n HTTP-Daemon-%{version}
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
# Some tests are skipped with "Can't talk to ourself (misconfigured system)".
# These tests actually are never run becuse the required CAN_TALK_TO_OURSELF
# file is never created. Those are author's tests.
make test

%files
%license LICENCE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 26 2022 Henry Li <lihl@microsoft.com> - 6.06-4
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.06-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
