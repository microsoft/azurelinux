Summary:        Azure Linux systemd network overrides
Name:           azurelinux-overrides
Version:        4.0
Release:        0.1
License:        MIT
URL:            https://aka.ms/azurelinux

Source1:        50-default.network

BuildArch:      noarch

%description
Provides systemd network override files installed to /etc/systemd/network. These make systemd manage all interfaces.

%prep

%build

%install
install -d %{buildroot}%{_sysconfdir}/systemd/network
install -m 644 %{_sourcedir}/50-default.network %{buildroot}%{_sysconfdir}/systemd/network/50-default.network

%files
%config(noreplace) /etc/systemd/network/50-default.network

%changelog
* Wed Jan 21 2026 Binu Philip <bphilip@microsoft.com> - 4.0-0.1
- Initial package
