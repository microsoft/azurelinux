# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Fedora Review: http://bugzilla.redhat.com/188180

# configure options
# -no-pch disables precompiled headers, make ccache-friendly
%define no_pch -no-pch

# See http://bugzilla.redhat.com/223663
%define multilib_archs x86_64 %{ix86} %{mips} ppc64 ppc64le ppc s390x s390 sparc64 sparcv9
%define multilib_basearchs x86_64 %{mips64} ppc64 ppc64le s390x sparc64

%if 0%{?fedora} || 0%{?rhel} > 6
# use external qt_settings pkg
%define qt_settings 1
%endif

%if (0%{?fedora} && 0%{?fedora} < 26) || (0%{?rhel} > 6 && 0%{?rhel} <= 7)
%global system_clucene 1
%endif

# See http://bugzilla.redhat.com/1279265
%if 0%{?rhel} && 0%{?rhel} <= 7
%global inject_optflags 1
%endif

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

# support qtchooser, except when building for inclusion in a flatpak
%if !0%{?flatpak}
%define qtchooser 1
%endif

%if 0%{?qtchooser}
%define priority 20
%ifarch %{multilib_basearchs}
%define priority 25
%endif
%endif

Summary: Qt toolkit
Name:    qt
Epoch:   1
Version: 4.8.7
Release: 82%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
# Automatically converted from old format: (LGPLv2 with exceptions or GPLv3 with exceptions) and ASL 2.0 and BSD and FTL and MIT - review is highly recommended.
License: (LGPL-2.0-or-later WITH FLTK-exception OR LicenseRef-Callaway-GPLv3-with-exceptions) AND Apache-2.0 AND LicenseRef-Callaway-BSD AND FTL AND LicenseRef-Callaway-MIT
Url:     http://qt-project.org/
%if 0%{?beta:1}
Source0: https://download.qt-project.org/development_releases/qt/4.8/%{version}-%{beta}/qt-everywhere-opensource-src-%{version}-%{beta}.tar.gz
%else
Source0: https://download.qt-project.org/official_releases/qt/4.8/%{version}/qt-everywhere-opensource-src-%{version}.tar.gz
%endif

Obsoletes: qt4 < %{version}-%{release}
Provides: qt4 = %{version}-%{release}
%{?_isa:Provides: qt4%{?_isa} = %{version}-%{release}}

# default Qt config file
Source4: Trolltech.conf

# header file to workaround multilib issue
Source5: qconfig-multilib.h

# set default QMAKE_CFLAGS_RELEASE
Patch2: qt-everywhere-opensource-src-4.8.0-tp-multilib-optflags.patch

# get rid of timestamp which causes multilib problem
Patch4: qt-everywhere-opensource-src-4.8.5-uic_multilib.patch

# reduce debuginfo in qtwebkit (webcore)
Patch5: qt-everywhere-opensource-src-4.8.5-webcore_debuginfo.patch

# cups16 printer discovery
Patch6: qt-cupsEnumDests.patch

# prefer adwaita over gtk+ on DE_GNOME
# https://bugzilla.redhat.com/show_bug.cgi?id=1192453
Patch10: qt-prefer_adwaita_on_gnome.patch

# enable ft lcdfilter
Patch15: qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch

# may be upstreamable, not sure yet
# workaround for gdal/grass crashers wrt glib_eventloop null deref's
Patch23: qt-everywhere-opensource-src-4.6.3-glib_eventloop_nullcheck.patch

# hack out largely useless (to users) warnings about qdbusconnection
# (often in kde apps), keep an eye on https://git.reviewboard.kde.org/r/103699/
Patch25: qt-everywhere-opensource-src-4.8.3-qdbusconnection_no_debug.patch

# lrelease-qt4 tries to run qmake not qmake-qt4 (http://bugzilla.redhat.com/820767)
Patch26: qt-everywhere-opensource-src-4.8.1-linguist_qmake-qt4.patch

# enable debuginfo in libQt3Support
Patch27: qt-everywhere-opensource-src-4.8.1-qt3support_debuginfo.patch

# kde4/multilib QT_PLUGIN_PATH
Patch28: qt-everywhere-opensource-src-4.8.5-qt_plugin_path.patch

## upstreamable bits
# add support for pkgconfig's Requires.private to qmake
Patch50: qt-everywhere-opensource-src-4.8.4-qmake_pkgconfig_requires_private.patch

# FTBFS against newer firebird-4.0.0
Patch51: qt-everywhere-opensource-src-4.8.7-firebird-4.0.0.patch

# workaround major/minor macros possibly being defined already
Patch52: qt-everywhere-opensource-src-4.8.7-QT_VERSION_CHECK.patch

# fix invalid inline assembly in qatomic_{i386,x86_64}.h (de)ref implementations
Patch53: qt-x11-opensource-src-4.5.0-fix-qatomic-inline-asm.patch

# fix invalid assumptions about mysql_config --libs
# http://bugzilla.redhat.com/440673
Patch54: qt-everywhere-opensource-src-4.8.5-mysql_config.patch

# http://bugs.kde.org/show_bug.cgi?id=180051#c22
Patch55: qt-everywhere-opensource-src-4.6.2-cups.patch

# backport https://codereview.qt-project.org/#/c/205874/
Patch56: qt-everywhere-opensource-src-4.8.7-mariadb.patch

# use QMAKE_LFLAGS_RELEASE when building qmake
Patch57: qt-everywhere-opensource-src-4.8.7-qmake_LFLAGS.patch

# Fails to create debug build of Qt projects on mingw (rhbz#653674)
Patch64: qt-everywhere-opensource-src-4.8.5-QTBUG-14467.patch

# fix QTreeView crash triggered by KPackageKit (patch by David Faure)
Patch65: qt-everywhere-opensource-src-4.8.0-tp-qtreeview-kpackagekit-crash.patch

# fix the outdated standalone copy of JavaScriptCore
Patch67: qt-everywhere-opensource-src-4.8.6-s390.patch

# https://bugs.webkit.org/show_bug.cgi?id=63941
# -Wall + -Werror = fail
Patch68: qt-everywhere-opensource-src-4.8.3-no_Werror.patch

# revert qlist.h commit that seems to induce crashes in qDeleteAll<QList (QTBUG-22037)
Patch69: qt-everywhere-opensource-src-4.8.0-QTBUG-22037.patch

# Buttons in Qt applications not clickable when run under gnome-shell (#742658, QTBUG-21900)
Patch71:  qt-everywhere-opensource-src-4.8.5-QTBUG-21900.patch

# workaround
# sql/drivers/tds/qsql_tds.cpp:341:49: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
Patch74: qt-everywhere-opensource-src-4.8.5-tds_no_strict_aliasing.patch

# add missing method for QBasicAtomicPointer on s390(x)
Patch76: qt-everywhere-opensource-src-4.8.0-s390-atomic.patch

# don't spam in release/no_debug mode if libicu is not present at runtime
Patch77: qt-everywhere-opensource-src-4.8.3-icu_no_debug.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=810500
Patch81: qt-everywhere-opensource-src-4.8.2--assistant-crash.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=694385
# https://bugs.kde.org/show_bug.cgi?id=249217
# https://bugreports.qt-project.org/browse/QTBUG-4862
# QDir::homePath() should account for an empty HOME environment variable on X11
Patch82: qt-everywhere-opensource-src-4.8.5-QTBUG-4862.patch

# poll support
Patch83: qt-4.8-poll.patch

# fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
Patch84: qt-everywhere-opensource-src-4.8.5-QTBUG-35459.patch

# systemtrayicon plugin support (for appindicators)
Patch86: qt-everywhere-opensource-src-4.8.6-systemtrayicon.patch

# fixes for LibreOffice from the upstream Qt bug tracker (#1105422):
Patch87: qt-everywhere-opensource-src-4.8.6-QTBUG-37380.patch
Patch88: qt-everywhere-opensource-src-4.8.6-QTBUG-34614.patch
Patch89: qt-everywhere-opensource-src-4.8.6-QTBUG-38585.patch

# build against the system clucene09-core
Patch90: qt-everywhere-opensource-src-4.8.6-system-clucene.patch

# fix arch autodetection for 64-bit MIPS
Patch91: qt-everywhere-opensource-src-4.8.7-mips64.patch

# fix build issue(s) with gcc6
Patch92: qt-everywhere-opensource-src-4.8.7-gcc6.patch

# support alsa-1.1.x
Patch93: qt-everywhere-opensource-src-4.8.7-alsa-1.1.patch

# support OpenSSL 1.1.x, from Debian (Gert Wollny, Dmitry Eremin-Solenikov)
# https://anonscm.debian.org/cgit/pkg-kde/qt/qt4-x11.git/tree/debian/patches/openssl_1.1.patch?h=experimental
# fixes for -openssl-linked by Kevin Kofler
Patch94: qt-everywhere-opensource-src-4.8.7-openssl-1.1.patch

# fix build with ICU >= 59, from OpenSUSE (Fabian Vogt)
# https://build.opensuse.org/package/view_file/KDE:Qt/libqt4/fix-build-icu59.patch?expand=1
Patch95: qt-everywhere-opensource-src-4.8.7-icu59.patch

# workaround qtscript failures when building with f28's gcc8
# https://bugzilla.redhat.com/show_bug.cgi?id=1580047
Patch96: qt-everywhere-opensource-src-4.8.7-gcc8_qtscript.patch

# Fix ordered pointer comparison against zero problem reported by gcc-11
Patch97: qt-everywhere-opensource-src-4.8.7-gcc11.patch

# hardcode the compiler version in the build key once and for all
Patch98: qt-everywhere-opensource-src-4.8.7-hardcode-buildkey.patch

# FTBFS openssl3
Patch99: qt-everywhere-opensource-src-4.8.7-openssl3.patch

# FTBFS icu76
Patch100: qt-4.6-ftbfs-icu76.patch

# upstream patches
# backported from Qt5 (essentially)
# http://bugzilla.redhat.com/702493
# https://bugreports.qt-project.org/browse/QTBUG-5545
Patch102: qt-everywhere-opensource-src-4.8.5-qgtkstyle_disable_gtk_theme_check.patch
# workaround for MOC issues with Boost headers (#756395)
# https://bugreports.qt-project.org/browse/QTBUG-22829
Patch113: qt-everywhere-opensource-src-4.8.6-QTBUG-22829.patch

# aarch64 support, https://bugreports.qt-project.org/browse/QTBUG-35442
Patch180: qt-aarch64.patch

# Fix problem caused by gcc 9 fixing a longstanding bug.
# https://github.com/qt/qtbase/commit/c35a3f519007af44c3b364b9af86f6a336f6411b.patch
Patch181: qt-everywhere-opensource-src-4.8.7-qforeach.patch

## upstream git

## security patches
# CVE-2018-19872 qt: malformed PPM image causing division by zero and crash in qppmhandler.cpp
Patch500: qt-everywhere-opensource-src-4.8.7-crash-in-qppmhandler.patch

# CVE-2020-17507 qt: buffer over-read in read_xbm_body in gui/image/qxbmhandler.cpp
Patch501: qt-CVE-2020-17507.patch

# no CVE qt: Clamp parsed doubles to float representable values
Patch502: qt-everywhere-opensource-src-4.8.7-clamp-parsed-doubles-to-float-representtable-values.patch

# CVE-2020-24741 qt: QLibrary loads libraries relative to CWD which could result in arbitrary code execution
Patch503: qt-everywhere-opensource-src-4.8.5-CVE-2020-24741.patch

# CVE-2023-32573 qt: Uninitialized variable usage in m_unitsPerEm
Patch504: qt-CVE-2023-32573.patch
Patch505: qt-CVE-2023-34410.patch

# desktop files
Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop
Source24: qtdemo.desktop
Source25: qtconfig.desktop

# upstream qt4-logo, http://trolltech.com/images/products/qt/qt4-logo
Source30: hi128-app-qt4-logo.png
Source31: hi48-app-qt4-logo.png

## BOOTSTRAPPING, undef docs, demos, examples, phonon, webkit

