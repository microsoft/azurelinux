# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 91900812333bb6ccca9ca0bf57363a3b1d3023a2
%global date 20231107
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

Summary: Cinnamon Screensaver
Name:    cinnamon-screensaver
Version: 6.4.0
Release: 4%{?dist}
# Automatically converted from old format: GPLv2+ and LGPLv2+ - review is highly recommended.
License: GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+
URL:     https://github.com/linuxmint/%{name}
%if 0%{?tag:1}
Source0: %url/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0: %url/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

ExcludeArch: %{ix86}

BuildRequires: desktop-file-utils
BuildRequires: meson
BuildRequires: gcc
BuildRequires: intltool
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gthread-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gdk-x11-3.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(libxdo)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(pam)
BuildRequires: python3-packaging

Requires: cinnamon-desktop%{?_isa} >= 6.2.0
Requires: cinnamon-translations >= 6.2.0
Requires: accountsservice-libs%{?_isa}
Requires: libgnomekbd%{?_isa}
Requires: python3-gobject%{?_isa}
Requires: python3-setproctitle%{?_isa}
Requires: python3-xapp
Requires: python3-xapps-overrides%{?_isa}
Requires: xapps%{?_isa}
Requires: xprop

# since we use it, and pam spams the log if a module is missing
Requires: gnome-keyring-pam%{?_isa}


%description
cinnamon-screensaver is a screen saver and locker.


%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif


%build
%meson
%meson_build


%install
%meson_install

desktop-file-install                                     \
  --delete-original                                      \
  --remove-only-show-in=Xfce                             \
  --dir %{buildroot}%{_datadir}/applications             \
  %{buildroot}%{_datadir}/applications/org.cinnamon.ScreenSaver.desktop

# Fix rpmlint errors
for file in %{buildroot}%{_datadir}/cinnamon-screensaver/{dbusdepot,util,widgets}/*.py; do
chmod a+x $file
done
for file in %{buildroot}%{_datadir}/cinnamon-screensaver/*.py; do
chmod a+x $file
done
chmod a-x %{buildroot}%{_datadir}/cinnamon-screensaver/{dbusdepot,util,widgets}/__init__.py
chmod a-x %{buildroot}%{_datadir}/cinnamon-screensaver/{__init__,config}.py
chmod a+x %{buildroot}%{_datadir}/cinnamon-screensaver/pamhelper/authClient.py

# Delete development files
rm %{buildroot}%{_datadir}/gir-1.0/CScreensaver-1.0.gir


%ldconfig_scriptlets


%files
%doc AUTHORS NEWS README.md
%license COPYING COPYING.LIB
%config(noreplace) %{_sysconfdir}/pam.d/cinnamon-screensaver
%{_bindir}/cinnamon-screensaver*
%{_bindir}/cinnamon-unlock-desktop
%{_datadir}/applications/org.cinnamon.ScreenSaver.desktop
%{_datadir}/cinnamon-screensaver/
%{_datadir}/dbus-1/services/org.cinnamon.ScreenSaver.service
%{_datadir}/icons/hicolor/scalable/*/*
%{_libexecdir}/cinnamon-screensaver/cinnamon-screensaver-pam-helper
%{_libexecdir}/cinnamon-screensaver/cs-backup-locker
%{_libexecdir}/cinnamon-screensaver/libcscreensaver.so
%{_libexecdir}/cinnamon-screensaver/girepository-1.0/CScreensaver-1.0.typelib

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 26 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.0-1
- Update to 6.4.0

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 6.2.0-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-1
- Update to 6.2.0

* Sat May 04 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.3-1
- Update to 6.0.3 release

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.2-2
- Revert upstream commit

* Fri Dec 29 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.2-1
- Update to 6.0.2 release

* Tue Dec 19 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-1
- Update to 6.0.1 release

* Sun Nov 19 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-1
- Update to 6.0.0 release

* Thu Nov 09 2023 Leigh Scott <leigh123linux@gmail.com> - 5.9.0-1.20231107git9190081
- Update to git snapshot

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-1
- Update to 5.8.0 release

