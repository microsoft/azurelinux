%global library google-auth
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-%{library}
Version:        2.6.6
Release:        1%{?dist}
Summary:        Google Auth Python Library
License:        ASL 2.0
URL:            https://github.com/googleapis/google-auth-library-python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.python.org/packages/source/g/%{library}/%{library}-%{version}.tar.gz

BuildArch:  noarch

%description
Google Auth Python Library

%package -n python3-%{library}
Summary:    Google Auth Python Library

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  git
Requires:  python3-pyasn1
Requires:  python3-pyasn1-modules
Requires:  python3-rsa
Requires:  python3-six
Requires:  python3-cachetools

%description -n python3-%{library}
Python client for the kubernetes API.

%prep
%autosetup -n %{library}-%{version}

#Allow newer cachetools
sed -i 's/<3\.2/<5.0/g' setup.py

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root=%{buildroot}

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/google/auth
%{python3_sitelib}/google/oauth2
%{python3_sitelib}/google_auth-%{version}*.egg-info
%{python3_sitelib}/google_auth-%{version}*.pth

%changelog
* Thu Apr 27 2022 Mateusz Malisz <mamalisz@microsoft.com> - 2.6.6-1
- Update to 2.6.6

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.20.1-1
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Wed Jul 29 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.20.0-1
- Update to 1.20.0 (#1858426)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.19.1-1
- Update to 1.19.1 (#1856662)

* Fri Jun 19 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.18.0-1
- Update to 1.18.0 (#1846258)

* Thu Jun 04 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.16.1-1
- Update to 1.16.1 (#1841468)

* Tue May 26 2020 Miro HronÄok <mhroncok@redhat.com> - 1:1.14.3-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.14.3-1
- Update to 1.14.3

* Thu May 07 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.14.2-1
- Update to 1.14.2 (#1832794)

* Wed Apr 22 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.14.1-1
- Update to 1.14.1 (#1824032)

* Thu Apr 02 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.13.1-1
- Update to 1.13.1 (#1817303)

* Mon Mar 16 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.11.3-1
- Update to 1.11.3

* Wed Feb 19 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.11.2-1
- Update to 1.11.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.11.0-1
- Update to 1.11.0 (#1794771)

* Thu Jan 23 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.10.2-2
- Update to 1.10.2 (#1793920)

* Wed Jan 15 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.10.1-1
- Update to 1.10.1 (#1779733)

* Fri Dec 20 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.10.0-1
- Update to 1.10.0

* Wed Dec 11 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.9.0-2
- Allow newer cachetools

* Wed Dec 11 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.9.0-1
- Update to 1.9.0

* Wed Dec 11 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.8.2-1
- Update to 1.8.2 (#1779733)

* Tue Nov 19 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.7.1-1
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Oct 03 2019 Miro HronÄok <mhroncok@redhat.com> - 1:1.1.1-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro HronÄok <mhroncok@redhat.com> - 1:1.1.1-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.1.1-6
- Enable python dependency generator

* Mon Jan 14 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.1.1-5
- Fix cachetools dependency for python2

* Thu Dec 13 2018 Jason Montleon <jmontleo@redhat.com> - 1:1.1.1-4
- Use python3_pkgversion for EPEL

* Mon Dec 3 2018 Jason Montleon <jmontleo@redhat.com> - 1:1.1.1-3
- Use GitHub instead of PyPI source tarball to build

* Tue Oct 23 2018 Alfredo Moralejo <amoralej@redhat.com> - 1:1.1.1-2
- Removed python2 subpackages in Fedora (rhbz#1636936).

* Mon Aug 13 2018 Alfredo Moralejo <amoralej@redhat.com> - 1:1.1.1-1
- Revert to version 1.1.1. Version 1.3.0 requires pyasn1-modules newer that in Fedora (rhbz#1577286).

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro HronÄok <mhroncok@redhat.com> - 1.3.0-4
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.3.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Alfredo Moralejo <amoralej@redhat.com> 1.3.0-1
- Update to 1.3.0

* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 1.1.1-1
- Initial Build