## optional plugin bits
# set to -no-sql-<driver> to disable
# set to -qt-sql-<driver> to enable *in* qt library
%global mysql -plugin-sql-mysql
%define odbc -plugin-sql-odbc
%define psql -plugin-sql-psql
%define sqlite -plugin-sql-sqlite
%if 0%{?rhel} && 0%{?rhel} <= 7
%define phonon -phonon
%define phonon_backend -phonon-backend
%endif
%define dbus -dbus-linked
%define graphicssystem -graphicssystem raster
%define gtkstyle -gtkstyle
%if 0%{?fedora} || 0%{?rhel} > 7
# FIXME/TODO: use system webkit for assistant, examples/webkit, demos/browser
%define webkit -webkit
%define ibase -plugin-sql-ibase
%define tds -plugin-sql-tds
%endif
%if 0%{?rhel} && 0%{?rhel} <= 7
%define no_javascript_jit -no-javascript-jit
%define ibase -no-sql-ibase
%define tds -no-sql-tds
%endif
# disable it temporary (firebird build failed on s390x, bz#1969393)
%if 0%{?fedora} > 34
%define ibase -no-sql-ibase
%endif

# workaround FTBFS with gcc9
#if 0%{?fedora} > 29
%if 0
%global no_javascript_jit -no-javascript-jit
%endif

# macros, be mindful to keep sync'd with macros.qt4
Source1: macros.qt4
%define _qt4 %{name}
%define _qt4_prefix %{_libdir}/qt4
%define _qt4_bindir %{_qt4_prefix}/bin
# _qt4_datadir is not multilib clean, and hacks to workaround that breaks stuff.
#define _qt4_datadir %{_datadir}/qt4
%define _qt4_datadir %{_qt4_prefix}
%define _qt4_demosdir %{_qt4_prefix}/demos
%define _qt4_docdir %{_docdir}/qt4
%define _qt4_examplesdir %{_qt4_prefix}/examples
%define _qt4_headerdir %{_includedir} 
%define _qt4_importdir %{_qt4_prefix}/imports 
%define _qt4_libdir %{_libdir}
%define _qt4_plugindir %{_qt4_prefix}/plugins
%define _qt4_sysconfdir %{_sysconfdir}
%define _qt4_translationdir %{_datadir}/qt4/translations

BuildRequires: make
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: gcc-c++
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig
BuildRequires: pkgconfig(alsa) 
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(glib-2.0)
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: pkgconfig(icu-i18n)
%else
BuildRequires: libicu-devel
%endif
## as far as I can tell, this isn't used anywhere, omitting for now
## https://bugzilla.redhat.com/show_bug.cgi?id=1606047
#BuildRequires: pkgconfig(NetworkManager)
%global openssl -openssl-linked
%if 0%{?fedora} == 27
BuildRequires: compat-openssl10-devel
%else
BuildRequires: openssl-devel
%endif
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(xtst) 
BuildRequires: pkgconfig(zlib)
BuildRequires: rsync

%define gl_deps pkgconfig(gl) pkgconfig(glu)
%define x_deps pkgconfig(ice) pkgconfig(sm) pkgconfig(xcursor) pkgconfig(xext) pkgconfig(xfixes) pkgconfig(xft) pkgconfig(xi) pkgconfig(xinerama) pkgconfig(xrandr) pkgconfig(xrender) pkgconfig(xt) pkgconfig(xv) pkgconfig(x11) pkgconfig(xproto)
BuildRequires: %{gl_deps}
BuildRequires: %{x_deps}

%if 0%{?system_clucene}
BuildRequires: clucene09-core-devel >= 0.9.21b-12
%endif

%if "%{?ibase}" != "-no-sql-ibase"
BuildRequires: firebird-devel
%endif

%if "%{?mysql}" == "-no-sql-mysql"
Obsoletes: %{name}-mysql < %{epoch}:%{version}-%{release}
%else
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
BuildRequires: mariadb-connector-c-devel
%else
BuildRequires: mysql-devel >= 4.0
%endif
%endif

%if "%{?phonon_backend}" == "-phonon-backend"
BuildRequires: pkgconfig(gstreamer-0.10) 
BuildRequires: pkgconfig(gstreamer-plugins-base-0.10) 
%endif

%if "%{?gtkstyle}" == "-gtkstyle"
BuildRequires: pkgconfig(gtk+-2.0) 
%endif

%if "%{?psql}" != "-no-sql-psql"
BuildRequires: libpq-devel
%endif

%if "%{?odbc}" != "-no-sql-odbc"
BuildRequires: unixODBC-devel
%endif

%if "%{?sqlite}" != "-no-sql-sqlite"
%define _system_sqlite -system-sqlite
BuildRequires: pkgconfig(sqlite3) 
%endif

Provides:  qt4-sqlite = %{version}-%{release}
%{?_isa:Provides: qt4-sqlite%{?_isa} = %{version}-%{release}}
Obsoletes: qt-sqlite < 1:4.7.1-16
Provides:  qt-sqlite = %{?epoch:%{epoch}:}%{version}-%{release} 
%{?_isa:Provides: qt-sqlite%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}}

%if "%{?tds}" != "-no-sql-tds"
BuildRequires: freetds-devel
%endif

Obsoletes: qgtkstyle < 0.1
Provides:  qgtkstyle = 0.1-1
Requires: %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: ca-certificates
%if 0%{?qt_settings}
Requires: qt-settings
%endif
%if 0%{?qtchooser}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%endif
Recommends: (ibus-qt if ibus)

%description 
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package common
Summary: Common files for Qt
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch
%description common
%{summary}.

%package assistant
Summary: Documentation browser for Qt 4
Requires: %{name}-sqlite%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: qt4-assistant = %{version}-%{release}
Requires: %{name}-x11%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if ! 0%{?system_clucene}
Provides: bundled(clucene09)
%endif
%description assistant
%{summary}.

%package config
Summary: Graphical configuration tool for programs using Qt 4 
# -config introduced in 4.7.1-10 , for upgrade path
# seems to tickle a pk bug, https://bugzilla.redhat.com/674326
#Obsoletes: %{name}-x11 < 1:4.7.1-10
Obsoletes: qt4-config < 4.5.0
Provides:  qt4-config = %{version}-%{release}
Requires: %{name}-x11%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description config 
%{summary}.

%define demos 1
%package demos
Summary: Demonstration applications for %{name}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-doc
%description demos
%{summary}.

%define docs 1
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-assistant
Obsoletes: qt4-doc < %{version}-%{release}
Provides:  qt4-doc = %{version}-%{release}
# help workaround yum bug http://bugzilla.redhat.com/502401
Obsoletes: qt-doc < 1:4.5.1-4
BuildArch: noarch
%description doc
%{summary}.

%package designer-plugin-webkit
Summary: Qt designer plugin for WebKit
Requires: %{name}-x11%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description designer-plugin-webkit
%{summary}.

%package devel
Summary: Development files for the Qt toolkit
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-x11%{?_isa}
Requires: %{name}-sqlite%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# qmake defaults, could also consider something like:
# Requires: (gcc-c++ if redhat-rpm-config
# or
# Recommends: gcc-c++
# or a combination of the 2
Requires: gcc-c++
Requires: %{gl_deps}
Requires: %{x_deps}
Requires: pkgconfig
%if 0%{?phonon:1}
Provides: qt4-phonon-devel = %{version}-%{release}
%endif
Obsoletes: qt4-designer < %{version}-%{release}
Provides:  qt4-designer = %{version}-%{release}
# as long as libQtUiTools.a is included
Provides:  %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt4-static = %{version}-%{release}
Obsoletes: qt4-devel < %{version}-%{release}
Provides:  qt4-devel = %{version}-%{release}
%{?_isa:Provides: qt4-devel%{?_isa} = %{version}-%{release}}
%if (0%{?fedora} && 0%{?inject_optflags}) || (0%{?rhel} > 7 && 0%{?inject_optflags})
# default flags are used, important configuration is contained here (#1279265)
Requires: redhat-rpm-config
%endif
%description devel
This package contains the files necessary to develop
applications using the Qt toolkit.  Includes:
Qt Linguist

# make a devel private subpkg or not?
%define private 1
%package devel-private
Summary: Private headers for Qt toolkit 
Provides: qt4-devel-private = %{version}-%{release}
Provides: %{name}-private-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: qt4-private-devel = %{version}-%{release}
Requires: %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch
%description devel-private
%{summary}.

%define examples 1
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description examples
%{summary}.

%define qvfb 1
%package qvfb
Summary: Virtual frame buffer for Qt for Embedded Linux
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description qvfb
%{summary}.

%package ibase
Summary: IBase driver for Qt's SQL classes
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt4-ibase = %{version}-%{release}
%{?_isa:Provides: qt4-ibase%{?_isa} = %{version}-%{release}}
%description ibase
%{summary}.

%package mysql
Summary: MySQL driver for Qt's SQL classes
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: qt4-MySQL < %{version}-%{release}
Provides:  qt4-MySQL = %{version}-%{release}
Obsoletes: qt4-mysql < %{version}-%{release}
Provides:  qt4-mysql = %{version}-%{release}
%{?_isa:Provides: qt4-mysql%{?_isa} = %{version}-%{release}}
%description mysql 
%{summary}.

%package odbc 
Summary: ODBC driver for Qt's SQL classes
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: qt4-ODBC < %{version}-%{release}
Provides:  qt4-ODBC = %{version}-%{release}
Obsoletes: qt4-odbc < %{version}-%{release}
Provides:  qt4-odbc = %{version}-%{release}
%{?_isa:Provides: qt4-odbc%{?_isa} = %{version}-%{release}}
%description odbc 
%{summary}.

%package postgresql 
Summary: PostgreSQL driver for Qt's SQL classes
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: qt4-PostgreSQL < %{version}-%{release}
Provides:  qt4-PostgreSQL = %{version}-%{release}
Obsoletes: qt4-postgresql < %{version}-%{release}
Provides:  qt4-postgresql = %{version}-%{release}
%{?_isa:Provides: qt4-postgresql%{?_isa} = %{version}-%{release}}
%description postgresql 
%{summary}.

%package tds
Summary: TDS driver for Qt's SQL classes
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: qt4-tds = %{version}-%{release}
%{?_isa:Provides: qt4-tds%{?_isa} = %{version}-%{release}}
%description tds
%{summary}.

%package x11
Summary: Qt GUI-related libraries
# include Obsoletes here to be safe(r) bootstrap-wise with phonon-4.5.0
# that will Provides: it -- Rex
Obsoletes: qt-designer-plugin-phonon < 1:4.7.2-6
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: qt4-x11 < %{version}-%{release}
Provides:  qt4-x11 = %{version}-%{release}
%{?_isa:Provides: qt4-x11%{?_isa} = %{version}-%{release}}
%if 0%{?fedora} || 0%{?rhel} > 7
## add kde-workspace too? -- rex
#Requires: (sni-qt%{?_isa} if plasma-workspace)
## yum-based tools still cannot handle rich deps ^^, so settle for Recommends until fixed
Recommends: sni-qt%{?_isa}
%endif
%description x11
Qt libraries used for drawing widgets and OpenGL items.

%package qdbusviewer
Summary: D-Bus debugger and viewer
# When split out from qt-x11
Obsoletes: qt-x11 < 1:4.8.5-2
Requires: %{name}-x11%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.


%prep
%setup -q -n qt-everywhere-opensource-src-%{version} 

