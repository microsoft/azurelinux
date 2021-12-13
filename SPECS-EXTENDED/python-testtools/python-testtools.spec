%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?__python3: %global __python3 /usr/bin/python3}

# what it's called on pypi
%global srcname testtools
# what it's imported as
%global libname %{srcname}
# name of egg info directory
%global eggname %{srcname}
# package name fragment
%global pkgname %{srcname}

%global common_description %{expand:
testtools is a set of extensions to the Python standard library's unit testing
framework.}

# To build this package in a new environment (i.e. a new EPEL branch), you'll
# need to build in a particular order.
#
# 1. python-testtools with the tests disabled
# 2. python-fixtures with the tests disabled
# 3. python-testscenarios
# 4. python-testtools and python-fixtures with tests enabled
%bcond_with tests
%bcond_without docs

Name:           python-%{pkgname}
Version:        2.4.0
Release:        8%{?dist}
Summary:        Extensions to the Python unit testing framework
License:        MIT
URL:            https://launchpad.net/testtools
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/t/%{libname}/%{libname}-%{version}.tar.gz
Patch0:         testtools-2.4.0-remove_backports.patch
# Reported as:
# https://github.com/testing-cabal/testtools/pull/293
Patch1:         testtools-2.4.0-fix_py39_test.patch
BuildArch:      noarch

%description %{common_description}

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-extras
BuildRequires:  python3-mimeparse
BuildRequires:  python3-pbr
BuildRequires:  python3-sphinx
BuildRequires:  python3-xml
#BuildRequires:  %{py3_dist setuptools extras python-mimeparse pbr}
%if %{with tests}
BuildRequires:  python3-testscenarios
#BuildRequires:  %{py3_dist testscenarios}
%endif
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{common_description}

%if %{with docs}
%package        doc
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-websupport
#BuildRequires:  %{py3_dist sphinx}
Summary:        Documentation for %{name}

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_temporary_exceptions
Provides:       bundled(jquery)

%description doc
This package contains HTML documentation for %{name}.
%endif

%prep
%autosetup -p 1 -n %{srcname}-%{version}
rm -rf %{eggname}.egg-info
rm testtools/_compat2x.py

%build
CFLAGS="%{optflags}" %{__python3} setup.py build

%if %{with docs}
PYTHONPATH=$PWD make SPHINXBUILD=sphinx-build3 -C doc html
%endif

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%if %{with tests}
%check
make PYTHON=%{__python3} check
%endif

%files -n python3-%{pkgname}
%license LICENSE
%doc NEWS
%doc README.rst
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info

%if %{with docs}
%files doc
%doc doc/_build/html/*
%endif

%changelog
* Tue Oct 13 2020 Steve Laughman <steve.laughman@microsoft.com> - 2.4.0-8
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-6
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-5
- Bootstrap for Python 3.9

* Sat May 16 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.4.0-4
- Fix syntax error test on Python 3.9

* Fri Apr 24 2020 Carl George <carl@george.computer> - 2.4.0-3
- Enable tests

* Fri Apr 24 2020 Carl George <carl@george.computer> - 2.4.0-2
- Disable tests for EPEL8 bootstrap

* Fri Apr  3 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Thu Feb 20 2020 Avram Lubkin <aviso@rockhopper.net> - 2.3.0-18
- Patch to remove unittest2 and traceback2 from source

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Avram Lubkin <aviso@rockhopper.net> - 2.3.0-16
- Remove unittest2 dependency
- Remove traceback2 dependency

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-15
- Subpackage python2-testtools has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Sep 26 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-14
- Reduce the build dependencies by not running tests on Python 2

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-13
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-12
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 15 2019 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.3.0-11
- Update project URL

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-8
- Rebuilt for Python 3.7

* Tue Jun 05 2018 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-7
- Backport upstream patch for Python 3.7 support (#1577621)
- Use python2 explicitly

* Fri Mar 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.3.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 2.3.0-4
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.3.0-3
- Python 2 binary package renamed to python2-testtools
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 2.3.0-1
- Upstream 2.3.0
- Refresh spec

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.8.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun  3 2016 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.8.0-5
- Add runtime dependency on traceback2 (bz#1251568)
- Bump required version of unittest2 (bz#1304326)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Jul 28 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.8.0-2
- Provide python2-testtools per updated guidelines

* Tue Jul 28 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Nov 27 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Fri Sep 19 2014 Jerry James <loganjerry@gmail.com> - 1.1.0-1
- Update to 1.1.0 (bz 1132881)
- Fix license handling
- Note bundling exception for jquery in -doc

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.35-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Feb 28 2014 Matthias Runge <mrunge@redhat.com> - 0.9.35-2
- re-enable building the python3-subpackage

* Mon Feb  3 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.35-1
- Update to 0.9.35

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul  4 2013 Michel Salim <salimma@fedoraproject.org> - 0.9.32-2
- Add new runtime dep on -extras to Python3 variant as well

* Thu Jul  4 2013 Michel Salim <salimma@fedoraproject.org> - 0.9.32-1
- Update to 0.9.32
- Switch to using split-off extras package

* Sat May 18 2013 Pádraig Brady <pbrady@redhat.com> - 0.9.30-1
- Update to 0.9.30

* Thu Feb 07 2013 Pádraig Brady <pbrady@redhat.com> - 0.9.29-1
- Update to 0.9.29

* Sat Oct 27 2012 Michel Alexandre Salim <michel@sojourner> - 0.9.21-1
- Update to 0.9.21

* Sat Oct 20 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.19-1
- Update to 0.9.19
- On Fedora, also build for Python 3.x

* Wed Sep  5 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.16-1
- Update to 0.9.16
- Remove deprecated sections

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.15-1
- Update to 0.9.15

* Thu Apr  5 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.14-1
- Update to 0.9.14
- Enable unit tests

* Tue Feb  7 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.13-1
- Update to 0.9.13

* Tue Jan 31 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.12-1
- Update to 0.9.12

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.11-1
- Update to 0.9.11
- Enable documentation generation

* Thu Apr  7 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.8-2
- Add definitions needed by older RPM versions

* Thu Apr  7 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.8-1
- Initial package
