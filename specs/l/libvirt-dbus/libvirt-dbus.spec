# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*- rpm-spec -*-

%global meson_version 0.49.0
%global glib2_version 2.44.0
%global libvirt_version 3.1.0
%global libvirt_glib_version 0.0.7
%global system_user libvirtdbus

Name: libvirt-dbus
Version: 1.4.1
Release: 9%{?dist}
Summary: libvirt D-Bus API binding
License: LGPL-2.1-or-later
URL: https://libvirt.org/
Source0: https://libvirt.org/sources/dbus/%{name}-%{version}.tar.xz

BuildRequires: gcc
BuildRequires: meson >= %{meson_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libvirt-devel >= %{libvirt_version}
BuildRequires: libvirt-glib-devel >= %{libvirt_glib_version}
BuildRequires: python3-docutils
BuildRequires: systemd-rpm-macros
BuildRequires: systemd

Requires: dbus
Requires: glib2 >= %{glib2_version}
Requires: libvirt-libs >= %{libvirt_version}
Requires: libvirt-glib >= %{libvirt_glib_version}
Requires: polkit


%description
This package provides D-Bus API for libvirt

%prep
%autosetup

# Create a sysusers.d config file
cat >libvirt-dbus.sysusers.conf <<EOF
u libvirtdbus - 'Libvirt D-Bus bridge' - -
EOF

%build
%meson \
    -Dinit_script=systemd
%meson_build

%install
%meson_install

install -m0644 -D libvirt-dbus.sysusers.conf %{buildroot}%{_sysusersdir}/libvirt-dbus.conf


%post
%systemd_post %{name}.service
%systemd_user_post %{name}.service

%preun
%systemd_preun %{name}.service
%systemd_user_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%systemd_user_postun_with_restart %{name}.service

%files
%doc AUTHORS.rst NEWS.rst
%license COPYING
%{_sbindir}/libvirt-dbus
%{_unitdir}/libvirt-dbus.service
%{_userunitdir}/libvirt-dbus.service
%{_datadir}/dbus-1/services/org.libvirt.service
%{_datadir}/dbus-1/system-services/org.libvirt.service
%{_datadir}/dbus-1/system.d/org.libvirt.conf
%{_datadir}/dbus-1/interfaces/org.libvirt.*.xml
%{_datadir}/polkit-1/rules.d/libvirt-dbus.rules
%{_mandir}/man8/libvirt-dbus.8*
%{_sysusersdir}/libvirt-dbus.conf

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.1-7
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-2
- Synchronize spec file with upstream

* Mon Oct 30 2023 Ladar Levison <ladar@lavabit.com> - 1.4.1-1
- Update to 1.4.1 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Pavel Hrdina <phrdina@redhat.com> - 1.4.0-1
- Update to 1.4.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Pavel Hrdina <phrdina@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Wed Aug 29 2018 Pavel Hrdina <phrdina@redhat.com> - 1.2.0-1
- Update to 1.2.0 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Pavel Hrdina <phrdina@redhat.com> - 1.1.0-1
- Update to 1.1.0 release

* Thu May 17 2018 Pavel Hrdina <phrdina@redhat.com> - 1.0.0-1
- Update to 1.0.0 release

* Tue Mar 27 2018 Pavel Hrdina <phrdina@redhat.com> - 0.0.1-1
- Initial RPM build
