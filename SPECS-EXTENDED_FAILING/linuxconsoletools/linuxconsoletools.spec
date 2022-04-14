Vendor:         Microsoft Corporation
Distribution:   Mariner
%global udevdir %(pkg-config --variable=udevdir udev)

Name:           linuxconsoletools
Version:        1.7.0
Release:        4%{?dist}
Summary:        Tools for connecting joysticks & legacy devices to the kernel's input subsystem
License:        GPLv2
URL:            http://sourceforge.net/projects/linuxconsole/
Source:         http://downloads.sourceforge.net/linuxconsole/%{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  systemd-udev
BuildRequires:  libudev-devel

Provides:       joystick = %{version}-%{release}
Provides:       ff-utils = %{version}-%{release}
Obsoletes:      joystick < 1.2.16-1
Obsoletes:      ff-utils < 2.4.22-1
Conflicts:      gpm < 1.20.6-26


%description
This package contains utilities for testing and configuring joysticks,
connecting legacy devices to the kernel's input subsystem (providing support
for serial mice, touchscreens etc.), and test the input event layer.


%prep
%autosetup


%build
%{set_build_flags}
%{make_build} PREFIX=%{_prefix}

# moving helper scripts from /usr/share/joystick to /usr/libexec/joystick
sed -i "s|%{_datadir}/joystick|%{_libexecdir}/joystick|g" utils/jscal-restore utils/jscal-store


%install
%{make_install} PREFIX=%{_prefix}

# moving helper scripts from /usr/share/joystick to /usr/libexec/joystick
install -d -m 0755 %{buildroot}%{_libexecdir}/joystick
mv -f %{buildroot}%{_datadir}/joystick/* %{buildroot}%{_libexecdir}/joystick/

# fixing udev dir
mv -f %{buildroot}/lib %{buildroot}/usr/

# fixing man permissions
chmod -x %{buildroot}%{_mandir}/man1/*


%files
%doc README NEWS
%license COPYING
%{_bindir}/ffcfstress
%{_bindir}/ffmvforce
%{_bindir}/ffset
%{_bindir}/fftest
%{_bindir}/inputattach
%{_bindir}/jscal
%{_bindir}/jscal-restore
%{_bindir}/jscal-store
%{_bindir}/jstest
%{_bindir}/evdev-joystick

%{_libexecdir}/joystick

%{udevdir}/js-set-enum-leds
%{_udevrulesdir}/80-stelladaptor-joystick.rules

%{_mandir}/man1/*


%changelog
* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.0-4
- Removing epoch.
- License verified.

* Wed Jun 23 2021 Thomas Crain <thcrain@microsoft.com> - 1.7.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Require libudev-devel at build-time for the udev pkgconfig file

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Vasiliy N. Glazov <vascom2@gmail.com>  - 1.7.0-1
- Update to 1.7.0

* Fri Sep 20 2019 Vasiliy N. Glazov <vascom2@gmail.com>  - 1.6.1-2
- Fix store/restore utils handling #1753648

* Tue Aug 13 2019 Vasiliy N. Glazov <vascom2@gmail.com>  - 1.6.1-1
- Update to 1.6.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 15 2017 Michal Ambroz <rebus _at seznam.cz> - 1.6.0-1
- Updating to 1.6.0 (#1328645)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Jaromir Capik <jcapik@redhat.com> - 1.4.9-1
- Updating to 1.4.9 (#1297157)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Jaromir Capik <jcapik@redhat.com> - 1.4.8-1
- Updating to 1.4.8 (#1183543)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 08 2014 Jaromir Capik <jcapik@redhat.com> - 1.4.7-1
- Update to 1.4.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.6-1
- Update to 1.4.6

* Tue Apr 09 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.5-1
- Update to 1.4.5

* Wed Feb 06 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-7
- Adding new switches to the ffcfstress man page

* Wed Feb 06 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-6
- Merging the 64bit patch from ff-utils

* Mon Feb 04 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-5
- Resolving conflicts with ff-utils

* Fri Jan 04 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-4
- Adding conflict with gpm < 1.20.6-26 (inputattach)

* Thu Jan 03 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-3
- Passing optflags to make

* Wed Jan 02 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-2
- Using prefix macro

* Wed Jan 02 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-1
- Initial package
