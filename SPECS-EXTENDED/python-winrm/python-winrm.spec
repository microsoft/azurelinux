%global srcname winrm

Name:           python-%{srcname}
Version:        0.4.1
Release:        5%{?dist}
Summary:        Python libraries for interacting with windows remote management
Vendor:		Microsoft Corporation
Distribution:	Mariner
License:        MIT
URL:            https://pypi.python.org/pypi/pywinrm
Source0:        https://github.com/diyan/pywinrm/archive/v%{version}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(mock)
BuildRequires:  python3dist(xmltodict)
BuildRequires:  python3dist(requests) >= 2.9.1
BuildRequires:  python3dist(requests-ntlm) >= 0.3
BuildRequires:  python3dist(six)

%global _description %{expand:
This has the python libraries for interacting with Windows Remote Management.}

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n pywinrm-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 -m pytest -vv winrm/tests

%files -n python3-%{srcname}
%license LICENSE
%doc README.md CHANGELOG.md
%{python3_sitelib}/pywinrm-*.egg-info/
%{python3_sitelib}/winrm/

%changelog
* Mon Dec 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.4.1-5
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Joel Capitao <jcapitao@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hroncok <mhroncok@redhat.com> - 0.3.0-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hroncok <mhroncok@redhat.com> - 0.3.0-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hroncok <mhroncok@redhat.com> - 0.3.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 17 2019 Miro Hroncok <mhroncok@redhat.com> - 0.3.0-5
- Subpackage python2-winrm has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hroncok <mhroncok@redhat.com> - 0.3.0-2
- Rebuilt for Python 3.7

* Tue Apr 17 2018 James Hogarth <james.hogarth@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.2.2-1
- Update to 0.2.2
- Update requires to fix bz#1409670

* Tue Dec 20 2016 James Hogarth <james.hogarth@gmail.com> - 0.2.1-3
- Fix broken requires for epel

* Mon Dec 19 2016 Miro Hroncok <mhroncok@redhat.com> - 0.2.1-2
- Rebuild for Python 3.6

* Mon Oct 24 2016 James Hogarth <james.hogarth@gmail.com> - 0.2.1-1
- Initial package
