## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname thermal_daemon

%bcond qt %[%{undefined rhel} || 0%{?rhel} < 10]

Name:		thermald
Version:	2.5.9
Release:	%autorelease
Summary:	Thermal Management daemon

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:	GPL-2.0-or-later
URL:		https://github.com/intel/%{pkgname}
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# No cpuid.h on other arches.
ExclusiveArch:	%{ix86} x86_64

BuildRequires:	make
BuildRequires:	autoconf autoconf-archive
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++
BuildRequires:	glib2-devel
BuildRequires:	libxml2-devel
BuildRequires:	systemd-rpm-macros
BuildRequires:  upower-devel
BuildRequires:  libevdev-devel
BuildRequires:  gtk-doc

Requires:	dbus%{?_isa}

Requires(pre):	glibc-common

%{?systemd_requires}

%description
%{name} monitors and controls platform temperature.

Thermal issues are important to handle proactively to reduce performance
impact.  %{name} uses the existing Linux kernel infrastructure and can
be easily enhanced.


%if %{with qt}
%package monitor
Summary:	Application for monitoring %{name}
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:	GPL-3.0-or-later

BuildRequires:	qcustomplot-qt5-devel
BuildRequires:	qt5-qtbase-devel

Requires:	hicolor-icon-theme
Requires:	%{name}%{?_isa}		== %{version}-%{release}

%description monitor
This package contains an Application to monitor %{name} for system
developers who want to enable application developers and their
customers with the responsive and flexible thermal management,
supporting optimal performance in desktop, clam-shell, mobile and
embedded devices.
%endif


%prep
%autosetup -n %{pkgname}-%{version} -p 1

# Create tmpfiles.d config.
mkdir -p fedora_addons
cat << EOF > fedora_addons/%{name}.conf
d %{_rundir}/%{name} 0755 root root -
EOF

%if %{with qt}
# Create desktop-file for the monitor-app.
cat << EOF > fedora_addons/%{name}-monitor.desktop
[Desktop Entry]
Name=%{name} Monitor
Comment=Application for monitoring %{name}
Icon=%{name}-monitor
Categories=System;Settings;
Exec=%{_bindir}/ThermalMonitor
Type=Application
StartupNotify=true
Terminal=false
EOF

# Create icon for the monitor-app.
cat << EOF > fedora_addons/%{name}-monitor.svg
<?xml version="1.0" encoding="iso-8859-1"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
<path style="fill:#EFEFEF;" d="M501.106,256c0,33.661-6.787,65.732-19.064,94.927L256,239.66L29.957,350.927
	C17.68,321.732,10.894,289.661,10.894,256C10.894,120.636,120.636,10.894,256,10.894S501.106,120.636,501.106,256z"/>
<path style="fill:#F15A29;" d="M430.294,256c0,22.43-4.238,43.869-11.961,63.564l-96.202-47.355c1.264-5.196,1.95-10.621,1.95-16.21
	c0-18.802-7.626-35.818-19.935-48.15l75.101-75.101C410.783,164.298,430.294,207.872,430.294,256z"/>
<path style="fill:#FBA026;" d="M418.332,319.564c-25.393,64.828-88.5,110.734-162.337,110.734
	c-73.826,0-136.933-45.895-162.337-110.723C85.935,299.879,81.698,278.43,81.698,256c0-96.256,78.042-174.298,174.298-174.298
	c48.128,0,91.702,19.51,123.25,51.047l-75.101,75.101c12.31,12.332,19.935,29.347,19.935,48.15c0,5.588-0.686,11.013-1.95,16.21
	L418.332,319.564z"/>
<path style="fill:#27AAE1;" d="M482.038,350.927c-37.093,88.227-124.34,150.179-226.043,150.179S67.046,439.154,29.953,350.927
	l63.706-31.352l96.212-47.365c-1.264-5.196-1.961-10.621-1.961-16.21c0-37.605,30.491-68.085,68.085-68.085
	c18.802,0,35.818,7.626,48.15,19.935c12.31,12.332,19.935,29.347,19.935,48.15c0,5.588-0.686,11.013-1.95,16.21l96.202,47.355
	L482.038,350.927z"/>
