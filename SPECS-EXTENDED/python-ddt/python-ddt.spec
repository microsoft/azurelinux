%global srcname ddt
%global common_description %{expand:
DDT (Data-Driven Tests) allows you to multiply one test case by running it with
different test data, and make it appear as multiple test cases.}

%bcond_without  tests


Name:           python-%{srcname}
Version:        1.6.0
Release:        10%{?dist}
Summary:        Python library to multiply test cases
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/datadriventests/ddt
Source:         %{pypi_source}#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires: 	python3-pip
BuildRequires: 	python3-wheel
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-PyYAML
BuildRequires:  python3-six
%endif


%description %{common_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname} %{common_description}


%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%if %{with tests}
%pytest
%else
%pyproject_check_import
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md


%changelog
* Tue May 06 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.6.0-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- Added BR on `python-PyYAML` for tests
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.6.0-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.6.0-4
- Rebuilt for Python 3.12

* Wed Jun 07 2023 Jan Friesse <jfriesse@redhat.com> - 1.6.0-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 22 2022 Joel Capitao <jcapitao@redhat.com> - 1.6.0-1
- Latest upstream, resolves: rhbz#2089550

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.4-2
- Rebuilt for Python 3.11

* Thu Apr 21 2022 Carl George <carl@george.computer> - 1.4.4-1
- Latest upstream, resolves: rhbz#1938360
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Stephen Gallagher <sgallagh@redhat.com> - 1.4.2-3
- Fix missing %%dist

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.2-2
- Rebuilt for Python 3.10

* Wed Apr 21 2021 Joel Capitao <jcapitao@redhat.com> - 1.4.2-1
- Latest upstream rhbz#1938360

* Fri Feb 05 2021 Carl George <carl@george.computer> - 1.4.1-5
- Fix FTBFS with PyYAML 5.4.1 rhbz#1917364

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-3
- BuildRequire six explicitly, it's used in tests

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 06 2020 Carl George <carl@george.computer> - 1.4.1-1
- Latest upstream rhbz#1778594

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Carl George <carl@george.computer> - 1.2.1-5
- Add patch0 to use mock from the standard library

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 07 2019 Carl George <carl@george.computer> - 1.2.1-1
- Latest upstream
- Disable py2 subpackage on f30+ and el8+

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-2
- Rebuilt for Python 3.7

* Mon May 14 2018 Carl George <carl@george.computer> - 1.1.3-1
- Latest upstream

* Wed Mar 07 2018 Carl George <carl@george.computer> - 1.1.2-1
- Latest upstream
- Enable EPEL python3 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1.1-2
- Add EPEL7 conditionals

* Wed Dec 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1.1-1
- Update to 1.1.1
- Modernize spec

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May 20 2016 Carl George <carl.george@rackspace.com> - 1.0.2-1
- Latest upstream

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 05 2015 Carl George <carl.george@rackspace.com> - 1.0.1-2
- Remove coverage build dependency
- Change python3 control macros to a bcond macro
- Add bcond macro to optionally require explicit python2 names

* Thu Nov 19 2015 Carl George <carl.george@rackspace.com> - 1.0.1-1
- Latest upstream

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Sep 01 2015 Carl George <carl.george@rackspace.com> - 1.0.0-3
- Update to new packaging guidelines

* Mon Jul 20 2015 Carl George <carl.george@rackspace.com> - 1.0.0-2
- Remove separate py3 build directory
- Update summary and description
- Use a common license and documentation directories between PY2/3 packages

* Thu Jul 16 2015 Carl George <carl.george@rackspace.com> - 1.0.0-1
- Initial spec file
