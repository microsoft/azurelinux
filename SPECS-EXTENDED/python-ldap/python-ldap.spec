### Abstract ###
# global prerelease b4
%global openldap_version 2.4.45-4
%global _description\
python-ldap provides an object-oriented API for working with LDAP within\
Python programs.  It allows access to LDAP directory servers by wrapping the\
OpenLDAP 2.x libraries, and contains modules for other LDAP-related tasks\
(including processing LDIF, LDAPURLs, LDAPv3 schema, etc.).

Summary:        An object-oriented API to access LDAP directory servers
Name:           python-ldap
Version:        3.4.0
Release:        1%{?dist}
License:        Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://python-ldap.org/
Source0:        https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}%{?prerelease}.tar.gz

# Test dependencies
BuildRequires:  %{_bindir}/tox
BuildRequires:  cyrus-sasl-devel
### Build Dependencies ###
BuildRequires:  gcc
BuildRequires:  openldap >= %{openldap_version}
BuildRequires:  openldap-devel >= %{openldap_version}
BuildRequires:  openssl-devel
BuildRequires:  python3-coverage
BuildRequires:  python3-devel
BuildRequires:  python3-pyasn1 >= 0.3.7
BuildRequires:  python3-pyasn1-modules >= 0.1.5
BuildRequires:  python3-setuptools

%description %{_description}

%package -n     python3-ldap
Summary:        %{summary}
%{?python_provide:%python_provide python3-ldap}
Requires:       openldap >= %{openldap_version}
Requires:       python3-pyasn1 >= 0.3.7
Requires:       python3-pyasn1-modules >= 0.1.5
Requires:       python3-setuptools
Obsoletes:      python3-pyldap < 3
Provides:       python3-pyldap = %{version}-%{release}
Provides:       python3-pyldap%{?_isa} = %{version}-%{release}

%description -n python3-ldap %{_description}

%prep
%setup -q -n %{name}-%{version}%{?prerelease}

# Fix interpreter
find . -name '*.py' | xargs sed -i '1s|^#!/usr/bin/env python|#!%{__python3}|'

# Disable warnings in test to work around "'U' mode is deprecated"
# https://github.com/python-ldap/python-ldap/issues/96
sed -i 's,-Werror,-Wignore,g' tox.ini


%build
%py3_build


%check
# don't download packages
export PIP_INDEX_URL=http://host.invalid./
export PIP_NO_DEPS=yes
TOXENV=py%{python3_version_nodots} LOGLEVEL=10 tox --sitepackages


%install
%py3_install

