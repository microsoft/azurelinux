Vendor:         Microsoft Corporation
Distribution:   Mariner

%bcond_with python2
%bcond_without python3

%global distname requests-oauthlib
%global modname requests_oauthlib

Name:               python-requests-oauthlib
Version:            1.2.0
Release:            8%{?dist}
Summary:            OAuthlib authentication support for Requests.

License:            ISC
URL:                http://pypi.python.org/pypi/requests-oauthlib
Source0:            https://github.com/requests/requests-oauthlib/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:          noarch

%description
This project provides first-class OAuth library support for python-request.

%if %{with python2}
%package -n python2-%{distname}
%if 0%{?python_provide:1}
%python_provide python2-%{distname}
%else
Provides: python-%{distname} = %{version}-%{release}
%endif

Summary:            OAuthlib authentication support for Requests.

BuildRequires:      python2-devel
BuildRequires:      python2-setuptools

BuildRequires:      python2-oauthlib >= 0.6.2
BuildRequires:      python2-requests >= 2.0.0

BuildRequires:      python2-mock

Requires:           python2-oauthlib
Requires:           python2-requests >= 2.0.0

%description -n python2-%{distname}
This project provides first-class OAuth library support for python-request.
%endif # with python2

%if %{with python3}
%package -n python3-%{distname}
%{?python_provide:%python_provide python3-%{distname}}
Summary:            OAuthlib authentication support for Requests.

BuildRequires:      python3-devel
BuildRequires:      python3-setuptools

BuildRequires:      python3-oauthlib >= 0.6.2
BuildRequires:      python3-requests >= 2.0.0

BuildRequires:      python3-mock

Requires:           python3-oauthlib
Requires:           python3-requests

%description -n python3-%{distname}
This project provides first-class OAuth library support for python-request.
%endif

%prep
%autosetup -n %{distname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{distname}.egg-info


%build
%if %{with python2}
%py2_build
%endif # with python2
%if %{with python3}
%py3_build
%endif

%install
%if %{with python2}
%py2_install
%endif # with python2
%if %{with python3}
%py3_install
%endif

# Upstream doesn't actually ship the tests with the tarball.
# https://github.com/requests/requests-oauthlib/pull/91
#%%check
#%%{__python2} setup.py test

%if %{with python2}
%files -n python2-%{distname}
%doc README.rst HISTORY.rst requirements.txt AUTHORS.rst
%license LICENSE
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-%{version}*
%endif # with python2

%if %{with python3}
%files -n python3-%{distname}
%doc README.rst HISTORY.rst requirements.txt AUTHORS.rst
%license LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}*
%endif

%changelog
* Mon Oct 17 2022 Riken Maharjan <rmaharjan@microsft.com> - 1.2.0-8
- Migrate the package to Mariner Core.
- License verified

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.2.0-7
- Remove epoch

* Mon Feb 08 2021 Joe Schmitt <joschmit@microsoft.com> - 1.2.0-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora version check for python version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 29 2019 Kevin Fenzi <kevin@scrye.com> - 1.2.0-1
- Update to 1.2.0. Fixes bug #1697439

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018  <jdennis@redhat.com> - 1.0.0-1
- upgrade to new upstream release 1.0.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018  <jdennis@redhat.com> - 0.8.0-6
- Unify Fedora/RHEL py2/py3 logic

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 12 2017 John Dennis <jdennis@redhat.com> - 0.8.0-2
- bring spec file for fedora & rhel closer together

* Sat Feb 25 2017 Kevin Fenzi <kevin@scrye.com> - 0.8.0-1
- Update to 0.8.0.
- Make sure to specify package versions required. Fixes bug #1320683

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 28 2016 Ralph Bean <rbean@redhat.com> - 0.5.0-5
- Add an explicit python2 subpackage for #1313242.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Ralph Bean <rbean@redhat.com> - 0.5.0-1
- new version

* Fri Jan 23 2015 Ralph Bean <rbean@redhat.com> - 0.4.0-7
- Alter egg requirements for epel.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar  3 2014 Jakub Dorňák <jdornak@redhat.com> - 0.4.0-4
- python3 and python version related macros required to build
  python3- subpackage are not available in el6 and el7

* Fri Nov 29 2013 Jakub Dorňák <jdornak@redhat.com> - 0.4.0-3
- added python3 subpackage

* Fri Nov 01 2013 Ralph Bean <rbean@redhat.com> - 0.4.0-2
- Modernized the python2 rpm macros as per review feedback.

* Thu Oct 31 2013 Ralph Bean <rbean@redhat.com> - 0.4.0-1
- Initial package for Fedora
