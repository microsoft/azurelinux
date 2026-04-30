## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 11;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel}
%bcond_with tests
%else
%bcond_without tests
%endif

Name:           cloud-init
Version:        25.2
Release:        %autorelease
Summary:        Cloud instance init scripts
License:        Apache-2.0 OR GPL-3.0-only
URL:            https://github.com/canonical/cloud-init

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        cloud-init-tmpfiles.conf

# https://github.com/canonical/cloud-init/pull/6448
# Removes auditd.service dependency to prevent systemd ordering issues
Patch:          6448.patch
# https://github.com/canonical/cloud-init/pull/6423
# Fixes systemd dependency cycle on Fedora by adding DefaultDependencies=no
# and including Fedora in distribution-specific conditional blocks
Patch:          0001-fix-avoid-dependency-cycle-on-Fedora.patch
# https://github.com/canonical/cloud-init/pull/6339
# Switches socket protocol from DGRAM to STREAM and removes ncat's -s flag
# for proper systemd service coordination
Patch:          6339.patch

BuildArch:      noarch

BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(systemd)

%if %{with tests}
BuildRequires:  iproute
BuildRequires:  passwd
BuildRequires:  procps-ng
# dnf is needed to make cc_ntp unit tests work
# https://bugs.launchpad.net/cloud-init/+bug/1721573
BuildRequires:  /usr/bin/dnf
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(responses)
BuildRequires:  python3dist(passlib)
BuildRequires:  python3dist(pyserial)
%endif

Requires:       dhcpcd

Requires:       hostname
Requires:       e2fsprogs
Requires:       iproute
Requires:       python3-libselinux
Requires:       policycoreutils-python3
Requires:       procps
Requires:       shadow-utils
Requires:       util-linux
Requires:       xfsprogs
Requires:       openssl
Requires:       /usr/bin/nc

%{?systemd_requires}


Patch: fix-avoid-incorrect-CPE-parsing-on-Azure-Linux.patch
%description
Cloud-init is a set of init scripts for cloud instances.  Cloud instances
need special scripts to run during initialization to retrieve and install
ssh keys and to let the user run various scripts.


%prep
%autosetup -p1

# Change shebangs
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/env python3|' \
       -e 's|#!/usr/bin/python|#!/usr/bin/python3|' tools/* cloudinit/ssh_util.py

# Removing shebang manually because of rpmlint, will update upstream later
sed -i -e 's|#!/usr/bin/python||' cloudinit/cmd/main.py

# Use unittest from the standard library. unittest2 is old and being
# retired in Fedora. See https://bugzilla.redhat.com/show_bug.cgi?id=1794222
find tests/ -type f | xargs sed -i s/unittest2/unittest/
find tests/ -type f | xargs sed -i s/assertItemsEqual/assertCountEqual/


%generate_buildrequires
%pyproject_buildrequires


%build
%py3_build


%install
%py3_install -- --init-system=systemd --distro=fedora

# Generate cloud-config file
python3 tools/render-template --variant %{?rhel:rhel}%{!?rhel:fedora} > $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg

mkdir -p $RPM_BUILD_ROOT/var/lib/cloud

# /run/cloud-init needs a tmpfiles.d entry
mkdir -p $RPM_BUILD_ROOT/run/cloud-init
mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/%{_tmpfilesdir}/%{name}.conf

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d
cp -p tools/21-cloudinit.conf $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d/21-cloudinit.conf

# installing man pages
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
for man in cloud-id.1 cloud-init.1 cloud-init-per.1; do
    install -c -m 0644 doc/man/${man} ${RPM_BUILD_ROOT}%{_mandir}/man1/${man}
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
done


%check
%if %{with tests}
python3 -m pytest tests/unittests
%else
%py3_check_import cloudinit
%endif

%post
%systemd_post cloud-config.service cloud-config.target cloud-final.service cloud-init-main.service cloud-init.target cloud-init-local.service cloud-init-network.service


%preun
%systemd_preun cloud-config.service cloud-config.target cloud-final.service cloud-init-main.service cloud-init.target cloud-init-local.service cloud-init-network.service


%postun
%systemd_postun cloud-config.service cloud-config.target cloud-final.service cloud-init-main.service cloud-init.target cloud-init-local.service cloud-init-network.service

