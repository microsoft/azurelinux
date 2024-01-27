#
# spec file for package influx-cli
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

Summary:        CLI for managing resources in InfluxDB
Name:           influx-cli
Version:        2.6.1
Release:        14%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Databases/Servers
URL:            https://github.com/influxdata/influx-cli
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Use generate_source_tarbbal.sh to get this generated from a source code file.
# How to re-build this file:
#   1. wget https://github.com/influxdata/influx-cli/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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

%description
CLI for managing resources in InfluxDB v2.

%package zsh-completion
Summary:        ZSH Completion for %{name}
Group:          Productivity/Databases/Servers
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description zsh-completion
The official zsh completion script for influx.

%prep
%autosetup -a 1

%build
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOPATH:$GOBIN
export GO111MODULE=on
go build -mod vendor -ldflags="-X main.version=%{version}" -o bin/influx ./cmd/influx

%install
mkdir -p %{buildroot}%{_bindir}
install -D -m 0755 bin/influx %{buildroot}%{_bindir}/

mkdir -p %{buildroot}/%{_datadir}/zsh/site-functions
bin/influx completion zsh > %{buildroot}/%{_datadir}/zsh/site-functions/_influx

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/influx

%files zsh-completion
%{_datadir}/zsh

%changelog
* Fri Jan 26 2024 Andrew Phelps <anphel@microsoft.com> - 2.6.1-14
- Remove restriction on golang BR version

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-13
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 2.6.1-12
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-9
- Bump release to rebuild with go 1.19.10

* Thu May 25 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsft.com> - 2.6.1-8
- Removed bash-completion subpackage since the script produced is included in original bash-completion.

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-7
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-6
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-5
- Bump release to rebuild with go 1.19.6

* Fri Feb 10 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.6.1-4
- Fixing spec supplement of bash-completion library to not conflict with existing bash-completion

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.6.1-3
- Bump release to rebuild with go 1.19.5

* Wed Feb 1 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.6.1-2
- Fixed build issue by requring to use golang 1.18.8. Does not work on 1.19 yet

* Mon Jan 30 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.6.1-1
- Upgrade to version 2.6.1

* Wed Jan 18 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.4.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- License verified
- Upgrade to version 2.4.0

* Wed Jun 15 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Version 2.3.0

* Wed Nov 17 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Initial version