%files -n python3-ldap
%license LICENCE
%doc CHANGES README TODO Demo
%{python3_sitearch}/_ldap.cpython-*.so
%{python3_sitearch}/ldapurl.py*
%{python3_sitearch}/ldif.py*
%{python3_sitearch}/__pycache__/*
%{python3_sitearch}/slapdtest/
%{python3_sitearch}/ldap/
%{python3_sitearch}/python_ldap-%{version}%{?prerelease}-py%{python3_version}.egg-info/

%changelog
* Tue Sep 19 2023 Archana Choudhary <archana1@microsoft.com> - 3.4.0-1
- Upgrade to 3.4.0 - CVE-2021-46823
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Oct 22 2020 Christian Heimes <cheimes@redhat.com> - 3.3.1-1
- New upstream release 3.3.1

* Tue Oct 13 2020 Alexander Bokovoy <abokovoy@redhat.com> - 3.1.0-10
- Add PyASN.1 fixes from https://github.com/python-ldap/python-ldap/pull/351

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 23 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-8
- Subpackage python2-ldap has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-2
- Rebuilt for Python 3.7

* Fri May 25 2018 Christian Heimes <cheimes@redhat.com> - 3.1.0-1
- New upstream release 3.1.0

* Wed Mar 21 2018 Christian Heimes <cheimes@redhat.com> - 3.0.0-1
- New upstream release 3.0.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-0.5.b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Christian Heimes <cheimes@redhat.com> - 3.0.0-0.4.b4
- New upstream release 3.0.0b4 (RHBZ #1496470)

* Wed Dec 20 2017 Christian Heimes <cheimes@redhat.com> - 3.0.0-0.3.b3
- New upstream release 3.0.0b3 (RHBZ #1496470)

* Mon Dec 11 2017 Christian Heimes <cheimes@redhat.com> - 3.0.0-0.2.b2
- New upstream release 3.0.0b2 (RHBZ #1496470)
- Require OpenLDAP with fix for NSS issue (see #1520990)

* Mon Dec 04 2017 Christian Heimes <cheimes@redhat.com> - 0:3.0.0-0.1.b1
- New upstream release 3.0.0b1 (RHBZ #1496470)
- Resolves RHBZ #1489184
- Enable unittests
- Remove dsml module
- Package python3-ldap, which obsoletes python3-pyldap

* Wed Nov 08 2017 Christian Heimes <cheimes@redhat.com> - 0:2.4.25-9
- Fix issue in pyasn1 patch

* Tue Nov 07 2017 Christian Heimes <cheimes@redhat.com> - 0:2.4.25-8
- Apply fix for pyasn1 >= 0.3

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0:2.4.25-7
- Python 2 binary package renamed to python2-ldap
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.4.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.4.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0:2.4.25-4
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.4.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.25-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 20 2016 Petr Spacek <pspacek@redhat.com> - 2.4.25-1
- New upstream release 2.4.25

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.4.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 29 2014 Petr Spacek <pspacek@redhat.com> - 0:2.4.17-1
- New upstream release adds features required in bug 1122486
- Dependency on pyasn1-modules was added to fix bug 995545

* Thu Sep 25 2014 Petr Spacek <pspacek@redhat.com> - 0:2.4.16-1
- New upstream release fixes bug 1007820
- Dependency on pyasn1 was added to fix bug 995545

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.6-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 24 2010 Parag Nemade <paragn AT fedoraproject.org> - 0:2.3.12-1
- Merge-review cleanup (#226343)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0:2.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jan 14 2010 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.10-1
- Update to 2.3.10
- Change source URI to pypi.python.org.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0:2.3.6-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.6-1
- Update to 2.3.6

* Fri Feb 27 2009 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.5-5
- Fix a build error.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 0:2.3.5-3
- rebuild with new openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0:2.3.5-2
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.5-1
- fix license tag
- update to 2.3.5

* Sun Feb 17 2008 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.1-3.fc9
- Rebuild with GCC 4.3

* Wed Dec 05 2007 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.1-2.fc9
- Rebuild against new openssl.

* Wed Oct 10 2007 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.1-1.fc8
- Update to 2.3.1

* Fri Jun 08 2007 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.0-1.fc8
- Update to 2.3
- Spec file cleanups.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0:2.2.0-3
- rebuild against python 2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Wed May 17 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.0-2
- Put back the epoch line... happy beehive?

* Mon May 15 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.0-1
- Update to 2.2.0
- Update python-ldap-2.0.6-rpath.patch and rename it to
  python-ldap-2.2.0-dirs.patch.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.6-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.6-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> - 2.0.6-5
- rebuilt with new openssl

* Tue Mar 22 2005 Warren Togami <wtogami@redhat.com> - 2.0.6-4
- add LICENCE (#150842)
- simplify python reqs
- remove invalid rpath

* Wed Mar 16 2005 Dan Williams <dcbw@redhat.com> - 0:2.0.6-2
- rebuilt to pick up new libssl.so.5

* Tue Feb  8 2005 David Malcolm <dmalcolm@redhat.com> - 0:2.0.6-1
- 2.0.6

* Tue Nov 16 2004 Nalin Dahyabhai <nalin@redhat.com> - 0:2.0.1-3
- rebuild (#139161)

* Mon Aug 30 2004 David Malcolm <dmalcolm@redhat.com> - 0:2.0.1-2
- Rewrote description; added requirement for openldap

* Tue Aug 17 2004 David Malcolm <dmalcolm@redhat.com> - 0:2.0.1-1
- imported into Red Hat's packaging system from Fedora.us; set release to 1

* Wed Jun 30 2004 Panu Matilainen <pmatilai@welho.com> 0:2.0.1-0.fdr.1
- update to 2.0.1

* Sun Dec 07 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.0-0.fdr.0.4.pre16
- fix spec permissions + release tag order (bug 1099)

* Sat Dec  6 2003 Ville Skyttä <ville.skytta at iki.fi> 0:2.0.0-0.fdr.0.pre16.3
- Stricter python version requirements.
- BuildRequire openssl-devel.
- Explicitly build *.pyo, install them as %%ghost.
- Own more installed dirs.
- Remove $RPM_BUILD_ROOT at start of %%install.

* Wed Dec 03 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.0-0.fdr.0.pre16.2
- duh, build requires python-devel, not just python...

* Wed Dec 03 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.0-0.fdr.0.pre16.1
- Initial Fedora packaging.
