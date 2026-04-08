# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libwacom
Version:        2.18.0
Release:        1%{?dist}
Summary:        Tablet Information Client Library
Requires:       %{name}-data

License:        HPND
URL:            https://github.com/linuxwacom/libwacom

Source0:        https://github.com/linuxwacom/libwacom/releases/download/%{name}-%{version}/%{name}-%{version}.tar.xz

BuildRequires:  meson gcc
BuildRequires:  glib2-devel libgudev1-devel libevdev-devel
BuildRequires:  systemd systemd-devel
BuildRequires:  git-core
BuildRequires:  libxml2-devel

Requires:       %{name}-data = %{version}-%{release}

%description
%{name} is a library that provides information about Wacom tablets and
tools. This information can then be used by drivers or applications to tweak
the UI or general settings to match the physical tablet.

%package devel
Summary:        Tablet Information Client Library Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Tablet information client library development package.

%package data
Summary:        Tablet Information Client Library Data Files
BuildArch:      noarch

%description data
Tablet information client library data files.

%package utils
Summary:        Tablet Information Client Library Utilities Package
Requires:       %{name} = %{version}-%{release}
Requires:       python3-libevdev python3-pyudev

%description utils
Utilities to handle and/or debug libwacom devices.

%prep
%autosetup -S git

%build
%meson -Dtests=disabled -Ddocumentation=disabled
%meson_build

%install
%meson_install
install -d ${RPM_BUILD_ROOT}/%{_udevrulesdir}

%check
%meson_test

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_libdir}/libwacom.so.*
%{_bindir}/libwacom-list-local-devices
%{_bindir}/libwacom-update-db

%{_mandir}/man1/libwacom-list-local-devices.1*

%files devel
%dir %{_includedir}/libwacom-1.0/
%dir %{_includedir}/libwacom-1.0/libwacom
%{_includedir}/libwacom-1.0/libwacom/libwacom.h
%{_libdir}/libwacom.so
%{_libdir}/pkgconfig/libwacom.pc

