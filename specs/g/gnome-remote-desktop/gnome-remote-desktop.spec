## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global systemd_unit_handover gnome-remote-desktop-handover.service
%global systemd_unit_headless gnome-remote-desktop-headless.service
%global systemd_unit_system gnome-remote-desktop.service
%global systemd_unit_user gnome-remote-desktop.service

%global tarball_version %%(echo %{version} | tr '~' '.')

%bcond rdp %[0%{?fedora} || 0%{?rhel} >= 10]
%bcond vnc %[0%{?fedora} || 0%{?rhel} < 10]

%global libei_version 1.0.901
%global pipewire_version 0.3.49

Name:           gnome-remote-desktop
Version:        49.3
Release:        %autorelease
Summary:        GNOME Remote Desktop screen share service

License:        GPL-2.0-or-later
URL:            https://gitlab.gnome.org/GNOME/gnome-remote-desktop
Source0:        https://download.gnome.org/sources/%{name}/49/%{name}-%{tarball_version}.tar.xz

# Adds encryption support (requires patched LibVNCServer)
Patch0:         gnutls-anontls.patch

BuildRequires:  asciidoc
BuildRequires:  gcc
BuildRequires:  meson >= 0.47.0
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(ffnvcodec)
%if %{with rdp}
BuildRequires:  glslc
BuildRequires:  spirv-tools
BuildRequires:  pkgconfig(fdk-aac)
BuildRequires:  pkgconfig(freerdp3)
BuildRequires:  pkgconfig(fuse3)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(winpr3)
%endif
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glib-2.0) >= 2.68
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libei-1.0) >= %{libei_version}
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libsecret-1)
%if %{with vnc}
BuildRequires:  pkgconfig(libvncserver) >= 0.9.11-7
%endif
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(tss2-esys)
BuildRequires:  pkgconfig(tss2-mu)
BuildRequires:  pkgconfig(tss2-rc)
BuildRequires:  pkgconfig(tss2-tctildr)

Requires:       libei%{?_isa} >= %{libei_version}
Requires:       pipewire%{?_isa} >= %{pipewire_version}

Obsoletes:      vino < 3.22.0-21

%description
GNOME Remote Desktop is a remote desktop and screen sharing service for the
GNOME desktop environment.


%prep
%autosetup -p1 -n %{name}-%{tarball_version}


%build
%meson \
%if %{with rdp}
    -Drdp=true \
%else
    -Drdp=false \
%endif
%if %{with vnc}
    -Dvnc=true \
%else
    -Dvnc=false \
%endif
    -Dsystemd=true \
    -Dtests=false
%meson_build


%install
%meson_install

%find_lang %{name}


%post
%systemd_post %{systemd_unit_system}
%systemd_user_post %{systemd_unit_handover}
%systemd_user_post %{systemd_unit_headless}
%systemd_user_post %{systemd_unit_user}


%preun
%systemd_preun %{systemd_unit_system}
%systemd_user_preun %{systemd_unit_handover}
%systemd_user_preun %{systemd_unit_headless}
%systemd_user_preun %{systemd_unit_user}


%postun
%systemd_postun_with_restart %{systemd_unit_system}
%systemd_user_postun_with_restart %{systemd_unit_handover}
%systemd_user_postun_with_restart %{systemd_unit_headless}
%systemd_user_postun_with_restart %{systemd_unit_user}


%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/grdctl
%{_libexecdir}/gnome-remote-desktop-daemon
%{_libexecdir}/gnome-remote-desktop-enable-service
%{_libexecdir}/gnome-remote-desktop-configuration-daemon
%{_userunitdir}/%{systemd_unit_user}
%{_userunitdir}/%{systemd_unit_headless}
%{_userunitdir}/%{systemd_unit_handover}
%{_unitdir}/%{systemd_unit_system}
%{_unitdir}/gnome-remote-desktop-configuration.service
%{_datadir}/applications/org.gnome.RemoteDesktop.Handover.desktop
%{_datadir}/dbus-1/system-services/org.gnome.RemoteDesktop.Configuration.service
%{_datadir}/dbus-1/system.d/org.gnome.RemoteDesktop.conf
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.enums.xml
%{_datadir}/polkit-1/actions/org.gnome.remotedesktop.configure-system-daemon.policy
%{_datadir}/polkit-1/actions/org.gnome.remotedesktop.enable-system-daemon.policy
%{_datadir}/polkit-1/rules.d/20-gnome-remote-desktop.rules
%{_sysusersdir}/gnome-remote-desktop-sysusers.conf
%{_tmpfilesdir}/gnome-remote-desktop-tmpfiles.conf

%if %{with rdp}
%{_datadir}/gnome-remote-desktop/
%endif
%{_mandir}/man1/grdctl.1*


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 49.3-2
- Latest state for gnome-remote-desktop

* Mon Feb 16 2026 Jonas Ådahl <jadahl@redhat.com> - 49.3-1
- Update to 49.3

