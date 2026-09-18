# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Created by pyp2rpm-3.3.2
%global pypi_name portend
# theres a dependency resolution issue with
# sphinx to build docs. Turning it off for now
%global with_docs 0
%{?python_enable_dependency_generator}

Name:           python-%{pypi_name}
Version:        3.2.0
Release:        11%{?dist}
Summary:        TCP port monitoring utilities

License:        MIT
URL:            https://github.com/jaraco/portend
Source0:        %{pypi_source}
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
%generate_buildrequires
%pyproject_buildrequires

%description
 por·tend pôrˈtend/ be a sign or warning that (something, especially something
momentous or calamitous) is likely to happen.

%package -n python3-%{pypi_name}
Summary:        portend documentation

%description -n python3-%{pypi_name}
 por·tend pôrˈtend/ be a sign or warning that (something, especially something
momentous or calamitous) is likely to happen.

%if 0%{?with_docs}
%package -n python-%{pypi_name}-doc
Summary:        portend documentation

BuildRequires:  python3dist(jaraco-packaging) >= 3.2
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(rst-linker) >= 1.9
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(tox)
BuildRequires:  python3-more-itertools

%description -n python-%{pypi_name}-doc
Documentation for portend
%endif

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%if 0%{?with_docs}
# generate html docs 
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
%if 0%{?el8}
# disable flake8 in the tests, need a newer version of pytest (3.5) which is not
# available on EL8, and is pulled in by python-pytest-flake8.
sed -i 's/ --flake8//' pytest.ini
%endif
LANG=C.utf-8 %{__python3} -m pytest --ignore=build

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info

%if 0%{?with_docs}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.2.0-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.2.0-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.2.0-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.2.0-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Dan Radez <dradez@redhat.com> - 3.2.0-1
- update to 3.2.0 rhbz#2218397

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 3.1.0-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.1.0-6
- Rebuilt for Python 3.11

* Mon Apr 04 2022 Dan Radez <dradez@redhat.com> - 3.1.0-5
- Turning off docs build. There's an issue with sphinx deps resolution
- switching to pyproject macros
- Fixes: rhbz#2069669

* Wed Feb 09 2022 Dan Radez <dradez@redhat.com> - 3.1.0-3
- Don't remove egginfo

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Dan radez <dradez@redhat.com> - 3.1.0-1
- update to 3.1.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.7.1-2
- Rebuilt for Python 3.10

* Mon Feb 15 2021 Dan radez <dradez@redhat.com> - 2.7.1-1
- update to 2.7.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Dan Radez <dradez@redhat.com> - 2.7.0-1
- update to 2.7

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.6-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Dan Radez <dradez@redhat.com> - 2.6-1
- update to 2.6
- reenable flake8
- add coverage build dep

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Dan Radez <dradez@redhat.com> - 2.5-1
- Update to 2.5

* Tue Apr 02 2019 Dan Radez <dradez@redhat.com> - 2.3-1
- Initial package.
