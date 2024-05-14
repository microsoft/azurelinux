Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global upstream_name itsdangerous


Name:           python-%{upstream_name}
Version:        0.24
Release:        21%{?dist}
Summary:        Python library for passing trusted data to untrusted environments
License:        BSD
URL:            https://pythonhosted.org/itsdangerous/
Source0:        https://pypi.python.org/packages/source/i/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
BuildArch:      noarch

%description
Itsdangerous is a Python library for passing data through untrusted 
environments (for example, HTTP cookies) while ensuring the data is not 
tampered with.

Internally itsdangerous uses HMAC and SHA1 for signing by default and bases the 
implementation on the Django signing module. It also however supports JSON Web 
Signatures (JWS).

%package -n python3-%{upstream_name}
Summary:        Python 3 library for passing trusted data to untrusted environments
%{?python_provide:%python_provide python3-%{upstream_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{upstream_name}
Itsdangerous is a Python 3 library for passing data through untrusted 
environments (for example, HTTP cookies) while ensuring the data is not 
tampered with.

Internally itsdangerous uses HMAC and SHA1 for signing by default and bases the 
implementation on the Django signing module. It also however supports JSON Web 
Signatures (JWS).

%prep
%setup -q -n %{upstream_name}-%{version}
rm -r *.egg-info

%build
%py3_build

%install
%py3_install

%check
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} tests.py

%files -n python3-%{upstream_name}
%license LICENSE
%doc CHANGES README
%{python3_sitelib}/%{upstream_name}.py
%{python3_sitelib}/%{upstream_name}*.egg-info
%{python3_sitelib}/__pycache__/%{upstream_name}*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.24-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 24 2019 Miro Hrončok <mhroncok@redhat.com> - 0.24-19
- Subpackage python2-itsdangerous has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.24-18
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.24-14
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.24-12
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Dan Callaghan <dcallagh@redhat.com> - 0.24-10
- renamed python-itsdangerous to python2-itsdangerous

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.24-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.24-5
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 31 2014 Dan Callaghan <dcallagh@redhat.com> - 0.24-1
- new upstream release 0.24

* Thu Aug 15 2013 Dan Callaghan <dcallagh@redhat.com> - 0.23-1
- new upstream release 0.23 (no code changes, only packaging fixes)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Dan Callaghan <dcallagh@redhat.com> - 0.22-1
- new upstream release 0.22

* Tue Jun 18 2013 Dan Callaghan <dcallagh@redhat.com> - 0.21-3
- disable Python 3 subpackage on Fedora 17

* Mon Jun 17 2013 Dan Callaghan <dcallagh@redhat.com> - 0.21-2
- $RPM_BUILD_ROOT -> %%{buildroot}

* Fri Jun 14 2013 Dan Callaghan <dcallagh@redhat.com> - 0.21-1
- updated to upstream release 0.21
- added Python 3 subpackage

* Wed Nov 16 2011 Dan Callaghan <dcallagh@redhat.com> - 0.11-1
- initial version
