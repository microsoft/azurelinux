# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define _default_patch_fuzz 2

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Name: qt3
Summary: The shared library for the Qt 3 GUI toolkit
Version: 3.3.8b
Release: 102%{?dist}
# Automatically converted from old format: QPL or GPLv2 or GPLv3 - review is highly recommended.
License: QPL-1.0 OR GPL-2.0-only OR GPL-3.0-only
Url: http://www.troll.no
Source0: ftp://ftp.trolltech.com/qt/source/qt-x11-free-%{version}.tar.gz
Source2: qt.sh
Source3: qt.csh
Source4: designer3.desktop
Source5: assistant3.desktop
Source6: linguist3.desktop
Source7: qtconfig3.desktop

Patch1: qt-3.3.4-print-CJK.patch
Patch2: qt-3.0.5-nodebug.patch
Patch3: qt-3.1.0-makefile.patch
Patch4: qt-x11-free-3.3.7-umask.patch
Patch5: qt-x11-free-3.3.6-strip.patch
Patch7: qt-x11-free-3.3.2-quiet.patch
Patch8: qt-x11-free-3.3.3-qembed.patch
Patch12: qt-uic-nostdlib.patch
Patch13: qt-x11-free-3.3.6-qfontdatabase_x11.patch
Patch14: qt-x11-free-3.3.3-gl.patch
Patch19: qt-3.3.3-gtkstyle.patch
# hardcode the compiler version in the build key once and for all
Patch20: qt-x11-free-3.3.8b-hardcode-buildkey.patch
Patch24: qt-x11-free-3.3.5-uic.patch
Patch25: qt-x11-free-3.3.8b-uic-multilib.patch
Patch27: qt-3.3.6-fontrendering-ml_IN-209097.patch
Patch29: qt-3.3.8-fontrendering-as_IN-209972.patch
Patch31: qt-3.3.6-fontrendering-te_IN-211259.patch
Patch32: qt-3.3.6-fontrendering-214371.patch
Patch33: qt-3.3.8-fontrendering-#214570.patch
Patch34: qt-3.3.6-fontrendering-ml_IN-209974.patch
Patch35: qt-3.3.6-fontrendering-ml_IN-217657.patch
Patch37: qt-3.3.6-fontrendering-gu-228452.patch
Patch38: qt-x11-free-3.3.8-odbc.patch
Patch39: qt-x11-free-3.3.7-arm.patch
# See http://bugzilla.redhat.com/549820
# Try to set some sane defaults, for style, fonts, plugin path
# FIXME: style doesn't work.  use kde3 plastik, if available
Patch40: qt-x11-free-3.3.8b-sane_defaults.patch
# and/or just use qtrc to do the same thing
Source10: qtrc
# add missing #include <cstdef> to make gcc-4.6 happier
Patch41: qt-x11-free-3.3.8b-cstddef.patch
# fix aliasing issue in qlocale.cpp
Patch42: qt-x11-free-3.3.8b-qlocale-aliasing.patch
# use the system SQLite 2 (Debian's 91_system_sqlite.diff)
Patch43: qt-x11-free-3.3.8b-system-sqlite2.patch
# silence compiler warning in qimage.h by adding parentheses
Patch44: qt-x11-free-3.3.8b-qimage-parentheses.patch
# fix the include path for zlib.h in qcstring.cpp to pick up the system version
Patch45: qt-x11-free-3.3.8b-system-zlib-header.patch
# fix FTBFS with libpng 1.5 (patch from NetBSD)
Patch46: qt-3.3.8-libpng15.patch
# work around -Werror=format-security false positives (#1037297)
Patch47: qt-x11-free-3.3.8b-#1037297.patch
# search for FreeType using pkg-config, fixes FTBFS with freetype >= 2.5.1
Patch48: qt-x11-free-3.3.8b-freetype251.patch
# rename the struct Param in qsqlextension_p.h that conflicts with PostgreSQL 11
Patch49: qt-x11-free-3.3.8b-postgresql11.patch

# immodule patches
Patch50: qt-x11-immodule-unified-qt3.3.8-20071116.diff.bz2
Patch51: qt-x11-immodule-unified-qt3.3.5-20051012-quiet.patch
Patch52: qt-x11-free-3.3.8b-fix-key-release-event-with-imm.diff
Patch53: qt-x11-free-3.3.6-qt-x11-immodule-unified-qt3.3.5-20060318-resetinputcontext.patch

# mariadb support
Patch60: qt-x11-free-3.3.8b-mariadb.patch

# compile with PostgreSQL 12
Patch70: qt-x11-free-3.3.8b-PostgreSQL12.patch

# qt-copy patches
Patch100: 0038-dragobject-dont-prefer-unknown.patch
Patch101: 0047-fix-kmenu-width.diff
Patch102: 0048-qclipboard_hack_80072.patch
Patch103: 0056-khotkeys_input_84434.patch
Patch105: 0073-xinerama-aware-qpopup.patch
Patch107: 0079-compositing-types.patch
Patch108: 0080-net-wm-sync-request-2.patch
Patch110: 0084-compositing-properties.patch

# upstream patches
Patch200: qt-x11-free-3.3.4-fullscreen.patch
Patch201: qt-x11-free-3.3.8b-gcc43.patch

# security patches
# fix for CVE-2013-4549 backported from Qt 4
Patch300: qt-x11-free-3.3.8b-CVE-2013-4549.patch
# fix for CVE-2014-0190 (QTBUG-38367) backported from Qt 4
Patch301: qt-x11-free-3.3.8b-CVE-2014-0190.patch
# fix for CVE-2015-0295 backported from Qt 4
Patch302: qt-x11-free-3.3.8b-CVE-2015-0295.patch
# fix for CVE-2015-1860 backported from Qt 4
Patch303: qt-x11-free-3.3.8b-CVE-2015-1860.patch

%define qt_dirname qt-3.3
%define qtdir %{_libdir}/%{qt_dirname}
%define qt_docdir %{_docdir}/qt-devel-%{version}

%define smp 1
%define immodule 1
%define debug 0

# MySQL plugins
%define plugin_mysql -plugin-sql-mysql
%define mysql_include_dir %{_includedir}/mysql
%define mysql_lib_dir %{_libdir}/mysql

# Postgres plugins
%define plugin_psql -plugin-sql-psql

# ODBC plugins
%define plugin_odbc -plugin-sql-odbc

# sqlite plugins
%if 0%{?rhel} && 0%{?rhel} < 7
%define plugin_sqlite -plugin-sql-sqlite
%else
%define plugin_sqlite %{nil}
%endif

%define plugins_style -qt-style-cde -qt-style-motifplus -qt-style-platinum -qt-style-sgi -qt-style-windows -qt-style-compact -qt-imgfmt-png -qt-imgfmt-jpeg -qt-imgfmt-mng
%define plugins %{plugin_mysql} %{plugin_psql} %{plugin_odbc} %{plugin_sqlite} %{plugins_style}

# not sure what this is for anymore? -- rex
Requires: coreutils

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: desktop-file-utils
BuildRequires: libmng-devel
BuildRequires: glibc-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: giflib-devel
BuildRequires: perl-interpreter
BuildRequires: sed
BuildRequires: findutils
BuildRequires: cups-devel
BuildRequires: tar
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: libXrender-devel
BuildRequires: libXrandr-devel
BuildRequires: libXcursor-devel
BuildRequires: libXinerama-devel
BuildRequires: libXft-devel
BuildRequires: libXext-devel
BuildRequires: libX11-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXt-devel
BuildRequires: libXmu-devel
BuildRequires: libXi-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: desktop-file-utils
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
BuildRequires: mariadb-connector-c-devel
%else
BuildRequires: mysql-devel
%endif
BuildRequires: postgresql-server-devel
BuildRequires: unixODBC-devel
%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires: sqlite2-devel
%endif

%package config
Summary: Graphical configuration tool for programs using Qt 3
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}


%package devel
Summary: Development files for the Qt 3 GUI toolkit
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: libXrender-devel
Requires: libXrandr-devel
Requires: libXcursor-devel
Requires: libXinerama-devel
Requires: libXft-devel
Requires: libXext-devel
Requires: libX11-devel
Requires: libSM-devel
Requires: libICE-devel
Requires: libXt-devel
Requires: xorg-x11-proto-devel
Requires: mesa-libGL-devel
Requires: mesa-libGLU-devel

%package devel-docs
Summary: Documentation for the Qt 3 GUI toolkit
Requires: %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%package ODBC
Summary: ODBC drivers for Qt 3's SQL classes
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%package MySQL
Summary: MySQL drivers for Qt 3's SQL classes
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%package PostgreSQL
Summary: PostgreSQL drivers for Qt 3's SQL classes
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%package sqlite
Summary: sqlite drivers for Qt 3's SQL classes
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%package designer
Summary: Interface designer (IDE) for the Qt 3 toolkit
Requires: %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains the shared library needed to run Qt 3
applications, as well as the README files for Qt 3.


%description config
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains a graphical configuration tool for programs using Qt 3.


%description devel
The %{name}-devel package contains the files necessary to develop
applications using the Qt GUI toolkit: the header files, the Qt meta
object compiler.

Install %{name}-devel if you want to develop GUI applications using the Qt 3
toolkit.


