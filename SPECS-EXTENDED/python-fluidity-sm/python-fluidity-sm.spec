%global srcname fluidity

Name:          python-fluidity-sm
Version:       0.2.0
Release:       21%{?dist}
Summary:       State machine implementation for Python objects
License:       MIT
URL:           https://github.com/nsi-iff/fluidity
#Source0:      https://github.com/nsi-iff/fluidity/archive/%{version}/fluidity-%{version}.tar.gz
Source0:       https://github.com/nsi-iff/fluidity/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
# For test suite
#BuildRequires: python3-nose
#BuildRequires: python3-should_dsl
#BuildRequires: python3-spec

%description 
State machine implementation for Python objects.

%package -n python3-fluidity-sm
Summary:	State machine implementation for Python objects
%{?python_provide:%python_provide python3-fluidity-sm}

%description -n python3-fluidity-sm
State machine implementation for Python objects.

%prep
%setup -q -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

#%check
#nosetests-3 -i spec --with-specplugin

%files -n python3-fluidity-sm
%license LICENSE
%doc CHANGELOG README.rst
%{python3_sitelib}/fluidity/
%{python3_sitelib}/fluidity_sm-%{version}-*.egg-info/

%changelog
* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.2.0-21
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-19
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Thu Dec 12 2019 Paul Howarth <paul@city-fan.org> - 0.2.0-17
- Run the test suite
- Cosmetic spec changes
* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-16
- Subpackage python2-fluidity-sm has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-15
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-11
- Rebuilt for Python 3.7
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Fri Aug 11 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 0.2.0-9
- Revamp the spec file to use new python packaging guidelines
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-6
- Rebuild for Python 3.6
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
* Mon Dec 01 2014 Athmane Madjoudj <athmane@fedoraproject.org> 0.2.0-1
- Initial spec