* Sun May 28 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.3-3
- Add requires xprop

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.3-1
- Update to 5.6.3 release

* Tue Dec 13 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.2-1
- Update to 5.6.2 release

* Fri Nov 18 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.0-1
- Update to 5.6.0 release

* Sun Aug 21 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.4-1
- Update to 5.4.4 release

* Tue Aug 02 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.2-1
- Update to 5.4.2 release

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 16 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.1-1
- Update to 5.4.1 release

* Fri Jun 10 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-1
- Update to 5.4.0 release

* Sat May 28 2022 Leigh Scott <leigh123linux@gmail.com> - 5.2.1-1
- Update to 5.2.1 release

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 19 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.0-1
- Update to 5.2.0 release

* Thu Nov 04 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.7-1
- Update to 5.0.7 release

* Tue Aug 17 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.6-3
- Fix mpris album art

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.6-1
- Update to 5.0.6 release

* Mon Jun 14 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.5-1
- Update to 5.0.5 release

* Fri Jun 11 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.4-1
- Update to 5.0.4 release

* Thu Jun 10 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.3-1
- Update to 5.0.3 release

* Fri Jun 04 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.2-1
- Update to 5.0.2 release

* Tue Jun 01 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.1-1
- Update to 5.0.1 release

* Mon May 31 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.0-1
- Update to 5.0.0 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.1-1
- Update to 4.8.1 release

* Thu Nov 26 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.0-1
- Update to 4.8.0 release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 12 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.0-1
- Update to 4.6.0 release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-1
- Update to 4.4.1 release

* Sat Nov 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-1
- Update to 4.4.0 release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 23 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-1
- Update to 4.2.0 release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.3-1
- Update to 4.0.3 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.2-1
- Update to 4.0.2 release

* Mon Nov 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-1
- Update to 4.0.1 release

* Sat Nov 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0 release
- Add Obsoletes cinnamon-screensaver-unsupported

* Sun Oct 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.2-4
- Drop EPEL/RHEL support

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.8.2-2
- Rebuilt for Python 3.7

* Fri Jun 08 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.2-1
- Update to 3.8.2 release

* Sun May 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.1-1
- Update to 3.8.1 release

* Thu Apr 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.0-1
- Update to 3.8.0 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6.1-3
- Remove obsolete scriptlets

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 3.6.1-2
- Adaptions for EPEL7

* Mon Nov 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.1-1
- update to 3.6.1 release

* Wed Oct 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.0-2
- bump translations requires

* Mon Oct 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.0-1
- update to 3.6.0 release

* Thu Oct 12 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.3-1
- update to 3.4.3 release

* Fri Sep 01 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.2-3
- Some more changes for EPEL

* Wed Aug 30 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.2-2
- Adjustments for EPEL

* Wed Aug 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.2-1
- update to 3.4.2 release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.1-2
- add missing python3-xapp requires

* Wed Jun 21 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.1-1
- update to 3.4.1 release

* Thu May 04 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.0-1
- update to 3.4.0 release

* Fri Apr 21 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.0-0.1.20170421git358369e
- update to latest git snapshot

* Thu Mar 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.14-0.4.20170308git39da3f0
- update to latest git snapshot

* Wed Mar 08 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.14-0.3.20170308git55a26c2
- update to latest git snapshot

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.14-0.2.20170124git5561f3c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.14-0.1.20170124git5561f3c
- update to git snapshot

* Tue Jan 10 2017 leigh scott <leigh123linux@googlemail.com> - 3.2.13-2
- add some upstream commits (fixes rhbz 1399731)

* Sun Jan 08 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.13-1
- update to 3.2.13 release

* Sat Dec 24 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.12-1
- update to 3.2.12 release
- patch to hide message strings

* Thu Dec 22 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.11-1
- update to 3.2.11 release

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2.9-3
- Rebuild for Python 3.6

* Thu Dec 15 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.9-2
- patch to fix cinnamon-screensaver-pam-helper rpmlint error

