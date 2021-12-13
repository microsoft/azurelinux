Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:       python-slip
Version:    0.6.4
Release:    21%{?dist}
Summary:    Convenience, extension and workaround code for Python 2.x

License:    GPLv2+
URL:        https://github.com/nphilipp/python-slip
Source0:    https://github.com/nphilipp/python-slip/releases/download/python-slip-%{version}/python-slip-%{version}.tar.bz2
BuildArch:  noarch

BuildRequires:  python3
BuildRequires:  python3-devel

%global _description\
The Simple Library for Python 2.x packages contain miscellaneous code for\
convenience, extension and workaround purposes.\
\
This package provides the "slip" and the "slip.util" modules.

%description %_description

%package -n python3-slip
Summary:    Convenience, extension and workaround code for Python 3.x
Requires:   python3-libselinux

%description -n python3-slip
The Simple Library for Python 3.x packages contain miscellaneous code for
convenience, extension and workaround purposes.

This package provides the "slip" and the "slip.util" modules.

%package -n python3-slip-dbus
Summary:    Convenience functions for dbus services in Python 3.x
Requires:   python3-slip = %{version}-%{release}
Requires:   python3-dbus >= 0.80
# Don't require any of pygobject2/3 because slip.dbus works with either one. In
# theory users of slip.dbus should require one or the other anyway to use the
# main loop.
#
# No hard requirement on polkit to allow minimal installs without polkit and
# its dependencies.
Conflicts:  PolicyKit < 0.8-3
Requires:   python3-decorator
Requires:   python3-six
%{?python_provide:%python_provide python3-slip-dbus}

%description -n python3-slip-dbus
The Simple Library for Python 3.x packages contain miscellaneous code for
convenience, extension and workaround purposes.

This package provides slip.dbus.service.Object, which is a dbus.service.Object
derivative that ends itself after a certain time without being used and/or if
there are no clients anymore on the message bus, as well as convenience
functions and decorators for integrating a dbus service with PolicyKit.

%prep
%setup -q

find . -name '*.py' -o -name '*.py.in' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'


%build

make PYTHON=%{__python3} %{?_smp_mflags}

%install

make install PYTHON=%{__python3} DESTDIR=%buildroot

%files -n python3-slip
%doc COPYING doc/dbus
%dir %{python3_sitelib}/slip/
%{python3_sitelib}/slip/__pycache__
%{python3_sitelib}/slip/__init__.py*
%{python3_sitelib}/slip/util
%{python3_sitelib}/slip/_wrappers
%{python3_sitelib}/slip-%{version}-py%{python3_version}.egg-info

