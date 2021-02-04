%global debug_package %{nil}

Summary:        Collection of configuration overrides for Azure hosted images
Name:           az-config
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://aka.ms/mariner
Group:          Applications/Text
Vendor:         Microsoft
Distribution:   Mariner
Source0:        01-cloud-init.cfg
Source1:        10-security-hardening.conf
Source2:        overlay.conf
Source3:        br_netfilter.conf
Source4:        .profile
Source5:        sshd_config
Source6:        iptables
Source7:        66-azure-storage.rules
Source8:        99-azure-product-uuid.rules
Source9:        system.conf
Source10:       LICENSE

Requires: openssh-server
Requires: cloud-init
Requires: dhcp-client
Requires: iptables
Requires: systemd
Requires: shadow-utils
Requires: initramfs

%description
Collection of configuration overrides for Azure hosted images

%prep

%build

%install
install -d -m 0755 %{buildroot}%{_sysconfdir}/cloud/cloud.cfg.d
install -p -m 644 -t %{buildroot}%{_sysconfdir}/cloud/cloud.cfg.d %{S:0}

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysctl.d
install -p -m 644 -t %{buildroot}%{_sysconfdir}/sysctl.d %{S:1}

install -d -m 0755 %{buildroot}%{_sysconfdir}/modules-load.d
install -p -m 644 -t %{buildroot}%{_sysconfdir}/modules-load.d %{S:2}
install -p -m 644 -t %{buildroot}%{_sysconfdir}/modules-load.d %{S:3}

install -d -m 0700 %{buildroot}/root
install -p -m 644 -t %{buildroot}/root %{S:4}

install -d -m 0755 %{buildroot}%{_sysconfdir}/ssh
install -p -m 644 -T %{S:5} %{buildroot}%{_sysconfdir}/ssh/sshd_config.ori

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 -t %{buildroot}%{_sysconfdir}/sysconfig %{S:6}

install -d -m 0755 %{buildroot}%{_sysconfdir}/udev/rules.d
install -p -m 644 -t %{buildroot}%{_sysconfdir}/udev/rules.d %{S:7}
install -p -m 644 -t %{buildroot}%{_sysconfdir}/udev/rules.d %{S:8}

install -d -m 0755 %{buildroot}%{_sysconfdir}/systemd/system.conf.d
install -p -m 644 -t %{buildroot}%{_sysconfdir}/systemd/system.conf.d %{S:9}

%post
# update dhcp configuration
cat <<EOF >> /etc/systemd/network/99-dhcp-en.network

[DHCP]
UseDomains=true
EOF

# dhclient to disallow long leases
cat <<EOF>> /etc/dhcp/dhclient.conf

supersede dhcp-rebinding-time 30000;
supersede dhcp-renewal-time 20000;
EOF

systemctl enable serial-getty@ttyS0.service
systemctl start serial-getty@ttyS0.service
# enable docker service
systemctl enable docker.service
systemctl start docker.service
# lock root password
passwd -l root
# update sshd
mv /etc/ssh/sshd_config.ori /etc/ssh/sshd_config
# update firewall configuration
mv /etc/sysconfig/iptables /etc/systemd/scripts/ip4save

%files
%defattr(-,root,root)
%license ../SOURCES/LICENSE
%{_sysconfdir}
/root/.profile

%changelog
* Thu Feb 04 2021 George Mileka <gmileka@microsoft.com> 1.0.0-0
- Created