%patch -P4 -p1 -b .uic_multilib
%patch -P5 -p1 -b .webcore_debuginfo
# ie, where cups-1.6+ is present
%if 0%{?fedora} || 0%{?rhel} > 7
#patch6 -p1 -b .cupsEnumDests
%endif
%patch -P10 -p0 -b .prefer_adwaita_on_gnome
%patch -P15 -p1 -b .enable_ft_lcdfilter
%patch -P23 -p1 -b .glib_eventloop_nullcheck
%patch -P25 -p1 -b .qdbusconnection_no_debug
%patch -P26 -p1 -b .linguist_qtmake-qt4
%patch -P27 -p1 -b .qt3support_debuginfo
%patch -P28 -p1 -b .qt_plugin_path
%patch -P50 -p1 -b .qmake_pkgconfig_requires_private
%patch -P51 -p1 -b .firebird
%patch -P52 -p1 -b .QT_VERSION_CHECK
## TODO: still worth carrying?  if so, upstream it.
%patch -P53 -p1 -b .qatomic-inline-asm
## TODO: upstream me
%patch -P54 -p1 -b .mysql_config
%patch -P55 -p1 -b .cups-1
%patch -P56 -p1 -b .mariadb
%patch -P57 -p1 -b .qmake_LFLAGS
%patch -P64 -p1 -b .QTBUG-14467
%patch -P65 -p1 -b .qtreeview-kpackagekit-crash
%patch -P67 -p1 -b .s390
%patch -P68 -p1 -b .no_Werror
%patch -P69 -p1 -b .QTBUG-22037
%patch -P71 -p1 -b .QTBUG-21900
%patch -P74 -p1 -b .tds_no_strict_aliasing
%patch -P76 -p1 -b .s390-atomic
%patch -P77 -p1 -b .icu_no_debug
%patch -P81 -p1 -b .assistant-crash
%patch -P82 -p1 -b .QTBUG-4862
%patch -P83 -p1 -b .poll
%patch -P87 -p1 -b .QTBUG-37380
%patch -P88 -p0 -b .QTBUG-34614
%patch -P89 -p0 -b .QTBUG-38585

%if 0%{?system_clucene}
%patch -P90 -p1 -b .system_clucene
# delete bundled copy
rm -rf src/3rdparty/clucene
%endif
%patch -P91 -p1 -b .mips64
%patch -P92 -p1 -b .gcc6
%patch -P93 -p1 -b .alsa1.1
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
%patch -P94 -p1 -b .openssl1.1
%endif
%patch -P95 -p1 -b .icu59
%if 0%{?fedora} > 27
%patch -P96 -p1 -b .gcc8_qtscript
%endif
%patch -P97 -p1 -b .gcc11
%patch -P98 -p1 -b .hardcode-buildkey
%patch -P99 -p1 -b .ssl3
%patch -P100 -p1 -b .ftbfs-icu76

# upstream patches
%patch -P102 -p1 -b .qgtkstyle_disable_gtk_theme_check
%patch -P113 -p1 -b .QTBUG-22829

%patch -P180 -p1 -b .aarch64
%patch -P181 -p1 -b .qforeach

# upstream git

# security fixes
%patch -P500 -p1 -b .malformed-ppb-image-causing-crash
%patch -P501 -p1 -b .buffer-over-read-in-read_xbm_body
%patch -P502 -p1 -b .clamp-parsed-doubles-to-float-representtable-values
%patch -P503 -p1 -b .CVE-2020-24741
%patch -P504 -p1 -b .CVE-2023-32573
%patch -P505 -p1 -b .CVE-2023-34410

# regression fixes for the security fixes
%patch -P84 -p1 -b .QTBUG-35459

%patch -P86 -p1 -b .systemtrayicon

%define platform linux-g++

# some 64bit platforms assume -64 suffix, https://bugzilla.redhat.com/569542
%if "%{?__isa_bits}"  == "64"
%define platform linux-g++-64
%endif

# https://bugzilla.redhat.com/478481
%ifarch x86_64 aarch64
%define platform linux-g++
%endif

%if 0%{?inject_optflags}
%patch -P2 -p1 -b .multilib-optflags
# drop backup file(s), else they get installed too, http://bugzilla.redhat.com/639463
rm -fv mkspecs/linux-g++*/qmake.conf.multilib-optflags

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

sed -i -e "s|-O2|$RPM_OPT_FLAGS|g" \
  mkspecs/%{platform}/qmake.conf 

sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 $RPM_LD_FLAGS|" \
  mkspecs/common/g++-unix.conf
%endif

# undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs (#193602)
sed -i -e 's|^\(QMAKE_STRIP.*=\).*$|\1|g' mkspecs/common/linux.conf

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  sed -i -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  sed -i -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi

# MIPS does not accept -m64/-m32 flags
%ifarch %{mips}
sed -i -e 's,-m32,,' mkspecs/linux-g++-32/qmake.conf
sed -i -e 's,-m64,,' mkspecs/linux-g++-64/qmake.conf
%endif

# let makefile create missing .qm files, the .qm files should be included in qt upstream
for f in translations/*.ts ; do
  touch ${f%.ts}.qm
done


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

%if 0%{?fedora} || 0%{?rhel} > 7
# workaround for class std::auto_ptr' is deprecated with gcc-6
CXXFLAGS="$CXXFLAGS -std=gnu++98"
# javascriptcore FTBFS with gcc-6
CXXFLAGS="$CXXFLAGS -Wno-deprecated"
%endif

export QTDIR=$PWD
export PATH=$PWD/bin:$PATH
export LD_LIBRARY_PATH=$PWD/lib/
# TODO: opensuse adds -DOPENSSL_LOAD_CONF, find out if we want that too -- rex
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS $RPM_LD_FLAGS"
export MAKEFLAGS="%{?_smp_mflags}"

./configure -v \
  -confirm-license \
  -opensource \
  -optimized-qmake \
  -fast \
  -prefix %{_qt4_prefix} \
  -bindir %{_qt4_bindir} \
  -datadir %{_qt4_datadir} \
  -demosdir %{_qt4_demosdir} \
  -docdir %{_qt4_docdir} \
  -examplesdir %{_qt4_examplesdir} \
  -headerdir %{_qt4_headerdir} \
  -importdir %{_qt4_importdir} \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -sysconfdir %{_qt4_sysconfdir} \
  -translationdir %{_qt4_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -cups \
  -fontconfig \
  -largefile \
  -gtkstyle \
  -no-rpath \
  %{?reduce_relocations} \
  -no-separate-debug-info \
  %{?phonon} %{!?phonon:-no-phonon} \
  %{?phonon_backend} \
  %{?no_pch} \
  %{?no_javascript_jit} \
  -sm \
  -stl \
  -system-libmng \
  -system-libpng \
  -system-libjpeg \
  -system-libtiff \
  -system-zlib \
  -xinput \
  -xcursor \
  -xfixes \
  -xinerama \
  -xshape \
  -xrandr \
  -xrender \
  -xkb \
  -glib \
  -icu \
  %{?openssl} \
  -xmlpatterns \
  %{?dbus} %{!?dbus:-no-dbus} \
  %{?graphicssystem} \
  %{?webkit} %{!?webkit:-no-webkit } \
  %{?ibase} \
  %{?mysql} \
  %{?psql} \
  %{?odbc} \
  %{?sqlite} %{?_system_sqlite} \
  %{?tds} \
  %{!?docs:-nomake docs} \
  %{!?demos:-nomake demos} \
  %{!?examples:-nomake examples}

# verify QT_BUILD_KEY
grep '^#define QT_BUILD_KEY ' src/corelib/global/qconfig.h
QT_BUILD_KEY_COMPILER="$(grep '^#define QT_BUILD_KEY ' src/corelib/global/qconfig.h | cut -d' ' -f5)"
if [ "$QT_BUILD_KEY_COMPILER" != 'g++-4' ]; then
  echo "QT_BUILD_KEY_COMPILER failure"
  exit 1
fi

%if ! 0%{?inject_optflags}
# ensure qmake build using optflags (which can happen if not munging qmake.conf defaults)
make clean -C qmake
%make_build -C qmake \
  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}" \
  QMAKE_STRIP=
%endif

%make_build

# TODO: consider patching tools/tools.pro to enable building this by default
%{?qvfb:%make_build -C tools/qvfb}

# recreate .qm files
bin/lrelease translations/*.ts


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?qvfb}
make install INSTALL_ROOT=%{buildroot} -C tools/qvfb
%find_lang qvfb --with-qt --without-mo
%else
rm -f %{buildroot}%{_qt4_translationdir}/qvfb*.qm
%endif

%if 0%{?private}
# install private headers
# using rsync -R as easy way to preserve relative path names
# we're cheating and using %%_prefix (/usr) directly here
rsync -aR \
  include/Qt{Core,Declarative,Gui,Script}/private \
  src/{corelib,declarative,gui,script}/*/*_p.h \
  %{buildroot}%{_prefix}/
%endif

# Add desktop files, --vendor=qt4 helps avoid possible conflicts with qt3/qt5
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt4" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{?dbus:%{SOURCE23}} %{?demos:%{SOURCE24}} %{SOURCE25}

## pkg-config
# strip extraneous dirs/libraries 
# safe ones
glib2_libs=$(pkg-config --libs glib-2.0 gobject-2.0 gthread-2.0)
if [ "%{?openssl}" == "-openssl-linked" ]; then
ssl_libs=$(pkg-config --libs openssl)
fi
for dep in \
  -laudio -ldbus-1 -lfreetype -lfontconfig ${glib2_libs} \
  -ljpeg -lm -lmng -lpng -lpulse -lpulse-mainloop-glib ${ssl_libs} -lsqlite3 -lz \
  -L/usr/X11R6/lib -L/usr/X11R6/%{_lib} -L%{_libdir} ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la 
#  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done
# riskier
for dep in -ldl -lphonon -lpthread -lICE -lSM -lX11 -lXcursor -lXext -lXfixes -lXft -lXinerama -lXi -lXrandr -lXrender -lXt ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la 
#  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc 
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done

