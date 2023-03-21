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

%description
rabbitmq-server

%prep
%autosetup

%build
export LANG="en_US.UTF-8"
%make_build

%install
%make_install

%files
%license LICENSE


%changelog
* Tue Mar 14 2023 Sam Meluch <sammeluch@microsoft.com> - 3.11.11-1
- Original version for CBL-Mariner
- License Verified
