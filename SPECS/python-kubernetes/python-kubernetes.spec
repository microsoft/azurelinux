%global library kubernetes

Name:       python-%{library}
Version:    28.1.0
Release:    1%{?dist}
Summary:    Python client for the kubernetes API.
License:    ASL 2.0
URL:        https://github.com/kubernetes-client/python
Source0:    https://github.com/kubernetes-client/python/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:  noarch

%package -n python3-%{library}
Summary:    Kubernetes Python Client
BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-certifi
Requires:       python3-six
Requires:       python3-dateutil
Requires:       python3-setuptools 
Requires:       python3-urllib3
Requires:       python3-PyYAML
Requires:       python3-google-auth
Requires:       python3-websocket-client


%description -n python3-%{library}
Python client for the kubernetes API.

%package -n python3-%{library}-tests
Summary:    Tests python-kubernetes library

Requires:  python3-pip
Requires:  python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
Tests python-kubernetes library


%description
Python client for the kubernetes API.

%prep
%autosetup -n python-%{version} -S git

%build
python3 setup.py build

%install

python3 setup.py install --skip-build --root=%{buildroot}
cp -pr kubernetes/test %{buildroot}%{python3_sitelib}/%{library}/
cp -pr kubernetes/e2e_test %{buildroot}%{python3_sitelib}/%{library}/

%files -n python3-%{library}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{library}
%{python3_sitelib}/%{library}-*.egg-info
%exclude %{python3_sitelib}/%{library}/test
%exclude %{python3_sitelib}/%{library}/e2e_test

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{library}/test
%{python3_sitelib}/%{library}/e2e_test

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 28.1.0-1
- Auto-upgrade to 28.1.0 - Azure Linux 3.0 - package upgrades

* Mon Feb 07 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 21.7.0-1
- Upgrade to 21.7.0

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 11.0.0-5
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 11.0.0-3
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> - 11.0.0-2
- Fix EPEL 7 and 8 builds

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> - 11.0.0-1
- Update to 11.0.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
- Work around BZ1758141 for BZ1799937

* Fri Nov 08 2019 Jason Montleon <jmontleo@redhat.com> 10.0.1-1
- Update to upstream 10.0.1

* Fri Oct 18 2019 Jason Montleon <jmontleo@redhat.com> 9.0.1-1
- Update to upstream 9.0.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 18 2019 Jason Montleon <jmontleo@redhat.com> 8.0.1-1
- Update to upstream 8.0.1

* Sat Feb 2 2019 Jason Montleon <jmontleo@redhat.com> 8.0.0-8
- add upstream patch to make python-adal optional
- remove python-adal requires for EL7 since it's not available in RHEL base, optional, or extras

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Jason Montleon <jmontleo@redhat.com> 8.0.0-6
- Only apply EL7 requirement patch on EL7 so Fedora dependency generator works correctly

* Thu Jan 17 2019 Jason Montleon <jmontleo@redhat.com> 8.0.0-5
- Keep python 2 enabled for Fedora 29.

* Tue Jan 15 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.0.0-4
- Enable python dependency generator

* Fri Dec 14 2018 Jason Montleon <jmontleo@redhat.com> 8.0.0-3
- Default to python 2 for EPEL 7 and python 3 for Fedora
- Add docs package for Fedora

* Mon Nov 26 2018 Jason Montleon <jmontleo@redhat.com> 8.0.0-2
- Patch setup.py to work with EL7 python-setuptools

* Mon Nov 5 2018 Jason Montleon <jmontleo@redhat.com> 8.0.0-1
- Update to 8.0.0

* Wed Oct 3 2018 Jason Montleon <jmontleo@redhat.com> 7.0.0-3
- Adding missing python3-adal dependency

* Wed Oct 3 2018 Jason Montleon <jmontleo@redhat.com> 7.0.0-2
- Adding missing python-adal dependency

* Wed Oct 3 2018 Jason Montleon <jmontleo@redhat.com> 7.0.0-1
- Update to 7.0.0

* Tue Feb 28 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.3.0b3
- Remove BRs for documentation building as it's not creating html docs.

* Mon Feb 27 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.2.0b3
- Fixed files section of python3-kubernetes-tests to contain python3 tests.

* Mon Feb 27 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.1.0b3
- Initial spec for release 1.0.0b3
