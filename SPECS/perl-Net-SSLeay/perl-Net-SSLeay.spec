Summary:        Perl extension for using OpenSSL
Name:           perl-Net-SSLeay
Version:        1.88
Release:        3%{?dist}
License:        Artistic 2.0
Group:          Development/Libraries
URL:            https://metacpan.org/pod/distribution/Net-SSLeay/lib/Net/SSLeay.pod
Source:         https://cpan.metacpan.org/modules/by-module/Net/Net-SSLeay-%{version}.tar.gz
%if 0%{?with_fips:1}
Source100:      openssl-fips-2.0.9-lin64.tar.gz
%endif
Vendor:         Microsoft Corporation
Distribution:   Mariner
Requires:       perl >= 5.28.0
Requires:       openssl
BuildRequires:  perl >= 5.28.0
BuildRequires:  openssl-devel

%description
Net::SSLeay module contains perl bindings to openssl (http://www.openssl.org) library.

Net::SSLeay module basically comprise of:
* High level functions for accessing web servers (by using HTTP/HTTPS)
* Low level API (mostly mapped 1:1 to openssl's C functions)
* Convenience functions (related to low level API but with more perl friendly interface)
* There is also a related module called Net::SSLeay::Handle included in this distribution that you might want to use instead. It has its own pod documentation.

%prep
%setup -q -n Net-SSLeay-%{version}

%build
%if 0%{?with_fips:1}
tar xf %{SOURCE100} --no-same-owner -C ..
# Do not package it to src.rpm
:> %{SOURCE100}
cp ../openssl-fips-2.0.9/include/openssl/fips.h /usr/include/openssl/
%endif
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete

%check
# Install required modules for test - Test::Pod, Test::Exception, Test::Warn and Test::NoWarnings
export PERL_MM_USE_DEFAULT=1
echo "yes" | cpan -a
cpan local::lib
cpan -i Test::Pod Test::Exception Test::Warn Test::NoWarnings
make test

%files
%license LICENSE
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Fri Nov 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.88-3
- Adding 'local::lib' perl5 library to fix test dependencies.

* Sat May 09 00:21:16 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.88-2
- Added %%license line automatically

*   Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 1.88-1
-   Update to version 1.88. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.85-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Dec 03 2018 Dweep Advani <dadvani@vmware.com> 1.85-3
-   Fixing makecheck tests
*   Wed Oct 17 2018 Alexey Makhalov <amakhalov@vmware.com> 1.85-2
-   Move fips logic to spec file
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.85-1
-   Update to version 1.85
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.81-2
-   Remove BuildArch
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.81-1
-   Update version to 1.81
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.72-2
-   GA - Bump release of all rpms
*   Mon Mar 28 2016 Mahmoud Bassiouny <mbassiounu@vmware.com> 1.72-1
-   Initial version.
