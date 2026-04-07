# Needed for Python bootstrap: keep tests opt-in to avoid extra dependency cycles.
%bcond_with tests
 
Name:           python-pyproject-hooks
Version:        1.2.0
Release:        1%{?dist}
Summary:        Wrappers to call pyproject.toml-based build backend hooks
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
 
# SPDX
License:        MIT
URL:            https://pypi.org/project/pyproject_hooks/
Source0:        %{pypi_source pyproject_hooks}
 
# Upstream fix for compatibility with Python 3.15
Patch:          f230da76.patch
 
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(testpath)
%endif
BuildRequires:  python3-flit-core

 
%global _description %{expand:
This is a low-level library for calling build-backends in
pyproject.toml-based project. It provides the basic functionality
to help write tooling that generates distribution files from
Python projects.}
 
 
%description %_description
%package -n     python3-pyproject-hooks
Summary:        %{summary}
 
%description -n python3-pyproject-hooks %_description
 
%prep
%autosetup -p1 -n pyproject_hooks-%{version}
sed -i "/flake8/d" dev-requirements.txt
 
 
%generate_buildrequires
%pyproject_buildrequires %{?with_tests:dev-requirements.txt}
 
 
%build
%pyproject_wheel
 
%install
%pyproject_install
%pyproject_save_files pyproject_hooks
 
 
%check
%pyproject_check_import
%if %{with tests}
%pytest
%endif
 
 
%files -n python3-pyproject-hooks -f %{pyproject_files}
%doc README.rst
%license LICENSE
 
%changelog
* Sat Apr 4 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.2.0-1
- Initial CBL-Mariner import from Fedora 44 (license: MIT).
- License verified
