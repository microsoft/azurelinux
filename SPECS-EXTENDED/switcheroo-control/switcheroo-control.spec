Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           switcheroo-control
Version:        2.4
Release:        3%{?dist}
Summary:        D-Bus service to check the availability of dual-GPU

License:        GPLv3
URL:            https://gitlab.freedesktop.org/hadess/switcheroo-control/
# URL from https://gitlab.freedesktop.org/hadess/switcheroo-control/-/releases
Source0:        https://gitlab.freedesktop.org/hadess/switcheroo-control/uploads/accd4a9492979bfd91b587ae7e18d3a2/switcheroo-control-2.4.tar.xz

BuildRequires:  gcc
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  meson
BuildRequires:  systemd
BuildRequires:	systemd-devel

%{?systemd_requires}

%description
D-Bus service to check the availability of dual-GPU.

%prep
%autosetup


%build
%meson -Dgtk_doc=false
%meson_build


%install
%meson_install

%post
if [ $1 -eq 2 ] && [ -x /usr/bin/systemctl ] ; then
	/usr/bin/systemctl daemon-reload
fi
%systemd_post switcheroo-control.service
%udev_hwdb_update

%preun
%systemd_preun switcheroo-control.service

%postun
%systemd_postun_with_restart switcheroo-control.service
%udev_hwdb_update

%files
%license COPYING
%doc NEWS README.md
%{_bindir}/switcherooctl
%{_sysconfdir}/dbus-1/system.d/net.hadess.SwitcherooControl.conf
%{_unitdir}/switcheroo-control.service
%{_libexecdir}/switcheroo-control
%{_udevhwdbdir}/30-pci-intel-gpu.hwdb

%changelog
* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4-3
- Removing gtk-docs since they require a network connection.
- License verified.

* Tue Jun 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add BR:systemd-devel for pkgconfig files

* Mon Jan 04 2021 Bastien Nocera <bnocera@redhat.com> - 2.4-1
+ switcheroo-control-2.4-1
- Update to 2.4

* Mon Apr 27 2020 Bastien Nocera <bnocera@redhat.com> - 2.2-1
+ switcheroo-control-2.2-1
- Update to 2.2

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Bastien Nocera <bnocera@redhat.com> - 2.1-1
+ switcheroo-control-2.1-1
- Update to 2.1
- Fix crasher on startup (#1786846)

* Thu Nov 21 2019 Bastien Nocera <bnocera@redhat.com> - 2.0-2
+ switcheroo-control-2.0-2
- Fix post scripts not reloading service file

* Tue Nov 05 2019 Bastien Nocera <bnocera@redhat.com> - 2.0-1
+ switcheroo-control-2.0-1
- Update to 2.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Bastien Nocera <bnocera@redhat.com> - 1.3.1-1
+ switcheroo-control-1.3.1-1
- Fix Secure Boot work-around

* Wed Jun 12 2019 Bastien Nocera <bnocera@redhat.com> - 1.3-1
+ switcheroo-control-1.3-1
- Update to 1.3
- Fix operation with SecureBoot enabled

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Bastien Nocera <bnocera@redhat.com> - 1.1-1
+ switcheroo-control-1.1-1
- Update to 1.1
- Don't throw errors when the machine doesn't have dual-GPU (#1391212)

* Fri Oct 21 2016 Kalev Lember <klember@redhat.com> - 1.0-1
- Initial Fedora packaging
