%define debug_package %{nil}
Summary:        Create new systemd timer to check for system restart
Name:           check-restart
Version:        1.0.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        check-restart.service
Source1:        check-restart.sh
Source2:        check-restart.timer
BuildRequires:  systemd
Requires:       dnf-utils
Requires:       systemd

%description
Creates a systemd service and timer that check if system needs to be restarted due to recent version updates

%prep

%build

%install
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_bindir}
install -D -m 644 %{SOURCE0} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.timer
install -m644 %{SOURCE1} %{buildroot}%{_bindir}/%{name}.sh

%post
%systemd_post check-restart.{service,timer}

%postun
%systemd_preun check-restart.{service,timer}

%files
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer
%{_bindir}/%{name}.sh

%changelog
* Tue Jan 04 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-2
- Update timer and service to avoid starting service on system reboot.
- License verified

* Mon Aug 02 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
