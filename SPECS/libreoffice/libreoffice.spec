# LibreOffice package spec file for Azure Linux
Summary:        Free and open source office suite
Name:           libreoffice
Version:        25.2.4.3
Release:        1%{?dist}
License:        MPLv2.0 AND LGPLv3+ AND ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.libreoffice.org/
Group:          Applications/Productivity

# Main source archive
Source0:        https://download.documentfoundation.org/libreoffice/src/25.2.4/libreoffice-%{version}.tar.xz

# Build requirements
BuildRequires:  build-essential
BuildRequires:  cmake
BuildRequires:  python3-devel
BuildRequires:  java-11-openjdk-devel
BuildRequires:  ant
BuildRequires:  perl
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gperf
BuildRequires:  zip
BuildRequires:  unzip
BuildRequires:  pkgconfig

# Library dependencies
BuildRequires:  boost-devel
BuildRequires:  cairo-devel
BuildRequires:  cups-devel
BuildRequires:  curl-devel
BuildRequires:  dbus-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib-devel
BuildRequires:  glibc-devel
BuildRequires:  gtk3-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  icu-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  nss-devel
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel

# X11 and graphics
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXrandr-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel

# Optional dependencies
BuildRequires:  hunspell-devel
BuildRequires:  hyphen-devel
BuildRequires:  mythes-devel
BuildRequires:  poppler-devel
BuildRequires:  redland-devel

# Runtime requirements
Requires:       hunspell
Requires:       hyphen
Requires:       mythes
Requires:       poppler
Requires:       java-11-openjdk
Requires:       gtk3

%description
LibreOffice is a powerful office suite; its clean interface and powerful tools
let you unleash your creativity and grow your productivity. LibreOffice embeds
several applications that make it the most powerful Free & Open Source Office
suite on the market: Writer, the word processor, Calc, the spreadsheet
application, Impress, the presentation engine, Draw, the drawing and
flowcharting application, Base, the database and database frontend,
and Math for editing mathematics.

This build has been configured to include the most commonly used features
and components suitable for Azure Linux environments.

%package core
Summary:        Core installation of LibreOffice
Group:          Applications/Productivity
Requires:       %{name}-ure = %{version}-%{release}

%description core
This package provides the core LibreOffice installation including the basic
applications (Writer, Calc, Impress, Draw, Math, Base) without language packs,
help files, or additional components.

%package ure
Summary:        UNO Runtime Environment
Group:          System Environment/Libraries

%description ure
UNO Runtime Environment (URE) is the UNO component technology platform
that provides a runtime environment for UNO components. UNO is the
component model of LibreOffice.

%package writer
Summary:        LibreOffice Writer - Word processor
Group:          Applications/Productivity
Requires:       %{name}-core = %{version}-%{release}

%description writer
LibreOffice Writer is the word processor component of LibreOffice.

%package calc
Summary:        LibreOffice Calc - Spreadsheet
Group:          Applications/Productivity
Requires:       %{name}-core = %{version}-%{release}

%description calc
LibreOffice Calc is the spreadsheet component of LibreOffice.

%package impress
Summary:        LibreOffice Impress - Presentation
Group:          Applications/Productivity
Requires:       %{name}-core = %{version}-%{release}

%description impress
LibreOffice Impress is the presentation component of LibreOffice.

%package draw
Summary:        LibreOffice Draw - Drawing
Group:          Applications/Productivity
Requires:       %{name}-core = %{version}-%{release}

%description draw
LibreOffice Draw is the drawing component of LibreOffice.

%package math
Summary:        LibreOffice Math - Equation editor
Group:          Applications/Productivity
Requires:       %{name}-core = %{version}-%{release}

%description math
LibreOffice Math is the equation editor component of LibreOffice.

%package base
Summary:        LibreOffice Base - Database
Group:          Applications/Productivity
Requires:       %{name}-core = %{version}-%{release}

%description base
LibreOffice Base is the database component of LibreOffice.

%prep
%setup -q -n libreoffice-%{version}

