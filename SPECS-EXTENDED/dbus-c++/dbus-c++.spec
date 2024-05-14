%bcond_with ecore

Name:          dbus-c++
Version:       0.9.0
Release:       23%{?dist}
Summary:       Native C++ bindings for D-Bus

License:       LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:           https://sourceforge.net/projects/dbus-cplusplus/
Source0:       https://downloads.sourceforge.net/dbus-cplusplus/lib%{name}-%{version}.tar.gz

Patch1: dbus-c++-gcc4.7.patch
Patch2: dbus-c++-linkfix.patch
# Fix collision between macro bind_property in dbus-c++/interface.h and method
# bind_property in glibmm/binding.h
Patch3: dbus-c++-macro_collision.patch
# Remove broken classes for multithreading support
# https://sourceforge.net/p/dbus-cplusplus/patches/18/
Patch4: dbus-c++-threading.patch
# https://sourceforge.net/p/dbus-cplusplus/patches/19/
Patch5: dbus-c++-writechar.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: dbus-devel
BuildRequires: glib2-devel
BuildRequires: autoconf automake libtool
BuildRequires: expat-devel
%if %{with ecore}
BuildRequires: ecore-devel
%endif

%description
dbus-c++ attempts to provide a C++ API for D-Bus.
Subpackages are provided with mainloop integration.

%if %{with ecore}
%package       ecore
Summary:       Ecore library for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description   ecore
This package contains the ecore mainloop library for %{name}
%endif

%package       glib
Summary:       GLib library for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description   glib
This package contains the GLib mainloop library for %{name}

%package       devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      pkgconfig
%description   devel
This package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n lib%{name}-%{version}
sed -i 's/\r//' AUTHORS
sed -i 's/libtoolize --force --copy/libtoolize -if --copy/' bootstrap
%patch 1 -p1 -b .gcc47
%patch 2 -p1 -b .linkfix
%patch 3 -p1 -b .collision
%patch 4 -p1 -b .threading
%patch 5 -p1 -b .writechar

%build
autoreconf -vfi
export CPPFLAGS='%{optflags}' CXXFLAGS='--std=gnu++11 %{optflags}'
%configure --disable-static --disable-tests \
%if %{without ecore}
           --disable-ecore
%else
  ;
%endif
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -print -delete

%ldconfig_scriptlets


%files
%license COPYING
%doc AUTHORS
%{_bindir}/dbusxx-introspect
%{_bindir}/dbusxx-xml2cpp
%{_libdir}/libdbus-c++-1.so.0*

%if %{with ecore}
%files ecore
%{_libdir}/libdbus-c++-ecore-1.so.0*
%endif

%files glib
%{_libdir}/libdbus-c++-glib-1.so.0*

%files devel
%doc TODO
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Tue Jan 12 2021 Joe Schmitt <joschmit@microsoft.com> - 0.9.0-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable ecore support

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.9.0-19
- Rebuild with fixed binutils

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Colin Walters <walters@verbum.org> - 0.9.0-17
- Add a bcond for ecore, some downstream distributions may not want it

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 16 2017 Jonathan Wakely <jwakely@redhat.com> - 0.9.0-13
- Remove broken multi-threading support that doesn't build with GCC 7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Lubomir Rintel <lkundrak@v3.sk> - 0.9.0-10
- Fix FTBFS

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.0-8
- Split ecore/glib mainloop out to subpackage to reduce deps
- Use %%license

* Sun Apr 19 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.0-7
- Rebuilt with gcc5 once again

* Thu Mar 05 2015 Sandro Mani <manisandro@gmail.com> - 0.9.0-6
- Add patch to fix macro macro collision (#1187045)

* Fri Feb 27 2015 Adel Gadllah <adel.gadllah@gmail.com> - 0.9.0-5
- Rebuilt with gcc5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9.0-2
- fix bootstrap script for ppc64le (#1070306)

* Tue Dec 17 2013 Jiri Popelka <jpopelka@redhat.com> - 0.9.0-1
- 0.9.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.17.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.16.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.15.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.14.20090203git13281b3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.13.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.12.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 13 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.11.20090203git13281b3
- Fix FTBS (RH #565052)

* Fri Jul 31 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.10.20090203git13281b3
- Fix build

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.9.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.8.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.7.20090203git13281b3
- bump..

* Wed Feb 18 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.6.20090203git13281b3
- Fix build with new gcc

* Wed Feb 18 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.5.20090203git13281b3
- Add the ability to get the senders unix userid (Patch by Jiri Moskovcak)

* Tue Feb 03 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.4.20090203git13281b3
- Update to new git snapshot
- Should fix RH #483418

* Wed Jul 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.3.20080716git1337c65
- Generate tarball with git-archive
- Fix cflags

* Wed Jul 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.2.20080716git1337c65
- Add commit id to version

* Wed Jul 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.1.20080716git
- Initial package
