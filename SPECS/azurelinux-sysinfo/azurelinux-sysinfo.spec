Summary:        Package to deploy azurelinux-sysinfo service
Name:           azurelinux-sysinfo
Version:        %{azl}.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/azurelinux
Source0:        collect-sysinfo
Source1:        sysinfo-schema-v1.json
Source2:        azurelinux-sysinfo.service
Source3:        sysinfo-selinuxpolicies.cil
Requires:       systemd
Requires:       python3-psutil

%description
Deploys a systemd service that gathers system information related to the device, operating system, cloud-init, boot 
time, resource utilization, installed packages, and SELinux mode. Collected information is written in JSON format to
a log file on the user's system for easy access and analysis. The systemd service runs at boot time if installed during 
image creation.

%install
# Copy collection python script to /usr/bin/
mkdir -p %{buildroot}%{_bindir}/
install -m 755 %{SOURCE0} %{buildroot}%{_bindir}/

# Copy data schema to /usr/share/azurelinux-sysinfo/
mkdir -p %{buildroot}%{_datadir}/azurelinux-sysinfo/
install -m 755 %{SOURCE1} %{buildroot}%{_datadir}/azurelinux-sysinfo/

# Copy service to /etc/systemd/system/
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/system/

# Copy the sysinfo-selinuxpolicies file to /usr/share/selinux/packages/
mkdir -p %{buildroot}%{_datadir}/selinux/packages/
install -m 755 %{SOURCE3} %{buildroot}%{_datadir}/selinux/packages/

%files
%{_bindir}/collect-sysinfo
%dir %{_datadir}/azurelinux-sysinfo/
%{_datadir}/azurelinux-sysinfo/sysinfo-schema-v1.json
%{_sysconfdir}/systemd/system/azurelinux-sysinfo.service
%{_datadir}/selinux/packages/sysinfo-selinuxpolicies.cil

%post
#!/bin/sh
# Enable the systemd service
systemctl enable azurelinux-sysinfo.service

if rpm -q selinux-policy &> /dev/null; then
    # Apply required SElinux policies only if selinux-policy is present
    semodule -i %{_datadir}/selinux/packages/sysinfo-selinuxpolicies.cil
fi

%postun
# If selinux-policy is present, remove the sysinfo-selinuxpolicies module
if rpm -q selinux-policy &> /dev/null; then
    semodule -r sysinfo-selinuxpolicies
fi

%changelog
* Thu Apr 04 2024 Amrita Kohli <amritakohli@microsoft.com> - 3.0-1
- License verified.
- Implementation of package that deploys azurelinux-sysinfo service.
- Original version for Azure Linux.


