# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pytest-forked

Name:           python-%{pypi_name}
Version:        1.6.0
Release: 14%{?dist}
Summary:        py.test plugin for running tests in isolated forked subprocesses

License:        MIT
URL:            https://github.com/pytest-dev/pytest-forked
Source0:        %{pypi_source}

# compatibility with pytest 8
Patch:          https://github.com/pytest-dev/pytest-forked/commit/b2742322d3.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
The pytest-forked plugin extends py.test by adding an option to run tests in
isolated forked subprocesses. This is useful if you have tests involving C or
C++ libraries that might crash the process. To use the plugin, simply use the
--forked argument when invoking py.test.}

%description %_description

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%check
%pytest


%files -n python3-%{pypi_name}
%doc example/boxed.txt README.rst
%license LICENSE
%{python3_sitelib}/pytest_forked*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.6.0-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.6.0-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.6.0-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 05 2024 Scott Talbert <swt@techie.net> - 1.6.0-8
- Update License tag to use SPDX identifiers

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.6.0-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.6.0-2
- Rebuilt for Python 3.12

* Mon Feb 13 2023 Scott Talbert <swt@techie.net> - 1.6.0-1
- Update to new upstream release 1.6.0 (#2169236)
- Modernize python packaging

* Sun Feb 12 2023 Scott Talbert <swt@techie.net> - 1.5.0-1
- Update to new upstream release 1.5.0 (#2169197)

* Tue Jan 24 2023 Scott Talbert <swt@techie.net> - 1.4.0-6
- Fix FTBFS with pytest 7.2.0+

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 11 2021 Scott Talbert <swt@techie.net> - 1.4.0-1
- Update to new upstream release (#2031175)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.3.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Scott Talbert <swt@techie.net> - 1.3.0-1
- Update to new upstream release 1.3.0 (#1861096)

* Thu Jun 25 2020 Scott Talbert <swt@techie.net> - 1.2.0-1
- Update to new upstream release 1.2.0 (#1851035)

* Wed Jun 24 2020 Scott Talbert <swt@techie.net> - 1.1.1-6
- Modernize Python packaging; BR setuptools

* Fri May 29 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.1.1-5
- Fix pytest 5 compatibility

* Fri May 29 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.1.1-4
- Drop manual requires on python3-pytest to support usage with pytest4 compat package

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 10 2019 Scott Talbert <swt@techie.net> - 1.1.1-1
- Update to new upstream release 1.1.1 (#1760556)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-4
- Rebuilt for Python 3.8

* Fri Aug 09 2019 Scott Talbert <swt@techie.net> - 1.0.2-3
- Remove Python 2 subpackages (#1739658)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Scott Talbert <swt@techie.net> - 1.0.2-1
- New upstream release 1.0.2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 12 2019 Scott Talbert <swt@techie.net> - 1.0.1-1
- New upstream release 1.0.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 17 2017 Scott Talbert <swt@techie.net> - 0.2-2
- Updated to use py[23]dist macros for BR and R

* Thu Aug 10 2017 Scott Talbert <swt@techie.net> - 0.2-1
- Initial package.
