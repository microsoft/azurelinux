%if %{defined el8}
# Disable tests on epel8 - dependencies dont exist.
%bcond_with tests
%else
%bcond_without tests
%endif

Name:           python-requests-mock
Version:        1.12.1
Release:        1%{?dist}
Summary:        Mock out responses from the requests package
License:        Apache-2.0
URL:            https://requests-mock.readthedocs.io/
Source:         %{pypi_source requests-mock}
Patch:          0003-Allow-skipping-purl-tests-if-it-is-not-present.patch
BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-requests-futures
%endif

%global _description %{expand:
requests-mock provides a building block to stub out the HTTP requests portions
of your testing code. You should checkout the docs for more information.}


%description %_description


%package -n python3-requests-mock
Summary:        %{summary}


%description -n python3-requests-mock %_description


%prep
%autosetup -n requests-mock-%{version} -p 1


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-x fixture}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files requests_mock


%check
%if %{with tests}
%pytest -v tests/pytest
%else
%pyproject_check_import -e requests_mock.contrib.fixture
%endif


%files -n python3-requests-mock -f %{pyproject_files}
%doc README.rst


%changelog
* Wed Sep 25 2024 Christoph Erhardt <fedora@sicherha.de> - 1.12.1-1
- Update to 1.12.1 (#2213553)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.10.0-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.10.0-4
- Rebuilt for Python 3.12

* Wed Feb 15 2023 Carl George <carl@george.computer> - 1.10.0-3
- Convert to pyproject macros

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 15 2022 Joel Capitao <jcapitao@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.9.3-2
- Rebuilt for Python 3.11

* Wed Feb 23 2022 Karolina Kula <kkula@redhat.com> - 1.9.3-1
- Update to 1.9.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Joel Capitao <jcapitao@redhat.com> - 1.8.0-1
- Update to 1.8.0
- Remove Python 2 subpackage

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Jamie Lennox <jamielennox@gmail.com> - 1.7.0-1
- Updated to upstream 1.7.0
- Conditionalized tests for EPEL8 not having required dependencies
- Add patch to skip purl tests as dependency not present.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.2-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.2-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 27 2019 Yatin Karel <ykarel@redhat.com> - 1.5.2-3
- Disable python2 build in Fedora and EL > 7

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 21 2018 Jamie Lennox <jamielennox@gmail.com> - 1.5.2-1
- Update to upstream 1.5.2.
- Fix bug introduced in 1.5.1

* Sat Jul 21 2018 Jamie Lennox <jamielennox@gmail.com> - 1.5.1-1
- Update to upstream 1.5.1.
- Fixes py.test plugin with py.test<3 as in EPEL.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-2
- Rebuilt for Python 3.7

* Sat Jun 23 2018 Jamie Lennox <jamielennox@gmail.com>- 1.5.0-1
- Update to upstream 1.5.0.

* Fri Jun 22 2018 Carl George <carl@george.computer> - 1.3.0-6
- EPEL compatibility

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-5
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.3.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.0-2
- Fix creation of python2- subpackage

* Fri Nov 17 2017 Alfredo Moralejo <amoralej@redhat.com> - 1.3.0-1
- Update to upstream 1.3.0. Required for OpenStack packages.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Jamie Lennox <jamielennox@gmail.com> - 1.2.0-1
- Upstream 1.2.0. Fixes testing bug preventing package rebuilding.

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rebuild for Python 3.6

* Mon Nov 14 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.0-1
- Upstream 1.1.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 27 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-1
- Upstream 1.0.0 (RHBZ#1334354)
- Use pypi.io for SourceURL
- Fix unversioned python macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 4 2015 Jamie Lennox <jamielennox@gmail.com> - 0.7.0-1
- Update package to new version.
- Add python2 subpackage for new python packaging guidelines.
- Redo patch1 to still apply.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 6 2015 Jamie Lennox <jamielennox@redhat.com> - 0.6.0-1
- Update package to new version

* Tue Sep 2 2014 Jamie Lennox <jamielennox@redhat.com> - 0.5.1-2
- Removed packaged egg-info to force rebuild.
- Removed unneeded CFLAGS from build commands.

* Thu Aug 28 2014 Jamie Lennox <jamielennox@redhat.com> - 0.5.1-1
- Initial Package.
