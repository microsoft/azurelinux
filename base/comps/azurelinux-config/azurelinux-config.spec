Summary:        Azure Linux configuration override meta-package
Name:           azurelinux-config
Version:        4.0
Release:        %autorelease %[0%{?is_development} ? "-p" : ""]
License:        MIT
URL:            https://aka.ms/azurelinux

Source1:        50-default.network

BuildArch:      noarch

%description
Provides AZL specifc configuration overrides via sub-packages. These sub-packages will be pulled in by the relevant owning packages via reverse dependencies.


%package systemd-networkd
Summary:        Azure Linux specific configuration for systemd-networkd.
Requires:       systemd-networkd

%description systemd-networkd
Provides systemd-networkd configuration installed to /etc/systemd/network. These ask systemd to manage all interfaces on the system.

%install
install -d %{buildroot}%{_sysconfdir}/systemd/network
install -m 644 %{_sourcedir}/50-default.network %{buildroot}%{_sysconfdir}/systemd/network/50-default.network

%files systemd-networkd
%config(noreplace) /etc/systemd/network/50-default.network

%changelog
%autochangelog
