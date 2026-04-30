Summary:        ACL-specific configuration overlay for WALinuxAgent
Name:           walinuxagent-acl-config
Version:        1.0.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Configuration
URL:            https://github.com/microsoft/azurelinux

Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz
Source1:        waagent.conf
Source2:        waagent.service
Source3:        10-waagent-sysext.conf

BuildRequires:  systemd-rpm-macros
Requires:       WALinuxAgent
BuildArch:      noarch

%description
Overrides the default Azure Linux WALinuxAgent configuration with
ACL-specific settings:
- waagent.conf tuned for Azure Container Linux provisioning
- waagent.service ordered after systemd-sysext.service
- multi-user.target drop-in to pull waagent.service on sysext boot

%prep
# Nothing to prep — config files are shipped as local sources.

%build
# Nothing to build.

%install
install -Dm 644 %{SOURCE1} %{buildroot}%{_datadir}/walinuxagent-acl-config/waagent.conf
install -Dm 644 %{SOURCE2} %{buildroot}%{_datadir}/walinuxagent-acl-config/waagent.service
install -Dm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/systemd/system/multi-user.target.d/10-waagent-sysext.conf

%posttrans
cp %{_datadir}/walinuxagent-acl-config/waagent.conf %{_sysconfdir}/waagent.conf
cp %{_datadir}/walinuxagent-acl-config/waagent.service %{_unitdir}/waagent.service
systemctl daemon-reload 2>/dev/null || :

%files
%{_datadir}/walinuxagent-acl-config/waagent.conf
%{_datadir}/walinuxagent-acl-config/waagent.service
%{_sysconfdir}/systemd/system/multi-user.target.d/10-waagent-sysext.conf

%changelog
* Thu Apr 23 2026 Mayank Singh <mayansingh@microsoft.com> - 1.0.1-1
- Initial package: ACL-specific WALinuxAgent config overlay
- waagent.conf with ACL provisioning defaults
- waagent.service ordered after systemd-sysext.service
- multi-user.target drop-in (Upholds=waagent.service)
- Original version for Azure Linux.
- License verified.
