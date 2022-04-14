%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global srcname lexicon

Name:          python-lexicon
Version:       1.0.0
Release:       13%{?dist}
Summary:       Powerful dict subclass(es) with aliasing and attribute access
License:       BSD
URL:           https://github.com/bitprophet/lexicon
#Source0:      https://github.com/bitprophet/lexicon/archive/%{version}/%{srcname}-%{version}.tar.gz
Source0:       https://github.com/bitprophet/lexicon/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-six
# For test suite
BuildRequires: python3-spec > 0.10.0

%description 
Lexicon is a simple collection of dict sub-classes providing extra power.

%package -n python3-lexicon
Summary:	Powerful dict subclass(es) with aliasing and attribute access
%{?python_provide:%python_provide python3-lexicon}
Requires:	python3-six

%description -n python3-lexicon
Lexicon is a simple collection of dict sub-classes providing extra power.

%prep
%setup -q -n lexicon-%{version}

%build
%py3_build

%install
%py3_install

%check
PYTHONPATH=%{buildroot}%{python3_sitelib} spec

%files -n python3-lexicon
%license LICENSE
%doc CHANGES README.md
%{python3_sitelib}/lexicon/
%{python3_sitelib}/lexicon-%{version}-*.egg-info/

%changelog
* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 1.0.0-13
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-11
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Wed Dec 11 2019 Paul Howarth <paul@city-fan.org> - 1.0.0-9
- Run the test suite
- Cosmetic spec changes
* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-8
- Subpackage python2-lexicon has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-7
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Rebuilt for Python 3.7
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Fri Aug 11 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0
- Revamp the spec to use the new python guidelines
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
* Mon Dec 01 2014 Athmane Madjoudj <athmane@fedoraproject.org> - 0.2.0-1
- Initial spec