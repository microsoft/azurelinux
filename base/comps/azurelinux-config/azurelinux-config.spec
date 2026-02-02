%define is_development 1

Summary:        Azure Linux configuration override meta-package
Name:           azurelinux-config
Version:        4.0
Release:        %autorelease %[0%{?is_development} ? "-p" : ""]
License:        MIT
URL:            https://aka.ms/azurelinux

Source1:        50-default.network
Source2:        azurelinux-firewalld-zone.xml
Source3:        firewalld-azurelinux.conf

BuildArch:      noarch

%description
Provides AZL specific configuration overrides via sub-packages. These sub-packages will be pulled in by the relevant owning packages via reverse dependencies.


%package systemd-networkd
Summary:        Azure Linux specific configuration for systemd-networkd.
Requires:       systemd-networkd
# This is a reverse dependency to make systemd-networkd pull-in this package.
# It is still experimental. Consider this as a placeholder.
Supplements:    systemd-networkd

%description systemd-networkd
Provides systemd-networkd configuration installed at /etc/systemd/network which asks systemd to manage all interfaces on the system.

%package firewalld
Summary:        Azure Linux firewall policies
Requires:       firewalld
Supplements:    firewalld

%description firewalld
Provides Azure Linux specific policies and zones for firewalld. 

%install
install -d %{buildroot}%{_sysconfdir}/systemd/network
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/network/50-default.network
install -d %{buildroot}%{_sysconfdir}/firewalld/zones
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/firewalld/zones/azurelinux.xml
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/firewalld/firewalld-azurelinux.conf

# We need the post/postun symlink to avoid littering /etc/firewalld with rpm save files.
%post firewalld
ln -sf %{_sysconfdir}/firewalld/firewalld-azurelinux.conf %{_sysconfdir}/firewalld/firewalld.conf

%postun firewalld
ln -sf %{_sysconfdir}/firewalld/firewalld-standard.conf %{_sysconfdir}/firewalld/firewalld.conf

%files systemd-networkd
%config(noreplace) /etc/systemd/network/50-default.network

%files firewalld
%config(noreplace) /etc/firewalld/zones/azurelinux.xml
%config(noreplace) /etc/firewalld/firewalld-azurelinux.conf

%changelog
%autochangelog
