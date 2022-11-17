Name:           influxdb2
Summary:        Scalable datastore for metrics, events, and real-time analytics
License:        MIT
Group:          Productivity/Databases/Servers
Version:        2.4.0
Release:        %1{?dist}
URL:            https://github.com/influxdata/influxdb
Source0:        %{URL}/archive/refs/tags/v%{version}.tar.gz
Source99:       %{name}-%{version}-vendor.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  sysuser-tools
%{sysusers_requires}
BuildRequires:  fdupes
BuildRequires:  go >= 1.18
BuildRequires:  golang-packaging >= 15.0.8
BuildRequires:  build-essential
BuildRequires:  pkg-config >= 0.171.0
BuildRequires:  protobuf-devel
BuildRequires:  kernel-headers
BuildRequires:  make
BuildRequires:  rust
BuildRequires:  clang
BuildRequires:  tzdata

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

%{!?_tmpfilesdir:%global _tmpfilesdir /usr/lib/tmpfiles.d}

%description
InfluxDB is an distributed time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%package        devel
Summary:        InfluxDB development files
Group:          Development/Languages/Golang
Requires:       go

%description devel
Go sources and other development files for InfluxDB

%prep
%setup -q
%setup -q -T -D -a 99

%build
export GO111MODULE=on

# Build influxdb
%goprep github.com/influxdata/influxdb/v2
%gobuild -mod=vendor -ldflags="-X main.version=%{version}" cmd/...

%sysusers_generate_pre %{SOURCE3} %{name}

%install
%gosrc
%fdupes -s %{buildroot}/%{go_contribsrcdir}/github.com/influxdata/influxdb

mkdir -p %{buildroot}%{_localstatedir}/log/influxdb
mkdir -p %{buildroot}%{_localstatedir}/lib/influxdb
mkdir -p %{buildroot}%{_sbindir}
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rcinfluxdb
install -D -m 0755 -t %{buildroot}%{_bindir} %{_builddir}/go/bin/*

%check
make test

%pre -f %{name}.pre
%service_add_pre influxdb.service

%preun
%service_del_preun influxdb.service

%post
%tmpfiles_create %_tmpfilesdir/influxdb.conf
%service_add_post influxdb.service

%postun
%service_del_postun influxdb.service

%files
%license LICENSE
%doc README.md CHANGELOG.md
%dir %{_sysconfdir}/influxdb2
%{_bindir}/influxd
%{_bindir}/telemetryd
%{_sbindir}/rcinfluxdb
%{_datadir}/influxdb2
%dir %{_tmpfilesdir}
%attr(0755, influxdb, influxdb) %dir %{_localstatedir}/log/influxdb
%attr(0755, influxdb, influxdb) %dir %{_localstatedir}/lib/influxdb

%files devel
%license LICENSE
%dir %{go_contribsrcdir}/github.com
%dir %{go_contribsrcdir}/github.com/influxdata
%{go_contribsrcdir}/github.com/influxdata/influxdb

%changelog