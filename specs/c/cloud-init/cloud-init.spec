## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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
%py3_install -- --init-system=systemd

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
* Mon Apr 06 2026 azldev <> - 25.2-11
- Latest state for cloud-init

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
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
