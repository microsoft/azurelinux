Summary:        Wireless daemon for Linux
Name:           iwd
Version:        1.22
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://git.kernel.org/pub/scm/network/wireless/iwd.git/
Source0:        https://www.kernel.org/pub/linux/network/wireless/%{name}-%{version}.tar.xz
BuildRequires:  asciidoc
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  python3-docutils
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(ell) >= 0.27
BuildRequires:  systemd-devel
Requires:       dbus
Requires:       systemd

%description
The daemon and utilities for controlling and configuring the Wi-Fi network
hardware.

%prep
%setup -q


%build
%configure                      \
        --enable-external-ell   \
        --enable-sim-hardcoded  \
        --enable-ofono          \
        --enable-wired          \
        --enable-hwsim          \
        --enable-tools

%make_build V=1


%install
%make_install
mkdir -p %{buildroot}%{_sharedstatedir}/iwd
mkdir -p %{buildroot}%{_sharedstatedir}/ead


%files
%license COPYING
%doc AUTHORS README TODO ChangeLog
%{_bindir}/iwctl
%{_bindir}/iwmon
%{_bindir}/hwsim
%{_libexecdir}/iwd
%{_libexecdir}/ead
%{_modulesloaddir}/pkcs8.conf
%{_unitdir}/ead.service
%{_unitdir}/iwd.service
%{_datadir}/dbus-1/system-services/net.connman.iwd.service
%{_datadir}/dbus-1/system-services/net.connman.ead.service
%{_datadir}/dbus-1/system.d/iwd-dbus.conf
%{_datadir}/dbus-1/system.d/ead-dbus.conf
%{_datadir}/dbus-1/system.d/hwsim-dbus.conf
%{_mandir}/man1/iwmon.1*
%{_sharedstatedir}/iwd
%{_sharedstatedir}/ead
%{_mandir}/man*/*

# Don't let iwd adjust interface naming. It would break user configurations.
%exclude /usr/lib/systemd/network/80-iwd.link


%changelog
* Tue Sep 19 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.22-2
- Fix build issue for systemd/systemd-bootstrap confusion

* Thu Dec 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.22-1
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Jun 15 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8-1
- Update to 1.8 release

* Wed Mar 25 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6-1
- Update to 1.6 release

* Sun Feb  9 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.5-1
- Update to 1.5 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4-1
- Update to 1.4 release

* Sat Dec 14 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-1
- Update to 1.3 release

* Fri Nov 15 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-1
- Update to 1.1 release

* Wed Oct 30 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.0-1
- Update to 1.0 release

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 0.23-1
- Update to 0.23 release

* Fri Oct 11 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.22-1
- Update to 0.22 release

* Fri Sep 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.21-1
- Update to 0.21 release

* Fri Sep 06 2019 Lubomir Rintel <lkundrak@v3.sk> - 0.20-2
- Create /var/lib/iwd and /var/lib/ead
- Bump the ell requirement

* Thu Aug 29 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.20-1
- Update to 0.20 release

* Mon Aug 05 2019 Lubomir Rintel <lkundrak@v3.sk> - 0.19-1
- Update to 0.19 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 12 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.18-1
- Update to 0.18 release

* Mon Apr 15 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.17-1
- Update to 0.17 release

* Thu Apr  4 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.16-1
- Update to 0.16 release

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.14-3
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.14-1
- Update to 0.14 release

* Wed Dec 12 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.13-1
- Update to 0.13 release

* Fri Nov 16 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.12-1
- Update to 0.12 release

* Sat Nov 10 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.11-1
- Update to 0.11 release

* Mon Sep 24 2018 Lubomir Rintel <lkundrak@v3.sk> - 0.8-1
- Update to 0.8 release

* Sat Aug 11 2018 Lubomir Rintel <lkundrak@v3.sk> - 0.6-1
- Update to 0.6 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Lubomir Rintel <lkundrak@v3.sk> - 0.3-1
- Update to 0.3 release

* Mon May 14 2018 Lubomir Rintel <lkundrak@v3.sk> - 0.2-1
- Update to 0.2 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-0.3.20171026git569be48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 29 2017 Lubomir Rintel <lkundrak@v3.sk> - 0.0-0.2.20171026git569be48
- Update to a later snapshot

* Sun Oct 22 2017 Lubomir Rintel <lkundrak@v3.sk> - 0.0-0.2.20171022git2c56501
- Added BR gcc
- Made build verbose
- Fixed license tag
- Addressed review issues (Robert-André Mauchin, #1505238):
- Dropped Group tag
- Added license and documentation texts

* Sun Oct 22 2017 Lubomir Rintel <lkundrak@v3.sk> - 0.0-0.1.20171022git2c56501
- Initial packaging
