%global pypi_name click
%global _description \
click is a Python package for creating beautiful command line\
interfaces in a composable way with as little amount of code as necessary.\
It's the "Command Line Interface Creation Kit".  It's highly configurable but\
comes with good defaults out of the box.

Summary:        Simple wrapper around optparse for powerful command line utilities
Name:           python-%{pypi_name}
Version:        8.1.7
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/mitsuhiko/click
Source0:        https://github.com/mitsuhiko/click/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description %{_description}

%package -n     python%{python3_pkgversion}-%{pypi_name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description -n python%{python3_pkgversion}-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest==7.2.2
pip3 install .
pytest -v tests

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE.rst
%doc README.rst CHANGES.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info/

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.1.7-1
- Auto-upgrade to 8.1.7 - Azure Linux 3.0 - package upgrades

* Tue May 30 2023 Olivia Crain <oliviacrain@microsoft.com> - 7.1.2-7
- Change %%check to install known-good version of pytest
- Use SPDX license expression in license tag

* Mon Oct 17 2022 Riken Maharjan <rmaharjan@microsft.com> - 7.1.2-6
- Migrate the package to Mariner Core.

* Mon Apr 25 2022 Muhammad Falak <mwani@microsoft.com> - 7.1.2-5
- Drop BR on pytest & pip install latest deps to enable ptest
- License verified

* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 7.1.2-4
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 7.1.2-2
- Rebuilt for Python 3.9

* Tue Apr 28 2020 Fabian Affolter <mail@fabian-affolter.ch> - 7.1.2-1
- Update to latest upstream release 7.1.2 (rhbz#1828589)

* Sat Apr 18 2020 Fabian Affolter <mail@fabian-affolter.ch> - 7.1.1-1
- Update to latest upstream release 7.1.1 (rhbz#1811727)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 18 2019 Miro Hrončok <mhroncok@redhat.com> - 7.0-6
- Subpackage python2-click has been removed
- See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 7.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.0-2
- Drop explicit locale setting
- See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Tue Oct 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 7.0-1
- Update to 7.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 6.7-8
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 12 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6.7-6
- Fixup EPEL packaging

* Thu Oct 12 2017 Carl George <carl@george.computer> - 6.7-6
- Add EPEL compatibility

* Thu Oct 12 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6.7-5
- Fix FTBFS

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Miro Hrončok <mhroncok@redhat.com> - 6.7-2
- Fixed a copy-paste bug in %%python_provide (rhbz#1411169)

* Sat Jan 07 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 6.7-1
- Update to 6.7
- Adopt to packaging guidelines

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 6.6-4
- Enable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 6.6-3
- Rebuild for Python 3.6
- Disable python3 tests for now

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.6-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 18 2016 Charalampos Stratakis <cstratak@redhat.com> - 6.6-1
- Update to 6.6
- Removed non-applied patch file.

* Tue Mar 08 2016 Robert Kuska <rkuska@redhat.com> - 6.3-1
- Update to 6.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Robert Kuska <rkuska@redhat.com> - 6.2-1
- Update to 6.2

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 5.1-2
- Rebuilt for Python3.5 rebuild

* Mon Aug 24 2015 Robert Kuska <rkuska@redhat.com> - 5.1-1
- Update to 5.1

* Mon Aug 03 2015 Robert Kuska <rkuska@redhat.com> - 4.1-1
- Update to 4.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Robert Kuska <rkuska@redhat.com> - 4.0-2
- Rebuilt

* Wed Apr 01 2015 Robert Kuska <rkuska@redhat.com> - 4.0-1
- Update to 4.0

* Fri Oct 03 2014 Robert Kuska <rkuska@redhat.com> - 3.3-1
- Update to 3.3

* Sun Aug 24 2014 Robert Kuska <rkuska@redhat.com> - 3.2-2
- Add patch for exception check of TypeError

* Sun Aug 24 2014 Robert Kuska <rkuska@redhat.com> - 3.2-1
- Update to 3.2

* Mon Aug 18 2014 Robert Kuska <rkuska@redhat.com> - 3.1-1
- Update to 3.1

* Wed Jul 16 2014 Robert Kuska <rkuska@redhat.com> - 2.4-1
- Update to 2.4

* Mon Jun 30 2014 Robert Kuska <rkuska@redhat.com> - 2.2-1
- Update to 2.2

* Thu Jun 12 2014 Robert Kuska <rkuska@redhat.com> - 2.0-1
- Update to 2.0

* Fri Jun 06 2014 Robert Kuska <rkuska@redhat.com> - 1.1-3
- Make click own its folder
- Use pythonX_version macros from devel package

* Thu May 29 2014 Robert Kuska <rkuska@redhat.com> - 1.1-2
- Remove __pycache__ folder from tests

* Mon May 12 2014 Robert Kuska <rkuska@redhat.com> - 1.1-1
- Update source

* Wed May 07 2014 Robert Kuska <rkuska@redhat.com> - 0.6-1
- Initial package.
