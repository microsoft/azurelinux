Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%define oname IPy
Summary:        Python module for handling IPv4 and IPv6 Addresses and Networks
Name:           python-%{oname}
Version:        1.01
Release:        13%{?dist}
URL:            https://github.com/haypo/python-ipy
Source0:        https://files.pythonhosted.org/packages/source/I/IPy/IPy-%{version}.tar.gz#/python-IPy-%{version}.tar.gz
License:        BSD
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch

%description
IPy is a Python module for handling IPv4 and IPv6 Addresses and Networks 
in a fashion similar to perl's Net::IP and friends. The IP class allows 
a comfortable parsing and handling for most notations in use for IPv4 
and IPv6 Addresses and Networks.




%package -n python3-%{oname}
Summary: Python 3 module for handling IPv4 and IPv6 Addresses and Networks
%{?python_provide:%python_provide python3-%{oname}}

%description -n python3-%{oname}
IPy is a Python 3 module for handling IPv4 and IPv6 Addresses and Networks 
in a fashion similar to perl's Net::IP and friends. The IP class allows 
a comfortable parsing and handling for most notations in use for IPv4 
and IPv6 Addresses and Networks.



%prep
%autosetup -n %{oname}-%{version} -p1


%build
%py3_build


%check
PYTHONPATH=$PWD %{__python3} test/test_IPy.py
#PYTHONPATH=$PWD %{__python3} test_doc.py  # FAILS


%install
%py3_install


%files -n python3-%{oname}
%license COPYING
%doc AUTHORS ChangeLog README.rst
%{python3_sitelib}/%{oname}*
%{python3_sitelib}/__pycache__/%{oname}*


%changelog
* Wed Dec 18 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.01-13
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.01-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.01-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.01-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Kevin Fenzi <kevin@scrye.com> - 1.01-1
- Update to 1.0.1. Fixes rhbz#1926615

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.00-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 02 2020 Adam Williamson <awilliam@redhat.com> - 1.00-1
- Update to 1.00
- Backport PR #69 to fix for Python 3.9

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.81-30
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.81-28
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 22 2019 Miro Hrončok <mhroncok@redhat.com> - 0.81-27
- Subpackage python2-IPy has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.81-26
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.81-22
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 03 2017 Miro Hrončok <mhroncok@redhat.com> - 0.81-19
- Modernized SPEC
- Updated source URL to a working one
- Fixed package names (#1440243)
- Actually run the tests (the Makefile is not present)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.81-17
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-16
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 0.81-14
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 0.81-12
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.81-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Dec 13 2013 Dan Walsh <dwalsh@redhat.com> - 0.81-9
- Move python3 bindings to separate package to shrink minimal/cloud install until we change to python3 by default

* Fri Oct 18 2013 Matt Domsch <mdomsch@fedoraproject.org> - 0.81-8
- rebuild

* Fri Oct 18 2013 Matt Domsch <mdomsch@fedoraproject.org> - 0.81-7
- upgrade to v0.81

* Fri Oct 18 2013 Dan Walsh <dwalsh@fedoraproject.org> - 0.75-7
- Add support for python3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Matt Domsch <mdomsch@fedoraproject.org> - 0.75-4
- project URL moved to github

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Matt Domsch <mdomsch@fedoraproject.org> - 0.75-1
- Version 0.75 (2011-04-12)
 * IP('::/0').netmask() gives IP('::') instead of IP('0.0.0.0') (BZ#690625)
 * Fix tests for Python 3.1 and 3.2
 * ip.__nonzero__() and (ipa in ipb) return a bool instead of 0 or 1
 * IP('0.0.0.0/0') + IP('0.0.0.0/0') raises an error, fix written by Arfrever
 * Support Python 3: setup.py runs 2to3
 * Update the ranges for IPv6 IPs
 * Fix reverseName() and reverseNames() for IPv4 in IPv6 addresses
 * Drop support of Python < 2.5
 * Include examples and MANIFEST.in in source build (add them to MANIFEST.in)
 * Remove __rcsid__ constant from IPy module
 * Use xrange() instead of range()
 * Use isinstance(x, int) instead of type(x) == types.IntType
 * Prepare support of Python3 (use integer division: x // y)
 * Fix IP(long) constructor: ensure that the address is not too large
 * Constructor raise a TypeError if the type is not int, long, str or unicode
 * 223.0.0.0/8 is now public (belongs to APNIC)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.70-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 10 2010 Matt Domsch <mdomsch@fedoraproject.org> - 0.70-1
- Version 0.70 (2009-10-29)
  * New "major" version because it may break compatibility
  * Fix __cmp__(): IP('0.0.0.0/0') and IP('0.0.0.0') are not equal
  * Fix IP.net() of the network "::/0": "::" instead of "0.0.0.0".
    IPy 0.63 should fix this bug, but it wasn't.

* Sun Aug 30 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.63-1
- Fix formatting of "IPv4 in IPv6" network: IP('::ffff:192.168.10.0/120')

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.62-2
- Rebuild for Python 2.6

* Sat Nov 22 2008 Matt Domsch <mdomsch@fedoraproject.org> - 0.62-1
- new upstream version
  - Fix reverse DNS of IPv6 address: use ".ip6.arpa." suffix instead of deprecated ".ip6.int." suffix
  - Patch from Aras Vaichas allowing the [-1] operator to work with an IP object of size 1.

* Tue May 20 2008 Matt Domsch <matt@domsch.com> 0.60-1
- with assistance from  Mike Frisch
- 0.60

* Tue Jun 05 2007 Matt Domsch <matt@domsch.com> 0.53-2
- simple cleanups per Fedora package review, with thanks to Nigel Jones.

* Thu May 10 2007 Matt Domsch <matt@domsch.com> 0.53-1
- repackaged for Fedora

* Sat Jan 20 2007 David Walluck <walluck@mandriva.org> 0.52-1mdv2007.0
+ Revision: 110982
- 0.52

* Wed Dec 13 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0:0.51-2mdv2007.1
+ Revision: 96523
- Rebuild against new python

* Thu Nov 02 2006 David Walluck <walluck@mandriva.org> 0:0.51-1mdv2007.1
+ Revision: 75609
- 0.51

* Sun Oct 15 2006 David Walluck <walluck@mandriva.org> 0:0.42-3mdv2007.1
+ Revision: 65303
- sync with 2mdv
- Import python-IPy



* Sat Sep 16 2006 David Walluck <walluck@mandriva.com> 0:0.42-1mdv2007.0
- release
