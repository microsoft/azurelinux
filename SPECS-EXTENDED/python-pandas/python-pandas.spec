Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname pandas

Name:           python-%{srcname}
Version:        2.2.3
Release:        1%{?dist}
Summary:        Powerful data structures for data analysis and statistics

License:        BSD-3-Clause
URL:            https://pandas.pydata.org
# Pinned to the 2.2 series, which builds with Azure Linux's Cython 3.0.x and
# numpy 1.26 (pandas 3.x requires Cython > 3.1 and numpy >= 2.0).
Source0:        https://files.pythonhosted.org/packages/9c/d6/9f8431bacc2e19dca897724cd097b1bb224a6ad5433784a44b587c7c13af/%{srcname}-%{version}.tar.gz

# Compiled (meson-python + Cython) package. Beyond the C/C++ toolchain it needs
# the meson backend, Cython, numpy and versioneer (used by generate_version.py).
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3-meson-python
BuildRequires:  python3-pyproject-metadata
BuildRequires:  python3-packaging
BuildRequires:  python3-Cython
BuildRequires:  python3-numpy
BuildRequires:  python3-versioneer

%global _description %{expand:
pandas is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive. It is the fundamental high-level building block for doing
practical, real-world data analysis in Python.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

# Relax the strict build-tool pins to the versions Azure Linux ships and allow
# building against numpy 1.x (the resulting wheel targets this distro).
sed -i 's/"meson-python==0.13.1"/"meson-python"/' pyproject.toml
sed -i 's/"meson==1.2.1"/"meson"/' pyproject.toml
sed -i 's/"numpy>=2.0"/"numpy"/' pyproject.toml
# The system tzdata package provides the zoneinfo database, so the Python tzdata
# module is not required on Azure Linux.
sed -i '/"tzdata>=2022.7"/d' pyproject.toml

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
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 2.2.3-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
