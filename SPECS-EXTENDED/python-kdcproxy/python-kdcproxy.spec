%global realname kdcproxy

Name:           python-%{realname}
Version:        1.0.0
Release:        18%{?dist}
Summary:        MS-KKDCP (kerberos proxy) WSGI module

License:        MIT
URL:            https://github.com/latchset/%{realname}
Source0:        https://github.com/latchset/%{realname}/archive/%{realname}-%{version}.tar.gz

Patch0: Drop-coverage-from-tests.patch
Patch1: Use-exponential-backoff-for-connection-retries.patch
Patch2: Use-dedicated-kdcproxy-logger.patch

BuildArch:      noarch
BuildRequires:  git

BuildRequires:  python3-devel
BuildRequires:  python3-dns
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools

%description
This package contains a Python WSGI module for proxying KDC requests over
HTTP by following the MS-KKDCP protocol. It aims to be simple to deploy, with
minimal configuration.

%package -n python3-%{realname}
Summary:        MS-KKDCP (kerberos proxy) WSGI module
Requires:       python3-dns
Requires:       python3-pyasn1

%{?python_provide:%python_provide python3-%{realname}}

%description -n python3-%{realname}
This package contains a Python 3.x WSGI module for proxying KDC requests over
HTTP by following the MS-KKDCP protocol. It aims to be simple to deploy, with
minimal configuration.

%prep
%autosetup -S git -n %{realname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} -m pytest

%files -n python3-%{realname}
%doc README
%license COPYING
%{python3_sitelib}/%{realname}/
%{python3_sitelib}/%{realname}-%{version}-*.egg-info

%changelog
* Mon Dec 23 2024 Julien Rische <jrische@redhat.com> - 1.0.0-18
- Log KDC timeout only once per request
  Resolves: rhbz#2333853

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.0-16
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.0.0-12
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.0.0-9
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.0-6
- Rebuilt for Python 3.10

* Thu Apr 08 2021 Robbie Harwood <rharwood@redhat.com> - 1.0.0-5
- Actually drop coverage dependency

* Fri Jan 29 2021 Robbie Harwood <rharwood@redhat.com> - 1.0.0-4
- Drop unused dependency on python3-mock
- Resolves: #1922344

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Robbie Harwood <rharwood@redhat.com> - 1.0.0-2
- Drop coverage from tests
- Resolves: #1916739

* Tue Dec 08 2020 Robbie Harwood <rharwood@redhat.com> - 1.0.0-1
- New upstream version (1.0.0)
- Drop asn1crypto in favor of pyasn1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Robbie Harwood <rharwood@redhat.com> - 0.4.2-5
- Explicitly depend on python3-setuptools

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.2-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.2-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 29 2019 Robbie Harwood <rharwood@redhat.com> - 0.4.2-1
- New upstream version (0.4.2)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 11 2019 Robbie Harwood <rharwood@redhdat.com> 0.4.1-1
- New upstream release - 0.4.1
- Fixes build with rawhide (dnspython/dnspython3)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 17 2018 Robbie Harwood <rharwood@redhat.com> - 0.4-3
- Drop python2 subpackage
- Resolves: #1629775

* Thu Aug 09 2018 Robbie Harwood <rharwood@redhat.com> - 0.4-2
- Update dependencies in test suite

* Thu Aug 09 2018 Robbie Harwood <rharwood@redhat.com> - 0.4-1
- New upstream release - 0.4
- Port to autosetup

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-13
- Rebuilt for Python 3.7

* Thu Mar 22 2018 Troy Dawson <tdawson@redhat.com> - 0.3.2-12
- Update conditionals.
- Make preperations for non-python2 builds

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.2-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 05 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.3.2-9
- Ignore test results

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Charalampos Stratakis <cstratak@redhat.com> - 0.3.2-6
- Fix failing tests
- Modernize the SPEC file

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-5
- Rebuild for Python 3.6
- BR /usr/bin/tox instead of python-tox
- Use %%{python3_version_nodots} instead of hardcoded 35

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Aug 03 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2
- Fixes CVE-2015-5159

* Wed Jul 22 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3-1
- Update to 0.3
- Run tests in Fedora (not RHEL due to python-tox)

* Fri Oct 24 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Thu Oct 23 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.2-1
- Update to 0.2
- Fix EPEL7 build

* Tue Jan 21 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.1.1-1
- Initial package
