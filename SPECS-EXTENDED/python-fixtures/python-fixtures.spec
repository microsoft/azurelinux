%global pypi_name fixtures

# fixtures has a circular dependency with testtools
%bcond_with bootstrap

Name:           python-%{pypi_name}
Version:        4.0.1
Release:        10%{?dist}
Summary:        Fixtures, reusable state for writing clean tests and more

License:        Apache-2.0 OR BSD-3-Clause
URL:            https://github.com/testing-cabal/fixtures
Source:         %pypi_source
BuildArch:      noarch


%global _description %{expand:
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing.  Helper and adaption logic is included to make it
easy to write your own fixtures using the fixtures contract.  Glue code is
provided that makes using fixtures that meet the Fixtures contract in unittest
compatible test cases easy and straight forward.}

%description %{_description}


%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel

%description -n python%{python3_pkgversion}-%{pypi_name} %{_description}

%if %{without bootstrap}
%pyproject_extras_subpkg -n python%{python3_pkgversion}-%{pypi_name} streams
%endif


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# The code supports falling back to the standard library mock, but some tests
# intentionally only test with the pypi mock.
sed -e '/mock/d' -i setup.cfg
sed -e 's/import mock/import unittest.mock as mock/' -i fixtures/tests/_fixtures/test_mockpatch.py

%generate_buildrequires
%pyproject_buildrequires %{!?with_bootstrap:-t -x streams}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%if %{without bootstrap}
%tox
%endif


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license Apache-2.0 BSD
%doc README.rst GOALS NEWS

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.0.1-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 17 2023 Zane Bitter <zaneb@fedoraproject.org> - 4.0.1-6
- Add streams extra

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 4.0.1-4
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.0.1-3
- Bootstrap for Python 3.12

* Wed Jun 07 2023 Jan Friesse <jfriesse@redhat.com> - 4.0.1-2
- migrated to SPDX license

* Mon Feb 06 2023 Joel Capitao <jcapitao@redhat.com> - 4.0.1-1
- Update to latest upstream (#2078479)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 3.0.0-30
- Rebuilt for Python 3.11

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 3.0.0-29
- Bootstrap for Python 3.11

* Fri Apr 29 2022 Carl George <carl@george.computer> - 3.0.0-28
- Convert to pyproject macros

* Wed Feb 23 2022 Alfredo Moralejo <amoralej@redhat.com> - 3.0.0-27
- Added python3-extras as runtime requirement

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-25
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 3.0.0-24
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 3.0.0-23
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 01 2020 Javier Peña <jpena@redhat.com> - 3.0.0-21
- Skip unit tests failing in Python 3.0 (bz#1787753)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-20
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-18
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-16
- Subpackage python2-fixtures has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-15
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-14
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-10
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.0.0-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 3.0.0-7
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.0-6
- Python 2 binary package renamed to python2-fixtures
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.0.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat May 21 2016 Matthias Runge <mrunge@redhat.com> - 3.0.0-1
- update to 3.0.0 (rhbz#1281945)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Paul Belanger <pabelanger@redhat.com> 1.4.0-1
- New upstream 1.4.0 release
- Update spec file latest python support
- Fix bogus date warning
- rpmlint warnings

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.14-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 24 2014 Matthias Runge <mrunge@redhat.com> - 0.3.14-1
- update to 0.3.14

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.3.12-3
- enable python3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 1 2013 Pádraig Brady <P@draigBrady.com> - 0.3.12-1
- Update to 0.3.12

* Fri Nov 16 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-4
- Update changelog

* Fri Nov 16 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-3
- Fix License:

* Thu Nov 15 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-2
- Remove version dependency on python-testtools (assume always >= 0.9.12)
- BuildRequire python2-devel rather than python-devel
- Adjust License:

* Wed Nov 14 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-1
- Initial package
