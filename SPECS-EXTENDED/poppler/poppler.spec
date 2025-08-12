Summary:        PDF rendering library
Name:           poppler
Version:        25.02.0
Release:        1%{?dist}
License:        (GPL-2.0-only OR GPL-3.0-only) AND GPL-2.0-or-later AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Libraries
URL:            https://poppler.freedesktop.org/
Source0:        https://poppler.freedesktop.org/%{name}-%{version}.tar.xz

BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(cairo-pdf)
BuildRequires:  pkgconfig(cairo-ps)
BuildRequires:  pkgconfig(cairo-svg)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(nss)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  boost-devel

Requires:       poppler-data

%description
%{name} is a PDF rendering library.

%package devel
Summary:        Libraries and headers for poppler
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package glib
Summary:        Glib wrapper for poppler
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description glib
%{summary}.

%package glib-devel
Summary:        Development files for glib wrapper
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Suggests:       %{name}-doc = %{version}-%{release}

%description glib-devel
%{summary}.

%package glib-doc
Summary:        Documentation for glib wrapper
BuildArch:      noarch

%description glib-doc
%{summary}.

%package cpp
Summary:        Pure C++ wrapper for poppler
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description cpp
%{summary}.

%package cpp-devel
Summary:        Development files for C++ wrapper
Requires:       %{name}-cpp%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description cpp-devel
%{summary}.

%package utils
Summary:        Command line utilities for converting PDF files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Command line tools for manipulating PDF files and converting them to
other formats.

%prep
%autosetup -p1

chmod -x poppler/CairoFontEngine.cc

%build
%cmake \
 -DENABLE_CMS=lcms2 \
 -DENABLE_DCTDECODER=libjpeg \
 -DENABLE_GTK_DOC=ON \
 -DENABLE_LIBOPENJPEG=openjpeg2 \
 -DENABLE_QT5=OFF \
 -DENABLE_QT6=OFF \
 -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
 -DENABLE_ZLIB=OFF \
 ..
%cmake_build

%install
%cmake_install
%find_lang pdfsig

%check
%make_build test

# verify pkg-config sanity/version
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion poppler)" = "%{version}"
test "$(pkg-config --modversion poppler-cpp)" = "%{version}"
test "$(pkg-config --modversion poppler-glib)" = "%{version}"

%ldconfig_scriptlets

%ldconfig_scriptlets glib

%ldconfig_scriptlets cpp

%files
%doc README.md
%license COPYING
%{_libdir}/libpoppler.so.146*

%files devel
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/libpoppler.so
%dir %{_includedir}/poppler/
# xpdf headers
%{_includedir}/poppler/*.h
%{_includedir}/poppler/fofi/
%{_includedir}/poppler/goo/
%{_includedir}/poppler/splash/

%files glib
%{_libdir}/libpoppler-glib.so.8*
%{_libdir}/girepository-1.0/Poppler-0.18.typelib

%files glib-devel
%{_libdir}/pkgconfig/poppler-glib.pc
%{_libdir}/libpoppler-glib.so
%{_datadir}/gir-1.0/Poppler-0.18.gir
%{_includedir}/poppler/glib/

%files glib-doc
%license COPYING
%{_datadir}/gtk-doc/

%files cpp
%{_libdir}/libpoppler-cpp.so.2*

%files cpp-devel
%{_libdir}/pkgconfig/poppler-cpp.pc
%{_libdir}/libpoppler-cpp.so
%{_includedir}/poppler/cpp

%files utils -f pdfsig.lang
%{_bindir}/pdf*
%{_mandir}/man1/*

%changelog
* Mon Aug 12 2025 Azure Linux Team <azlinux@microsoft.com> - 25.02.0-1
- Original version for Azure Linux
- License Verified
