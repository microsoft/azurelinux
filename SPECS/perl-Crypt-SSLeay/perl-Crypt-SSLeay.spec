%define LICENSE_PATH LICENSE.PTR

Summary:        Crypt::SSLeay - OpenSSL support for LWP
Name:           perl-Crypt-SSLeay
Version:        0.72
Release:        7%{?dist}
URL:            https://metacpan.org/release/Crypt-SSLeay
License:        Artistic 2.0
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://cpan.metacpan.org/authors/id/N/NA/NANIS/Crypt-SSLeay-%{version}.tar.gz
Source1:        %{LICENSE_PATH}
Patch0:         Use_TLS_client_method-with-OpenSSL-1.1.1.patch
Requires:       perl >= 5.28.0
Requires:       openssl
BuildRequires:  perl >= 5.28.0
BuildRequires:  openssl-devel
BuildRequires:  perl-Path-Class
BuildRequires:  perl-Try-Tiny

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
%patch0 -p0

%build
PERL5LIB=$(pwd) env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
sed -i 's/CCCDLFLAGS = /CCCDLFLAGS = -g /' Makefile
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
            -name '*.bs' -size 0 \) -exec rm -f {} ';'

%check
make test

%files
%license %{LICENSE_PATH}
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
*   Mon Mar 15 2021 Andrew Phelps <anphel@microsoft.com> 0.72-7
-   Add patch to fix test issue
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
