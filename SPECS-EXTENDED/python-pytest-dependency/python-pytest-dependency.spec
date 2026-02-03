%global srcname pytest-dependency

Name:           python-%{srcname}
Summary:        Pytest plugin to manage dependencies of tests
Version:        0.6.0
Release:        8%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        Apache-2.0
URL:            https://github.com/RKrahl/pytest-dependency
Source:         %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-devel

%global _description %{expand:
This module is a plugin for the popular Python testing framework pytest.
It manages dependencies of tests: you may mark some tests as dependent from
other tests. These tests will then be skipped if any of the dependencies did
fail or has been skipped.}

%description %_description

%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pytest_dependency

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGES.rst

%changelog
* Fri Dec 26 2025 Aditya Singh <v-aditysing@microsoft.com> - 0.6.0-8
- Initial Azure Linux import from Fedora 44 (license: MIT).
- License verified. 

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.6.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.6.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.14

* Sat Apr 19 2025 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.6.0-3
- Fix FTBFS due to missing tox configuration - Closes rhbz#2354118

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 26 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.6.0-1
- Initial package - Closes rhbz#2283312
