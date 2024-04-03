Summary:        Package to TODO
Name:           azurelinux-sysinfo
Version:        %{azl}.0
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0: collect-mariner-metrics.py
Source1: mariner_metrics_schema_v1.json
Source2: mariner-metrics-livecd.service
Requires: systemd
Requires: selinux-policy
# Requires: python-attrs
Requires: python3-psutil
# Apr 03 15:33:47 mariner-vm python3[1576]:     from attrs import define
# Apr 03 15:33:47 mariner-vm python3[1576]: ModuleNotFoundError: No module named 'attrs'
BuildRequires: systemd 
BuildRequires: selinux-policy
# do we need this in requires or buildrequires? find out through trial and error

%description
This is my first RPM package, which does nothing.

%prep
# we have no source, so nothing here

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
/usr/local/bin/collect-mariner-metrics.py
/usr/local/data/mariner_metrics_schema_v1.json
/etc/systemd/system/mariner-metrics-livecd.service

%post
# selinux policies for service needed:
FILE10=/tmp/selinuxpolicies.cil
cat << EOF > $FILE10
(allow semanage_t rpm_script_tmp_t (file (read open getattr map)))
(allow systemd_analyze_t sysctl_kernel_t (dir (search)))
(allow systemd_analyze_t locale_t (dir (search)))
(allow systemd_analyze_t init_runtime_t (dir (search)))
(allow systemd_analyze_t sysctl_kernel_t (file (read)))
(allow systemd_analyze_t locale_t (file (read)))
(allow systemd_analyze_t systemd_analyze_t (capability (net_admin)))
(allow systemd_analyze_t init_t (unix_stream_socket (connectto)))
(allow systemd_analyze_t system_dbusd_runtime_t (dir (search)))
(allow systemd_analyze_t security_t (filesystem (getattr)))
(allow systemd_analyze_t selinux_config_t (dir (search)))
(allow systemd_analyze_t init_t (system (status)))
(allow systemd_analyze_t init_t (service (status)))
(allow systemd_analyze_t systemdunit (service (status)))
(allow systemd_analyze_t etc_t (service (status)))

EOF

semodule -X 100 -i $FILE10

#!/bin/sh
systemctl enable mariner-metrics-livecd.service

%changelog
* Fri Mar 29 2024 Amrita Kohli <amritakohli@microsoft.com> - 3.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
- Bump version to 3.0 for AzureLinux 3.0


