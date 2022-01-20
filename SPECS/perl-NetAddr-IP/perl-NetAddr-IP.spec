Summary:        Manages IPv4 and IPv6 addresses and subnets
Name:           perl-NetAddr-IP
Version:        4.079
Release:        5%{?dist}
License:        GPLv2+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/NetAddr-IP
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MIKER/NetAddr-IP-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  perl
BuildRequires:  perl-generators

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Math::BigInt)

Provides:       perl(NetAddr::IP) = %{version}-%{release}
Provides:       perl(NetAddr::IP::InetBase) = %{version}-%{release}
Provides:       perl(NetAddr::IP::Lite) = %{version}-%{release}
Provides:       perl(NetAddr::IP::Util) = %{version}-%{release}
Provides:       perl(NetAddr::IP::UtilPP) = %{version}-%{release}
Provides:       perl(NetAddr::IP::UtilPolluted) = %{version}-%{release}
Provides:       perl(NetAddr::IP::Util_IS) = %{version}-%{release}

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
%license Artistic Copying
%{perl_vendorarch}/*
%{_mandir}/man3/*

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.079-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 4.079-4
- Use new perl package names.
- Change perl_vendorlib to perl_vendorarch directory for packaging.
- Provide perl(NetAddr::IP*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.079-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.079-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.079-1
- Initial version.
