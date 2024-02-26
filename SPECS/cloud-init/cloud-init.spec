%if 0%{?rhel}
%bcond_with tests
%else
%bcond_without tests
%endif

Name:           cloud-init
Version:        23.4.4
Release:        1%{?dist}
Summary:        Cloud instance init scripts
License:        Apache-2.0 OR GPL-3.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/canonical/cloud-init

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        10-azure-kvp.cfg
Patch:          0001-Add-new-distro-azurelinux-for-Microsoft-Azure-Linux.patch

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
%endif

# ISC DHCP is no longer maintained and cloud-init will ship a 
# release with dhcpcd support soon. See BZ 2247055 for details.
#
# Cloud-init dhcpcd support is pending a release here:
# https://github.com/canonical/cloud-init/pull/4746/files
Requires:       dhcp-client

Requires:       hostname
Requires:       e2fsprogs
Requires:       iproute
Requires:       python3-libselinux
Requires:       net-tools
Requires:       policycoreutils-python3
Requires:       procps
Requires:       shadow-utils
Requires:       util-linux
Requires:       xfsprogs
# https://bugzilla.redhat.com/show_bug.cgi?id=1974262
Requires:       gdisk
Requires:       openssl

%{?systemd_requires}


%description
Cloud-init is a set of init scripts for cloud instances.  Cloud instances
need special scripts to run during initialization to retrieve and install
ssh keys and to let the user run various scripts.


%package azure-kvp
Summary:        Cloud-init configuration for Hyper-V telemetry
Requires:       %{name} = %{version}-%{release}


%description    azure-kvp
Cloud-init configuration for Hyper-V telemetry


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
python3 tools/render-template --variant azurelinux > $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg

mkdir -p $RPM_BUILD_ROOT/%{_sharedstatedir}/cloud
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg.d

install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg.d

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d
cp -p tools/21-cloudinit.conf $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d/21-cloudinit.conf

# installing man pages
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
for man in cloud-id.1 cloud-init.1 cloud-init-per.1; do
    install -c -m 0644 doc/man/${man} ${RPM_BUILD_ROOT}%{_mandir}/man1/${man}
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
done

# Put files in /etc/systemd/system in the right place
cp -a %{buildroot}/etc/systemd %{buildroot}/usr/lib
rm -rf %{buildroot}/etc/systemd


%check
%if %{with tests}
python3 -m pytest tests/unittests
%else
%py3_check_import cloudinit
%endif

%post
%systemd_post cloud-config.service cloud-config.target cloud-final.service cloud-init.service cloud-init.target cloud-init-local.service


%preun
%systemd_preun cloud-config.service cloud-config.target cloud-final.service cloud-init.service cloud-init.target cloud-init-local.service


%postun
%systemd_postun cloud-config.service cloud-config.target cloud-final.service cloud-init.service cloud-init.target cloud-init-local.service


%files
%license LICENSE LICENSE-Apache2.0 LICENSE-GPLv3
%doc ChangeLog
%doc doc/*
%doc %{_sysconfdir}/cloud/clean.d/README
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg
%dir               %{_sysconfdir}/cloud/cloud.cfg.d
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/*.cfg
%doc               %{_sysconfdir}/cloud/cloud.cfg.d/README
%dir               %{_sysconfdir}/cloud/templates
%config(noreplace) %{_sysconfdir}/cloud/templates/*
%config(noreplace) %{_sysconfdir}/rsyslog.d/21-cloudinit.conf
%{_udevrulesdir}/66-azure-ephemeral.rules
%{_unitdir}/cloud-config.service
%{_unitdir}/cloud-final.service
%{_unitdir}/cloud-init.service
%{_unitdir}/cloud-init-local.service
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


%files azure-kvp
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/10-azure-kvp.cfg


%changelog
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