%description devel-docs
The %{name}-devel-docs package contains the man pages, the HTML documentation and
example programs for Qt 3.


%description ODBC
ODBC driver for Qt 3's SQL classes (QSQL)


%description MySQL
MySQL driver for Qt 3's SQL classes (QSQL)


%description PostgreSQL
PostgreSQL driver for Qt 3's SQL classes (QSQL)


%description sqlite
sqlite driver for Qt 3's SQL classes (QSQL)


%description designer
The %{name}-designer package contains an User Interface designer tool
for the Qt 3 toolkit.


%prep
%setup -q -n qt-x11-free-%{version}
%patch -P1 -p1 -b .cjk
%patch -P2 -p1 -b .ndebug
%patch -P3 -p1 -b .makefile
%patch -P4 -p1 -b .umask
%patch -P5 -p1 -b .strip
# drop backup file(s), else they get installed too, http://bugzilla.redhat.com/639459
rm -fv mkspecs/linux-g++*/qmake.conf.strip
%patch -P7 -p1 -b .quiet
%patch -P8 -p1 -b .qembed
%patch -P12 -p1 -b .nostdlib
%patch -P13 -p1 -b .fonts
%patch -P14 -p1 -b .gl
%patch -P19 -p1 -b .gtk
gcc -dumpversion ||:
%patch -P20 -p1 -b .hardcode-buildkey
%patch -P24 -p1 -b .uic
%patch -P25 -p1 -b .uic-multilib
%patch -P27 -p1 -b .fontrendering-ml_IN-bz#209097
%patch -P29 -p1 -b .fontrendering-as_IN-bz#209972
%patch -P31 -p1 -b .fontrendering-te_IN-bz#211259
%patch -P32 -p1 -b .fontrendering-bz#214371
%patch -P33 -p1 -b .fontrendering-#214570
%patch -P34 -p1 -b .fontrendering-#209974
%patch -P35 -p1 -b .fontrendering-ml_IN-217657
%patch -P37 -p1 -b .fontrendering-gu-228452
%patch -P38 -p1 -b .odbc
# it's not 100% clear to me if this is safe for all archs -- Rex
%ifarch %{arm} 
%patch -P39 -p1 -b .arm
%endif
%patch -P40 -p1 -b .sane_defaults
sed -i.KDE3_PLUGIN_PATH \
  -e "s|@@KDE3_PLUGIN_PATH@@|%{_libdir}/kde3/plugins|" \
  src/kernel/qapplication.cpp
%patch -P41 -p1 -b .cstddef
%patch -P42 -p1 -b .qlocale-aliasing
%patch -P43 -p1 -b .system-sqlite2
%patch -P44 -p1 -b .qimage-parentheses
%patch -P45 -p1 -b .system-zlib-header
%if 0%{?fedora} > 16 || 0%{?rhel} > 6
# This patch works ONLY with libpng >= 1.5.
%patch -P46 -p0 -b .libpng15
%endif
%patch -P47 -p1 -b .#1037297
%patch -P48 -p1 -b .freetype251
%patch -P49 -p1 -b .postgresql11

# immodule patches
%if %{immodule}
%patch -P50 -p1
%patch -P51 -p1 -b .quiet
%patch -P52 -p1 -b .fix-key-release-event-with-imm
%patch -P53 -p1 -b .resetinputcontext
%endif

# mariadb
%patch -P60 -p1 -b .mariadb

# PostgreSQL 12
%patch -P70 -p1 -b .PostgreSQL12

# qt-copy patches
%patch -P100 -p0 -b .0038-dragobject-dont-prefer-unknown
%patch -P101 -p0 -b .0047-fix-kmenu-width
%patch -P102 -p0 -b .0048-qclipboard_hack_80072
%patch -P103 -p0 -b .0056-khotkeys_input_84434
%patch -P105 -p0 -b .0073-xinerama-aware-qpopup
%patch -P107 -p0 -b .0079-compositing-types
%patch -P108 -p0 -b .0080-net-wm-sync-request
%patch -P110 -p0 -b .0084-compositing-properties

# upstream patches
%patch -P200 -p1 -b .fullscreen
%patch -P201 -p1 -b .gcc34

# security patches
%patch -P300 -p1 -b .CVE-2013-4549
%patch -P301 -p1 -b .CVE-2014-0190
%patch -P302 -p1 -b .CVE-2015-0295
%patch -P303 -p1 -b .CVE-2015-1860

# convert to UTF-8
iconv -f iso-8859-1 -t utf-8 < doc/man/man3/qdial.3qt > doc/man/man3/qdial.3qt_
mv doc/man/man3/qdial.3qt_ doc/man/man3/qdial.3qt

# get rid of bundled libraries to ensure they won't be used
rm -rf src/3rdparty/{lib*,sqlite,zlib}

%build
export QTDIR=`/bin/pwd`
export LD_LIBRARY_PATH="$QTDIR/lib:$LD_LIBRARY_PATH"
export PATH="$QTDIR/bin:$PATH"
export QTDEST=%{qtdir}

%if %{smp}
   export SMP_MFLAGS="%{?_smp_mflags}"
%endif

%if %{immodule}
   sh ./make-symlinks.sh
%endif

# set correct X11 prefix
perl -pi -e "s,QMAKE_LIBDIR_X11.*,QMAKE_LIBDIR_X11\t=," mkspecs/*/qmake.conf
perl -pi -e "s,QMAKE_INCDIR_X11.*,QMAKE_INCDIR_X11\t=," mkspecs/*/qmake.conf
perl -pi -e "s,QMAKE_INCDIR_OPENGL.*,QMAKE_INCDIR_OPENGL\t=," mkspecs/*/qmake.conf
perl -pi -e "s,QMAKE_LIBDIR_OPENGL.*,QMAKE_LIBDIR_OPENGL\t=," mkspecs/*/qmake.conf

# don't use rpath
perl -pi -e "s|-Wl,-rpath,| |" mkspecs/*/qmake.conf

perl -pi -e "s|-O2|$INCLUDES %{optflags} -fno-strict-aliasing|g" mkspecs/*/qmake.conf

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  perl -pi -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  perl -pi -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi

# build shared, threaded (default) libraries
echo yes | ./configure \
  -prefix $QTDEST \
  -docdir %{qt_docdir} \
%if "%{_lib}" == "lib64"
  -platform linux-g++-64 \
%else
  -platform linux-g++ \
%endif
%if %{debug}
  -debug \
%else
  -release \
%endif
  -shared \
  -largefile \
  -qt-gif \
  -system-zlib \
  -system-libpng \
  -system-libmng \
  -system-libjpeg \
  -no-exceptions \
  -enable-styles \
  -enable-tools \
  -enable-kernel \
  -enable-widgets \
  -enable-dialogs \
  -enable-iconview \
  -enable-workspace \
  -enable-network \
  -enable-canvas \
  -enable-table \
  -enable-xml \
  -enable-opengl \
  -enable-sql \
  -qt-style-motif \
  %{plugins} \
  -stl \
  -thread \
  -cups \
  -sm \
  -xinerama \
  -xrender \
  -xkb \
  -ipv6 \
  -dlopen-opengl \
  -xft \
  -tablet

%make_build src-qmake

%if 0%{?rhel} && 0%{?rhel} < 7
# build sqlite plugin
pushd plugins/src/sqldrivers/sqlite
qmake -o Makefile sqlite.pro
popd
%endif

# build psql plugin
pushd plugins/src/sqldrivers/psql
qmake -o Makefile "INCLUDEPATH+=%{_includedir}/pgsql %{_includedir}/pgsql/server %{_includedir}/pgsql/internal" "LIBS+=-lpq" psql.pro
popd

# build mysql plugin
pushd plugins/src/sqldrivers/mysql
qmake -o Makefile "INCLUDEPATH+=%{mysql_include_dir}" "LIBS+=-L%{mysql_lib_dir} -lmysqlclient" mysql.pro
popd

# build odbc plugin
pushd plugins/src/sqldrivers/odbc
qmake -o Makefile "LIBS+=-lodbc" odbc.pro
popd

%make_build src-moc
%make_build sub-src
%make_build sub-tools UIC="$QTDIR/bin/uic -nostdlib -L $QTDIR/plugins"

%install
rm -rf %{buildroot}

export QTDIR=`/bin/pwd`
export LD_LIBRARY_PATH="$QTDIR/lib:$LD_LIBRARY_PATH"
export PATH="$QTDIR/bin:$PATH"
export QTDEST=%{qtdir}

make install INSTALL_ROOT=%{buildroot}

install -m644 -D %{SOURCE10} %{buildroot}%{qtdir}/etc/settings/qtrc
sed -i \
  -e "s|@@QTDIR@@|%{qtdir}|" \
  -e "s|@@KDE3_PLUGIN_PATH@@|%{_libdir}/kde3/plugins|" \
   %{buildroot}%{qtdir}/etc/settings/qtrc

for i in findtr qt20fix qtrename140 lrelease lupdate ; do
   install bin/$i %{buildroot}%{qtdir}/bin/
done

