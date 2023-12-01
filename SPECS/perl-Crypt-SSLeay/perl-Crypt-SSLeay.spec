%define LICENSE_PATH LICENSE.PTR

Summary:        Crypt::SSLeay - OpenSSL support for LWP
Name:           perl-Crypt-SSLeay
Version:        0.73_06
Release:        2%{?dist}
URL:            https://metacpan.org/release/Crypt-SSLeay
License:        Artistic 2.0
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://cpan.metacpan.org/authors/id/N/NA/NANIS/Crypt-SSLeay-%{version}.tar.gz
Source1:        %{LICENSE_PATH}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(XSLoader)
Requires:       openssl
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  openssl-devel
BuildRequires:  perl-Path-Class
BuildRequires:  perl-Try-Tiny
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Bytes::Random::Secure)

Provides:       perl(Crypt::SSLeay) = %{version}-%{release}
Provides:       perl(Crypt::SSLeay::CTX) = %{version}-%{release}
Provides:       perl(Crypt::SSLeay::Conn) = %{version}-%{release}
Provides:       perl(Crypt::SSLeay::Err) = %{version}-%{release}
Provides:       perl(Crypt::SSLeay::MainContext) = %{version}-%{release}
Provides:       perl(Crypt::SSLeay::Version) = %{version}-%{release}
Provides:       perl(Crypt::SSLeay::X509) = %{version}-%{release}
Provides:       perl(Net::SSL) = %{version}-%{release}

%description
This Perl module provides support for the HTTPS protocol under LWP, to allow an LWP::UserAgent object to perform GET, HEAD and POST requests. Please see LWP for more information on POST requests.

The Crypt::SSLeay package provides Net::SSL, which is loaded by LWP::Protocol::https for https requests and provides the necessary SSL glue.

This distribution also makes following deprecated modules available:

Crypt::SSLeay::CTX
Crypt::SSLeay::Conn
Crypt::SSLeay::X509
Work on Crypt::SSLeay has been continued only to provide https support for the LWP (libwww-perl) libraries.

%prep
%setup -q -n Crypt-SSLeay-%{version}
cp %{SOURCE1} ./

%build
PERL5LIB=$(pwd) env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
sed -i 's/CCCDLFLAGS = /CCCDLFLAGS = -g /' Makefile
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find "%{buildroot}" -type f \( -name .packlist -o -name '*.bs' -size 0 \) -exec rm -f {} ';'

%check
make test

%files
%license %{LICENSE_PATH}
%{perl_vendorarch}/*
%{_mandir}/man?/*

%changelog
* Wed Jul 27 2022 Muhammad Falak <mwani@micrsofot.com> - 0.73_06-2
- Add BR on `perl(Test::More)` & `perl(Bytes::Random::Secure)` to enable ptest

* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 0.73_06
- Update to 0.73_06
- Add missing requires for ExtUtils::CBuilder.

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.72-8
- Adding 'BuildRequires: perl-generators'.

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.72-8
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 0.72-7: Add patch to fix test issue

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 0.72-7
-   Use new perl package names.
-   Change perl_vendorlib to perl_vendorarch directory for packaging.
-   Provide perl(Crypt::*).
*   Thu Jun 06 2020 Joe Schmitt <joschmit@microsoft.com> 0.72-6
-   Added %%license macro.
-   Update License.
-   Verified License.
-   Update Source0.
-   Update URL.
-   Remove sha1 macro.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.72-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Nov 20 2018 Dweep Advani <dadvani@vmware.com> 0.72-4
-   Reverting to 0.72 as 0.73_06 is still a DEV version
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.73_06-1
-   Update version to 0.73_06
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.72-3
-   Remove BuildArch
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.72-2
-   Fix arch
*   Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.72-1
-   Initial version.
