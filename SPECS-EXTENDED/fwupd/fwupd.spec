Summary:        Firmware update daemon
Name:           fwupd
Version:        2.0.1
Release:        2%{?dist}
License:        LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/fwupd/fwupd
Source0:        https://github.com/fwupd/fwupd/releases/download/%{version}/%{name}-%{version}.tar.xz

%global glib2_version 2.45.8
%global libxmlb_version 0.1.3
%global libusb_version 1.0.9
%global libcurl_version 7.62.0
%global libjcat_version 0.1.0
%global systemd_version 249
%global json_glib_version 1.1.1
%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '%{_sysconfdir}/bash_completion.d')

# although we ship a few tiny python files these are utilities that 99.99%
# of users do not need -- use this to avoid dragging python onto CoreOS
%global __requires_exclude ^%{python3}$
%global enable_tests 0
%global enable_docs 0

%global enable_dummy 1
# fwupd.efi is only available on these arches
%ifarch x86_64 aarch64 riscv64
%global have_uefi 1
%endif
# gpio.h is only available on these arches
%ifarch x86_64 aarch64
%global have_gpio 1
%endif
# flashrom is only available on these arches
%ifarch i686 x86_64 armv7hl aarch64 ppc64le riscv64
%global have_flashrom 1
%endif
%ifarch i686 x86_64
%global have_msr 1
%endif
# Until we actually have seen it outside x86
%ifarch i686 x86_64
%global have_thunderbolt 1
%endif
# only available recently
%global have_modem_manager 1
%global have_passim 1
BuildRequires:  freefont
BuildRequires:  gettext
%if 0%{?enable_docs}
BuildRequires:  gi-docgen
%endif
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  gnutls-devel
BuildRequires:  gnutls-utils
BuildRequires:  gobject-introspection-devel
BuildRequires:  json-glib-devel
BuildRequires:  libarchive-devel
BuildRequires:  libcbor-devel
BuildRequires:  libcurl-devel
BuildRequires:  libdrm-devel
BuildRequires:  libjcat
BuildRequires:  libjcat-devel
# JocelynB - reducing libusb1-devel to libusb-devel. This is required to avoid a conflict when bringing the usbutils dependency.
BuildRequires:  libusb-devel
BuildRequires:  libxmlb
BuildRequires:  libxmlb-devel
BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  polkit-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  python3-jinja2
BuildRequires:  python3-packaging
BuildRequires:  sqlite-devel
BuildRequires:  systemd
BuildRequires:  systemd-devel
# JocelynB - usbutils provides usb.ids that is required by the fwupd meson build system (without this, an error is produced on ARM)
BuildRequires:  usbutils
BuildRequires:  vala
BuildRequires:  pkgconfig(bash-completion)
Requires:       glib2%{?_isa}
Requires:       libusb%{?_isa}
Requires:       libxmlb%{?_isa}
Requires:       shared-mime-info
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd
Provides:       dbxtool
%if 0%{?have_passim}
BuildRequires:  passim-devel
%endif
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
BuildRequires:  valgrind-devel
%endif
%if 0%{?have_flashrom}
BuildRequires:  flashrom-devel
%endif
%if 0%{?have_modem_manager}
BuildRequires:  ModemManager-glib-devel
BuildRequires:  libmbim-devel
BuildRequires:  libqmi-devel
%endif
%if 0%{?have_uefi}
BuildRequires:  cairo-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  fontconfig
BuildRequires:  freetype
#BuildRequires:  google-noto-sans-cjk-ttc-fonts
BuildRequires:  pango-devel
BuildRequires:  python3
BuildRequires:  python3-cairo
BuildRequires:  python3-gobject
BuildRequires:  tpm2-tss-devel
%endif

%description
fwupd is a daemon to allow session software to update device firmware.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package tests
Summary:        Data files for installed tests
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tests
Data files for installed tests.

%if 0%{?have_modem_manager}
%package plugin-modem-manager
Summary:        fwupd plugin using ModemManger
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description plugin-modem-manager
This provides the optional package which is only required on hardware that
might have mobile broadband hardware. It is probably not required on servers.
%endif

%if 0%{?have_flashrom}
%package plugin-flashrom
Summary:        fwupd plugin using flashrom
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description plugin-flashrom
This provides the optional package which is only required on hardware that
can be flashed using flashrom. It is probably not required on servers.
%endif

%if 0%{?have_uefi}
%package plugin-uefi-capsule-data
Summary:        Localized data for the UEFI UX capsule
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description plugin-uefi-capsule-data
This provides the pregenerated BMP artwork for the UX capsule, which allows the
"Installing firmware update…" localized text to be shown during a UEFI firmware
update operation. This subpackage is probably not required on embedded hardware
or server machines.
%endif

%prep
%autosetup -p1

%build

%meson \
    -Dumockdev_tests=disabled \
%if 0%{?enable_docs}
    -Ddocs=enabled \
%else
    -Ddocs=disabled \
%endif
    -Dlvfs=disabled \
%if 0%{?enable_tests}
    -Dtests=true \
%else
    -Dtests=false \
%endif
%if 0%{?have_flashrom}
    -Dplugin_flashrom=enabled \
