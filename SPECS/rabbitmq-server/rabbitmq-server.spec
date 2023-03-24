%define  debug_package %{nil}
Summary:        rabbitmq-server
Name:           rabbitmq-server
Version:        3.11.11
Release:        1%{?dist}
License:        Apache-2.0 and MPL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rabbitmq.com
Source0:        https://github.com/rabbitmq/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:        https://github.com/rabbitmq/mix_task_archive_deps/releases/download/1.0.0/mix_task_archive_deps-1.0.0.ez
Source2:        rabbitmq-server-hex-vendor-%{version}.tar.gz
Source3:        rabbitmq-server-hex-cache-%{version}.tar.gz

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

# install hex archive with mix and fill out hex cache ahead of build
tar -xzf %{SOURCE2} -C deps/.hex/packages/hexpm
pushd deps/.hex/packages/hexpm
tar -xzf hex-2.0.6.tar.gz
pushd hex-2.0.6
mix archive.build
mix archive.install --force hex-2.0.6.ez
popd
rm -r hex-2.0.6
popd

# replace rabbitmq-server cache.erl file with our own to support the install-time dependencies
tar -xzf %{SOURCE3} -C deps/.hex
rm deps/.hex/cache.ets
make restore-hex-cache-ets-file

mkdir -p /root/.hex
cp deps/.hex/cache.ets /root/.hex/cache.ets

%make_build

%install
export LANG="en_US.UTF-8"
# install mix_task_archive_deps ahead of install
mix archive.install --force %{SOURCE1}



# install rabbitmq-server
%make_install

%files
%license LICENSE


%changelog
* Tue Mar 14 2023 Sam Meluch <sammeluch@microsoft.com> - 3.11.11-1
- Original version for CBL-Mariner
- License Verified
