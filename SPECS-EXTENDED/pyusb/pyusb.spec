Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: pyusb
Version: 1.0.2
Release: 7%{?dist}
Summary: Python bindings for libusb
License: BSD
URL: https://github.com/pyusb/pyusb/
Source0: https://github.com/pyusb/pyusb/archive/pyusb-%{version}.tar.gz
BuildRequires: libusb-devel
BuildArch: noarch

%global _description\
PyUSB provides easy USB access to python. The module contains classes and\
methods to support most USB operations.

%description %_description

%package -n python3-pyusb
Summary:       %summary
%{?python_provide:%python_provide python3-pyusb}
BuildRequires: python3-devel

%description -n python3-pyusb
PyUSB provides easy USB access to python. The module contains classes and 
methods to support most USB operations.

%prep
%autosetup
sed -i -e 's/\r//g' README.rst

%build
%py3_build

%install
%py3_install

%files -n python3-pyusb
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-7
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Mon Oct 21 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.0.2-6
- Drop Python 2.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.2-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 10 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.0.2-1
- 1.0.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-9
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 05 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.0.0-7
- Cleanup packaging and fix archful provide in noarch package

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.0-6
- Python 2 binary package renamed to python2-pyusb
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 14 2016 Jon Ciesla <limburgher@gmail.com> - 1.0.0-1
- Latest upstream, BZ 1192561.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.14.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.13.b2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.12.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Jon Ciesla <limburgher@gmail.com> - 1.0.0-0.11.b2
- Latest upstream, BZ 1192561.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.10.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.0-0.9.b1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Nov 11 2013 Jon Ciesla <limburgher@gmail.com> - 1.0.0-0.8.b1
- Latest upstream.
- Add python3 support, spec cleanup, BZ 1022851.
- Fixed changelog.

* Fri Sep 13 2013 Jon Ciesla <limburgher@gmail.com> - 1.0.0-0.7.a3
- Latest upstream.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.6.a2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.a2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.4.a2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Tim Waugh <twaugh@redhat.com> - 1.0.0-0.3.a2
- 1.0.0-a2.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.2.a1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 30 2011 Tim Waugh <twaugh@redhat.com> - 1.0.0-0.1.a1
- 1.0.0-a1 (bug #586950).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.1-3
- Rebuild for Python 2.6

* Mon Jun 16 2008 Jeremy Katz <katzj@redhat.com> - 0.4.1-2
- Fix end-of-line in README

* Mon Jun 16 2008 Jeremy Katz <katzj@redhat.com> - 0.4.1-1
- Initial packaging

