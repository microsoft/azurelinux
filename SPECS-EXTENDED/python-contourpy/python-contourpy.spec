Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname contourpy

Name:           python-%{srcname}
Version:        1.2.1
Release:        1%{?dist}
Summary:        Python library for calculating contours of 2D quadrilateral grids

License:        BSD-3-Clause
URL:            https://github.com/contourpy/contourpy
# Pinned to 1.2.1, the last release whose C++ extension uses the 2-argument
# PYBIND11_MODULE form. Newer releases use the 3-argument (mod_gil_not_used)
# form, which requires pybind11 >= 2.13 (Azure Linux ships pybind11 2.11).
Source0:        https://files.pythonhosted.org/packages/8d/9e/e4786569b319847ffd98a8326802d5cf8a5500860dbfc2df1f0f4883ed99/%{srcname}-%{version}.tar.gz

# Compiled (meson-python/pybind11) package. %%pyproject_buildrequires pulls the
# meson-python backend, pybind11 and numpy; the C/C++ toolchain is required too.
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
BuildRequires:  python3-pybind11
BuildRequires:  python3-numpy

%global _description %{expand:
ContourPy is a Python library for calculating contours of 2D quadrilateral
grids. It is written in C++11 with a Python wrapper and is the contouring engine
used by matplotlib.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}
# Relax the pybind11 build pin (>= 2.12.0) to match the distro's 2.11.x, which
# is ABI-compatible with the 2-argument PYBIND11_MODULE used by this release.
sed -i 's/"pybind11 >= 2.12.0"/"pybind11"/' pyproject.toml

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
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 1.2.1-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