* Wed Dec 10 2025 Adrian Vovk <adrianvovk@gmail.com> - 49.2-1
- Update to 49.2

* Thu Oct 16 2025 Petr Schindler <pschindl@redhat.com> - 49.1-1
- Update to 49.1

* Tue Sep 16 2025 Jonas Ådahl <jadahl@redhat.com> - 49.0-1
- Bump version to 49.0

* Tue Sep 16 2025 Gordon Messmer <gordon.messmer@gmail.com> - 49~alpha-4
- Examine the server process GOT for signs of tampering.

* Fri Aug 29 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49~alpha-3
- Fix changelog and use %%autorelease

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 49~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-1
- Update to 49.alpha

* Mon Apr 14 2025 nmontero <nmontero@redhat.com> - 48.1-1
- Update to 48.1

* Thu Mar 20 2025 nmontero <nmontero@redhat.com> - 48.0-1
- Update to 48.0

* Thu Mar 06 2025 Fabio Valentini <decathorpe@gmail.com> - 48~rc-1
- Update to 48.rc

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 47.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 25 2024 nmontero <nmontero@redhat.com> - 47.2-1
- Update to 47.2

* Tue Oct 22 2024 nmontero <nmontero@redhat.com> - 47.1-1
- Update to 47.1

* Tue Sep 17 2024 nmontero <nmontero@redhat.com> - 47.0-1
- Update to 47.0

* Sun Sep 01 2024 David King <amigadave@amigadave.com> - 47~rc-1
- Update to 47.rc

* Wed Aug 14 2024 nmontero <nmontero@redhat.com> - 47~beta-1
- Update to 47~beta

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 47~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 David King <amigadave@amigadave.com> - 47~alpha-1
- Update to 47.alpha

* Mon May 27 2024 Nieves Montero <nmontero@redhat.com> - 46.2-2
- Update to 46.2

* Thu May 23 2024 Nieves Montero <nmontero@redhat.com> - 46.2-1
- Update to 46.2

* Thu Apr 18 2024 David King <amigadave@amigadave.com> - 46.1-1
- Update to 46.1

* Thu Mar 28 2024 Adam Williamson <awilliam@redhat.com> - 46.0-2
- Correct systemd macros

* Tue Mar 26 2024 Jonas Ådahl <jadahl@redhat.com> - 46.0-1
- Bump version to 46.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 45.1-2
- Disable VNC in RHEL 10+

* Sun Oct 22 2023 Kalev Lember <klember@redhat.com> - 45.1-1
- Update to 45.1

* Sat Oct 21 2023 Kalev Lember <klember@redhat.com> - 45.0-1
- Update to 45.0

* Wed Sep 06 2023 Kalev Lember <klember@redhat.com> - 45.rc-2
- Add minimum required libei version

* Tue Sep 05 2023 Kalev Lember <klember@redhat.com> - 45.rc-1
- Update to 45.rc

* Fri Aug 11 2023 Kalev Lember <klember@redhat.com> - 45.beta-1
- Update to 45.beta

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 45.alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Jonas Ådahl <jadahl@redhat.com> - 45.alpha-2
- Add missing function definition in TLS patch

* Wed Jul 05 2023 Jonas Ådahl <jadahl@redhat.com> - 45.alpha-1
- Update to 45.alpha

* Wed May 31 2023 Kalev Lember <klember@redhat.com> - 44.2-1
- Update to 44.2

* Mon Apr 24 2023 David King <amigadave@amigadave.com> - 44.1-1
- Update to 44.1

* Sun Mar 19 2023 David King <amigadave@amigadave.com> - 44.0-1
- Update to 44.0

* Thu Mar 16 2023 Jonas Ådahl <jadahl@redhat.com> - 44~rc-2
- Enable RDP in ELN

* Sun Mar 05 2023 David King <amigadave@amigadave.com> - 44~rc-1
- Update to 44.rc

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 44~alpha-1
- Update to 44.alpha

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 43.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 David King <amigadave@amigadave.com> - 43.2-1
- Update to 43.2

* Tue Nov 08 2022 Stephen Gallagher <sgallagh@redhat.com> - 43.1-2
- Fix build on RHEL 9+/ELN

* Thu Oct 27 2022 David King <amigadave@amigadave.com> - 43.1-1
- Update to 43.1

* Tue Sep 20 2022 Jonas Ådahl <jadahl@redhat.com> - 43.0-1
- Bump version to 43.0

* Thu Aug 18 2022 Jonas Ådahl <jadahl@redhat.com> - 43~beta-6
- Drop dependency on tpm2-abrmd

* Tue Aug 16 2022 Kalev Lember <klember@redhat.com> - 43~beta-5
- Avoid manual requires on tss2* and rely on automatic soname deps instead

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 43~beta-4
- Add missing build requirement

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 43~beta-3
- Rebuild for updated FreeRDP

* Thu Aug 11 2022 Jonas Ådahl <jadahl@redhat.com> - 43~beta-2
- Fix typo