# strip extraneous dirs/libraries, stop overlinking
sed -i -e 's|^Libs: -L${libdir} -lqt-mt.*|Libs: -L${libdir} -lqt-mt|g' %{buildroot}%{qtdir}/lib/pkgconfig/*.pc
sed -i -e "s|^QMAKE_PRL_LIBS =.*|QMAKE_PRL_LIBS = -L%{qtdir}/lib -lqt-mt|g" %{buildroot}%{qtdir}/lib/*.prl

# pkgconfig love
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}%{qtdir}/lib/pkgconfig/*.pc %{buildroot}%{_libdir}/pkgconfig/

# install man pages
mkdir -p %{buildroot}%{_mandir}
cp -fR doc/man/* %{buildroot}%{_mandir}/

# clean up
make -C tutorial clean
make -C examples clean

# Make sure the examples can be built outside the source tree.
# Our binaries fulfill all requirements, so...
perl -pi -e "s,^DEPENDPATH.*,,g;s,^REQUIRES.*,,g" `find examples -name "*.pro"`

# don't include Makefiles of qt examples/tutorials
find examples -name "Makefile" | xargs rm -f
find examples -name "*.obj" | xargs rm -rf
find examples -name "*.moc" | xargs rm -rf
find tutorial -name "Makefile" | xargs rm -f

for a in */*/Makefile ; do
  sed 's|^SYSCONF_MOC.*|SYSCONF_MOC		= %{qtdir}/bin/moc|' < $a > ${a}.2
  mv -v ${a}.2 $a
done

mkdir -p %{buildroot}/etc/profile.d
install -m 644 %{SOURCE2} %{SOURCE3} %{buildroot}/etc/profile.d/

# Add desktop files
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --vendor="qt" \
  %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7}

# Patch qmake to use qt-mt unconditionally
perl -pi -e "s,-lqt ,-lqt-mt ,g;s,-lqt$,-lqt-mt,g" %{buildroot}%{qtdir}/mkspecs/*/qmake.conf

# remove broken links
rm -f %{buildroot}%{qtdir}/mkspecs/default/linux-g++*
rm -f %{buildroot}%{qtdir}/lib/*.la

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{qtdir}/lib" > %{buildroot}/etc/ld.so.conf.d/qt-%{_arch}.conf

# install icons
mkdir %{buildroot}%{_datadir}/pixmaps
install -m 644 tools/assistant/images/qt.png %{buildroot}%{_datadir}/pixmaps/qtconfig3.png
install -m 644 tools/assistant/images/designer.png %{buildroot}%{_datadir}/pixmaps/designer3.png
install -m 644 tools/assistant/images/assistant.png %{buildroot}%{_datadir}/pixmaps/assistant3.png
install -m 644 tools/assistant/images/linguist.png %{buildroot}%{_datadir}/pixmaps/linguist3.png

# own style directory
mkdir -p %{buildroot}%{qtdir}/plugins/styles


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc FAQ LICENSE* README* changes*
%dir %{qtdir}
%dir %{qtdir}/bin
%dir %{qtdir}/etc/
%dir %{qtdir}/etc/settings/
%dir %{qtdir}/lib
%dir %{qtdir}/plugins
%dir %{qtdir}/plugins/sqldrivers
%dir %{qtdir}/plugins/styles
%config %{qtdir}/etc/settings/qtrc
%{qtdir}/translations/
%{qtdir}/plugins/designer/
%if %{immodule}
%{qtdir}/plugins/inputmethods
%endif
%config /etc/profile.d/*
/etc/ld.so.conf.d/*
%{qtdir}/lib/libqui.so.*
%{qtdir}/lib/libqt*.so.*

%files config
%{qtdir}/bin/qtconfig
%{_datadir}/applications/*qtconfig*.desktop
%{_datadir}/pixmaps/qtconfig3.png

%files devel
%{qt_docdir}/
%{qtdir}/bin/moc
%{qtdir}/bin/uic
%{qtdir}/bin/findtr
%{qtdir}/bin/qt20fix
%{qtdir}/bin/qtrename140
%{qtdir}/bin/assistant
%{qtdir}/bin/qm2ts
%{qtdir}/bin/qmake
%{qtdir}/bin/qembed
%{qtdir}/bin/linguist
%{qtdir}/bin/lupdate
%{qtdir}/bin/lrelease
%{qtdir}/include
%{qtdir}/mkspecs
%{qtdir}/lib/libqt*.so
%{qtdir}/lib/libqui.so
%{qtdir}/lib/libeditor.a
%{qtdir}/lib/libdesigner*.a
%{qtdir}/lib/libqassistantclient.a
%{qtdir}/lib/*.prl
%{qtdir}/phrasebooks
%{_libdir}/pkgconfig/*
%{_datadir}/applications/*linguist*.desktop
%{_datadir}/applications/*assistant*.desktop
%{_datadir}/pixmaps/linguist3.png
%{_datadir}/pixmaps/assistant3.png

%files devel-docs
%doc examples
%doc tutorial
%{_mandir}/*/*

%if 0%{?rhel} && 0%{?rhel} < 7
%files sqlite
%{qtdir}/plugins/sqldrivers/libqsqlite.so
%endif

%files ODBC
%{qtdir}/plugins/sqldrivers/libqsqlodbc.so

%files PostgreSQL
%{qtdir}/plugins/sqldrivers/libqsqlpsql.so

%files MySQL
%{qtdir}/plugins/sqldrivers/libqsqlmysql.so

