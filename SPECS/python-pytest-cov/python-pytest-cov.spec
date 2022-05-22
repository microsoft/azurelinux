%global srcname pytest-cov
Summary:        Pytest plugin for coverage reporting
Name:           python-%{srcname}
Version:        2.12.1
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/pytest-cov
Source0:        https://github.com/pytest-dev/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-skip-tests-that-are-expected-to-fail.patch
BuildArch:      noarch

%description
Py.test plugin for coverage reporting with support for both centralised and
distributed testing, including subprocesses and multiprocessing for Python.

%package -n python%{python3_pkgversion}-%{srcname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Summary:        Pytest plugin for coverage reporting
BuildRequires:  python%{python3_pkgversion}-coverage >= 4.4
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# For tests
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python%{python3_pkgversion}-%{srcname}
Py.test plugin for coverage reporting with support for both centralised and
distributed testing, including subprocesses and multiprocessing for Python 3.

%prep
%autosetup -p1 -n %{srcname}-%{version}
rm -rf *.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
tox -e py%{python3_version_nodots} -v

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc AUTHORS.rst CHANGELOG.rst CONTRIBUTING.rst README.rst
%{python3_sitelib}/*

%changelog
* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.12.1-3
- Updating source URL.

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 2.12.1-2
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Wed Feb 16 2022 Muhammad Falak <mwani@microsoft.com> - 2.12.1-1
- Bump version to 2.12.1
- Introduce patch to skip known test failures
- Use tox instead of pytest to enable ptest

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 2.10.1-3
- Update check section to use pytest module
- License verified

* Mon Dec 07 2020 Steve Laughman <steve.laughman@microsoft.com> - 2.10.1-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Fri Aug 14 2020 Chedi Toueiti <chedi.toueiti@gmail.com> - 2.10.1-1
- Update to 2.10.1 (#1868968)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 9 2020 Chedi Toueiti <chedi.toueiti@gmail.com> - 2.10.0
- Update to 2.10.0

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.8.1-6
- Rebuilt for Python 3.9

* Mon Mar 2 2020 Chedi Toueiti <chedi.toueiti@gmail.com> - 2.8.1-5
- Forcing current pytest-cov version usage during checks

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Lumír Balhar <lbalhar@redhat.com> - 2.8.1-3
- Unskip tests which are working with the newest coverage

* Sun Nov  3 2019 Orion Poplawski <orion@nwra.com> - 2.8.1-2
- Drop python 2 for F32+ (bz#1767517)

* Sat Oct  5 2019 Orion Poplawski <orion@nwra.com> - 2.8.1-1
- Update to 2.8.1

* Fri Oct  4 2019 Orion Poplawski <orion@nwra.com> - 2.8.0-1
- Update to 2.8.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.1-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.1-5
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Orion Poplawski <orion@nwra.com> - 2.7.1-4
- Enable python dependency generator
- Specify minimum pytest requirement in BR

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Lumír Balhar <lbalhar@redhat.com> - 2.7.1-2
- Skip three tests (multiprocessing_pool) to fix FTBFS with Python 3.8

* Sun May  5 2019 Orion Poplawski <orion@nwra.com> - 2.7.1-1
- Update to 2.7.1

* Thu Apr 04 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-1
- Update to 2.6.1 for pytest 4 compatibility

* Tue Feb 12 2019 Orion Poplawski <orion@nwra.com> - 2.6.0-3
- Build with pytest-xdist

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 9 2017 Orion Poplawski <orion@cora.nwra.com> - 2.5.1-3
- Ship python2-pytest-cov

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Orion Poplawski <orion@cora.nwra.com> - 2.5.1-1
- Update to 2.5.1

* Wed May 10 2017 Orion Poplawski <orion@cora.nwra.com> - 2.5.0-1
- Update to 2.5.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 2.4.0-2
- Rebuild for Python 3.6

* Mon Oct 10 2016 Orion Poplawski <orion@cora.nwra.com> - 2.4.0-1
- Update to 2.4.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 7 2016 Orion Poplawski <orion@cora.nwra.com> - 2.3.0-1
- Update to 2.3.0

* Mon May 23 2016 Orion Poplawski <orion@cora.nwra.com> - 2.2.1-1
- Ignore failing tests

* Sat Feb 13 2016 Orion Poplawski <orion@cora.nwra.com> - 2.2.1-1
- Update to 2.2.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 2.2.0-2
- Rebuilt for Python3.5 rebuild
- Skip tests for a python3 rebuild as it seems to be env failure

* Mon Oct 5 2015 Orion Poplawski <orion@cora.nwra.com> - 2.2.0-1
- Update to 2.2.0

* Mon Sep 14 2015 Orion Poplawski <orion@cora.nwra.com> - 2.1.0-2
- Modernize spec
- Run tests properly, skipping xdist tests for now

* Mon Sep 14 2015 Tomas Tomecek <ttomecek@redhat.com> - 2.1.0-1
- upstream release 2.1.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Orion Poplawski <orion@cora.nwra.com> - 1.6-2
- Rebuild for Python 3.4

* Tue Feb 25 2014 Orion Poplawski <orion@cora.nwra.com> - 1.6-1
- Initial package
