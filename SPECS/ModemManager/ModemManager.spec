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

%bcond check 1

%global glib2_version %(pkg-config --modversion glib-2.0 2>/dev/null || echo bad)
%global qmi_version %(pkg-config --modversion qmi-glib 2>/dev/null || echo bad)
%global mbim_version %(pkg-config --modversion mbim-glib 2>/dev/null || echo bad)
%global qrtr_version %(pkg-config --modversion qrtr-glib 2>/dev/null || echo bad)

%global forgeurl https://gitlab.freedesktop.org/mobile-broadband/ModemManager

Name: ModemManager
Version: 1.24.2
Release: %autorelease
Summary: Mobile broadband modem management service
License: GPL-2.0-or-later
URL: %{forgeurl}
Source: %{forgeurl}/-/archive/%{version}/%{name}-%{version}.tar.bz2

# For mbim-proxy and qmi-proxy
Requires: libmbim-utils
Requires: libqmi-utils
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

# Don't allow older versions of these than what we built against,
# because they add new API w/o versioning it or bumping the SONAME
Conflicts: glib2%{?_isa} < %{glib2_version}
Conflicts: libqmi%{?_isa} < %{qmi_version}
Conflicts: libmbim%{?_isa} < %{mbim_version}
Conflicts: libqrtr-glib%{?_isa} < %{qrtr_version}

Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

Requires: polkit

BuildRequires: meson >= 0.53
BuildRequires: dbus-devel
BuildRequires: dbus-daemon
BuildRequires: gettext-devel >= 0.19.8
BuildRequires: glib2-devel >= 2.56
BuildRequires: gobject-introspection-devel >= 1.38
BuildRequires: gtk-doc
BuildRequires: libgudev1-devel >= 232
BuildRequires: libmbim-devel >= 1.32.0
BuildRequires: libqmi-devel >= 1.36.0
BuildRequires: libqrtr-glib-devel >= 1.0.0
BuildRequires: systemd
BuildRequires: systemd-devel >= 209
BuildRequires: vala
BuildRequires: polkit-devel
%if %{with check}
BuildRequires: python3-gobject
BuildRequires: python3-dbus
%endif

%global __provides_exclude ^libmm-plugin-

%description
The ModemManager service manages WWAN modems and provides a consistent API for
interacting with these devices to client applications.


%package devel
Summary: Libraries and headers for adding ModemManager support to applications
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains various headers for accessing some ModemManager functionality
from applications.


%package glib
Summary: Libraries for adding ModemManager support to applications that use glib.
License: LGPL-2.1-or-later
Requires: glib2 >= %{glib2_version}

%description glib
This package contains the libraries that make it easier to use some ModemManager
functionality from applications that use glib.


%package glib-devel
Summary: Libraries and headers for adding ModemManager support to applications that use glib.
License: LGPL-2.1-or-later
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}
Requires: pkgconfig

%description glib-devel
This package contains various headers for accessing some ModemManager functionality
from glib applications.


%package vala
Summary: Vala bindings for ModemManager
License: LGPL-2.1-or-later
Requires: vala
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description vala
Vala bindings for ModemManager


%prep
%autosetup -p1


%build
# Let's avoid BuildRequiring bash-completion because it changes behavior
# of shell, at least until the .pc file gets into the -devel subpackage.
# We'll just install the bash-completion file ourselves.
%meson \
	-Ddist_version='"%{version}-%{release}"' \
	-Dudevdir=/usr/lib/udev \
	-Dsystemdsystemunitdir=%{_unitdir} \
	-Ddbus_policy_dir=%{_datadir}/dbus-1/system.d \
	-Dvapi=true \
	-Dgtk_doc=true \
	-Dpolkit=permissive \
	-Dbash_completion=false
%meson_build


%install
%meson_install
find %{buildroot}%{_datadir}/gtk-doc |xargs touch --reference meson.build
%find_lang %{name}
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
cp -a cli/mmcli-completion %{buildroot}%{_datadir}/bash-completion/completions/mmcli

