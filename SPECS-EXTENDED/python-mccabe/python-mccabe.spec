%global modname mccabe

Summary:        McCabe complexity checker
Name:           python-%{modname}
Version:        0.6.1
Release:        18%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/mccabe
Source0:        https://files.pythonhosted.org/packages/source/m/%{modname}/%{modname}-%{version}.tar.gz#/python-%{modname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-runner
BuildRequires:  python%{python3_pkgversion}-setuptools

%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
Ned's script to check McCabe complexity.

This module provides a plugin for flake8, the Python code
checker.

%package -n python%{python3_pkgversion}-%{modname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}
Summary:        McCabe checker, plugin for flake8

%description -n python%{python3_pkgversion}-%{modname}
Ned's script to check McCabe complexity.

This module provides a plugin for flake8, the Python code
checker.

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest
python3 -m pytest -v

%files -n python%{python3_pkgversion}-%{modname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}.py*
%{python3_sitelib}/%{modname}-%{version}-*
%{python3_sitelib}/__pycache__/%{modname}.*

%changelog
* Wed May 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.1-18
- Bringing back removed BRs to fix package build.

* Thu Apr 28 2022 Muhammad Falak <mwani@microsoft.com> - 0.6.1-17
- Drop BR on pytest & pip install latest deps to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.1-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-14
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-13
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 27 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-11
- Remove Python 2 subpackage

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-8
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 25 2017 Matěj Cepl <mcepl@redhat.com> - 0.6.1-6
- Fix wrong conditional

* Tue Oct 24 2017 Matěj Cepl <mcepl@redhat.com> - 0.6.1-5
- Apply fix for building on EPEL7, thanks to mvadkert.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 25 2017 Ville Skyttä <ville.skytta@iki.fi> - 0.6.1-3
- Use explicit python2-* dependencies where available
- Build Python 3 version by default on EL7

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Ville Skyttä <ville.skytta@iki.fi> - 0.6.1-1
- Update to 0.6.1

* Tue Jan 24 2017 Ville Skyttä <ville.skytta@iki.fi> - 0.6.0-1
- Update to 0.6.0

* Thu Jan 12 2017 Ville Skyttä <ville.skytta@iki.fi> - 0.5.3-1
- Update to 0.5.3
- Drop pytest-runner avoidance patch

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.5.2-3
- Rebuild for Python 3.6

* Mon Oct 24 2016 Orion Poplawski <orion@cora.nwra.com> - 0.5.2-2
- Enable python3 for EPEL
- Ship python2-mccabe
- Ship LICENSE
- Modernize spec

* Sun Aug 14 2016 Ville Skyttä <ville.skytta@iki.fi> - 0.5.2-1
- Update to 0.5.2

* Sat Aug 13 2016 Ville Skyttä <ville.skytta@iki.fi> - 0.5.0-3
- Add python3-pytest build dep, patch to build/test without pytest-runner

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 01 2016 Matěj Cepl <mcepl@redhat.com> - 0.5.0-1
- Upstream upgrade

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Matěj Cepl <mcepl@redhat.com> - 0.4.0-1
- Upstream upgrade

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 0.2.1-8
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 29 2014 Matěj Cepl <mcepl@redhat.com> - 0.2.1-4
- Fix building on RHEL-7 (we really don’t have Python3)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Matěj Cepl <mcepl@redhat.com> 0.2.1-2
- Fix %%changelog.

* Sun Apr 14 2013 Matěj Cepl <mcepl@redhat.com> 0.2.1-1
- initial package for Fedora
