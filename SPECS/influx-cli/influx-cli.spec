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
Release:        1%{?dist}
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
BuildRequires:  go >= 1.17
BuildRequires:  golang-packaging >= 15.0.8
BuildRequires:  systemd-rpm-macros

%description
CLI for managing resources in InfluxDB v2.

%package bash-completion
Summary:        Bash Completion for %{name}
Group:          Productivity/Databases/Servers
Requires:       bash-completion
Supplements:    (%{name} and bash)
BuildArch:      noarch

%description bash-completion
The official bash completion script for influx. It includes support
for every argument that can currently be passed to influx.

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

mkdir -p %{buildroot}/%{_datadir}/bash-completion/completions
bin/influx completion bash > %{buildroot}/%{_datadir}/bash-completion/completions/influx

mkdir -p %{buildroot}/%{_datadir}/zsh/site-functions
bin/influx completion zsh > %{buildroot}/%{_datadir}/zsh/site-functions/_influx

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/influx

%files bash-completion
%{_datadir}/bash-completion

%files zsh-completion
%{_datadir}/zsh

%changelog
* Wed Jan 18 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.4.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified
- Upgrade to version 2.4.0

* Wed Jun 15 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Version 2.3.0

* Wed Nov 17 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Initial version
