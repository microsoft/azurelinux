# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} >= 10
%bcond_with gtk2
%else
%bcond_without gtk2
%endif

%if 0%{?rhel} >= 9
%bcond_with mono
%else
%bcond_without mono
%endif

Name:		libappindicator
Version:	12.10.1
Release:	9%{?dist}
Summary:	Application indicators library

# Automatically converted from old format: LGPLv2 and LGPLv3 - review is highly recommended.
License:	LicenseRef-Callaway-LGPLv2 AND LGPL-3.0-only
URL:		https://launchpad.net/libappindicator
# see https://launchpad.net/ubuntu/+source/libappindicator/12.10.1+20.10.20200706.1-0ubuntu1
Source0:	https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/%{name}/%{version}+20.10.20200706.1-0ubuntu1/%{name}_%{version}+20.10.20200706.1.orig.tar.gz
Patch0:		0001_Fix_mono_dir.patch

BuildRequires: make
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	vala
BuildRequires:	dbus-glib-devel
BuildRequires:	libdbusmenu-devel
%if %{with gtk2}
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	gtk2-devel
%endif
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk3-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
%if %{with mono}
%ifarch %{mono_arches}
BuildRequires:	gtk-sharp2-devel
BuildRequires:	gtk-sharp2-gapi
BuildRequires:	mono-devel
BuildRequires:	mono-nunit-devel
%endif
%endif

%description
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.


%if %{with gtk2}
%package devel
Summary:	Development files for %{name}

Requires:	%{name} = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	libdbusmenu-devel

%description devel
This package contains the development files for the appindicator library.
%endif


%package gtk3
Summary:	Application indicators library - GTK 3

%description gtk3
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.

This package contains the GTK 3 version of this library.


%package gtk3-devel
Summary:	Development files for %{name}-gtk3

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	libdbusmenu-devel

%description gtk3-devel
This package contains the development files for the appindicator-gtk3 library.


%package docs
Summary:	Documentation for %{name} and %{name}-gtk3

BuildArch:	noarch

%description docs
This package contains the documentation for the appindicator and
appindicator-gtk3 libraries.


%if %{with mono}
%ifarch %{mono_arches}
%package sharp
Summary:	Application indicators library - C#

Requires: mono-complete

%description sharp
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.

This package contains the Mono C# bindings for this library.


%package sharp-devel
Summary:	Development files for %{name}-sharp

Requires:	%{name}-sharp = %{version}-%{release}

%description sharp-devel
This package contains the development files for the appindicator-sharp library.
%endif
%endif


%prep
%setup -q -c
%patch -P0 -p1 -b .monodir


sed -i "s#mono-csc#mcs#g" configure.ac
# fix for gtk-doc 1.26
sed -i 's/--nogtkinit//' docs/reference/Makefile.am
gtkdocize --copy
cp -f gtk-doc.make gtk-doc.local.make
autoreconf -vif


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

%if %{with gtk2}
pushd build-gtk2
export CFLAGS="%{optflags} $CFLAGS -Wno-deprecated-declarations -Wno-error"
%configure --with-gtk=2 --enable-gtk-doc --disable-static
# Parallel make, crash the build
make -j1 V=1
popd
%endif

pushd build-gtk3
export CFLAGS="%{optflags} $CFLAGS -Wno-deprecated-declarations"
%configure --with-gtk=3 --enable-gtk-doc --disable-static
# Parallel make, crash the build
make -j1 V=1
popd


%install
%if %{with gtk2}
pushd build-gtk2
make install DESTDIR=%{buildroot}
popd
%endif

pushd build-gtk3
make install DESTDIR=%{buildroot}
popd

find %{buildroot} -type f -name '*.la' -delete


%if %{with gtk2}
%ldconfig_scriptlets
%endif
%ldconfig_scriptlets gtk3


%if %{with gtk2}
%files
%doc AUTHORS README COPYING COPYING.LGPL.2.1
%{_libdir}/libappindicator.so.*


