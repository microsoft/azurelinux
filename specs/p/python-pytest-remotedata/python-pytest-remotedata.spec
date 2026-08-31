# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname pytest-remotedata
%global sum Pytest plugin for controlling remote data access

Name:           python-%{srcname}
Version:        0.4.1
Release:        10%{?dist}
Summary:        %{sum}

License:        BSD-3-Clause
URL:            https://github.com/astropy/pytest-remotedata
Source0:        %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
This package provides a plugin for the pytest framework that allows developers
to control unit tests that require access to data from the internet. 

Many software packages provide features that require access to data from the
internet. These features need to be tested, but unit tests that access the
internet can dominate the overall runtime of a test suite. The pytest-remotedata
plugin allows developers to indicate which unit tests require access to the
internet, and to control when and whether such tests should execute as part of
any given run of the test suite.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{sum}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pytest_remotedata

%check
# Deselect tests that require internet
%pytest \
--deselect "test_strict_with_decorator.py::test_internet_access" \
--deselect "tests/test_strict_check.py::test_default_behavior" \
--deselect "tests/test_strict_check.py::test_strict_with_decorator[any]"


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.rst
%doc CHANGES.rst README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.4.1-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.4.1-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.4.1-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.4.1-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 31 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 0.4.1-1
- New upstream source 0.4.1
- SPDX migration, license is BSD-3-Clause
- Run tests

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.3-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3.3-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 31 2021 Christian Dersch <lupinix@fedoraproject.org> - 0.3.3-1
- new version

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3.2-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Christian Dersch <lupinix@fedoraproject.org> - 0.3.2-1
- new version

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 29 2019 Christian Dersch <lupinix@fedoraproject.org> - 0.3.1-1
- new version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 24 2018 Christian Dersch <lupinix@fedoraproject.org> - 0.3.0-1
- new version

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-2
- Rebuilt for Python 3.7

* Sat Mar 17 2018 Christian Dersch <lupinix@mailbox.org> - 0.2.0-1
- initial packaging effort

