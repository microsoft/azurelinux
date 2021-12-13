%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global srcname betamax

# tests need internet access therefore disabled by default
# $ fedpkg mockbuild --enable-network --with=tests
%bcond_with tests

Summary:        VCR imitation for python-requests
Name:           python-%{srcname}
Version:        0.8.1
Release:        12%{?dist}
License:        ASL 2.0
URL:            https://github.com/sigmavirus24/%{srcname}
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
Source0:        https://github.com/sigmavirus24/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%global _description \
Betamax is a VCR_ imitation for requests. This will make mocking out requests\
much easier.

%description %{_description}

%package -n     python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-requests >= 2.0
%endif
Requires:       python3-requests >= 2.0

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%if %{with tests}
# test_pytest_fixture: not sure why it fails but better run some tests than none
# test_replays_response_from_cassette: https://github.com/betamaxpy/betamax/issues/184
# TestPyTestParametrizedFixtures: failure reason unknown
TEST_SELECTOR="not test_fixtures and not test_replays_response_from_cassette and not TestPyTestParametrizedFixtures"
py.test-%{python3_version} -vk "$TEST_SELECTOR"
%endif

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%changelog
* Mon Oct 19 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.8.1-12
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8.1-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8.1-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8.1-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 11 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8.1-5
- Subpackage python2-betamax has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.1-2
- Rebuilt for Python 3.7

* Wed Mar 14 2018 Parag Nemade <pnemade AT redhat DOT com> - 0.8.1-1
- Update to 0.8.1 version (#1555089)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.7.1-2
- Add missing Requires: pythonX-requests
- Make python2- subpkg
- Minor fixes

* Wed Jun 15 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.7.1-1
- Update to 0.7.1 release

* Mon May 02 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.7.0-1
- Update to 0.7.0 release
- disable tests as they need network access

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.5.1-1
- Initial packaging
