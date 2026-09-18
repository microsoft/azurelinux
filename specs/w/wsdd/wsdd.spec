# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           wsdd
Version:        0.8
Release:        5%{?dist}
Summary:        Web Services Dynamic Discovery host daemon
License:        MIT 
URL:            https://github.com/christgau/wsdd 
Source0:        https://github.com/christgau/wsdd/archive/v%{version}/wsdd-%{version}.tar.gz

Patch:          Modify-systemd-service-for-Fedora.patch

BuildArch:      noarch
BuildRequires:  systemd


%description
wsdd implements a Web Service Discovery host daemon. This enables (Samba)
hosts, like your local NAS device, to be found by Web Service Discovery Clients
like Windows.


%prep
%autosetup -p1


%install
install -pDm644 etc/firewalld/services/wsdd.xml %{buildroot}%{_usr}/lib/firewalld/services/wsdd.xml
install -pDm644 etc/firewalld/services/wsdd-http.xml %{buildroot}%{_usr}/lib/firewalld/services/wsdd-http.xml
install -pDm644 etc/systemd/wsdd.defaults %{buildroot}%{_sysconfdir}/sysconfig/wsdd
install -pDm644 etc/systemd/wsdd.service %{buildroot}%{_unitdir}/wsdd.service
install -pDm644 man/wsdd.8 %{buildroot}%{_mandir}/man8/wsdd.8
install -pDm755 src/wsdd.py %{buildroot}%{_bindir}/wsdd

# Create a sysusers.d config file
cat >wsdd.sysusers.conf <<EOF
u wsdd - '%{summary}' - -
EOF

install -m0644 -D wsdd.sysusers.conf %{buildroot}%{_sysusersdir}/wsdd.conf



%post
%systemd_post wsdd.service

%preun
%systemd_preun wsdd.service

%postun
%systemd_postun_with_restart wsdd.service

%files
%{_unitdir}/wsdd.service
%{_usr}/lib/firewalld/services/wsdd.xml
%{_usr}/lib/firewalld/services/wsdd-http.xml
%config(noreplace) %{_sysconfdir}/sysconfig/wsdd
%{_bindir}/wsdd
%{_mandir}/man8/wsdd.8*
%license LICENSE
%doc AUTHORS README.md
%{_sysusersdir}/wsdd.conf


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-4
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 17 2024 Ondrej Holy <oholy@redhat.com> - 0.8.0-1
- Update to 0.8

* Fri Feb 16 2024 Ondrej Holy <oholy@redhat.com> - 0.7.1-3
- Fix backward compatibility (#2254986)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 06 2023 Ondrej Holy <oholy@redhat.com> - 0.7.1-1
- Update to 0.7.1.

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 03 2021 survient@fedoraproject.org - 0.7.0-1
- Latest upstream release.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 04 2021 Sam P <survient@fedoraproject.org> - 0.6.4-1
- Updated to latest upstream release.

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.3-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Sun Jan 31 2021 shareuser - 0.6.3-1
- Latest upstream release

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Sam P <survient@fedoraproject.org> - 0.6.1-2
- Added fixes from rh#1858858

* Mon Jul 13 2020 Sam P <survient@fedoraproject.org> - 0.6.1-1
- Updated to upstream latest release

* Fri Feb 21 2020 Sam P <survient@fedoraproject.org> - 0.5-2
- Removed unnecessary build dependency

* Thu Feb 20 2020 Sam P <survient@fedoraproject.org> - 0.5-1
- Updated to latest upstream release

* Wed Dec 11 2019 Sam P <survient@fedoraproject.org> - 0.4-2
- Added systemd unit scriptlet sections

* Tue Nov 19 2019 Sam P <survient@fedoraproject.org> - 0.4-1
- Initial package
