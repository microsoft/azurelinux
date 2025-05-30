%define _legacy_common_support 1

Name:		   usbip
Summary:	   USB/IP user-space
Version:	   6.6.14.1
Release:	   1%{?dist}
License:	   GPLv2+
Vendor:            Microsoft Corporation
Distribution:   Azure Linux
Group:             System/Kernel
# https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-%%{azl}/%%{version}.tar.gz
# In the interests of keeping the source rpm from being ridiculously large,
# download the Linux kernel from above and run `extract_usbip.sh <version> <azure_linux_version>`
# in the SOURCE directory.
URL:		   https://github.com/microsoft/CBL-Mariner-Linux-Kernel
# The kernel modules require working USB and there's no USB for s390x
# See bug #1483403
ExcludeArch:       s390x
Source:		   %{_distro_sources_url}/usbip-%{version}.tar.xz
Source1:	   usbip-server.service
Source2:	   usbip-client.service
Source99:	   extract_usbip.sh
Patch0:            usbip-5.5-fix-gcc9.patch

BuildRequires:     make
BuildRequires:	   systemd
BuildRequires:	   libudev-devel
BuildRequires:	   libtool autoconf
BuildRequires:	   kernel-devel

Requires:	   kernel
Requires:	   hwdata
Requires(post):	   systemd
Requires(preun):   systemd
Requires(postun):  systemd

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

%description
USB/IP allows you to share USB devices over a network.  With USB/IP, you can
plug a USB device into one computer and use it on a different computer on the
network.

This package contains the user-space tools for USB/IP, both for servers and
clients

%package devel
Summary: USB/IP headers and development libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains headers and static libraries for USB/IP user-space
development

%prep
%autosetup -p1

%build
./autogen.sh
%configure --disable-static --with-usbids-dir=%{_datadir}/hwdata
make %{?_smp_mflags}

%install
%make_install
rm -f %{buildroot}%{_libdir}/libusbip*.la
mkdir -p %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE2} %{buildroot}%{_unitdir}

%post
%systemd_post usbip-client.service usbip-server.service

%preun
%systemd_preun usbip-client.service usbip-server.service

%postun
%systemd_postun_with_restart usbip-client.service usbip-server.service

%files
%license COPYING
%doc README AUTHORS
%{_sbindir}/*
%{_libdir}/*.so.*
%{_mandir}/man8/*
%{_unitdir}/*

%files devel
%license COPYING
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Fri Mar 15 2024 Daniel McIlvaney <damcilva@microsoft.com> - 6.6.14.1-1
- Update version to 6.6.14.1

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.15.34.1-3
- Updating naming for 3.0 version of Azure Linux.

* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.15.34.1-2
- Updating source URL.

* Wed Apr 20 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.34.1-1
- Update version to 5.15.34.1

* Wed Apr 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.15.32.1-1
- Update version to 5.15.32.1

* Thu Feb 24 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.15.18.1-1
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified
- Updated extract_usbip.sh to get sources from Mariner kernel version.
- Added Group and updated URL with CBL-Mariner kernel sources path

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.7.9-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Jonathan Dieter <jdieter@gmail.com> - 5-7.9-1
- Update to 5.7.9 to hopefully fix #1856443

* Mon Feb 03 2020 Jonathan Dieter <jdieter@gmail.com> - 5.5-1
- Update to 5.5
- Work around build failure on GCC 10
- Remove unneeded hardened build flag (since all builds are hardened by default)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Jonathan Dieter <jdieter@gmail.com> - 4.20.12-1
- Update to 4.20.12
- Fix build failure on GCC 9.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 20 2018 Jonathan Dieter <jdieter@gmail.com> - 4.18.9-1
- Update to 4.18.9
- Add patch to fix problem importing device when another device is in
  /sys/devices/platform after vhci (#1631148)
- Fix missing period in patch

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jonathan Dieter <jdieter@gmail.com> - 4.15.10-2
- Remove unneeded ldconfig scriptlets

* Thu Mar 15 2018 Jonathan Dieter <jdieter@gmail.com> - 4.15.10-1
- Attempt another build after supposed failure the last time
- Update to 4.15.10 to fix GCC 8 build failure

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 08 2018 Jonathan Dieter <jdieter@gmail.com> - 4.14.11-2
- Remove obsolete Group tag

* Sat Jan 13 2018 Jonathan Dieter <jdieter@lesbg.com> - 4.14.11-1
- Update usbip to 4.14.11

* Fri Jan 12 2018 Zamir SUN <sztsian@gmail.com> - 4.14.0-1
- Update usbip to 4.14.0 (Fixes bug #1533864)

* Sat Aug 26 2017 Jonathan Dieter <jdieter@lesbg.com> - 4.9.9-6
- Exclude s390x because it doesn't support USB

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Jonathan Dieter <jdieter@lesbg.com> - 4.9.9-3
- Fix 32-bit build failures

* Mon Feb 20 2017 Jonathan Dieter <jdieter@lesbg.com> - 4.9.9-2
- Add patches to fix continuing build failures with GCC 7

* Sun Feb 12 2017 Jonathan Dieter <jdieter@lesbg.com> - 4.9.9-1
- Update to 4.9.9 with build fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Apr 25 2016 Jonathan Dieter <jdieter@lesbg.com> - 4.5-1
- Update to 4.5 with very minor fixes
- Add dependency to kernel-modules-extra (fixes #1329313)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb  5 2015 - Jonathan Dieter <jdieter@lesbg.com> - 3.18-4
- Fix datadir (#1189855)
- Fix client service type

* Thu Jan 15 2015 - Jonathan Dieter <jdieter@lesbg.com> - 3.18-3
- Improve description

* Wed Jan 14 2015 - Jonathan Dieter <jdieter@lesbg.com> - 3.18-2
- Remove clean section
- Remove defattr in files list
- Use license macro for COPYING
- Use combined doc directory
- Combine systemd macros into one
- Remove /etc/default config file
- Stop rmmoding when services stop
- Remove unneeded After=syslog.target in services
- Update to 3.18
- Replace /usr/share with datadir macro in configure
- Switch to make_install macro
- When manually using install, preserve timestamps

* Tue Dec 16 2014 - Jonathan Dieter <jdieter@lesbg.com> - 3.17-1
- Initial release
