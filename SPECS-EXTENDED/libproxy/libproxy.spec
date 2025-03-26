Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global _privatelibs libpxbackend-1.0[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$
 
Name:           libproxy
Version:        0.5.8
Release:        1%{?dist}
Summary:        A library handling all the details of proxy configuration
 
License:        LGPL-2.1-or-later
URL:            https://libproxy.github.io/libproxy/
Source0:        https://github.com/libproxy/%{name}/archive/refs/tags/%{version}.tar.gz
 
BuildRequires:  gcc
BuildRequires:  meson
#BuildRequires:  /usr/bin/gi-docgen
BuildRequires:  /usr/bin/vapigen
 
BuildRequires:  pkgconfig(duktape)
BuildRequires:  pkgconfig(gio-2.0) >= 2.71.3
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  python3-devel
# For config-gnome
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
 
 
%description
libproxy offers the following features:
 
    * extremely small core footprint
    * minimal dependencies within libproxy core
    * only 4 functions in the stable-ish external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment
 
 
%package        bin
Summary:        Binary to test %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    bin
The %{name}-bin package contains the proxy binary for %{name}
 
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
 
%prep
%autosetup -p1
 
 
%build
%meson \
  -Ddocs=false \
  -Dconfig-gnome=false \
  -Dconfig-kde=true \
  -Dconfig-osx=false \
  -Dconfig-windows=false \
  -Dintrospection=true \
  -Dtests=true \
  -Dvapi=true
%meson_build
 
%install
%meson_install
 
%check
%meson_test
%ldconfig_scriptlets


%files
%doc README.md
%license COPYING
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Libproxy-1.0.typelib
%{_libdir}/libproxy.so.*
%dir %{_libdir}/libproxy
%{_libdir}/libproxy/libpxbackend-1.0.so
 
%files bin
%{_bindir}/proxy
%{_mandir}/man8/proxy.8*
 
%files devel
#%{_docdir}/libproxy-1.0/
%{_includedir}/libproxy/
%{_libdir}/libproxy.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Libproxy-1.0.gir
%dir %{_datadir}/vala/vapi/
%{_datadir}/vala/vapi/libproxy-1.0.deps
%{_datadir}/vala/vapi/libproxy-1.0.vapi


%changelog
* Tue Nov 12 2024 Sumit Jena <v-sumitjena@microsoft.com> - 0.5.8-1
- Update to version 0.5.8

* Wed Mar 02 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.17-5
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- Enabling 'gnome' and 'kde' subpackages.
- License verified.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 David King <amigadave@amigadave.com> - 0.4.17-2
- Rebuilt for Python 3.10 (#1898060)

* Fri May 28 2021 David King <amigadave@amigadave.com> - 0.4.17-1
- Update to 0.4.17

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 David King <amigadave@amigadave.com> - 0.4.15-29
- Tweak KDE conditionals to only apply at runtime

* Mon Nov 30 2020 David King <amigadave@amigadave.com> - 0.4.15-28
- Depend on KDE only on Fedora (#1902608)

* Tue Oct 06 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 0.4.15-27
- Disable mozjs backend by default, obsolete it by webkit subpackage

* Tue Sep 29 2020 David King <amigadave@amigadave.com> - 0.4.15-26
- Fix PAC buffer overflow (#1883584)

* Fri Sep 18 2020 David King <amigadave@amigadave.com> - 0.4.15-25
- Fix CVE-2020-25219 (#1880350)

* Tue Aug 18 2020 Jeff Law <law@redhat.com> - 0.4.15-24
- Force C++14 as this code is not C++17 ready

* Tue Aug 04 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 0.4.15-23
- build with mozjs68
- backport use after free fix for mozjs backend

* Tue Aug 04 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 0.4.15-22
- Fix build by switching to cmake macros instead of make

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-21
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.15-19
- Rebuilt for Python 3.9

* Thu Feb 13 2020 David King <amigadave@amigadave.com> - 0.4.15-18
- Fix build against Python 3.9 (#1791942)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.15-16
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.15-15
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 08 2019 Kalev Lember <klember@redhat.com> - 0.4.15-13
- Build with mozjs60

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 22 2018 David King <amigadave@amigadave.com> - 0.4.15-11
- Add Obsoletes on old Python 2 subpackage (#1634211)

* Thu Sep 20 2018 David King <amigadave@amigadave.com> - 0.4.15-10
- Remove Python 2 subpackage (#1631331)

* Sun Aug 26 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.15-9
- Add patch and build against mozjs 52

* Fri Jul 20 2018 David King <amigadave@amigadave.com> - 0.4.15-8
- Provide direct path to Python 2 (#1604646)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.15-7
- Rebuilt for Python 3.7

* Fri May 04 2018 David King <amigadave@amigadave.com> - 0.4.15-6
- Resurrect an old patch (#1459779)
- Add BuildRequires on gcc-c++
- Switch to %%ldconfig_scriptlets
- Remove obsolete Group tags

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 David King <amigadave@amigadave.com> - 0.4.15-2
- Use pkgconfig for BuildRequires
- Fix crash in pacrunner module (#1459779)

* Tue May 16 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.15-1
- Update to 0.4.15

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 David King <amigadave@amigadave.com> - 0.4.14-1
- Update to 0.4.14

* Sun Jan 01 2017 David King <amigadave@amigadave.com> - 0.4.13-1
- Update to 0.4.13

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.12-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.12-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 04 2016 David King <amigadave@amigadave.com> - 0.4.12-3
- Install bindings for both Python 2 and 3 (#1323251)

* Fri Mar 04 2016 David King <amigadave@amigadave.com> - 0.4.12-2
- Fix a Python bindings crash on 64-bit systems (#1296817)

* Mon Feb 29 2016 David King <amigadave@amigadave.com> - 0.4.12-1
- Update to 0.4.12
- Simplify conditional macros
- Use isa macro when requiring base package
- Use license macro for COPYING
- Use pkgconfig for BuildRequires
- Use javascriptcoregtk-4.0
- Apply an upstream patch to pair new[] with delete[]
- Fix slowdown in KDE plugin
- Make the pacrunner subpackage depend on pacrunner (#1171679)
- Install man page from Debian

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.4.11-11
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Dan Winship <danw@redhat.com> - 0.4.11-8
- Really fix the JS_AbortIfWrongThread crash (#998232)

* Thu Sep 19 2013 Dan Winship <danw@redhat.com> - 0.4.11-7
- Fix file descriptor leak (#911066)
- Fix crash when pacrunner fails (probably because of EMFILE...) (#998232)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 David Woodhouse <David.Woodhouse@intel.com> - 0.4.11-5
- Add PacRunner module now that Fedora has PacRunner

* Mon Jun 03 2013 Colin Walters <walters@redhat.com> - 0.4.11-4
- Add patch to build with mozjs17, use it by default

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 Dan Winship <danw@redhat.com> - 0.4.11-2
- Minor dependency fixes

* Mon Dec 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.11-1
- Update to 0.4.11 -  CVE-2012-5580

* Tue Oct 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.10-1
- Update to 0.4.10
- Fix CVE-2012-4504

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.7-4
- Add upstream patches to use js rather than xulrunner
- Add patch to fix FTBFS on gcc 4.7
- Cleanup spec for latest updates and remove obsolete bits

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.4.7-2
- Rebuild for new libpng

* Tue Jun 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.7-1
- Update to 0.4.7
- libproxy-1.0.pc is now reliable starting with 0.4.7

* Tue Apr 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.7-0.1svn20110412
- Update to 0.4.7 svn20110412
- Add support for webkitgtk3
- Add support for xulrunner 2.0
- fix #683015 - libproxy fails with autoconfiguration
- fix #683018 - libproxy needs BR: NetworkManager-glib-devel  (f14)
- Manually fix libproxy-1.0.pc version field - #664781 / #674854

* Wed Nov 24 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-3
- Fix mozjs/webkit obsoletion - rhbz#656849
- Workaround unreliable Version field in pkg-config - rhbz#656484

* Sun Nov 07 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-1
- Update to 0.4.6
- Fix python module not arch dependant

* Mon Sep 06 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.5-2
- Update to 0.4.5
- Disable mozjs on fedora >= 15
- Disable webkit
- Add libproxy bootstrap option to disable modules.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 13 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.4-6
- Fix libproxy-1.0.pc

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-5
- Re-enable mozjs and webkit

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-4
- Disable mozjs to get around a build error temporarily

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-3
- Disable webkit subpackage in order to resolve circular dep

* Sat Jul 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-2
- Fix missing BuildRequires: libmodman-devel

* Sun Jun 13 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-1
- Update to 0.4.4
- Removed install workarounds (fixed upstream)
- Removed patches (fixed upstream)
- Moved -python to noarch
- Downgrade cmake requirement (upstream change)
- Disabled perl bindings
- Run tests

* Thu Mar 11 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-4
- Add missing libXmu-devel

* Sun Feb 21 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-4
- Globalism and update gecko to 1.9.2
- Avoid rpath on _libdir
- Fix BR for kde4 to kdelibs-devel

* Sun Dec 27 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1
- Avoid dependecies on -python and -bin subpackages
- Create -networkmanager sub-package.

* Thu Sep 24 2009 kwizart < kwizart at gmail.com > - 0.3.0-1
- Update to 0.3.0

* Thu Sep 17 2009 kwizart < kwizart at gmail.com > - 0.2.3-12
- Remove Requirement of %%{name}-pac virtual provides
  from the main package - #524043

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 kwizart < kwizart at gmail.com > - 0.2.3-10
- Rebuild for webkit
- Raise requirement for xulrunner to 1.9.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 kwizart < kwizart at gmail.com > - 0.2.3-8
- Merge NetworkManager module into the main libproxy package
- Main Requires the -python and -bin subpackage
 (splitted for multilibs compliance).

* Fri Oct 24 2008 kwizart < kwizart at gmail.com > - 0.2.3-7
- Disable Gnome/KDE default support via builtin modules.
 (it needs to be integrated via Gconf2/neon instead).

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-6
- Disable Obsoletes.
- Requires ev instead of evr for optionnals sub-packages.

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-5
- Use conditionals build.

* Mon Sep 15 2008 kwizart < kwizart at gmail.com > - 0.2.3-4
- Remove plugin- in the name of the packages

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-3
- Move proxy.h to libproxy/proxy.h
  This will prevent it to be included in the default include path
- Split main to libs and util and use libproxy to install all

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-2
- Rename binding-python to python
- Add Requires: gecko-libs >= %%{gecko_version}
- Fix some descriptions
- Add plugin-webkit package

* Fri Jul 11 2008 kwizart < kwizart at gmail.com > - 0.2.3-1
- Convert to Fedora spec

* Fri Jun 6 2008 - dominique-rpm@leuenberger.net
- Updated to version 0.2.3
* Wed Jun 4 2008 - dominique-rpm@leuenberger.net
- Extended spec file to build all available plugins
* Tue Jun 3 2008 - dominique-rpm@leuenberger.net
- Initial spec file for Version 0.2.2