%files designer
%{qtdir}/templates
%{qtdir}/bin/designer
%{_datadir}/applications/*designer*.desktop
%{_datadir}/pixmaps/designer3.png


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 3.3.8b-100
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-99
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-98
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-97
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 30 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.3.8b-96
- Rebuilt for PostgreSQL 16 (BZ#2251109)
- For more info see the Fedora Change: https://fedoraproject.org/wiki/Changes/PostgreSQL_16

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-95
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-94
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Ondřej Sloup <osloup@redhat.com> - 3.3.8b-93
- Rebuild for new PostgreSQL 15

* Fri Sep 09 2022 Than Ngo <than@redhat.com> - 3.3.8b-92
- fixed bz#2120316 - qt3 shouldn't require postgresql-private-devel

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-91
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-90
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Than Ngo <than@redhat.com> - 3.3.8b-89
- Rebuild for Postgresql 14

* Thu Sep 16 2021 Than Ngo <than@redhat.com> - 3.3.8b-88
- Fix FTBFS

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-87
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 3.3.8b-86
- rebuild for libpq ABI fix rhbz#1908268

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-85
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-84
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Than Ngo <than@redhat.com> - 3.3.8b-83
- Use make macros, https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Jul 16 2020 Than Ngo <than@redhat.com> - 3.3.8b-82
- fixed 1839125 - compile with PostgreSQL 12, FTBFS

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 3.3.8b-81
- Fix string quoting for rpm >= 4.16

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-79
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-78
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-77
- Hardcode the compiler version in the build key once and for all
- Rename the struct Param in qsqlextension_p.h that conflicts with PostgreSQL 11

* Fri Jul 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-76
- BR: gcc-c++

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-74
- Fix CVE-2016-10040 (stack overflow in QXmlSimpleReader due to a too high
  entityCharacterLimit in the CVE-2013-4549 patch) (#1409603)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.3.8b-73
- Escape macros in %%changelog

* Mon Nov 13 2017 Than Ngo <than@redhat.com> - 3.3.8b-72
- backport mysql driver mariadb fix
- BR: mariadb-connector-c-devel (f28+, #1494085)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-70
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Mar 28 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.3.8b-68
- qt.sh: Avoid unnecessary command invocations

* Wed Feb 10 2016 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-67
- update gccX-buildkey.patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8b-66
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-64
- updated gcc5-buildkey patch for GCC 5 (supersedes gcc4-buildkey) (#1218091)

* Tue Apr 21 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-63
- backport CVE-2015-1860 (GIF handler buffer overflow, #1210675) fix from Qt 4

* Sat Feb 28 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-62
- backport CVE-2015-0295 (BMP image handler DoS, #1197275) fix from Qt 4

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-61
- rebuild (gcc5)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-58
- backport CVE-2014-0190 (GIF image handler DoS, QTBUG-38367) fix from Qt 4

* Sun Feb 23 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-57
- add ppc64le support to qt.sh and qt.csh (#1068898)
- fix ppc64 support in qt.csh
- search for FreeType using pkg-config, fixes FTBFS with freetype >= 2.5.1

* Tue Jan 14 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-56
- work around -Werror=format-security false positives (#1037297)

* Mon Jan 13 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-55
- fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
- fix QTBUG-35460 (error message for CVE-2013-4549 is misspelled)

* Thu Dec 05 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-54
- backport CVE-2013-4549 fix from Qt 4

* Tue Aug 27 2013 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-53
- trim changelog

* Tue Aug 27 2013 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-52
- strip extraneous libs from .pc/.prl files
- -devel: due to ^^, drop non-X11-related deps too

* Mon Aug 26 2013 Jon Ciesla <limburgher@gmail.com> - 3.3.8b-51
- libmng rebuild.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.3.8b-49
- Perl 5.18 rebuild

* Thu Apr 25 2013 Than Ngo <than@redhat.com> - 3.3.8b-48
- build with -fno-strict-aliasing
- drop deprecated Encoding

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 3.3.8b-46
- rebuild due to "jpeg8-ABI" feature drop

* Wed Oct 24 2012 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-45
- rebuild (libjpeg-turbo v8)

* Tue Oct 09 2012 Than Ngo <than@redhat.com> - 3.3.8b-44
- fix url

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Than Ngo <than@redhat.com> - 3.3.8b-42
- add rhel condition

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 10 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-40
- fix FTBFS with F17's libpng 1.5 (patch from NetBSD)

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.3.8b-39
- Rebuild for new libpng

* Thu Dec 01 2011 Than Ngo <than@redhat.com> - 3.3.8b-38
- add rhel7 condition

* Fri Nov 04 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-37
- fix aliasing issue in qlocale.cpp
- build against the system sqlite2-devel (patch from Debian)
- BuildRequires: sqlite2-devel instead of unused sqlite-devel (SQLite 3)
- silence compiler warning in qimage.h by adding parentheses
- fix the include path for zlib.h in qcstring.cpp to pick up the system version

* Sun Aug 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-36.1
- Rebuilt for rpm (#728707)

* Thu Jul 21 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-36
- drop extraneous Requires:

* Wed Mar 23 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-35
- rebuild (mysql)

* Thu Mar 10 2011 Than Ngo <than@redhat.com> - 3.3.8b-34
- fix multilib issue on ppc64

* Sun Jan 30 2011 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-33
- cstddef patch (for gcc-4.6)

* Mon Oct 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-32
- better fix for omitting patched qmake.conf files (#639459)

* Mon Oct 04 2010 Than Ngo <than@redhat.com> - 3.3.8b-31
- fix bz#639459, don't include *.orig files

* Wed Aug 11 2010 Than Ngo <than@redhat.com> - 3.3.8b-30
- drop not useful provides/obsoletes, bz#623106

* Tue Dec 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-29
- sane defaults (#549820)

* Thu Sep 10 2009 Than Ngo <than@redhat.com> - 3.3.8b-28
- drop support fedora < 10

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-26
- arm patch

* Thu Apr 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-25
- move designer plugins to runtime (#487622)

* Fri Apr 10 2009 Than Ngo <than@redhat.com> - 3.3.8b-24
- unneeded executable permissions for profile.d scripts 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8b-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 24 2009 Than Ngo <than@redhat.com> - 3.3.8b-22
- fix build problem against new unixODBC

* Wed Feb 04 2009 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-21
- unowned %%qt_docdir (#483441)

* Mon Feb 02 2009 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-20
- unowned dirs (#483441)

* Sat Jan 31 2009 Karsten Hopp <karsten@redhat.com> 3.3.8b-19
- s390x is 64bit, s390 is 32bit. Fixed in /etc/profile.d/qt.*

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> 3.3.8b-18
- respin (mysql)

* Wed Oct 08 2008 Than Ngo <than@redhat.com> 3.3.8b-17
- update qt-x11-immodule-unified-qt3 patch

* Tue Sep 30 2008 Than Ngo <than@redhat.com> 3.3.8b-16
- mv translations in main package (bz#448761)

* Sat Sep 20 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.3.8b-15
- set _default_patch_fuzz (fixes FTBFS)

* Mon Jul 07 2008 Rex Dieter <rdieter@fedoraproject.org> - 3.3.8b-14
- QTDIR isn't set in ppc64 buildroot (#454313)
- /etc/profile.d/qt.sh leaks variable ARCH (#454260)

* Fri May 23 2008 Than Ngo <than@redhat.com> -  3.3.8b-13
- fix rh#448027, qt3's PATH not set properly unless qt3-devel is installed

* Wed Apr 02 2008 Than Ngo <than@redhat.com> -  3.3.8b-12
- get rid of 0088-fix-xinput-clash.diff, it's fixed in
  new xorg-x11-proto-7.3-11

* Mon Mar 17 2008 Than Ngo <than@redhat.com> 3.3.8b-11
- fix obsolete/provides of version/release

* Thu Mar 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.3.8b-10
- fix %%{?epoch:%%{epoch}:} idiom not to add a ':' after it

* Wed Mar 12 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.3.8b-9
- rename to qt3 on Fedora >= 9

* Tue Mar 11 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.3.8b-8
- prepare for rename to qt3 on Fedora >= 9 (not enabled yet)
- add Provides and Obsoletes everywhere
- update summaries and descriptions
- remove dots at end of Summary tags
- fix non-UTF-8 characters

* Tue Mar 11 2008 Than Ngo <than@redhat.com> 3.3.8b-7
- 0088-fix-xinput-clash.diff, fix compile errors with Xmd.h

* Fri Mar 07 2008 Than Ngo <than@redhat.com> 3.3.8b-6
- move qt.[c]sh in main package (#221000)

* Mon Feb 18 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.3.8b-5
- fix buildkey for GCC 4.3 (#433235)

* Mon Feb 11 2008 Than Ngo <than@redhat.com> 3.3.8b-4
- rebuild for GCC 4.3

* Thu Jan 24 2008 Than Ngo <than@redhat.com> 3.3.8b-3
- add LICENSE.GPL2/GPL3

* Thu Jan 24 2008 Than Ngo <than@redhat.com> 3.3.8b-2
- License: GPLv2 or GPLv3
- merged in 3.3.8b -> drop following patches:
    * qt-3.3.6-fontrendering-punjabi-209970.patch
    * qt-3.3.6-fontrendering-or_IN-209098.patch
    * qt-3.3.6-fontrendering-gu-228451.patch
    * qt-font-default-subst.diff
    * 0076-fix-qprocess.diff
    * 0082-fix-qdatetime-fromstring.diff
    * qt-x11-free-3.3.8-bz#243722-mysql.patch
    * qt3-CVE-2007-3388.patch
    * utf8-bug-qt3-CVE-2007-0242.diff
    * qt-3.3.6-bz#292941-CVE-2007-4137.patch

* Wed Jan 23 2008 Than Ngo <than@redhat.com> 3.3.8b-1
- update to 3.3.8b, fix License

* Mon Nov 26 2007 Than Ngo <than@redhat.com> 3.3.8-11
- add Provides: qt3 = %%version-%%release

* Wed Nov  7 2007 Stepan Kasal <skasal@redhat.com> - 3.3.8-10
- rh#239216, fix a typo in qt-config description

* Thu Oct 04 2007 Than Ngo <than@redhat.com> - 3.3.8-9
- rh#309091, qt should provide %%{qtdir}/plugins/styles
- rh#276521, qt-copy patches 0079, 0080, 0082 and 0084

* Mon Sep 17 2007 Than Ngo <than@redhat.com> - 3.3.8-8
- CVE-2007-4137

* Wed Aug 29 2007 Than Ngo <than@redhat.com> - 1:3.3.8-7.fc7.1
- CVE-2007-0242

* Tue Aug 28 2007 Than Ngo <than@redhat.com> - 1:3.3.8-7
- CVE-2007-3388 qt3 format string flaw
- backport to fix #bz243722, bz#244148, Applications using qt-mysql crash if database is
  removed before QApplication is destroyed
- cleanup desktop files

* Mon Apr 23 2007 Than Ngo <than@redhat.com> - 1:3.3.8-5.fc7
- apply patch to fix fontrendering problem in gu_IN #228451,#228452

* Wed Apr 11 2007 Than Ngo <than@redhat.com> - 1:3.3.8-4.fc7
- adjust qt-3.3.8-fontrendering-as_IN-209972.patch and
  qt-3.3.8-fontrendering-#214570.patch for qt-3.3.8

* Mon Apr 02 2007 Than Ngo <than@redhat.com> - 1:3.3.8-3.fc7
- apply patches to fix
   Qt UTF-8 overlong sequence decoding vulnerability
   QPopupMenu aware of Xinerama
   a regression in QProgress::writeToStdin()

* Tue Mar 27 2007 Than Ngo <than@redhat.com> 1:3.3.8-2.fc7
- enable tablet support

* Mon Mar 19 2007 Than Ngo <than@redhat.com> 1:3.3.8-1.fc7
- update to 3.3.8

* Wed Dec 06 2006 Than Ngo <than@redhat.com> - 1:3.3.7-2.fc7
- Resolves: bz#214371, bn_IN font rendering
- Resolves: bz#217657, ml_IN issue with cursor position
- Resolves: bz#217638, regression bug in qt
- Resolves: bz#209974, Vowel position set properly
- Resolves: bz#214570, Rendering is not fine for 'RA' 09B0

* Thu Nov 09 2006 Than Ngo <than@redhat.com> 1:3.3.7-1.fc6
- update to 3.3.7
- fix #209097, ml_IN font rendering
- fix #209970, pa font rendering
- fix #209098, or_IN font rendering
- fix #209972, as_IN font rendering
- fix #209975, bn_IN font rendering
- fix #211259, te_IN font rendering
- fix #211436, as_IN font rendering
  thanks Sachin Tawniya, LingNing Zhang for the fixes
- move html files to devel
- add sqlite plugin
- fix #189012, qt settings should be readable for other

* Thu Aug 31 2006 Than Ngo <than@redhat.com> 1:3.3.6-13
- add missing desktop files

* Mon Jul 17 2006 Than Ngo <than@redhat.com> 1:3.3.6-12
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.3.6-11.1
- rebuild

* Mon Jul 10 2006 Than Ngo <than@redhat.com> 1:3.3.6-11
- apply upstream patches, fix arabic fonts issue, and
  problems with missing minimum size when richtext
  labels are used

* Thu Jun 29 2006 Than Ngo <than@redhat.com> 1:3.3.6-10
- apply patch from Lars, fixes Qt 3.3.6 for Arabic fonts

* Wed Jun 28 2006 Than Ngo <than@redhat.com> 1:3.3.6-9
- fix #183302, IM preedit issue in kbabel

* Mon Jun 26 2006 Than Ngo <than@redhat.com> 1:3.3.6-8
- rebuilt

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 1:3.3.6-7
- fix utf8 issue in changelog
- fix #195410, don't strip binaries/libraries
- fix #156572, keyReleaseEvent issue

* Mon Jun 05 2006 Than Ngo <than@redhat.com> 1:3.3.6-6
- qt-devel requires on mesa-libGLU-devel mesa-libGU-devel

* Tue May 16 2006 Than Ngo <than@redhat.com> 1:3.3.6-5 
- fix #191895, BR libXmu-devel
- disable warnings if debug is off

* Mon May 15 2006 Than Ngo <than@redhat.com> 1:3.3.6-4
- fix multilib issue 

* Tue May 09 2006 Than Ngo <than@redhat.com> 1:3.3.6-3 
- add subpackage qt-devel-docs #191099

* Thu Apr 13 2006 Than Ngo <than@redhat.com> 1:3.3.6-2
- fix xorg prefix #188510

* Mon Mar 20 2006 Than Ngo <than@redhat.com> 1:3.3.6-1
- update to 3.3.6
- adapt qt-x11-immodule-unified-qt3.3.5-20060318 to qt-3.3.6
- remove set of fixes for the immodule patch, included in qt-x11-immodule-unified-qt3.3.5-20060318
- remove 0051-qtoolbar_77047.patch, qt-x11-free-3.3.4-assistant_de.patch,
  qt-x11-free-3.3.5-warning.patch, included in new upstream


* Mon Feb 27 2006 Than Ngo <than@redhat.com> 1:3.3.5-13
- add set of fixes for the immodule patch, thanks to Dirk Müller

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.3.5-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.3.5-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Than Ngo <than@redhat.com> 1:3.3.5-12
- add BuildRequires on mesa-libGL-devel

* Wed Dec 21 2005 Than Ngo <than@redhat.com> 1:3.3.5-11 
- BuildRequires on libXt-devel/xorg-x11-proto-devel
 
* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt
 
* Sun Nov 13 2005 Than Ngo <than@redhat.com> 1:3.3.5-10
- workaround for keyboard input action in KHotKeys

* Tue Nov 08 2005 Than Ngo <than@redhat.com> 1:3.3.5-9 
- fix for modular X

* Tue Nov 08 2005 Than Ngo <than@redhat.com> 1:3.3.5-8
- get rid of xorg-x11-devel, fix for modular X

* Tue Oct 25 2005 Than Ngo <than@redhat.com> 1:3.3.5-7
- update qt-x11-immodule-unified-qt3.3.5-20051012-quiet.patch

* Mon Oct 24 2005 Than Ngo <than@redhat.com> 1:3.3.5-6
- update qt-x11-immodule-unified-qt3.3.5-20051018.diff
- remove unneeded qt-x11-immodule-unified-qt3.3.5-20051012-build.patch

* Thu Oct 13 2005 Than Ngo <than@redhat.com> 1:3.3.5-5
- update qt-x11-immodule-unified-qt3.3.5-20051012
- disable some debug messages
- apply patch to fix build problem with the new immodule patch

* Tue Sep 27 2005 Than Ngo <than@redhat.com> 1:3.3.5-4
- apply patch to fix gcc warnings

* Mon Sep 26 2005 Than Ngo <than@redhat.com> 1:3.3.5-3 
- export QTINC/QTLIB, thanks to Rex Dieter (#169132)

* Tue Sep 20 2005 Than Ngo <than@redhat.com> 1:3.3.5-2
- German translation of the Qt Assistent #161558
- add uic workaround

* Sun Sep 11 2005 Than Ngo <than@redhat.com> 1:3.3.5-1
- update to 3.3.5

* Mon Aug 22 2005 Than Ngo <than@redhat.com> 1:3.3.4-22
- apply upstream patch to fix kmail folder selector #166430

* Mon Aug 15 2005 Than Ngo <than@redhat.com> 1:3.3.4-21
- fix gcc4 build problem

* Wed Aug 10 2005 Than Ngo <than@redhat.com> 1:3.3.4-20
- apply missing patches

* Wed Aug 10 2005 Than Ngo <than@redhat.com> 1:3.3.4-19
- apply patch to fix wrong K menu width, #165510

* Mon Aug 01 2005 Than Ngo <than@redhat.com> 1:3.3.4-18
- add visibility patch

* Wed Jul 20 2005 Than Ngo <than@redhat.com> 1:3.3.4-17
- fix German translation of the Qt Assistent #161558

* Mon Jun 27 2005 Than Ngo <than@redhat.com> 1:3.3.4-16
- apply patch to fix Rendering for Punjabii, thanks to Trolltech #156504

* Tue May 24 2005 Than Ngo <than@redhat.com> 1:3.3.4-15
- add better fix for #156977, thanks to trolltech
- apply patch to fix keyReleaseEvent problem #156572

* Wed May 18 2005 Than Ngo <than@redhat.com> 1:3.3.4-14
- apply patch to use ecvt, fcvt (thanks to Jakub)
- fix a bug in printing of postscript #156977

* Wed May 18 2005 Than Ngo <than@redhat.com> 1:3.3.4-13
- rebuild

* Thu Apr 14 2005 Than Ngo <than@redhat.com> 1:3.3.4-12
- fix bad symlink #154086

* Wed Apr 13 2005 Than Ngo <than@redhat.com> 1:3.3.4-11
- remove bad symlink #154086
- built with PostgresSQL 8.0.2

* Wed Mar 23 2005 Than Ngo <than@redhat.com> 1:3.3.4-10
- add GtkStyle patch from Peter Backlund #141125

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 1:3.3.4-9
- fix buildkey issue with gcc-4

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 1:3.3.4-8
- rebuilt against gcc-4.0.0-0.31

* Tue Mar 01 2005 Than Ngo <than@redhat.com> 1:3.3.4-7
- fix build problem with gcc4

* Mon Feb 28 2005 Than Ngo <than@redhat.com> 1:3.3.4-6
- rebuilt against gcc-4

* Tue Feb 22 2005 Than Ngo <than@redhat.com> 1:3.3.4-5
- fix application crash when input methode not available (bug #140658)
- remove .moc/.obj
- add qt-copy patch to fix KDE #80072

* Fri Feb 11 2005 Than Ngo <than@redhat.com> 1:3.3.4-4
- update qt-x11-immodule-unified patch

* Thu Feb 10 2005 Than Ngo <than@redhat.com> 1:3.3.4-3 
- fix rpm file conflict

* Wed Feb 02 2005 Than Ngo <than@redhat.com> 1:3.3.4-2
- remove useless doc files #143949
- fix build problem if installman is disable #146311
- add missing html/examples/tutorial symlinks

* Fri Jan 28 2005 Than Ngo <than@redhat.com> 1:3.3.4-1
- update to 3.3.4
- adapt many patches to qt-3.3.4
- drop qt-x11-free-3.3.0-freetype, qt-x11-free-3.3.3-qmake, qt-x11-free-3.3.1-lib64
  qt-x11-free-3.3.3-qimage, which are included in new upstream

* Tue Nov 30 2004 Than Ngo <than@redhat.com> 1:3.3.3-16
- add sql macro

* Mon Nov 29 2004 Than Ngo <than@redhat.com> 1:3.3.3-15
- convert qdial.3qt to UTF-8 bug #140946

* Tue Nov 23 2004 Than Ngo <than@redhat.com> 1:3.3.3-14
- add missing lupdate and lrelease #140230

* Fri Nov 19 2004 Than Ngo <than@redhat.com> 1:3.3.3-13 
- apply patch to fix qinputcontext

* Thu Nov 11 2004 Than Ngo <than@redhat.com> 1:3.3.3-12
- link against MySQL 3
- fix rpm conflict

* Wed Nov 10 2004 Than Ngo <than@redhat.com> 1:3.3.3-11
- apply patch to fix fullscreen problem
- remove html documents duplicate #135696

* Tue Nov 02 2004 Than Ngo <than@redhat.com> 1:3.3.3-10
- rebuilt

* Tue Nov 02 2004 Than Ngo <than@redhat.com> 1:3.3.3-9
- remove unused patch
- set XIMInputStyle=On The Spot
- require xorg-x11-devel instead XFree86-devel

* Thu Oct 14 2004 Than Ngo <than@redhat.com> 1:3.3.3-8
- don't compress examples/tutorial

* Thu Oct 07 2004 Than Ngo <than@redhat.com> 1:3.3.3-7
- fix build problem without qt immodule #134918

* Tue Sep 28 2004 Than Ngo <than@redhat.com> 1:3.3.3-6
- fix font problem, bz #133578

* Tue Sep 14 2004 Than Ngo <than@redhat.com> 1:3.3.3-4
- update new immodule patch
- fix multilib problem #132516

* Wed Aug 18 2004 Than Ngo <than@redhat.com> 1:3.3.3-3
- add patch to fix dlopen issue (#126422)
- add image handling fix

* Thu Aug 12 2004 Than Ngo <than@redhat.com> 1:3.3.3-2
- fix qmake broken link (#129723)

* Wed Aug 11 2004 Than Ngo <than@redhat.com> 1:3.3.3-1
- update to 3.3.3 release

* Thu Jul 01 2004 Than Ngo <than@redhat.com> 1:3.3.2-10
- add immodule for Qt

* Tue Jun 29 2004 Than Ngo <than@redhat.com> 1:3.3.2-9
- add sub package config, allow multi lib installation (#126643)

* Thu Jun 24 2004 Than Ngo <than@redhat.com> 1:3.3.2-8
- add fontconfig fix for qfontdatabase, #123868
- fix some buildrequires problem, #125289
- fix dangling symlink, #125351
- get rid of backup files

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 1:3.3.2-7
- rebuilt

* Tue May 25 2004 Than Ngo <than@redhat.com> 1:3.3.2-5
- add missing qembed tool #124052, #124052
- get rid of unused trigger
- add qt.conf in ld.so.conf.d -> don't change ld.so.conf #124080

* Wed May 12 2004 Than Ngo <than@redhat.com> 1:3.3.2-4
- backport some qt patches, Symbol font works again

* Mon May 10 2004 Than Ngo <than@redhat.com> 1:3.3.2-3
- fixed annoying warning

* Tue May 04 2004 Than Ngo <than@redhat.com> 1:3.3.2-2
- fix broken symlink at qt document, bug #121652

* Thu Apr 29 2004 Than Ngo <than@redhat.com> 3.3.2-1
- update to 3.3.2

* Thu Apr 22 2004 Than Ngo <than@redhat.com> 3.3.1-1
- add cvs backport
- fix lib64 issue, #121052
- fix CJK font display, bug #121017, #120542, thanks to Leon Ho
- compress tutorial/examples

* Fri Mar 26 2004 Than Ngo <than@redhat.com> 3.3.1-0.8
- fixed symlinks issue, #117572

* Thu Mar 25 2004 Than Ngo <than@redhat.com> 3.3.1-0.7
- add Trolltech patch, fix dpi setting issue

* Tue Mar 23 2004 Than Ngo <than@redhat.com> 3.3.1-0.6
- add 0034-qclipboard_recursion_fix.patch from CVS, #118368
- add better qt-x11-free-3.3.1-fontdatabase.patch

* Sun Mar 07 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.5
- disable smpflags

* Fri Mar 05 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.4
- fix font alias

* Thu Mar 04 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.3
- add fontdatabase fix from Trolltech

* Thu Mar 04 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.2
- fix wrong symlink #117451

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 01 2004 Than Ngo <than@redhat.com> 3.3.1-0.1
- update to 3.3.1

* Mon Feb 23 2004 Than Ngo <than@redhat.com> 3.3.0-0.4
- add fix for building with freetype 2.1.7 or newer

* Tue Feb 17 2004 Than Ngo <than@redhat.com> 3.3.0-0.3 
- enable IPv6 support
- use dlopen, instead of linking with OpenGL libraries directly
- don't install backup files

* Thu Feb 05 2004 Than Ngo <than@redhat.com> 1:3.3.0-0.2
- fix fontdatabase
- don't use strip in install script
- fix qt default setting
 
* Wed Feb 04 2004 Than Ngo <than@redhat.com> 1:3.3.0-0.1
- 3.3.0

* Fri Jan 30 2004 Than Ngo <than@redhat.com> 1:3.2.3-0.4
- add mouse patch from CVS, bug #114647

* Tue Jan 20 2004 Than Ngo <than@redhat.com> 1:3.2.3-0.3
- rebuild

* Tue Dec  2 2003 Than Ngo <than@redhat.com> 1:3.2.3-0.2
- Added missing prl files, (report from trolltech)
- Fixed description
- include requires XFree86-devel on qt-devel
 
* Fri Nov 14 2003 Than Ngo <than@redhat.com> 1:3.2.3-0.1
- 3.2.3 release

* Thu Oct 30 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.4
- fix encoding problem

* Sat Oct 18 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.3
- fix encoding problem

* Fri Oct 17 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.2
- add font alias patch file, thanks to Leon Ho
- clean up monospace.patch from Leon Ho
- remove some unneeded patch files

* Thu Oct 16 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.1
- 3.2.2 release
- remove a patch file, which is included in 3.2.2

* Tue Oct 14 2003 Than Ngo <than@redhat.com> 1:3.2.1-1.3
- remove some unneeded patch files
- don't load XLFDs if XFT2 is used

* Mon Sep 08 2003 Than Ngo <than@redhat.com> 1:3.2.1-1.2
- fixed rpm file list

* Tue Sep 02 2003 Than Ngo <than@redhat.com> 1:3.2.1-1.1
- fix for the khtml form lineedit bug from CVS

* Wed Aug 27 2003 Than Ngo <than@redhat.com> 1:3.2.1-1
- 3.2.1 release

* Wed Jul 23 2003 Than Ngo <than@redhat.com> 1:3.2.0-1
- 3.2.0 release

* Mon Jun 23 2003 Than Ngo <than@redhat.com> 3.2.0b2-0.1
- 3.2.0b2
- add missing templates for designer

* Wed Jun 18 2003 Than Ngo <than@redhat.com> 3.2.0b1-0.2
- clean up specfile

* Wed Jun 18 2003 Than Ngo <than@redhat.com> 3.2.0b1-0.1
- 3.2.0b1

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.1.2-12
- rebuilt

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.1.2-10
- add missing translations

* Wed Jun 11 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 19 2003 Than Ngo <than@redhat.com> 3.1.2-7
- add some patches from KDE CVS qt-copy, thanks to Alexei Podtelezhnikov

* Mon May  5 2003 Than Ngo <than@redhat.com> 3.1.2-5.1
- set correct permission config scripts

* Tue Apr 29 2003 Than Ngo <than@redhat.com> 3.1.2-4
- fix typo bug in font loader

* Wed Apr  9 2003 Than Ngo <than@redhat.com> 3.1.2-2
- add xrandr extension

* Mon Mar  3 2003 Than Ngo <than@redhat.com> 3.1.2-1
- 3.1.2 release

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com> 3.1.1-7
- ppc64 support

* Wed Jan 29 2003 Than Ngo <than@redhat.com> 3.1.1-6
- add missing Categories section in qt designer #82920

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 30 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- Change qmlined.h to not include an attic header that is also not shipped
  with Red Hat Linux. This also fixes building unixODBC, that includes this
  header (apparently also without needing it).

* Thu Dec 19 2002 Than Ngo <than@redhat.com> 3.1.1-3
- add monospace patch file from Leon Ho (bug #79949)
- add small patch file from Sysoltsev Slawa (bug #79731)

* Tue Dec 17 2002 Than Ngo <than@redhat.com> 3.1.1-2
- don't require XFree86, it's not needed

* Tue Dec 17 2002 Than Ngo <than@redhat.com> 3.1.1-1
- update to 3.1.1

* Thu Nov 28 2002 Than Ngo <than@redhat.com> 3.1.0-1.3
- don't write Date into created moc files

* Mon Nov 18 2002 Than Ngo <than@redhat.com> 3.1.0-1.2
- add missing libs
- remove workaround for ppc

* Sun Nov 17 2002 Than Ngo <than@redhat.com> 3.1.0-1.1
- adjust qfontdatabase_x11 for 3.1.0
- fix lib64 issue
- add workaround to build on ppc

* Wed Nov 13 2002 Than Ngo <than@redhat.com> 3.1.0-1
- update to 3.1.0
- adjust some patch files for 3.1.0
- clean up specfile
- remove some Xft2 patch files, which are now in 3.1.0
- add qwidget_x11.cpp.diff from Trolltech
- install qt in %%{_libdir}/qt-3.1 (bug #77706)
- don't use rpath
- enable large file support
- use system Xinerama
- remove unneeded cups patch file
- fix to build against new XFree86

* Tue Nov  5 2002 Than Ngo <than@redhat.com> 3.0.5-19
- examples misconfigured (bug #76083)
- don't include pkg-config (bug #74621)
- fix build problem with new XFree86

* Tue Sep 17 2002 Than Ngo <than@redhat.com> 3.0.5-18
- Fixed binaries symlinks

* Mon Sep  9 2002 Than Ngo <than@redhat.com> 3.0.5-17hammer
- clean up spec file for 64bit machine

* Thu Aug 29 2002 Than Ngo <than@redhat.com> 3.0.5-17
- Fixed rpath issue (bug #69692, #69575)
- Removed dlopen patch
- Added monospace alias patch from Leon Ho (bug #72811)
- Added man pages

* Sun Aug 25 2002 Than Ngo <than@redhat.com> 3.0.5-16
- Added missing catagory in qt designer
- Added small gb18030 patch file from Leon Ho

* Thu Aug 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-15
- Prereq fileutils (#71500)

* Tue Aug 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-14
- Don't link to libstdc++, it isn't used
- Work around s390 compiler bug (fpic/fPIC coexistance)
- Do away with the "Feature Bluecurve already defined" warning message
- Remove qmake cache files from the package

* Wed Aug 14 2002 Than Ngo <than@redhat.com> 3.0.5-13
- Added fix to use VT100 graphic characters (bug #71364)
- Added fontdatabase fix from llch@redhat.com (bug #68353)

* Mon Aug 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> [not built]
- Fix default qtrc

* Mon Aug 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-12
- Fix CJK Printing (#71123)

* Sun Aug 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-11
- Move qtconfig from qt-devel to qt, it's generally useful
- Use -fno-use-cxa-atexit
- Some tweaks to allow building Qt/Embedded with the same spec file
- Apply the GB18030 patch even if xft2 isn't set

* Fri Aug  9 2002 Than Ngo <than@redhat.com> 3.0.5-10
- Added XIM patch from llch@redhat.com (bug #70411)

* Sun Aug  4 2002 Than Ngo <than@redhat.com> 3.0.5-9
- add a missing patch file (closelock/openlock)

* Thu Aug  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-8
- Define QT_INSTALL_PREFIX in qmake

* Thu Aug  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-7
- Find correct location of qmake mkspecs even if QTDIR isn't set

* Thu Jul 25 2002 Than Ngo <than@redhat.com> 3.0.5-6
- Check file descriptor before closelock
* Thu Jul 25 2002 Than Ngo <than@redhat.com> 3.0.5-5
- Fixed a bug in openlock

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 3.0.5-4
- Tiny tweaks to qt3 patch

* Tue Jul 23 2002 Owen Taylor <otaylor@redhat.com>
- Tiny fix to qt3.diff to not add '0' as a test character (#68964)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 3.0.5-2
- rebuild using gcc-3.2-0.1

* Mon Jul 22 2002 Than Ngo <than@redhat.com> 3.0.5-1
- 3.0.5
- Fixed dependencies issue

* Thu Jul 18 2002 Than Ngo <than@redhat.com> 3.0.4-12
- Added qt-clipfix from Harald Hoyer (bug #67648)

* Tue Jul 16 2002 Than Ngo <than@redhat.com> 3.0.4-11
- get rid of qt resource, it's now in redhat-artworks
- add some define to build for 7.3

* Thu Jul 11 2002 Than Ngo <than@redhat.com> 3.0.4-10
- add missing Buildprequires desktop-file-utils
- add patches for GB18030 (llch@redhat.com) bug #68430

* Tue Jul 09 2002 Than Ngo <than@redhat.com> 3.0.4-9
- add new desktop file for qt designer

* Fri Jul  5 2002 Jakub Jelinek <jakub@redhat.com> 3.0.4-8
- compile libXinerama.a with -fpic in Qt until XFree86 is fixed
- make %%xft2 work even if old Xft headers aren't installed

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-6
- Re-enable Xft2 now that fontconfig is fixed
- Require a version of fontconfig that works
- Use -fPIC rather than -fpic on alpha

* Tue Jun 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-5
- Revert to Xft1 for now, Xft2 is too unstable
- Exclude alpha for now to work around binutils bugs

* Tue Jun 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-4
- Add (and fix up) fontconfig patch

* Mon Jun  3 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-3
- Remove the glweak patch, it isn't needed after dropping XFree86 3.x

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May  5 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-1
- 3.0.4
- Make SQL plugins optional (buildtime)
- Register with pkgconfig

* Thu May 02 2002 Than Ngo <than@redhat.com> 3.0.3-12
- qtdir /usr/lib/qt3
- build against gcc-3.1-0.26
- add qt-3.0.3-glweak.patch 

* Wed Apr 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-11
- qt3-gcc2.96 should be in qt, not qt-devel

* Mon Apr 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-10
- Tweaks to allow parallel installations of Qt 3.x (gcc 2.96) and Qt 3.x
  (gcc 3.1)
- Fix up debug spewage at Qt designer startup

* Wed Apr 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-9
- Spec file fixes

* Wed Apr 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-8
- Get rid of non-threaded version, dlopen()'ing threaded code
  (like plugins) from non-threaded code is dangerous
- Add some fixes from qt-copy, fixing the ksplash crash some people
  have noticed on a first login
- Add translation fixes from CVS
- Patch example .pro files to build outside the Qt source tree (#63023)
- Fix various bugs

* Thu Apr 04 2002 Leon Ho <llch@redhat.com> 3.0.3-7
- fixes for CJK - qpsprinter
- fixes for CJK - gb18030

* Fri Mar 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-6
- Make sure it builds with both gcc 2.96 and 3.1

* Wed Mar 28 2002 Leon Ho <llch@redhat.com> 3.0.3-5
- fixes for CJK - qpsprinter

* Wed Mar 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-4
- Add CJK patches

* Tue Mar 26 2002 Than Ngo <than@redhat.com> 3.0.3-3
- fix loading kde styles

* Tue Mar 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-1
- Update to 3.0.3 final

* Thu Mar 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-0.cvs20020314.1
- Update to 3.0.3-pre, required for KDE3
- force -fPIC usage
- Remove conflict with qt2 < 2.3.2-1, the new qt2 2.3.1 is fixed and qt 2.3.2
  is broken
- Ship the qmake config files (so qmake works for building any 3rd party stuff,
  e.g. aethera)

* Wed Mar  6 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-2
- Add some fixes from KDE's qt-copy CVS
- Pluginize image formats

* Mon Feb 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-1
- 3.0.2 final

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020118.3
- Add GB18030 codec patch, #60034
- Force-build jpeg support, fixing #59775 and #59795

* Sat Jan 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020118.2
- Build with CUPS support

* Fri Jan 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020118.1
- Fix up /usr/bin/moc links, they should point to qt3

* Mon Jan 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020114.1
- Build styles directly into the main library for now, there's too much broken
  code out there depending on this ATM.

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020109.1
- Stop excluding alpha, gcc has been fixed

* Tue Jan  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020108.1
- Add fixes from CVS; this fixes the "Alt + F1, arrow up, arrow up doesn't work
  in KDE" bug

* Mon Dec 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.1-2
- Fix up settings search path
- Add default qtrc allowing to use KDE 3.x Qt plugins
- Make sure QLibrary uses RTLD_GLOBAL when dlopen()ing libraries

* Thu Dec 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.1.0-1
- Work around gcc bug #57467

* Wed Dec 12 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.0.1 final

* Mon Dec 10 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.1-0.cvs20011210.1
- Update to current (needed by KDE 3.x)
- Rebuild with current libstdc++
- Temporarily disable building on alpha
- Fix build with PostgreSQL 7.2

* Mon Nov 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-5
- Fix up glweak

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-4
- Give designer, uic, moc, etc. their real names - the qt2 versions
  have been renamed in qt2-2.3.2-1.
  Conflict with qt2 < 2.3.2-1.

* Thu Oct 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-3
- Add symlink /usr/lib/qt-3.0.0 -> /usr/lib/qt3 and set QTDIR to the
  symlink, allowing to update to 3.0.1 without breaking rpath'ed binaries

* Tue Oct 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-1
- 3.0.0 final
- fix some minor specfile bugs
- Modularize some more (image format plugins)
- Build codecs

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta5.1
- beta5
- Share more code between qt-x11 and qt-embedded builds

* Wed Aug 29 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta4.1
- beta4
- build the Motif style directly into Qt rather than as a plugin - Qt should
  always have at least one style...
- replace the designer3 symlink with a shell script that sets QTDIR correctly
  before launching designer
- Add desktop file for designer

* Mon Aug  6 2001 Tim Powers <timp@redhat.com> 3.0.0-0.beta3.4
- explicitly include qm2ts, qmake, qtconfig in the devel package file list to avoid dangling symlinks

* Thu Aug  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta3.3
- Try yet another workaround for buildsystem breakages

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add another ugly workaround for build system problems, this should finally
  get rid of the dangling symlinks

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta3.2
- Rephrase parts of the spec file, hopefully pleasing the build system

* Sun Jul 29 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta3.1
- beta3
- Fix dangling symlinks

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta1.2
- Fix up QSQL Postgres classes for Postgres 7.1.x
- Fix various bugs:
  - QtMultilineEdit and QtTableView should actually compile
  - Link libqsqlpsql with libpq
  - Don't link the base library with libmysqlclient, linking the MySQL
    module with it is sufficient
- Add missing const qualifier
- move the SQL drivers to separate packages to avoid dependencies
- build and install designer plugins - converting glade files to Qt is fun. ;)
- handle RPM_OPT_FLAGS

* Tue May 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta1.1
- 3.0 beta 1

* Wed May 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20010516.1
- Update, remove conflicts with Qt 2.x

* Mon May 14 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20010514.1
- Initial build of 3.0 branch

* Fri Apr 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.0-6
- Fix crashes on ia64, Patch from Bill Nottingham <notting@redhat.com>
- Allow building qt-nox

* Fri Apr 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.0-5
- Make sure uic and designer use the libqui from the source tree, not
  a previously installed one.
  Linking uic-x11 against libqui-embedded is definitely not a feature. ;)
- The qclipboard fix is needed for qt-x11 only, don't apply it if we're
  building qt-embedded

* Sat Apr 14 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Handle LPRng specific constructs in printcap, Bug #35937

* Sun Mar 25 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add qfont patch from Trolltech

* Tue Mar 13 2001 Harald Hoyer <harald@redhat.de>
- added patch for '@euro' language settings

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.0 final
- BuildRequires XFree86-devel >= 4.0.2 (#30486)

* Mon Feb 26 2001 Than Ngo <than@redhat.com>
- fix check_env function, so that qt does not crash if QT_XFT is not set
- fix symlinks

* Mon Feb 26 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.0b1
- Add a patch to qpsprinter that handles TrueType fonts even if they come from xfs

* Tue Feb 13 2001 Preston Brown <pbrown@redhat.com>
- japanese input and clipboard fixes applied.  Changes have been sent upstream by patch authors.

* Fri Feb  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild with new Mesa to get rid of pthreads linkage
- Add Xft fix from KDE CVS

* Wed Feb  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add printing bugfix patch from Trolltech

* Sat Feb  3 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.4
- Qt Embedded: Add QVfb and VNC support

* Tue Jan 16 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't segfault when running Qt/Embedded applications as root
- Improve the Qt/Embedded sparc patch so we don't need the specfile hacks
  anymore
- Fix a bug in QPrintDialog (causing KDE Bug #18608)

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- bzip2 source to save space
- Qt/Embedded 2.2.3
- Fix qte build on sparc

* Wed Dec 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Run ldconfig in %%post and %%postun for qt-Xt

* Sun Dec 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Build with the Xrender extension
  (Patch from Keith Packard <keithp@keithp.com>)

* Wed Dec 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.3

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to fix permissions on doc dir
- Don't exclude ia64 anymore

* Fri Nov 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up uic (Patch from trolltech) 

* Wed Nov 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Build qt-embedded
  changes to base: fix build, fix ISO C99 compliance, fix 64bit support

* Mon Nov 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.2

* Tue Oct 24 2000 Than Ngo <than@redhat.com>
- call ldconfig for updating (Bug #19687)
- added patch from Trolltech, thanks to Rainer <rms@trolltech.com>

* Wed Oct 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add missing msg2qm, msgmerge, qconfig tools (Bug #18997), introduced
  by broken Makefiles in base
- fix up %%install so it works both with old-style and new-style fileutils
  (fileutils <= 4.0z don't know about -L)

* Fri Oct 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Disable exception handling; this speeds up KDE 2.x and reduces its
  memory footprint by 20 MB.

* Tue Oct 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- dereference symlinks in include

* Sun Oct  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix -devel
- update to the new version of 2.2.1 on trolltech.com; the initial tarball
  contained broken docs

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.1

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add missing uic

* Thu Sep 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move Qt designer to a different source RPM to get rid of a
  circular dependency (kdelibs2->qt, qt->kdelibs2)
- Enable MNG support
- Don't compile (just include) examples and tutorials
- move the static libraries to a separate package (qt-static).
  They're HUGE, and most people won't ever need them.
- clean up spec file
- fix up dependencies (-devel requires base, -static requires devel,
  Xt requires base)
- add BuildRequires line

* Tue Sep 12 2000 Than Ngo <than@redhat.com>
- update release 2.2.0
- changed copyright to GPL
- added missing static libraries
- made symbolic link for designer to load the help files correct
- made designer and designer-kde2 as sub packages
- added missing templates for designer
- remove jakub patch, since the release 2.2.0 already 
  contains this patch.
- fixed qt again to compile with gcc-2.96
- use make -j for building

* Wed Aug 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Work around compiler bugs (Patch from Jakub)
- Use relative symlinks (Bug #16750)

* Mon Aug 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta2

* Mon Aug 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new qt-copy from KDE2 CVS

* Wed Aug 9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- official beta 1

* Thu Aug 3 2000 Than Ngo <than@redhat.de>
- rebuilt against the libpng-1.0.8

* Thu Jul 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild (so we have it on all arches)

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move man pages to a more reasonable place (this fixes Bug #14126)
- exclude ia64 for now (compiler problems!!!)

* Mon Jul 24 2000 Harald Hoyer <harald@redhat.de>
- modified connect patch to fit qt 2.2.0 beta.

* Thu Jul 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current qt-copy; this is now a qt 2.2.0 beta.

* Mon Jul 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current qt-copy in kde CVS, required

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 11 2000 Harald Hoyer <harald@redhat.de>
- made patch smaller and binary compatible when recompiled with 6.2
- modified connect and moc to cope with the new g++ class layout

* Sun Jul 09 2000 Than Ngo <than@redhat.de>
- rebuilt qt with gcc-2.96-34

* Fri Jul 07 2000 Than Ngo <than@redhat.de>
- rebuilt qt with c++ 2.96

* Mon Jul  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix dependancies

* Sun Jul  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Use egcs++ for now ** FIXME

* Wed Jun 28 2000 Preston Brown <pbrown@redhat.com>
- fix up qt.sh

* Sun Jun 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Build in jpeg and threading support
- Fix a bug in clipboard pasting code

* Wed Jun 07 2000 Preston Brown <pbrown@redhat.com>
- fix qt.{sh,csh}
- use new rpm macro paths
- package man pages

* Fri Jun  2 2000 Bill Nottingham <notting@redhat.com>
- build without optimization on ia64

* Mon May 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.1.1

* Thu May 18 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- recompile with correct libstdc++

* Thu Apr 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.1.0 final

* Wed Apr  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta4
- depend on libGL.so.1 rather than Mesa - XFree86 4.0 provides that
  lib, too

* Wed Mar 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta3

* Tue Mar  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta2
- fix compilation of the NSPlugin add-on

* Fri Mar  3 2000 Bill Nottingham <notting@redhat.com>
- fix %%postun script

* Fri Feb 18 2000 Bernhard Rosenkränzer <bero@redhat.com>
- beta1
- get rid of qt-ImageIO, the functionality is now in the main Qt library
- remove qt-Network, the functionality is now in the main Qt library
- add changes-2.1.0 to %%doc

* Thu Feb 17 2000 Preston Brown <pbrown@redhat.com>
- no refcount check on postun script, we want it to happen even on upgrades

* Thu Feb 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot, should fix QWhatsThisButton
- remove executable permissions from *.pro files

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- strip binaries in examples, tutorial

* Mon Jan 31 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot - should fix the hotkey bug
- Fix up the Makefiles so it compiles

* Tue Jan 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot - we need those QVariant fixes

* Thu Jan 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- switch from glxMesa to Mesa for the GL addon

* Wed Jan 5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix up dependencies
- new snapshot

* Mon Jan 3 2000 Ngo Than <than@redhat.de>
- new snapshot for Red Hat Linux 6.2
- increase version number

* Mon Dec 20 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- handle RPM_OPT_FLAGS

* Mon Dec 13 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- -GL requires libGL.so.1 instead of Mesa (might as well be glxMesa
  or some commercial OpenGL)
- -GL BuildPrereqs /usr/X11R6/include/GL/gl.h instead of Mesa-devel
  (might as well be glxMesa or some commercial OpenGL)

* Sun Dec 05 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current RSYNC version
- remove compilation patch - it finally works out of the box

* Wed Oct 27 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current CVS snapshot
- build extensions
- add patch to fix QNetwork compilation

* Sun Oct 24 1999 Bernhard Rosenkraenzer <bero@redhat.de>
- current CVS snapshot
- fix compilation with gcc 2.95.x
- use install -c rather than just install to make BSD install happy

* Mon Oct 11 1999 Bernhard Rosenkraenzer <bero@redhat.de>
- 2.1.0 snapshot (for KDE2)
- Fix typo in spec

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- don't ship tutorial or example binaries

* Tue Sep 21 1999 Preston Brown <pbrown@redhat.com>
- substitution in tutorial and examples so that dependencies are correct and
  they can be successfully rebuilt.
- switched to completely using QTDIR.  trying to coexist with links into
  /usr/{include,lib} and still compile with qt 1.x is very hard for
  configure scripts to cope with.

* Thu Aug 19 1999 Preston Brown <pbrown@redhat.com>
- implemented QTDIR compatibility.

* Tue Jul 20 1999 Preston Brown <pbrown@redhat.com>
- qt 2.0.1 packaged.

* Wed Jul 14 1999 Preston Brown <pbrown@redhat.com>
- Qt 2.00 packaged.
- examples, html documentation, tutorial moved to /usr/doc

* Sat Apr 17 1999 Preston Brown <pbrown@redhat.com>
- static library supplied in dev package.

* Wed Apr 07 1999 Preston Brown <pbrown@redhat.com>
- turn on internal GIF reading support

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Mon Mar 15 1999 Preston Brown <pbrown@redhat.com>
- upgrade to qt 1.44.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Jan 19 1999 Preston Brown <pbrown@redhat.com>
- moved includes to /usr/include/qt

* Mon Jan 04 1999 Preston Brown <pbrown@redhat.com>
- made setup phase silent.

* Fri Dec 04 1998 Preston Brown <pbrown@redhat.com>
- upgraded to qt 1.42, released today.

* Tue Dec 01 1998 Preston Brown <pbrown@redhat.com>
- took Arnts RPM and made some minor changes for Red Hat.