%files data
%doc COPYING
%{_udevrulesdir}/65-libwacom.rules
%{_udevhwdbdir}/65-libwacom.hwdb
%dir %{_datadir}/libwacom
%{_datadir}/libwacom/*.tablet
%{_datadir}/libwacom/*.stylus
%dir %{_datadir}/libwacom/layouts
%{_datadir}/libwacom/layouts/*.svg

%files utils
%{_bindir}/libwacom-list-devices
%{_bindir}/libwacom-show-stylus
%{_mandir}/man1/libwacom-list-devices.1*
%{_mandir}/man1/libwacom-show-stylus.1*

%changelog
* Tue Feb 03 2026 Peter Hutterer <peter.hutterer@redhat.com> - 2.18.0-1
- libwacom 2.18.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Nov 12 2025 Peter Hutterer <peter.hutterer@redhat.com> - 2.17.0-1
- libwacom 2.17.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Peter Hutterer <peter.hutterer@redhat.com> - 2.16.1-1
- libwacom 2.16.1

* Fri Jun 13 2025 Peter Hutterer <peter.hutterer@redhat.com> - 2.16.0-1
- libwacom 2.16.0

* Fri Mar 21 2025 Peter Hutterer <peter.hutterer@redhat.com> - 2.15.0-1
- libwacom 2.15.0

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 Peter Hutterer <peter.hutterer@redhat.com> - 2.14.0-1
- libwacom 2.14.0

* Mon Sep 02 2024 Peter Hutterer <peter.hutterer@redhat.com> - 2.13.0-1
- libwacom 2.13.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Peter Hutterer <peter.hutterer@redhat.com> - 2.12.2-1
- libwacom 2.12.2

* Thu Jun 13 2024 Stephen Gallagher <sgallagh@redhat.com> - 2.12.1-2
- Fix typo in Release field

* Wed Jun 12 2024 Peter Hutterer <peter.hutterer@redhat.com> 2.12.1-1
- libwacom 2.12.1

* Thu Jun 06 2024 Peter Hutterer <peter.hutterer@redhat.com> 2.12.0-1
- libwacom 2.12

* Wed Feb 07 2024 Peter Hutterer <peter.hutterer@redhat.com> - 2.10.0-1
- libwacom 2.10.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.9.0-1
- libwacom 2.9.0

* Tue Sep 05 2023 Peter Hutterer <peter.hutterer@redhat.com>
- SPDX migration: update to SPDX identifiers.
  Turns out the COPYING file references the HPND, not MIT.

* Thu Aug 31 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.8.0-1
- libwacom 2.8.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 17 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.7.0-1
- libwacom 2.7.0

* Mon Jan 23 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.6.0-1
- libwacom 2.6.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 28 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.4.0-1
- libwacom 2.4.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-1
- libwacom 2.3.0

* Fri Mar 25 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.2.0-1
- libwacom 2.2.0

* Fri Feb 11 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.1.0-1
- libwacom 2.1.0

* Mon Jan 31 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.0.0-3
- Split utilities into a separate package (#2047568)
  libwacom-list-local-devices is the most commonly used one so let's leave
  that in the main package, the others are for debugging so let's move them
  out.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.0.0-1
- libwacom 2.0.0

* Mon Dec 13 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.99.1-1
- libwacom 1.99.1

* Wed Sep 01 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.12-1
- libwacom 1.12

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.11-1
- libwacom 1.11

* Wed Apr 28 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.10-1
- libwacom 1.10

* Thu Mar 25 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.9-2
- Add X1 Yoga6 data files (#1940872)

* Wed Feb 24 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.9-1
- libwacom 1.9

* Tue Feb 09 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.8-2
- Add tablet file for Lenovo Yoga 6

* Fri Jan 29 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.8-1
- libwacom 1.8

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.7-2
- Add tablet file for Lenovo ThinkPad P15 (#1914409)

* Thu Dec 17 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.7-1
- libwacom 1.7

* Wed Nov 04 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.6-2
- Change BuildRequires to git-core, we don't need full git

* Tue Nov 03 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.6-1
- libwacom 1.6

* Mon Aug 31 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.5-1
- libwacom 1.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.4.1-1
- libwacom 1.4.1

* Wed Jun 24 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.4-1
- libwacom 1.4

* Wed Mar 25 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.3-1
- libwacom 1.3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 23 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.2-2
- Disable documentation explicitly. Fedora uses --auto-features=enabled
  during the build.

* Mon Dec 23 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.2-1
- libwacom 1.2

* Thu Nov 07 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.1-2
- Require a libwacom-data package of the same version

* Mon Sep 16 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.1-1
- libwacom 1.1

* Mon Aug 26 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.0-1
- libwacom 1.0

* Thu Aug 08 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.99.901-1
- libwacom 1.0rc1
- switch to meson

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 12 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.33-1
- libwacom 0.33

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.32-2
- Move the udev rule to the noarch libwacom-data package (#1648743)

* Mon Nov 05 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.32-1
- libwacom 0.32

* Thu Aug 09 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.31-1
- libwacom 0.31

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 18 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.30-1
- libwacom 0.30

* Wed Mar 07 2018 Peter Hutterer <peter.hutterer@redhat.com>
- Switch URLs to github

* Mon Mar 05 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.29-1
- libwacom 0.29

* Tue Feb 13 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.28-3
- Fix PairedID entry causing a debug message in the udev rules

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.28-2
- Escape macros in %%changelog

* Thu Feb 08 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.28-1
- libwacom 0.28
- use autosetup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.26-3
- Switch to %%ldconfig_scriptlets

* Tue Oct 17 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.26-2
- run make check as part of the build (#1502637)

*  Fri Aug 25 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.26-1
- libwacom 0.26

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 11 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.25-1
- libwacom 0.25

* Wed Feb 15 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.24-1
- libwacom 0.24

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.23-2
- Upload the sources too...

* Fri Jan 20 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.23-1
- libwacom 0.23

* Fri Nov 11 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.22-2
- Add Lenovo X1 Yoga data file (#1389849)

* Wed Jul 20 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.22-1
- libwacom 0.22

* Fri Jun 17 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.21-1
- libwacom 0.21

* Wed Jun 08 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.20-1
- libwacom 0.20

* Tue Apr 26 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.19-1
- libwacom 0.19

* Fri Apr 01 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.18-2
- Add a custom quirk for HUION Consumer Control devices (#1314955)

* Fri Apr 01 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.18-1
- libwacom 0.18

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17-1
- libwacom 0.17

* Fri Nov 13 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16-1
- libwacom 0.16

* Sun Jul 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.15-3
- fix %%{_udevrulesdir} harder

* Sat Jul 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.15-2
- Use %%{_udevrulesdir} so rule.d doesn't inadvertantly end up in /
- Use %%license

* Wed Jul 08 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15-1
- libwacom 0.15

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 21 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13-2
- Don't label touchscreens as touchpads (#1208685)

* Mon Apr 20 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13-1
- libwacom 0.13

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.12-1
- libwacom 0.12

* Thu Nov 06 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.11-1
- libwacom 0.11

* Wed Aug 20 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.10-1
- libwacom 0.10

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.9-2
- Generate the rules file from the database

* Tue Mar 04 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.9-1
- libwacom 0.9

* Mon Jan 20 2014 Peter Hutterer <peter.hutterer@redhat.com> - 0.8-2
- Update rules file to current database

* Mon Oct 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.8-1
- libwacom 0.8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-3
- Disable silent rules

* Wed May 01 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-2
- Use stdout, not stdin for printing

* Tue Apr 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-1
- libwacom 0.7.1

* Fri Feb 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7-3
- Install into correct udev rules directory (#913723)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.7-1
- libwacom 0.7

* Fri Nov 09 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6.1-1
- libwacom 0.6.1
- update udev.rules files for new tablet descriptions

* Fri Aug 17 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-5
- remove %%defattr, not necessary anymore

* Mon Jul 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-4
- ... and install the rules in %%libdir

* Mon Jul 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-3
- udev rules can go into %%libdir now

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-1
- libwacom 0.6

* Tue May 08 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-3
- Fix crash with WACf* serial devices (if not inputattach'd) (#819191)

* Thu May 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-2
- Fix gnome-control-center crash for Bamboo Pen & Touch
- Generic styli needs to have erasers, default to two tools.

* Wed May 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-1
- Update to 0.5
- Fix sources again - as long as Source0 points to sourceforge this is a bz2

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> 0.4-1
- Update to 0.4

* Thu Mar 22 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3-6
- Fix udev rules generator patch to apply ENV{ID_INPUT_TOUCHPAD} correctly
  (#803314)

* Thu Mar 08 2012 Olivier Fourdan <ofourdan@redhat.com> 0.3-5
- Mark data subpackage as noarch and make it a requirement for libwacom
- Use generated udev rule file to list only known devices from libwacom
  database

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3-4
- libwacom-0.3-add-list-devices.patch: add API to list devices
- libwacom-0.3-add-udev-generator.patch: add a udev rules generater tool
- libwacom-0.3-add-bamboo-one.patch: add Bamboo One definition

* Tue Feb 21 2012 Olivier Fourdan <ofourdan@redhat.com> - 0.3-2
- Add udev rules to identify Wacom as tablets for libwacom

* Tue Feb 21 2012 Peter Hutterer <peter.hutterer@redhat.com>
- Source file is .bz2, not .xz

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 0.3-1
- Update to 0.3

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 0.2-1
- Update to 0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.1-1
- Initial import (#768800)
