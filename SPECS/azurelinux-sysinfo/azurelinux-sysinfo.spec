Summary:        Package to deploy azurelinux-sysinfo service
Name:           azurelinux-sysinfo
Version:        %{azl}.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/azurelinux
Source0:        collect-sysinfo.py
Source1:        sysinfo-schema-v1.json
Source2:        azurelinux-sysinfo.service
Requires:       systemd
Requires:       python3-psutil

%description
Deploys a systemd service that collects system information related to the device, operating system, cloud-init, boot 
time, resource utilization, installed packages, and SELinux mode. Collected information is written in JSON format to
a log file on the user's system for easy access and analysis. The systemd service runs at boot time if installed during 
image creation.

%install
# Copy collection python script to /usr/local/bin/
mkdir -p %{buildroot}/usr/local/bin/
install -m 755 %{SOURCE0} %{buildroot}/usr/local/bin/

# Copy data schema to /usr/local/data/
mkdir -p %{buildroot}/usr/local/data/
install -m 755 %{SOURCE1} %{buildroot}/usr/local/data/

# Copy service to /etc/systemd/system/
mkdir -p %{buildroot}/etc/systemd/system/
install -m 755 %{SOURCE2} %{buildroot}/etc/systemd/system/

%files
/usr/local/bin/collect-sysinfo.py
/usr/local/data/sysinfo-schema-v1.json
/etc/systemd/system/azurelinux-sysinfo.service

%post
#!/bin/sh
systemctl enable azurelinux-sysinfo.service

%changelog
* Wed Apr 03 2024 Amrita Kohli <amritakohli@microsoft.com> - 3.0-1
- License verified.
- Implementation of package that deploys azurelinux-sysinfo service.
- Original version for Azure Linux.


