%define  debug_package %{nil}
Summary:        rabbitmq-server
Name:           rabbitmq-server
Version:        3.13.0
Release:        1%{?dist}
License:        Apache-2.0 and MPL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://rabbitmq.com
Source0:        https://github.com/rabbitmq/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

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
* Thu Mar 28 2024 Sam Meluch <sammeluch@microsoft.com> - 3.13.0-1
- Upgrade rabbitmq-server to version 3.13.0 for Azure Linux 3.0
- Remove now unused vendor tarballs

* Tue Mar 14 2023 Sam Meluch <sammeluch@microsoft.com> - 3.11.11-1
- Original version for CBL-Mariner
- License Verified
