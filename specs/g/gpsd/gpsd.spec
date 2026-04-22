# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname gpsd

# RHEL builds the core, EPEL builds the libs
%global with_core %{undefined epel}
# libgps ABI changes too frequently to be provided in RHEL
%global with_libs %[%{defined fedora} || %{defined epel} || %{defined eln}]
# requires qt-4.x
%global with_qt %{defined fedora}
# scons is not available in RHEL
%global with_bundled_scons %{defined rhel}

%if 0%{?epel}
Name:           gpsd-epel
%else
Name:           gpsd
%endif
Version:        3.26.1
Release: 7%{?dist}
Epoch:          1
Summary:        Service daemon for mediating access to a GPS

License:        BSD-2-Clause
URL:            https://gpsd.gitlab.io/gpsd/index.html
Source0:        https://download-mirror.savannah.gnu.org/releases/gpsd/%{pkgname}-%{version}.tar.gz
# used only for building
%global scons_ver 4.9.1
Source1:        https://github.com/SCons/scons/archive/%{scons_ver}/scons-%{scons_ver}.tar.gz
%if %{with_bundled_scons}
%global scons %{python3} scons-%{scons_ver}/scripts/scons.py
%else
%global scons scons
%endif
Source11:       gpsd.sysconfig

# Add old status names to gps.h for compatibility
Patch1:         gpsd-apistatus.patch
# Fix buffer overflow in NMEA2000 driver
Patch2:         gpsd-cve-2025-67268.patch
# Fix integer underflow in handling of Navcom packets
Patch3:         gpsd-cve-2025-67269.patch

BuildRequires:  gcc
BuildRequires:  dbus-devel
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  gtk3-devel
%if !%{with_bundled_scons}
BuildRequires:  python3-scons
%endif
BuildRequires:  python3-gobject
BuildRequires:  python3-cairo
BuildRequires:  python3-pyserial
BuildRequires:  desktop-file-utils
BuildRequires:  bluez-libs-devel
BuildRequires:  pps-tools-devel
BuildRequires:  systemd-rpm-macros
%if %{with_qt}
BuildRequires:  gcc-c++
BuildRequires:  qt-devel
%endif
BuildRequires:  libusb1-devel

Requires:       udev
%{?systemd_requires}

%if !%{with_libs}
Obsoletes:      gpsd-libs < %{epoch}:%{version}-%{release}
Obsoletes:      gpsd-devel < %{epoch}:%{version}-%{release}
%endif

%description
gpsd is a service daemon that mediates access to a GPS sensor
connected to the host computer by serial or USB interface, making its
data on the location/course/velocity of the sensor available to be
queried on TCP port 2947 of the host computer.  With gpsd, multiple
GPS client applications (such as navigational and war-driving software)
can share access to a GPS without contention or loss of data.  Also,
gpsd responds to queries with a format that is substantially easier to
parse than NMEA 0183.

%if %{with_libs}
%package -n %{pkgname}-libs
Summary:        Client libraries in C for talking to a running gpsd or GPS

%description -n %{pkgname}-libs
This package contains the gpsd libraries that manage access
to a GPS for applications.

%package -n %{pkgname}-devel
Summary:        Development files for the gpsd library
Requires:       %{pkgname}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description -n %{pkgname}-devel
This package provides C header files for the gpsd shared libraries that
manage access to a GPS for applications
%endif

%if %{with_qt}
%package -n %{pkgname}-qt
Summary:        C++/Qt5 bindings for the gpsd library
%if %{with_libs}
Requires:       %{pkgname}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%endif

%description -n %{pkgname}-qt
This package provide C++ and Qt bindings for use with the libgps library from
gpsd.

%package -n %{pkgname}-qt-devel
Summary:        Development files for the C++/Qt5 bindings for the gpsd library
Requires:       %{pkgname}-qt%{?_isa} = %{epoch}:%{version}-%{release}

%description -n %{pkgname}-qt-devel
This package provides the development files for the C++ and Qt bindings for use
with the libgps library from gpsd.
%endif

%if %{with_core}
%package -n python3-%{name}
Summary:        Python libraries and modules for use with gpsd
Requires:       python3-pyserial
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
This package contains the python3 modules that manage access to a GPS for
applications.

%package clients
Summary:        Clients for gpsd
Requires:       python3-%{name} = %{epoch}:%{version}-%{release}
%if %{with_libs}
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%endif

%description clients
This package contains various clients using gpsd.