# nuke dangling reference(s) to %buildroot
sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" %{buildroot}%{_qt4_libdir}/*.prl
sed -i -e "s|-L%{_builddir}/qt-everywhere-opensource-src-%{version}%{?beta:-%{beta}}/lib||g" \
  %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc \
  %{buildroot}%{_qt4_libdir}/*.prl

# nuke QMAKE_PRL_LIBS, seems similar to static linking and .la files (#520323)
# don't nuke, just drop -lphonon (above)
#sed -i -e "s|^QMAKE_PRL_LIBS|#QMAKE_PRL_LIBS|" %{buildroot}%{_qt4_libdir}/*.prl

# .la files, die, die, die.
rm -f %{buildroot}%{_qt4_libdir}/lib*.la

%if 0
#if "%{_qt4_docdir}" != "%{_qt4_prefix}/doc"
# -doc make symbolic link to _qt4_docdir
rm -rf %{buildroot}%{_qt4_prefix}/doc
ln -s  ../../share/doc/qt4 %{buildroot}%{_qt4_prefix}/doc
%endif

# hardlink files to %{_bindir}, add -qt4 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt4_bindir}
for i in * ; do
  case "${i}" in
    # qt3 stuff
    assistant|designer|linguist|lrelease|lupdate|moc|qmake|qtconfig|qtdemo|uic)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt4
      ln -sv ${i} ${i}-qt4
      ;;
    # qt5/qtchooser stuff
    qmlviewer)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt4
      ln -sv ${i} ${i}-qt4
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

# _debug targets (see bug #196513)
pushd %{buildroot}%{_qt4_libdir}
for lib in libQt*.so ; do
   libbase=`basename $lib .so | sed -e 's/^lib//'`
#  ln -s $lib lib${libbase}_debug.so
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.so 
done
for lib in libQt*.a ; do
   libbase=`basename $lib .a | sed -e 's/^lib//' `
#  ln -s $lib lib${libbase}_debug.a
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.a
done
popd

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-multilib.h
  ln -sf qconfig-multilib.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig.h
  ln -sf ../QtCore/qconfig.h %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h
%endif

%if "%{_qt4_libdir}" != "%{_libdir}"
  mkdir -p %{buildroot}/etc/ld.so.conf.d
  echo "%{_qt4_libdir}" > %{buildroot}/etc/ld.so.conf.d/qt4-%{__isa_bits}.conf
%endif

# qtchooser conf
%if 0%{?qtchooser}
  mkdir -p %{buildroot}%{_sysconfdir}/xdg/qtchooser
  pushd    %{buildroot}%{_sysconfdir}/xdg/qtchooser
  echo "%{_qt4_bindir}" >  4-%{__isa_bits}.conf
  echo "%{_qt4_prefix}" >> 4-%{__isa_bits}.conf
  # alternatives targets
  touch default.conf 4.conf
  popd
%endif

%if ! 0%{?qt_settings}
# Trolltech.conf
install -p -m644 -D %{SOURCE4} %{buildroot}%{_qt4_sysconfdir}/Trolltech.conf
%endif

# qt4-logo (generic) icons
install -p -m644 -D %{SOURCE30} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qt4-logo.png
install -p -m644 -D %{SOURCE31} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/qt4-logo.png

# assistant icons
install -p -m644 -D tools/assistant/tools/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant.png
install -p -m644 -D tools/assistant/tools/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant.png

# designer icons
install -p -m644 -D tools/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer.png

# linguist icons
for icon in tools/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist.png
done

# qdbusviewer icons
install -p -m644 -D tools/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer.png
install -p -m644 -D tools/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer.png

# Qt.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt.pc<<EOF
prefix=%{_qt4_prefix}
bindir=%{_qt4_bindir}
datadir=%{_qt4_datadir}
demosdir=%{_qt4_demosdir}
docdir=%{_qt4_docdir}
examplesdir=%{_qt4_examplesdir}
headerdir=%{_qt4_headerdir}
importdir=%{_qt4_importdir}
libdir=%{_qt4_libdir}
moc=%{_qt4_bindir}/moc
plugindir=%{_qt4_plugindir}
qmake=%{_qt4_bindir}/qmake
sysconfdir=%{_qt4_sysconfdir}
translationdir=%{_qt4_translationdir}

Name: Qt
Description: Qt Configuration
Version: %{version}
EOF

# rpm macros
install -p -m644 -D %{SOURCE1} \
  %{buildroot}%{rpm_macros_dir}/macros.qt4
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch}:}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt4

# create/own stuff under %%_qt4_docdir
mkdir -p %{buildroot}%{_qt4_docdir}/{html,qch,src}

 # create/own stuff under %%_qt4_plugindir
mkdir -p %{buildroot}%{_qt4_plugindir}/{crypto,gui_platform,styles}

## nuke bundled phonon bits
rm -fv  %{buildroot}%{_qt4_libdir}/libphonon.so*
rm -rfv %{buildroot}%{_libdir}/pkgconfig/phonon.pc
# contents slightly different between phonon-4.3.1 and qt-4.5.0
rm -fv  %{buildroot}%{_includedir}/phonon/phononnamespace.h
# contents dup'd but should remove just in case
rm -fv  %{buildroot}%{_includedir}/phonon/*.h
rm -rfv %{buildroot}%{_qt4_headerdir}/phonon*
#rm -rfv %{buildroot}%{_qt4_headerdir}/Qt/phonon*
rm -fv %{buildroot}%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
rm -fv %{buildroot}%{_qt4_plugindir}/designer/libphononwidgets.so
# backend
rm -fv %{buildroot}%{_qt4_plugindir}/phonon_backend/*_gstreamer.so
rm -fv %{buildroot}%{_datadir}/kde4/services/phononbackends/gstreamer.desktop

# nuke bundled webkit bits 
rm -fv %{buildroot}%{_qt4_datadir}/mkspecs/modules/qt_webkit_version.pri
rm -fv %{buildroot}%{_qt4_headerdir}/Qt/qgraphicswebview.h
rm -fv %{buildroot}%{_qt4_headerdir}/Qt/qweb*.h
rm -fv %{buildroot}%{_qt4_headerdir}/Qt/QtWebKit
rm -frv %{buildroot}%{_qt4_headerdir}/QtWebKit/
rm -frv %{buildroot}%{_qt4_importdir}/QtWebKit/
rm -fv %{buildroot}%{_qt4_libdir}/libQtWebKit*
rm -fv %{buildroot}%{_libdir}/pkgconfig/QtWebKit.pc
rm -frv %{buildroot}%{_qt4_prefix}/tests/

%find_lang qt --with-qt --without-mo

%find_lang assistant --with-qt --without-mo
%find_lang qt_help --with-qt --without-mo
%find_lang qtconfig --with-qt --without-mo
%find_lang qtscript --with-qt --without-mo
cat assistant.lang qt_help.lang qtconfig.lang qtscript.lang >qt-x11.lang

%find_lang designer --with-qt --without-mo
%find_lang linguist --with-qt --without-mo
cat designer.lang linguist.lang >qt-devel.lang



%if 0%{?qtchooser}
%pre
if [ $1 -gt 1 ] ; then
# remove short-lived qt4.conf alternatives
%{_sbindir}/update-alternatives  \
  --remove qtchooser-qt4 \
  %{_sysconfdir}/xdg/qtchooser/qt4-%{__isa_bits}.conf >& /dev/null ||:

%{_sbindir}/update-alternatives  \
  --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/qt4.conf >& /dev/null ||:
fi
%endif

%post
%{?ldconfig}
%if 0%{?qtchooser}
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/qtchooser/4.conf \
  qtchooser-4 \
  %{_sysconfdir}/xdg/qtchooser/4-%{__isa_bits}.conf \
  %{priority}

%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/qtchooser/default.conf \
  qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/4.conf \
  %{priority}
%endif

%postun
%{?ldconfig}
%if 0%{?qtchooser}
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives  \
  --remove qtchooser-4 \
  %{_sysconfdir}/xdg/qtchooser/4-%{__isa_bits}.conf

%{_sbindir}/update-alternatives  \
  --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/4.conf
fi
%endif

%files -f qt.lang
%doc README
%license LICENSE.GPL3 LICENSE.LGPL LGPL_EXCEPTION.txt
%if 0%{?qtchooser}
%dir %{_sysconfdir}/xdg/qtchooser
# not editable config files, so not using %%config here
%ghost %{_sysconfdir}/xdg/qtchooser/default.conf
%ghost %{_sysconfdir}/xdg/qtchooser/4.conf
%{_sysconfdir}/xdg/qtchooser/4-%{__isa_bits}.conf
%endif
%if "%{_qt4_libdir}" != "%{_libdir}"
/etc/ld.so.conf.d/*
%dir %{_qt4_libdir}
%endif
%dir %{_qt4_prefix}
%if "%{_qt4_bindir}" == "%{_bindir}"
%{_qt4_prefix}/bin
%else
%dir %{_qt4_bindir}
%endif
%if "%{_qt4_datadir}" != "%{_datadir}/qt4"
%dir %{_datadir}/qt4
%else
%dir %{_qt4_datadir}
%endif
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/html/
%dir %{_qt4_docdir}/qch/
%dir %{_qt4_docdir}/src/

%if "%{_qt4_sysconfdir}" != "%{_sysconfdir}"
%dir %{_qt4_sysconfdir}
%endif
%if ! 0%{?qt_settings}
%config(noreplace) %{_qt4_sysconfdir}/Trolltech.conf
%endif
%{_qt4_datadir}/phrasebooks/
%{_qt4_libdir}/libQtCore.so.4*
%if 0%{?dbus:1}
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qdbus
%endif
%{_qt4_bindir}/qdbus
%{_qt4_libdir}/libQtDBus.so.4*
%endif
%{_qt4_libdir}/libQtNetwork.so.4*
%{_qt4_libdir}/libQtScript.so.4*
%{_qt4_libdir}/libQtSql.so.4*
%{_qt4_libdir}/libQtTest.so.4*
%{_qt4_libdir}/libQtXml.so.4*
%{_qt4_libdir}/libQtXmlPatterns.so.4*
%dir %{_qt4_plugindir}
%dir %{_qt4_plugindir}/crypto/
%dir %{_qt4_plugindir}/sqldrivers/
%dir %{_qt4_translationdir}/
%{_qt4_plugindir}/sqldrivers/libqsqlite*

%files common
# empty for now, consider: filesystem/dir ownership, licenses

%files assistant
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/assistant*
%endif
%{_qt4_bindir}/assistant*
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*

%files config
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qt*config*
%endif
%{_qt4_bindir}/qt*config*
%{_datadir}/applications/*qtconfig.desktop

%if 0%{?demos}
%files demos
%{_qt4_bindir}/qt*demo*
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qt*demo*
%endif
%{_datadir}/applications/*qtdemo.desktop
%{_qt4_demosdir}/
%endif

%if "%{?webkit}" == "-webkit"
%files designer-plugin-webkit
%{_qt4_plugindir}/designer/libqwebview.so
%endif

%files devel -f qt-devel.lang
%{rpm_macros_dir}/macros.qt4
%{_qt4_bindir}/lconvert
%{_qt4_bindir}/lrelease*
%{_qt4_bindir}/lupdate*
%{_qt4_bindir}/moc*
%{_qt4_bindir}/pixeltool*
%{_qt4_bindir}/qdoc3*
%{_qt4_bindir}/qmake*
%{_qt4_bindir}/qmlviewer*
%{_qt4_bindir}/qmlplugindump
%{_qt4_bindir}/qt3to4
%{_qt4_bindir}/qttracereplay
%{_qt4_bindir}/rcc*
%{_qt4_bindir}/uic*
%{_qt4_bindir}/qcollectiongenerator
%if 0%{?dbus:1}
%{_qt4_bindir}/qdbuscpp2xml
%{_qt4_bindir}/qdbusxml2cpp
%endif
%{_qt4_bindir}/qhelpconverter
%{_qt4_bindir}/qhelpgenerator
%{_qt4_bindir}/xmlpatterns
%{_qt4_bindir}/xmlpatternsvalidator
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/moc*
%{_bindir}/uic*
%{_bindir}/designer*
%{_bindir}/linguist*
%{_bindir}/lconvert
%{_bindir}/pixeltool
%{_bindir}/qcollectiongenerator
%{_bindir}/qdoc3
%{_bindir}/qmake*
%{_bindir}/qmlviewer*
%{_bindir}/qt3to4
%{_bindir}/qttracereplay
%if 0%{?dbus:1}
%{_bindir}/qdbuscpp2xml
%{_bindir}/qdbusxml2cpp
%endif
%{_bindir}/qhelpconverter
%{_bindir}/qhelpgenerator
%{_bindir}/qmlplugindump
%{_bindir}/rcc
%{_bindir}/xmlpatterns
%{_bindir}/xmlpatternsvalidator
%endif
%if "%{_qt4_headerdir}" != "%{_includedir}"
%dir %{_qt4_headerdir}/
%endif
%{_qt4_headerdir}/*
%{_qt4_datadir}/mkspecs/
%if "%{_qt4_datadir}" != "%{_qt4_prefix}"
%{_qt4_prefix}/mkspecs/
%endif
%{_qt4_datadir}/q3porting.xml
%if 0%{?phonon:1}
## nuke this one too?  -- Rex
%{_qt4_libdir}/libphonon.prl
%endif
%{_qt4_libdir}/libQt*.so
%{_qt4_libdir}/libQtUiTools*.a
%{_qt4_libdir}/libQt*.prl
%{_libdir}/pkgconfig/*.pc
# Qt designer
%{_qt4_bindir}/designer*
%{_datadir}/applications/*designer.desktop
%{_datadir}/icons/hicolor/*/apps/designer*
%{?docs:%{_qt4_docdir}/qch/designer.qch}
# Qt Linguist
%{_qt4_bindir}/linguist*
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist*
%{?docs:%{_qt4_docdir}/qch/linguist.qch}
%if 0%{?private}
%exclude %{_qt4_headerdir}/*/private/

%files devel-private
%{_qt4_headerdir}/QtCore/private/
%{_qt4_headerdir}/QtDeclarative/private/
%{_qt4_headerdir}/QtGui/private/
%{_qt4_headerdir}/QtScript/private/
%{_qt4_headerdir}/../src/corelib/
%{_qt4_headerdir}/../src/declarative/
%{_qt4_headerdir}/../src/gui/
%{_qt4_headerdir}/../src/script/
%endif

%if 0%{?docs}
%files doc
%{_qt4_docdir}/html/*
%{_qt4_docdir}/qch/*.qch
%exclude %{_qt4_docdir}/qch/designer.qch
%exclude %{_qt4_docdir}/qch/linguist.qch
%{_qt4_docdir}/src/*
#{_qt4_prefix}/doc
%endif

%if 0%{?examples}
%files examples
%{_qt4_examplesdir}/
%endif

%if 0%{?qvfb}
%files qvfb -f qvfb.lang
%{_bindir}/qvfb
%{_qt4_bindir}/qvfb
%endif

%if "%{?ibase}" == "-plugin-sql-ibase"
%files ibase
%{_qt4_plugindir}/sqldrivers/libqsqlibase*
%endif

%if "%{?mysql}" == "-plugin-sql-mysql"
%files mysql
%{_qt4_plugindir}/sqldrivers/libqsqlmysql*
%endif

%if "%{?odbc}" == "-plugin-sql-odbc"
%files odbc 
%{_qt4_plugindir}/sqldrivers/libqsqlodbc*
%endif

%if "%{?psql}" == "-plugin-sql-psql"
%files postgresql 
%{_qt4_plugindir}/sqldrivers/libqsqlpsql*
%endif

%if "%{?tds}" == "-plugin-sql-tds"
%files tds
%{_qt4_plugindir}/sqldrivers/libqsqltds*
%endif

%ldconfig_scriptlets x11

%files x11 -f qt-x11.lang
%dir %{_qt4_importdir}/
%{_qt4_importdir}/Qt/
%{_qt4_libdir}/libQt3Support.so.4*
%{_qt4_libdir}/libQtCLucene.so.4*
%{_qt4_libdir}/libQtDesigner.so.4*
%{_qt4_libdir}/libQtDeclarative.so.4*
%{_qt4_libdir}/libQtDesignerComponents.so.4*
%{_qt4_libdir}/libQtGui.so.4*
%{_qt4_libdir}/libQtHelp.so.4*
%{_qt4_libdir}/libQtMultimedia.so.4*
%{_qt4_libdir}/libQtOpenGL.so.4*
%{_qt4_libdir}/libQtScriptTools.so.4*
%{_qt4_libdir}/libQtSvg.so.4*
%{_qt4_plugindir}/*
%exclude %{_qt4_plugindir}/crypto
%if "%{?webkit}" == "-webkit"
%exclude %{_qt4_plugindir}/designer/libqwebview.so
%endif
%exclude %{_qt4_plugindir}/sqldrivers
%{_datadir}/icons/hicolor/*/apps/qt4-logo.*

