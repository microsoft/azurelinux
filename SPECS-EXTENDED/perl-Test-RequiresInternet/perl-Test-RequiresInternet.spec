Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		perl-Test-RequiresInternet
Version:	0.05
Release:	17%{?dist}
Summary:	Easily test network connectivity
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/Test-RequiresInternet
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-RequiresInternet-%{version}.tar.gz#/perl-Test-RequiresInternet-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Socket)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module is intended to easily test network connectivity before functional
tests begin to non-local Internet resources. It does not require any modules
beyond those supplied in core Perl.

If you do not specify a host/port pair, then the module defaults to using
www.google.com on port 80. You may optionally specify the port by its name, as
in http or ldap. If you do this, the test module will attempt to look up the
port number using getservbyname. If you do specify a host and port, they must
be specified in pairs. It is a fatal error to omit one or the other.

If the environment variable NO_NETWORK_TESTING is set, then the tests will be
skipped without attempting any socket connections.

If the sockets cannot connect to the specified hosts and ports, the exception
is caught, reported and the tests skipped.

%prep
%setup -q -n Test-RequiresInternet-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::RequiresInternet.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.05-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 28 2019 Paul Howarth <paul@city-fan.org> - 0.05-15
- Spec tidy-up
  - Use author-independent source URL
  - Specify all build requirements
  - Simplify find command using -delete

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-2
- Perl 5.22 rebuild

* Tue May 26 2015 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Fix test error when NO_NETWORK_TESTING is set (CPAN RT#101996, GH#3)

* Thu Jan 29 2015 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - Test::More prior to 0.88 (included with perl 5.10.1) does not support the
    done_testing() function; revert to a test plan to support older perls
    (GH#2)

* Mon Jan 26 2015 Paul Howarth <paul@city-fan.org> - 0.03-2
- Sanitize for Fedora submission

* Mon Jan 26 2015 Paul Howarth <paul@city-fan.org> - 0.03-1
- Initial RPM version
