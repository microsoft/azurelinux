Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           python-memcached
Version:        1.58
Release:        13%{?dist}
Summary:        A Python memcached client library

License:        Python
URL:            https://github.com/linsomniac/python-memcached
Source0:        https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-nose
# Required for running test suite
BuildRequires:  %{_bindir}/memcached

%global _description\
This software is a 100% Python interface to the memcached memory cache\
daemon.  It is the client side software which allows storing values in one\
or more, possibly remote, memcached servers.  Search google for memcached\
for more information.

%description %_description


%package -n python3-memcached
Summary: %summary
%{?python_provide:%python_provide python3-memcached}

%description -n python3-memcached %_description


%prep
%autosetup -n %{name}-%{version}


%build
%py3_build


%install
%py3_install


%check
pidfile=$(mktemp)
memcached -d -P $pidfile

%{__python3} -m nose

kill $(cat $pidfile)


%files -n python3-memcached
%license PSL.LICENSE
%doc ChangeLog README.md
%attr(755,root,root) %{python3_sitelib}/memcache.py
%{python3_sitelib}/memcache.py
%{python3_sitelib}/__pycache__/memcache.*
%{python3_sitelib}/python_memcached-%{version}-py*.egg-info/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.58-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.58-11
- Subpackage python2-memcached has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.58-10
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 1.58-6
- Rebuilt for Python 3.7

* Wed May 23 2018 Miro Hrončok <mhroncok@redhat.com> - 1.58-5
- Merge with the Python 3 package
- Run upstream tests

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.58-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.58-2
- Python 2 binary package renamed to python2-memcached
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Tue Aug 29 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 1.58-1
- Upstream 1.58

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.54-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Mar  8 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.54-3
- Use versioned python macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 26 2015 Kevin Fenzi <kevin@scrye.com> - 1.54-1
- Update to 1.54

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 15 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.53-1
- New upstream release 1.53
- Fixing set_multi() so that if the server closes the connection it will no
  longer raise AttributeError
- readline() now will mark the connection dead if the read fails
- Changing check_keys to use re.match() instead of str.translate(), because
  re.match() works with Python < 2.6
- Add a MANIFEST.in file
- Client() now takes a "check_keys" option, which defaults to True
- Converting control character checking of keys based on performance testing of
  alternatives
- Converted unicode tests from using u''
- Doing a "set" after server goes away, raised AttributeError: 'NoneType'
  object has no attribute 'sendall'
- incr/decr return None instead of 0 on server connection failure
- Supports IPv6 connections using: "inet6:[fd00::32:19f7]:11000"

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 01 2012 Radek Novacek <rnovacek@redhat.com> 1.48-2
- Enable running tests in %check

* Wed Oct 31 2012 Radek Novacek <rnovacek@redhat.com> 1.48-1
- Update to 1.48

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Kevin Fenzi <kevin@tummy.vom> - 1.47-1
- Update to 1.47

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.43-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.43-3
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.43-2
- add BR: python-setuptools

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.43-1
- fix license tag
- update to 1.43

* Tue Aug 14 2007 Sean Reifschneider <jafo@tummy.com> 1.39-1
- Update to 1.39 upstream release.

* Sat Aug 11 2007 Sean Reifschneider <jafo@tummy.com> 1.38-1
- Update to 1.38 upstream release.

* Sun Jun 10 2007 Sean Reifschneider <jafo@tummy.com> 1.36-3
- Changes based on feedback from Ruben Kerkhof:
- Fixing license.
- Removing PKG-INFO from doc.
- Fixing summary.
- Removing setuptools build dependency.
- Changing permissions of memcache module to 

* Sat Jun 09 2007 Sean Reifschneider <jafo@tummy.com> 1.36-2
- Adding python-devel build requirement.

* Sat Jun 09 2007 Sean Reifschneider <jafo@tummy.com> 1.36-1
- Initial RPM spec file.
