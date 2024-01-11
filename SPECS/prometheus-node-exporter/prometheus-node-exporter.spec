%global build_date $(date +"%%Y%%m%%d-%%T")
%global debug_package %{nil}
%global go_version %(go version | sed -E "s/go version go(\\S+).*/\\1/")

Summary:        Exporter for machine metrics
Name:           prometheus-node-exporter
Version:        1.7.0
Release:        1%{?dist}
# Upstream license specification: Apache-2.0
License:        ASL 2.0 AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/prometheus/node_exporter
Source0:        https://github.com/prometheus/node_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using vendored Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/prometheus/node_exporter/archive/refs/tags/v%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. Apply patches from the spec (may change go dependencies).
#   5. go mod vendor
#   6. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
Source2:        %{name}.sysusers
Source3:        %{name}.service
Source4:        %{name}.conf
Source5:        %{name}.logrotate
# Replace defaults paths for config files
Patch0:         defaults-paths.patch

BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

Requires(pre):  shadow-utils

%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written
in Go with pluggable metric collectors.

%prep
%autosetup -p1 -n node_exporter-%{version}

rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner

%build
export BUILDTAGS="netgo osusergo static_build"
LDFLAGS="-X github.com/prometheus/common/version.Version=%{version}      \
         -X github.com/prometheus/common/version.Revision=%{release}     \
         -X github.com/prometheus/common/version.Branch=tarball          \
         -X github.com/prometheus/common/version.BuildDate=%{build_date} \
         -X github.com/ncabatoff/process-exporter/version.GoVersion=%{go_version}"
go build -ldflags "$LDFLAGS" -mod=vendor -v -a -tags "$BUILDTAGS" -o bin/node_exporter

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp bin/* %{buildroot}%{_bindir}/
mv %{buildroot}%{_bindir}/node_exporter %{buildroot}%{_bindir}/%{name}
ln -s %{name} %{buildroot}%{_bindir}/node_exporter

install -Dpm0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -Dpm0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -Dpm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/%{name}
install -Dpm0644 example-rules.yml %{buildroot}%{_datadir}/prometheus/node-exporter/example-rules.yml
install -Dpm0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus/node-exporter

%check
bin/node_exporter --help && make test

%pre
# Steps extracted from Fedora's /usr/lib/rpm/sysusers.generate-pre.sh script.
# The script and the RPM macro 'sysusers_create_compat' calling it are not available
# in Mariner's 'systemd-rpm-macros' package.
# Input file for the script was %%{SOURCE2}.
getent group 'prometheus' >/dev/null || groupadd -r 'prometheus'
getent passwd 'prometheus' >/dev/null || useradd -r -g 'prometheus' -d '%{_sharedstatedir}/prometheus' -s '%{_sbindir}/nologin' -c 'Prometheus user account' 'prometheus'

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE NOTICE
%doc docs examples CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md
%doc MAINTAINERS.md SECURITY.md README.md
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/*
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_datadir}/prometheus/node-exporter/example-rules.yml
%dir %attr(0755,prometheus,prometheus) %{_sharedstatedir}/prometheus
%dir %attr(0755,prometheus,prometheus) %{_sharedstatedir}/prometheus/node-exporter

%changelog
* Wed Jan 10 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.0-1
- Auto-upgrade to 1.7.0

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-21
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.3.1-20
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-19
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-18
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-17
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-16
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-15
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-14
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-13
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-12
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.3.1-11
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.3.1-10
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.3.1-9
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.3.1-8
- Bump release to rebuild with golang 1.18.3

* Thu Mar 31 2022 Matthew Torr <matthewtorr@microsoft.com> - 1.3.1-7
- Build executable, not ar archive.

* Mon Jan 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.1-6
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-4
- Add logrotate file

* Sat Jan 15 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-3
- Add LDFLAGS

* Fri Jan 14 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-2
- Fix home directory permissions

* Fri Jan 14 2022 Robert-André Mauchin <zebob.m@gmail.com> 1.3.1-1
- Update to 1.3.1 Close: rhbz#2024811 Close: rhbz#2039257

* Thu Aug 12 2021 Robert-André Mauchin <zebob.m@gmail.com> 1.2.2-1
- Update to 1.2.2 Close: rhbz#1945422

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Mar 28 18:14:35 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.1.1-2
- Fix binary location

* Wed Feb 17 22:48:22 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.1.1-1
- Initial package
