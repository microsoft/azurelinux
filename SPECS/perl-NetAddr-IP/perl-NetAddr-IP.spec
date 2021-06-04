Summary:        Manages IPv4 and IPv6 addresses and subnets
Name:           perl-NetAddr-IP
Version:        4.079
Release:        3%{?dist}
License:        GPLv2+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/NetAddr-IP
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MIKER/NetAddr-IP-%{version}.tar.gz
%define sha1    NetAddr-IP=41f0048dccf016077e65b93a681e40b4f6b28336
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  perl
Requires:       perl

%description
This module provides an object-oriented abstraction on top of IP
addresses or IP subnets, that allows for easy manipulations.

%prep
%setup -q -n NetAddr-IP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%license Copying
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.079-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.079-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.079-1
-   Initial version.
