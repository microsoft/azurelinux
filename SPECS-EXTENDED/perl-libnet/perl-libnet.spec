# Run optional test
%bcond_without perl_libnet_enables_optional_test
# SASL support
%bcond_without perl_libnet_enables_sasl
# SSL support
%bcond_without perl_libnet_enables_ssl
Summary:        Perl clients for various network protocols
Name:           perl-libnet
Version:        3.11
Release:        443%{?dist}
# other files:  GPL+ or Artistic
## Not in binary packages
# repackage.sh: GPLv2+
## Removed from upstream sources:
# lib/Net/libnetFAQ.pod:    Artistic    (CPAN RT#117888)
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/libnet
# Origin source archive contains Artistic only files, CPAN RT#117888.
# Local archive produced by "./repackage.sh %%{version}" command.
# http://www.cpan.org/authors/id/S/SH/SHAY/libnet-%%{version}.tar.gz
Source0:        %{_mariner_sources_url}/%{name}_repackaged-%{version}.tar.gz
# Replacement for the Artistic only file, CPAN RT#117888.
Source1:        libnetFAQ.pod
# Convert Changes to UTF-8
Patch0:         libnet-3.09-Normalize-Changes-encoding.patch
# Do not create Net/libnet.cfg, bug #1238689
Patch1:         libnet-3.08-Do-not-create-Net-libnet.cfg.patch
# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((IO::Socket|Socket)\\)$
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# Run-time:
BuildRequires:  perl(Carp)
# MD5 not used because we prefer Digest::MD5
# MIME::Base64 not used at tests
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
# Convert::EBCDIC not used
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Temp)
# File::Basename not used at tests
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket) >= 1.05
# Prefer IO::Socket::IP over IO::Socket::INET6 and IO::Socket::INET
# IO::Socket::INET6 not used
BuildRequires:  perl(IO::Socket::IP) >= 0.25
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket) >= 2.016
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(constant)
# Getopt::Std not used because of Do-not-create-Net-libnet.cfg.patch
# IO::File not used because of Do-not-create-Net-libnet.cfg.patch
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Digest::MD5 or MD5
Requires:       perl(Digest::MD5)
Requires:       perl(File::Basename)
Requires:       perl(IO::Socket) >= 1.05
# Prefer IO::Socket::IP over IO::Socket::INET6 and IO::Socket::INET
Requires:       perl(IO::Socket::IP) >= 0.25
Requires:       perl(POSIX)
Requires:       perl(Socket) >= 2.016
Conflicts:      perl < 4:5.22.0-347
BuildArch:      noarch
# Optional run-time:
# Authen::SASL not used at tests
# Digest::MD5 not used at tests
%if %{with perl_libnet_enables_ssl} && !%{defined perl_bootstrap}
# Core modules must be built without non-core dependencies
BuildRequires:  perl(IO::Socket::SSL) >= 2.007
%endif
%if %{with perl_libnet_enables_optional_test}
# Optional tests:
%if %{with perl_libnet_enables_ssl} && !%{defined perl_bootstrap}
# Core modules must be built without non-core dependencies
BuildRequires:  perl(IO::Socket::SSL::Utils)
%endif
# Test::CPAN::Changes not used
# Test::Perl::Critic not used
# Test::Pod 1.00 not used
# Test::Pod::Coverage 0.08 not used
%endif

%description
This is a collection of Perl modules which provides a simple and
consistent programming interface (API) to the client side of various
protocols used in the internet community.

%prep
# Avoid autosetup
%setup -q -n libnet-%{version}
# Provide dummy Net::libnetFAQ document, CPAN RT#117888
install -m 0644 %{SOURCE1} lib/Net
%patch0 -p1
%patch1 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 </dev/null
%make_build

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license Artistic Copying LICENCE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Mar 07 2023 Muhammad Falak <mwani@microsoft.com> - 3.11-443
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.11-442
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.11-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.11-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.11-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.11-416
- Increase release to favour standalone package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 12 2017 Petr Pisar <ppisar@redhat.com> - 3.11-2
- Require Digest::MD5 for APOP login method

* Wed Nov 15 2017 Petr Pisar <ppisar@redhat.com> - 3.11-1
- 3.11 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.10-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.10-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 16 2016 Petr Pisar <ppisar@redhat.com> - 3.10-2
- Net::libnetFAQ document replaced with a hyper link because of the Artistic
  license (CPAN RT#117888)

* Mon Aug 01 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.10-1
- 3.10 bump

* Wed Jul 27 2016 Petr Pisar <ppisar@redhat.com> - 3.09-2
- Fix blocking in Net::FTP and other subclasses (bug #1360610)

* Wed Jul 20 2016 Petr Pisar <ppisar@redhat.com> - 3.09-1
- 3.09 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.08-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.08-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Petr Pisar <ppisar@redhat.com> - 3.08-1
- 8.08 bump

* Mon Jul 20 2015 Petr Pisar <ppisar@redhat.com> - 3.07-1
- 3.07 bump

* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> 3.06-1
- Specfile autogenerated by cpanspec 1.78.
- Do not create Net/libnet.cfg (bug #1238689)
