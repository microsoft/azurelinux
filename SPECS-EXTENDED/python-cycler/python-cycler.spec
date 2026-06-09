Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname cycler

Name:           python-%{srcname}
Version:        0.12.1
Release:        1%{?dist}
Summary:        Composable style cycles

License:        BSD-3-Clause
URL:            https://github.com/matplotlib/cycler
Source0:        https://files.pythonhosted.org/packages/a9/95/a3dbbb5028f35eafb79008e7522a75244477d2838f38cbb722248dabc2a8/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
cycler provides a small, composable abstraction for "style cycles" - cycling
through a set of property values (such as colours and line styles) when drawing
repeated elements. It is a core dependency of matplotlib.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

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
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 0.12.1-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
