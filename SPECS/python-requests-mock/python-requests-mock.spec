%global pypi_name requests-mock
Name:           python-%{pypi_name}
Version:        1.8.0
Release:        6%{?dist}
Summary:        A requests mocking tool for python
License:        ASL 2.0
Vendor:         Mariner
Distribution:   Microsoft Corporation
URL:            https://requests-mock.readthedocs.io/
Source0:        https://pypi.io/packages/source/r/requests-mock/%{pypi_name}-%{version}.tar.gz
Patch0:         0002-Use-system-urllib3-package.patch
BuildArch:      noarch

%description
requests-mock provides a simple way to do HTTP mocking at the
python-requests layer.

%package -n python3-%{pypi_name}
Summary:        A requests mocking tool for python
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-requests
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-pbr
BuildRequires:  python%{python3_pkgversion}-urllib3
BuildRequires:  python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-requests
Requires:       python%{python3_pkgversion}-six

%if %{with_check}
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-pytest
%endif

%{?python_provide:%python_provide python3-requests-mock}

%description -n python3-%{pypi_name}
requests-mock provides a simple way to do HTTP mocking at the
python-requests layer.

%prep
%autosetup -p1 -n requests-mock-%{version}
# Remove bundled egg-info
rm -rf requests_mock.egg-info

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pip install -r test-requirements.txt
%{python3} -m testtools.run discover
%pytest3 tests/pytest

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.rst ChangeLog
%{python3_sitelib}/requests_mock
%{python3_sitelib}/requests_mock-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Jun 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.8.0-6
- Updating SPEC from Fedora 36 (license: MIT)
- Bump version to 1.8.0
- Adding as build dependency for apache-libcloud needed by cassandra-medusa.
- License verified

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

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
