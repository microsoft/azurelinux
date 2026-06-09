Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname colorlog
%global gitname python-colorlog

Name:           python-%{srcname}
Version:        6.10.1
Release:        1%{?dist}
Summary:        Add colours to the output of Python's logging module

License:        MIT
URL:            https://github.com/borntyping/python-colorlog
Source0:        https://github.com/borntyping/%{gitname}/archive/refs/tags/v%{version}.tar.gz#/%{gitname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
Colorlog provides a formatter for Python's standard logging module that adds
colour to log output using ANSI escape codes. It is a drop-in formatter that
colours each record by its log level and supports custom colours, secondary
log colours, and integration with libraries such as colorama for cross-platform
terminal support.}

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
%doc README.md

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 6.10.1-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
