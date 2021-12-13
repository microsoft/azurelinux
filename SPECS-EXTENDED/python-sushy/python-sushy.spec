Vendor:         Microsoft Corporation
Distribution:   Mariner
# Macros for py2/py3 compatibility

%global pyver %{python3_pkgversion}

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1
%global sname sushy

%global common_desc \
Sushy is a Python library to communicate with Redfish based systems (http://redfish.dmtf.org)

%global common_desc_tests Tests for Sushy

Name: python-%{sname}
Version: 2.0.3
Release: 2%{?dist}
Summary: Sushy is a Python library to communicate with Redfish based systems
License: ASL 2.0
URL: http://launchpad.net/%{sname}/

Source0: http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz

BuildArch: noarch

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary: Sushy is a Python library to communicate with Redfish based systems
%{?python_provide:%python_provide python%{pyver}-%{sname}}

BuildRequires: git
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-pbr
BuildRequires: python%{pyver}-setuptools
# For running unit tests during check phase
BuildRequires: python%{pyver}-requests
BuildRequires: python%{pyver}-six
BuildRequires: python%{pyver}-dateutil
BuildRequires: python%{pyver}-stevedore

Requires: python%{pyver}-pbr >= 2.0.0
Requires: python%{pyver}-six >= 1.10.0
Requires: python%{pyver}-requests >= 2.14.2
Requires: python%{pyver}-dateutil
Requires: python%{pyver}-stevedore >= 1.29.0

%description -n python%{pyver}-%{sname}
%{common_desc}

%package -n python%{pyver}-%{sname}-tests
Summary: Sushy tests
Requires: python%{pyver}-%{sname} = %{version}-%{release}

BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-testrepository
BuildRequires: python%{pyver}-testscenarios
BuildRequires: python%{pyver}-testtools

Requires: python%{pyver}-oslotest
Requires: python%{pyver}-testrepository
Requires: python%{pyver}-testscenarios
Requires: python%{pyver}-testtools

%description -n python%{pyver}-%{sname}-tests
%{common_desc_tests}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: Sushy documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{sname}-doc
Documentation for Sushy
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
%{pyver_bin} setup.py test

%install
%{pyver_install}

%files -n python%{pyver}-%{sname}
%license LICENSE
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/%{sname}-*.egg-info
%exclude %{pyver_sitelib}/%{sname}/tests

%files -n python%{pyver}-%{sname}-tests
%license LICENSE
%{pyver_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
* Tue Feb 23 2021 Henry Li <lihl@microsoft.com> - 2.0.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable python2 build and use python3 build 

* Tue May 26 2020 Dmitry Tantsur <divius.inside@gmail.com> - 2.0.3-1
- Update to 2.0.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 2.0.0-1
- Update to upstream version 2.0.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 Dmitry Tantsur <divius.inside@gmail.com> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 06 2019 Dmitry Tantsur <divius.inside@gmail.com> - 1.3.3-1
- Update to 1.3.3 to fix the UEFI boot mode issue

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.0-7
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 16 2018 Javier Peña <jpena@redhat.com> - 1.2.0-6
- Fixed Rawhide build (bz#1605933)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-4
- Rebuilt for Python 3.7

* Thu Feb 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 14 2017 Nathaniel Potter <nathaniel.potter@intel.com> 1.2.0-1
- Update for fedora packaging.
* Mon Mar 20 2017 Lucas Alvares Gomes <lucasagomes@gmail.com> 0.1.0-1
- Initial package.
