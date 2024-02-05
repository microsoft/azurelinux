#
# spec file for package influxdb
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Summary:        Scalable datastore for metrics, events, and real-time analytics
Name:           influxdb
Version:        2.7.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Productivity/Databases/Servers
URL:            https://github.com/influxdata/influxdb
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Use generate_source_tarbbal.sh to get this generated from a source code file.
# How to re-build this file:
#   1. wget https://github.com/influxdata/influxdb/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
# Below is a manually created tarball, no download link.
# predownloaded assets include ui assets and swager json. Used to replace fetch-assets and fetch-swagger script.
# Use generate_source_tarbbal.sh to get this generated from a source code file.
# How to rebuild this file:
#   1. wget https://github.com/influxdata/influxdb/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. make generate-web-assets
#   5. cd static
#   6. tar -cvf %%{name}-%%{version}-static-data.tar.gz data/
Source2:        %{name}-%{version}-static-data.tar.gz
Source3:        influxdb.service
Source4:        influxdb.tmpfiles
Source5:        config.yaml
Source6:        influxdb-user.conf
BuildRequires:  clang
BuildRequires:  golang <= 1.18.8
BuildRequires:  kernel-headers
BuildRequires:  protobuf-devel
BuildRequires:  rust >= 1.60.0
BuildRequires:  systemd-rpm-macros
BuildRequires:  tzdata
# IMPORTANT:  when upgrading this, make sure the flux version matches what is required by go.mod file in the soure code of influxdb.
BuildRequires:  pkgconfig(flux) >= 0.194.5
Requires:       tzdata
Requires(post): systemd
Conflicts:      influxdb
%{?systemd_requires}

%description
InfluxDB is an distributed time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%package        devel
Summary:        InfluxDB development files
Group:          Development/Languages/Golang
Requires:       go
Requires:       tzdata
Conflicts:      influxdb

%description devel
Go sources and other development files for InfluxDB

%prep
%autosetup -a 1

mkdir -pv static
tar -xf %{SOURCE2} -C static/ --no-same-owner

%build
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOPATH:$GOBIN
export GO111MODULE=on

# Build influxdb
export TAGS='sqlite_foreign_keys,sqlite_json,assets'
go generate -mod vendor -tags $TAGS ./static
go build -mod vendor -tags $TAGS -ldflags "-X main.version=%{version}" -o bin/influxd ./cmd/influxd
go build -mod vendor -tags $TAGS -ldflags "-X main.version=%{version}" -o bin/telemetryd ./cmd/telemetryd

%install
mkdir -p %{buildroot}%{_bindir}
install -D -m 0755 bin/influxd %{buildroot}%{_bindir}/
install -D -m 0755 bin/telemetryd %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_sbindir}
install -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/influxdb.service
ln -s %{_sbindir}/service %{buildroot}%{_sbindir}/rcinfluxdb
install -D -m 0644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/influxdb.conf
install -D -m 0644 %{SOURCE6} %{buildroot}%{_sysusersdir}/influxdb-user.conf
install -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/influxdb/config.yaml

%check
export GOTRACEBACK=all
export GO111MODULE=on
go test ./...

%pre
%sysusers_create_package %{name} %{SOURCE6}

%preun
%systemd_preun influxdb.service

%post
%tmpfiles_create %{_tmpfilesdir}/influxdb.conf
%systemd_post influxdb.service

%postun
%systemd_postun_with_restart influxdb.service

%files
%license LICENSE
%doc README.md CHANGELOG.md
%dir %{_sysconfdir}/influxdb
%config(noreplace) %{_sysconfdir}/influxdb/config.yaml
%{_bindir}/influxd
%{_bindir}/telemetryd
%{_sbindir}/rcinfluxdb
%{_unitdir}/influxdb.service
%{_sysusersdir}/influxdb-user.conf
%dir %{_tmpfilesdir}
%{_tmpfilesdir}/influxdb.conf

%changelog
* Thu Feb 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.7.3-1
- Upgrade to version 2.7.3

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-12
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 2.6.1-11
- Bump release to rebuild with updated version of Go.

* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 2.6.1-10
- Bump package to rebuild with rust 1.72.0

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-9
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-8
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-7
- Bump release to rebuild with go 1.19.10

* Tue Apr 11 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.6.1-6
- Fixed uninstallation step not working

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-5
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-4
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-3
- Bump release to rebuild with go 1.19.6

* Wed Feb 1 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.6.1-2
- Fixed build issue by requring to use golang 1.18.8. Does not work on 1.19 yet.

* Mon Jan 30 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.6.1-1
- Upgrade to version 2.6.1

* Fri Jan 13 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.4.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified
- Upgrade to version 2.4.0

* Tue Oct  4 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 2.3.0, see
  * https://github.com/influxdata/influxdb/releases/tag/v2.3.0
  Drop 0001-fix-executor-do-not-assume-ints-are-64bits-4652.patch:
  upstreamed

* Thu Jun  9 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 2.2.0, see
  * https://github.com/influxdata/influxdb/releases/tag/v2.2.0
  Add 0001-fix-executor-do-not-assume-ints-are-64bits-4652.patch:
  fix build on 32-bit architectures

* Tue Nov 16 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 2.1.1, see
  * https://github.com/influxdata/influxdb/releases/tag/v2.1.1
- influx binary has been deleted upstream:
  * https://github.com/influxdata/influxdb/issues/21773

* Tue Oct 26 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 2.0.9, see
  * https://github.com/influxdata/influxdb/releases/tag/v2.0.9

* Fri Sep 24 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 2.0.8, see
  * https://github.com/influxdata/influxdb/releases/tag/v2.0.8

* Thu Jun 10 2021 Michal Hrusecky <michal.hrusecky@opensuse.org>
- Reintroduce configuration file in etc and provide example configuration:
  * no tracking by default
  * conservative memory limits to prevent OOM
  * description how to obtain list of possible values
  * example how to move stored data into different directory

* Thu Jun 10 2021 Michal Hrusecky <michal.hrusecky@opensuse.org>
- Update to version 2.0.7, see
  * https://github.com/influxdata/influxdb/releases/tag/v2.0.7

* Thu May 27 2021 Michal Hrusecky <michal.hrusecky@opensuse.org>
- Include prebuild UI assets
- Drop the last mention of config file in service file

* Wed May 19 2021 Michal Hrusecky <michal.hrusecky@opensuse.org>
- Update to version 2.0.6, see
  * https://github.com/influxdata/influxdb/releases/tag/v2.0.6
  * https://github.com/influxdata/influxdb/releases/tag/v2.0.5

* Mon May 17 2021 Michal Hrusecky <michal.hrusecky@opensuse.org>
- Update service file not to use invalid options
- Dropping config file as upstream does and dropping unused directories

* Thu Mar 18 08:12:08 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Install lost influxdb-user.conf

* Tue Mar 16 13:33:34 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Drop unused BuildRequirements
- use sysusers.d

* Sun Mar  7 08:54:12 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Initial version
