%global srcname requests_ntlm
%define debug_package %{nil}

Name:           python-%{srcname}
Version:        1.1.0
Release:        17%{?dist}
Summary:        NTLM module for python requests
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        ISC
URL:            https://pypi.python.org/pypi/requests_ntlm
Source0:        https://github.com/requests/requests-ntlm/archive/v%{version}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%global _description %{expand:
This package allows Python clients running on any operating system to provide
NTLM authentication to a supporting server.}

%description %{_description}

%package -n     python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(requests) >= 2
BuildRequires:  python3dist(ntlm-auth) >= 1.0.2
BuildRequires:  python3dist(cryptography) >= 1.3
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(flask)

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n requests-ntlm-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 -m tests.test_server &
%python3 -m pytest --ignore=tests/functional/test_functional.py --ignore=tests/test_server.py -vv

%files -n python3-%{srcname}
%license LICENSE
%doc CONTRIBUTORS.rst README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%changelog
* Mon Dec 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1.0-17
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.0-15
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.1.0-13
- Update spec

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-8
- Rebuilt for Python 3.8

* Tue Aug 13 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.0-7
- Refactor packaging

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-5
- Subpackage python2-requests_ntlm has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.7
- Add missing BR python3-cryptography

* Tue Apr 17 2018 James Hogarth <james.hogarth@gmail.com> - 1.1.0-1
- Upstream release 1.1.0

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Rebuild for Python 3.6

* Mon Oct 10 2016 James Hogarth <james.hogarth@gmail.com> - 0.3.0-1
- Initial package.
