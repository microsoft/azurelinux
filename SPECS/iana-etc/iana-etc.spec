Summary:      Data for network services and protocols
Name:         iana-etc
Version:      2.30
Release:      5%{?dist}
License:      OSL 3.0
URL:          http://freshmeat.net/projects/iana-etc
Group:        System Environment/Base
Vendor:       Microsoft Corporation
Distribution: Mariner
BuildArch:    noarch
Source0:      http://anduin.linuxfromscratch.org/sources/LFS/lfs-packages/conglomeration//iana-etc/%{name}-%{version}.tar.bz2

%description
The Iana-Etc package provides data for network services and protocols.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%license COPYING
%config %_sysconfdir/protocols
%config %_sysconfdir/services

%changelog
*   Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.30-5
-   Adding the "%%license" macro.
*   Fri May 08 2020 Joe Schmitt <joschmit@microsoft.com> 2.30-4
-   Remove sha1 macro.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.30-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.30-2
-   GA - Bump release of all rpms
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.30-1
-   Initial build. First version
