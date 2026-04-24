# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pytest-isort

Name:           python-%{pypi_name}
Version:        4.0.0
Release: 4%{?dist}
Summary:        Pytest plugin to check import ordering using isort

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            http://github.com/moccu/pytest-isort/
Source0:        %{pypi_source}
BuildArch:      noarch

%description
py.test plugin to check import ordering using isort.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-isort
BuildRequires:  python3-pytest
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
py.test plugin to check import ordering using isort.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%check
%{pytest} -v tests

%files -n python3-%{pypi_name}
%license LICENSE.rst
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/pytest_isort/
%{python3_sitelib}/*.dist-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Jul 29 2025 Federico Pellegrin <fede@evolware.org> - 4.0.0-1
- Bump to 4.0.0

* Tue Jul 29 2025 Federico Pellegrin <fede@evolware.org> - 3.0.0-15
- Use new Python macros in spec file (rhbz#2378111)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.0.0-13
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 3.0.0-11
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.0.0-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.0.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.0-2
- Rebuilt for Python 3.11

* Thu Mar 03 2022 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.0-1
- Update to latest upstream release 3.0.0 (closes rhbz#2059965)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 26 2021 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.0-1
- Update to latest upstream release 2.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.0-1
- Update to latest upstream release 1.2.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.1.0-1
- Update to latest upstream release 1.1.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.1-2
- Update removal of test files (rhbz#1787443)

* Thu Jan 02 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.1-1
- Initial package for Fedora
