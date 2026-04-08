# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pipewire-media-session
Summary:        PipeWire reference session manager
Version:        0.4.3
Release:        1%{?dist}
License:        MIT
URL:            https://pipewire.org/
Source0:        https://gitlab.freedesktop.org/pipewire/media-session/-/archive/%{version}/media-session-%{version}.tar.gz

# Virtual Provides to support swapping between PipeWire session manager implementations
Provides:       pipewire-session-manager
Conflicts:      pipewire-session-manager

BuildRequires:  meson gcc pkgconfig
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.44
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  gettext
BuildRequires:  systemd-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros

Requires:       systemd

%description
Media Session is the reference session manager for the PipeWire media server.

%prep
%autosetup -p1 -n media-session-%{version}

%build
%meson \
    -Ddocs=disabled \
    -Dsystemd=enabled \
    -Dwith-module-sets=alsa,pulseaudio,jack
%meson_build

%install
%meson_install

%find_lang media-session

%posttrans
%systemd_user_post pipewire-media-session.service

%preun
%systemd_user_preun pipewire-media-session.service

%files -f media-session.lang
%license LICENSE COPYING
%doc README.md
%{_bindir}/pipewire-media-session
%{_userunitdir}/pipewire-media-session.service
%dir %{_datadir}/pipewire/media-session.d/
%{_datadir}/pipewire/media-session.d/alsa-monitor.conf
%{_datadir}/pipewire/media-session.d/bluez-monitor.conf
%{_datadir}/pipewire/media-session.d/media-session.conf
%{_datadir}/pipewire/media-session.d/v4l2-monitor.conf

%{_datadir}/pipewire/media-session.d/with-alsa
%{_datadir}/pipewire/media-session.d/with-jack
%{_datadir}/pipewire/media-session.d/with-pulseaudio

%changelog
* Thu Jul 31 2025 Wim Taymans <wtaymans@redhat.com> 0.4.3-1
- media-session 0.4.3

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 28 2023 Peter Hutterer <peter.hutterer@redhat.com>
- SPDX migration: mark as done

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 10 2023 Wim Taymans <wtaymans@redhat.com> 0.4.2-1
- media-session 0.4.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 17 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.1-3
- Move the systemd scriptlet to posttrans so we can dnf swap with
  wireplumber (#2022584)

* Tue Nov 09 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.1-2
- BuildRequire pipewire 0.3.39

* Wed Oct 27 2021 Peter Hutterer <peter.hutterer@redhat.com> 0.4.1-1
- media-session 0.4.1

* Tue Oct 19 2021 Peter Hutterer <peter.hutterer@redhat.com> 0.4.0-1
- Initial package import after split from pipewire (#2016247)
