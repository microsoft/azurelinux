Summary:        A 2D graphics library.
Name:           cairo
Version:        1.18.0
Release:        1%{?dist}
License:        LGPLv2 OR MPLv1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://cairographics.org
Source0:        https://cairographics.org/releases/%{name}-%{version}.tar.xz


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xrender)

%description
Cairo is a 2D graphics library designed to provide high-quality display
and print output. Currently supported output targets include the X Window
System, in-memory image buffers, and image files (PDF, PostScript, and SVG).
 
Cairo is designed to produce consistent output on all output media while
taking advantage of display hardware acceleration when available.
 
%package        devel
Summary:        Development files for cairo
License:        (LGPLv2 OR MPLv1.1) AND MIT AND Public Domain

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.
 
This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo graphics library.

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

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains tools for working with the cairo graphics library.
 * cairo-trace: Record cairo library calls for later playback

%prep
%autosetup -p1

%build

%meson \
  -Dfreetype=enabled \
  -Dfontconfig=enabled \
  -Dglib=enabled \
  -Dgtk_doc=true \
  -Dspectre=disabled \
  -Dsymbol-lookup=disabled \
  -Dtee=enabled \
  -Dtests=disabled \
  -Dxcb=enabled \
  -Dxlib=enabled \
  %{nil}
%meson_build
%install
%meson_install

%files
%defattr(-,root,root)
%license COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1
%{_libdir}/libcairo.so.*
%{_libdir}/libcairo-script-interpreter.so.*

%files devel
%dir %{_includedir}/cairo/
%{_includedir}/cairo/cairo-deprecated.h
%{_includedir}/cairo/cairo-features.h
%{_includedir}/cairo/cairo-ft.h
%{_includedir}/cairo/cairo.h
%{_includedir}/cairo/cairo-pdf.h
%{_includedir}/cairo/cairo-ps.h
%{_includedir}/cairo/cairo-script-interpreter.h
%{_includedir}/cairo/cairo-svg.h
%{_includedir}/cairo/cairo-tee.h
%{_includedir}/cairo/cairo-version.h
%{_includedir}/cairo/cairo-xlib-xrender.h
%{_includedir}/cairo/cairo-xlib.h
%{_includedir}/cairo/cairo-script.h
%{_includedir}/cairo/cairo-xcb.h
%{_libdir}/libcairo.so
%{_libdir}/libcairo-script-interpreter.so
%{_libdir}/pkgconfig/cairo-fc.pc
%{_libdir}/pkgconfig/cairo-ft.pc
%{_libdir}/pkgconfig/cairo.pc
%{_libdir}/pkgconfig/cairo-pdf.pc
%{_libdir}/pkgconfig/cairo-png.pc
%{_libdir}/pkgconfig/cairo-ps.pc
%{_libdir}/pkgconfig/cairo-script-interpreter.pc
%{_libdir}/pkgconfig/cairo-svg.pc
%{_libdir}/pkgconfig/cairo-tee.pc
%{_libdir}/pkgconfig/cairo-xlib.pc
%{_libdir}/pkgconfig/cairo-xlib-xrender.pc
%{_libdir}/pkgconfig/cairo-script.pc
%{_libdir}/pkgconfig/cairo-xcb-shm.pc
%{_libdir}/pkgconfig/cairo-xcb.pc
%{_datadir}/gtk-doc/html/cairo
 
%files gobject
%{_libdir}/libcairo-gobject.so.2*
 
%files gobject-devel
%{_includedir}/cairo/cairo-gobject.h
%{_libdir}/libcairo-gobject.so
%{_libdir}/pkgconfig/cairo-gobject.pc
 
%files tools
%{_bindir}/cairo-trace
%{_libdir}/cairo/
 
%changelog
* Mon Jan 29 2024 Sean Dougherty <sdougherty@microsoft.com> - 1.18.0-1
- Upgrading to 1.18.0 for Mariner 3.0

* Wed Oct 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.17.4-3
- Adding X components from "UI-cairo".
- Adding the "tools" subpackage.

* Thu Sep 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.17.4-2
- Disabling "symbol-lookup" feature due to compilation errors.

* Fri Mar 26 2021 Thomas Crain <thcrain@microsoft.com> - 1.17.4-1
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