<circle style="fill:#EFEFEF;" cx="256" cy="256" r="21.787"/>
<g>
	<path style="fill:#231F20;" d="M191.566,307.802l-77.373,38.086c-5.398,2.657-7.62,9.187-4.963,14.584
		c1.895,3.851,5.762,6.085,9.781,6.085c1.614,0,3.255-0.362,4.802-1.122l77.373-38.087c5.398-2.657,7.62-9.187,4.963-14.584
		C203.495,307.369,196.965,305.147,191.566,307.802z"/>
	<path style="fill:#231F20;" d="M245.106,457.532c0,6.017,4.878,10.894,10.894,10.894c28.936,0,57.027-5.721,83.495-17.005
		c26.031-11.098,49.226-27.021,68.936-47.325c4.192-4.316,4.088-11.213-0.228-15.405c-4.317-4.19-11.213-4.087-15.405,0.229
		c-36.133,37.22-84.715,57.719-136.799,57.719C249.985,446.638,245.106,451.515,245.106,457.532z"/>
	<path style="fill:#231F20;" d="M415.931,379.26c1.884,1.293,4.028,1.912,6.153,1.912c3.47,0,6.88-1.655,8.993-4.731l0.15-0.219
		c3.403-4.961,2.142-11.742-2.82-15.145c-4.958-3.403-11.74-2.142-15.145,2.819l-0.15,0.219
		C409.708,369.076,410.969,375.856,415.931,379.26z"/>
	<path style="fill:#231F20;" d="M288.681,256.002c0-18.02-14.661-32.681-32.681-32.681s-32.681,14.661-32.681,32.681
		S237.98,288.683,256,288.683S288.681,274.022,288.681,256.002z M245.106,256.002c0-6.007,4.887-10.894,10.894-10.894
		c6.007,0,10.894,4.887,10.894,10.894c0,6.007-4.887,10.894-10.894,10.894C249.993,266.896,245.106,262.009,245.106,256.002z"/>
	<path style="fill:#231F20;" d="M512,256c0-68.378-26.628-132.665-74.982-181.017S324.379,0,256,0
		C187.622,0,123.335,26.629,74.982,74.983C26.629,123.335,0,187.622,0,256c0,34.321,6.685,67.638,19.868,99.032
		c0.015,0.039,0.026,0.078,0.042,0.118C59.97,450.433,152.639,512,255.996,512s196.025-61.567,236.085-156.851
		c0,0,0-0.001,0.001-0.002l0.002,0.003C505.299,323.726,512,290.367,512,256z M255.996,490.213
		c-91.135,0-173.186-52.313-211.823-134.142l150.511-74.087c4.58-2.255,6.98-7.387,5.774-12.348
		c-1.097-4.507-1.653-9.095-1.653-13.636c0-31.536,25.657-57.191,57.191-57.191c15.265,0,29.632,5.949,40.44,16.738
		c10.802,10.822,16.751,25.188,16.751,40.453c0,4.57-0.552,9.157-1.642,13.636c-1.206,4.961,1.194,10.094,5.775,12.348
		l150.499,74.086C429.182,437.898,347.131,490.213,255.996,490.213z M92.591,256c0-90.101,73.303-163.404,163.404-163.404
		c39.988,0,77.792,14.274,107.592,40.406l-59.981,59.984c-13.652-10.349-30.203-15.964-47.611-15.964
		c-43.549,0-78.979,35.429-78.979,78.979c0,3.354,0.218,6.721,0.651,10.076l-77.795,38.292
		C95.042,288.781,92.591,272.563,92.591,256z M378.993,148.407C405.126,178.206,419.4,216.011,419.4,256
		c0,16.559-2.443,32.779-7.276,48.367l0.001,0.002l-77.797-38.297c0.43-3.344,0.646-6.712,0.646-10.072
		c0-17.413-5.618-33.97-15.981-47.631l0.031,0.01L378.993,148.407z M431.875,314.091c6.176-18.676,9.312-38.169,9.312-58.091
		c0-45.811-16.535-89.081-46.766-123.018l5.449-5.448c4.254-4.254,4.254-11.152,0-15.406c-4.253-4.254-11.149-4.254-15.407,0
		l-5.449,5.449c-33.938-30.232-77.207-46.768-123.018-46.768C153.881,70.809,70.804,153.885,70.804,256
		c0,19.926,3.134,39.421,9.309,58.095L35.774,335.92c-9.286-25.546-13.986-52.377-13.986-79.92
		C21.787,126.855,126.854,21.787,256,21.787S490.213,126.855,490.213,256c0,27.547-4.701,54.378-13.987,79.922l0.002,0.003
		L431.875,314.091z"/>
