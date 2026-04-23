Summary:        ACL-specific configuration overlay for WALinuxAgent
Name:           walinuxagent-acl-config
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Configuration
URL:            https://github.com/microsoft/azurelinux

Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz

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
%setup -q -c

%build
# Nothing to build.

%install
# Stage waagent.conf -> copied to /etc by %%posttrans to avoid file
# conflict with the base WALinuxAgent package.
install -Dm 644 waagent.conf %{buildroot}%{_datadir}/walinuxagent-acl-config/waagent.conf

# Install service and drop-in to /etc/systemd/system so they take
# precedence over WALinuxAgent's /usr/lib/systemd/system copies.
install -Dm 644 waagent.service %{buildroot}%{_sysconfdir}/systemd/system/waagent.service
install -Dm 644 10-waagent-sysext.conf %{buildroot}%{_sysconfdir}/systemd/system/multi-user.target.d/10-waagent-sysext.conf

%posttrans
cp %{_datadir}/walinuxagent-acl-config/waagent.conf %{_sysconfdir}/waagent.conf
systemctl daemon-reload 2>/dev/null || :

%files
%{_datadir}/walinuxagent-acl-config/waagent.conf
%{_sysconfdir}/systemd/system/waagent.service
%{_sysconfdir}/systemd/system/multi-user.target.d/10-waagent-sysext.conf

%changelog
* Thu Apr 23 2026 Mayank Singh <mayansingh@microsoft.com> - 1.0.0-1
- Initial package: ACL-specific WALinuxAgent config overlay
- waagent.conf with ACL provisioning defaults
- waagent.service ordered after systemd-sysext.service
- multi-user.target drop-in (Upholds=waagent.service)
- Original version for Azure Linux.
- License verified.
