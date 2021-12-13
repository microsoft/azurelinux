Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name hacking

# disable tests for now, see
# https://bugs.launchpad.net/hacking/+bug/1652409
# https://bugs.launchpad.net/hacking/+bug/1607942
# https://bugs.launchpad.net/hacking/+bug/1652411

# requires flake8 >= 2.6.0, < 2.7.0
%global with_tests 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        11%{?dist}
Summary:        OpenStack Hacking Guideline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://pypi.io/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%description
OpenStack Hacking Guideline Enforcement plugin for flake8.

%package -n python3-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-d2to1
BuildRequires:  python3-flake8
BuildRequires:  python3-pbr
BuildRequires:  python3-sphinx
BuildRequires:  python3-subunit
BuildRequires:  python3-sphinx
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-six
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-openstackdocstheme

Requires: python3-flake8
Requires: python3-pbr
Requires: python3-pycodestyle
Requires: python3-six

%description  -n python3-%{pypi_name}
OpenStack Hacking Guideline Enforcement plugin for flake8.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove /usr/bin/env from core.py
sed -i '1d' hacking/core.py

# remove /usr/bin/env from tests/test_doctest.py
sed -i '1d' hacking/tests/test_doctest.py

rm -rf {test-,}requirements.txt

%build

# generate html docs
sphinx-build-3 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%py3_build

%install
%py3_install

%check
%if 0%{?with_tests}
rm -rf .testrepository/
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%doc html README.rst
%license LICENSE
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 25 2019 Matthias Runge <mrunge@redhat.com> - 1.1.0-6
- drop python2 package (rhbz#1701951)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Matthias Runge <mrunge@redhat.com> - 1.1.0-4
- drop requirements pyflakes, pep8, flake8 and use pycodestyle instead

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.7

* Wed May 09 2018 Matthias Runge <mrunge@redhat.com> - 1.1.0-1
- update to 1.1.0 (rhbz#1576139)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 20 2017 Matthias Runge <mrunge@redhat.com> - 0.13.0-2
- disable tests for now (see above for links to bugs)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Adam Williamson <awilliam@redhat.com> - 0.13.0-1
- Update to 0.13.0 (some fixes for flake8 3.x compat from upstream)
- Patch test suite to be compatible with flake8 2.x and 3.x
- Disable 'local-check' feature on >F25 (incompatible with flake8 3.x)
- Re-enable Python 3 tests (they seem to work again now)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Sep 01 2015 Lukas Bezdicka <lbezdick@redhat.com> - 0.10.2-1
- Add python3 sub package and update to 0.10.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Matthias Runge <mrunge@redhat.com> - 0.10.1-1
- update to 0.10.1

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 0.9.2-1
- udapte to 0.9.2

* Tue Jun 10 2014 Matthias Runge <mrunge@redhat.com> - 0.9.1-1
- update to 0.9.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Matthias Runge <mrunge@redhat.com> - 0.8.1-1
- update to 0.8.1

* Tue Nov 19 2013 Matthias Runge <mrunge@redhat.com> - 0.8.0-1
- update to 0.8.0

* Tue Sep 17 2013 Matthias Runge <mrunge@redhat.com> - 0.7.2-1
- update to 0.7.2

* Fri Jun 07 2013 Matthias Runge <mrunge@redhat.com> - 0.5.3-2
- also use checks and move requirements to rpm-requiremens

* Mon Apr 29 2013 Matthias Runge <mrunge@redhat.com> - 0.5.3-1
- Initial package.
