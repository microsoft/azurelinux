Summary:        SSL sockets with IO::Socket interface
Name:           perl-IO-Socket-SSL
Version:        2.066
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/IO-Socket-SSL
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-Socket-SSL-%{version}.tar.gz
Source1:        LICENSE.PTR
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
Requires:       perl >= 5.28.0
Requires:       perl-Net-SSLeay
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-Net-SSLeay

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
make test

%files
%license LICENSE.PTR
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
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
