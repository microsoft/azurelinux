Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname jabberpy
Name:          %{srcname}
Version:       0.5
# Used like this because upstream releases like 0.5-0
Release:       2%{?dist}
Summary:       Python xmlstream and jabber IM protocol libs

License:       LGPLv2+
URL:           http://sourceforge.net/projects/jabberpy/
Source0:       http://downloads.sf.net/sourceforge/%{srcname}/%{srcname}-%{version}-0.tar.gz
Source1:       %{name}-LICENSE.txt
Patch0:        jabberpy-no-init.patch
Patch1:        jabberpy-clean-sockets.patch
Patch2:        jabberpy-ipv6.patch
Patch3:        jabberpy-sha-deprecation.patch
Patch4:        jabberpy-proxy-read.patch
Patch5:        jabberpy-python3.patch
BuildArch:     noarch

%description
jabber.py is a Python module for the jabber instant messaging
protocol. jabber.py deals with the xml parsing and socket code,
leaving the programmer to concentrate on developing quality jabber
based applications with Python.

%package -n python3-%{srcname}
Summary:        Python xmlstream and jabber IM protocol libs
BuildRequires:  python3-devel

%description -n python3-%{srcname}
jabber.py is a Python module for the jabber instant messaging
protocol. jabber.py deals with the xml parsing and socket code,
leaving the programmer to concentrate on developing quality jabber
based applications with Python.

This module contains python3 bindings.

%prep
%setup -q -n %{srcname}-%{version}-0
chmod -x examples/*.py
%patch0 -p1 -b .no-init
%patch1 -p1 -b .clean-sockets
%patch2 -p0 -b .ipv6
%patch3 -p0 -b .sha-deprecation
%patch4 -p1 -b .proxy
%patch5 -p1 -b .python3

mv %{SOURCE1} ./LICENSE.txt

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE.txt
%doc examples README
%{python3_sitelib}/jabber*

%changelog
* Fri Dec 11 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.5-2
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5-0.46
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5-0.45
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5-0.42
- Subpackage python2-jabberpy has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Jul 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5-0.41
- Update Python macros to new packaging standards
  (See https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5-0.39
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5-0.38
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5-0.34
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.33
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed May  4 2016 Miroslav Suchy <msuchy@redhat.com> 0.5-0.32
- improve python3 support

* Thu Apr 28 2016 Miroslav Suchy <msuchy@redhat.com> 0.5-0.31
- add support for python3
- more of removal of old sha crypto

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul  8 2014 Milan Zazrivec <mzazrivec@redhat.com> 0.5-0.29
- fix sha module deprecation warning
- use blocking read in initial communication with http proxy

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 23 2011 Milan Zazrivec <mzazrivec@redhat.com> 0.5-0.23
- 670881 - IPv6 support for jabberpy

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.5-0.21
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5-0.18
- Rebuild for Python 2.6

* Fri Oct 24 2008 Michael Stahnke <stahnma@fedoraproject.org> 0.5.0.17
- Minor Spec tweaks for review

* Fri Oct 10 2008 Michael Stahnke <stahnma@fedoraproject.org> 0.5-0.16
- Clean up for Fedora Review and submission

* Wed Sep  3 2008 Jesus Rodriguez <jesusr@redhat.com> 0.5-0.15
- remove reliance on external version file

* Tue Oct 09 2007 Pradeep Kilambi <pkilambi@redhat.com>
- clean dangling ports left out by jabberpy

* Mon Jun 14 2004 Mihai Ibanescu <misa@redhat.com>
- Initial build
- Patched to add a __init__ file
