Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Enable Python dependency generation
%{?python_enable_dependency_generator}

# Created by pyp2rpm-3.3.2
%global pypi_name pytest-flake8

%global desc \
%{name} is a plugin for pytest to leverage flake8 to automatically\
and efficiently checking for PEP8 compliance of a project.

Name:           python-%{pypi_name}
Version:        1.3.0
Release:        1%{?dist}
Summary:        Plugin for pytest to check PEP8 compliance with Flake8

License:        BSD
URL:            https://github.com/tholo/pytest-flake8
Source0:        https://github.com/coherent-oss/pytest-flake8/archive/refs/tags/v%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(flake8) >= 3.5
BuildRequires:  python3dist(pytest) >= 3.5
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%description %{desc}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{desc}

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%pyproject_wheel

%install
%pyproject_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/pytest_flake8.py
%{python3_sitelib}/pytest_flake8-0.0.0.dist-info/*

%changelog
* Mon Dec 15 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.3.0-1
- Upgrade to version 1.3.0 (license: MIT).
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.4-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.4-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Dan Radez <dradez@redhat.com> - 1.0.4-1
- update to 1.0.4

* Wed Feb 27 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-3
- Subpackage python2-pytest-flake8 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 11 2018 Neal Gompa <ngompa13@gmail.com> - 1.0.1-1
- Initial package
