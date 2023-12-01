Summary:        A 2D graphics library.
Name:           cairo
Version:        1.17.4
Release:        3%{?dist}
License:        LGPLv2 OR MPLv1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://cairographics.org
Source0:        https://cairographics.org/snapshots/%{name}-%{version}.tar.xz

BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  libpng-devel
BuildRequires:  libX11-devel
BuildRequires:  libxml2-devel
BuildRequires:  libXrender-devel
BuildRequires:  pixman-devel
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(xext)

Requires:       expat
Requires:       glib
Requires:       libpng
Requires:       pixman

%description
Cairo is a 2D graphics library with support for multiple output devices.

%package        devel
Summary:        Header and development files
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain

Requires:       %{name} = %{version}-%{release}
Requires:       fontconfig-devel
Requires:       freetype-devel
Requires:       libpng-devel
Requires:       pixman-devel

%description    devel
It contains the libraries and header files to create applications

%package gobject
Summary:        GObject bindings for cairo
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gobject
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains functionality to make cairo graphics library
integrate well with the GObject object system used by GNOME.

%package gobject-devel
Summary:        Development files for cairo-gobject
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain

Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-gobject%{?_isa} = %{version}-%{release}

%description gobject-devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo Gobject library.

%package tools
Summary:        Development tools for cairo

License:        GPLv3

%description tools
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains tools for working with the cairo graphics library.
 * cairo-trace: Record cairo library calls for later playback

%prep
%autosetup -p1

%build
%configure \
        --disable-gl \
        --disable-gtk-doc \
        --disable-static \
        --disable-symbol-lookup \
        --enable-ft \
        --enable-gobject \
        --enable-pdf \
        --enable-ps \
        --enable-svg \
        --enable-tee \
        --enable-win32=no \
        --enable-xlib

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

rm -rf %{buildroot}%{_datadir}/gtk-doc

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1
%{_libdir}/libcairo.so.*
%{_libdir}/libcairo-script-interpreter.so.*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files gobject
%{_libdir}/libcairo-gobject.so.*

%files gobject-devel
%{_includedir}/%{name}/cairo-gobject.h
%{_libdir}/libcairo-gobject.so
%{_libdir}/pkgconfig/cairo-gobject.pc

%files tools
%license util/cairo-trace/COPYING util/cairo-trace/COPYING-GPL-3
%{_bindir}/cairo-trace
%{_libdir}/%{name}/

%changelog
* Wed Oct 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.17.4-3
- Adding X components from "UI-cairo".
- Adding the "tools" subpackage.

* Thu Sep 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.17.4-2
- Disabling "symbol-lookup" feature due to compilation errors.

* Fri Mar 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.17.4-1
- Merge the following releases from 1.0 to dev branch
- niontive@microsoft.com, 1.16.0-5: Fix CVE-2018-19876
- niontive@microsoft.com, 1.17.4-1: Upgrade to version 1.17.4, which resolves CVE-2020-35492. Fix Source URL

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.16.0-5
- Import gobject support from Fedora 32 spec (license: MIT)
- Update URLs to https
- Add missing dependencies on libpng-devel and fontconfig-devel to devel subpackage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.16.0-4
- Added %%license line automatically

*  Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.16.0-3
-  Rename freetype2-devel to freetype-devel.
-  Remove sha1 macro.

*  Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.16.0-2
-  Initial CBL-Mariner import from Photon (license: Apache2).

*  Thu Mar 14 2019 Michelle Wang <michellew@vmware.com> 1.16.0-1
-  Upgrade cairo to 1.16.0 for CVE-2018-18064
-  CVE-2018-18064 is for version up to (including) 1.15.14

*  Tue Sep 11 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.14.12-1
-  Update to version 1.14.12

*  Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-3
-  Fix CVE-2017-9814

*  Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 1.14.8-2
-  Remove %check

*  Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-1
-  Initial version
