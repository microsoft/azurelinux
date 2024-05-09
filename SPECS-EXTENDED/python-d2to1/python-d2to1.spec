Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname d2to1

Name: python-%{srcname}
Version: 0.2.12
Release: 18%{?dist}
Summary: Allows using distutils2-like setup.cfg files with setup.py
License: BSD

URL: https://pypi.python.org/pypi/d2to1
Source0: https://pypi.python.org/packages/source/d/%{srcname}/%{srcname}-%{version}.post1.tar.gz#/%{name}-%{version}.post1.tar.gz

BuildArch: noarch

%global _description\
d2to1 allows using distutils2-like setup.cfg files for a package's metadata\
with a distribute/setuptools setup.py script. It works by providing a\
distutils2-formatted setup.cfg file containing all of a package's metadata,\
and a very minimal setup.py which will slurp its arguments from the setup.cfg.

%description %_description

%package -n python3-d2to1
Summary: Allows using distutils2-like setup.cfg files with setup.py
%{?python_provide:%python_provide python3-d2to1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  python3-setuptools

%description -n python3-d2to1 %_description

%prep
#%setup -q -n %{srcname}-%{version}
%setup -q -n %{srcname}-%{version}.post1

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%py3_build

%install
%py3_install

%files -n python3-d2to1
%doc CHANGES.rst README.rst
%license LICENSE
%{python3_sitelib}/*


%changelog
* Tue Apr 26 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.2.12-18
- Updated source URL.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.12-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-16.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-15.post1
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-14.post1
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-13.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 05 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-12.post1
- Subpackage python2-d2to1 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-11.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-10.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-9.post1
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.2.12-8.post1
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-7.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.12-6.post1
- Python 2 binary package renamed to python2-d2to1
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-5.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-4.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-3.post1
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-2.post1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Mar 29 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.12-1.post1
- New upstream source (0.2.12)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Feb 24 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.11-1
- New upstream source (0.2.11)
- Use python2 macro

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.10-1
- New upstream source

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.7-2
- Requires for python3 inside python3 package (bz #891381)

* Wed Sep 26 2012 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.7-1
- New upstream source
- Removing upstream egg-info and defattr

* Thu Sep 22 2011 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.5-1
- Initial spec file

