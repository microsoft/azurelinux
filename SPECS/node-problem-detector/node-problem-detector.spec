Summary:        Kubernetes daemon to detect and report node issues
Name:           node-problem-detector
Version:        0.8.10
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            https://github.com/kubernetes/node-problem-detector
Source0:        https://github.com/kubernetes/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         001-remove_arm64_build.patch
Patch1:         002-remove_windows_build.patch
Patch2:         003-add_mariner_OSVersion.patch
BuildRequires:  golang
BuildRequires:  systemd-devel
%if %{with_check}
BuildRequires:  mariner-release
%endif
Requires:       mariner-release
ExclusiveArch:  x86_64

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
install -pm 755 output/linux_amd64/bin/node-problem-detector %{buildroot}%{_bindir}/
install -pm 755 output/linux_amd64/bin/health-checker %{buildroot}%{_bindir}/
install -pm 755 output/linux_amd64/bin/log-counter %{buildroot}%{_bindir}/

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
