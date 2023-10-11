Summary:        Kubernetes daemon to detect and report node issues
Name:           node-problem-detector
Version:        0.8.10
Release:        16%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            https://github.com/kubernetes/node-problem-detector
Source0:        https://github.com/kubernetes/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         001-remove_arch_specific_makefile_logic.patch
Patch1:         002-add_mariner_OSVersion.patch
BuildRequires:  golang
BuildRequires:  systemd-devel
Requires:       mariner-release
%if %{with_check}
BuildRequires:  mariner-release
%endif

%description
node-problem-detector aims to make various node problems visible to the
upstream layers in the cluster management stack. It is a daemon that
runs on each node, detects node problems and reports them to apiserver.

%package config
Summary:        Default configs for node-problem-detector
Requires:       node-problem-detector

%description config
Default configuration files for node-problem-detector

%prep
%autosetup -p1

%build
%make_build build-binaries VERSION=%{version}

%install
mkdir -p %{buildroot}%{_bindir}/
install -vdm 755 %{buildroot}/%{_bindir}
install -pm 755 output/linux/bin/node-problem-detector %{buildroot}%{_bindir}/
install -pm 755 output/linux/bin/health-checker %{buildroot}%{_bindir}/
install -pm 755 output/linux/bin/log-counter %{buildroot}%{_bindir}/

install -vdm 755 %{buildroot}%{_sysconfdir}/node-problem-detector.d
cp -R config %{buildroot}%{_sysconfdir}/node-problem-detector.d

chmod 755 %{buildroot}%{_sysconfdir}/node-problem-detector.d/config/plugin/check_ntp.sh
chmod 755 %{buildroot}%{_sysconfdir}/node-problem-detector.d/config/plugin/network_problem.sh

%check
make test

%files
%license LICENSE
%defattr(-,root,root,0755)
%{_bindir}/node-problem-detector
%{_bindir}/health-checker
%{_bindir}/log-counter

%files config
%license LICENSE
%defattr(-,root,root,0755)
%config(noreplace) %{_sysconfdir}/node-problem-detector.d/*

%changelog
* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.8.10-16
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-15
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-14
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-13
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-12
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-11
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-10
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-9
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.10-8
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.8.10-7
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.8.10-6
- Bump release to rebuild with go 1.18.8

* Mon Aug 29 2022 Sean Dougherty <sdougherty@microsoft.com> - 0.8.10-5
- Removed arch-specific logic in Makefile with 001-remove_arch_specific_makefile_logic.patch.

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.8.10-4
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 0.8.10-3
- Bump release to rebuild with golang 1.18.3

* Wed Jun 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.8.10-2
- Add explicit check/run-time dependencies on mariner-release

* Fri Feb 25 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 0.8.10-1
- Upgrading to v0.8.10
- Disable arm64 builds in Makefile with remove_arm64_build.patch.

* Tue Jun 15 2021 Henry Beberman <henry.beberman@microsoft.com> - 0.8.8-1
- Add node-problem-detector spec.
- Add Mariner to OSVersion detection and disable exe builds in makefile.
- License verified
- Original version for CBL-Mariner
