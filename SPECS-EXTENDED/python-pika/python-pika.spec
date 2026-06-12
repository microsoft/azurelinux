%bcond_without check

Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global pypi_name pika

Name:           python-%{pypi_name}
Version:        1.3.2
Release:        1%{?dist}
Summary:        AMQP 0-9-1 client library for Python
License:        BSD-3-Clause
URL:            https://github.com/pika/pika
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

%global _description %{expand:
Pika is a pure-Python implementation of the AMQP 0-9-1 protocol that
tries to stay fairly independent of the underlying network support
library.}

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%if %{with check}
%check
# Exclude the optional gevent/tornado/twisted connection adapters: those
# third-party libraries are not build dependencies, so importing those
# adapter modules would fail. pika's core only needs the stdlib.
%pyproject_check_import -e '*.gevent_connection' -e '*.tornado_connection' -e '*.twisted_connection'
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md README.rst

%changelog
* Thu Jun 11 2026 Adit Jha <aditjha@microsoft.com> - 1.3.2-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.