# In the F42->F43 upgrade, cloud-init.service is moved to cloud-init-main.service; we need to do a onetime
# cleanup and preset the new service.
%posttrans
if [ -L /etc/systemd/system/cloud-init.target.wants/cloud-init.service ]; then
    systemctl preset cloud-init-main.service
    rm -f /etc/systemd/system/cloud-init.target.wants/cloud-init.service
fi


%files
%license LICENSE LICENSE-Apache2.0 LICENSE-GPLv3
%doc ChangeLog
%doc doc/*
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg
%dir               %{_sysconfdir}/cloud/cloud.cfg.d
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/*.cfg
%doc               %{_sysconfdir}/cloud/cloud.cfg.d/README
%dir               %{_sysconfdir}/cloud/templates
%config(noreplace) %{_sysconfdir}/cloud/templates/*
%dir               %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/rsyslog.d/21-cloudinit.conf
%{_udevrulesdir}/66-azure-ephemeral.rules
%{_unitdir}/cloud-config.service
%{_unitdir}/cloud-final.service
%{_unitdir}/cloud-init-main.service
%{_unitdir}/cloud-init-local.service
%{_unitdir}/cloud-init-network.service
%{_unitdir}/cloud-config.target
%{_unitdir}/cloud-init.target
/usr/lib/systemd/system-generators/cloud-init-generator
%{_unitdir}/cloud-init-hotplugd.service
%{_unitdir}/cloud-init-hotplugd.socket
%{_unitdir}/sshd-keygen@.service.d/disable-sshd-keygen-if-cloud-init-active.conf
%{_tmpfilesdir}/%{name}.conf
%{python3_sitelib}/*
%{_libexecdir}/%{name}
%{_bindir}/cloud-init*
%{_bindir}/cloud-id
%dir /run/cloud-init
%dir /var/lib/cloud
%{_datadir}/bash-completion/completions/cloud-init


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 25.2-11
- test: add initial lock files

* Mon Dec 15 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 25.2-10
- Clean up old cloud-init.service and preset cloud-init-main.service

* Mon Dec 15 2025 Major Hayden <major@redhat.com> - 25.2-9
- Add dependency on nc

* Mon Dec 15 2025 Major Hayden <major@redhat.com> - 25.2-8
- Remove netcat dependency

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 25.2-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Thu Sep 11 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 25.2-6
- Backport revert auditd.service dependency

* Wed Aug 27 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 25.2-5
- Adjust the dependency cycle patch to drop After=dbus.socket

* Mon Aug 25 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 25.2-4
- Break dependency cycle with auditd (rhbz 2390898)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 25.2-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 13 2025 Vitaly Kuznetsov <vkuznets@redhat.com> - 25.2-2
- Get rid of 'sgdisk' dependency

* Wed Aug 13 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 25.2-1
- Update to 25.2

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 25.1.4-1
- Update to v25.1.4
- fix: disable cloud-init when non-x86 environments have no DMI-data and no
  strict datasources detected (LP: #2069607) (CVE-2024-6174)

* Fri Jul 11 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 25.1.3-1
- Update to upstream release 25.1.3

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 25.1-2
- Rebuilt for Python 3.14

* Sat Mar 08 2025 František Zatloukal <fzatlouk@redhat.com> - 25.1-1
- Update to 25.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 13 2024 Adam Williamson <awilliam@redhat.com> - 24.2-3
- Fix btrfs version check with btrfs-progs 6.10

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Major Hayden <major@redhat.com> - 24.2-1
- Update to 24.2

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 24.1.7-2
- Rebuilt for Python 3.13

* Wed Jun 05 2024 Major Hayden <major@redhat.com> - 24.1.7-1
- Update to 24.1.7

* Wed May 29 2024 Major Hayden <major@redhat.com> - 24.1.6-1
- Update to 24.1.6; remove net-tools dep

* Wed Apr 17 2024 Major Hayden <major@redhat.com> - 24.1.4-2
- Switch to dhcpcd

* Wed Apr 17 2024 Major Hayden <major@redhat.com> - 24.1.4-1
- Update to 24.1.4

* Tue Feb 27 2024 Major Hayden <major@redhat.com> - 23.4.4-1
- Update to 23.4.4

* Thu Feb 01 2024 Major Hayden <major@redhat.com> - 23.4.1-6
- Update packit config

* Thu Feb 01 2024 Major Hayden <major@redhat.com> - 23.4.1-5
- Switch back to dhcp-client temporarily

* Tue Jan 30 2024 Major Hayden <major@redhat.com> - 23.4.1-4
- Replace dhcp-client with udhcpc

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 František Zatloukal <fzatlouk@redhat.com> - 23.4.1-1
- Update to 23.4.1

* Fri Aug 11 2023 Miroslav Suchý <msuchy@redhat.com> - 23.2.1-2
- correct SPDX formula

* Thu Jul 20 2023 Major Hayden <major@redhat.com> - 23.2.1-1
- Update to 23.2.1

* Thu Jul 20 2023 Major Hayden <major@redhat.com> - 23.2-4
- Add packit config

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 23.2-2
- Rebuilt for Python 3.12

* Thu Jun 22 2023 Major Hayden <major@redhat.com> - 23.2-1
- Update to 23.2 rhbz#2196523

* Wed May 17 2023 Major Hayden <major@redhat.com> - 23.1.2-10
- Migrate to pyproject-rpm-macros for build requirements

* Tue May 16 2023 Major Hayden <major@redhat.com> - 23.1.2-9
- ec2: Do not enable DHCPv6 on EC2

* Tue May 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 23.1.2-8
- Disable tests by default in RHEL builds

* Thu May 11 2023 Major Hayden <major@redhat.com> - 23.1.2-7
- Update changelog for rhbz#2068529

* Thu May 11 2023 Major Hayden <major@redhat.com> - 23.1.2-6
- Allow > 3 nameservers to be used rhbz#2068529

* Sun Apr 30 2023 Neal Gompa <ngompa@fedoraproject.org> - 23.1.2-5
- Use the correct SourceURL format for the upstream sources
- Switch to SPDX identifiers for the license field

* Fri Apr 28 2023 Major Hayden <major@redhat.com> - 23.1.2-4
- Switch to GitHub for upstream source

* Fri Apr 28 2023 Major Hayden <major@redhat.com> - 23.1.2-3
- Revert "Use forge source"

* Fri Apr 28 2023 Major Hayden <major@redhat.com> - 23.1.2-2
- Use forge source

* Thu Apr 27 2023 Major Hayden <major@redhat.com> - 23.1.2-1
- Update to 23.1.2

* Thu Mar 23 2023 František Zatloukal <fzatlouk@redhat.com> - 23.1.1-1
- Rebase to 23.1.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 22.2-3
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.2-2
- Add dhcp-client dependency for Azure and OCI network bootstrap

* Thu May 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.2-1
- Rebase to 22.2

* Thu Mar 10 2022 Dusty Mabe <dusty@dustymabe.com> - 22.1-3
- Don't require NetworkManager-config-server

* Tue Feb 22 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.1-2
- Drop extra tests search in prep

* Tue Feb 22 2022 Neal Gompa <ngompa@fedoraproject.org> - 22.1-1
- Rebase to 22.1
- Backport cloud-init PR to add proper NetworkManager support
- Add patch to prefer NetworkManager

* Wed Feb 16 2022 Charalampos Stratakis <cstratak@redhat.com> - 21.3-6
- Remove redundant dependencies on nose and mock

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Neal Gompa <ngompa@fedoraproject.org> - 21.3-4
- Add gdisk and openssl deps to fix UEFI / Azure initialization
  [bz#1974262]

* Wed Dec 15 2021 Neal Gompa <ngompa@fedoraproject.org> - 21.3-3
- Backport fix for tests running with new pyyaml

* Wed Sep 08 2021 Eduardo Otubo <otubo@redhat.com> - 21.3-2
- Adding man pages to spec file

* Thu Sep 02 2021 Eduardo Otubo <otubo@redhat.com> - 21.3-1
- Update to 20.4

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 František Zatloukal <fzatlouk@redhat.com> - 20.4-7
- Fixup collections import on Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 20.4-6
- Rebuilt for Python 3.10

* Mon Feb 08 2021 Eduardo Otubo <otubo@redhat.com> - 20.4-5
- Revert "ssh_util: handle non-default AuthorizedKeysFile config (#586)"
  (#775)

* Thu Feb 04 2021 Eduardo Otubo <otubo@redhat.com> - 20.4-4
- Adding 'Requires: hostname'

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Eduardo Otubo <otubo@redhat.com> - 20.4-2
- Adding RHEL default cloud.cfg

* Thu Dec 10 2020 Eduardo Otubo <otubo@redhat.com> - 20.4-1
- Rebase to 20.4

* Mon Sep 07 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-9
- Scaleway: Fix DatasourceScaleway to avoid backtrace (#128)

* Mon Sep 07 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-8
- Patch references missing on spec file

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <miro@hroncok.cz> - 19.4-6
- Rebuilt for Python 3.9

* Tue Apr 14 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-5
- Backport for CVE-2020-8631 and CVE-2020-8632

* Sun Feb 23 2020 Dusty Mabe <dusty@dustymabe.com> - 19.4-4
- Add missing files to package

* Sun Feb 23 2020 Dusty Mabe <dusty@dustymabe.com> - 19.4-3
- Fix failing unittests by including `BuildRequires: passwd`

* Sun Feb 23 2020 Dusty Mabe <dusty@dustymabe.com> - 19.4-2
- Fix sed substitutions for unittest2 and assertItemsEqual

* Fri Feb 21 2020 Eduardo Otubo <otubo@redhat.com> - 19.4-1
- Update to 19.4

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Miro Hrončok <miro@hroncok.cz> - 17.1-16
- Drop unneeded build dependency on python3-unittest2

* Thu Oct 03 2019 Miro Hrončok <miro@hroncok.cz> - 17.1-15
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <miro@hroncok.cz> - 17.1-14
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Björn Esser <besser82@fedoraproject.org> - 17.1-12
- Add (Build)Requires: python3-distro

* Tue Apr 23 2019 Björn Esser <besser82@fedoraproject.org> - 17.1-11
- Add patch to replace platform.dist() [RH:1695953]

* Tue Apr 23 2019 Björn Esser <besser82@fedoraproject.org> - 17.1-10
- Add patch to fix failing test for EPOCHREALTIME bash env [RH:1695953]

* Tue Apr 23 2019 Björn Esser <besser82@fedoraproject.org> - 17.1-9
- Fix %%%%systemd_postun macro [RH:1695953]

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <miro@hroncok.cz> - 17.1-6
- Rebuilt for Python 3.7

* Mon Apr 23 2018 Lars Kellogg-Stedman <lars@redhat.com> - 17.1-5
- Enable dhcp on ec2 interfaces with only local ipv4 addresses [RH:1569321]

* Mon Mar 26 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 17.1-4
- Make sure the patch does not add infinitely many entries

* Mon Mar 26 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 17.1-3
- Add patch to retain old values of /etc/sysconfig/network

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 06 2017 Garrett Holmstrom <gholms@devzero.com> - 17.1-1
- Update to 17.1

* Fri Sep 15 2017 Dusty Mabe <dusty@dustymabe.com> - 0.7.9-29
- add in hook-dhclient script to enable azure

* Fri Sep 15 2017 Dusty Mabe <dusty@dustymabe.com> - 0.7.9-28
- Add in upstream patch to fix call to xfs_growfs

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-26
- Fix broken sysconfig file writing on DigitalOcean

* Wed Jun 21 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-25
- Fix broken fs_setup cmd option handling

* Wed Jun 21 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-24
- Resolve a conflict between cloud-init and NetworkManager writing
  resolv.conf

* Wed Jun 21 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-23
- Fix NameError in package module

* Mon Apr 17 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-22
- Use %%py3_build, %%py3_install macros

* Mon Apr 17 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-21
- Use if index to assign DigitalOcean IPv4 LL addrs

* Mon Apr 17 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-20
- Configure all NICs presented in DigitalOcean metadata

* Mon Apr 17 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-19
- Make DigitalOcean data sources handle DNS servers similar to OpenStack

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-18
- Merge branch 'f25'

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-17
- Remove cruft

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-16
- Merge branch 'f25'

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-15
- Order cloud-init.service after network.service and NetworkManager.service

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-14
- Fix IPv6 gateways in network sysconfig

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-13
- Make > 3 name servers a warning, not a fatal error

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-12
- Fix errors in network sysconfig handling

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-11
- Fix systemd dependency cycle with cloud-init and multi-user.target

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-10
- Fix systemd dependency cycle with cloud-final and os-collect-config

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-8
- Fix calls to hostnamectl occuring before dbus is up

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-7
- Remove old cruft

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-6
- Normalize patch file names

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-5
- Remove disable-failing-tests.patch

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.9-4
- Merge branch 'f25'

* Fri Jan 20 2017 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.9-3
- limit tests in %%check to unittests

* Fri Jan 20 2017 Colin Walters <walters@verbum.org> - 0.7.9-2
- Update sources for previous commit

* Fri Jan 20 2017 Colin Walters <walters@verbum.org> - 0.7.9-1
- Update to 0.7.9

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.7.8-8
- Rebuild for Python 3.6

* Tue Oct 25 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-7
- Enable the DigitalOcean metadata provider by default

* Fri Oct 14 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-6
- Do not write NM_CONTROLLED=no in generated interface config files

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-5
- Add xfsprogs dependency

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-4
- Backport DigitalOcean network config support

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-3
- Order cloud-init-local before NetworkManager

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-2
- Drop run-parts dependency

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-1
- Update to 0.7.8

* Tue Aug 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.7-1
- Update to 0.7.7

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-23
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Thu Jul 07 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-22
- Update to bzr snapshot 1245

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 0.7.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.6-20
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Aug 16 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-19
- Update to bzr snapshot 1137

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 0.7.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-17
- Drop dmidecode depencency, switch back to noarch

* Mon Feb 23 2015 Miro Hrončok <miro@hroncok.cz> - 0.7.6-16
- Require iproute for tests

* Mon Feb 23 2015 Miro Hrončok <miro@hroncok.cz> - 0.7.6-15
- Change shebangs

* Mon Feb 23 2015 Miro Hrončok <miro@hroncok.cz> - 0.7.6-14
- Switch to python 3 and add a %%check section

* Mon Feb 23 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-13
- Update to bzr snapshot 1060 for python 3 support

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-12
- Switch to dnf instead of yum when available

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-11
- Stop enabling services in %%post

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-10
- Ensure cloud-init.service doesn't write all over the login prompt

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-9
- Change network.target systemd deps to network-online.target

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-8
- Fix handling of user group lists that contain spaces

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-7
- Add recognition of 3 ecdsa-sha2-nistp* ssh key types

* Thu Feb 19 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-6
- Stop implicitly listing doc files twice

* Thu Feb 19 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-5
- Stop depending on git to build

* Thu Feb 19 2015 Colin Walters <walters@verbum.org> - 0.7.6-4
- Update changelog to match current release

* Sun Nov 16 2014 Colin Walters <walters@verbum.org> - 0.7.6-3
- Add missed patch, remove unused patches

* Sat Nov 15 2014 Colin Walters <walters@verbum.org> - 0.7.6-2
- Update sources

* Fri Nov 14 2014 Colin Walters <walters@verbum.org> - 0.7.6-1
- New upstream version [RH:974327]
- Drop python-cheetah dependency (same as above bug)

* Fri Nov 07 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-13
- Drop rsyslog dependency

* Fri Nov 07 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-12
- Drop python-boto dependency

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Dennis Gilmore <dennis@ausil.us> - 0.7.5-10
- fix typo in settings.py preventing metadata being fecthed in ec2

* Mon Jun 09 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-9
- Stop calling ``udevadm settle'' with --quiet since systemd 213 removed it

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 0.7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-7
- Merge branch 'f20'

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-6
- Make dmidecode dependency arch-dependent

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-5
- Mention which bug asked us to require jsonpatch

* Fri May 30 2014 Matthew Miller <mattdm@mattdm.org> - 0.7.5-4
- add missing python-jsonpatch dependency

* Tue Apr 29 2014 Sam Kottler <shk@linux.com> - 0.7.5-3
- Add missing day of the week in the changelog

* Tue Apr 29 2014 Sam Kottler <shk@linux.com> - 0.7.5-2
- Remove old patches for the 0.7.2 series

* Tue Apr 29 2014 Sam Kottler <shk@linux.com> - 0.7.5-1
- Update to 0.7.5 and rename associate patches

* Sat Jan 25 2014 Sam Kottler <shk@redhat.com> - 0.7.2-16
- Remove patch to the Puppet service unit nane [RH:1057860]

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-15
- Actually bump the release number  :)

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-14
- Drop xfsprogs dependency

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-13
- Add yum-add-repo module

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-12
- Merge branch 'f19'

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-11
- Add missing modules

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-10
- Fix rsyslog log filtering

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-9
- Fix restorecon failure when selinux is disabled

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-8
- Let systemd handle console output

* Wed Sep 25 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-7
- Fix puppet agent service name

* Fri Sep 13 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.2-6
- Drop obsolete patches

* Sat Aug 03 2013 Dennis Gilmore <dennis@ausil.us> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Matthew Miller <mattdm@mattdm.org> - 0.7.2-4
- switch ec2-user to "fedora" --  see bugzilla #971439.

* Fri May 17 2013 Steven Hardy <shardy@redhat.com> - 0.7.2-3
- update to release 0.7.2

* Thu May 02 2013 Steven Hardy <shardy@redhat.com> - 0.7.2-2
- add dependency on python-requests

* Thu May 02 2013 Steven Hardy <shardy@redhat.com> - 0.7.2-1
- update to upstream revision 809 to fix various issues

* Sun Apr 07 2013 Orion Poplawski <orion@cora.nwra.com> - 0.7.1-7
- Don't ship tests

* Wed Feb 13 2013 Dennis Gilmore <dennis@ausil.us> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.1-5
- Fix default_user syntax

* Thu Dec 13 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.1-4
- Add default_user to cloud.cfg (this is required for ssh keys to work)

* Wed Nov 21 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.1-3
- Fix "resize_root: noblock"

* Wed Nov 21 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.1-2
- Fix broken sudoers file generation

* Wed Nov 21 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.1-1
- Rebase against version 0.7.1

* Wed Oct 10 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-10
- Fix / filesystem resizing

* Wed Oct 10 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-9
- Rebase against version 0.7.0

* Sun Sep 23 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-8
- Add dmidecode dependency for DataSourceAltCloud

* Sun Sep 23 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-7
- Fix sudoers file permissions

* Sun Sep 23 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-6
- Fix ssh key printing

* Sun Sep 23 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-5
- Fix hostname persistence

* Sun Sep 23 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-4
- Rebase against upstream rev 659

* Tue Sep 18 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-3
- Update Fedora README

* Tue Sep 18 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-2
- Upload cloud-init-0.7.0-bzr650.tar.gz this time :)

* Tue Sep 18 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.7.0-1
- Rebase against upstream rev 650

* Mon Sep 17 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-11
- Clean up .gitignore

* Fri Sep 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-10
- Bump n-v-r

* Fri Sep 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-9
- Send output to the console

* Fri Sep 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-8
- Shut off systemd timeouts

* Fri Sep 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-7
- Use a FQDN for instance data URL fallback

* Fri Sep 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-6
- Add missing patch commentary

* Wed Jul 18 2012 Dennis Gilmore <dennis@ausil.us> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Pádraig Brady <P@draigBrady.com> - 0.6.3-4
- Add support for installing yum packages

* Sat Mar 31 2012 Andy Grimm <agrimm@gmail.com> - 0.6.3-3
- Fixed incorrect interpretation of relative path for AuthorizedKeysFile
  (BZ #735521)

* Mon Mar 05 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-2
- Fix runparts() compabitility with Fedora

* Mon Mar 05 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.3-1
- Rebase against upstream rev 532

* Thu Jan 12 2012 Dennis Gilmore <dennis@ausil.us> - 0.6.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 05 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-26
- Disable SSH key-deleting on startup

* Tue Oct 04 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-25
- Refresh patches

* Tue Oct 04 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-24
- Deal with differences from Ubuntu's sshd

* Thu Sep 29 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-23
- Update sshkeytypes patch

* Wed Sep 28 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-22
- Fix cloud-init.service dependencies

* Wed Sep 28 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-21
- Consolidate selinux file context patches

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-20
- Fix the release tag's latest bump

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-19
- Minor spec file cleanup

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-18
- Add missing dependencies

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-17
- Rebase against upstream rev 457

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-16
- Add more macros to the spec file

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-15
- Note that the botobundle patch was submitted upstream

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-14
- Fix failures due to empty script dirs [LP:857926]

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-13
- Disable the grub_dpkg module

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-12
- Update localefile patch

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-11
- Fix a bad method call in FQDN-guessing [LP:857891]

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-10
- Fix SSH key generation

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-9
- Fix logfile permission checking

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-8
- Minor spec file fixes

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-7
- Updated tzsysconfig patch

* Sat Sep 24 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.6.2-6
- Initial build (0.6.2-0.1.bzr450)

* Sat Jun 15 2013 Matthew Miller <mattdm@mattdm.org> - 0.7.2-5
- switch ec2-user to "fedora" --  see bugzilla #971439.

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.2-4
- BuildRequire python-setuptools, not python-setuptools-devel

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.2-3
- Use the %%license rpm macro

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.2-2
- Add tmpfiles.d configuration for /run/cloud-init

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.2-1
- Write /etc/locale.conf instead of /etc/sysconfig/i18n

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-24
- Update changelog for systemd loop fix

* Fri Jan 27 2017 Dusty Mabe <dusty@dustymabe.com> - 0.7.8-23
- fix systemd unit dependency cycle

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-22
- Disable unit tests broken by httpretty update

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-21
- Re-apply rsyslog configuration fixes

* Fri Jan 27 2017 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.8-20
- limit tests in %%check to unittests

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-19
- Do not cache IAM instance profile credentials on disk

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-18
- Order cloud-init.service after network.service and NetworkManager.service

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-17
- Re-enable all tests

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-16
- Bump Release

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-15
- Do not cache IAM instance profile credentials on disk

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-14
- Order cloud-init.service after network.service and NetworkManager.service

* Tue Mar 14 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-13
- Re-enable all tests

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-12
- Update changelog for systemd loop fix

* Fri Jan 27 2017 Dusty Mabe <dusty@dustymabe.com> - 0.7.8-11
- fix systemd unit dependency cycle

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-10
- Disable unit tests broken by httpretty update

* Fri Jan 27 2017 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-9
- Re-apply rsyslog configuration fixes

* Fri Jan 27 2017 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.8-8
- limit tests in %%check to unittests

* Tue Oct 25 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-7
- Enable the DigitalOcean metadata provider by default

* Fri Oct 14 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-6
- Do not write NM_CONTROLLED=no in generated interface config files

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-5
- Add xfsprogs dependency

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-4
- Backport DigitalOcean network config support

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-3
- Order cloud-init-local before NetworkManager

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-2
- Drop run-parts dependency

* Fri Sep 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.8-1
- Update to 0.7.8

* Tue Aug 30 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.7-1
- Update to 0.7.7

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-23
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Thu Jul 07 2016 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-22
- Update to bzr snapshot 1245

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 0.7.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.6-20
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Aug 16 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-19
- Update to bzr snapshot 1137

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 0.7.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-17
- Drop dmidecode depencency, switch back to noarch

* Mon Feb 23 2015 Miro Hrončok <miro@hroncok.cz> - 0.7.6-16
- Require iproute for tests

* Mon Feb 23 2015 Miro Hrončok <miro@hroncok.cz> - 0.7.6-15
- Change shebangs

* Mon Feb 23 2015 Miro Hrončok <miro@hroncok.cz> - 0.7.6-14
- Switch to python 3 and add a %%check section

* Mon Feb 23 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-13
- Update to bzr snapshot 1060 for python 3 support

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-12
- Switch to dnf instead of yum when available

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-11
- Stop enabling services in %%post

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-10
- Ensure cloud-init.service doesn't write all over the login prompt

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-9
- Change network.target systemd deps to network-online.target

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-8
- Fix handling of user group lists that contain spaces

* Fri Feb 20 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-7
- Add recognition of 3 ecdsa-sha2-nistp* ssh key types

* Thu Feb 19 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-6
- Stop implicitly listing doc files twice

* Thu Feb 19 2015 Garrett Holmstrom <gholms@devzero.com> - 0.7.6-5
- Stop depending on git to build

* Thu Feb 19 2015 Colin Walters <walters@verbum.org> - 0.7.6-4
- Update changelog to match current release

* Sun Nov 16 2014 Colin Walters <walters@verbum.org> - 0.7.6-3
- Add missed patch, remove unused patches

* Sat Nov 15 2014 Colin Walters <walters@verbum.org> - 0.7.6-2
- Update sources

* Fri Nov 14 2014 Colin Walters <walters@verbum.org> - 0.7.6-1
- New upstream version [RH:974327]
- Drop python-cheetah dependency (same as above bug)

* Fri Nov 07 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-13
- Drop rsyslog dependency

* Fri Nov 07 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-12
- Drop python-boto dependency

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Dennis Gilmore <dennis@ausil.us> - 0.7.5-10
- fix typo in settings.py preventing metadata being fecthed in ec2

* Mon Jun 09 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-9
- Stop calling ``udevadm settle'' with --quiet since systemd 213 removed it

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 0.7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Garrett Holmstrom <gholms@devzero.com> - 0.7.5-7
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
