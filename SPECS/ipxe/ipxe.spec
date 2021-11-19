%global security_hardening none
%define debug_package %{nil}

Summary:        iPXE open source boot firmware
Name:           ipxe
Version:        1.21.1
Release:        1%{?dist}
License:        GPLv2
URL:            https://ipxe.org
Source0:        https://github.com/ipxe/ipxe/archive/%{name}-%{version}.tar.gz
#Source0:        https://github.com/ipxe/ipxe/archive/v%{version}.tar.gz
Group:          System Environment/Daemons
Vendor:         Microsoft Corporation
Distribution:   Mariner
ExclusiveArch:  x86_64
BuildRequires:  cdrkit
BuildRequires:  perl

%description
iPXE is the leading open source network boot firmware. It provides a full
PXE implementation enhanced with additional features.

%prep
%setup -q

%build
cd src
make %{_smp_mflags} NO_WERROR=1 V=1

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}/usr/share/ipxe
install -vDm 644 src/bin/ipxe.{dsk,iso,lkrn,usb} %{buildroot}/usr/share/ipxe/
install -vDm 644 src/bin/*.{rom,mrom} %{buildroot}/usr/share/ipxe/

%files
%defattr(-,root,root)
%license COPYING
/usr/share/ipxe/ipxe.dsk
/usr/share/ipxe/ipxe.iso
/usr/share/ipxe/ipxe.lkrn
/usr/share/ipxe/ipxe.usb
/usr/share/ipxe/10222000.rom
/usr/share/ipxe/10500940.rom
/usr/share/ipxe/10ec8139.rom
/usr/share/ipxe/15ad07b0.rom
/usr/share/ipxe/1af41000.rom
/usr/share/ipxe/8086100e.mrom
/usr/share/ipxe/8086100f.mrom
/usr/share/ipxe/808610d3.mrom
/usr/share/ipxe/80861209.rom
/usr/share/ipxe/rtl8139.rom

%changelog
*   Wed Nov 10 2021 Andrew Phelps <anphel@microsoft.com> 1.21.1-1
-   Update version. Remove unnecessary BR. Modify to build with gcc11.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.20.1-3
-   Added %%license line automatically
*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 1.20.1-2
-   Replace BuildArch with ExclusiveArch
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.20.1-1
-   Update to release tagged version 1.20.1 from date based versioning.
-   Verified license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 20180717-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 20180717-2
-   Adding BuildArch
*   Thu Oct 11 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 20180717-1
-   Use commit date instead of commit id as the package version.
*   Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> d2063b7-1
-   Update version to get it to build with gcc 7.3
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  553f485-2
-   disable debuginfo gen
*   Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 553f485-1
-   Version update to build with gcc-6.3
-   Removed linux/linux-devel build-time dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> ed0d7c4-2
-   GA - Bump release of all rpms
*   Thu Nov 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> ed0d7c4-1
-   Initial build. First version