</g>
</svg>
EOF

# Create ReadMe.txt for the monitor-app.
cat << EOF > fedora_addons/%{name}-monitor.ReadMe.txt
Running the thermald-monitor-app
--------------------------------

To communicate with thermald via dbus, the user has to be member
of the "power" group.  So make sure to add your user id to this
group before using the thermald-monitor-app.
EOF
%endif

NO_CONFIGURE=1 ./autogen.sh

# Create a sysusers.d config file
cat >thermald.sysusers.conf <<EOF
g power -
EOF


%build
%configure									\
	--with-systemdsystemunitdir=%{_unitdir}					\
	--disable-option-checking						\
	--disable-silent-rules

%make_build

%if %{with qt}
# Build the monitor-app.
pushd tools/thermal_monitor
sed -i -e 's/QCustomPlot/qcustomplot-qt5/' ThermalMonitor.pro
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..
%make_build
popd
popd
%endif


%install
%make_install

# Install management-script.
install -Dpm 0755 tools/thermald_set_pref.sh				\
	%{buildroot}%{_bindir}/%{name}-set-pref

# Setup tmpfiles.d
install -Dpm 0644 fedora_addons/%{name}.conf %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -dm 0755 %{buildroot}%{_rundir}/%{name}
/bin/echo "%{name}_pid" > %{buildroot}%{_rundir}/%{name}/%{name}.pid
chmod -c 0644 %{buildroot}%{_rundir}/%{name}/%{name}.pid

%if %{with qt}
# Install the monitor-app.
install -Dpm 0755 tools/thermal_monitor/%{_target_platform}/ThermalMonitor	\
	%{buildroot}%{_bindir}/ThermalMonitor
install -Dpm 0644 fedora_addons/%{name}-monitor.desktop			\
	%{buildroot}%{_datadir}/applications/%{name}-monitor.desktop
install -Dpm 0644 fedora_addons/%{name}-monitor.svg			\
	%{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-monitor.svg
%endif

install -m0644 -D thermald.sysusers.conf %{buildroot}%{_sysusersdir}/thermald.conf


%check
%if %{with qt}
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
%endif




%post
%systemd_post thermald.service


%preun
%systemd_preun thermald.service


%postun
%systemd_postun_with_restart thermald.service

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/%{name}
%doc README.txt thermal_daemon_usage.txt
%ghost %dir %{_rundir}/%{name}
%ghost %{_rundir}/%{name}/%{name}.pid
%{_bindir}/%{name}-set-pref
%{_datadir}/dbus-1/system-services/org.freedesktop.%{name}.service
%{_datadir}/dbus-1/system.d/org.freedesktop.%{name}.conf
%{_mandir}/man5/thermal-conf.xml.5*
%{_mandir}/man8/%{name}.8*
%{_sbindir}/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_sysusersdir}/thermald.conf


%if %{with qt}
%files monitor
%doc fedora_addons/%{name}-monitor.ReadMe.txt
%license tools/thermal_monitor/COPYING
%{_bindir}/ThermalMonitor
%{_datadir}/applications/%{name}-monitor.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}-monitor.svg
%endif


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.5.9-3
- test: add initial lock files

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 12 2025 Björn Esser <besser82@fedoraproject.org> - 2.5.9-1
- Update to 2.5.9, Fixes: rhbz#2272271

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.8-3
- Add sysusers.d config file to allow rpm to create users/groups
  automatically

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 15 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.5.8-1
- Update to 2.5.8

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 2.5.6-5
- convert GPLv2+ license to SPDX

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 2.5.6-4
- convert GPLv3+ license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.6-2
- Call getent/groupadd without full path

