Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global srcname voluptuous

Name: python-%{srcname}
Version: 0.11.7
Release: 4%{?dist}
Summary: A Python data validation library
License: BSD
URL: https://github.com/alecthomas/voluptuous
Source0: %{pypi_source}

BuildArch: noarch
BuildRequires: python3-devel

%description
Voluptuous, despite the name, is a Python data validation library. It is 
primarily intended for validating data coming into Python as JSON, YAML, etc.


%package -n python3-%{srcname}
Summary: A Python data validation library
BuildRequires: python3-devel python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Voluptuous, despite the name, is a Python data validation library. It is 
primarily intended for validating data coming into Python as JSON, YAML, etc.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%doc README.md
%license COPYING
%{python3_sitelib}/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11.7-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11.7-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.11.7-1
- Update to 0.11.7 (#1742700)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11.5-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 21 2019 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-5
- Drop python2 subpackage (bz #1712339)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 06 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-3
- Readd python2 subpackage, not yet

* Fri Oct 05 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-2
- Drop python2 subpackage

* Tue Aug 21 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-1
- New upstream source (0.11.5)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11.1-2
- Rebuilt for Python 3.7

* Thu Mar 08 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.1-1
- New upstream source (0.11.1)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.10.5-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.5-1
- New upstream source (0.10.5.1)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.3-3
- Rebuild for Python 3.6

* Sun Oct 02 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.9.3-2
- New upstream source (0.9.3)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.11-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 13 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.11-1
- New upstream source (0.8.11)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.8-1
- New upstream source
- Use new python macros
- Enable python3, fixes bz #1292616

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 22 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.5-2
- Use tarball from github
- Add COPYING to doc

* Mon Mar 17 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.5-1
- Initial spec file

