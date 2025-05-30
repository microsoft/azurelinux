Name:           python-flaky
Version:        3.8.1
Release:        4%{?dist}
Summary:        Plugin for pytest that automatically reruns flaky tests
License:        ASL 2.0
URL:            https://github.com/box/flaky
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://files.pythonhosted.org/packages/5b/c5/ef69119a01427204ff2db5fc8f98001087bcce719bbb94749dcd7b191365/flaky-3.8.1.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-pytest                                                       
BuildRequires:  python3-pytest-mock
BuildRequires:  python3-wheel
BuildRequires:  python3-packaging
BuildRequires:  python3-toml
BuildRequires:  python3-setuptools

%description
Flaky is a plugin for pytest that automatically reruns flaky
tests. Ideally, tests reliably pass or fail, but sometimes test fixtures must
rely on components that aren't 100% reliable. With flaky, instead of removing
those tests or marking them to @skip, they can be automatically retried.


%package -n     python3-flaky
Summary:        %{summary}

%description -n python3-flaky
Flaky is a plugin for pytest that automatically reruns flaky
tests. Ideally, tests reliably pass or fail, but sometimes test fixtures must
rely on components that aren't 100% reliable. With flaky, instead of removing
those tests or marking them to @skip, they can be automatically retried.


%prep
%autosetup -p1 -n flaky-%{version}

# Use mock from standard library:
sed -i -e 's/import mock/from unittest import mock/' \
       -e 's/from mock/from unittest.mock/' \
       test/test_*/test_*.py


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files flaky


%check
# adapted from upstream's tox.ini
%pytest -v -k 'example and not options' --doctest-modules test/test_pytest/
%pytest -v -k 'example and not options' test/test_pytest/
%pytest -v -p no:flaky test/test_pytest/test_flaky_pytest_plugin.py
%pytest -v --force-flaky --max-runs 2 test/test_pytest/test_pytest_options_example.py


%files -n python3-flaky -f %{pyproject_files}
%doc README.rst


%changelog
* Fri Feb 21 2025 Jyoti kanase <v-jykanase@microsoft.com> -  3.8.1.-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.8.1-2
- Rebuilt for Python 3.13

* Thu Mar 28 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.8.1-1
- Update to 3.8.1
- Fixes: rhbz#2268803

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.7.0-11
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.7.0-8
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 25 2021 Miro Hrončok <mhroncok@redhat.com> - 3.7.0-6
- Modernize packaging

* Mon Nov 22 2021 Charalampos Stratakis <cstratak@redhat.com> - 3.7.0-5
- Remove the dependency on the deprecated nose test runner

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.7.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 23 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.7.0-1
- Update to 3.7.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-2
- Rebuilt for Python 3.9

* Wed Mar 11 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.3-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.3-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 30 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Miro Hrončok <mhroncok@redhat.com> - 3.4.0-1
- Initial package

## END: Generated by rpmautospec
