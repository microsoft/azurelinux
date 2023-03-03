# what it's called on pypi
%global srcname ddt
# what it's imported as
%global libname %{srcname}
# name of egg info directory
%global eggname %{srcname}
# package name fragment
%global pkgname %{srcname}

%global common_description %{expand:
DDT (Data-Driven Tests) allows you to multiply one test case by running it with
different test data, and make it appear as multiple test cases. It is used in
combination with other testing frameworks like unittest and nose.}

%bcond_without  tests

Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           python-%{pkgname}
Version:        1.4.2
Release:        6%{?dist}
Summary:        Python library to multiply test cases
License:        MIT
URL:            https://github.com/datadriventests/ddt
Source0:        %pypi_source
BuildArch:      noarch


%description %{common_description}


%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
%if %{with tests}
BuildRequires:  %{py3_dist pytest pyyaml six}
%endif
%{?python_provide:%python_provide python3-%{pkgname}}


%description -n python3-%{pkgname} %{common_description}


%prep
%autosetup -n %{srcname}-%{version} -p 1
rm -rf %{eggname}.egg-info


%build
%py3_build


%install
%py3_install


%if %{with tests}
%check
%pytest --verbose
%endif


%files -n python3-%{pkgname}
%license LICENSE.md
%doc README.md
%pycached %{python3_sitelib}/%{libname}.py
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info


%changelog
* Fri Mar 03 2023 Muhammad Falak <mwani@microsoft.com> - 1.4.2-6
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

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
