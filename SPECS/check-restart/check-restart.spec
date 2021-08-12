%define debug_package %{nil}

Name:           check-restart
Version:        1.0.0
Release:        1%{?dist}
Summary:        Create new systemd timer to check for system restart 
License:        MIT
Source0:        check-restart.service
Source1:        check-restart.sh
Source2:        check-restart.timer
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  systemd
Requires:       systemd
Requires:       dnf-utils

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
* Mon Aug 02 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
