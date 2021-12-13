Vendor:         Microsoft Corporation
Distribution:   Mariner
# When we are bootstrapping, we drop some dependencies.
# Set this to 0 after bootstrapping.
%{!?_with_bootstrap: %global bootstrap 1}

Name:           libproxy
Version:        0.4.15
Release:        20%{?dist}
Summary:        A library handling all the details of proxy configuration

License:        LGPLv2+
URL:            https://libproxy.github.io/libproxy/
Source0:        https://github.com/libproxy/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Taken from the Debian package.
Source1:        proxy.1
# http://code.google.com/p/libproxy/issues/detail?id=152
Patch0:         0001-Add-config-module-for-querying-PacRunner-d-mon.patch
Patch1:         libproxy-0.4.11-crash.patch
Patch2:         libproxy-0.4.15-python3738.patch
# https://github.com/libproxy/libproxy/pull/86
# https://github.com/libproxy/libproxy/pull/87
Patch3:         libproxy-0.4.15-mozjs52.patch
# https://github.com/libproxy/libproxy/pull/95
Patch4:         libproxy-0.4.15-mozjs60.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1880350
Patch5:         libproxy-0.4.15-fix-CVE-2020-25219.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1883584
Patch6:         libproxy-0.4.15-fix-pac-buffer-overflow.patch

BuildRequires:  cmake >= 2.6.0
BuildRequires:  gcc-c++
BuildRequires:  libmodman-devel >= 2.0.1

%if ! 0%{?bootstrap}
# gnome
BuildRequires:  pkgconfig(gio-2.0) >= 2.26
# mozjs
BuildRequires:  pkgconfig(mozjs-60)
# NetworkManager
BuildRequires:  pkgconfig(libnm)
# pacrunner (and NetworkManager)
BuildRequires:  pkgconfig(dbus-1)
# webkit (gtk3)
BuildRequires:  pkgconfig(javascriptcoregtk-4.0)
# kde
BuildRequires:  /usr/bin/kreadconfig5
# Python
BuildRequires:  python3-devel
%else
# Obsoletes of disabled subpackages.
Provides: %{name}-mozjs = %{version}-%{release}
Obsoletes: %{name}-mozjs < %{version}-%{release}
Provides: %{name}-webkitgtk4 = %{version}-%{release}
Obsoletes: %{name}-webkitgtk4 < %{version}-%{release}
%endif
# The Python 2 subpackage was removed. Remove in F32.
Obsoletes: python2-libproxy < %{version}-%{release}


%description
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 


%package        bin
Summary:        Binary to test %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    bin
The %{name}-bin package contains the proxy binary for %{name}


%package -n     python3-%{name}
Summary:        Binding for %{name} and python3
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
The python3 binding for %{name}

%if ! 0%{?bootstrap}
%package        gnome
Summary:        Plugin for %{name} and gnome
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    gnome
The %{name}-gnome package contains the %{name} plugin for gnome.

%package        kde
Summary:        Plugin for %{name} and kde
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       /usr/bin/kreadconfig5

%description    kde
The %{name}-kde package contains the %{name} plugin for kde.

%package        mozjs
Summary:        Plugin for %{name} and mozjs
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-pac = %{version}-%{release}

%description    mozjs
The %{name}-mozjs package contains the %{name} plugin for mozjs.

%package        networkmanager
Summary:        Plugin for %{name} and networkmanager
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    networkmanager
The %{name}-networkmanager package contains the %{name} plugin
for networkmanager.

%package        webkitgtk4
Summary:        Plugin for %{name} and webkitgtk3
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-pac = %{version}-%{release}

%description    webkitgtk4
The %{name}-webkitgtk4 package contains the %{name} plugin for
webkitgtk3.

%package        pacrunner
Summary:        Plugin for %{name} and PacRunner
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-pac = %{version}-%{release}
Requires:       pacrunner

%description    pacrunner
The %{name}-pacrunner package contains the %{name} plugin for
PacRunner.
%endif


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1


%build
%{cmake} \
  -DMODULE_INSTALL_DIR=%{_libdir}/%{name}/%{version}/modules \
  -DWITH_PERL=OFF \
%if ! 0%{?bootstrap}
  -DWITH_GNOME3=ON \
  -DWITH_PYTHON2=OFF \
  -DWITH_PYTHON3=ON \
  -DWITH_WEBKIT3=ON \
  -DWITH_MOZJS=ON \
%else
  -DWITH_PYTHON2=OFF \
  -DWITH_PYTHON3=ON \
%endif
   .
%make_build


%install
%make_install INSTALL="install -p"

#In case all modules are disabled
mkdir -p %{buildroot}%{_libdir}/%{name}/%{version}/modules

# Man page.
install -Dpm 0644 %{SOURCE1} %{buildroot}/%{_mandir}/man1/proxy.1

%if 0%{?bootstrap}
rm %{buildroot}%{_libdir}/%{name}/%{version}/modules/config_kde.so
%endif

%check
make test

%ldconfig_scriptlets


%files 
%doc AUTHORS README
%license COPYING
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules

%files bin
%{_bindir}/proxy
%{_mandir}/man1/proxy.1*


%files -n python3-%{name}
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{name}.*

%if ! 0%{?bootstrap}
%files gnome
%{_libdir}/%{name}/%{version}/modules/config_gnome3.so
%{_libexecdir}/pxgsettings

%files kde
%{_libdir}/%{name}/%{version}/modules/config_kde.so

%files mozjs
%{_libdir}/%{name}/%{version}/modules/pacrunner_mozjs.so

%files networkmanager
%{_libdir}/%{name}/%{version}/modules/network_networkmanager.so

%files webkitgtk4
%{_libdir}/%{name}/%{version}/modules/pacrunner_webkit.so

%files pacrunner
%{_libdir}/%{name}/%{version}/modules/config_pacrunner.so
%endif

%files devel
%{_includedir}/proxy.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%{_datadir}/cmake/Modules/Findlibproxy.cmake


%changelog
* Tue Jan 12 2021 Joe Schmitt <joschmit@microsoft.com> - 0.4.15-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn on bootstrap mode

* Tue Sep 29 2020 David King <amigadave@amigadave.com> - 0.4.15-19
- Fix PAC buffer overflow (#1883584)

* Fri Sep 18 2020 David King <amigadave@amigadave.com> - 0.4.15-18
- Fix CVE-2020-25219 (#1880350)

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

