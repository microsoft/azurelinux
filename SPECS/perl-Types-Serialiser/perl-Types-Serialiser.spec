# Got the intial spec from Fedora and modified it
Summary:	Simple data types for common serialization formats
Name:		perl-Types-Serialiser
Version:	1.01
Release:    1%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Types-Serialiser/
Source0:	http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Types-Serialiser-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:	noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl-common-sense
BuildRequires:  perl(ExtUtils::MakeMaker)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl-common-sense

Provides:       perl(Types::Serialiser) = %{version}-%{release}
Provides:       perl(Types::Serialiser::BooleanBase) = %{version}-%{release}
Provides:       perl(Types::Serialiser::Error) = %{version}-%{release}

# Filter bogus provide of JSON::PP::Boolean (for rpm ≥ 4.9)
%global __provides_exclude ^perl\\(JSON::PP::Boolean\\)

%description
This module provides some extra data types that are used by common
serialization formats such as JSON or CBOR. The idea is to have a repository of
simple/small constants and containers that can be shared by different
implementations so they become interoperable between each other.

%prep
%setup -q -n Types-Serialiser-%{version}

# Filter bogus provide of JSON::PP::Boolean (for rpm < 4.9)
%global provfilt /bin/sh -c "%{__perl_provides} | grep -v '^perl(JSON::PP::Boolean)'"
%define __perl_provides %{provfilt}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%files
%license COPYING
%{perl_vendorlib}/Types/
%{_mandir}/man3/*

%changelog
* Thu Feb 01 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 1.01-1
- Auto-upgrade to 1.01 - Azure Linux 3.0 - package upgrades

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-8
- Adding 'BuildRequires: perl-generators'.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-7
- Removing the explicit %%clean stage.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.0-6
- Use new perl package names.
- Provide perl(Types::Serialiser*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0-5
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.0-3
- Consuming perl version upgrade of 5.28.0

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-2
- GA - Bump release of all rpms

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.0-1
- Initial version.
