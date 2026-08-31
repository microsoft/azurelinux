# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enable tests by default.
%bcond_without tests

%global pypi_name pytest-aiohttp

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        5%{?dist}
Summary:        Pytest plugin for aiohttp support

License:        Apache-2.0
URL:            https://github.com/aio-libs/pytest-aiohttp/
Source0:        %{pypi_source pytest_aiohttp}
BuildArch:      noarch

%description
The library allows to use aiohttp pytest plugin without need for implicitly
loading it like pytest_plugins = 'aiohttp.pytest_plugin'.

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
The library allows to use aiohttp pytest plugin without need for implicitly
loading it like pytest_plugins = 'aiohttp.pytest_plugin'.

%prep
%autosetup -n pytest_aiohttp-%{version} -p1

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_install
%pyproject_save_files pytest_aiohttp


%if %{with tests}
%check
%pytest -W ignore::DeprecationWarning
%endif

%files -n python3-%{pypi_name}  -f %{pyproject_files}
%doc CHANGES.rst README.rst
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.1.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.1.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.14

* Tue Apr 01 2025 Fabian Affolter <mail@fabian-affolter.ch> - 1.1.0-1
- Update to latest upstream release (closes rhbz#2341772)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0.5-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.5-2
- Rebuilt for Python 3.13

* Sat Feb 03 2024 Fabian Affolter <mail@fabian-affolter.ch> - 1.0.5-1
- Update to latest upstream release 1.0.5 (closes rhbz#2237729)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 1.0.4-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.0.4-3
- Rebuilt for Python 3.11

* Thu Apr 28 2022 Major Hayden <major@mhtx.net> - 1.0.4-2
- Update to use pyproject-rpm-macros.

* Thu Mar 03 2022 Fabian Affolter <mail@fabian-affolter.ch> - 1.0.4-1
- Update to latest upstream release 1.0.4 (closes rhbz#2054997)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3.0-12
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.0-9
- Add python3-setuptools as BR

* Fri Jun 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.0-8
- Add python3-setuptools as BR

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.0-2
- Change source (rhbz#1719010)

* Mon Jun 10 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.0-1
- Initial package for Fedora
