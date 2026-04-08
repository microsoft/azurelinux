# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libevdev
Version:        1.13.6
Release:        1%{?dist}
Summary:        Kernel Evdev Device Wrapper Library

# SPDX
License:        MIT
URL:            http://www.freedesktop.org/wiki/Software/libevdev
Source0:        http://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  git-core
BuildRequires:  meson gcc
BuildRequires:  python3 python3-rpm-macros

%description
%{name} is a library to wrap kernel evdev devices and provide a proper API
to interact with those devices.

%package devel
Summary:        Kernel Evdev Device Wrapper Library Development Package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Kernel Evdev Device Wrapper Library Development Package.

%package utils
Summary:        Kernel Evdev Device Wrapper Library Utilities Package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities to handle and/or debug evdev devices.

%prep
%autosetup -S git
# Replace whatever the source uses with the approved call
%py3_shebang_fix $(git grep -l  '#!/usr/bin/.*python3')

%build
%meson -Dtests=disabled -Ddocumentation=disabled -Dcoverity=false
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%doc COPYING
%{_libdir}/libevdev.so.*

%files devel
%dir %{_includedir}/libevdev-1.0/
%dir %{_includedir}/libevdev-1.0/libevdev
%{_includedir}/libevdev-1.0/libevdev/libevdev.h
%{_includedir}/libevdev-1.0/libevdev/libevdev-uinput.h
%{_libdir}/libevdev.so
%{_libdir}/pkgconfig/libevdev.pc
%{_mandir}/man3/libevdev.3*

%files utils
%{_bindir}/touchpad-edge-detector
%{_bindir}/mouse-dpi-tool
%{_bindir}/libevdev-tweak-device
%{_mandir}/man1/libevdev-tweak-device.1*
%{_mandir}/man1/touchpad-edge-detector.1*
%{_mandir}/man1/mouse-dpi-tool.1*

%changelog
* Mon Dec 01 2025 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.6-1
- libevdev 1.13.6

* Mon Oct 20 2025 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.5-1
- libevdev 1.13.5

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Mar 25 2025 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.4-1
- libevdev 1.13.4

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 03 2024 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.3-1
- libevdev 1.13.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Peter Hutterer <peter.hutterer@redhat.com> 1.13.2-2
- libevdev 1.13.2, with sources

* Fri May 31 2024 Peter Hutterer <peter.hutterer@redhat.com> 1.13.2-1
- libevdev 1.13.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 05 2023 Peter Hutterer <peter.hutterer@redhat.com>
- SPDX migration: licences is already SPDX compatible

* Thu Jul 20 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.1-2
- BuildRequires python3-rpm-macros for pathfix.py and use the rpm macro

* Fri May 05 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.1-1
- libevdev 1.13.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 02 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.0-1
- libevdev 1.13.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.12.1-1
- libevdev 1.12.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 09 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.12.0-1
- libevdev 1.12.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 01 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.11.0-1
- libevdev 1.11.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.10.1-1
- libevdev 1.10.1

* Mon Oct 26 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.10.0-1
- libevdev 1.10.0

* Tue Oct 20 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.9.902-1
- libevdev 1.10 rc2

* Tue Oct 06 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.9.901-1
- libevdev 1.10 rc1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-2
- libevdev 1.9.1 - this time with sources

* Thu Jul 16 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-1
- libevdev 1.9.1

* Thu Jun 04 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-2
- Use meson instead of autotools

* Mon Mar 02 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-1
- libevdev 1.9.0

* Fri Feb 21 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.8.901-1
- libevdev 1.9rc1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 26 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-1
- libevdev 1.8.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.7.0-1
- libevdev 1.7.0

* Fri May 24 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.6.901-1
- libevdev 1.7rc1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-1
- libevdev 1.6.0

* Fri Jul 13 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.5.9-5
- Add gcc as explicit BR. Pulled in by libtool atm but let's be
  explicit anyway

* Thu Jul 12 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.5.9-4
- Replace all python3 calls with the rpm macro
- Switch to autosetup git to match other packages

* Wed Apr 04 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.5.9-3
- Use python3 instead of python2
- use autosetup

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.5.9-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Mar 08 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.5.9-1
- libevdev 1.5.9

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5.8-2
- Switch to %%ldconfig_scriptlets

* Mon Jan 29 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.5.8-1
- libevdev 1.5.8

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 04 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.5.7-1
- libevdev 1.5.7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.5.6-1
- libevdev 1.5.6

* Thu Dec 01 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.5-1
- libevdev 1.5.5

* Fri Aug 26 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.4-1
- libevdev 1.5.4

* Mon Aug 22 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.3-1
- libevdev 1.5.3

* Wed Aug 17 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-2
- Fix complaints about double tracking IDs on the MagicMouse (#1361325)

* Wed Jun 15 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-1
- libevdev 1.5.2

* Mon May 16 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.1-1
- libevdev 1.5.1

* Fri May 13 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.0-1
- libevdev 1.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.4.5-2
- Fix a couple of coverity warnings
- Fix a potential race condition when checking uinput device's syspath
  (inactive in Fedora, we use the ioctl and never get here)

* Wed Nov 11 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.4.5-1
- libevdev 1.4.5

* Tue Sep 01 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.4.4-1
- libevdev 1.4.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.4.2-1
- libevdev 1.4.2

* Wed Apr 08 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.4.1-1
- libevdev 1.4.1

* Wed Mar 04 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.4-1
- libevdev 1.4

* Fri Dec 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.3.2-1
- libevdev 1.3.2

* Thu Nov 13 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.3.1-1
- libevdev 1.3.1

* Tue Sep 09 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.3-1
- libevdev 1.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.99.901-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.2.99.901-1
- libevdev 1.3RC1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-1
- libevdev 1.2.2

* Wed May 14 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-1
- libevdev 1.2.1

* Tue May 13 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.2-5
- Bump release to fix the upgrade path from F20 which is now named
  1.2-04compat.

* Wed Apr 30 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.2-1
- libevdev 1.2

* Thu Apr 24 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99.1-1
- libevdev 1.2 RC1

* Tue Mar 25 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.1-1
- libevdev 1.1

* Wed Mar 19 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.2-1
- libevdev 1.0.99.2

* Tue Mar 11 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.1-1
- libevdev 1.0.99.1
- Add libevdev-utils sub-package

* Fri Mar 07 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-1
- libevdev 1.0.1

* Tue Feb 18 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.0-1
- libevdev 1.0

* Wed Feb 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.9.1-1
- libevdev 1.0RC1

* Fri Jan 03 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.6-3
- Restore deprecated constants LIBEVDEV_READ_* dropped from 0.6 (#1046426)

* Thu Dec 26 2013 Adam Williamson <awilliam@redhat.com> 0.6-2
- revert catastrophic upstream dropping of 'deprecated' functions - #1046426

* Mon Dec 23 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.6-1
- libevdev 0.6

* Fri Nov 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.5-1
- libevdev 0.5

* Fri Nov 01 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.4.1-1
- libevdev 0.4.1

* Wed Oct 02 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.4-2
- disable gcov (#1012180)
- disable unittests, we don't run them anyway

* Wed Sep 18 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.4-1
- libevdev 0.4

* Tue Aug 13 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3-1
- libevdev 0.3

* Thu Jul 25 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.2.1-1
- Initial package (#987204)