* Mon Dec 12 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.9-1
- update to 3.2.9 release

* Sun Dec 11 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.7-2
- add missing requires python3-setproctitle

* Sat Dec 10 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.7-1
- update to 3.2.7 release

* Thu Nov 24 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.6-1
- update to 3.2.6 release

* Thu Nov 17 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.3-1
- update to 3.2.3 release

* Wed Nov 09 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.0-2
- Fix python gi requires

* Mon Nov 07 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.2.0-1
- update to 3.2.0 release

* Mon May 30 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.1-1
- update to 3.0.1 release

* Sat Apr 23 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.0-1
- update to 3.0.0 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.0-4
- remove unsupported sub-package for epel as there is no xscreensaver

* Fri Nov 27 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.0-3
- fix epel conditional

* Mon Nov 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.0-2
- rebuilt

* Fri Oct 16 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.0-1
- update to 2.8.0 release

* Mon Aug 24 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.4-4
- Try upstream commits to fix bz 1234998

* Sat Aug 01 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.4-3
- revert upstream commit as it kills the real process (bz 1234998)

* Mon Jun 29 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.4-2
- add missing requires to unsupported sub-package

* Fri Jun 26 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.4-1
- update to 2.6.4 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.3-2
- make sub-package noarch

* Wed Jun 03 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.3-1
- update to 2.6.3 release
- split webkit and xscreensaver into an unsupported sub-package

* Mon May 25 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.1-1
- update to 2.6.1 release

* Wed May 20 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.0-2
- add conditional for f20 webkit br

* Wed May 20 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.0-1
- update to 2.6.0 release

* Fri May 15 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.0-0.3.git024e5fd
- update to git snapshot

* Wed May 06 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.0-0.2.gitc4820fd
- update to git snapshot

* Tue May 05 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.0-0.1.git6ea738d
- update to git snapshot

* Tue Mar 31 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.2-1
- update to 2.4.2

* Sun Mar 29 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-3
- fix bz 1206907

* Wed Mar 18 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-2
- drop patch and use the upstream fix instead

* Sat Feb 21 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-1
- update to 2.4.1

* Fri Oct 31 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-1
- update to 2.4.0

* Fri Oct 03 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.3.git8de7ff0
- readd revert 58a522e commit

* Wed Oct 01 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.2.git8de7ff0
- update to latest git

* Tue Sep 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.1.gitaf298bc
- update to latest git

* Mon Aug 25 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-5
- apply upstream fix for CVE-2014-1949 (bz 1064695)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-3
- Fix CVE-2014-1949 (bz 1064695)

* Tue Aug 05 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-2
- revert 58a522e commit

* Fri Jun 27 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-1
- update to 2.2.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 11 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.3-1
- update to 2.2.3

* Fri May 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.1-1
- update to 2.2.1

* Thu Apr 24 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-2
- don't clear the window on every draw, just do it on realized

* Sat Apr 12 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-1
- update to 2.2.0

* Wed Oct 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.3-1
- update to 2.0.3
- add patch to fix suspend locking

* Thu Oct 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.2-1
- update to 2.0.2

* Fri Oct 18 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-1
- update to 2.0.1

* Thu Oct 17 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-2
- Stop starting in gnome-shell as it pissed off the gnome devs

* Wed Oct 02 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-1
- update to 2.0.0

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.1-1
- 1.9.1

* Sun Sep 15 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.1-0.2.git4f741eb
- update to latest git
- add requires cinnamon-translations

* Sun Aug 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.1-0.1.git94ca899
- update to latest git
- Change buildrequires to cinnamon-desktop-devel
- Change requires to cinnamon-desktop

* Thu Aug 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.0-5
- rebuilt

* Sun Jul 28 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.0-4
- disable console-kit in configure
- add systemd patch

* Mon Jul 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.0-3
- fix prep warnings

* Mon Jul 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.0-2
- fix prep warnings

* Thu Jan 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.0-1
- Initial build
