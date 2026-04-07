# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           fedora-iot-config
Version:        1
Release:        4%{?dist}
Summary:        Fedora IoT Configuration file

License:        MIT
URL:            https://fedoraproject.org/
Source0:        fedora-iot.conf
Source1:        fedora-iot-config-remote-fix.service
Source2:        fedora-iot-config-remote-fix.sh

BuildArch: noarch

BuildRequires: systemd-rpm-macros
BuildRequires: ostree-libs
Requires: ostree-libs

Provides:       fedora-iot-config(%{version}) = %{release}

%description
Fedora IoT configuration file for ostree repositories. 


%prep
# None required

%build
# None required

%install
install -d %{buildroot}%{_sysconfdir}/ostree/remotes.d/
install -pm 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/ostree/remotes.d/
install -d %{buildroot}%{_unitdir}/
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -d %{buildroot}%{_sbindir}
install -pm 0755 %{SOURCE2} %{buildroot}%{_sbindir}

%post
%systemd_post fedora-iot-config-remote-fix.service

%preun
%systemd_preun fedora-iot-config-remote-fix.service

%postun
%systemd_postun fedora-iot-config-remote-fix.service

%files
%config %{_sysconfdir}/ostree/remotes.d/fedora-iot.conf
%{_unitdir}/fedora-iot-config-remote-fix.service
%{_sbindir}/fedora-iot-config-remote-fix.sh


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 16 2024 Paul Whalen <pwhalen@fedoraproject.org> - 1-1
- add systemd scriptlets

* Wed Feb 07 2024 Paul Whalen <pwhalen@fedoraproject.org> - 0.0-7
- add script and service to detect and remove sysroot remote repo (issue#2)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Paul Whalen <pwhalen@fedoraproject.org> - 0.0-4
- change gpg-verify to true

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 30 2023 Paul Whalen <pwhalen@fedoraproject.org> - 0.0-2
- Add requires ostree-libs, fix spec

* Tue Mar 07 2023 Paul Whalen <pwhalen@fedoraproject.org> - 0.0-1
- initial packaging
