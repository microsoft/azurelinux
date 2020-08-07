Name:           kexec-tools
Summary:        The kexec kdump tools
Version:        2.0.19
Release:        3%{?dist}
License:        GPLv2
Group:          Applications/System
Url:            https://www.kernel.org/doc/Documentation/kdump/kdump.txt
Source0:        https://www.kernel.org/pub/linux/utils/kernel/kexec/%{name}-%{version}.tar.xz
Patch0:		kexec-tools-disable-test.patch
Vendor:         Microsoft Corporation
Distribution:   Mariner
ExclusiveArch:  x86_64
BuildRequires:  zlib-devel
BuildRequires:  zlib
Requires:	zlib

%description
kexec-tools allows booting of a linux kernel from the context of a running kernel using kernel's kexec feature

%prep
%setup -q
%patch0 -p1

%build
%configure
make

%install
make install DESTDIR=%{buildroot}

%files
%license COPYING
%{_sbindir}/*
%{_mandir}/man8/*
%doc News
%doc COPYING
%doc TODO

%changelog
* Sat May 09 00:21:32 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.0.19-3
- Added %%license line automatically

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 2.0.19-2
-   Replace BuildArch with ExclusiveArch
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 2.0.19-1
-   Update to 2.0.19. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0.17-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 2.0.17-2
-   Adding BuildArch
*   Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 2.0.17-1
-   Version update to fix compilation issue againts glibc-2.28
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.14-1
-   Updated to version 2.0.14
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.11-2
-   GA - Bump release of all rpms
*   Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com>  2.0.11-1
-   Initial version