%else
    -Dplugin_flashrom=disabled \
%endif
%if 0%{?have_msr}
    -Dplugin_msr=enabled \
%else
    -Dplugin_msr=disabled \
%endif
%if 0%{?have_gpio}
    -Dplugin_gpio=enabled \
%else
    -Dplugin_gpio=disabled \
%endif
%if 0%{?have_uefi}
    -Dplugin_uefi_capsule=enabled \
    -Dplugin_uefi_pk=enabled \
    -Dplugin_tpm=enabled \
    -Defi_binary=false \
%else
    -Dplugin_uefi_capsule=disabled \
    -Dplugin_uefi_pk=disabled \
    -Dplugin_tpm=disabled \
%endif
%if 0%{?have_modem_manager}
    -Dplugin_modem_manager=enabled \
%else
    -Dplugin_modem_manager=disabled \
%endif
%if 0%{?have_passim}
    -Dpassim=enabled \
%else
    -Dpassim=disabled \
%endif
    -Dman=true \
    -Dsystemd_unit_user="" \
    -Dbluez=enabled \
    -Dplugin_powerd=disabled \
    -Dlaunchd=disabled \
    -Dsupported_build=enabled

%meson_build

%if 0%{?enable_tests}
%check
%meson_test
%endif

%install
%meson_install

mkdir -p --mode=0700 %{buildroot}%{_localstatedir}/lib/fwupd/gnupg

# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1757948
mkdir -p %{buildroot}%{_localstatedir}/cache/fwupd

%find_lang %{name}

%post
%systemd_post fwupd.service fwupd-refresh.timer

%preun
%systemd_preun fwupd.service fwupd-refresh.timer

%postun
%systemd_postun_with_restart fwupd.service fwupd-refresh.timer