%files -n python3-slip-dbus
%doc doc/dbus/*
%{python3_sitelib}/slip/dbus
%{python3_sitelib}/slip.dbus-%{version}-py%{python3_version}.egg-info

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.6.4-21
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.4-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-18
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-17
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 09 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-14
- Don't require python2 at build time, it is not needed

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.4-13
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-11
- Rebuilt for Python 3.7

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.4-10
- Also rename python-slip-dbus and python-slip-gtk to python2-*
- Add missing %%python_provide macros
- Use new python2- names in dependencies

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.4-8
- Python 2 binary package renamed to python2-slip
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.6.4-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep 18 2015 Nils Philippsen <nils@redhat.com> - 0.6.4-1
- util.files.overwrite_safely(): preserve ownership

* Mon Aug 17 2015 Nils Philippsen <nils@redhat.com> - 0.6.3-1
- wrap up GObject -> GLib change (#1254077)
- fix URLs
- remove some obsolete RPM building cruft

* Thu Aug 13 2015 Nils Philippsen <nils@redhat.com> - 0.6.2-1
- dbus: listen less aggressively on NameOwnerChanged signals
- use GLib instead of GObject for wrapper functions (#1202554)

* Thu Apr 16 2015 Nils Philippsen <nils@redhat.com> - 0.6.1-1
- fix detection of imported gobject flavor (#1194235)

* Tue Oct 22 2013 Nils Philippsen <nils@redhat.com> - 0.6.0-1
- version 0.6.0
  - support Python 3.x
  - fix util.hookable hashing, add Hookable.add_hook_hookable()
- remove our own age-old python directory macros
- fix changelog date

* Fri Mar 08 2013 Nils Philippsen <nils@redhat.com> - 0.4.0-1
- version 0.4.0:
  - get rid of (ancient) PolicyKit-0.x support
  - add basic (experimental, unstable) dbus introspection support
  - learn to cope with polkitd being restarted

* Mon Nov 12 2012 Nils Philippsen <nils@redhat.com> - 0.2.24-1
- dbus.polkit: fall back to unix uids if polkit is not available

* Fri Nov 09 2012 Nils Philippsen <nils@redhat.com> - 0.2.23-1
- default to classic gobject if available
- actually distribute gobject wrapper code

* Fri Nov 09 2012 Nils Philippsen <nils@redhat.com> - 0.2.22-1
- dbus: work with either gobject or gi.repository.GObject (pygobject2/3)

* Mon Oct 22 2012 Nils Philippsen <nils@redhat.com> - 0.2.21-1
- add slip.util.files.symlink_atomically()

* Fri Nov 04 2011 Nils Philippsen <nils@redhat.com> - 0.2.20-1
- revert "preserve signature, docstrings, etc. of decorated methods" (#757517)

* Thu Nov 03 2011 Nils Philippsen <nils@redhat.com> - 0.2.19-1
- allow service object methods to be called locally
- preserve signature, docstrings, etc. of decorated methods

* Wed Oct 19 2011 Nils Philippsen <nils@redhat.com> - 0.2.18-1
- actually use persistent value in Object constructor

* Mon Jun 27 2011 Nils Philippsen <nils@redhat.com> - 0.2.17-1
- fix default timeouts of None in bus objects (#716620)
- reduce proxy method calling overhead a bit more

* Tue Jun 21 2011 Nils Philippsen <nils@redhat.com> - 0.2.16-1
- actually distribute slip.dbus.constants module (#714980)

* Mon Jun 20 2011 Nils Philippsen <nils@redhat.com> - 0.2.15-1
- reduce proxy method call overhead
- fix magic value for infinite timeouts (#708761)

* Mon Oct 11 2010 Nils Philippsen <nils@redhat.com> - 0.2.14-1
- use plain "raise" in some places to ease debugging

* Tue Aug 31 2010 Nils Philippsen <nils@redhat.com> - 0.2.13-1
- revert "use tempfile.mkstemp"

* Tue Aug 24 2010 Nils Philippsen <nils@redhat.com> - 0.2.12-1
- use os.path.abspath instead of .realpath (#615819)
- use tempfile.mkstemp
- don't use hardcoded file ext separator

* Wed Jun 30 2010 Nils Philippsen <nils@redhat.com> - 0.2.11-1
- fix re-raising exceptions
- add slip.util.files.overwrite_safely()

* Fri Jun 11 2010 Nils Philippsen <nils@redhat.com> - 0.2.10-1
- add pygobject2 requirement to dbus subpackage

* Mon Mar 22 2010 Nils Philippsen <nils@redhat.com> - 0.2.9-1
- fix throwing auth fail exceptions

* Thu Mar 11 2010 Nils Philippsen <nils@redhat.com> - 0.2.8-1
- improve polkit.enable_proxy decorator

* Thu Feb 11 2010 Nils Philippsen <nils@redhat.com>
- deprecate IsSystemBusNameAuthorized()

* Tue Sep 29 2009 Nils Philippsen <nils@redhat.com> - 0.2.7-1
- fix persistent service objects

* Mon Sep 28 2009 Nils Philippsen <nils@redhat.com> - 0.2.6-1
- ship all slip.dbus modules (#525790)

* Thu Sep 24 2009 Nils Philippsen <nils@redhat.com> - 0.2.5-1
- make polkit checks in dbus services non-blocking

* Mon Sep 14 2009 Nils Philippsen <nils@redhat.com>
- improve example documentation

* Tue Sep 08 2009 Nils Philippsen <nils@redhat.com> - 0.2.4-1
- fix dbus example

* Tue Sep 01 2009 Nils Philippsen <nils@redhat.com> - 0.2.3-1
- add issamefile(), linkfile(), linkorcopyfile() to slip.util.files

* Tue Sep 01 2009 Nils Philippsen <nils@redhat.com> - 0.2.2-1
- add slip.util.files

* Tue Aug 25 2009 Nils Philippsen <nils@redhat.com> - 0.2.1-1
- ship slip.gtk.tools

* Mon Aug 24 2009 Nils Philippsen <nils@redhat.com> - 0.2.0-1
- use PolicyKit version 1.0 if possible (#518996)
- update and ship dbus README

* Fri Aug 21 2009 Nils Philippsen <nils@redhat.com>
- require polkit >= 0.94 from F-12 on

* Thu Nov 27 2008 Nils Philippsen <nphilipp@redhat.com
- use fedorahosted.org URLs

* Tue Oct 14 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.15
- add slip.dbus.polkit.AreAuthorizationsObtainable()

* Mon Sep 15 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.14
- clarify examples a bit

* Tue Sep 09 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.13
- add working examples

* Fri Aug 29 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.12
- make slip.dbus.service.Object persistence overridable per object

* Tue Aug 05 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.11
- implement freezing/thawing hooks

* Tue Aug 05 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.10
- implement disabling/enabling hooks

* Tue Aug 05 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.9
- make slip.util.hookable more flexible, easier extendable

* Mon Aug 04 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.8
- add slip.util.hookable

* Thu Jul 24 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.7
- fix import error (#456511)

* Wed Jul 23 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.6
- move proxy.polkit_enable to polkit.enable_proxy
- rename polkit.NotAuthorized to NotAuthorizedException, polkit.auth_required
  to require_auth

* Tue Jul 22 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.5
- don't reset timeout on failed polkit authorizations

* Mon Jul 21 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.4
- implement PolicyKit convenience functions and decorators
- rename slip.dbus.service.TimeoutObject -> slip.dbus.service.Object

* Fri Jul 11 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.3
- BR: python-devel

* Fri Jul 11 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.2
- fix more inconsistent tabs/spaces

* Fri Jul 11 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1.1
- fix inconsistent tabs/spaces

* Tue May 27 2008 Nils Philippsen <nphilipp@redhat.com> - 0.1
- move gtk.py -> gtk/__init__.py
- rename gtk.set_autowrap () -> gtk.label_autowrap ()

* Mon May 26 2008 Nils Philippsen <nphilipp@redhat.com>
- initial build
