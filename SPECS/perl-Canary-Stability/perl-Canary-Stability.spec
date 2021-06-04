Summary:        Canary to check perl compatibility for Schmorp's modules
Name:           perl-Canary-Stability
Version:        2012
Release:        4%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Canary-Stability/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Canary-Stability-%{version}.tar.gz
%define sha1 Canary-Stability=9d3c5476081da9200ef59cacafea55bd011b6d8a
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
Requires:       perl >= 5.28.0

%description
This module is used by Schmorp's modules during configuration stage to test
the installed perl for compatibility with his modules.

%prep
%setup -q -n Canary-Stability-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%license COPYING
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2012-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2012-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2012-2
-   Consuming perl version upgrade of 5.28.0
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 2012-1
-   Initial version.