* Sun Feb 11 2024 Peter Robinson <pbrobinson@gmail.com> - 2.5.6-1
- Update to 2.5.6, spec cleanups

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.5-6
- Disable monitor in RHEL builds

* Sun Jul 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.5-5
- Fix build with latest systemd

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 17 2022 Kalev Lember <klember@redhat.com> - 2.5-2
- Fix the build

* Tue Aug 16 2022 Kalev Lember <klember@redhat.com> - 2.5-1
- Update to 2.5

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 09 2022 Benjamin Berg <bberg@redhat.com> - 2.4.8-4
- Pull in adaptive fixes/improvements and p-p-d integration

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Benjamin Berg <bberg@redhat.com> - 2.4.8-1
- Update to 2.4.8 (#2038523)

* Wed Nov 24 2021 Benjamin Berg <bberg@redhat.com> - 2.4.6-3
- Pull AlderLake and JasperLake support from upstream

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Benjamin Berg <bberg@redhat.com> - 2.4.6-1
- Update to 2.4.6 (#1965783)
- Update main license to GPLv2 only for now
- Add bundled(qcustomplot) for monitor subpackage

* Fri May 14 2021 Benjamin Berg <bberg@redhat.com> - 2.4.4-1
- Update to 2.4.4
  Resolves: #1935728

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.1-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Feb 02 2021 Benjamin Berg <bberg@redhat.com> - 2.4.1-3
- Add upstream patch fixing parsing of passive targets

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Benjamin Berg <bberg@redhat.com> - 2.4.1-1
- New upstream release (#1903094)

* Thu Nov 26 2020 Benjamin Berg <bberg@redhat.com> - 2.4-1
- New upstream release (#1901810)
  Resolves: #1894178
  Resolves: #1892534

* Tue Sep 01 2020 Benjamin Berg <bberg@redhat.com> - 2.3-2
- Fix Lenovo kill switch (#1874462)

* Tue Aug 25 2020 Benjamin Berg <bberg@redhat.com> - 2.3-1
- New upstream release 2.3 (rhbz#1866784)
- Add patch to fix printf on non-64 bit

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Benjamin Berg <bberg@redhat.com> - 2.2-1
- New upstream release 2.2 (rhbz#1827883)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Benjamin Berg <bberg@redhat.com> - 1.9.1-1
- New upstream release 1.9 (rhbz#1782249)
- Drop Patch0, it has been merged upstream

* Fri Sep 20 2019 Christian Kellner <ckellner@redhat.com> - 1.9-1
- New upstream release 1.9 (rhbz#1742290)
- Update patch0 (taken from upstream, commit dcdaf52...)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Benjamin Berg <bberg@redhat.com> - 1.8-2
- Fix build on i686

* Fri May 17 2019 Benjamin Berg <bberg@redhat.com> - 1.8-1
- New upstream release (#1582506)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 28 2017 Björn Esser <besser82@fedoraproject.org> - 1.7.1-1
- New upstream release (#1505144)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 01 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-6
- Add upstreamed patch to silence compiler warnings

* Sat Jul 01 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-5
- Replace fix for rhbz#1464548 from upstream commit
- Add upstream patch to fix README

* Fri Jun 30 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-4
- Add upstream patch to fix ThermalMonitor (rhbz#1464548)
- Add several fixes from upstream

* Tue Apr 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-3
- Explicitly turn on hardening, if required

* Tue Apr 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-2
- Fix missing trailing semicolon in desktop-file

* Tue Apr 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-1
- Initial import (rhbz#1440406)

* Mon Apr 10 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.4
- Use qmake_qt5-macro and build out of tree

* Sat Apr 08 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.3
- Small packaging improvements

* Sat Apr 08 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.2
- Add management-script

* Sat Apr 08 2017 Björn Esser <besser82@fedoraproject.org> - 1.6-0.1
- Initial rpm-release (rhbz#1440406)

## END: Generated by rpmautospec
