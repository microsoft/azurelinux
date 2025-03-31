%global srcname testtools
%global common_description %{expand:
testtools is a set of extensions to the Python standard library's unit testing
framework.}

# To build this package in a new environment (i.e. a new EPEL branch), you'll
# need to build in a particular order.  Duplicate numbered steps can happen at
# the same time.
#
# 1. bootstrap python-extras
# 1. bootstrap python-fixtures
# 2. bootstrap python-testtools
# 3. python-extras
# 3. python-fixtures
# 3. python-testscenarios
# 4. python-testresources
# 5. python-testtools
%bcond_with bootstrap

Name:           python-%{srcname}
Version:        2.7.1
Release:        8%{?dist}
Summary:        Extensions to the Python standard library unit testing framework
License:        MIT
URL:            https://github.com/testing-cabal/testtools
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source:         https://files.pythonhosted.org/packages/07/a7/3f3daee7a525d5288b84581448d21a39d0b9ae9f4a235d99850682944857/testtools-2.7.1.tar.gz#/%{name}-%{version}.tar.gz
# When rebasing patches, be aware that setup.cfg uses spaces in the git source,
# but tabs in the PyPI tarball.

# Compatibility with pytest 8
# https://github.com/testing-cabal/testtools/commit/48e689b4
Patch:          Treat-methodName-runTest-similar-to-unittest.TestCas.patch

BuildArch:      noarch
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec 
BuildRequires:  python3-pluggy
BuildRequires:  python3-twisted
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
BuildRequires:  python3-trove-classifiers
#BuildRequires:  python3-testscenarios
#BuildRequires:  python3-fixtures
BuildRequires:   python3-typing-extensions

%description %{common_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-%{srcname} %{common_description}

%if %{without bootstrap}
%package        doc
BuildRequires:  make
BuildRequires:  python3-sphinx
Summary:        Documentation for %{name}

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_temporary_exceptions
Provides:       bundled(jquery)

%description doc
This package contains HTML documentation for %{name}.
%endif


%prep
%autosetup -p 1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires %{!?with_bootstrap:-x test -x twisted}


%build
%pyproject_wheel

%if %{without bootstrap}
make -C doc html
%endif


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%if %{without bootstrap}
PYTHONPATH=%{buildroot}%{python3_sitelib} %{python3} -m testtools.run testtools.tests.test_suite
# Typically we would want an %%else condition to run an import check, but it
# will fail during the bootstrap phase, so leave it out.
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%license %{python3_sitelib}/testtools-2.7.1.dist-info/licenses/*
%doc NEWS README.rst

%if %{without bootstrap}
%files doc
%doc doc/_build/html/*
%endif


%changelog
* Fri Dec 21 2025 Jyoti kanase <v-jykanase@microsoft.com> -  2.7.1-8
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Tue Jul 23 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.7.1-7
- Backport upstream patch needed for compatibility with pytest 8

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 2.7.1-5
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.7.1-4
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 03 2023 Joel Capitao <jcapitao@redhat.com> - 2.7.1-1
- Update to 2.7.1 (rhbz#2247544)

* Thu Sep 14 2023 Michel Lind <salimma@fedoraproject.org> - 2.6.0-2
- Certify that we are using the SPDX license identifier

* Thu Aug 03 2023 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0 (rhbz#2178177, rhbz#2226353)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 2.5.0-13
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.5.0-12
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 2.5.0-9
- Rebuilt for Python 3.11

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 2.5.0-8
- Bootstrap for Python 3.11

* Fri Apr 29 2022 Carl George <carl@george.computer> - 2.5.0-7
- Switch to bootstrap macros

* Fri Apr 29 2022 Carl George <carl@george.computer> - 2.5.0-6
- Disable tests for EPEL9 bootstrap

* Tue Apr 26 2022 Carl George <carl@george.computer> - 2.5.0-5
- Convert to pyproject macros

* Tue Apr 26 2022 Carl George <carl@george.computer> - 2.5.0-4
- Fix Python 3.10 (final, not beta) FTBFS
- Resolves: rhbz#2046915

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.4.0-10
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 2.4.0-9
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

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
