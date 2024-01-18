%define  debug_package %{nil}
Summary:        rabbitmq-server
Name:           rabbitmq-server
Version:        3.11.11
Release:        2%{?dist}
License:        Apache-2.0 and MPL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rabbitmq.com
Source0:        https://github.com/rabbitmq/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:        https://github.com/rabbitmq/mix_task_archive_deps/releases/download/1.0.0/mix_task_archive_deps-1.0.0.ez
Source2:        rabbitmq-server-hex-vendor-%{version}.tar.gz
# --------
# Steps to create the rabbitmq-server-hex-vendor tarball. A network connection is required ot create this vendor tarball
# --------
# 1. Run `./generate-rabbitmq-server-tarball.sh`
# --------
Source3:        rabbitmq-server-hex-cache-%{version}.tar.gz
# --------
# Steps to create the rabbitmq-server-hex-cache tarball. A network connection is required to create this cache.
# --------
# 1. To ensure the cache file is as small as possible, first delete ~/.hex/cache.ets if it exists
# 2. Pull the rabbitmq-server source from Source0
# 3. Unpack the source and run `make` with the rabbitmq-server-<version> directory
# 4. Run `make install`
# 5. Find the cache.ets file created by hex (likely ~/.hex/cache.ets by default)
# 6. Copy the cache.ets file to the same directory as rabbitmqHexCacheMakefile
# 7. Run `make generate-hex-cache -f rabbitmqHexCacheMakefile`
# 8. Run `tar -czf rabbitmq-server-hex-cache-<version>.tar.gz cache.erl`
# --------

BuildRequires:  erlang
BuildRequires:  elixir
BuildRequires:  libxslt
BuildRequires:  xmlto
BuildRequires:  python
BuildRequires:  python%{python3_pkgversion}-simplejson
BuildRequires:  zip
BuildRequires:  unzip
BuildRequires:  rsync
BuildRequires:  glibc-lang

Requires:       erlang
Requires:       elixir
Requires:       libxslt
Requires:       xmlto
Requires:       python
Requires:       python%{python3_pkgversion}-simplejson
Requires:       zip
Requires:       unzip
Requires:       rsync
Requires:       glibc-lang

%description
rabbitmq-server

%prep
%autosetup

%build
export LANG="en_US.UTF-8"
%make_build

%install
export LANG="en_US.UTF-8"
# Install mix_task_archive_deps ahead of install
mix archive.install --force %{SOURCE1}

# Unpack hex tar dependency tarball into .hex/packages/hexpm
mkdir -p /root/.hex/packages/hexpm
tar -xzf %{SOURCE2} -C /root/.hex/packages/hexpm

# Build hex archive to install from source
pushd /root/.hex/packages/hexpm
tar -xzf hex-2.0.6.tar.gz
pushd hex-2.0.6
mix archive.build
popd
popd
mv /root/.hex/packages/hexpm/hex-2.0.6/hex-2.0.6.ez ./hex-2.0.6.ez

# Install mix_task_archive_deps and hex ahead of install
mix archive.install --force %{SOURCE1}
mix archive.install --force hex-2.0.6.ez

# Make and place hex cache.ets file
mv deps/.hex/cache.erl deps/.hex/cache.erl.rmq
mv deps/.hex/cache.ets deps/.hex/cache.ets.rmq

tar -xzf %{SOURCE3} -C deps/.hex
make restore-hex-cache-ets-file
mv deps/.hex/cache.ets /root/.hex/cache.ets

mv deps/.hex/cache.erl deps/.hex/cache.erl.ven
mv deps/.hex/cache.erl.rmq deps/.hex/cache.erl
mv deps/.hex/cache.ets.rmq deps/.hex/cache.ets

# Install rabbitmq-server
%make_install PREFIX=%{_prefix} RMQ_ROOTDIR=%{_prefix}/lib/rabbitmq

install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmqctl
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmq-server
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmq-plugins
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{_sbindir}/rabbitmq-diagnostics

# Make necessary symlinks
mkdir -p %{_prefix}/lib/rabbitmq/bin
for app in rabbitmq-defaults rabbitmq-env rabbitmq-plugins rabbitmq-diagnostics rabbitmq-server rabbitmqctl ; do
	ln -s %{_prefix}/lib/rabbitmq/lib/rabbitmq_server-%{version}/sbin/${app} %{_prefix}/lib/rabbitmq/bin/${app}
done

%files
%license LICENSE LICENSE-*
%{_libdir}/rabbitmq/lib/rabbitmq_server-%{version}/*

%changelog
* Wed Jan 17 2024 Harshit Gupta <guptaharshit@microsoft.com> - 3.11.11-2
- Release bump with no changes to force a rebuild and consume new erlang build

* Tue Mar 14 2023 Sam Meluch <sammeluch@microsoft.com> - 3.11.11-1
- Original version for CBL-Mariner
- License Verified