%if 0%{?dbus:1}
%post qdbusviewer
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans qdbusviewer
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun qdbusviewer
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files qdbusviewer
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qdbusviewer
%endif
%{_qt4_bindir}/qdbusviewer
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer.*
%endif


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-81
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 24 2025 Than Ngo <than@redhat.com> - 1:4.8.7-80
- Fix rhbz#2341255, FTBFS due to new icu76

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-79
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1:4.8.7-78
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-77
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-74
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 09 2023 Than Ngo <than@redhat.com> - 4.8.7-73
- fix #2212749, CVE-2023-34410

* Thu May 18 2023 Than Ngo <than@redhat.com> - 4.8.7-72
- fix #2208136, CVE-2023-32573 Uninitialized variable usage in m_unitsPerEm 

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Ondřej Sloup <osloup@redhat.com> - 1:4.8.7-70
- Rebuild for new PostgreSQL 15

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 25 2022 Jens Petersen <petersen@redhat.com> - 1:4.8.7-68
- Recommend ibus-qt when ibus is installed

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 19 2021 Than Ngo <than@redhat.com> - 1:4.8.7-66
- Fix FTBFS

* Tue Oct 12 2021 Than Ngo <than@redhat.com> - 1:4.8.7-65
- CVE-2020-24741, Do not attempt to load a library relative to $PWD

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1:4.8.7-64
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 29 2021 Than Ngo <than@redhat.com> - 4.8.7-63
- Fixed FTBFS against firebird-4.0.0

* Tue Jul 27 2021 Than Ngo <than@redhat.com> - 4.8.7-62
- Fixed FTBFS 

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 09 2021 Than Ngo <than@redhat.com> - 4.8.7-60
- Resolves: #1931444, Clamp parsed doubles to float representable values 

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 1:4.8.7-59
- rebuild for libpq ABI fix rhbz#1908268

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.8.7-57
- Hardcode the compiler version in the build key once and for all

* Wed Aug 19 2020 Jeff Law <law@redhat.com> - 4.8.7-56
- Add support for gcc-11
- Fix ordered pointer comparison against zero problems

* Thu Aug 13 2020 Than Ngo <than@redhat.com> - 4.8.7-55
- fixed #1868534 - CVE-2020-17507

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 4.8.7-53
- Disable LTO

* Fri Jan 31 2020 Than Ngo <than@redhat.com> - 4.8.7-52
- fixed FTBFS against gcc10

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Apr 20 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.8.7-49
- re-enable javascript-jit

* Tue Apr 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.8.7-48
- rebuild

* Fri Mar 22 2019 Than Ngo <than@redhat.com> - 4.8.7-47
- fixed #1691638 - CVE-2018-19872 qt: malformed PPM image causing division by zero and crash in qppmhandler.cpp

