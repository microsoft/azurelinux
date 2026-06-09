Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname knack
%global gitname knack

Name:           python-%{srcname}
Version:        0.14.0
Release:        1%{?dist}
Summary:        A Command-Line Interface framework

License:        MIT
URL:            https://github.com/microsoft/knack
Source0:        https://github.com/microsoft/%{gitname}/archive/refs/tags/v%{version}.tar.gz#/%{gitname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
Knack is a Command-Line Interface (CLI) framework. It provides the building
blocks for creating CLIs: a command loader and dispatcher, argument and command
parsing, output formatting (JSON, table, TSV), configuration, prompting, and
help generation. It is the framework that underpins the Azure CLI.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{gitname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 0.14.0-1
- Original version for Azure Linux.
- License verified.
