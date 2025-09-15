%global pypi_name pytest-subtests

Name:           python-%{pypi_name}
Version:        0.12.1
Release:        4%{?dist}
Summary:        Support for unittest subTest() and subtests fixture

# SPDX
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/pytest-dev/pytest-subtests
Source0:        https://files.pythonhosted.org/packages/source/p/pytest-subtests/pytest-subtests-0.12.1.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
pytest-subtests unittest subTest() support and subtests fixture.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires: 	python3-wheel
BuildRequires: 	python3-pip
BuildRequires: 	python3-setuptools_scm

%{?python_provide:%python_provide python3-%{pypi_name}}
 
%description -n python3-%{pypi_name}
pytest-subtests unittest subTest() support and subtests fixture.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pytest_subtests

%check
# https://github.com/pytest-dev/pytest-subtests/issues/21
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{python3} -m pytest -v tests \
  -k "not TestFixture and not TestCapture and not test_simple_terminal"

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc CHANGELOG.rst README.rst
%license LICENSE

%changelog
* Thu Feb 20 2025 Akhila Guruju <v-guakhila@microsoft.com> - 0.12.1-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
- Added `BuildRequires: python3-setuptools_scm` to fix build

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.12.1-2
- Rebuilt for Python 3.13

* Mon Apr 08 2024 Fabian Affolter <mail@fabian-affolter.ch> - 0.12.1
- Update to latest upstream release (closes rhbz#2196751, closes rhbz#2203842)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.10.0-2
- Rebuilt for Python 3.12

* Mon Mar 27 2023 Christian Heimes <cheimes@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.5.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 25 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.0-1
- Update to latest upstream release 0.5.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.4.0-2
- Rebuilt for Python 3.10

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 0.4.0-1
- Update to 0.4 (#1925972)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.1-1
- Update to latest upstream release 0.3.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Rebuilt for Python 3.9

* Mon Mar 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.0-1
- Initial package for Fedora
