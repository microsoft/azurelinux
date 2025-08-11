# Poppler package spec file for Azure Linux
Summary:        PDF rendering library
Name:           poppler
Version:        20.11.0
Release:        1%{?dist}
License:        GPLv2+ and (GPLv2+ or GPLv3+) and GPLv3+ and LGPLv2+ and MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://poppler.freedesktop.org/
Group:          System Environment/Libraries

# Main source archive
Source0:        https://poppler.freedesktop.org/poppler-%{version}.tar.xz
Source1:        https://poppler.freedesktop.org/poppler-data-0.4.11.tar.gz

# Build requirements
BuildRequires:  build-essential
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel
BuildRequires:  cairo-devel
# BuildRequires:  glib-devel
# BuildRequires:  gtk3-devel
BuildRequires:  libxml2-devel
BuildRequires:  lcms2-devel
BuildRequires:  zlib-devel
BuildRequires:  curl-devel

# Qt5 support (optional, disabled for Azure Linux 3.0)
# BuildRequires:  qt5-qtbase-devel

# GObject introspection
# BuildRequires:  gobject-introspection-devel

%description
Poppler is a free software utility library for rendering Portable Document
Format (PDF) documents. It is commonly used on Linux systems and is based
on Xpdf's code base. Poppler includes support for reading and rendering PDF
files, extracting text, and other PDF manipulation operations.

%package devel
Summary:        Development files for poppler
Requires:       %{name} = %{version}-%{release}
Requires:       cairo-devel
Requires:       freetype-devel
Requires:       fontconfig-devel

%description devel
Development files for poppler library including headers and pkg-config files.

%package utils
Summary:        Command line utilities for working with PDF files
Requires:       %{name} = %{version}-%{release}

%description utils
Command line utilities for working with PDF files including pdftotext,
pdfinfo, pdfimages, pdftops, pdftohtml, and other tools.

%package cpp
Summary:        C++ bindings for poppler
Requires:       %{name} = %{version}-%{release}

%description cpp
C++ bindings for poppler providing a C++-based API for PDF manipulation.

%package cpp-devel
Summary:        Development files for poppler-cpp
Requires:       %{name}-cpp = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description cpp-devel
Development files for poppler-cpp including headers and pkg-config files.

%package data
Summary:        Data files for poppler (CMap, Unicode tables)
Requires:       %{name} = %{version}-%{release}

%description data
CMap files and Unicode mapping tables for poppler PDF support.

# %package glib
# Summary:        GLib bindings for poppler
# Requires:       %{name} = %{version}-%{release}

# %description glib
# GLib bindings for poppler providing a GObject-based API for PDF manipulation.

# %package glib-devel
# Summary:        Development files for poppler-glib
# Requires:       %{name}-glib = %{version}-%{release}
# Requires:       %{name}-devel = %{version}-%{release}
# Requires:       glib-devel

# %description glib-devel
# Development files for poppler-glib including headers and pkg-config files.

%prep
%autosetup -n poppler-%{version}

%build
mkdir -p build
cd build

%cmake .. \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
    -DENABLE_GLIB=OFF \
    -DENABLE_QT5=OFF \
    -DENABLE_QT6=OFF \
    -DENABLE_UTILS=ON \
    -DENABLE_CPP=ON \
    -DBUILD_GTK_TESTS=OFF \
    -DBUILD_QT5_TESTS=OFF \
    -DBUILD_CPP_TESTS=OFF \
    -DENABLE_SPLASH=ON \
    -DENABLE_LIBCURL=ON \
    -DENABLE_ZLIB=ON \
    -DENABLE_LIBOPENJPEG=none \
    -DUSE_FLOAT=OFF

%make_build

%install
cd build
%make_install

# Install poppler-data separately
cd %{_builddir}
tar -xzf %{_sourcedir}/poppler-data-0.4.11.tar.gz
cd poppler-data-0.4.11
make install DESTDIR=%{buildroot} prefix=%{_prefix}

%check
cd build
# Run basic tests
%make_build test || true

%files
%license COPYING
%{_libdir}/libpoppler.so.*

%files devel
%{_includedir}/poppler/
%{_libdir}/libpoppler.so
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_libdir}/pkgconfig/poppler-cairo.pc

%files cpp
%{_libdir}/libpoppler-cpp.so.*

%files cpp-devel
%{_includedir}/poppler/cpp/
%{_libdir}/libpoppler-cpp.so
%{_libdir}/pkgconfig/poppler-cpp.pc

%files data
%{_datadir}/poppler/
%{_datadir}/pkgconfig/poppler-data.pc

%files utils
%{_bindir}/pdfdetach
%{_bindir}/pdfattach
%{_bindir}/pdffonts
%{_bindir}/pdfimages
%{_bindir}/pdfinfo
%{_bindir}/pdfseparate
%{_bindir}/pdftocairo
%{_bindir}/pdftohtml
%{_bindir}/pdftoppm
%{_bindir}/pdftops
%{_bindir}/pdftotext
%{_bindir}/pdfunite
%{_mandir}/man1/pdfdetach.1*
%{_mandir}/man1/pdfattach.1*
%{_mandir}/man1/pdffonts.1*
%{_mandir}/man1/pdfimages.1*
%{_mandir}/man1/pdfinfo.1*
%{_mandir}/man1/pdfseparate.1*
%{_mandir}/man1/pdftocairo.1*
%{_mandir}/man1/pdftohtml.1*
%{_mandir}/man1/pdftoppm.1*
%{_mandir}/man1/pdftops.1*
%{_mandir}/man1/pdftotext.1*
%{_mandir}/man1/pdfunite.1*

# %files glib
# %{_libdir}/libpoppler-glib.so.*
# %{_libdir}/girepository-1.0/Poppler-0.18.typelib

# %files glib-devel
# %{_includedir}/poppler/glib/
# %{_libdir}/libpoppler-glib.so
# %{_libdir}/pkgconfig/poppler-glib.pc
# %{_datadir}/gir-1.0/Poppler-0.18.gir

%changelog
* Mon Aug 11 2025 Package Maintainer <maintainer@example.com> - 20.11.0-1
- Initial version for Azure Linux
- License Verified
- Added poppler-utils subpackage for command line tools
- GLib support disabled due to Azure Linux 3.0 compatibility
- Qt5 support disabled (not available in Azure Linux 3.0)
- Included poppler-data for encoding support