%package xclients
Summary:        Graphical clients for gpsd
Requires:       python3-%{name} = %{epoch}:%{version}-%{release}
Requires:       python3-cairo
Requires:       python3-gobject
Requires:       gtk3
# subpackage split
Conflicts:      gpsd-clients < 1:3.25-6

%description xclients
This package contains X clients using gpsd.

%package compat
Summary:        Transitional package for gpsd-clients
Obsoletes:      gpsd-clients < 1:3.25-6
Requires:       gpsd-clients = %{epoch}:%{version}-%{release}
Requires:       gpsd-xclients = %{epoch}:%{version}-%{release}

%description compat
This package only exists to help transition gpsd-clients users to the new
package split. It will be removed after one distribution release cycle, please
do not reference it or depend on it in any way.
%endif

%prep
%setup -q -n %{pkgname}-%{version}
%autopatch -p1

%if %{with_bundled_scons}
%setup -q -T -D -a 1
%endif

# don't try reloading systemd when installing in the build root
sed -i 's|systemctl daemon-reload|true|' SConscript

iconv -f iso8859-1 -t utf8 NEWS > NEWS_ && mv NEWS_ NEWS

%build
export CCFLAGS="%{optflags}"
# scons ignores LDFLAGS. LINKFLAGS partially work (some flags like
# -spec=... are filtered)
export LINKFLAGS="%{__global_ldflags}"

# breaks with %%{_smp_mflags}
%{scons} \
    dbus_export=yes \
    systemd=yes \
%if %{with_qt}
    qt=yes \
%else
    qt=no \
%endif
    debug=yes \
    leapfetch=no \
    manbuild=no \
    prefix="" \
    sysconfdif=%{_sysconfdir} \
    bindir=%{_bindir} \
    includedir=%{_includedir} \
    libdir=%{_libdir} \
    sbindir=%{_sbindir} \
    mandir=%{_mandir} \
    mibdir=%{_docdir}/gpsd \
    docdir=%{_docdir}/gpsd \
    pkgconfigdir=%{_libdir}/pkgconfig \
    icondir=%{_datadir}/gpsd \
    udevdir=$(dirname %{_udevrulesdir}) \
    unitdir=%{_unitdir} \
    target_python=python3 \
    python_shebang=%{python3} \
    python_libdir=%{python3_sitearch} \
    build

%install
# avoid rebuilding
export CCFLAGS="%{optflags}"
export LINKFLAGS="%{__global_ldflags}"

DESTDIR=%{buildroot} %{scons} install systemd_install udev-install

%if %{with_core}
# use the old name for udev rules
mv %{buildroot}%{_udevrulesdir}/{25,99}-gpsd.rules

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE11} \
    %{buildroot}%{_sysconfdir}/sysconfig/gpsd

# Install the .desktop files
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    gpsd-%{version}/packaging/X11/xgps.desktop
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    gpsd-%{version}/packaging/X11/xgpsspeed.desktop

# Missed in scons install
install -p -m 0755 gpsinit %{buildroot}%{_sbindir}
%endif

# Remove shebang and fix permissions
sed -i '/^#!.*python/d' %{buildroot}%{python3_sitearch}/gps/{aio,}gps.py
chmod 644 %{buildroot}%{python3_sitearch}/gps/gps.py

rm -f %{buildroot}%{_libdir}/libgpsdpacket.so

# Remove unpackaged files
%if !%{with_core}
rm -rf %{buildroot}%{_sbindir}
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_sysconfdir}
rm -f %{buildroot}%{_libdir}/libgpsdpacket.so*
rm -rf %{buildroot}%{python3_sitearch}
rm -rf %{buildroot}%{_unitdir}
rm -rf %{buildroot}%{_udevrulesdir}
rm -rf %{buildroot}%{_datadir}/gpsd
rm -rf %{buildroot}%{_mandir}/man[18]
%endif
%if !%{with_libs}
rm -f %{buildroot}%{_libdir}/lib{gps*.so,gps.so.*}
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_mandir}/man{3,5}
%endif
%if !%{with_qt}
rm -f %{buildroot}%{_libdir}/libQgpsmm* \
    %{buildroot}%{_libdir}/pkgconfig/Qgpsmm* \
    %{buildroot}%{_mandir}/man3/libQgpsmm.3*
%endif
rm -rf %{buildroot}%{_docdir}/gpsd

%if %{with_core}
%post
%systemd_post gpsd.service gpsd.socket

