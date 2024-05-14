Name:           libxkbcommon
Version:        1.6.0
Release:        2%{?dist}
Summary:        X.Org X11 XKB parsing library
License:        MIT AND X11 AND MIT-CMU
URL:            https://www.x.org
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Source0:        https://xkbcommon.org/download/%{name}-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  byacc flex bison
BuildRequires:  xorg-x11-proto-devel libX11-devel
BuildRequires:  xkeyboard-config-devel
BuildRequires:  pkgconfig(xcb-xkb) >= 1.10
BuildRequires:  libxml2-devel

Requires:       xkeyboard-config

%description
%{name} is the X.Org library for compiling XKB maps into formats usable by
the X Server or other display servers.

%package devel
Summary:        X.Org X11 XKB parsing development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
X.Org X11 XKB parsing development package

%package x11
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description x11
%{name}-x11 is the X.Org library for creating keymaps by querying the X
server.

%package x11-devel
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}-x11%{?_isa} = %{version}-%{release}

%description x11-devel
X.Org X11 XKB keymap creation library development package

%package utils
Summary:        X.Org X11 XKB parsing utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
%{name}-utils is a set of utilities to analyze and test XKB parsing.

%prep
%autosetup

%build
%meson -Denable-docs=false \
       -Denable-x11=true \
       -Denable-wayland=false
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/libxkbcommon.so.0.0.0
%{_libdir}/libxkbcommon.so.0
%{_libdir}/libxkbregistry.so.0.0.0
%{_libdir}/libxkbregistry.so.0

%files devel
%{_libdir}/libxkbcommon.so
%{_libdir}/libxkbregistry.so
%dir %{_includedir}/xkbcommon/
%{_includedir}/xkbcommon/xkbcommon.h
%{_includedir}/xkbcommon/xkbcommon-compat.h
%{_includedir}/xkbcommon/xkbcommon-compose.h
%{_includedir}/xkbcommon/xkbcommon-keysyms.h
%{_includedir}/xkbcommon/xkbcommon-names.h
%{_includedir}/xkbcommon/xkbregistry.h
%{_libdir}/pkgconfig/xkbcommon.pc
%{_libdir}/pkgconfig/xkbregistry.pc

%ldconfig_scriptlets x11

%files x11
%{_libdir}/libxkbcommon-x11.so.0.0.0
%{_libdir}/libxkbcommon-x11.so.0

%files x11-devel
%{_libdir}/libxkbcommon-x11.so
%{_includedir}/xkbcommon/xkbcommon-x11.h
%{_libdir}/pkgconfig/xkbcommon-x11.pc

%files utils
%{_bindir}/xkbcli
%{_libexecdir}/xkbcommon/xkbcli-compile-keymap
%{_libexecdir}/xkbcommon/xkbcli-how-to-type
%{_libexecdir}/xkbcommon/xkbcli-interactive-evdev
%{_libexecdir}/xkbcommon/xkbcli-interactive-x11
%{_libexecdir}/xkbcommon/xkbcli-list
%{_mandir}/man1/xkbcli-compile-keymap.1.gz
%{_mandir}/man1/xkbcli-how-to-type.1.gz
%{_mandir}/man1/xkbcli-interactive-evdev.1.gz
%{_mandir}/man1/xkbcli-interactive-x11.1.gz
%{_mandir}/man1/xkbcli-list.1.gz
%{_mandir}/man1/xkbcli.1.gz
%{_datadir}/bash-completion/completions/xkbcli

%changelog
* Sun Feb 04 2024 Dan Streetman <ddstreet@ieee.org> - 1.6.0-2
- Update to version from Fedora 39.
- Next line is present only to avoid tooling failures, and does not indicate the actual package license.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- license verified
- remove git as build dep, as we don't need to use autpsetup -S git

* Mon Oct 09 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.0-1
- libxkbcommon 1.6.0

* Tue Sep 05 2023 Peter Hutterer <peter.hutterer@redhat.com>
- SPDX migration: update to SPDX license identifiers

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.0-1
- libxbkcommon 1.5.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 23 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.1-1
- libxkbcommon 1.4.1

