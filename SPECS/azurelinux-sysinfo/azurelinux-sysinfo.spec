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

%files
%{_bindir}/collect-sysinfo
%{_datadir}/azurelinux-sysinfo/sysinfo-schema-v1.json
%{_sysconfdir}/systemd/system/azurelinux-sysinfo.service

%post
#!/bin/sh
systemctl enable azurelinux-sysinfo.service

%changelog
* Thu Apr 04 2024 Amrita Kohli <amritakohli@microsoft.com> - 3.0-1
- License verified.
- Implementation of package that deploys azurelinux-sysinfo service.
- Original version for Azure Linux.


