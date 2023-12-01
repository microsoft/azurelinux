Summary:        SSL sockets with IO::Socket interface
Name:           perl-IO-Socket-SSL
Version:        2.074
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/IO-Socket-SSL
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-Socket-SSL-%{version}.tar.gz
Source1:        LICENSE.PTR
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-Net-SSLeay
%if %{with_check}
BuildRequires:  perl(Test::More)
BuildRequires:  perl(FindBin)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Config)
Requires:       perl(HTTP::Tiny)
Requires:       perl(IO::Socket::INET)
Requires:       perl(IO::Socket::IP) >= 0.31
Requires:       perl(Socket) >= 1.95
Requires:       openssl-libs >= 0.9.8

Requires:       perl-Net-SSLeay

Provides:       perl(IO::Socket::SSL) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::Intercept) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::OCSP_Cache) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::OCSP_Resolver) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::PublicSuffix) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::SSL_Context) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::SSL_HANDLE) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::Session_Cache) = %{version}-%{release}
Provides:       perl(IO::Socket::SSL::Utils) = %{version}-%{release}

%description
IO::Socket::SSL makes using SSL/TLS much easier by wrapping the necessary functionality into the familiar IO::Socket interface and providing secure defaults whenever possible. This way, existing applications can be made SSL-aware without much effort, at least if you do blocking I/O and don't use select or poll.

%prep
%setup -q -n IO-Socket-SSL-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
            -name '*.bs' -size 0 \) -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
cp %{SOURCE1} ./

%check
# Disable t/protocol_version.t test which is failing due to our openssl configuration.
# Example error:
#   "looks like OpenSSL was compiled without SSLv3 support"
#   Failed test 'accept TLSv1 with TLSv1'" got: 'TLSv1_3'" expected: 'TLSv1'"
rm -v ./t/protocol_version.t
make test

%files
%license LICENSE.PTR
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Fri Jul 29 2022 Muhammad Falak <mwani@microsoft.com> - 2.074-2
- Add BR on `perl(ExtUtils::MakeMaker)` & check deps to enable ptest

* Tue Apr 22 2022 Mateusz Malisz <mamalisz@microsoft.com> - 2.074-1
- Update to 2.074

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.066-6
- Adding 'BuildRequires: perl-generators'.

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.066-5
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 2.066-4: Fix check tests.

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 2.066-4
-   Use new perl package names.
-   Provide perl(IO::Socket::SSL*).
*   Wed May 27 2020 Nick Samson <nisamson@microsoft.com> 2.066-3
-   Added LICENSE file and %%license invocation.
*   Wed Apr 15 2020 Nick Samson <nisamson@microsoft.com> 2.066-2
-   Updated Source0. License verified.
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 2.066-1
-   Update to 2.066. License fixed.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.060-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.060-1
-   Update to version 2.060
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.047-2
-   Ensure non empty debuginfo
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 2.047-1
-   Update to 2.047
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.024-2
-   GA - Bump release of all rpms
*   Mon Mar 28 2016 Mahmoud Bassiouny <mbassiounu@vmware.com> 2.024-1
-   Initial version.