* Mon Feb 07 2022 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-1
- libxkbcommon 1.4.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 13 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.1-1
- libxkbcommon 1.3.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 04 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-1
- libxkbcommon 1.3.0

* Thu Apr 08 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-1
- libxkbcommon 1.2.1

* Tue Apr 06 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-1
- libxkbcommon 1.2.0
- Fix Source link

* Wed Mar 10 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-1
- libxkbcommon 1.1.0
- remove the git snapshot handling, we haven't used it in 9 years

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.0.3-1
- libxkbcommon 1.0.3

* Mon Nov 23 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.0.2-1
- libxkbcommon 1.0.2

* Fri Sep 11 2020 Pete Walter <pwalter@fedoraproject.org> - 1.0.1-1
- libxkbcommon 1.0.1

* Mon Sep 07 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-1
- libxkbcommon 1.0.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-1
- libxkbcommon 0.10.0

* Fri Dec 13 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.9.1-3
- convert ssharp to the correct uppercase letter

* Fri Nov 01 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.9.1-2
- drop the wayland-devel BR, we disable the wayland test programs

* Fri Oct 25 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.9.1-1
- libxkbcommon 0.9.1

* Mon Oct 21 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.8.4-3
- switch to meson as build system

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.8.4-1
- libxkbcommon 0.8.4

* Wed Feb 13 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.8.3-1
- libxkbcommon 0.8.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 06 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.8.2-1
- libxkbcommon 0.8.2

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.8.0-6
- Rebuild with fixed binutils

* Mon Jul 30 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.8.0-5
- Fix invalid pointer passed to FreeStmt()

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.0-2
- Switch to %%ldconfig_scriptlets

* Tue Dec 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.8.0-1
- libxkbcommon 0.8.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Hans de Goede <hdegoede@redhat.com> - 0.7.1-3
- Add patch from upstream adding XF86Keyboard and XF86RFKill keysyms

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-1
- xkbcommon 0.7.1

* Mon Nov 14 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-1
- xkbcommon 0.7.0

* Fri Jun 03 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.6.1-1
- xkbcommon 0.6.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Dan Horák <dan[at]danny.cz> - 0.5.0-3
- always build the x11 subpackage

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 22 2014 Hans de Goede <hdegoede@redhat.com> - 0.5.0-1
- Update to 0.5.0 (#1154574)

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.3-2
- Require xkeyboard-config (#1145260)

* Wed Aug 20 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.3-1
- Update to 0.4.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-3
- make -x11 support conditional (f21+, #1000497)
- --disable-silent-rules

* Fri May 23 2014 Hans de Goede <hdegoede@redhat.com> - 0.4.2-2
- Bump release to 2 to avoid confusion with non official non scratch 0.4.2-1

* Thu May 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-1
- xkbcommon 0.4.2 (#1000497)
- own %%{_includedir}/xkbcommon/
- -x11: +ldconfig scriptlets
- -devel: don't include xkbcommon-x11.h
- run reautoconf in %%prep (instead of %%build)
- tighten subpkg deps via %%_isa
- .spec cleanup, remove deprecated stuff
- BR: pkgconfig(xcb-xkb) >= 1.10

* Wed Feb 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.4.0-1
- xkbcommon 0.4.0
- Add new xkbcommon-x11 and xkbcommon-x11-devel subpackages

* Tue Aug 27 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3.1-1
- xkbcommon 0.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 18 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3.0-1
- xkbcommon 0.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Adam Jackson <ajax@redhat.com> 0.2.0-1
- xkbcommon 0.2.0

* Mon Sep 17 2012 Thorsten Leemhuis <fedora@leemhuis.info> 0.1.0-8.20120917
- Today's git snapshot

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7.20120306
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.1.0-6.20120306
- BuildRequire xkeyboard-config-devel to get the right XKB target path (#799717)

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.1.0-5.20120306
- Today's git snapshot

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-4.20111109
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 0.1.0-3
- Today's git snap

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2.20101110
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 06 2010 Dave Airlie <airlied@redhat.com> 0.1.0-1.20101110
- inital import