%build
# Set up build environment
export CFLAGS="${CFLAGS:-%optflags}"
export CXXFLAGS="${CXXFLAGS:-%optflags}"
export LDFLAGS="${LDFLAGS:-%__global_ldflags}"

# Configure the build
./autogen.sh \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --disable-ccache \
    --disable-dependency-tracking \
    --disable-static \
    --enable-shared \
    --disable-debug \
    --enable-release-build \
    --enable-python=system \
    --enable-openssl \
    --with-system-libs \
    --with-system-headers \
    --with-system-boost \
    --with-system-cairo \
    --with-system-curl \
    --with-system-dbus \
    --with-system-fontconfig \
    --with-system-freetype \
    --with-system-harfbuzz \
    --with-system-hunspell \
    --with-system-hyphen \
    --with-system-icu \
    --with-system-jpeg \
    --with-system-libpng \
    --with-system-libxml \
    --with-system-mythes \
    --with-system-nss \
    --with-system-openldap \
    --with-system-poppler \
    --with-system-sqlite \
    --with-system-zlib \
    --without-system-jars \
    --without-junit \
    --without-system-apache-commons \
    --with-java-target-version=11 \
    --enable-gtk3 \
    --disable-gtk4 \
    --disable-kde5 \
    --disable-qt5 \
    --disable-qt6 \
    --enable-cups \
    --enable-dbus \
    --enable-gio \
    --enable-scripting-python \
    --disable-scripting-beanshell \
    --disable-scripting-javascript \
    --with-help=html \
    --with-lang="en-US" \
    --without-krb5 \
    --without-gssapi \
    --disable-report-builder \
    --disable-lotuswordpro \
    --disable-coinmp \
    --disable-lpsolve \
    --disable-odk \
    --without-doxygen

# Build LibreOffice
make build-nocheck %{?_smp_mflags}

%install
# Install LibreOffice
make install DESTDIR=%{buildroot}

# Remove unnecessary files
find %{buildroot} -name "*.la" -delete
find %{buildroot} -name "*.a" -delete

# Create desktop files directories
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor

%files
# Meta-package that includes all components
%doc README*
%license COPYING*

%files ure
%{_libdir}/libreoffice/ure/
%{_libdir}/libreoffice/program/uno*

%files core
%{_bindir}/libreoffice
%{_bindir}/soffice
%{_libdir}/libreoffice/program/
%exclude %{_libdir}/libreoffice/program/uno*
%{_datadir}/libreoffice/
%{_datadir}/applications/libreoffice-*.desktop
%{_datadir}/icons/hicolor/*/apps/libreoffice-*.png

%files writer
%{_bindir}/lowriter
%{_libdir}/libreoffice/program/*writer*
%{_datadir}/applications/libreoffice-writer.desktop

%files calc
%{_bindir}/localc
%{_libdir}/libreoffice/program/*calc*
%{_datadir}/applications/libreoffice-calc.desktop

%files impress
%{_bindir}/loimpress
%{_libdir}/libreoffice/program/*impress*
%{_datadir}/applications/libreoffice-impress.desktop

%files draw
%{_bindir}/lodraw
%{_libdir}/libreoffice/program/*draw*
%{_datadir}/applications/libreoffice-draw.desktop

%files math
%{_bindir}/lomath
%{_libdir}/libreoffice/program/*math*
%{_datadir}/applications/libreoffice-math.desktop

%files base
%{_bindir}/lobase
%{_libdir}/libreoffice/program/*base*
%{_datadir}/applications/libreoffice-base.desktop

%post core
/sbin/ldconfig

%postun core
/sbin/ldconfig

%changelog
* Mon Aug 11 2025 Microsoft <azurelinux@microsoft.com> - 25.2.4.3-1
- Initial Azure Linux package for LibreOffice 25.2.4.3
- Built from official LibreOffice source with Azure Linux optimizations
- Configured with system libraries and GTK3 support
- Split into modular subpackages for flexible installation
