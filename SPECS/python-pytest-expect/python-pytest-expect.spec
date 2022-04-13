%global pypi_name pytest-expect

Summary:        py.test plugin to store test expectations and mark tests based on them
Name:           python-%{pypi_name}
Version:        1.1.0
Release:        8%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/gsnedders/pytest-expect
Source0:        %{pypi_source}
Source1:        %{url}/raw/%{version}/LICENSE

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%?python_enable_dependency_generator

%description
A py.test plugin that stores test expectations by saving the set of failing
tests, allowing them to be marked as xfail when running them in future.
The tests expectations are stored such that they can be distributed alongside
the tests.

%package -n     python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}

%description -n python3-%{pypi_name}
A py.test plugin that stores test expectations by saving the set of failing
tests, allowing them to be marked as xfail when running them in future.
The tests expectations are stored such that they can be distributed alongside
the tests.

%prep
%autosetup -n %{pypi_name}-%{version}
cp -p %{SOURCE1} .

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/pytest_expect
%{python3_sitelib}/pytest_expect-%{version}-py?.?.egg-info

%changelog
* Fri Apr 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-8
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 20 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-1
- Initial package
