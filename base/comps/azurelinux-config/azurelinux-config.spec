%define is_development 1

Summary:        Azure Linux configuration override meta-package
Name:           azurelinux-config
Version:        4.0
Release:        %autorelease %[0%{?is_development} ? "-p" : ""]
License:        MIT
URL:            https://aka.ms/azurelinux

Source1:        50-default.network
Source2:        10-azurelinux-firewalld.preset
Source3:        azurelinux-firewalld-zone.xml
Source4:        firewalld-azurelinux.conf

BuildArch:      noarch

%description
Provides AZL specifc configuration overrides via sub-packages. These sub-packages will be pulled in by the relevant owning packages via reverse dependencies.


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
install -m 644 %{_sourcedir}/50-default.network %{buildroot}%{_sysconfdir}/systemd/network/50-default.network
install -d %{buildroot}%{_sysconfdir}/systemd/system-preset
install -m 644 %{_sourcedir}/10-azurelinux-firewalld.preset %{buildroot}%{_sysconfdir}/systemd/system-preset/10-azurelinux-firewalld.preset
install -d %{buildroot}%{_sysconfdir}/firewalld/zones
install -m 644 %{_sourcedir}/azurelinux-firewalld-zone.xml %{buildroot}%{_sysconfdir}/firewalld/zones/azurelinux.xml
install -m 644 %{_sourcedir}/firewalld-azurelinux.conf %{buildroot}%{_sysconfdir}/firewalld/firewalld-azurelinux.conf

%post firewalld
ln -sf %{_sysconfdir}/firewalld/firewalld-azurelinux.conf %{_sysconfdir}/firewalld/firewalld.conf

%postun firewalld
ln -sf %{_sysconfdir}/firewalld/firewalld-standard.conf %{_sysconfdir}/firewalld/firewalld.conf

%files systemd-networkd
%config(noreplace) /etc/systemd/network/50-default.network

%files firewalld
%config(noreplace) /etc/systemd/system-preset/10-azurelinux-firewalld.preset
%config(noreplace) /etc/firewalld/zones/azurelinux.xml
%config(noreplace) /etc/firewalld/firewalld-azurelinux.conf

%changelog
%autochangelog
