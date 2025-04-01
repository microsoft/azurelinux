%global srcname conda-libmamba-solver
%global _description %{expand:
conda-libmamba-solver is a new solver for the conda package manager which
uses the solver from the mamba project behind the scenes, while carefully
implementing conda's functionality and expected behaviors on top. The
library used by mamba to do the heavy-lifting is called libsolv.}
Summary:        The libmamba based solver for conda
Name:           python-%{srcname}
Version:        24.9.0
Release:        3%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/conda/conda-libmamba-solver
Source:         %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-pip
BuildRequires:  python3-pluggy
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-trove-classifiers
BuildArch:      noarch

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -p1 -n %{srcname}-%{version}
sed -i -e '/tool.hatch.version/afallback-version = "%{version}"' pyproject.toml
sed -i -e '/doctest/d' -e '/reruns/d' pyproject.toml



%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files conda_libmamba_solver


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.*
%license %{python3_sitelib}/conda_libmamba_solver-%{version}.dist-info/licenses/LICENSE
%license %{python3_sitelib}/conda_libmamba_solver-%{version}.dist-info/licenses/AUTHORS.md

%changelog
* Tue Apr 01 2025 Riken Maharjan <rmaharjan@microsoft.com> - 24.9.0-3
- Initial Azure Linux import from Fedora 42 (license: MIT)
- License Verified

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 18 2024 Orion Poplawski <orion@nwra.com> - 24.9.0-1
- Update to 24.9.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 23.11.1-5
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 20 2023 Karolina Surma <ksurma@redhat.com> - 23.11.1-2
- Conditionalize test run to avoid circular dependency on conda

* Sat Dec 02 2023 Orion Poplawski <orion@nwra.com> - 23.11.1-1
- Initial Fedora package
