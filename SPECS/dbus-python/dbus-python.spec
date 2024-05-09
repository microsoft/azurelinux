Summary:        D-Bus Python Bindings
Name:           dbus-python
Version:        1.2.16
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.freedesktop.org/wiki/Software/DBusBindings/
Source0:        https://dbus.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
# borrow centos7 patch to use sitearch properly
Patch0:         0001-Move-python-modules-to-architecture-specific-directo.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1788491
Patch1:         python39.patch

BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  libtool

%description
D-Bus python bindings for use with python programs.

%package -n python3-dbus
Summary:        D-Bus bindings for python3

%{?python_provide:%python_provide python3-dbus}
BuildRequires:  python3-devel
# for py3_build
BuildRequires:  python3dist(setuptools)

%description -n python3-dbus
%{summary}.

%package devel
Summary:        Libraries and headers for dbus-python

%description devel
Headers and static libraries for hooking up custom mainloops to the dbus python
bindings.

%prep
%autosetup -p1

# For new arches (aarch64/ppc64le), and patch0
autoreconf -vif

%build
%set_build_flags
%py3_build
%configure PYTHON="%{__python3}"
%make_build

%install
%py3_install
%make_install

# unpackaged files
rm -fv  %{buildroot}%{python3_sitearch}/*.la
rm -rfv %{buildroot}%{_docdir}/dbus-python/

%check
make check -k || (cat test-suite.log && false)

%files -n python3-dbus
%doc NEWS
%license COPYING
%{python3_sitearch}/*.so
%{python3_sitearch}/dbus/
%{python3_sitearch}/dbus_python*egg-info

%files devel
%doc README ChangeLog doc/API_CHANGES.txt doc/tutorial.txt
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_libdir}/pkgconfig/dbus-python.pc

%changelog
* Fri Jul 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.16-3
- License verified.

* Tue Jan 12 2021 Joe Schmitt <joschmit@microsoft.com> - 1.2.16-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove buildrequires for check

* Tue Feb 11 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.16-1
- Update to 1.2.16 (#1788491)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-9
- Subpackage python2-dbus has been removed
  See https://fedoraproject.org/wiki/Changes/RetirePython2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-7
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 11 2019 Neal Gompa <ngompa13@gmail.com> - 1.2.8-5
- Run setuptools build to generate pythonXdist() metadata (#1663693)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-2
- Rebuilt for Python 3.7

* Wed May 23 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-1
- Update to 1.2.8 (#1539950) (#1578726)
- Cat the logs if tests failed

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.4-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Nov 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.4-11
- Cleanups in packaging

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.4-10
- Also add Provides for the old name without %%_isa
- Use %%python_provide for the python3 subpackage and drop manual Provide which
  conflicts with %%python_provide in the python2 subpackage.

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.4-9
- Python 2 binary package renamed to python2-dbus
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Kevin Fenzi <kevin@scrye.com> - 1.2.4-5
- Rebuild again for Python 3.6

* Sun Dec 11 2016 leigh scott <leigh123linux@googlemail.com> - 1.2.4-4
- Add missing build requires needed for check

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.2.4-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Mar 07 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.2.4-1
- Update to 1.2.4 (#1310915)

* Tue Feb 23 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.2.2-1
- Update to 1.2.2 (#1310915)
- add build requires autoconf-archive

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-12
- Drop object manager patch

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 1.2.0-11
- Rebuilt for Python3.5 rebuild

* Wed Aug 19 2015 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-10
- rebuilt

* Wed Aug 19 2015 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-9
- rebuilt

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-7
- python2_sitelib should be python2_sitearch (#1161121)
- update URL, s/python/python2/ a bit

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.2.0-5
- Add patch needed that adds Object Manager functionality for Fedora server dbus api.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-3
- Drop old python3 conditionals, SPEC cleanups

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-2
- rebuild (f21-python)

* Mon Oct 28 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-1
- dbus-python-1.2.0 is available (#1021817)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-5
- Add upstream patch to fix pygobject 3.8

* Fri Mar 29 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.1.1-4
- Apply patch to support aarch64 (#925236)
- Fix URL

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-3
- python3-dbus subpkg (#892474)
- (main) Provides: python-dbus
- BR: python-docutils
- .spec cosmetics
- skip failed tests on rawhide (#913936)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 07 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-1
- dbus-python-1.1.1 (#800487)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.83.0-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.83.0-4
- Rebuild for Python 2.6

* Tue Sep 16 2008 Marco Pesenti Gritti - 0.83.0-3
- Add patch for https://bugs.freedesktop.org/show_bug.cgi?id=17551

* Tue Aug 05 2008  Huang Peng <phuang@redhat.com> - 0.83.0-2
- Update to 0.83.0.

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.82.4-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.82.4-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 0.82.4-1
- Update to 0.82.4

* Mon Oct 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-3
- Rebuild against new dbus-glib

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.82.0-2
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-1
- Update to 0.82.0
- Put all docs in the usual place

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-3
- Rebuild

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-2
- Don't examine args for functions declared METH_NOARGS (#235017)

* Tue Feb 13 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.2-1
- upgrade to 0.80.2 which fixes some memleaks

* Wed Jan 24 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.1-1
- upgrade to 0.80.1
- remove dependency on Pyrex and libxml2
- some API breakage,
  please see https://dbus.freedesktop.org/doc/dbus-python/NEWS.html
  for notes on changes

* Wed Jan  3 2007 David Zeuthen <davidz@redhat.com> - 0.70-9%{?dist}
- rebuild against new Pyrex

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 0.70-8
- rebuild against python 2.5

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.70-7
- Fix a typo in the spec file

* Fri Aug 18 2006 Karsten Hopp <karsten@redhat.com> - 0.70-6
- require libxml2-python for site-packages/dbus/introspect_parser.py

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-5
- Remove unnecessary obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-4
- Try python_sitearch this time

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Add a BR on dbus-devel

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups
- Add PKG_CONFIG_PATH

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial package import