* Thu Feb 28 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-46
- backport qforeach.patch from qt5
- -no-javascript-jit on f30 to workaround gcc9 FTBFS for now

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 19 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:4.8.7-44
- fix QAudio hardcoding hw:0,0 on ALSA1.1 (patch by Jaroslav Škarvada, #1641151)
- disable OpenSSL 1.1 patch for F27, keep building against compat-openssl10
  (It really does not make sense to switch over the F27 package at this point.)

* Fri Sep 21 2018 Owen Taylor <otaylor@redhat.com> - 1:4.8.7-43
- Disable qtchooser for Flatpak builds

* Sat Jul 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-42
- drop BR: pkgconfig(NetworkManager) (#1606047)
- use %%make_build %%ldconfig

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat May 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-40
- build only qtscript using -O1 (#1580047)

* Sat May 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-39
- workaround qtscript/gcc8 bug (#1580047)

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-38
- -devel: Requires: gcc-c++

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-37
- BR: gcc-c++, use %%license, .spec cosmetics

* Thu Feb 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-36
- qt: Fedora build flags only partially applied (#1543887)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:4.8.7-35
- Escape macros in %%changelog

* Fri Jan 05 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:4.8.7-34
- build with OpenSSL 1.1.x, from Debian (Gert Wollny, Dmitry Eremin-Solenikov)
- fix build with ICU >= 59, from OpenSUSE (Fabian Vogt)
- update URL to use HTTPS

* Wed Oct 25 2017 Troy Dawson <tdawson@redhat.com> - 1:4.8.7-33
- Cleanup spec file conditionals

* Mon Oct 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-32
- BR: mariadb-connector-c-devel (f28+, #1494085)
- backport mysql driver mariadb fix (QTBUG-63108)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Than Ngo <than@redhat.com> - 1:4.8.7-29
- fixed bz#1409600, stack overflow in QXmlSimpleReader, CVE-2016-1004

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.8.7-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue Mar 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-27
- drop system_clucene on f26+ (clucene09 is FTBFS, #1424046)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.7-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-25
- update QTBUG-22829.patch to use _SYS_SYSMACROS_H_OUTER instead (#1396755)

* Thu Dec 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-24
- namespace QT_VERSION_CHECK to workaround major/minor being pre-defined (#1396755)
- update QTBUG-22829.patch to define _SYS_SYSMACROS_H (#1396755)

* Wed Dec 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-23
- (re)enable mysql support (#1400233)

* Thu Dec 1 2016 Orion Poplawski <orion@cora.nwra.com> - 1:4.8.7-22
- Add additional workarounds for boost/glib parsing (#1396755)

* Wed Nov 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-21
- BR: compat-openssl10-devel, restore -openssl-linked (#1328659)
- -no-sql-mysql (#1400233)

* Wed Nov 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-20
- FTBFS firebird
- FTBFS openssl-1.1, bootstrap using -no-openssl (#1400196)

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-19
- load openssl libs dynamically, f26+ (#1328659)

* Sun Jun 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-18
- qmake-qt4 adds '-std=gnu++98' flag to compiler flags (#1349951)

* Wed Apr 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-17
- %%build: drop --buildkey g++-4 (#1327360)
- %%build: add QT_BUILD_KEY verification (to avoid future regressions)

* Sun Apr 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-16
- use epoch in -static Provides
- -devel-private: Provides: qt(4)-private-devel

* Fri Apr 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-15
- %%build: -buildkey g++-4 (#1327360)

* Sun Apr 03 2016 Michal Toman <mtoman@fedoraproject.org> - 1:4.8.7-14
- Fix build on MIPS (#1322524)

* Wed Mar 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-13
- respin boost/moc patch for boost-1.60 (BOOST_TYPE_TRAITS_HPP)

* Mon Mar 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-12
- -x11: back to Recommends: sni-qt (#1317481)

* Sat Mar 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-11
- -x11: Requires: sni-qt if plasma-workspace, f23+

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-10
- -x11: Recommends: sni-qt, f24+

* Tue Mar 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.7-9
- rebuild (openssl)

* Wed Feb 10 2016 Than Ngo <than@redhat.com> - 1:4.8.7-8
- fix build issue with gcc6
- fix alsa version check for version >= 1.1.x

* Tue Feb 02 2016 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.7-7
- macros.qt4 : cleanup, introduce %%_qt4_optflags, %%_qt4_ldflags, %%_qt4_qmake_flags

* Thu Nov 26 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.7-6
- don't inject $RPM_OPT_FLAGS/$RPM_LD_FLAGS into qmake defaults (#1279265)

* Wed Nov 25 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.7-5
- -devel: Requires: redhat-rpm-config (#1279265)

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 1:4.8.7-4
- Remove no longer required AppData file

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.7-3
- macros.qt4: fix qmake_qt4 so "FOO=BAR %%qmake_qt4" works as expected

* Tue Jun 09 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.7-2
- drop -reduce-relocations (f22+)

* Tue May 26 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.7-1
- qt-4.8.7 (final)

* Fri May 08 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.7-0.1.rc2
- qt-4.8.7-rc2

* Tue May 05 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-30
- backport: data corruption in QNetworkAccessManager

* Thu Apr 30 2015 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.6-29
- introduce -common noarch subpkg, should help multilib issues
- -doc: fix %%description (doesn't include assistant)

* Mon Apr 13 2015 Than Ngo <than@redhat.com> - 1:4.8.6-28
- bz#1210677, CVE-2015-1860 CVE-2015-1859 CVE-2015-1858

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1:4.8.6-27
- Add an AppData file for the software center

* Fri Mar 20 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-26
- macros.qt4: fix _qt4_evr macro (missing : after epoch)

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-25
- DoS vulnerability in the BMP image handler (CVE-2015-0295)

* Mon Feb 16 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-24
- more gcc5 detection fixes, in particular, ensure same QT_BUILD_KEY as gcc4 for now

* Fri Feb 13 2015 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.6-23
- Qt: FTBFS with gcc5 (#1192464)
- Make Adwaita the default theme for applications running in the GNOME DE (#1192453)

* Wed Feb 11 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-22
- rebuild (gcc5)

* Thu Jan 29 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-21
- refresh boost/moc patch (QTBUG-22829)

* Sun Jan 18 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-20
- fix %%pre scriptlet (#1183299)

* Sat Jan 17 2015 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-19
- ship /etc/xdg/qtchooser/4.conf alternative instead (of qt4.conf)

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-18
- omit previously-overlooked webkit bits (#1168259)

* Sun Nov 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-17
- Broken qmake_qt4 in /usr/lib/rpm/macros.d/macros.qt4 (#1161927)

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.6-16
- macros.qt4: standalone, improved %%qmake_qt4 macro (sync'd with qt5 version)

* Sat Nov 01 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:4.8.6-15
- sync system-clucene patch from qt5-qttools (some QDir::mkpath in QtCLucene)

* Sun Oct 26 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:4.8.6-14
- build against the system clucene09-core (same patch as for qt5-qttools)

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.6-13
- qmlviewer: -qt4 wrapper, move to -devel
- pull in some upstream fixes

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.8.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.8.6-11
- drop Phonon-GStreamer0.10 support from qtconfig-qt4 on F21+ (#1123112)

* Wed Jul 23 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.8.6-10
- use alternatives to fix qtchooser conf's in non-basearch multilib case (#1122316)

* Thu Jul 17 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-9.1
- rebuild (for pulseaudio, bug #1117683)

* Sat Jun 07 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.6-9
- apply proposed fixes for QTBUG-34614,37380,38585 for LibreOffice (#1105422)

* Tue Jun 03 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-8
- backport selected upstream commits...
- Fix visual index lookup (QTBUG-37813)
- RGB30 fix (QTBUG-25998,#1018566)
- QDBus comparison

* Wed May 07 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-7
- gcc should be fixed, drop workaround (#1091482)

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-6
- try -fno-devirtualize workaround fc21+ (#1091482, gcc #60965)

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.8.6-5
- drop f21 gcc-4.9 workarounds (they didn't work)
- omit qt-cupsEnumDests.patch, again, pending more testing (#980952)

* Fri Apr 25 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-4
- -fno-tree-vrp (#1091482)

* Fri Apr 25 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-3
- try -fno-delete-null-pointer-checks to workaround bug #1091482

* Thu Apr 24 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-2
- DoS vulnerability in the GIF image handler (QTBUG-38367)

* Thu Apr 24 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-1
- 4.8.6 (final)

* Tue Apr 15 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.6-0.2.rc2
- 4.8.6-rc2

* Tue Apr 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.8.6-0.1.rc1
- 4.8.6-rc1

* Wed Mar 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-24
- support ppc64le arch (#1081216)

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.5-23
- fix QMAKE_STRIP handling (#1074041)

* Fri Mar 07 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-22
- respin mysql_config patch

* Fri Mar 07 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-21
- restore qt-cupsEnumDests.patch (#980952)

* Thu Mar 06 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-20
- systemtrayicon plugin support (from kubuntu)

* Tue Feb 18 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-19
- cleanup QMAKE_STRIP handling

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-18
- rebuild (libicu)

* Sat Feb 01 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-17
- better %%rpm_macros_dir handling

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-16
- macros.qt4: ++%%_qt4_examplesdir (keep %%_qt4_examples around for compatibility)

* Fri Jan 17 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.8.5-15
- drop "Discover printers shared by CUPS 1.6 (#980952)" (#1054312, #980952#c18)

* Mon Jan 13 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.8.5-14
- fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
- fix QTBUG-35460 (error message for CVE-2013-4549 is misspelled)

* Mon Dec 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 4.8.5-13
- Add support for aarch64 (#1046360) 

* Thu Dec 05 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-12
- XML Entity Expansion Denial of Service (CVE-2013-4549)

* Wed Oct 09 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-11
- Discover printers shared by CUPS 1.6 (#980952)

* Mon Oct 07 2013 Daniel Vrátil <dvratil@redhat.com> 4.8.5-10
- drop revert of the PostgreSQL driver patch (fixed in Akonadi 1.10.3)

* Thu Oct 03 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-9
- rework %%_bindir %%_qt4_bindir links to be more qtchooser friendly

* Thu Sep 12 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-8
- Keyboard shortcuts doesn't work for russian keyboard layout (#968367, QTBUG-32908)

* Mon Aug 26 2013 Jon Ciesla <limburgher@gmail.com> - 4.8.5-7
- libmng rebuild.

* Thu Aug 08 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-6.1
- qt4 rpm macros not found by rpm in F18 (#994739)

* Tue Jul 30 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-6
- enable qtchooser support

* Tue Jul 30 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-5
- revert upstream postgresql driver changes wrt escaping (QTBUG-30076)

* Thu Jul 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-4
- drop qtscript(javascriptcore) debuginfo patch, savings not significant

* Thu Jul 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-3
- reduce debuginfo in qtwebkit(webcore) and qtscript(javascriptcore)

* Tue Jul 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-2
- qdbusviewer subpkg (#968336)

* Tue Jul 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-1
- 4.8.5 (final)

* Wed Jun 26 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-0.6.rc2
- trim changelog
- cleaner rpm_macros_dir handling

* Fri Jun 21 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-0.5.rc2
- drop multilib portion from qt_plugin_path.patch

* Tue Jun 18 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-0.4.rc2
- (re)add kde4/multilib QT_PLUGIN_PATH

* Mon Jun 10 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-0.3.rc2
- 4.8.5-rc2

* Mon Jun 10 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-0.2.rc
- RFE: Add %%qmake_qt4 macro (#870199)

* Sun Jun 09 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.5-0.1.rc
- 4.8.5-RC

* Thu May 30 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-19
- drop QTBUG-27809 candidate fix, causes regressions (#968794)

* Tue May 28 2013 Than Ngo <than@redhat.com> - 4.8.4-18
- QTBUG-27809, fix multiple calls to QDBusPendingReply::waitForFinished on separate objects

* Thu Apr 25 2013 Than Ngo <than@redhat.com> - 4.8.4-17
- Desktop file sanity, drop key "Encoding", it's deprecated

* Fri Apr 19 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-16
- update URL (#859286)
- include qdbusviewer .desktop/icon
- .desktop files: +mime scriptlets, +GenericName keys

* Wed Mar 20 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-15
- pull in a few more upstream fixes

* Mon Feb 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-14
- SIGSEGV when called from QMetaObject::metaCall (QTBUG-29082, kde#311751)

* Mon Feb 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-13
- qmake: add support for pkgconfig Requires.private

* Mon Feb 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-12
- add more moc/boost workarounds, thanks boost-1.53 (QTBUG-22829)

* Mon Feb 04 2013 Than Ngo <than@redhat.com> - 4.8.4-11
- backport: fix security flaw was found in the way QSharedMemory class, CVE-2013-0254

* Sat Jan 26 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.4-10
- rebuild (icu)

* Thu Jan 24 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.4-9
- make qtchooser support non-conflicting

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1:4.8.4-8
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-7
- add qtchooser support (disabled by default)

* Mon Jan 07 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-6
- blacklist unauthorized SSL certificates by Türktrust

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.4-5
- QGtkStyle was unable to detect the current GTK+ theme (#702493, QTBUG-5545))

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.4-4
- QSslSocket may report incorrect errors when certificate verification fails

* Thu Jan 03 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.4-3
- -x11: %%exclude %%{_qt4_plugindir}/designer/libqwebview.so

* Sun Dec 16 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.4-2
- -designer-plugin-webkit subpkg (#887501)
- fix/prune/changelog

* Thu Nov 29 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.4-1
- 4.8.4

* Wed Oct 31 2012 Than Ngo <than@redhat.com> - 1:4.8.3-8
- add poll support to fix QAbstractSocket errors with more than
  1024 file descriptors, thanks Florian for the patch

* Wed Oct 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.3-7
- Crash in Qt script (QTBUG-27322)

* Tue Oct 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.3-6
- fix/respin qdevice_pri patch

* Mon Oct 22 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.3-5
- QDir::homePath() should account for an empty $HOME (QTBUG-4862, kde#249217, #694385)

* Sat Oct 20 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.3-4
- $RPM_LD_FLAGS should be propagated to qmake's defaults (#868554)

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.3-3
- find qdevice.pri even for installed qt builds

* Thu Sep 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.3-2
- upstream disable-SSL-compression patch

* Thu Sep 13 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.3-1
- qt-4.8.3 final
- revert QtScript-JIT commit

* Tue Sep 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.2-6
- revert "fix QtScript JIT crash" patch, causes frequent segmentation faults (#853587)

* Mon Aug 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.2-5
- fix QtScript JIT crash (QTBUG-23871, kde#297661) 

* Thu Jul 05 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.2-4
- text cursor blinks not in the current cell (kde#296490)

* Tue Jun 19 2012 Than Ngo <than@redhat.com> - 4.8.2-3
- fix bz#810500, fix crash in assistant

* Tue May 29 2012 Than Ngo <than@redhat.com> - 4.8.2-2
- fix bz#820767, lrelease-qt4 tries to run qmake not qmake-qt4

* Tue May 22 2012 Than Ngo <than@redhat.com> - 4.8.2-1
- 4.8.2

* Fri May 18 2012 Than Ngo <than@redhat.com> - 4.8.1-15
- add rhel/fedora condition

* Thu May 17 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-14
- Can't build 32bit Qt release application on 64bit (#822710)

* Wed May 16 2012 Than Ngo <than@redhat.com> - 4.8.1-13
- add upstream patch to fix crash on big endian machine

* Fri May 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-12
- enable debuginfo in libQt3Support

* Fri May 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-11
- lrelease-qt4 tries to run qmake not qmake-qt4 (#820767)

* Thu May 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-10
- Requires: qt-settings (f17+)

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-9
- rebuild (libtiff)

* Thu May 03 2012 Than Ngo <than@redhat.com> - 4.8.1-8
- add rhel/fedora condition

* Wed Apr 18 2012 Than Ngo <than@redhat.com> - 4.8.1-7
- add rhel condition

* Tue Apr 17 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-6
- omit qdbusconnection warnings in release/no-debug mode

* Tue Apr 03 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-5
- Fix a crash in cursorToX() when new block is added (QTBUG-24718)

* Fri Mar 30 2012 Than Ngo <than@redhat.com> - 4.8.1-4
- Fix QTgaHandler::canRead() not obeying image plugin specs

* Thu Mar 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-3
- Header file name mismatch in qt-devel i686 (#808087)

* Thu Mar 29 2012 Than Ngo <than@redhat.com> - 4.8.1-2
- add correct flags

* Wed Mar 28 2012 Than Ngo <than@redhat.com> - 4.8.1-1
- 4.8.1

* Wed Feb 22 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-10
- -demos: Requires: -doc (#795859)

* Mon Feb 20 2012 Than Ngo <than@redhat.com> - 4.8.0-9
- get rid of timestamp which causes multilib problem

* Tue Jan 24 2012 Than Ngo <than@redhat.com> - 4.8.0-8
- disable Using gold linker, g++ doesn't support flags gold linker
- fix gcc-4.7 issue

* Tue Jan 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-7
- improved filter_event patch (kde#275469)

* Mon Jan 09 2012 Than Ngo <than@redhat.com> - 4.8.0-6
- bz#772128, CVE-2011-3922, Stack-based buffer overflow in embedded harfbuzz code

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-5
- fix qvfb 

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-4
- filter event patch, avoid "ghost entries in kde taskbar" problem (kde#275469)

* Tue Dec 20 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-3
- don't spam if libicu is not present at runtime (#759923)

* Mon Dec 19 2011 Dan Horák <dan[at]dannu.cz> 4.8.0-2
- add missing method for QBasicAtomicPointer on s390(x)

* Thu Dec 15 2011 Jaroslav Reznik <jreznik@redhat.com> 4.8.0-1
- 4.8.0

* Mon Dec 12 2011 Jaroslav Reznik <jreznik@redhat.com> 4.8.0-0.29.rc1
- Fixes the position of misplaced mouse input (QTBUG-22420)

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.28.rc1
- Control whether icu support is built (#759923)

* Sat Dec 03 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.0-0.27.rc1
- work around a MOC issue with Boost 1.48 headers (#756395)

* Wed Nov 30 2011 Than Ngo <than@redhat.com> - 4.8.0-0.26.rc1
- workaround crash on ppc64

* Mon Nov 14 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.25.rc1
- BuildRequires: pkgconfig(libpng)
- -devel: drop Requires: libpng-devel libjpeg-devel 
- qt4.macros: +%%_qt4_epoch, %%_qt4_evr

* Thu Nov 03 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.24.rc1
- build tds sql driver with -fno-strict-aliasing 

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.23.rc1
- crash when using a visual with 24 bits per pixel (#749647,QTBUG-21754)

* Fri Oct 28 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.0-0.22.rc1
- fix FTBFS in QtWebKit's wtf library with GLib 2.31

* Thu Oct 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.0-0.21.rc1
- fix missing NULL check in the toLocalFile patch (fixes Digikam segfault)

* Thu Oct 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.20.rc1
- restore qt-4.7-compatible behavior to QUrl.toLocalFile (#749213)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.8.0-0.19.rc1
- Rebuilt for glibc bug#747377

* Mon Oct 24 2011 Than Ngo <than@redhat.com> 4.8.0-0.18.rc1
- bz#748297, update the URL of qt packages

* Tue Oct 18 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.17.rc1
- Buttons in Qt applications not clickable when run under gnome-shell (#742658, QTBUG-21900)

* Mon Oct 17 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.16.rc1
- Qt doesn't close orphaned file descriptors after printing (#746601, QTBUG-14724)

* Sat Oct 15 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.15.rc1
- revert qlist.h commit that seems to induce crashes in qDeleteAll<QList... (QTBUG-22037)

* Sat Oct 15 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.14.rc1
- pkgconfig-style deps

* Thu Oct 13 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.13.rc1
- 4.8.0-rc1

* Mon Oct 03 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.12.20111002
- 20111002 4.8 branch snapshot

* Sat Sep 17 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.11.beta1
- ./configure -webkit

* Wed Sep 14 2011 Lukas Tinkl <ltinkl@redhat.com> 1:4.8.0-0.10.beta1
- fix missing CSS styles and JS functions in the generated HTML
  documentation, omitted from the upstream tarball

* Wed Aug 17 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.9.beta1
- -graphicssystem raster (#712617)
- drop sqlite_pkg option

* Sun Jul 31 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.8.beta1
- macros.qt4: s|_qt47|_qt48|

* Thu Jul 28 2011 Dan Horák <dan[at]danny.cz> 1:4.8.0-0.7.beta1
- fix the outdated standalone copy of JavaScriptCore (s390)

* Sat Jul 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.6.beta1
- fix QMAKE_LIBDIR_QT, for missing QT_SHARED define (#725183)

* Wed Jul 20 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.5.beta1
- 4.8.0-beta1
- drop webkit_packaged conditional
- drop old patches
- drop qvfb (for now, ftbfs)

* Wed Jul 13 2011 Than Ngo <than@redhat.com> - 1:4.8.0-0.4.tp
- move macros.* to -devel

* Tue Jul 05 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.3.tp
- Adding qt-sql-ibase driver for qt (#719002) 
- qvfb subpackage (#718416)

* Tue Jun 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.2.tp
- fontconfig patch (#705348, QTBUG-19947)

* Wed May 25 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.8.0-0.1.tp
- 4.8.0-tp
- drop phonon_internal, phonon_backend_packaged build options

* Thu May 19 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.3-3
- omit %%{_qt4_plugindir}/designer/libqwebview.so too

* Thu May 19 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.3-2
- omit bundled webkit on f16+ (in favor of separately packaged qtwebkit)

* Thu May 05 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.3-1
- 4.7.3

* Thu Apr 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-9
- -webkit-devel: move qt_webkit_version.pri here

* Fri Apr 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-8
- -devel-private: qt-creator/QmlDesigner requires qt private headers (#657498)

* Fri Mar 25 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-7
- followup patch for QTBUG-18338, blacklist fraudulent SSL certifcates

* Fri Mar 25 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-6
- drop qt-designer-plugin-phonon

* Fri Mar 25 2011 Than Ngo <than@redhat.com> - 1:4.7.2-5
- apply patch to fix QTBUG-18338, blacklist fraudulent SSL certifcates

* Tue Mar 22 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.2-4
- rebuild (mysql)

* Fri Mar 11 2011 Dan Horák <dan[at]danny.cz> 1:4.7.2-3
- workaround memory exhaustion during linking of libQtWebKit on s390

* Mon Mar 07 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.2-2
- Fix QNetworkConfigurationManager crash due to null private pointer (#682656)

* Tue Mar 01 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.2-1
- 4.7.2

* Wed Feb 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-18
- libQtWebKit.so has no debug info (#667175)

* Wed Feb 16 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-17
- Obsoletes: qt-sqlite < 1:4.7.1-16

* Tue Feb 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-16
- drop -sqlite subpkg, move into main (#677418) 

* Wed Feb 09 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-15
- -assistant subpkg (#660287)
- -config drop Obsoletes: qt-x11 (avoid/workaround #674326)
- -config unconditionally drop NoDisplay (since we're dropping the Obsoletes too)
- -designer-plugin-phonon subpkg (#672088)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.7.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-13
- -config: fix Obsoletes for real this time

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-12
- fix qt-config related Obsoletes/Provides

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-11
- upstream fix for QTextCursor regression (QTBUG-15857, kde#249373)

* Tue Jan 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-10
- -config subpkg
- qt-x11 pulls in phonon (#672088)
- qtconfig.desktop: drop NoDisplay (f15+ only, for now)

* Thu Jan 20 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-9.1
- apply the Assistant QtWebKit dependency removal (#660287) everywhere

* Thu Jan 06 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-9
- qsortfilterproxymodel fix (merge_request/934)

* Tue Jan 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-8
- only do Requires: phonon-backend if using qt's phonon

* Fri Dec 24 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.1-7
- fix QTreeView crash triggered by KPackageKit (patch by David Faure)

* Fri Dec 24 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-6
- rebuild (mysql)

* Wed Dec 08 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.1-5
- make the Assistant QtWebKit dependency removal (#660287) F15+ only for now
- fix QTextCursor crash in Lokalize and Psi (QTBUG-15857, kde#249373, #660028)
- add some more NULL checks to the glib_eventloop_nullcheck patch (#622164)

* Mon Dec 06 2010 Than Ngo <than@redhat.com> 4.7.1-4
- bz#660287, using QTextBrowser in assistant to drop qtwebkit dependency

* Tue Nov 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.1-3
- Fails to create debug build of Qt projects on mingw (#653674, QTBUG-14467)

* Mon Nov 22 2010 Than Ngo <than@redhat.com> - 4.7.1-2
- bz#528303, Reordering of Malayalam Rakar not working properly

* Thu Nov 11 2010 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Mon Oct 25 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.7.0-8
- QtWebKit, CVE-2010-1822: crash by processing certain SVG images (#640290)

* Mon Oct 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-7
- qt-devel contains residues from patch run (#639463)

* Fri Oct 15 2010 Than Ngo <than@redhat.com> - 4.7.0-6
- apply patch to fix the color issue in 24bit mode (cirrus driver)

* Thu Sep 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-5
- Wrong Cursor when widget become native on X11 (QTBUG-6185)

* Mon Sep 27 2010 Than Ngo <than@redhat.com> - 4.7.0-4
- apply upstream patch to fix QTreeView-regression (QTBUG-13567)

* Thu Sep 23 2010 Than Ngo <than@redhat.com> - 4.7.0-3
- fix typo in license

* Thu Sep 23 2010 Than Ngo <than@redhat.com> - 4.7.0-2
- fix bz#562049, bn-IN Incorrect rendering
- fix bz#562058, bn_IN init feature is not applied properly
- fix bz#631732, indic invalid syllable's are not recognized properly
- fix bz#636399, oriya script open type features are not applied properly

* Tue Sep 21 2010 Than Ngo <than@redhat.com> - 4.7.0-1
- 4.7.0

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.31.rc1
- -webkit-devel: add missing %%defattr
- -webkit: move qml/webkit bits here

* Wed Sep 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.30.rc1
- Crash in drawPixmap in Qt 4.7rc1 (#631845, QTBUG-12826)

* Mon Aug 30 2010 Than Ngo <than@redhat.com> - 4.7.0-0.29.rc1
- drop the patch, it's already fixed in upstream

* Thu Aug 26 2010 Than Ngo <than@redhat.com> - 4.7.0-0.28.rc1
- 4.7.0 rc1

* Thu Jul 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.26.beta2
- rebase patches, avoiding use of patch fuzz
- omit old qt-copy/kde-qt patches, pending review
- omit kde4_plugin patch
- ftbfs:s/qml/qmlviewer, libQtMediaServices no longer included

* Thu Jul 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.25.beta2
- 4.7.0-beta2

* Thu Jul 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.24.beta1
- X11Embed broken (rh#609757, QTBUG-10809)

* Thu Jul 01 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.7.0-0.23.beta1
- use find_lang to package the qm files (#609749)
- put the qm files into the correct subpackages
- remove qvfb translations, we don't ship qvfb

* Tue Jun 29 2010 Rex Dieter <rdieter@fedoraproject.org. 4.7.0-0.22.beta1
- workaround glib_eventloop crasher induced by gdal/grass (bug #498111)

* Sun Jun 20 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-0.20.beta1
- avoid timestamps in uic-generated files to be multilib-friendly

* Fri Jun 18 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-0.19.beta1
- revert -no-javascript-jit change, false-alarm (#604003)
- QtWebKit does not search correct plugin path(s) (#568860)
- QtWebKit browsers crash with flash-plugin (rh#605677,webkit#40567)
- drop qt-x11-opensource-src-4.5.0-gcc_hack.patch

* Wed Jun 16 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-0.18.beta1
- -no-javascript-jit on i686 (#604003)

* Wed Jun 16 2010 Karsten Hopp <karsten@redhat.com> 4.7.0-0.17.beta1 
- add s390 and s390x to 3rdparty/webkit/JavaScriptCore/wtf/Platform.h and
  3rdparty/javascriptcore/JavaScriptCore/wtf/Platform.h

* Fri Jun 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.16.beta1
- scrub -lpulse-mainloop-glib from .prl files (#599844)
- scrub references to %%buildroot in .pc, .prl files

* Thu May 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.15.beta1
- Unsafe use of rand() in X11 (QTBUG-9793)

* Fri May 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.14.beta1
- drop -no-javascript-jit (webkit#35154)

* Mon May 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.13.beta1
- QT_GRAPHICSSYSTEM env support

* Sun May 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.12.beta1
- -webkit-devel: move Qt/qweb*.h here (#592680)

* Fri May 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.11.beta1
- -webkit-devel: Obsoletes: qt-devel ... (upgrade path)

* Thu May 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.10.beta1
- -webkit-devel: Provides: qt4-webkit-devel , Requires: %%name-devel

* Thu May 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.9.beta1
- 4.7.0-beta1
- -webkit-devel : it lives! brainz!

* Fri Apr 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.8.tp
- prepping for separate QtWebKit(-2.0)
- -webkit subpkg,  Provides: QtWebKit ...
- -devel: Provides: QtWebKit-devel ...
- TODO: -webkit-devel (and see what breaks)

* Wed Apr 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.7.tp
- own %%{_qt4_plugindir}/crypto

* Sat Apr 03 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.7.0-0.6.tp
- backport fix for QTBUG-9354 which breaks kdeutils build

* Fri Apr 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.5.tp
- Associate text/vnd.trolltech.linguist with linguist (#579082)

* Tue Mar 23 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.7.0-0.4.tp
- fix type cast issue on sparc64

* Sun Mar 21 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.7.0-0.3.tp
- also strip -lpulse from .prl files (fixes PyQt4 QtMultimedia binding build)

* Tue Mar 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.2.tp
- qt-4.7.0-tp
- macros.qt4 : +%%_qt4_importdir
- don't strip libs from pkgconfig files, Libs.private is now used properly
- add -lphonon to stripped libs instead of brutally hacking out
  QMAKE_PRL_LIBS altogether (#520323)
- qt-assistant-adp packaged separately now, not included here

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-7
- BR alsa-lib-devel (for QtMultimedia)

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-6
- Provides: qt-assistant-adp(-devel)

* Fri Mar 05 2010 Than Ngo <than@redhat.com> - 4.6.2-5
- Make tablet detection work with new wacom drivers (#569132)

* Mon Mar 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-4
- fix 64bit platform logic, use linux-g++-64 everywhere except x86_64 (#569542)

* Sun Feb 28 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-3
- fix CUPS patch not to crash if currentPPD is NULL (#566304)

* Tue Feb 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-2
- macros.qt4: s/qt45/qt46/

* Mon Feb 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-1
- 4.6.2

* Fri Feb 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-3
- improve cups support (#523846, kde#180051#c22)

* Tue Jan 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-2
- drop bitmap_font_speed patch, rejected upstream

* Tue Jan 19 2010 Than Ngo <than@redhat.com> - 4.6.1-1
- 4.6.1

* Mon Jan 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-5
- bitmap_font_speed patch (QTBUG-7255)

* Sat Jan 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-4
- Fix crash when QGraphicsItem destructor deletes other QGraphicsItem (kde-qt cec34b01)
- Fix a crash in KDE/Plasma with QGraphicsView. TopLevel list of items (kde-qt 63839f0c)

* Wed Dec 23 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.0-3
- disable QtWebKit JavaScript JIT again, incompatible with SELinux (#549994)

* Sat Dec 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.0-2
- own %%{_qt4_plugindir}/gui_platform

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.6.0-1
- 4.6.0

* Tue Nov 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.6.rc1
- qt-4.6.0-rc1

* Sat Nov 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.5.beta1 
- -tds: Add package with TDS sqldriver (#537586)
- add arch'd provides for sql drivers

* Sun Nov 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.4.beta1
- -x11: Requires: %%{name}-sqlite%%{?_isa}

* Mon Oct 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.3.beta1
- kde-qt patches (as of 20091026)

* Fri Oct 16 2009 Than Ngo <than@redhat.com> - 4.6.0-0.2.beta1 
- subpackage sqlite plugin, add Require on qt-sqlite in qt-x11
  for assistant
- build/install qdoc3 again

* Wed Oct 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.1.beta1
- qt-4.6.0-beta1
- no kde-qt patches (yet)

* Sat Oct 10 2009 Than Ngo <than@redhat.com> - 4.5.3-4
- fix translation build issue
- rhel cleanup

* Tue Oct 06 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.5.3-3
- disable JavaScriptCore JIT, SE Linux crashes (#527079)

* Fri Oct 02 2009 Than Ngo <than@redhat.com> - 4.5.3-2
- cleanup patches
- if ! phonon_internal, exclude more/all phonon headers
- qt-devel must Requires: phonon-devel (#520323)

* Thu Oct 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.3-1
- qt-4.5.3

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-21
- switch to external/kde phonon

* Mon Sep 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-20
- use internal Qt Assistant/Designer icons
- -devel: move designer.qch,linguist.qch here
- move ownership of %%_qt4_docdir, %%_qt4_docdir/qch to main pkg

* Sun Sep 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-19
- Missing Qt Designer icon (#476605)

* Fri Sep 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-18
- drop gcc -fno-var-tracking-assignments hack (#522576)

* Fri Sep 11 2009 Than Ngo <than@redhat.com> - 4.5.2-17
- drop useless check for ossl patch, the patch works fine with old ossl

* Wed Sep 09 2009 Than Ngo <than@redhat.com> - 4.5.2-16
- add a correct system_ca_certificates patch

* Tue Sep 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-15
- use system ca-certificates (#521911)

* Tue Sep 01 2009 Than Ngo <than@redhat.com> - 4.5.2-14
- drop fedora < 9 support
- only apply ossl patch for fedora > 11

* Mon Aug 31 2009 Than Ngo <than@redhat.com> - 4.5.2-13
- fix for CVE-2009-2700

* Thu Aug 27 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-12
- use platform linux-g++ everywhere (ie, drop linux-g++-64 on 64 bit),
  avoids plugin/linker weirdness (bug #478481)

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1:4.5.2-11
- rebuilt with new openssl

* Thu Aug 20 2009 Than Ngo <than@redhat.com> - 4.5.2-10
- switch to kde-qt branch

* Tue Aug 18 2009 Than Ngo <than@redhat.com> - 4.5.2-9
- security fix for CVE-2009-1725 (bz#513813)

* Sun Aug 16 2009 Than Ngo <than@redhat.com> - 4.5.2-8
- fix phonon-backend-gstreamer for using pulsaudio (#513421)

* Fri Aug 14 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-7
- kde-qt: 287-qmenu-respect-minwidth
- kde-qt: 0288-more-x-keycodes (#475247)

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-6
- use linker scripts for _debug targets (#510246)
- tighten deps using %%{?_isa}
- -x11: Requires(post,postun): /sbin/ldconfig

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.5.2-5
- apply upstream patch to fix issue in Copy and paste

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Than Ngo <than@redhat.com> - 4.5.2-3
- pregenerate PNG, drop BR on GraphicsMagick (bz#509244)

* Fri Jun 26 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.2-2
- take current qt-copy-patches snapshot (20090626)
- disable patches which are already in 4.5.2
- fix the qt-copy patch 0274-shm-native-image-fix.diff to apply against 4.5.2

* Thu Jun 25 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.5.2-1
- Qt 4.5.2

* Sun Jun 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-18
- phonon-backend-gstreamer pkg, with icons
- optimize (icon-mostly) scriptlets

* Sun Jun 07 2009 Than Ngo <than@redhat.com> - 4.5.1-17
- drop the hack, apply patch to install Global header, gstreamer.desktop
  and dbus services file

* Sat Jun 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-16
- install awol Phonon/Global header

* Fri Jun 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.1-15
- apply Phonon PulseAudio patch (needed for the xine-lib backend)

* Fri Jun 05 2009 Than Ngo <than@redhat.com> - 4.5.1-14
- enable phonon and gstreamer-backend

* Sat May 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-13
- -doc: Obsoletes: qt-doc < 1:4.5.1-4 (workaround bug #502401)

* Sat May 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-12
- +phonon_internal macro to toggle packaging of qt's phonon (default off)

* Fri May 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-11
- qt-copy-patches-20090522

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10.2
- full (non-bootstrap) build

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10.1
- allow for minimal bootstrap build (*cough* arm *cough*)

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10
- improved kde4_plugins patch, skip expensive/unneeded canonicalPath

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-9
- include kde4 plugin path by default (#498809)

* Mon May 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-8
- fix invalid assumptions about mysql_config --libs (bug #440673)
- fix %%files breakage from 4.5.1-5

* Wed Apr 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-7
- -devel: Provides: qt4-devel%%{?_isa} ...

* Mon Apr 27 2009 Than Ngo <than@redhat.com> - 4.5.1-6
- drop useless hunk of qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch

* Mon Apr 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-5
- -devel: Provides: *-static for libQtUiTools.a

* Fri Apr 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-4
- qt-doc noarch
- qt-demos, qt-examples (split from -doc)
- (cosmetic) re-order subpkgs in alphabetical order
- drop unused profile.d bits

* Fri Apr 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-3
- enable FT_LCD_FILTER (uses freetype subpixel filters if available at runtime)

* Fri Apr 24 2009 Than Ngo <than@redhat.com> - 4.5.1-2
- apply upstream patch to fix the svg rendering regression

* Thu Apr 23 2009 Than Ngo <than@redhat.com> - 4.5.1-1
- 4.5.1

* Tue Apr 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-14
- fix vrgb/vgbr corruption, disable QT_USE_FREETYPE_LCDFILTER (#490377)

* Fri Apr 10 2009 Than Ngo <than@redhat.com> - 4.5.0-13
- unneeded executable permissions for profile.d scripts

* Wed Apr 01 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.0-12
- fix inline asm in qatomic (de)ref (i386/x86_64), should fix Kolourpaint crash

* Mon Mar 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-11
- qt fails to build on ia64 (#492174)

* Wed Mar 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-10
- qt-copy-patches-20090325

* Tue Mar 24 2009 Than Ngo <than@redhat.com> - 4.5.0-9
- lrelease only shows warning when duplicate messages found in *.ts( #491514)

* Fri Mar 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-8
- qt-copy-patches-20090319

* Thu Mar 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-7
- include more phonon bits, attempt to fix/provide phonon bindings
  for qtscriptgenerator, PyQt, ...

* Tue Mar 17 2009 Than Ngo <than@redhat.com> - 4.5.0-6
- fix lupdate segfault (#486866)

* Sat Mar 14 2009 Dennis Gilmore <dennis@ausil.us> - 4.5.0-5
- add patch for sparc64. 
- _Atomic_word is not always an int

* Tue Mar 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-4
- macros.qt4: %%_qt45
- cleanup more phonon-related left-overs 

* Wed Mar 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-3
- -no-phonon-backend
- include qdoc3
- move designer plugins to runtime (#487622)

* Tue Mar 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-2
- License: LGPLv2 with exceptions or GPLv3 with exceptions
- BR: gstreamer-devel
- drop qgtkstyle patch (no longer needed)
- -x11: move libQtScriptTools here (linked with libQtGui)

* Tue Mar 03 2009 Than Ngo <than@redhat.com> - 4.5.0-1
- 4.5.0

* Fri Feb 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 1:4.5.0-0.8.20090224
- 20090224 snapshot
- adjust pkgconfig hackery

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.0-0.7.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.5.rc1
- revert license, change won't land until official 4.5.0 release
- workaround broken qhostaddress.h (#485677)
- Provides: qgtkstyle = 0.1

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.4.rc1
- saner versioned Obsoletes
- -gtkstyle, Obsoletes: qgtkstyle < 0.1
- enable phonon support and associated hackery

* Mon Feb 16 2009 Than Ngo <than@redhat.com> 4.5.0-0.3.rc1
- fix callgrindChildExitCode is uninitialzed

* Sun Feb 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-0.2.rc1
- qt-copy-patches-20090215
- License: +LGPLv2

* Wed Feb 11 2009 Than Ngo <than@redhat.com> - 4.5.0-0.rc1.0
- 4.5.0 rc1

* Thu Feb 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-16
- track branches/qt-copy/4.4, and backout previous trunk(qt45) ones

* Mon Feb 02 2009 Than Ngo <than@redhat.com> 4.4.3-15
- disable 0269,0270,0271 patches, it causes issue in systray

* Thu Jan 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-14
- qt-copy-patches-20090129

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-13
- Provides: qt4%%{?_isa} = %%version-%%release
- add %%_qt4 to macros.qt4

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-12 
- respin (mysql)

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.4.3-11
- rebuild for new OpenSSL

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-10
- drop qt-x11-opensource-src-4.3.4-no-hardcoded-font-aliases.patch (#447298),
  in favor of qt-copy's 0263-fix-fontconfig-handling.diff

* Mon Jan 12 2009 Than Ngo <than@redhat.com> - 4.4.3-9
- qt-copy-patches-20090112

* Tue Dec 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-8
- qt-copy-patches-20081225

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-7
- rebuild for pkgconfig deps

* Wed Nov 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-6
- qt-copy-patches-20081112

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 4.4.3-5
- drop 0256-fix-recursive-backingstore-sync-crash.diff, it's
  included in qt-copy-pathes-20081110

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-4
- qt-copy-patches-20081110

* Mon Nov 10 2008 Than Ngo <than@redhat.com> 4.4.3-3
- apply 0256-fix-recursive-backingstore-sync-crash.diff

* Thu Nov 06 2008 Than Ngo <than@redhat.com> 4.4.3-2
- bz#468814, immodule selection behavior is unpredictable without QT_IM_MODULE,
  patch from Peng Wu
- backport fix from 4.5

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-1
- 4.4.3

* Wed Sep 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.2-2
- omit systray patch (for now)

* Sat Sep 20 2008 Than Ngo <than@redhat.com> 4.4.2-1
- 4.4.2

* Mon Sep 08 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-3
- apply QMAKEPATH portion of multilib patch only if needed
- qt-copy-patches-20080908

* Wed Aug 06 2008 Than Ngo <than@redhat.com> -  4.4.1-2
- fix license tag
- fix Obsoletes: qt-sqlite (missing epoch)

* Tue Aug 05 2008 Than Ngo <than@redhat.com> -  4.4.1-1
- 4.4.1

* Tue Aug 05 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-17
- fold -sqlite subpkg into main (#454930)

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-16
- qt-copy-patches-20080723 (kde#162793)
- omit deprecated phonon bits

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-15
- fix/workaround spec syntax 

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-14
- macros.qt4: fix %%_qt4_datadir, %%_qt4_translationdir

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-13
- (re)fix qconfig-multilib.h for sparc64

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-12
- qt-copy-patches-20080711

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-11
- fix dbus conditional (#452487)

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-10
- strip -lsqlite3 from .pc files (#451490)

* Sat Jun 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-9
- restore -qt4 suffixes

* Fri Jun 13 2008 Than Ngo <than@redhat.com> 4.4.0-8
- drop qt wrapper, make symlinks to /usr/bin

* Tue Jun 10 2008 Than Ngo <than@redhat.com> 4.4.0-7
- fix #450310, multilib issue 

* Fri Jun 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-6
- qt-copy-patches-20080606
- drop BR: libungif-devel (not used)
- move libQtXmlPatters, -x11 -> main
- move qdbuscpp2xml, qdbusxml2cpp, xmlpatters, -x11 -> -devel

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-5
- under GNOME, default to QGtkStyle if available

* Mon May 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-4
- don't hardcode incorrect font substitutions (#447298)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-3
- qt-copy-patches-20080516

* Tue May 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-2
- revert _qt4_bindir change for now, needs more work (#446167)

* Tue May 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-1
- qt-4.4.0
