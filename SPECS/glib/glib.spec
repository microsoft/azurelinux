%define majorver %(echo %{version} | cut -d. -f1-2)
Summary:        Low-level libraries useful for providing data structure handling for C.
Name:           glib
Version:        2.78.1
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://developer.gnome.org/glib/
Source0:        https://ftp.gnome.org/pub/gnome/sources/glib/%{majorver}/%{name}-%{version}.tar.xz
BuildRequires:  cmake
BuildRequires:  gtk-doc
BuildRequires:  libffi-devel
BuildRequires:  libselinux-devel
BuildRequires:  meson
BuildRequires:  pcre-devel
BuildRequires:  pkg-config
BuildRequires:  python3-xml
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  which
BuildRequires:  python3-pygments
Requires:       libffi
Requires:       libselinux
Requires:       pcre-libs
Provides:       glib2 = %{version}-%{release}
Provides:       glib2%{?_isa} = %{version}-%{release}
Provides:       glib2-static = %{version}-%{release}

%description
The GLib package contains a low-level libraries useful for providing data structure handling for C, portability wrappers and interfaces for such runtime functionality as an event loop, threads, dynamic loading and an object system. Development libs and headers are in glib-devel.

%package devel
Summary:        Header files for the glib library
Group:          Development/Libraries
Requires:       glib = %{version}-%{release}
Requires:       glib-schemas = %{version}-%{release}
Requires:       libffi-devel
Requires:       pcre-devel
Requires:       python3-xml
Requires:       python3
Provides:       glib2-devel = %{version}-%{release}
Provides:       glib2-devel%{?_isa} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for the glib library

%package schemas
Summary:        gsettings schemas compiling tool
Group:          Development/Libraries
Requires:       glib
Provides:       glib2-schemas = %{version}-%{release}

%description schemas
Gsettings schemas compiling tool

%package doc
Summary:        A library of handy utility functions
Requires:       %{name} = %{version}-%{release}
Provides:       glib2-doc = %{version}-%{release}
BuildArch:      noarch

%description doc
The glib2-doc package includes documentation for the GLib library.

%prep
%autosetup -p1

%build
%meson \
    -Dgtk_doc=true \
    --default-library=both

%meson_build

%install
%meson_install

mv %{buildroot}%{_bindir}/gio-querymodules %{buildroot}%{_bindir}/gio-querymodules-%{__isa_bits}

# Manually create this directory. The build procedure of glib requires setting -Dfam=true to 
# produce this directory, but this config will introduce new BR that introduces build cycles that 
# can't be resolved. Since the 'fam' feature is not needed currently, we will not enable it.
mkdir -p %{buildroot}%{_libdir}/gio/modules
touch %{buildroot}%{_libdir}/gio/modules/giomodule.cache

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libglib-*.so.*
%{_libdir}/libgthread-*.so.*
%{_libdir}/libgmodule-*.so.*
%{_libdir}/libgio-*.so.*
%{_libdir}/libgobject-*.so.*
%{_libexecdir}/gio-launch-desktop

%files devel
%defattr(-, root, root)
%{_bindir}/*
%exclude %{_bindir}/glib-compile-schemas
%exclude %{_bindir}/gsettings
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/gio/*
%{_libdir}/glib-*/*
%{_includedir}/*
%{_datadir}/*
%exclude %{_datadir}/gtk-doc/html/
%exclude %{_datadir}/glib-2.0/schemas/

%files schemas
%defattr(-, root, root)
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_datadir}/glib-2.0/schemas/*

%files doc
%doc %{_datadir}/gtk-doc/html/*

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 2.78.1-1
- Upgrade to version 2.78.1

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.71.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 10 2022 Henry Li <lihl@microsoft.com> - 2.71.0-1
- Upgrade to version 2.71.0
- Add python3-pygments as BR
- Don't remove pcre sources which no longer apply for the new version
- Fix Source0 URL to use macro to represent major version

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.60.1-6
- Remove manual pkgconfig(*) provides in toolchain specs

* Wed May 19 2021 Nick Samson <nisamson@microsoft.com> - 2.60.1-5
- Removed python2 support

* Wed May 19 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.60.1-4
- Require schemas subpackage from devel subpackage

* Fri Apr 27 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.60.1-3
- Remove CVE-2019-13012 patch (already in the this version)
- Exclude doubly-packaged files from devel subpackage
- Merge the following releases from 1.0 to dev branch
- nisamson@microsoft.com, 2.58.0-7: Added patch for CVE-2020-35457, removed %%sha, license verified.
- oliviacrain@microsoft.com, 2.58.0-8: Added patch for CVE-2021-27218, CVE-2021-27219
- niontive@microsoft.com, 2.58.0-9: Added patch for CVE-2021-28153

* Fri Apr 16 2021 Henry Li <lihl@microsoft.com> - 2.60.1-2
- Add libselinux as runtime requirement for glib

* Fri Apr 16 2021 Henry Li <lihl@microsoft.com> - 2.60.1-1
- Upgrade to version 2.60.1
- Switch to meson build and install
- Fix file section for glib-devel

* Tue Mar 16 2021 Henry Li <lihl@microsoft.com> - 2.58.0-12
- Add gtk-doc as build requirement
- Add --enable-gtk-doc during configuration
- Add glib-doc subpackage and provides glib2-doc from glib-doc

* Tue Feb 23 2021 Henry Li <lihl@microsoft.com> - 2.58.0-11
- Fix file section for glib-devel.

* Tue Jan 12 2021 Ruying Chen <v-ruyche@microsoft.com> - 2.58.0-10
- Build static library and provide glib2-static.

* Thu Dec 10 2020 Joe Schmitt <joschmit@microsoft.com> - 2.58.0-9
- Provide isa versions of glib2 provides.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 2.58.0-8
- Provide glib2 versions from each package.

*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 2.58.0-7
-   Move "Provides:pkgconfig(...)" to glib-devel

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.58.0-6
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.58.0-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jul 09 2019 Ankit Jain <ankitja@vmware.com> - 2.58.0-4
- Fix for CVE-2019-13012

* Mon Jun 03 2019 Ankit Jain <ankitja@vmware.com> - 2.58.0-3
- Fix for CVE-2019-12450

* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> - 2.58.0-2
- glib-devel requires python-xml.

* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> - 2.58.0-1
- Update version to 2.58.0

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.52.1-2
- Requires pcre-libs, BuildRequires libffi-devel.

* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> - 2.52.1-1
- Updated to version 2.52.1-1

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 2.48.2-2
- Modified %check

* Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.48.2-1
- Updated to version 2.48.2-1

* Thu Aug 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.47.6-3
- Update glib require for devel to use the same version and release

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.47.6-2
- GA - Bump release of all rpms

* Thu Apr 14 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.47.6-1
- Updated to version 2.47.6

* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.46.2-1
- Updated to version 2.46.2

* Fri Jun 12 2015 Alexey Makhalov <amakhalov@vmware.com> - 2.42.0-3
- Added glib-schemas package

* Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> - 2.42.0-2
- Added more 'Provides: pkgconfig(...)' for base package

* Thu Nov 06 2014 Sharath George <sharathg@vmware.com> - 2.42.0-1
- Initial version
