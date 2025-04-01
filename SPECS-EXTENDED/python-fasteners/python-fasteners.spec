Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond tests %{undefined rhel}
Name:           python-fasteners
Version:        0.19
Release:        1%{?dist}
Summary:        A python package that provides useful locks

License:        Apache-2.0
URL:            https://github.com/harlowja/fasteners
# We need to use the GitHub archive instead of the PyPI sdist to get tests.
Source:         %{url}/archive/%{version}/fasteners-%{version}.tar.gz

BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros            
BuildRequires:  python3-packaging
BuildRequires:  python3-requests
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-diskcache

%global common_description %{expand:
Cross platform locks for threads and processes}
 
%description %{common_description}
 
 
%package -n python3-fasteners
Summary:        A python package that provides useful locks

%description -n python3-fasteners %{common_description}
 
 
%prep
%autosetup -n fasteners-%{version}
# Omit eventlet integration tests:
#   python-eventlet fails to build with Python 3.13: AttributeError: module
#   'eventlet.green.thread' has no attribute 'start_joinable_thread'
#   https://bugzilla.redhat.com/show_bug.cgi?id=2290561
sed -r 's/^eventlet\b/# &/' requirements-test.txt |
  tee requirements-test-filtered.txt
 
%generate_buildrequires
%pyproject_buildrequires %{?with_tests:requirements-test-filtered.txt}
 
%build
%pyproject_wheel
 
%install
%pyproject_install

%pyproject_save_files fasteners
 
%check
%if %{with tests}
# See notes in %%prep:
ignore="${ignore-} --ignore=tests/test_eventlet.py"
 

%pytest ${ignore-} -v
%else
%pyproject_check_import -e 'fasteners.pywin32*'
%endif
 
 
%files -n python3-fasteners -f %{pyproject_files}
%doc CHANGELOG.md
%doc README.md
 
%changelog
* Tue Mar 25 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 0.19-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Mon Jul 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19-9
- Omit eventlet integration tests

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Python Maint <python-maint@redhat.com> - 0.19-7
- Finish Python 3.13 bootstrap

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.19-6
- Bootstrap for Python 3.13

* Mon May 20 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19-5
- Drop -doc Provides/Obsoletes for historical upgrade path

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19-2
- Assert that %%pyproject_files contains a license file

* Sat Sep 30 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19-1
- Update to 0.19 (close RHBZ#2240009)

* Sat Sep 30 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.18-10
- Restore python-diskcache test dependency since it was unretired

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.18-8
- Cleaner build conditional for tests

* Fri Jul 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.18-7
- Use new (rpm 4.17.1+) bcond style

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.18-6
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.18-5
- Bootstrap for Python 3.12

* Fri May 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.18-3
- Disable tests by default in RHEL builds

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.18-1
- Update to 0.18 (close RHBZ#2126965)
- The separate -doc subpackage is dropped since upstream switched from
  sphinx to mkdocs

* Thu Sep 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-7
- Update License to SPDX

* Mon Aug 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-6
- Parallelize sphinx-build

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-4
- Fix extra newline in description

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.17.3-3
- Rebuilt for Python 3.11

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-2
- Build Sphinx docs as PDF in a new -doc subpackage

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-1
- Update to 0.17.3 (close RHBZ#1712140)

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17-4
- Use pyproject-rpm-macros

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17-3
- Drop EPEL8 conditionals

* Tue May 03 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17-1
- Update to 0.17

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-26
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.14.1-25
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-22
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.14.1-21
- Fix conditionals.

* Mon Jan 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.14.1-19
- Disable tests on EL-8

* Mon Sep 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-18
- Subpackage python2-fasteners has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-17
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-13
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.14.1-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.14.1-10
- Fix monotonic req on py3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-7
- Rebuild for Python 3.6

* Mon Aug 29 2016 Matthias Runge <mrunge@redhat.com> - 0.14.1-6
- Use time.monotonic if available (Python3 > 3.2)
  patch thanks to Ville Skyttä (rhbz#1294335)
- modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar 16 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.14.1-4
- Spec cleanups

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Matthias Runge <mrunge@redhat.com> - 0.14.1-2
- update to 0.14.1 (rhbz#1281772)
- fix python_provide

* Mon Nov 16 2015 Matthias Runge <mrunge@redhat.com> - 0.13.0-3
- Fix build

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Aug 28 2015 Matthias Runge <mrunge@redhat.com> - 0.13.0-1
- update to 0.13.0 (rhbz#1256153)

* Mon Jun 22 2015 Matthias Runge <mrunge@redhat.com> - 0.12.0-1
- update to 0.12.0 (rhbz#1234253)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Matthias Runge <mrunge@redhat.com> - 0.9.0-2
- switch to github sourcecode, license included
- add tests, fix conditionals for python3

* Thu Jun 11 2015 Matthias Runge <mrunge@redhat.com> - 0.9.0-1
- Initial package. (rhbz#1230548)
