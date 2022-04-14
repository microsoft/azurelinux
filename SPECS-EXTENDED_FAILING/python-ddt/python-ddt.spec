Vendor:         Microsoft Corporation
Distribution:   Mariner
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




%bcond_without  python3


Name:           python-%{pkgname}
Version:        1.2.1
Release:        7%{?dist}
Summary:        Python library to multiply test cases
License:        MIT
URL:            https://github.com/datadriventests/ddt
Source0:        %pypi_source
# https://github.com/datadriventests/ddt/pull/74
Patch0:         use-mock-from-standard-library.patch
BuildArch:      noarch


%description %{common_description}


%if %{with python2}
%package -n python2-%{pkgname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-nose
BuildRequires:  python2-mock
BuildRequires:  python2-six >= 1.4.0
%if %{defined rhel} && 0%{?rhel} <= 7
BuildRequires:  PyYAML
%else
BuildRequires:  python2-yaml
%endif
%if %{defined fedora} || (%{defined rhel} && 0%{?rhel} >= 8)
Recommends:     python2-yaml
%endif
%{?python_provide:%python_provide python2-%{pkgname}}


%description -n python2-%{pkgname} %{common_description}
%endif


%if %{with python3}
%package -n python%{python3_pkgversion}-%{pkgname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-six >= 1.4.0
BuildRequires:  python%{python3_pkgversion}-yaml
%if %{defined fedora} || (%{defined rhel} && 0%{?rhel} >= 8)
Recommends:     python%{python3_pkgversion}-yaml
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}


%description -n python%{python3_pkgversion}-%{pkgname} %{common_description}
%endif


%prep
%autosetup -n %{srcname}-%{version} -p 1
rm -rf %{eggname}.egg-info


%build
%{?with_python2:%py2_build}
%{?with_python3:%py3_build}


%install
%{?with_python2:%py2_install}
%{?with_python3:%py3_install}


%check
%{?with_python2:PYTHONPATH=%{buildroot}%{python2_sitelib} nosetests-%{python2_version} --verbose}
%{?with_python3:PYTHONPATH=%{buildroot}%{python3_sitelib} nosetests-%{python3_version} --verbose}


%if %{with python2}
%files -n python2-%{pkgname}
%license LICENSE.md
%doc README.md
%{python2_sitelib}/%{libname}.py*
%{python2_sitelib}/%{eggname}-%{version}-py%{python2_version}.egg-info
%endif


%if %{with python3}
%files -n python%{python3_pkgversion}-%{pkgname}
%license LICENSE.md
%doc README.md
%{python3_sitelib}/%{libname}.py
%{python3_sitelib}/__pycache__/%{libname}.cpython-%{python3_version_nodots}*.py*
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info
%endif


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
