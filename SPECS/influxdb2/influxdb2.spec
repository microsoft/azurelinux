Summary:        Scalable datastore for metrics, events, and real-time analytics
Name:           influxdb2
Version:        2.4.0
Release:        0%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Databases/Servers
URL:            https://github.com/influxdata/influxdb
Source0:        %{url}%{archive}/refs/tags/v%{version}#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
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
# How to rebuild this file:
#   1. wget https://github.com/influxdata/influxdb/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. make generate-web-assets
#   5. cd static
#   6. tar -cvf %%{name}-%%{version}-static-data.tar.gz data/
Source2:        %{name}-%{version}-static-data.tar.gz
BuildRequires:  go >= 1.18
BuildRequires:  golang-packaging >= 15.0.8
BuildRequires:  pkgconfig(flux) >= 0.179.0
BuildRequires:  protobuf-devel
BuildRequires:  kernel-headers
BuildRequires:  make
BuildRequires:  rust >= 1.60.0
BuildRequires:  clang
BuildRequires:  tzdata
Requires:       tzdata
Conflicts:      influxdb

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
%autosetup

%build
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOPATH:$GOBIN
export GO111MODULE=on
tar -xf %{SOURCE1} --no-same-owner

mkdir -pv static
tar -xf %{SOURCE2} -C static/ --no-same-owner

# Build influxdb
export TAGS='sqlite_foreign_keys,sqlite_json,assets'
go generate -mod vendor -tags $TAGS ./static
go build -mod vendor -tags $TAGS -ldflags "-X main.version=%{version}" -o bin/influxd ./cmd/influxd
go build -mod vendor -tags $TAGS -ldflags "-X main.version=%{version}" -o bin/telemetryd ./cmd/telemetryd


%install
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOBIN

mkdir -p %{buildroot}%{_bindir}
install -D -m 0755 bin/influxd %{buildroot}%{_bindir}/
install -D -m 0755 bin/telemetryd %{buildroot}%{_bindir}/

%check
export GOTRACEBACK=all
export GO111MODULE=on
go test ./...

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/influxd
%{_bindir}/telemetryd
%changelog
