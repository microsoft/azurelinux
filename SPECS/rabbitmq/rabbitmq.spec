%define  debug_package %{nil}
Summary:        rabbitmq-server
Name:           rabbitmq-server
Version:        3.11.9
Release:        1%{?dist}
License:        Apache-2.0 and MPL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rabbitmq.com
Source0:        https://github.com/rabbitmq/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        rabbitmq-vendor-%{version}.tar.gz
# -----------------
# steps to create the vendor tarball are in the generate-rabbitmq-tarball.sh script
# running this script will produce the rabbitmq-vendor-3.11.9.tar.gz tarball in your current directory
# ./generate-rabbitmq-tarball.sh
# -----------------
BuildRequires:  erlang
BuildRequires:  elixir
BuildRequires:  libxslt
BuildRequires:  xmlto
BuildRequires:  python
BuildRequires:  python%{python3_pkgversion}-simplejson
BuildRequires:  zip
BuildRequires:  unzip

%description
rabbitmq-server

%prep
%autosetup

%build
tar -xzf %{SOURCE1} -C deps/
%make_build

%install
%make_install

%files
%license LICENSE


%changelog
* Tue Mar 14 2023 Sam Meluch <sammeluch@microsoft.com> - 3.11.9-1
- Original version for CBL-Mariner
- License Verified
