Vendor:         Microsoft Corporation
Distribution:   Mariner

# Enable python3 build by default
%bcond_without python3

# Disable python2 build by default
%bcond_with python2

%global srcname jwcrypto

Name:           python-%{srcname}
Version:        0.6.0
Release:        8%{?dist}
Summary:        Implements JWK, JWS, JWE specifications using python-cryptography

License:        LGPLv3+
URL:            https://github.com/latchset/%{srcname}
Source0:        https://github.com/latchset/%{srcname}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz

BuildArch:      noarch
%if 0%{?with_python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-cryptography >= 1.5
BuildRequires:  python2-pytest
%endif

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-cryptography >= 1.5
BuildRequires:  python%{python3_pkgversion}-pytest
%endif

%description
Implements JWK, JWS, JWE specifications using python-cryptography


%if 0%{?with_python2}
%package -n python2-%{srcname}
Summary:        Implements JWK,JWS,JWE specifications using python-cryptography
Requires:       python2-cryptography >= 1.5
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Implements JWK, JWS, JWE specifications using python-cryptography
%endif


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Implements JWK, JWS, JWE specifications using python-cryptography
Requires:       python%{python3_pkgversion}-cryptography >= 1.5
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Implements JWK, JWS, JWE specifications using python-cryptography
%endif


%prep
%setup -q -n %{srcname}-%{version}


%build
%if 0%{?with_python2}
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif


%check
%if 0%{?with_python2}
%{__python2} -bb -m pytest %{srcname}/test*.py
%endif
%if 0%{?with_python3}
%{__python3} -bb -m pytest %{srcname}/test*.py
%endif


%install
%if 0%{?with_python2}
%py2_install
%endif
%if 0%{?with_python3}
%py3_install
%endif

rm -rf %{buildroot}%{_docdir}/%{srcname}
%if 0%{?with_python2}
rm -rf %{buildroot}%{python2_sitelib}/%{srcname}/tests{,-cookbook}.py*
%endif
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/tests{,-cookbook}.py*
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/__pycache__/tests{,-cookbook}.*.py*
%endif


%if 0%{?with_python2}
%files -n python2-%{srcname}
%doc README.md
%license LICENSE
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%endif


%changelog
* Thu Mar 02 2021 Henry Li <lihl@microsoft.com> - 0.6.0-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Enable python3 and disable python2 build

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 29 2019 Christian Heimes <cheimes@redhat.com> - 0.6.0-5
- Remove Python 2 subpackages from F32+
- Resolves: RHBZ #1746760

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Christian Heimes <cheimes@redhat.com> - 0.6.0-1
- New upstream release 0.6.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-2
- Rebuilt for Python 3.7

* Wed Jun 27 2018 Christian Heimes <cheimes@redhat.com> - 0.5.0-1
- New upstream release 0.5.0

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.2-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Christian Heimes <cheimes@redhat.com> - 0.4.2-3
- Run tests with bytes warning

* Tue Aug 01 2017 Christian Heimes <cheimes@redhat.com> - 0.4.2-2
- Modernize spec

* Tue Aug 01 2017 Christian Heimes <cheimes@redhat.com> - 0.4.2-1
- Upstream release 0.4.2
- Resolves: RHBZ #1476150

* Mon Jul 24 2017 Christian Heimes <cheimes@redhat.com> - 0.4.1-1
- Upstream release 0.4.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-2
- Rebuild for Python 3.6

* Wed Aug 31 2016 Simo Sorce <simo@redhat.com> - 0.3.2-1
- Security release 0.3.2
- Resolves: CVE-2016-6298

* Fri Aug 19 2016 Simo Sorce <simo@redhat.com> - 0.3.1-1
- Bugfix release 0.3.1

* Wed Aug 10 2016 Simo Sorce <simo@redhat.com> - 0.3.0-1
- New release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Aug  3 2015 Simo Sorce <simo@redhat.com> - 0.2.1-1
- New release
- Fixes some key generation issues

* Mon Jun 22 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-5
- Fix macro in changelog
- Remove the last remnants of the test suite

* Wed Jun 17 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-4
- Ship readme and license with python3 subpackage
- Move tests to %%check

* Wed Jun 17 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-3
- Fix F21 build error by adding buildrequire python-setuptools
- Move files into python3-jwcrypto subpackage
- Run test suite
- Do not install test suite
- Fix summary and description of python3-jwcrypto

* Tue Jun 16 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-2
- Enable python3 build

* Tue Jun 16 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-1
- Initial packaging