%if %{with check}
%check
%meson_test
%endif


%post
%systemd_post ModemManager.service


%preun
%systemd_preun ModemManager.service


%postun
%systemd_postun ModemManager.service


%files -f %{name}.lang
%license COPYING
%doc README.md
%{_datadir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager1.service
%attr(0755,root,root) %{_sbindir}/ModemManager
%attr(0755,root,root) %{_bindir}/mmcli
%dir %{_libdir}/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/*.so*
%{_udevrulesdir}/*
%{_datadir}/polkit-1/actions/*.policy
%{_unitdir}/ModemManager.service
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/bash-completion
%{_datadir}/ModemManager
%{_mandir}/man1/*
%{_mandir}/man8/*


%files devel
%{_includedir}/ModemManager/
%dir %{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gtk-doc/html/%{name}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/dbus-1/interfaces/*.xml


%files glib
%license COPYING
%{_libdir}/libmm-glib.so.*
%{_libdir}/girepository-1.0/*.typelib


%files glib-devel
%{_libdir}/libmm-glib.so
%dir %{_includedir}/libmm-glib
%{_includedir}/libmm-glib/*.h
%{_libdir}/pkgconfig/mm-glib.pc
%dir %{_datadir}/gtk-doc/html/libmm-glib
%{_datadir}/gtk-doc/html/libmm-glib/*
%{_datadir}/gir-1.0/*.gir


%files vala
%{_datadir}/vala/vapi/libmm-glib.*


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.24.2-2
- Latest state for ModemManager

* Wed Aug 13 2025 Lubomir Rintel <lkundrak@v3.sk> - 1.24.2-1
- Update to 1.24.2

* Wed Aug 13 2025 Lubomir Rintel <lkundrak@v3.sk> - 1.24.0-3
- Fix libmbim BR

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Davide Cavalca <dcavalca@fedoraproject.org> - 1.24.0-1
- Update to 1.24.0; Fixes: RHBZ#2360675, RHBZ#2368369

* Sat Jul 12 2025 Davide Cavalca <dcavalca@fedoraproject.org> - 1.22.0-10
- Move dbus configuration; Fixes: RHBZ#2351826

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Dennis Gilmore <dennis@ausil.us> - 1.22.0-1
- update to 1.22.0

* Sun Jul 30 2023 Tao Jin <tao-j@outlook.com> - 1.20.6-3
- Rebuilt for RHBZ#2226577

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 24 2023 Lubomir Rintel <lkundrak@v3.sk> - 1.20.6-1
- Update to 1.20.6

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Lubomir Rintel <lkundrak@v3.sk> - 1.20.2-3
- Version the qrtr-glib dependency

* Sun Jan 08 2023 Lubomir Rintel <lkundrak@v3.sk> - 1.20.2-2
- Switch to build using meson

* Tue Nov 22 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.20.2-1
- Update to 1.20.2

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat May 14 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.18.8-1
- Update to 1.18.8

* Sat Feb 12 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.18.6-1
- Update to 1.18.6

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Sep 19 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.18.2-1
- update to 1.18.2

* Mon Sep 13 2021 Thomas Haller <thaller@redhat.com> - 1.18.0-2
- depend ModemManager on polkit package

* Sun Sep 12 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.18.0-1
- Update to 1.18.0

* Sat Aug 14 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.17.900-1
- Update to 1.18.0 RC1

* Wed Aug 04 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.16.8-4
- Rebuild for new libmbim/libqmi

* Thu Jul 29 2021 Bastien Nocera <bnocera@redhat.com> - 1.16.8-3
+ ModemManager-1.16.8-3
- Add polkit support as used upstream

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.16.8-1
- Update to 1.16.8

* Mon Jun 07 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.16.6-1
- Update to 1.16.6

* Fri Apr 30 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.16.4-1
- Update to 1.16.4

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.14.10-1
- Update to 1.14.10
- Spec clean up

* Mon Dec 28 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.14.8-2
- Drop unneeded libxslt dependency

* Mon Dec 28 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.14.8-1
- Update to 1.14.8

* Tue Nov  3 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.14.6-1
- Update to 1.14.6

* Thu Aug 20 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.14.2-1
- Update to 1.14.2

* Mon Jul 27 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.14.0-1
- Update to 1.14.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 24 2020 Lubomir Rintel <lkundrak@v3.sk> - 1.12.8-1
- Update to 1.12.8 release

* Thu Mar  5 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.6-1
- Update to 1.12.6 release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.10.8-1
- Update to 1.10.8 release

* Mon Sep 23 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.10.6-2
- Don't grab cdc_ether devices on Sierra QMI modems

* Mon Sep 23 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.10.6-1
- Update to 1.10.6 release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.10.4-1
- Update to 1.10.4 release

* Fri Jun 14 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.10.2-1
- Update to 1.10.2 release
- Don't grab cdc_ether devices on Sierra QMI modems

* Wed Mar 27 2019 Richard Hughes <richard@hughsie.com> 1.10.0-1
- Update to the release tarball.

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 1.10.0-0.3.rc1
- Update BRs for vala packaging changes

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.10.0-0.1.rc1
- Update to 1.10 release candidate 1

* Tue Jan 15 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.2-1
- Update to 1.8.2 release

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.8.0-4
- Rebuild with fixed binutils

* Sun Jul 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.8.0-3
- -devel: own %%_includedir/ModemManager/
- %%build: --disable-silent-rules
- use %%make_build %%make_install

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 03 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.8.0-1
- Update to 1.8.0 release

* Tue Apr 24 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.8.0-0.rc2.1
- Update to 1.8 release candidate 2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.6.12-2
- Switch to %%ldconfig_scriptlets

* Mon Jan 22 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.6.12-1
- Update to 1.6.12 release
- Require libmbim and libqmi we were built with (rh #1534945)
- Restore the scriptlets where they are needed

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.6.10-2
- Remove obsolete scriptlets

* Sun Oct 22 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.6.10-1
- Update to 1.6.10 release

* Tue Aug 29 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.6.8-1
- Update to 1.6.8 release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 15 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.6.4-1
- Update to 1.6.4 release

* Tue Oct 04 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.6.2-1
- Update to 1.6.2 release

* Tue Jul 26 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.6.0-1
- Update to 1.6.0 release

* Fri Jul 08 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.6-0.4.rc4
- Enable suspend/resume support (rh#1341303)

* Fri Jul 08 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.6-0.3.rc4
- Update to 1.6 release candidate 4

* Mon May 02 2016 Francesco Giudici <fgiudici@redhat.com> - 1.6-0.3.rc3
- Update to 1.6 release candidate 3

* Tue Apr 12 2016 Than Ngo <than@redhat.com> - 1.6-0.3.rc2
- add better fix for big endian issue on s390x/ppc64

* Thu Apr 07 2016 Than Ngo <than@redhat.com> - 1.6-0.2.rc2
- fix big endian issue on s390x/ppc64

* Fri Mar 25 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.6-0.1.rc2
- Update to 1.6 release candidate 2

* Mon Mar 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.6-0.1.rc1
- Update to 1.6 release candidate

* Mon Mar 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.4.14-1
- Update to 1.4.14 release

* Mon Feb 29 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4.10-4
- Disable -Werror (#1307284)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 07 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.4.10-2
- Ensure systemctl's around when we preset the service (rh #1227424)

* Tue Aug 18 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.4.10-1
- Update to 1.4.10 release

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 29 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.4.6-1
- Update to 1.4.6 release

* Mon Mar  2 2015 Dan Williams <dcbw@redhat.com> - 1.4.4-2
- Don't print location information in logs (rh #1194492)

* Wed Feb 11 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.4.4-1
- Update to 1.4.4 release

* Thu Jan 15 2015 Dan Williams <dcbw@redhat.com> - 1.4.2-1
- Update to 1.4.2 release

* Wed Aug 27 2014 Dan Williams <dcbw@redhat.com> - 1.4.0-1
- Update to 1.4.0 release
- Quiet debug messages about access technology changes
- Improve network time support for Huawei 3GPP devices
- Always use DHCP for QMI bearers (fixes some Huawei devices)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Dan Williams <dcbw@redhat.com> - 1.3.0-1
- Update to git development snapshot
- Add IPv6 support for many devices
- Updated blacklist for non-modem USB devices
- Support for more MBIM devices from various manufacturers
- Support for more Huawei devices with network ports
- Add new "unmanaged" GPS location mode
- Many bug fixes for various modems

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.2.0-3
- Rebuilt for gobject-introspection 1.41.4

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb  1 2014 poma <poma@gmail.com> - 1.2.0-1
- Update to 1.2.0 release

* Fri Sep 13 2013 Dan Williams <dcbw@redhat.com> - 1.1.0-2.git20130913
- Build with MBIM support
- Enable Vala bindings

* Fri Sep  6 2013 Dan Williams <dcbw@redhat.com> - 1.1.0-1.git20130906
- Update to latest git snapshot

* Mon Aug 26 2013 Dan Williams <dcbw@redhat.com> - 1.0.1-2.git20130723
- Fix udev rules file paths
- Remove 'dia' from BuildRequires

* Tue Jul 23 2013 Dan Williams <dcbw@redhat.com> - 1.0.1-1.git20130723
- Update to 1.0.1 release
- Enable QMI support

* Wed Jul 10 2013 Dan Williams <dcbw@redhat.com> - 0.7.991-2.git20130710
- Handle PNP connected devices
- Fall back to AT for messaging if QMI modem doesn't support the WMS service
- Fix IPv6 bearer creation for HSO devices
- Fix detection of supported modes on Icera-based modems
- Fix handling of some Icera-based modems with limited capability ports
- Add support for Olivetti Olicard 200

* Fri Jun  7 2013 Dan Williams <dcbw@redhat.com> - 0.7.991-1.git20130607
- Update to 0.7.991 snapshot
- Fix SMS validity parsing
- Allow registration changes to 'searching' without disconnecting
- Fix reading SMS messages from some QMI-based devices
- Increase connection timeout for Novatel E362
- Fix PIN retries checking when unlocking Ericsson devices
- Better handling of supported and preferred modes (eg 2G, 3G, 4G preference)

* Wed May 22 2013 Kalev Lember <kalevlember@gmail.com> - 0.7.990-3.git20130515
- Install the libmm-glib.so symlink in -glib-devel
- Include the /usr/share/libmm-glib directory in -glib-devel
- Make sure -glib-devel subpackage depends on the base -glib package

* Thu May 16 2013 Bruno Wolff III <bruno@wolff.to> - 0.7.990-2.git20130515
- Removed epoch macro references

* Wed May 15 2013 Dan Williams <dcbw@redhat.com> - 0.7.990-1.git20130515
- Update to 0.8 snapshot

* Thu Jan 31 2013 Tom Callaway <spot@fedoraproject.org> - 0.6.0.0-3
- blacklist common arduino devices (rh #861620)

* Tue Nov 27 2012 Jiří Klimeš <jklimes@redhat.com> - 0.6.0.0-2
- core: fix a crash in g_utf8_validate() (rh #862341)

* Tue Sep  4 2012 Dan Williams <dcbw@redhat.com> - 0.6.0.0-1
- Update to 0.6.0
- core: fix SMS notifications on many Qualcomm devices
- core: use SMS PDU mode by default (more compatible)
- novatel: fix CDMA roaming indication
- zte: support more devices
- zte: power down modems when disabled
- mbm: power down modems when disabled
- mbm: add support for Ericsson H5321
- sierra: fix detection of secondary ports
- sierra: more reliable connections with USB 305/AT&T Lightning

* Fri Jul 20 2012 Dan Williams <dcbw@redhat.com> - 0.5.3.96-1
- Update to 0.5.3.96 (0.5.4-rc2)
- core: fix SMS handling on a number of devices
- zte: support for devices that use Icera chipsets
- core: ignore unsupported QMI WWAN ports (rh #835153)

* Wed Mar 14 2012 Dan Williams <dcbw@redhat.com> - 0.5.2.0-1
- Update to 0.5.2
- core: retry sending SMS in PDU mode if text fails
- hso: fix connection regression due to Nokia device fixes

* Sat Feb 25 2012 Dan Williams <dcbw@redhat.com> - 0.5.1.97-1
- Update to 0.5.2-rc1
- core: fix a few crashes
- nokia: fix issues with various Nokia devices
- huawei: fix modem crashes with older Huawei devices (like E220)

* Tue Feb  7 2012 Dan Williams <dcbw@redhat.com> - 0.5.1.96-1
- Update to git snapshot of 0.5.2
- option: fix handling of access technology reporting
- cdma: fix handling of EVDO registration states
- mbm: fix problems reconnecting on Ericsson F5521gw modems
- gsm: fix connections using the Motorola Flipout
- gsm: better detection of registration state when connecting
- mbm: add support for more Ericsson modems
- gobi: ensure rebranded Gobi devices are driven by Gobi
- gsm: fix SMS multipart messages, PDU-only mode, and text-mode message listing
- huawei: fix USSD handling
- nokia: add support for Nokia Internet Sticks
- gsm: fix registration response handling on some newer devices
- sierra: add support for Icera-based devices (USB305, AT&T Lightning)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.998-2.git20110706
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul  7 2011 Dan Williams <dcbw@redhat.com> - 0.4.998-1.git20110706
- Update to 0.5-beta4
- gsm: various USSD fixes
- samsung: support for Y3400 module and various other fixes
- gobi: support access technology reporting while disconnected
- nokia: fix issues with N900 USB connected operation (rh #583691)

* Mon Jun  6 2011 Dan Williams <dcbw@redhat.com> - 0.4.997-1
- Update to 0.5-beta3
- samsung: only support Y3300 (fixes issues with other Samsung modems)
- longcheer: restrict to only supported devices
- simtech: add support for Prolink PH-300
- gsm: various SMS cleanups and fixes
- x22x: add support for access technology reporting and the Alcatel X200 modem

* Wed Apr 27 2011 Dan Williams <dcbw@redhat.com> 0.4-8.git20110427
- samsung: add support for Samsung Y3300 GSM modem
- huawei: fixes for probing and handling various Huawei devices
- wavecom: add support for some Wavecom modems
- zte: fix crashes with Icera-based devices
- mbm: add support for Lenovo F5521gw module
- core: add support for basic SMS reception
- core: faster probing for devices that support it (option, samsung)

* Fri Feb 25 2011 Rex Dieter <rdieter@fedoraproejct.org> 0.4-7.git20110201.1
- hack around FTBFS on sparc

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7.git20110201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Dan Williams <dcbw@redhat.com> - 0.4-6.git20110201
- Attempt to fix Icera plugin crash on second dial

* Tue Feb  1 2011 Dan Williams <dcbw@redhat.com> - 0.4-5.git20110201
- core: add device and SIM identifier properties
- dbus: fix property access permissions via D-Bus (rh #58594)
- cdma: better detection of EVDO registration
- cdma: recognize dual-mode devices as CDMA instead of GSM
- gsm: better handling of wrong PIN entry
- gsm: allow usage of older GSM character encoding schemes
- gsm: preliminary USSD support
- gsm: fix handling of modems that report signal strength via +CIND
- sierra: fix handling of Sierra CnS ports mistakenly recognized as QCDM
- sierra: ensure packet-switched network attachment before dialing
- zte: add support for T-Mobile Rocket 2.0
- mbm: add support for HP-branded Ericsson devices
- linktop: add support for Linktop/Teracom LW273
- x22x: add support for various Alcatel devices (like the X220D)

* Tue Jul 20 2010 Dan Williams <dcbw@redhat.com> - 0.4-4.git20100720
- gsm: fix location services API signals
- gsm: fix issue with invalid operator names (rh #597088)
- novatel: fix S720 signal strength reporting
- novatel: detect CDMA home/roaming status

* Wed Jun 30 2010 Dan Williams <dcbw@redhat.com> - 0.4-3.git20100630
- gsm: enable the location services API

* Mon Jun 28 2010 Dan Williams <dcbw@redhat.com> - 0.4-2.git20100628
- core: fix crash during probing when a plugin doesn't support all ports (rh #603294)
- gsm: better registration state checking when devices don't support AT+CREG (Blackberries)
- gsm: add support for getting remaining unlock retry counts

* Tue Jun 22 2010 Dan Williams <dcbw@redhat.com> - 0.4-1.git20100622
- core: fix occasional crash when device is unplugged (rh #591728)
- core: ensure errors are correctly returned when device is unplugged
- core: ensure claimed ports don't fall back to Generic (rh #597296)
- gsm: better compatibility with various phones
- mbm: better detection of connection errors
- simtech: add plugin for Simtech devices (like Airlink 3GU)
- sierra: fix CDMA roaming detection

* Fri May  7 2010 Dan Williams <dcbw@redhat.com> - 0.3-13.git20100507
- core: fix crash when plugging in some Sierra and Option NV devices (rh #589798)
- gsm: better compatibility with various Sony Ericsson phones
- longcheer: better support for Alcatel X060s modems

* Tue May  4 2010 Dan Williams <dcbw@redhat.com> - 0.3-12.git20100504
- core: fix data port assignments (rh #587400)

* Sun May  2 2010 Dan Williams <dcbw@redhat.com> - 0.3-11.git20100502
- core: ignore some failures on disconnect (rh #578280)
- core: add support for platform serial devices
- gsm: better Blackberry DUN support
- gsm: periodically poll access technology
- cdma: prevent crash on modem removal (rh #571921)
- mbm: add support for Sony Ericsson MD400, Dell 5541, and Dell 5542 modems
- novatel: better signal strength reporting on CDMA cards
- novatel: add access technology and mode preference support on GSM cards
- zte: fix mode preference retrieval
- longcheer: add support for Zoom modems (4595, 4596, etc)
- longcheer: add access technology and mode preference support

* Fri Apr 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.3-10.git20100409
- Silence %%post
- Update scripts

* Fri Apr  9 2010 Dan Williams <dcbw@redhat.com> - 0.3-9.git20100409
- gsm: fix parsing Blackberry supported character sets response

* Thu Apr  8 2010 Dan Williams <dcbw@redhat.com> - 0.3-8.git20100408
- mbm: fix retrieval of current allowed mode
- gsm: fix initialization issues with some devices (like Blackberries)

* Mon Apr  5 2010 Dan Williams <dcbw@redhat.com> - 0.3-7.git20100405
- core: fix detection of some generic devices (rh #579247)
- core: fix detection regression of some Huawei devices in 0.3-5
- cdma: periodically poll registration state and signal quality
- cdma: really fix registration detection on various devices (rh #569067)

* Wed Mar 31 2010 Dan Williams <dcbw@redhat.com> - 0.3-6.git20100331
- core: fix PPC/SPARC/etc builds

* Wed Mar 31 2010 Dan Williams <dcbw@redhat.com> - 0.3-5.git20100331
- core: only export a modem when all its ports are handled (rh #540438, rh #569067, rh #552121)
- cdma: handle signal quality requests while connected for more devices
- cdma: handle serving system requests while connected for more devices
- gsm: determine current access technology earlier
- huawei: work around automatic registration issues on some devices

* Tue Mar 23 2010 Dan Williams <dcbw@redhat.com> - 0.3-4.git20100323
- core: ensure enabled modems are disabled when MM stops
- core: better capability detection for Blackberry devices (rh #573510)
- cdma: better checking of registration states (rh #540438, rh #569067, rh #552121)
- gsm: don't block modem when it requires PIN2
- option: fix access technology updates

* Wed Mar 17 2010 Dan Williams <dcbw@redhat.com> - 0.3-3.git20100317
- mbm: add device IDs for C3607w
- mbm: fail earlier during connection failures
- mbm: fix username/password authentication when checked by the network
- hso: implement asynchronous signal quality updates
- option: implement asynchronous signal quality updates
- novatel: correctly handle CDMA signal quality
- core: basic PolicyKit support
- core: fix direct GSM registration information requests
- core: general GSM PIN/PUK unlock fixes
- core: poll GSM registration state internally for quicker status updates
- core: implement GSM 2G/3G preference
- core: implement GSM roaming allowed/disallowed preference
- core: emit signals on access technology changes
- core: better handling of disconnections
- core: fix simple CDMA status requests

* Thu Feb 11 2010 Dan Williams <dcbw@redhat.com> - 0.3-2.git20100211
- core: startup speed improvements
- core: GSM PIN checking improvements
- huawei: fix EVDO-only connections on various devices (rh #553199)
- longcheer: add support for more devices

* Tue Jan 19 2010 Dan Williams <dcbw@redhat.com> - 0.3-1.git20100119
- anydata: new plugin for AnyData CDMA modems (rh #547294)
- core: fix crashes when devices are unplugged during operation (rh #553953)
- cdma: prefer primary port for status/registration queries
- core: fix probing/detection of some PIN-locked devices (rh #551376)
- longcheer: add plugin for Alcatel (X020, X030, etc) and other devices
- gsm: fix Nokia N80 network scan parsing

* Fri Jan  1 2010 Dan Williams <dcbw@redhat.com> - 0.2.997-5.git20100101
- core: fix apparent hangs by limiting retried serial writes
- gsm: ensure modem state is reset when disabled

* Fri Dec 18 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-4.git20091218
- sierra: fix CDMA registration detection in some cases (rh #547513)

* Wed Dec 16 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-3.git20091216
- sierra: ensure CDMA device is powered up when trying to use it
- cdma: better signal quality parsing (fixes ex Huawei EC168C)
- zte: handle unsolicited messages better during probing

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-2.git20091214
- cdma: fix signal strength reporting on some devices
- cdma: better registration state detection when dialing (ex Sierra 5275)
- option: always use the correct tty for dialing commands

* Mon Dec  7 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-1
- core: fix reconnect after manual disconnect (rh #541314)
- core: fix various segfaults during registration
- core: fix probing of various modems on big-endian architectures (ie PPC)
- core: implement modem states to avoid duplicate operations
- hso: fix authentication for Icera-based devices like iCON 505
- zte: use correct port for new devices
- nozomi: fix detection

* Thu Nov  5 2009 Dan Williams <dcbw@redhat.com> - 0.2-4.20091105
- Update to latest git
- core: fix pppd 2.4.5 errors about 'baudrate 0'
- cdma: wait for network registration before trying to connect
- gsm: add cell access technology reporting
- gsm: allow longer-running network scans
- mbm: various fixes for Ericsson F3507g/F3607gw/Dell 5530
- nokia: don't power down phones on disconnect
- hso: fix disconnection/disable

* Wed Aug 26 2009 Dan Williams <dcbw@redhat.com> - 0.2-3.20090826
- Fixes for Motorola and Ericsson devices
- Fixes for CDMA "serving-system" command parsing

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com>
- Fix a typo in one of the udev rules files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2.20090707
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 0.2-1.20090707
- Fix source repo location
- Fix directory ownership

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 0.2-0.20090707
- Initial version

## END: Generated by rpmautospec
