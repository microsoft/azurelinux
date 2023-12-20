Summary:        USB Utils
Name:           usbutils
Version:        017
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            http://linux-usb.sourceforge.net
Source0:        https://www.kernel.org/pub/linux/utils/usb/usbutils/%{name}-%{version}.tar.xz
Source1:        usb.ids
BuildRequires:  libusb-devel
BuildRequires:  pkg-config
BuildRequires:  systemd
BuildRequires:  systemd-devel
Requires:       libusb

%description
The USB Utils package contains an utility used to display information
about USB buses in the system and the devices connected to them.

%prep
%autosetup -p1

%build
./configure --prefix=%{_prefix} \
            --datadir=%{_datadir}/misc \
            --disable-zlib &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_datadir}/misc/
install -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/misc/
# Remove the pkgconfig file
rm -rf %{buildroot}/%{_libdir}/pkgconfig/usbutils.pc

%files
%defattr(-,root,root,-)
%license LICENSES/GPL*
%{_bindir}/usb-devices
%{_bindir}/lsusb
%{_bindir}/lsusb.py
%{_bindir}/usbhid-dump
%{_mandir}/*/*
%{_datadir}/misc/usb.ids

%changelog
* Mon Dec 18 2023 Rachel Menge <rachelmenge@microsoft.com> - 017-1
- Update to 017 release

* Wed Feb 02 2022 Chris Co <chrco@microsoft.com> - 014-1
- Update to 014 release
- License shipped upstream now.
- License verified

* Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 010-3
- Adding a license reference.
- License verified.
- Removed "sha1" macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 010-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> - 010-1
- Update version to 010.

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 008-4
- Change systemd dependency

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 008-3
- GA - Bump release of all rpms

* Tue May 10 2016 Nick Shi <nshi@vmware.com> - 008-2
- Update Source0 to the correct link

* Fri May 06 2016 Nick Shi <nshi@vmware.com> - 008-1
- Initial version