%files devel
%dir %{_includedir}/libappindicator-0.1/
%dir %{_includedir}/libappindicator-0.1/libappindicator/
%{_includedir}/libappindicator-0.1/libappindicator/*.h
%{_libdir}/libappindicator.so
%{_libdir}/pkgconfig/appindicator-0.1.pc
%endif


%files gtk3
%doc AUTHORS README COPYING COPYING.LGPL.2.1
%{_libdir}/libappindicator3.so.*
%{_libdir}/girepository-1.0/AppIndicator3-0.1.typelib


%files gtk3-devel
%dir %{_includedir}/libappindicator3-0.1/
%dir %{_includedir}/libappindicator3-0.1/libappindicator/
%{_includedir}/libappindicator3-0.1/libappindicator/*.h
%{_libdir}/libappindicator3.so
%{_libdir}/pkgconfig/appindicator3-0.1.pc
%{_datadir}/gir-1.0/AppIndicator3-0.1.gir
%{_datadir}/vala/vapi/appindicator3-0.1.vapi
%{_datadir}/vala/vapi/appindicator3-0.1.deps


%files docs
%doc %{_datadir}/gtk-doc/html/libappindicator/


%if %{with mono}
%ifarch %{mono_arches}
%files sharp
%doc AUTHORS README COPYING COPYING.LGPL.2.1
%dir %{_libdir}/appindicator-sharp-0.1/
%{_libdir}/appindicator-sharp-0.1/appindicator-sharp.dll
%{_libdir}/appindicator-sharp-0.1/appindicator-sharp.dll.config
%{_libdir}/appindicator-sharp-0.1/policy.0.0.appindicator-sharp.config
%{_libdir}/appindicator-sharp-0.1/policy.0.0.appindicator-sharp.dll
%{_libdir}/appindicator-sharp-0.1/policy.0.1.appindicator-sharp.config
%{_libdir}/appindicator-sharp-0.1/policy.0.1.appindicator-sharp.dll
%dir %{_prefix}/lib/mono/appindicator-sharp/
%{_prefix}/lib/mono/appindicator-sharp/appindicator-sharp.dll
%{_prefix}/lib/mono/appindicator-sharp/policy.0.0.appindicator-sharp.dll
%dir %{_prefix}/lib/mono/gac/appindicator-sharp/
%dir %{_prefix}/lib/mono/gac/appindicator-sharp/*/
%{_prefix}/lib/mono/gac/appindicator-sharp/*/appindicator-sharp.dll
%{_prefix}/lib/mono/gac/appindicator-sharp/*/appindicator-sharp.dll.config
%dir %{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/
%dir %{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/
%{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/policy.0.0.appindicator-sharp.dll
%{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/policy.0.0.appindicator-sharp.config


%files sharp-devel
%{_libdir}/pkgconfig/appindicator-sharp-0.1.pc

%endif
%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Michel Lind <salimma@fedoraproject.org> - 12.10.1-7
- Drop gtk2 support on EL >= 10

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 12.10.1-6
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 07 2022 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 12.10.1-0
- Upgrade to 12.10.1 to fix bug 2135815

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 26 2022 Neal Gompa <ngompa@fedoraproject.org> - 12.10.0-33
- Disable Mono bindings for RHEL 9+ for now

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Apr 12 2020 Eduardo Echeverria <echevemaster@gmail.com> - 12-10-0-28
- Added mono to sharp sub-package 

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 04 2019 Miro Hrončok <mhroncok@redhat.com> - 12.10.0-26
- Subpackage python2-appindicator has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 12.10.0-24
- Update BRs for vala packaging changes

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Tomáš Popela <tpopela@redhat.com> - 12.10.0-22
- Fix the build due to python_sitearch usage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 10 2018 Tomas Popela <tpopela@redhat.com> - 12.10.0-20
- Fix the build on F28+ with new glib2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 12.10.0-18
- Switch to %%ldconfig_scriptlets

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 12.10.0-17
- Python 2 binary package renamed to python2-appindicator
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 12.10.0-13
- rebuild - mono on aarch64

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-12
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 12.10.0-9
- Rebuild (mono4)

* Sun Jan  4 2015 Peter Robinson <pbrobinson@fedoraproject.org> 12.10.0-8
- Rather than exclude the entire library from non mono arches just don't build the bindings

* Mon Dec 29 2014 Eduardo Echeverria  <echevemaster@gmail.com> - 12.10.0-7
- Added workaround -Wno-deprecated-declarations for fix FTBFS

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 12.10.0-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Dan Horák <dan[at]danny.cz> - 12.10.0-2
- set ExclusiveArch

* Fri May 31 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 12.10.0-1
- Initial Packaging
