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

BuildRequires:  elixir
BuildRequires:  erlang
BuildRequires:  glibc-lang
BuildRequires:  libxslt
BuildRequires:  python
BuildRequires:  python%{python3_pkgversion}-simplejson
BuildRequires:  rsync
BuildRequires:  unzip
BuildRequires:  xmlto
BuildRequires:  zip

Requires:       elixir
Requires:       erlang
Requires:       glibc-lang
Requires:       libxslt
Requires:       python
Requires:       python%{python3_pkgversion}-simplejson
Requires:       rsync
Requires:       unzip
Requires:       xmlto
Requires:       zip

%description
RabbitMQ is a reliable and mature messaging and streaming broker, which is easy to deploy on cloud environments, on-premises, and on your local machine.

%prep
%autosetup

%build
export LANG="en_US.UTF-8"
# Running with -j1 to solve a race condition during build with a patch added to erlang to resolve
# an arm64 build error related to heap allocation
%make_build -j1

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
