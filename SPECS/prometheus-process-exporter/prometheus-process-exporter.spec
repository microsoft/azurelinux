%global build_date $(date +"%%Y%%m%%d-%%T")
%global debug_package %{nil}
%global go_version %(go version | sed -E "s/go version go(\\S+).*/\\1/")

Summary:        Prometheus exporter exposing process metrics from procfs
Name:           prometheus-process-exporter
Version:        0.7.10
Release:        2%{?dist}
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
Source2:        %{name}.service
Source3:        %{name}.logrotate
Source4:        %{name}.conf
Patch0:         01-fix-RSS-test-on-non4K-pagesize-systems.patch
Patch1:         03-disable-fakescraper.patch

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
%autosetup -p1 -n process-exporter-%{version}

rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner

%build
LDFLAGS="-X github.com/ncabatoff/process-exporter/version.Version=%{version}      \
         -X github.com/ncabatoff/process-exporter/version.Revision=%{release}     \
         -X github.com/ncabatoff/process-exporter/version.Branch=tarball          \
         -X github.com/ncabatoff/process-exporter/version.BuildDate=%{build_date} \
         -X github.com/ncabatoff/process-exporter/version.GoVersion=%{go_version}"

# Modified "build" target from Makefile.
CGO_ENABLED=0 go build -ldflags "$LDFLAGS" -mod=vendor -v -a -tags netgo -o process-exporter ./cmd/process-exporter

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp process-exporter %{buildroot}%{_bindir}/%{name}
ln -s %{name} %{buildroot}%{_bindir}/process-exporter

install -Dpm0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -Dpm0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -Dpm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/%{name}

mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus

%check
make test integ

%pre
# Same user/group creation steps as for "prometheus-node-exporter".
getent group 'prometheus' >/dev/null || groupadd -r 'prometheus'
getent passwd 'prometheus' >/dev/null || useradd -r -g 'prometheus' -d '%{_sharedstatedir}/prometheus' -s '%{_sbindir}/nologin' -c 'Prometheus user account' 'prometheus'

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/*process-exporter
%{_unitdir}/%{name}.service
%dir %attr(0755,prometheus,prometheus) %{_sharedstatedir}/prometheus

%changelog
* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 0.7.10-2
- Bump release to rebuild with golang 1.18.3

* Tue Feb 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.10-1
- Initial CBL-Mariner import from Debian source package (license: MIT).
- License verified.
