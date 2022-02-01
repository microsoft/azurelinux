%global debug_package %{nil}
%global builddate $(date +"%%Y%%m%%d-%%T")

Summary:        Prometheus exporter exposing process metrics from procfs
Name:           prometheus-process-exporter
Version:        0.7.10
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ncabatoff/process-exporter
Source0:        https://github.com/ncabatoff/process-exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using vendored Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/ncabatoff/process-exporter/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

Requires(pre):  shadow-utils

%description
Prometheus exporter that exposes process metrics from procfs.

Some apps are impractical to instrument directly, either because you don't
control the code or they're written in a language that isn't easy to
instrument with Prometheus. This exporter solves that issue by mining
process metrics from procfs.

%prep
%autosetup -n process-exporter-%{version} -p1

rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner

%build
export BUILDTAGS="netgo osusergo static_build"
LDFLAGS="-X github.com/prometheus/common/version.Version=%{version}  \
         -X github.com/prometheus/common/version.Revision=%{release} \
         -X github.com/prometheus/common/version.Branch=tarball      \
         -X github.com/prometheus/common/version.BuildDate=%{builddate} "
go build -ldflags "$LDFLAGS" -mod=vendor -v -a -tags "$BUILDTAGS" -o bin/node_exporter ./collector

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp bin/* %{buildroot}%{_bindir}/
mv %{buildroot}%{_bindir}/node_exporter %{buildroot}%{_bindir}/%{name}
pushd %{buildroot}%{_bindir}
ln -s %{name} node_exporter
popd

install -Dpm0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -Dpm0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -Dpm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/%{name}
install -Dpm0644 example-rules.yml %{buildroot}%{_datadir}/prometheus/node-exporter/example-rules.yml
install -Dpm0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus/node-exporter

%check
pushd collector
go test
popd

%pre
%{sysusers_create_compat} %{SOURCE2}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc docs examples CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md
%doc MAINTAINERS.md SECURITY.md README.md
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_datadir}/prometheus/node-exporter/example-rules.yml
%dir %attr(0755,prometheus,prometheus) %{_sharedstatedir}/prometheus
%dir %attr(0755,prometheus,prometheus) %{_sharedstatedir}/prometheus/node-exporter

%changelog
* Tue Feb 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.10-1
- Initial CBL-Mariner import from Debian source package (license: MIT).
- License verified.
