# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# RHEL does not include all the test dependencies
%bcond tests %{undefined rhel}

%global srcname requests-ftp

Name:           python-%{srcname}
Version:        0.3.1
Release: 43%{?dist}
Summary:        FTP transport adapter for python-requests

License:        Apache-2.0
URL:            https://github.com/Lukasa/requests-ftp

# the last pypi release was 0.3.1, from commit 20ce5bf5388ae9b9edfdd9bf6d381a399e5bcad0 but without test data
%global commit d959118dbfc1f04c9726dfff48d5a2a64c1a01f2
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Source0:        https://github.com/Lukasa/%{srcname}/archive/%{commit}/%{srcname}-%{shortcommit}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

# Remove use of the cgi module, which is only used to implement STOR
Patch6:         0001-Remove-use-of-the-cgi-module.patch

Patch7:         0001-Relax-the-test-requirement-versions.patch
Patch8:         0001-Add-explicit-schemes-to-the-proxy-URLs.patch

%description
Requests-FTP is an implementation of a very stupid FTP transport adapter for
use with the awesome Requests Python library.

%package -n python3-%{srcname}
Summary:        FTP transport adapter for python3-requests

%description -n python3-requests-ftp
Requests-FTP is an implementation of a very stupid FTP transport adapter for
use with the awesome Requests Python library.

This is the Python 3 version of the transport adapter module.

%prep
%autosetup -n %{srcname}-%{commit} -p1

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:test_requirements.txt}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files requests_ftp

%check
%pyproject_check_import
%if %{with tests}
%pytest tests
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.3.1-42
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.3.1-41
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.3.1-40
- Avoid tox dependency

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul  8 2025 David Shea <reallylongword@gmail.com> - 0.3.1-38
- Switch to pyproject macros
- Remove python2 support
- Switch to github for the upstream source
- Run the tests in %%check

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.3.1-37
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.3.1-34
- Rebuilt for Python 3.13

* Mon Jan 29 2024 David Shea <reallylongword@gmail.com> - 0.3.1-33
- Migrate to SPDX license

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct  2 2023 David Shea <reallylongword@gmail.com> - 0.3.1-30
- Remove use of the cgi module

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.1-28
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3.1-25
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.3.1-22
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-19
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-17
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-16
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 2  2018 David Shea <dshea@redhat.com> - 0.3.1-13
- Fix handling of multi-line FTP responses

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-11
- Rebuilt for Python 3.7

* Tue Apr 24 2018 David Shea <dshea@redhat.com> - 0.3.1-10
- Conditionalize the python2 and python3 builds

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.3.1-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 0.3.1-2
- Rebuilt for Python3.5 rebuild

* Mon Sep 14 2015 David Shea <dshea@redhat.com> - 0.3.1-1
- Update to requests-ftp-0.3.1, which fixes the LIST command
- Switch to the new python packaging guidelines, which renames python-requests-ftp to python2-requests-ftp

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 David Shea <dshea@redhat.com> - 0.3.0-1
- New upstream version 0.3.0
- Adds proxy support and improves compatibility with HTTP requests

* Thu Mar 12 2015 David Shea <dshea@redhat.com> - 0.2.0-1
- Initial package
