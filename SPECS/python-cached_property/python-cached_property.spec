%global projectname cached-property
%global modulename  cached_property
Summary:        A cached-property for decorating methods in Python classes
Name:           python-%{modulename}
Version:        1.5.2
Release:        9%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/pydanny/%{projectname}
Source0:        https://github.com/pydanny/%{projectname}/archive/%{version}/%{projectname}-%{version}.tar.gz
# Disable a couple of test checks that fail with freezegun 0.3.11
# See https://github.com/pydanny/cached-property/issues/131
Patch0:         0001-Disable-checks-broken-with-freezegun-0.3.11-131.patch
# Fix for removal of asyncio.coroutine in Python 3.11
# https://github.com/pydanny/cached-property/pull/267
Patch1:         267.patch
BuildArch:      noarch

%description
cached_property allows properties in Python classes to be cached until the cache
is invalidated or expired.

%package -n python%{python3_pkgversion}-%{modulename}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modulename}}
Summary:        A cached-property for decorating methods in Python classes.
BuildRequires:  python%{python3_pkgversion}-dateutil
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
Provides:       python%{python3_pkgversion}-%{projectname} = %{version}-%{release}
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python%{python3_pkgversion}-%{modulename}
cached_property allows properties in Python classes to be cached until the cache
is invalidated or expired.

%prep
%autosetup -p1 -n %{projectname}-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%check
pip3 install pytest==7.1.3 freezegun
%pytest

%files -n python%{python3_pkgversion}-%{modulename}
%doc AUTHORS.rst HISTORY.rst CONTRIBUTING.rst README.rst
%license LICENSE
%{python3_sitelib}/%{modulename}*
%{python3_sitelib}/__pycache__/%{modulename}*

%changelog
* Tue Nov 01 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.5.2-9
- License verified
- Initial CBL-Mariner import from Fedora 37 (license: MIT).

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.5.2-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 02 2021 Adam Williamson <awilliam@redhat.com> - 1.5.2-5
- Backport PR #267 to fix compatibility with Python 3.11 (thanks Petr Viktorin)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.5.2-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 16:02:58 CET 2021 Petr Viktorin <pviktori@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5.1-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.1-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.1-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 11 2019 Adam Williamson <awilliam@redhat.com> - 1.5.1-3
- Disable a couple of test checks that fail with freezegun 0.3.11

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 23 2018 Adam Williamson <awilliam@redhat.com> - 1.5.1-1
- New release 1.5.1
- Disable Python 2 build on F30+, EL8+

* Fri Nov 23 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.3-1
- Update to 1.4.3 (used by pipenv)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-12
- Rebuilt for Python 3.7

* Sun Feb 11 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.3.0-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 10 2017 Adam Williamson <awilliam@redhat.com> - 1.3.0-7
- Enable Python 3 build on EPEL 7

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 03 2016 Adam Williamson <awilliam@redhat.com> - 1.3.0-4
- disable tests on F22 (it doesn't know about py3.5)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 09 2015 Adam Williamson <awilliam@redhat.com> - 1.3.0-2
- try to repair the mess I made of package naming:
- # both subpackages now use module name not project name
- # try to ensure all previous names are provided/obsoleted

* Thu Nov 26 2015 Adam Williamson <awilliam@redhat.com> - 1.3.0-1
- new release 1.3.0, drop patch (merged upstream)
- switch to python2-foo / python3-foo package naming

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Adam Williamson <awilliam@redhat.com> - 1.2.0-1
- new upstream release 1.2.0 (refactoring, bug fixes)
- patch out non-ASCII characters in HISTORY.rst (breaks py3 build in koji)

* Thu Apr 16 2015 Adam Williamson <awilliam@redhat.com> - 1.1.0-1
- new upstream release 1.1.0 (insignificant changes)

* Wed Mar 25 2015 Adam Williamson <awilliam@redhat.com> - 1.0.0-4
- python3 build only for Fedora (no python3 in RHEL6 or 7)
- provide python2-cached_property
- guard against #license not being available
- only run tests on F>=22 (tox is too old on everything else)

* Fri Mar 13 2015 Pete Travis <me@petetravis.com> - 1.0.0-2
- Use the module name for the package name.

* Fri Feb 20 2015 Pete Travis <me@petetravis.com> 1.0.0-1
- Initial packaging. 
