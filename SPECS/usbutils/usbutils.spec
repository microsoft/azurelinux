Summary:       USB Utils
Name:          usbutils
Version:       010
Release:       3%{?dist}
License:       GPLv2+
URL:           http://linux-usb.sourceforge.net
Group:         Applications/System
Vendor:        Microsoft Corporation
Distribution:  Mariner
Source0:       https://www.kernel.org/pub/linux/utils/usb/usbutils/%{name}-%{version}.tar.xz
Source1:       usb.ids
Source2:       LICENSE.PTR
BuildRequires: libusb-devel
BuildRequires: pkg-config
BuildRequires: systemd
Requires:      libusb
BuildRequires: systemd-devel

%description
The USB Utils package contains an utility used to display information
about USB buses in the system and the devices connected to them.

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=/usr \
            --datadir=/usr/share/misc \
            --disable-zlib &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_datadir}/misc/
install -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/misc/

cp %{SOURCE2} .

%files
%defattr(-,root,root,-)
%license LICENSE.PTR
%{_bindir}/usb-devices
%{_bindir}/lsusb
%{_bindir}/lsusb.py
%{_bindir}/usbhid-dump
%{_mandir}/*/*
%{_datadir}/misc/usb.ids

%changelog
*   Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 010-3
-   Adding a license reference.
-   License verified.
-   Removed "sha1" macro.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 010-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com>  010-1
-   Update version to 010.
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  008-4
-   Change systemd dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 008-3
-   GA - Bump release of all rpms
*   Tue May 10 2016 Nick Shi <nshi@vmware.com> - 008-2
-   Update Source0 to the correct link
*   Fri May 06 2016 Nick Shi <nshi@vmware.com> - 008-1
-   Initial version
