Name:           python-kmod
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:        Python module to work with kernel modules
Version:        0.9
Release:        28%{?dist}
URL:            https://github.com/agrover/python-kmod/
Source0:        https://github.com/downloads/agrover/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-Cython
BuildRequires:  python3
BuildRequires:  kmod-devel

%global _description\
Python module to allow listing, loading, and unloading\
Linux kernel modules, using libkmod.

%description %_description

%package -n python3-kmod
Summary:        Python module to work with kernel modules

%description -n python3-kmod
Python module to allow listing, loading, and unloading
Linux kernel modules, using libkmod.

%prep
%setup -q

%build
%py3_build

%install
%py3_install

%files -n python3-kmod
%{python3_sitearch}/kmod/
%{python3_sitearch}/kmod*.egg-info
%doc COPYING.LESSER README

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9-28
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9-26
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9-25
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 27 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9-22
- Subpackage python2-kmod has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9-20
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.9-18
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 03 2018 Lumír Balhar <lbalhar@redhat.com> - 0.9-17
- Fix directory ownership

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9-16
- Python 2 binary package renamed to python2-kmod
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9-13
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9-11
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-10
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Oct 30 2014 Andy Grover <agrover@redhat.com> - 0.9-6
- Initial Python 3 support

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Andy Grover <agrover@redhat.com> - 0.9-1
- Update for new upstream release
- Add build dep on Cython

* Wed Aug 1 2012 Andy Grover <agrover@redhat.com> - 0.1-4
- Update for new upstream release location

* Fri May 4 2012 Andy Grover <agrover@redhat.com> - 0.1-3
- Update for new upstream release location

* Tue Apr 17 2012 Andy Grover <agrover@redhat.com> - 0.1-2
- Correct License field to LGPLv2+
- Remove explicit Requires for kmod-libs

* Thu Apr 12 2012 Andy Grover <agrover@redhat.com> - 0.1-1
- Initial packaging