%files -f %{name}.lang
%doc README.md
%license COPYING
%config(noreplace)%{_sysconfdir}/fwupd/fwupd.conf
%dir %{_libexecdir}/fwupd
%{_libexecdir}/fwupd/fwupd
%ifarch x86_64
%{_libexecdir}/fwupd/fwupd-detect-cet
%endif
%{_bindir}/dbxtool
%{_bindir}/fwupdmgr
%{_bindir}/fwupdtool
%dir %{_sysconfdir}/fwupd
%dir %{_sysconfdir}/fwupd/bios-settings.d
%{_sysconfdir}/fwupd/bios-settings.d/README.md
%dir %{_sysconfdir}/fwupd/remotes.d
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/vendor-directory.conf
%config(noreplace)%{_sysconfdir}/pki/fwupd
%{_sysconfdir}/pki/fwupd-metadata
%if 0%{?have_msr}
%{_libdir}/modules-load.d/fwupd-msr.conf
%endif
%{_datadir}/dbus-1/system.d/org.freedesktop.fwupd.conf
%{bash_completionsdir}/fwupdmgr
%{bash_completionsdir}/fwupdtool
%{_datadir}/fish/vendor_completions.d/fwupdmgr.fish
%dir %{_datadir}/fwupd
%dir %{_datadir}/fwupd/metainfo
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd*.metainfo.xml
%dir %{_datadir}/fwupd/remotes.d
%dir %{_datadir}/fwupd/remotes.d/vendor
%dir %{_datadir}/fwupd/remotes.d/vendor/firmware
%{_datadir}/fwupd/remotes.d/vendor/firmware/README.md
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_datadir}/polkit-1/actions/org.freedesktop.fwupd.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.fwupd.rules
%{_datadir}/dbus-1/system-services/org.freedesktop.fwupd.service
%{_mandir}/man1/fwupdtool.1*
%{_mandir}/man1/dbxtool.*
%{_mandir}/man1/fwupdmgr.1*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/metainfo/org.freedesktop.fwupd.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/org.freedesktop.fwupd.*
%{_datadir}/fwupd/firmware_packager.py
%{_datadir}/fwupd/simple_client.py
%{_datadir}/fwupd/add_capsule_header.py
%{_datadir}/fwupd/install_dell_bios_exe.py
%{_unitdir}/fwupd.service
%{_unitdir}/fwupd-refresh.service
%{_unitdir}/fwupd-refresh.timer
%dir %{_localstatedir}/lib/fwupd
%dir %{_localstatedir}/cache/fwupd
%dir %{_datadir}/fwupd/quirks.d
%{_datadir}/fwupd/quirks.d/builtin.quirk.gz
%if 0%{?enable_docs}
%{_docdir}/fwupd/*.html
%endif
%if 0%{?have_uefi}
%config(noreplace)%{_sysconfdir}/grub.d/35_fwupd
%endif
%{_libdir}/libfwupd.so.3*
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib
%{_libdir}/systemd/system-shutdown/fwupd.shutdown
%dir %{_libdir}/fwupd-%{version}
%{_libdir}/fwupd-%{version}/libfwupd*.so
%ghost %{_localstatedir}/lib/fwupd/gnupg

%if 0%{?have_modem_manager}
%files plugin-modem-manager
%{_libdir}/fwupd-%{version}/libfu_plugin_modem_manager.so
%endif

%if 0%{?have_flashrom}
%files plugin-flashrom
%{_libdir}/fwupd-%{version}/libfu_plugin_flashrom.so
%endif

%if 0%{?have_uefi}
%files plugin-uefi-capsule-data
%{_datadir}/fwupd/uefi-capsule-ux.tar.xz
%endif

%files devel
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%if 0%{?enable_docs}
%{_docdir}/fwupd/libfwupdplugin
%{_docdir}/fwupd/libfwupd
%{_docdir}/libfwupdplugin
%{_docdir}/libfwupd
%endif
%{_datadir}/vala/vapi
%{_includedir}/fwupd-3
%{_libdir}/libfwupd*.so
%{_libdir}/pkgconfig/fwupd.pc

%files tests
%if 0%{?enable_tests}
%{_datadir}/fwupd/host-emulate.d/*.json.gz
%{_datadir}/installed-tests/fwupd
# libgusb >= 0.4.5
%{_datadir}/fwupd/device-tests/*.json
%{_libexecdir}/installed-tests/fwupd
%{_datadir}/fwupd/remotes.d/fwupd-tests.conf
%endif

%changelog
* Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 2.0.1-2
- Integrating the spec into Azure Linux
- Initial CBL-Mariner import from Fedora 42 (license: MIT).
- License verified.

* Tue Oct 15 2024 Richard Hughes <richard@hughsie.com> - 2.0.1-1
- New upstream release

* Fri Oct 04 2024 Richard Hughes <richard@hughsie.com> - 2.0.0-3
- Fix build on s390x

* Fri Oct 04 2024 Richard Hughes <richard@hughsie.com> - 2.0.0-2
- No CET on i686

* Fri Oct 04 2024 Richard Hughes <richard@hughsie.com> - 2.0.0-1
- New upstream release

* Wed Sep 25 2024 Richard Hughes <richard@hughsie.com> - 1.9.25-1
- New upstream release

* Mon Aug 05 2024 Richard Hughes <richard@hughsie.com> - 1.9.23-1
- New upstream release

* Fri Jul 26 2024 Richard Hughes <richard@hughsie.com> - 1.9.22-1
- New upstream release

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 26 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.9.21-2
- Disable passim on RHEL

* Thu Jun 13 2024 Richard Hughes <richard@hughsie.com> - 1.9.21-1
- New upstream release

* Mon May 20 2024 Richard Hughes <richard@hughsie.com> - 1.9.20-2
- Fix filelists

* Mon May 20 2024 Richard Hughes <richard@hughsie.com> - 1.9.20-1
- New upstream release

* Fri May 03 2024 Richard Hughes <richard@hughsie.com> - 1.9.19-1
- New upstream release

* Mon Apr 22 2024 Richard Hughes <richard@hughsie.com> - 1.9.17-1
- New upstream release

* Fri Apr 05 2024 Richard Hughes <richard@hughsie.com> - 1.9.16-1
- New upstream release

* Thu Apr 04 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1.9.15-2
- Add riscv64 support

* Mon Mar 11 2024 Richard Hughes <richard@hughsie.com> - 1.9.15-1
- New upstream release

* Tue Feb 27 2024 Richard Hughes <richard@hughsie.com> - 1.9.14-2
- Use bash-completion-devel on Fedora >= 41

* Mon Feb 26 2024 Richard Hughes <richard@hughsie.com> - 1.9.14-1
- New upstream release

* Thu Feb 08 2024 Richard Hughes <richard@hughsie.com> - 1.9.13-1
- New upstream release

* Mon Feb 05 2024 Richard Hughes <richard@hughsie.com> - 1.9.12-2
- Bump for side-tag

* Wed Jan 24 2024 Richard Hughes <richard@hughsie.com> - 1.9.12-1
- New upstream release#

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Richard Hughes <richard@hughsie.com> - 1.9.11-4
- Rebuild for redhat-rpm-config regression

* Fri Jan 05 2024 Kevin Fenzi <kevin@scrye.com> - 1.9.11-3
- Rebuild again to fix missing provides caused by #2256645

* Thu Jan 04 2024 Adam Williamson <awilliam@redhat.com> - 1.9.11-2
- Rebuild to fix missing provides caused by #2256645

* Wed Jan 03 2024 Richard Hughes <richard@hughsie.com> - 1.9.11-1
- New upstream release

* Mon Dec 04 2023 Richard Hughes <richard@hughsie.com> - 1.9.10-1
- New upstream release

* Mon Nov 20 2023 Richard Hughes <richard@hughsie.com> - 1.9.9-1
- New upstream release

* Tue Nov 14 2023 Richard Hughes <richard@hughsie.com> - 1.9.8-1
- New upstream release

* Wed Nov 01 2023 Richard Hughes <richard@hughsie.com> - 1.9.7-1
- New upstream release

* Mon Oct 30 2023 Richard Hughes <richard@hughsie.com> - 1.9.6-2
- Revert "Use a softer dep for passim (the daemon)"

* Fri Oct 06 2023 Richard Hughes <richard@hughsie.com> - 1.9.6-1
- New upstream release

* Fri Sep 29 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.5-4
- Redo preset call on upgrades

* Thu Sep 07 2023 Richard Hughes <richard@hughsie.com> - 1.9.5-3
- Use a softer dep for passim (the daemon)

* Mon Sep 04 2023 Richard Hughes <richard@hughsie.com> - 1.9.5-2
- Fix BRs

* Mon Sep 04 2023 Richard Hughes <richard@hughsie.com> - 1.9.5-1
- New upstream release

* Tue Aug 22 2023 Richard Hughes <richard@hughsie.com> - 1.9.4-1
- New upstream release

* Fri Aug 11 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3-3
- Rebuild for EVR upgrade path

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Richard Hughes <richard@hughsie.com> - 1.9.3-1
- New upstream release

* Fri Jul 07 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.9.2-2
- Fix ELN build

* Mon Jun 12 2023 Richard Hughes <richard@hughsie.com> - 1.9.2-1
- New upstream release

* Sat May 13 2023 Richard Hughes <richard@hughsie.com> - 1.9.1-1
- New upstream release

* Fri May 12 2023 Richard Hughes <richard@hughsie.com> - 1.8.15-1
- New upstream release

* Fri Mar 31 2023 Richard Hughes <richard@hughsie.com> - 1.8.14-1
- New upstream release

* Tue Mar 28 2023 Richard Hughes <richard@hughsie.com> - 1.8.13-1
- New upstream release

* Tue Mar 07 2023 Richard Hughes <richard@hughsie.com> - 1.8.12-2
- Rebuilt due to libcbor bump

* Fri Feb 24 2023 Richard Hughes <richard@hughsie.com> - 1.8.12-1
- New upstream release

* Thu Feb 23 2023 Richard Hughes <richard@hughsie.com> - 1.8.11-1
- New upstream release

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 1.8.10-2
- migrated to SPDX license

* Mon Jan 23 2023 Richard Hughes <richard@hughsie.com> - 1.8.10-1
- New upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Richard Hughes <richard@hughsie.com> - 1.8.9-3
- Use updated upstream patch

* Tue Jan 03 2023 Richard Hughes <richard@hughsie.com> - 1.8.9-2
- Backport a patch from upstream to fix s390x build

* Tue Jan 03 2023 Richard Hughes <richard@hughsie.com> - 1.8.9-1
- New upstream release

* Wed Dec 07 2022 Richard Hughes <richard@hughsie.com> - 1.8.8-2
- Actually upload sources....

* Wed Dec 07 2022 Richard Hughes <richard@hughsie.com> - 1.8.8-1
- New upstream release

* Tue Nov 29 2022 Richard Hughes <richard@hughsie.com> - 1.8.7-4
- Disable the libsmbios requirement

* Wed Nov 09 2022 Richard Hughes <richard@hughsie.com> - 1.8.7-3
- Fix the lvfs-testing remote

* Wed Nov 09 2022 Richard Hughes <richard@hughsie.com> - 1.8.7-2
- Fix s390x

* Wed Nov 09 2022 Richard Hughes <richard@hughsie.com> - 1.8.7-1
- New upstream release

* Fri Oct 07 2022 Richard Hughes <richard@hughsie.com> - 1.8.6-1
- New upstream release

* Thu Sep 22 2022 Richard Hughes <richard@hughsie.com> - 1.8.5-1
- New upstream release

* Tue Aug 30 2022 Richard Hughes <richard@hughsie.com> - 1.8.4-3
- Fix fwupd-devel upgrade issue

* Tue Aug 30 2022 Richard Hughes <richard@hughsie.com> - 1.8.4-2
- Fix filelists

* Tue Aug 30 2022 Richard Hughes <richard@hughsie.com> - 1.8.4-1
- New upstream release

* Fri Jul 22 2022 Richard Hughes <richard@hughsie.com> - 1.8.3-3
- Fix ppc64le, which has no tests

* Fri Jul 22 2022 Richard Hughes <richard@hughsie.com> - 1.8.3-2
- trivial: Add BR

* Fri Jul 22 2022 Richard Hughes <richard@hughsie.com> - 1.8.3-1
- New upstream release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Richard Hughes <richard@hughsie.com> - 1.8.2-1
- New upstream release

* Fri May 27 2022 Richard Hughes <richard@hughsie.com> - 1.8.1-1
- New upstream release

* Thu Apr 28 2022 Richard Hughes <richard@hughsie.com> - 1.8.0-1
- New upstream release

* Tue Apr 05 2022 Richard Hughes <richard@hughsie.com> - 1.7.7-1
- New upstream release

* Fri Feb 25 2022 Richard Hughes <richard@hughsie.com> - 1.7.6-1
- New upstream release

* Mon Feb 07 2022 Richard Hughes <richard@hughsie.com> - 1.7.5-1
- New upstream release

* Mon Jan 31 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 1.7.4-3
- Fix 'bogus date in changelog' warning

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Richard Hughes <richard@hughsie.com> - 1.7.4-1
- New upstream release

* Mon Dec 13 2021 Richard Hughes <richard@hughsie.com> - 1.7.3-1
- New upstream release

* Fri Nov 19 2021 Richard Hughes <richard@hughsie.com> - 1.7.2-2
- trivial: Fix %%files

* Fri Nov 19 2021 Richard Hughes <richard@hughsie.com> - 1.7.2-1
- New upstream release

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 1.7.1-2
- Rebuilt for protobuf 3.19.0

* Mon Nov 01 2021 Richard Hughes <richard@hughsie.com> - 1.7.1-1
- New upstream release

* Mon Oct 25 2021 Adrian Reber <adrian@lisas.de> - 1.7.0-4
- Rebuilt for protobuf 3.18.1

* Wed Oct 06 2021 Richard Hughes <richard@hughsie.com> - 1.7.0-3
- Backport a patch from upstream to fix s390x

* Wed Oct 06 2021 Richard Hughes <richard@hughsie.com> - 1.7.0-2
- trivial: Update BRs

* Wed Oct 06 2021 Richard Hughes <richard@hughsie.com> - 1.7.0-1
- New upstream release

* Fri Sep 24 2021 Richard Hughes <richard@hughsie.com> - 1.6.4-1
- New upstream release

* Tue Aug 10 2021 Richard Hughes <richard@hughsie.com> - 1.6.3-1
- New upstream release

* Mon Aug 02 2021 Richard Hughes <richard@hughsie.com> - 1.6.2-1
- New upstream release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Richard Hughes <richard@hughsie.com> - 1.6.1-2
- trivial: Upload the actual new tarball

* Mon Jun 14 2021 Richard Hughes <richard@hughsie.com> - 1.6.1-1
- New upstream release

* Wed Apr 28 2021 Richard Hughes <richard@hughsie.com> - 1.6.0-1
- New upstream release

* Thu Apr 15 2021 Andrew Thurman <ajtbecool@gmail.com> - 1.5.9-2
- Backport https://github.com/fwupd/fwupd/pull/3144 to fix https://bugzilla.redhat.com/show_bug.cgi?id=1949491

* Tue Apr 13 2021 Richard Hughes <richard@hughsie.com> - 1.5.9-1
- New upstream release

* Wed Mar 24 2021 Richard Hughes <richard@hughsie.com> - 1.5.8-1
- New upstream release

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.7-3
- Rebuilt for updated systemd-rpm-macros

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.7-2
- Coalesce systemd scriptlets

* Tue Feb 23 2021 Richard Hughes <richard@hughsie.com> - 1.5.7-1
- New upstream release

* Tue Feb 16 2021 Richard Hughes <richard@hughsie.com> - 1.5.6-1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Richard Hughes <richard@hughsie.com> - 1.5.5-2
- trivial: Fix date

* Mon Jan 11 2021 Richard Hughes <richard@hughsie.com> - 1.5.5-1
- New upstream release

* Wed Dec 16 2020 Richard Hughes <richard@hughsie.com> - 1.5.4-1
- New upstream release

* Tue Dec 08 2020 Richard Hughes <richard@hughsie.com> - 1.5.3-1
- New upstream release

* Mon Nov 23 2020 Richard Hughes <richard@hughsie.com> - 1.5.2-3
- Set supported_build=true for the next build

* Mon Nov 23 2020 Richard Hughes <richard@hughsie.com> - 1.5.2-2
- trivial: NVMe is now available on all arches

* Mon Nov 23 2020 Richard Hughes <richard@hughsie.com> - 1.5.2-1
- New upstream release

* Sat Nov 21 2020 Adam Williamson <awilliam@redhat.com> - 1.5.1-2
- Backport #2605 for #2600, seems to help RHBZ #1896540

* Mon Nov 02 2020 Richard Hughes <richard@hughsie.com> - 1.5.1-1
- New upstream release

* Mon Oct 26 2020 Richard Hughes <richard@hughsie.com> - 1.5.0-1
- New upstream release

* Mon Sep 07 2020 Richard Hughes <richard@hughsie.com> - 1.4.6-1
- New upstream release

* Tue Aug 18 2020 Richard Hughes <richard@hughsie.com> - 1.4.5-4
- Rebuild for the libxmlb API bump

* Mon Aug 03 2020 Peter Jones <pjones@redhat.com> - 1.4.5-3
- Make dual signing happen.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-2
- Second attempt - Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 30 2020 Richard Hughes <richard@hughsie.com> - 1.4.5-1
- New upstream release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 10 2020 Richard Hughes <richard@hughsie.com> - 1.4.4-1
- New upstream release

* Wed Jun 10 2020 Richard Hughes <richard@hughsie.com> - 1.4.3-1
- New upstream release

* Fri May 22 2020 Richard Hughes <richard@hughsie.com> - 1.4.2-2
- Backport a patch to fix the synaptics fingerprint reader update

* Mon May 18 2020 Richard Hughes <richard@hughsie.com> - 1.4.2-1
- New upstream release

* Mon Apr 27 2020 Richard Hughes <richard@hughsie.com> - 1.4.1-1
- New upstream release

* Tue Apr 14 2020 Richard Hughes <richard@hughsie.com> - 1.4.0-3
- Make the -tests subdir arch specific

* Tue Apr 14 2020 Richard Hughes <richard@hughsie.com> - 1.4.0-2
- Fix ppc64le build

* Tue Apr 14 2020 Richard Hughes <richard@hughsie.com> - 1.4.0-1
- New upstream release

* Mon Mar 09 2020 Nicolas Mailhot <nim@fedoraproject.org> - 1.3.9-3
- Rebuild against the new Gusb

* Wed Mar 04 2020 Richard Hughes <richard@hughsie.com> - 1.3.9-2
- No flashrom on s390, which seems fine

* Wed Mar 04 2020 Richard Hughes <richard@hughsie.com> - 1.3.9-1
- New upstream release

* Thu Feb 13 2020 Richard Hughes <richard@hughsie.com> - 1.3.8-1
- New upstream release

* Fri Jan 31 2020 Richard Hughes <richard@hughsie.com> - 1.3.7-2
- Actually upload new tarball

* Fri Jan 31 2020 Richard Hughes <richard@hughsie.com> - 1.3.7-1
- New upstream release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Richard Hughes <richard@hughsie.com> - 1.3.6-3
- trivial: Fix filelists to reflect reality

* Mon Dec 30 2019 Richard Hughes <richard@hughsie.com> - 1.3.6-2
- trivial: Only build the TPM plugin where we have tss2-esys

* Mon Dec 30 2019 Richard Hughes <richard@hughsie.com> - 1.3.6-1
- New upstream release

* Sat Dec 14 2019 Jeff Law <law@redhat.com> - 1.3.5-2
- Fix date in ChangeLog entry

* Fri Nov 29 2019 Richard Hughes <richard@hughsie.com> - 1.3.5-1
- New upstream release

* Fri Nov 22 2019 Richard Hughes <richard@hughsie.com> - 1.3.4-1
- New upstream release

* Fri Nov 01 2019 Richard Hughes <richard@hughsie.com> - 1.3.3-1
- New upstream release

* Tue Oct 08 2019 Richard Hughes <richard@hughsie.com> - 1.3.2-2
- Manually create /var/cache/fwupd to work around #1757948

* Thu Sep 26 2019 Richard Hughes <richard@hughsie.com> - 1.3.2-1
- New upstream release

* Thu Aug 01 2019 Miro Hrončok <miro@hroncok.cz> - 1.2.10-3
- Stop recommending python3, the package already requires it via shebang

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Richard Hughes <richard@hughsie.com> - 1.2.10-1
- New upstream release

* Mon May 20 2019 Richard Hughes <richard@hughsie.com> - 1.2.9-3
- Only run the self tests on fast arches

* Mon May 20 2019 Richard Hughes <richard@hughsie.com> - 1.2.9-2
- Only run the self tests on fast arches

* Mon May 20 2019 Richard Hughes <richard@hughsie.com> - 1.2.9-1
- New upstream release

* Tue Apr 23 2019 Richard Hughes <richard@hughsie.com> - 1.2.8-1
- New upstream release

* Wed Apr 17 2019 Richard Hughes <richard@hughsie.com> - 1.2.7-4
- Revert a patch from upstream

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 1.2.7-3
- Rebuild with Meson fix for #1699099

* Thu Apr 11 2019 Richard Hughes <richard@hughsie.com> - 1.2.7-2
- Fix filelists for non x64

* Thu Apr 11 2019 Richard Hughes <richard@hughsie.com> - 1.2.7-1
- New upstream release

* Wed Mar 27 2019 Richard Hughes <richard@hughsie.com> - 1.2.6-2
- Enable the ModemManager plugin

* Tue Mar 26 2019 Richard Hughes <richard@hughsie.com> - 1.2.6-1
- New upstream release

* Mon Feb 25 2019 Richard Hughes <richard@hughsie.com> - 1.2.5-1
- New upstream release

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.4-5
- Remove obsolete scriptlets

* Sat Feb 02 2019 Richard Hughes <richard@hughsie.com> - 1.2.4-4
- Add BuildRequires: glibc-langpack-en

* Fri Feb 01 2019 Richard Hughes <richard@hughsie.com> - 1.2.4-3
- Fix building, harder

* Fri Feb 01 2019 Richard Hughes <richard@hughsie.com> - 1.2.4-2
- Backport a build fix from master

* Fri Feb 01 2019 Richard Hughes <richard@hughsie.com> - 1.2.4-1
- New upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 04 2019 Richard Hughes <richard@hughsie.com> - 1.2.3-1
- New upstream release

* Sun Dec 30 2018 Richard Hughes <richard@hughsie.com> - 1.2.2-1
- New upstream release

* Tue Nov 27 2018 Richard Hughes <richard@hughsie.com> - 1.2.1-1
- New upstream release

* Wed Nov 07 2018 Richard Hughes <richard@hughsie.com> - 1.2.0-1
- New upstream release

* Fri Oct 12 2018 Richard Hughes <richard@hughsie.com> - 1.1.3-1
- New upstream release

* Mon Sep 10 2018 Richard Hughes <richard@hughsie.com> - 1.1.2-3
- trivial: Fix filelists

* Mon Sep 10 2018 Richard Hughes <richard@hughsie.com> - 1.1.2-2
- trivial: Only build NVMe when efivars is available

* Mon Sep 10 2018 Richard Hughes <richard@hughsie.com> - 1.1.2-1
- New upstream release

* Mon Aug 13 2018 Richard Hughes <richard@hughsie.com> - 1.1.1-1
- New upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Richard Hughes <richard@hughsie.com> - 1.1.0-3
- Rebuild to get the EFI executable signed with the Red Hat key

* Wed Jul 11 2018 Richard Hughes <richard@hughsie.com> - 1.1.0-2
- Fix BRs

* Wed Jul 11 2018 Richard Hughes <richard@hughsie.com> - 1.1.0-1
- New upstream release

* Thu Jun 07 2018 Richard Hughes <richard@hughsie.com> - 1.0.8-1
- New upstream release

* Mon Apr 30 2018 Richard Hughes <richard@hughsie.com> - 1.0.7-1
- New upstream release

* Mon Mar 12 2018 Richard Hughes <richard@hughsie.com> - 1.0.6-2
- trivial: Fix up non x64 build

* Mon Mar 12 2018 Richard Hughes <richard@hughsie.com> - 1.0.6-1
- New upstream release

* Fri Feb 23 2018 Richard Hughes <richard@hughsie.com> - 1.0.5-2
- Use the new CDN for metadata

* Wed Feb 14 2018 Richard Hughes <richard@hughsie.com> - 1.0.5-1
- New upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Richard Hughes <richard@hughsie.com> - 1.0.4-4
- Wl,-z,defs is broken

* Thu Jan 25 2018 Richard Hughes <richard@hughsie.com> - 1.0.4-3
- trivial: Fix -Wl,-z,defs build failure by backporting a patch from upstream

* Thu Jan 25 2018 Richard Hughes <richard@hughsie.com> - 1.0.4-2
- trivial: Add the correct json_glib_version version

* Thu Jan 25 2018 Richard Hughes <richard@hughsie.com> - 1.0.4-1
- New upstream release

* Fri Jan 12 2018 Richard Hughes <richard@hughsie.com> - 1.0.3-2
- Backport a patch that fixes applying firmware updates using gnome software

* Tue Jan 09 2018 Richard Hughes <richard@hughsie.com> - 1.0.3-1
- New upstream release

* Mon Dec 04 2017 Kalev Lember <klember@redhat.com> - 1.0.2-2
- Fix date in %%changelog

* Tue Nov 28 2017 Richard Hughes <richard@hughsie.com> - 1.0.2-1
- New upstream release

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> - 1.0.1-3
- Rebuild against libappstream-glib 0.7.4

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> - 1.0.1-2
- Fix libdfu obsoletes versions

* Thu Nov 09 2017 Richard Hughes <richard@hughsie.com> - 1.0.1-1
- New upstream release

* Mon Oct 09 2017 Richard Hughes <richard@hughsie.com> - 1.0.0-1
- New upstream release

* Fri Sep 01 2017 Richard Hughes <richard@hughsie.com> - 0.9.7-1
- New upstream release

* Fri Sep 01 2017 Richard Hughes <richard@hughsie.com> - 0.9.6-3
- Fix deps on i686

* Thu Aug 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.6-2
- move %%meson_test to %%check section

* Thu Aug 03 2017 Richard Hughes <richard@hughsie.com> - 0.9.6-1
- New upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Richard Hughes <richard@hughsie.com> - 0.9.5-2
- Disable BuildArch: noarch for the labels sub-package

* Tue Jul 04 2017 Richard Hughes <richard@hughsie.com> - 0.9.5-1
- New upstream release

* Thu Jun 15 2017 Richard Hughes <richard@hughsie.com> - 0.9.4-2
- trivial: Do not build with tests enabled

* Thu Jun 15 2017 Richard Hughes <richard@hughsie.com> - 0.9.4-1
- New upstream release

* Wed Jun 07 2017 Richard Hughes <richard@hughsie.com> - 0.9.3-1
- New upstream release

* Tue May 23 2017 Richard Hughes <richard@hughsie.com> - 0.9.2-4
- Backport several fixes

* Mon May 22 2017 Richard Hughes <richard@hughsie.com> - 0.9.2-3
- Fix build

* Mon May 22 2017 Richard Hughes <richard@hughsie.com> - 0.9.2-2
- trivial: Fix build

* Mon May 22 2017 Richard Hughes <richard@hughsie.com> - 0.9.2-1
- New upstream release

* Thu Apr 20 2017 Richard Hughes <richard@hughsie.com> - 0.8.2-2
- trivial: Fix 32 bit architectures

* Thu Apr 20 2017 Richard Hughes <richard@hughsie.com> - 0.8.2-1
- New upstream release

* Thu Mar 23 2017 Bastien Nocera <hadess@hadess.net> - 0.8.1-3
- + fwupd-0.8.1-2 Release claimed devices on error, fixes unusable input devices

* Mon Feb 27 2017 Richard Hughes <richard@hughsie.com> - 0.8.1-2
- trivial: Update BRs

* Mon Feb 27 2017 Richard Hughes <richard@hughsie.com> - 0.8.1-1
- New upstream release

* Wed Feb 08 2017 Richard Hughes <richard@hughsie.com> - 0.8.0-2
- trivial: Fix build on non-x86_64 hardware

* Wed Feb 08 2017 Richard Hughes <richard@hughsie.com> - 0.8.0-1
- New upstream release

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.5-2
- Rebuild for gpgme 1.18

* Wed Oct 19 2016 Richard Hughes <richard@hughsie.com> - 0.7.5-1
- New upstream release

* Mon Sep 19 2016 Richard Hughes <richard@hughsie.com> - 0.7.4-1
- New upstream release

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> - 0.7.3-4
- Add ldconfig scripts for libdfu and libebitdo subpackages

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> - 0.7.3-3
- Tighten libebitdo-devel requires with the _isa macro

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> - 0.7.3-2
- Fix an unexpanded macro in the spec file

* Mon Aug 29 2016 Richard Hughes <richard@hughsie.com> - 0.7.3-1
- New upstream release

* Fri Aug 19 2016 Peter Jones <pjones@redhat.com> - 0.7.2-8
- Rebuild to get libfwup.so.1 as our fwupdate dep.

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 0.7.2-7
- Fix bogus changelog date

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 0.7.2-6
- rebuild against new efivar and fwupdate

* Fri Aug 12 2016 Adam Williamson <awilliam@redhat.com> - 0.7.2-5
- rebuild against new efivar and fwupdate

* Thu Aug 11 2016 Richard Hughes <richard@hughsie.com> - 0.7.2-4
- Use the new CDN for firmware metadata

* Thu Jul 14 2016 Kalev Lember <klember@redhat.com> - 0.7.2-3
- Tighten subpackage dependencies

* Tue Jul 12 2016 Kalev Lember <klember@redhat.com> - 0.7.2-2
- Set minimum required versions of various libraries so that we can be sure they get updated in lockstep with fwupd.

* Mon Jun 13 2016 Richard Hughes <richard@hughsie.com> - 0.7.2-1
- New upstream release

* Fri May 13 2016 Richard Hughes <richard@hughsie.com> - 0.7.1-1
- New upstream release

* Fri Apr 01 2016 Richard Hughes <richard@hughsie.com> - 0.7.0-1
- New upstream release

* Mon Mar 14 2016 Richard Hughes <richard@hughsie.com> - 0.6.3-1
- New upstream release

* Fri Feb 12 2016 Richard Hughes <richard@hughsie.com> - 0.6.2-1
- New upstream release

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Richard Hughes <richard@hughsie.com> - 0.6.1-1
- New upstream release

* Mon Dec 07 2015 Richard Hughes <richard@hughsie.com> - 0.6.0-1
- New upstream release

* Thu Nov 19 2015 Richard Hughes <richard@hughsie.com> - 0.5.4-2
- Actually upload new sources

* Wed Nov 18 2015 Richard Hughes <richard@hughsie.com> - 0.5.4-1
- New upstream release

* Thu Nov 05 2015 Richard Hughes <richard@hughsie.com> - 0.5.3-1
- New upstream release

* Wed Oct 28 2015 Richard Hughes <richard@hughsie.com> - 0.5.2-1
- New upstream release

* Mon Sep 21 2015 Richard Hughes <richard@hughsie.com> - 0.5.1-1
- Update to 0.5.1 to fix a bug in the offline updater

* Tue Sep 15 2015 Richard Hughes <richard@hughsie.com> - 0.5.0-1
- New upstream release

* Thu Sep 10 2015 Richard Hughes <richard@hughsie.com> - 0.1.6-4
- Do not merge the existing firmware metadata with the submitted files

* Thu Sep 10 2015 Kalev Lember <klember@redhat.com> - 0.1.6-3
- Make fwupd-sign obsoletes versioned

* Thu Sep 10 2015 Kalev Lember <klember@redhat.com> - 0.1.6-2
- Own system-update.target.wants directory

* Thu Sep 10 2015 Richard Hughes <richard@hughsie.com> - 0.1.6-1
- New upstream release

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 0.1.5-3
- Disable fwupd offline update service

* Wed Aug 19 2015 Richard Hughes <richard@hughsie.com> - 0.1.5-2
- Use the non-beta download URL prefix

* Wed Aug 12 2015 Richard Hughes <richard@hughsie.com> - 0.1.5-1
- New upstream release

* Sat Jul 25 2015 Richard Hughes <richard@hughsie.com> - 0.1.4-1
- New upstream release

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Richard Hughes <richard@hughsie.com> - 0.1.3-3
- Do not compile the UEFI support for 32 bit ARM

* Wed Jun 03 2015 Richard Hughes <richard@hughsie.com> - 0.1.3-2
- Compile with libfwupdate for UEFI firmware support

* Thu May 28 2015 Richard Hughes <richard@hughsie.com> - 0.1.3-1
- New upstream release

* Wed Apr 22 2015 Richard Hughes <richard@hughsie.com> - 0.1.2-1
- New upstream release

* Mon Mar 23 2015 Richard Hughes <richard@hughsie.com> - 0.1.1-2
- Add BRs

* Mon Mar 23 2015 Richard Hughes <richard@hughsie.com> - 0.1.1-1
- New upstream release

* Mon Mar 16 2015 Richard Hughes <richard@hughsie.com> - 0.1.0-1
- First release
## END: Generated by rpmautospec