%preun
%systemd_preun gpsd.service gpsd.socket

%postun
# Don't restart the service
%systemd_postun gpsd.service gpsd.socket
%endif

%if %{with_libs}
%ldconfig_scriptlets libs
%endif

%if %{with_qt}
%ldconfig_scriptlets qt
%endif

%if %{with_core}
%files
%doc README.adoc NEWS
%license COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/gpsd
%{_sbindir}/gpsdctl
%{_sbindir}/gpsinit
%{_bindir}/gpsmon
%{_bindir}/gpsctl
%{_bindir}/ntpshmmon
%{_bindir}/ppscheck
%{_unitdir}/gpsd.service
%{_unitdir}/gpsd.socket
%{_unitdir}/gpsdctl@.service
%{_udevrulesdir}/*.rules
%{_mandir}/man8/gpsd.8*
%{_mandir}/man8/gpsdctl.8*
%{_mandir}/man8/gpsinit.8*
%{_mandir}/man8/ppscheck.8*
%{_mandir}/man1/gpsmon.1*
%{_mandir}/man1/gpsctl.1*
%{_mandir}/man1/ntpshmmon.1*
%endif

%if %{with_libs}
%files -n %{pkgname}-libs
%{_libdir}/libgps.so.31*

%files -n %{pkgname}-devel
%doc TODO HACKING
%{_libdir}/libgps.so
%{_libdir}/pkgconfig/libgps.pc
%{_includedir}/gps.h
%{_includedir}/libgpsmm.h
%{_mandir}/man3/libgps.3*
%{_mandir}/man3/libgpsmm.3*
%{_mandir}/man5/gpsd_json.5*
%endif

%if %{with_qt}
%files -n %{pkgname}-qt
%{_libdir}/libQgpsmm.so.31*

%files -n %{pkgname}-qt-devel
%{_libdir}/libQgpsmm.so
%{_libdir}/libQgpsmm.prl
%{_libdir}/pkgconfig/Qgpsmm.pc
%{_mandir}/man3/libQgpsmm.3*
%endif

%if %{with_core}
%files -n python3-%{name}
%license COPYING
%{_libdir}/libgpsdpacket.so*
%{python3_sitearch}/gps*

%files clients
%{_bindir}/cgps
%{_bindir}/gegps
%{_bindir}/gps2udp
%{_bindir}/gpscat
%{_bindir}/gpscsv
%{_bindir}/gpsdebuginfo
%{_bindir}/gpsdecode
%{_bindir}/gpslogntp
%{_bindir}/gpspipe
%{_bindir}/gpsplot
%{_bindir}/gpsprof
%{_bindir}/gpsrinex
%{_bindir}/gpssnmp
%{_bindir}/gpssubframe
%{_bindir}/gpxlogger
%{_bindir}/lcdgps
%{_bindir}/gpsfake
%{_bindir}/ubxtool
%{_bindir}/zerk
%{_mandir}/man1/gegps.1*
%{_mandir}/man1/gps.1*
%{_mandir}/man1/gps2udp.1*
%{_mandir}/man1/gpscsv.1*
%{_mandir}/man1/gpsdebuginfo.1*
%{_mandir}/man1/gpsdecode.1*
%{_mandir}/man1/gpslogntp.1*
%{_mandir}/man1/gpspipe.1*
%{_mandir}/man1/gpsplot.1*
%{_mandir}/man1/gpsprof.1*
%{_mandir}/man1/gpsrinex.1*
%{_mandir}/man1/gpssnmp.1*
%{_mandir}/man1/gpssubframe.1*
%{_mandir}/man1/gpxlogger.1*
%{_mandir}/man1/lcdgps.1*
%{_mandir}/man1/cgps.1*
%{_mandir}/man1/gpscat.1*
%{_mandir}/man1/gpsfake.1*
%{_mandir}/man1/ubxtool.1*
%{_mandir}/man1/zerk.1*

%files xclients
%{_bindir}/xgps
%{_bindir}/xgpsspeed
%{_datadir}/applications/*.desktop
%dir %{_datadir}/gpsd
%{_datadir}/gpsd/gpsd-logo.png
%{_mandir}/man1/xgps.1*
%{_mandir}/man1/xgpsspeed.1*

%files compat
%endif

%changelog
* Mon Jan 12 2026 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.26.1-6
- fix buffer overflow in NMEA2000 driver (CVE-2025-67268)
- fix integer underflow in handling of Navcom packets (CVE-2025-67269)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:3.26.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:3.26.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1:3.26.1-2
- Rebuilt for Python 3.14

* Mon May 19 2025 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.26.1-1
- update to 3.26.1

* Tue May 06 2025 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.25-17
- bundle scons in eln and rhel source rpm

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:3.25-15
- Refactor for ELN and EPEL

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1:3.25-13
- Rebuilt for Python 3.13

* Thu Apr 25 2024 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.25-12
- fix icon path in desktop files

* Mon Apr 22 2024 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.25-11
- fix dependencies for build without libs
- fix annobin coverage

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 03 2023 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.25-8
- disable libs and devel subpackages on RHEL
- don't require libs in main package

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.25-6
- split X clients to separate subpackage
- add missing dependencies for python clients
- add explicit gcc dependency
- drop xmlto from build dependencies
- enable libusb1-devel on s390x
- fix qt build option
- fix spec indentation

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1:3.25-5
- Rebuilt for Python 3.12

* Thu May 11 2023 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.25-4
- convert NEWS to UTF-8
- remove shebang in python module files and fix permissions
- remove unnecessary .so symlink
- update URL

* Sun Mar 12 2023 Tim Orling <ticotimo@gmail.com> - 1:3.25-3
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.25-1
- update to 3.25

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:3.24-2
- Rebuilt for Python 3.11

* Wed May 04 2022 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.24-1
- update to 3.24

* Sat Feb 12 2022 Jeff Law <jeffreyalaw@gmail.com> - 1:3.23.1-3
- Re-enable LTO

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 27 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.23.1-1
- update to 3.23.1
- add old status names to gps.h for compatibility

* Wed Aug 11 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.23-1
- update to 3.23

* Wed Aug 11 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.22-5
- fix handling of GPS weeks after 2180 (#1989379)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:3.22-3
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.22-1
- update to 3.22
- keep all python modules in python subpackage
- move gpsprof to clients subpackage
- disable LTO on aarch64

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 18 2020 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.20-1
- update to 3.20

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:3.19-6
- Rebuilt for Python 3.9

* Mon Feb 03 2020 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.19-5
- fix missing epoch in dependencies (#1797370)

* Fri Jan 31 2020 Dan Horák <dan[at]danny.cz> - 1:3.19-2
- all Requires must use Epoch too

* Tue Jan 28 2020 Miroslav Lichvar <mlichvar@redhat.com> - 1:3.19-1
- revert to 3.19 (#1787784)

* Tue Jan 21 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.20-2
- Update to latest upstream release 3.20

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.19-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.19-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Miroslav Lichvar <mlichvar@redhat.com> - 3.19-1
- update to 3.19
- fix systemd scriptlet (#1716467)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 24 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.18.1-1
- update to 3.18.1

* Tue Oct 09 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.18-3
- fix paths in systemd unit files

* Tue Oct 09 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.18-2
- use python3 scons and fix build requirements for xgps

* Thu Oct 04 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.18-1
- update to 3.18
- drop python2 subpackage (#1633793)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.17-4
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.17-2
- use macro for systemd scriptlet dependencies
- use macro for ldconfig scriptlets

* Fri Sep 08 2017 Troy Curtis, Jr <troycurtisjr@gmail.com> - 3.17-1
- Update to 3.17
- Build both python2 and python3 files and install into separate subpackages
- Add Qt5 subpackage

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Miroslav Lichvar <mlichvar@redhat.com> - 3.16-1
- update to 3.16

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Miroslav Lichvar <mlichvar@redhat.com> - 3.15-1
- update to 3.15

* Tue Apr 21 2015 Miroslav Lichvar <mlichvar@redhat.com> - 3.14-1
- update to 3.14

* Fri Mar 06 2015 Rex Dieter <rdieter@fedoraproject.org> 3.13-2
- track library sonames and api files closer, so bumps aren't a surprise

* Mon Mar 02 2015 Miroslav Lichvar <mlichvar@redhat.com> - 3.13-1
- update to 3.13

* Mon Aug 25 2014 Miroslav Lichvar <mlichvar@redhat.com> - 3.11-1
- update to 3.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-6.20140524gitd6b65b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 Miroslav Lichvar <mlichvar@redhat.com> - 3.10-5.20140524gitd6b65b
- update to 20140524gitd6b65b
- fix PPS with large offsets
- set gpsd revision string to include package revision

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-4.20140127gitf2753b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Miroslav Lichvar <mlichvar@redhat.com> - 3.10-3.20140127gitf2753b
- update to 20140127gitf2753b
- replace udev hotplug script with gpsdctl service (#909563)
- add dependency on gpsd.socket to gpsd.service
- reenable dbus export

* Fri Dec 20 2013 Miroslav Lichvar <mlichvar@redhat.com> - 3.10-2
- use systemd socket activation (#909563)
- don't use -n in default gpsd service options
- update gpsd service file

* Mon Nov 25 2013 Miroslav Lichvar <mlichvar@redhat.com> - 3.10-1
- update to 3.10
- move udev rules from /etc to /usr/lib (#971851)
- enable hardened build (#1000643)
- drop also supplementary groups when dropping privileges
- set time stamp in chrony SOCK sample correctly
- remove RPATH from all files
- don't package INSTALL file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 02 2013 Miroslav Lichvar <mlichvar@redhat.com> - 3.9-1
- update to 3.9
- move files from /lib

* Wed Feb 27 2013 Miroslav Lichvar <mlichvar@redhat.com> - 3.8-1
- update to 3.8
- use systemd macros (#850135)
- don't set vendor for desktop files
- make some dependencies arch-specific
- remove obsolete macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Miroslav Lichvar <mlichvar@redhat.com> - 3.5-1
- update to 3.5

* Thu Jan 26 2012 Miroslav Lichvar <mlichvar@redhat.com> - 3.4-1
- update to 3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.3-1
- update to 3.3

* Mon Aug 29 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.1-1
- update to 3.1

* Tue Aug 23 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.0-1
- update to 3.0
- enable PPSAPI support
- fix PPS without -N
- change service type to simple
- start after chrony
- fix permissions of systemd unit file
- fix ldconfig scriptlets
- package client-howto.txt

* Tue Jul 26 2011 Miroslav Lichvar <mlichvar@redhat.com> - 2.95-7
- make -libs subpackage (#663124)
- replace SysV initscript with systemd service (#717419)
- explicitly set USBAUTO=true in sysconfig file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.95-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 2.95-5
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.95-4
- don't crash in gpscat when started without arguments (#633117)

* Fri Aug 27 2010 Dan Horák <dan[at]danny.cz> - 2.95-3
- no USB on s390(x)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.95-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.95-1
- update to 2.95
- add /usr/sbin to PATH in gpsd.hotplug.wrapper
- pass sysconfig variables to gpsd started from udev
- enable libusb support

* Thu May 06 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.94-1
- update to 2.94 (#556642)

* Tue Mar 02 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.39-7
- don't use deprecated SYSFS{} in udev rules (#569089)
- fix init script LSB compliance

* Mon Feb 15 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.39-6
- fix linking with --no-add-needed (#564662)
- use %%global macro instead of %%define

* Wed Aug 12 2009 Marek Mahut <mmahut@fedoraproject.org> - 2.39-5
- RHBZ#505588: gpsd has a broken initscript that fails to launch daemon

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.39-3
- some of the gpsd client bits went into gpsdclient.h, but that file wasn't getting installed
  specifically, viking needs that header to build.

* Wed Mar 25 2009 Douglas E. Warner <silfreed@silfreed.net> - 2.39-2
- adding patch to try to fix parallel make errors

* Thu Mar 19 2009 Douglas E. Warner <silfreed@silfreed.net> - 2.39-1
- updating to 2.39
- fixed potential core dump in C client handling of "K" responses
- Made device hotplugging work again; had been broken by changes in udev
- Introduced major and minor API version symbols into the public interfaces
- The sirfmon utility is gone, replaced by gpsmon which does the same job
  for multiple GPS types
- Fixed a two-year old error in NMEA parsing that nobody noticed because its
  only effect was to trash VDOP values from GSA sentences, and gpsd computes
  those with an internal error model when they look wonky
- cgpxlogger has been merged into gpxlogger
- Speed-setting commands now allow parity and stop-bit setting if the GPS
  chipset and adaptor can support it
- Specfile and other packaging paraphenalia now live in a packaging
  subdirectory
- rtcmdecode becomes gpsdecode and can now de-armor and dump AIDVM packets
- The client library now work correctly in locales where the decimal separator
  is not a period

* Mon Mar 16 2009 Douglas E. Warner <silfreed@silfreed.net> - 2.38-1
- updating to 2.38
- creating init script and sysconfig files
- migrating hotplug rules to udev + hotplug wrapper script from svn r5147
- updating pyexecdir patch
- fixing udev rule subsystem match
- Regression test load for RoyalTek RGM3800 and Blumax GPS-009 added
- Scaling on E error-estimate fields fixed to match O
- Listen on localhost only by default to avoid security problems; this can be
  overridden with the -G command-line option
- The packet-state machine can now recognize RTCM3 packets, though support is
  not yet complete
- Added support for ublox5 and mkt-3301 devices
- Add a wrapper around gpsd_hexdump to save CPU
- Lots of little fixes to various packet parsers
- Always keep the device open: "-n" is not optional any more
- xgpsspeed no longer depends on Motif
- gpsctl can now ship arbitrary payloads to a device;
  It's possible to send binary through the control channel with the
  new "&" command
- Experimental new driver for Novatel SuperStarII
- The 'g' mode switch command now requires, and returns, 'rtcm104v2' rather
  than 'rtcm104'; this is design forward for when RTCM104v2 is fully working

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.37-3
- Rebuild for Python 2.6

* Wed Mar 19 2008 Douglas E. Warner <silfreed@silfreed.net> - 2.37-2
- moving gpspacket.so python lib to main package

* Wed Feb 27 2008 Douglas E. Warner <silfreed@silfreed.net> - 2.37-1
- update to 2.37
- removed install-gpsd_config.h.patch
- installed pkgconfig files in devel package
- added patch to install python modules in sitearch
- removing rpath from inclucded libtool
- moving X11 app-defaults to datadir
- using macros for commands in install; using install instead of cp and mkdir
- cleaning up spaces/tabs for rpmlint

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.34-9
- Autorebuild for GCC 4.3

* Sun Aug 19 2007 Matthew Truch <matt at truch.net> - 2.34-8
- Patch Makefile to also install gpsd_config.h as needed by
  libgpsmm.h.  Redhat BZ 253433.

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-7
- Make sure the logo is actually included (via the spec file).
  I need to wake up before I try even trivial updates.

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-6
- Learn how to use search and replace (aka fix all instances of
  gpsd-logo.png spelled incorrectly as gspd-logo.png).

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-5
- Fix desktop file and logo file name.

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-4
- Include icon for .desktop files per BZ 241428

* Tue Mar 20 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.34-3
- Bump release for FE5 -> Fedora 7 upgrade path.

* Tue Feb 27 2007 Matthew Truch <matt at truch.net> - 2.34-2
- BR python-devel instead of python to make it build.

* Tue Feb 27 2007 Matthew Truch <matt at truch.net> - 2.34-1
- Upgrade to 2.34.
- Get rid of %%makeinstall (which was never needed).
- Possibly fix hotplug issuses (BZ 219750).
- Use %%python_sitelib for python site-files stuff.

* Sat Dec 9 2006 Matthew Truch <matt at truch.net> - 2.33-6
- Rebuild to pull in new version of python.

* Tue Sep 26 2006 Matthew Truch <matt at truch.net> - 2.33-5
- Remove openmotif requirment, and switch to lesstif.

* Mon Aug 28 2006 Matthew Truch <matt at truch.net> - 2.33-4
- Bump release for rebuild in prep. for FC6.

* Thu Jul 20 2006 Matthew Truch <matt at truch.net> - 2.33-3
- Actually, was a missing BR glib-dbus-devel. Ooops.

* Thu Jul 20 2006 Matthew Truch <matt at truch.net> - 2.33-2
- Missing BR glib-devel

* Thu Jul 20 2006 Matthew Truch <matt at truch.net> - 2.33-1
- Update to version 2.33

* Wed Apr 19 2006 Matthew Truch <matt at truch.net> - 2.32-5
- Don't --enable-tnt in build as it causes some gpses to not work
  properly with sattelite view mode.  See bugzilla bug 189220.

* Thu Apr 13 2006 Matthew Truch <matt at truch.net> - 2.32-4
- Add dbus-glib to BuildRequires as needed for build.

* Sun Apr 9 2006 Matthew Truch <matt at truch.net> - 2.32-3
- Include xmlto and python in buildrequires so things build right.
- Don't package static library file.

* Wed Apr 5 2006 Matthew Truch <matt at truch.net> - 2.32-2
- Use ye olde %%{?dist} tag.

* Wed Apr 5 2006 Matthew Truch <matt at truch.net> - 2.32-1
- Initial Fedora Extras specfile