* Thu Aug 11 2022 Jonas Ådahl <jadahl@redhat.com> - 43~beta-1
- Bump version to gnome-remote-desktop-43.beta

* Fri Jul 29 2022 Tomas Popela <tpopela@redhat.com> - 43~alpha-3
- Don't enable RDP support in ELN/RHEL 9+

* Thu Jul 28 2022 Jonas Ådahl <jadahl@redhat.com> - 43~alpha-2
- README -> README.md

* Thu Jul 28 2022 Jonas Ådahl <jadahl@redhat.com> - 43~alpha-1
- Update to 43.alpha

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 David King <amigadave@amigadave.com> - 42.3-1
- Update to 43.3 (#2091415)

* Sun May 29 2022 David King <amigadave@amigadave.com> - 42.2-1
- Update to 42.2

* Wed May 11 2022 David King <amigadave@amigadave.com> - 42.1.1-1
- Update to 42.1.1 (#2061546)

* Wed Apr 27 2022 David King <amigadave@amigadave.com> - 42.1-3
- Update sources

* Wed Apr 27 2022 David King <amigadave@amigadave.com> - 42.1-2
- Fix isa macro in Requires

* Tue Apr 26 2022 David King <amigadave@amigadave.com> - 42.1-1
- Update to 42.1 (#2061546)

* Mon Mar 21 2022 Jonas Ådahl <jadahl@redhat.com> - 42.0-1
- Update to 42.0

* Mon Mar 14 2022 Jonas Ådahl <jadahl@redhat.com> - 42~rc-5
- Fix path to man page

* Mon Mar 14 2022 Jonas Ådahl <jadahl@redhat.com> - 42~rc-4
- Fix path to grdctl

* Mon Mar 14 2022 Jonas Ådahl <jadahl@redhat.com> - 42~rc-3
- Add missing patch

* Mon Mar 14 2022 Jonas Ådahl <jadahl@redhat.com> - 42~rc-2
- Add man page

* Mon Mar 14 2022 Jonas Ådahl <jadahl@redhat.com> - 42~rc-1
- Update to 42.rc

* Wed Feb 16 2022 Jonas Ådahl <jadahl@redhat.com> - 42~beta-3
- Add build requirements needed for tests

* Wed Feb 16 2022 Jonas Ådahl <jadahl@redhat.com> - 42~beta-2
- Add missing added dependencies

* Wed Feb 16 2022 Jonas Ådahl <jadahl@redhat.com> - 42~beta-1
- Update to 42.beta

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 41.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 08 2021 Jonas Ådahl <jadahl@redhat.com> - 41.2-1
- Update to 41.2

* Mon Nov 01 2021 Kalev Lember <klember@redhat.com> - 41.1-1
- Update to 41.1

* Mon Sep 20 2021 Kalev Lember <klember@redhat.com> - 41.0-1
- Update to 41.0

* Wed Sep 08 2021 Kalev Lember <klember@redhat.com> - 41~rc-2
- Fix the build

* Tue Sep 07 2021 Jonas Ådahl <jadahl@redhat.com> - 41~rc-1
- Bump to 41.rc

* Wed Aug 04 2021 Kalev Lember <klember@redhat.com> - 40.1-5
- Bump release

* Wed Aug 04 2021 Kalev Lember <klember@redhat.com> - 40.1-4
- Remove old, unused tarball from sources file

* Wed Aug 04 2021 Kalev Lember <klember@redhat.com> - 40.1-3
- Avoid systemd_requires as per updated packaging guidelines

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 03 2021 Jonas Ådahl <jadahl@redhat.com> - 40.1-1
- Bump to 40.1

* Thu Apr 15 2021 Simone Caronni <negativo17@gmail.com> - 40.0-3
- Rebuild for updated FreeRDP

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-2
- Use macro for converting between GNOME and Fedora pre-release versioning

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Thu Mar 18 2021 Michael Catanzaro <mcatanzaro@gnome.org> - 40.0~rc-2
- Add Obsoletes: vino

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40.0~rc-1
- Update to 40.rc

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40.0~beta-2
- Fix rpmbuild changelog chronological order warning

* Fri Mar 05 2021 Jonas Ådahl <jadahl@redhat.com> - 40.0~beta-1
- Bump to 40.beta

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 12 2020 Jonas Ådahl <jadahl@redhat.com> - 0.1.9-2
- Copy using the right destination stride

* Mon Sep 14 2020 Jonas Ådahl <jadahl@redhat.com> - 0.1.9-1
- Update gnome-remote-desktop
- Update to 0.1.9
- Backport race condition crash fix
- Rebase anon-tls patches
- Cleanup left-over patches

* Thu Aug 27 2020 Ray Strode <rstrode@redhat.com> - 0.1.8-6
- add missing changelog entry

* Thu Aug 27 2020 Ray Strode <rstrode@redhat.com> - 0.1.8-5
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
