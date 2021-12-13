Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: redfish-finder 
Version: 0.4
Release: 4%{?dist}
Summary: Utility for parsing SMBIOS information and configuring canonical BMC access
BuildArch: noarch

License: GPLv2
URL: https://github.com/nhorman/redfish-finder
Source0: %url/archive/V%{version}/%{name}-%{version}.tar.gz

Patch0: redfish-finder-python3.patch

%{?systemd_requires}
BuildRequires: systemd

Requires: python3 NetworkManager dmidecode

%description
Scans Smbios information for type 42 management controller information, and uses
that to configure the appropriate network interface so that the BMC is
canonically accessible via the host name redfish-localhost

%prep
%autosetup


%build
#noop here

%install
install -D -p -m 0755 redfish-finder %{buildroot}/%{_bindir}/redfish-finder
install -D -p -m 0644 redfish-finder.1 %{buildroot}/%{_mandir}/man1/redfish-finder.1
install -D -p -m 0644 ./redfish-finder.service %{buildroot}/%{_unitdir}/redfish-finder.service

%post
%systemd_post redfish-finder.service

%preun
%systemd_preun redfish-finder.service

%postun
%systemd_postun_with_restart redfish-finder.service


%files
%doc README.md
%license COPYING
%{_bindir}/redfish-finder
%{_mandir}/man1/redfish-finder.1.*
%{_unitdir}/redfish-finder.service

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Neil Horman <nhorman@redhat.com> - 0.4-2
-Fixup interpreter (bz 1770861)

* Thu Oct 17 2019 Neil Horman <nhorman@redhat.com> - 0.4-1
- Update to latest upstream (bz1730589)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Neil Horman <nhorman@redhat.com> - 0.3-1
- Update to latest upstream release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 19 2018 Neil Horman <nhorman@redhat.com> - 0.2-1
- Update to new upstream release

* Thu Oct 04 2018 Neil Horman <nhorman@tuxdriver.com> - 0.1-3
- Fixed missing BuildRequires/Requires
- Fixed missing dist tag
- Fixed Source url

* Wed Oct 03 2018 Neil Horman <nhorman@tuxdriver.com> - 0.1-2
- Updated requires for python3
- Removed unneeded BuildRequires
- Globed the inclusion of man page
- Fixed license file tagging

* Mon Oct 01 2018 Neil Horman <nhorman@tuxdriver.com> - 0.1-1 
- Initial import

