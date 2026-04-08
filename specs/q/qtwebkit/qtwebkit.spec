# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# qtwebkit is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%global _lto_cflags %{nil}

%global _hardened_build 1

Name: qtwebkit
Summary: Qt WebKit bindings

Version: 2.3.4
Release: 46%{?dist}

# Automatically converted from old format: LGPLv2 with exceptions or GPLv3 with exceptions - review is highly recommended.
License: LGPL-2.0-or-later WITH FLTK-exception OR LicenseRef-Callaway-GPLv3-with-exceptions
URL: http://trac.webkit.org/wiki/QtWebKit
Source0: http://download.kde.org/stable/qtwebkit-2.3/%{version}/src/qtwebkit-%{version}.tar.gz
# qmake wrapper
Source1:  qmake.sh

# search /usr/lib{,64}/mozilla/plugins-wrapped for browser plugins too
Patch1: webkit-qtwebkit-2.2-tp1-pluginpath.patch

# smaller debuginfo s/-g/-g1/ (debian uses -gstabs) to avoid 4gb size limit
Patch3: qtwebkit-2.3-debuginfo.patch

# tweak linker flags to minimize memory usage on "small" platforms
Patch4: qtwebkit-2.3-save_memory.patch

# use SYSTEM_MALLOC on ppc/ppc64, plus some additional minor tweaks (needed only on ppc? -- rex)
Patch10: qtwebkit-ppc.patch

# add missing function Double2Ints(), backport
# rebased for 2.3.1, not sure if this is still needed?  -- rex
Patch11: qtwebkit-23-LLInt-C-Loop-backend-ppc.patch

# truly madly deeply no rpath please, kthxbye
Patch14: webkit-qtwebkit-23-no_rpath.patch

# Port to python3
Patch15: webkit-qtwebkit-23-port-python3.patch
# Fix compilation with gcc14 -Werror=incompatble-pointer-types
# wrt constness for libxml2 xmlError
# ref: https://gitlab.gnome.org/GNOME/libxml2/-/commit/61034116d0a3c8b295c6137956adc3ae55720711
Patch16: webkit-qtwebkit-23-xmlerror-constness.patch

## upstream patches
# backport from qt5-qtwebkit
# qtwebkit: undefined symbol: g_type_class_adjust_private_offset
# https://bugzilla.redhat.com/show_bug.cgi?id=1202735
Patch100: webkit-qtwebkit-23-gcc5.patch
# backport from qt5-qtwebkit: URLs visited during private browsing show up in WebpageIcons.db
Patch101: webkit-qtwebkit-23-private_browsing.patch
# fix FTBFS with bison-3.7
Patch102: qtwebkit-bison-3.7.patch
# fix FTBFS wtih glib ≥ 2.68
Patch103: webkit-qtwebkit-23-glib2.patch

BuildRequires: make
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc-c++
BuildRequires: gperf
BuildRequires: libicu-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0) >= 2.10
BuildRequires: pkgconfig(fontconfig)
# gstreamer media support
%if 0%{?fedora} || 0%{?rhel} > 7
%global gstreamer1 1
BuildRequires: pkgconfig(gstreamer-1.0) pkgconfig(gstreamer-app-1.0)
%else
# We don't want to use GStreamer 1 where the rest of the Qt 4 stack doesn't,
# or we run into symbol conflicts. So build against GStreamer 0.10 on Fedora up
# to 20 and RHEL up to 7. (Up to RHEL 6, GStreamer 0.10 is the only option.)
BuildRequires: pkgconfig(gstreamer-0.10) pkgconfig(gstreamer-app-0.10)
%endif
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(QtCore) pkgconfig(QtNetwork)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xrender)
BuildRequires: perl(version)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Getopt::Long)
BuildRequires: python3-devel
BuildRequires: ruby ruby(rubygems)
%if 0%{?fedora} || 0%{?rhel} > 7
# qt-mobility bits
BuildRequires: pkgconfig(QtLocation) >= 1.2
BuildRequires: pkgconfig(QtSensors) >= 1.2
%endif
# workaround bad embedded png files, https://bugzilla.redhat.com/1639422
BuildRequires:  findutils
BuildRequires:  pngcrush
BuildRequires:  perl-File-Find perl-FindBin perl-lib perl-English

Obsoletes: qt-webkit < 1:4.9.0
Provides: qt-webkit = 2:%{version}-%{release}
Provides: qt4-webkit = 2:%{version}-%{release}
Provides: qt4-webkit%{?_isa} = 2:%{version}-%{release}

Requires: mozilla-filesystem
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%global glib2_version %(pkg-config --modversion glib-2.0 2>/dev/null || echo "2.10")
## Naughty glib2, adding new symbols without soname bump or symbol versioning... -- rex
## https://bugzilla.redhat.com/show_bug.cgi?id=1202735
Requires: glib2%{?_isa} >= %{glib2_version}

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: qt-webkit-devel < 1:4.9.0
Provides:  qt-webkit-devel = 2:%{version}-%{release}
Provides:  qt4-webkit-devel = 2:%{version}-%{release}
Provides:  qt4-webkit-devel%{?_isa} = 2:%{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q -c -n webkit-qtwebkit-23

%patch -P1 -p1 -b .pluginpath
%patch -P3 -p1 -b .debuginfo
%patch -P4 -p1 -b .save_memory
%ifarch ppc ppc64 ppc64le s390 s390x %{mips}
%patch -P10 -p1 -b .system-malloc
%endif
%ifarch ppc ppc64 s390 s390x mips mips64
# all big-endian arches require the Double2Ints fix
# still needed?  -- rex
%patch -P11 -p1 -b .Double2Ints
%endif
%patch -P14 -p1 -b .no_rpath
%patch -P15 -p1 -b .python3
%patch -P16 -p1 -b .xmlerror

%patch -P100 -p1 -b .gcc5
%patch -P101 -p1 -b .private_browsing
%if 0%{?fedora} > 33 || 0%{?rhel} > 8
%patch -P102 -p1 -b .bison37
%endif
%if 0%{?fedora} > 34 || 0%{?rhel} > 8
%patch -P103 -p1 -b .glib2
%endif

install -m755 -D %{SOURCE1} bin/qmake

# find/fix pngs with "libpng warning: iCCP: known incorrect sRGB profile"
find -name \*.png | xargs -n3 pngcrush -ow -fix


%build 
# add an unversioned python symlink to python3 to the PATH (FTBFS #1736570)
mkdir python3-unversioned-command
ln -s %{__python3} python3-unversioned-command/python

CFLAGS="%{optflags}"; export CFLAGS
CXXFLAGS="%{optflags}"; export CXXFLAGS
LDFLAGS="%{?__global_ldflags}"; export LDFLAGS
PATH=`pwd`/python3-unversioned-command:`pwd`/bin:%{_qt4_bindir}:$PATH; export PATH
QMAKEPATH=`pwd`/Tools/qmake; export QMAKEPATH
QTDIR=%{_qt4_prefix}; export QTDIR

%ifarch aarch64 %{mips}
%global qtdefines  DEFINES+=ENABLE_JIT=0 DEFINES+=ENABLE_YARR_JIT=0 DEFINES+=ENABLE_ASSEMBLER=0
%endif

mkdir -p %{_target_platform}
pushd    %{_target_platform}
WEBKITOUTPUTDIR=`pwd`; export WEBKITOUTPUTDIR
../Tools/Scripts/build-webkit \
  --qt %{?qtdefines} \
  --no-webkit2 \
  --release \
  --qmakearg="CONFIG+=production_build DEFINES+=HAVE_LIBWEBP=1" \
  --makeargs="%{?_smp_mflags}" \
  --system-malloc
popd

  
%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}/Release

## pkgconfig love
# drop Libs.private, it contains buildroot references, and
# we don't support static linking libQtWebKit anyway
pushd %{buildroot}%{_libdir}/pkgconfig
grep -v "^Libs.private:" QtWebKit.pc > QtWebKit.pc.new && \
mv QtWebKit.pc.new QtWebKit.pc
popd


%ldconfig_scriptlets

%files
%{_qt4_libdir}/libQtWebKit.so.4*
%if 0%{?_qt4_importdir:1}
%{_qt4_importdir}/QtWebKit/
%endif

%files devel
%{_qt4_datadir}/mkspecs/modules/qt_webkit.pri
%{_qt4_headerdir}/QtWebKit/
%{_qt4_libdir}/libQtWebKit.prl
%{_qt4_libdir}/libQtWebKit.so
%{_libdir}/pkgconfig/QtWebKit.pc


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 31 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.4-44
- Port to python3
- Fix for gcc14 -Werror=incompatible-pointer-types with libxml2 constness change

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.3.4-43
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 16 2021 Than Ngo <than@redhat.com> - 2.3.4-35
- Fixed FTBFS with glib2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 31 2020 Than Ngo <than@redhat.com> - 2.3.4-32
- Fixed FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-31
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Aug 11 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.3.4-28
- Remove obsolete comments about source tarball generation (an upstream release
  tarball has been used for years and there is and will be no better source)
- Drop the extra no-sse2 build on i686, Fedora has required SSE2 since F29

* Sun Aug 11 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.3.4-27
- Fix FTBFS due to unversioned python no longer being Python 2 (#1736570)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.3.4-24
- QtWebkit bundles malformed PNG files (#1639422)

* Sat Jul 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.3.4-23
- BR: %%_bindir/python gcc-c++ (#1606056)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.3.4-21
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 25 2017 Troy Dawson <tdawson@redhat.com> - 2.3.4-19
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 2.3.4-14
- Rebuild (libwebp)

* Tue Jan 31 2017 Merlin Mathesius <mmathesi@redhat.com> - 2.3.4-13
- Add BuildRequires: python to fix FTBFS (BZ#1418102).

* Wed Nov 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.3.4-12
- rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Michal Toman <mtoman@fedoraproject.org> - 2.3.4-10
- Add support for MIPS (#1294886)

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.3.4-9
- Rebuilt for libwebp soname bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.3.4-7
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 2.3.4-6
- QtWebKit logs visited URLs to WebpageIcons.db in private browsing mode (#1204795)

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 2.3.4-5
- drop ppc64le patch (that no longer applies or is needed)

* Fri Mar 20 2015 Rex Dieter <rdieter@fedoraproject.org> - 2.3.4-4
- gcc-5.0.0-0.20.fc23 FTBFS qtwebkit (#1203008)
- add versioned glib2 dep (#1202735)

* Tue Mar 17 2015 Rex Dieter <rdieter@fedoraproject.org> 2.3.4-3
- qtwebkit enable jit for ppc64le (#1096330)

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 2.3.4-2
- rebuild (gcc5)

* Thu Oct 16 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.4-1
- qtwebkit-2.3.4

* Tue Sep 23 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-18
- enable hardened build (#1051790)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.3-16
- build against GStreamer1 on F21+ (#1092642, patch from openSUSE)

* Fri Jun 20 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-15
- use pkgconfig deps for qt-mobility

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Jaromir Capik <jcapik@redhat.com> - 2.3.3-13
- ppc64le support

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-12
- Requires: mozilla-filesystem (#1000673)

* Fri May 02 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-11
- no need to set empty qtdefines macro
- no rpath for real, drop chrpath hacks

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.3-10
- rebuild against fixed qt to fix -debuginfo (#1074041)

* Thu Mar 06 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.3-9
- update aarch64 patchset

* Fri Feb 28 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-8
- initial backport aarch64 javascriptcore fixes, needswork (#1070446)
- apply downstream patches *after* upstream ones

* Thu Feb 13 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-7
- backport more upstream fixes

* Thu Feb 13 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-6
- ftbfs using bison3

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-5
- rebuild (libicu)

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-4
- rebuild (libwebp)

* Wed Dec 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 2.3.3-3
- support out-of-source-tree build
- %%ix86: build both no-sse2 and sse2 versions

* Mon Dec 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-2
- build-webkit --system-malloc (unconditionally, WAS only ppc)

* Thu Oct 03 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-1
- qtwebkit-2.3.3
- include some post 2.3.3 commits/fixes

* Thu Sep 12 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.2-3
- SIGSEGV - ~NonSharedCharacterBreakIterator (#1006539, webkit#101337)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.2-1
- qtwebkit-2.3.2

* Thu Apr 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 2.3.1-1
- qtwebkit-2.3.1
- -devel: drop explicit Requires: qt4-devel (let pkgconfig deps do it)

* Mon Mar 25 2013 Dan Horák <dan[at]danny.cz> 2.3.0-2
- use ppc fixes also on s390

* Fri Mar 15 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.0-1
- 2.3.0 (final)
- enable libwebp support
- .spec cleanup

* Sat Mar 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.6.rc1
- should use libxml and libxslt (#919778)

* Sat Mar 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.5.rc1
- qt_webkit_version.pri is missing in 2.3-rc1 package (#919477)

* Tue Mar 05 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.4.rc1
- 2.3-rc1

* Tue Mar 05 2013 Than Ngo <than@redhat.com> - 2.3-0.3.beta2
- add missing function Double2Ints() on ppc, backport

* Mon Feb 25 2013 Than Ngo <than@redhat.com> - 2.3-0.2.beta2
- fix 64k page issue on ppc/ppc64
- set -g1 on ppc/ppc64 to reduce archive size

* Thu Feb 21 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.1.beta2
- qtwebkit-2.3-beta2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-8
- fix rpath (#902571)

* Tue Jan 15 2013 Than Ngo <than@redhat.com> - 2.2.2-7
- use SYSTEM_MALLOC on ppc/ppc64

* Fri Jan 11 2013 Than Ngo <than@redhat.com> 2.2.2-6
- bz#893447, fix 64k pagesize issue

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-5
- segfault in requiresLineBox at rendering/RenderBlockLineLayout.cpp (#891464)

* Mon Dec 24 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-4
- switch to upstream versions of some patches

* Tue Nov 13 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-3
- Certain SVG content freezes QtWebKit (webkit#97258)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-1
- qtwebkit-2.2.2

* Fri May 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.1-6
- can't render Complex Text Layout (Hindi, Arabic) (#761337)

* Fri May 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.1-5
- respin tarball using upstream make-package.py tool

* Tue Jan 24 2012 Than Ngo <than@redhat.com> - 2.2.1-4
- gcc doesn't support flag -fuse-ld=gold yet
- fix build failure with gcc-4.7 

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Than Ngo <than@redhat.com> - 2.2.1-2
- backport the correct patch from trunk to fix glib-2.31 issue

* Mon Dec 19 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.1-1
- qtwebkit-2.2.1
- add explicit BR: pkgconfig(xext) pkgconfig(xrender)

* Sun Nov 27 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-3
- add explicit BR: libjpeg-devel libpng-devel

* Fri Nov 18 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-2
- fix FTBFS against newer glib

* Thu Sep 29 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-1
- qtwebkit-2.2.0 (final)
- more pkgconfig-style deps

* Wed Sep 14 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-0.1.rc1
- qtwebkit-2.2.0-rc1

* Tue Sep 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-16.week35
- qtwebkit-2.2-week35 snapshot

* Thu Sep 01 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-15.week34
- qtwebkit-2.2-week34 snapshot

* Sat Aug 27 2011 Than Ngo <than@redhat.com> - 2.2-14.week32
- drop conditional

* Thu Aug 18 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-13.week32
- qtwebkit-2.2-week32 snapshot

* Wed Aug 10 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-12.week31
- BR: gstreamer-devel bits

* Tue Aug 09 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-11.week31
- qtwebkit-2.2-week31 snapshot

* Sat Jul 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-10.week28
- rebuild

* Wed Jul 20 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-9.week28
- qtwebkit-2.2-week28 snapshot

* Wed Jul 20 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-8.20110621
- rebuild (qt48)

* Wed Jun 22 2011 Dan Horák <dan[at]danny.cz> 2.2-7.20110621
- bump release for the s390 build fix

* Tue Jun 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-6.20110621
- 20110621 snapshot
- s390: respin javascriptcore_debuginfo.patch to omit -g from CXXFLAGS too

* Fri Jun 03 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-5.20110603
- 20110603 snapshot
- drop unused/deprecated phonon/gstreamer support snippets
- add minimal qt4 dep

* Tue May 24 2011 Than Ngo <than@redhat.com> - 2.2-4.20110513
- fix for qt-4.6.x
- add condition for rhel
- enable shared for qtwebkit build

* Thu May 19 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-3.20110513
- bump up Obsoletes: qt-webkit a bit, to be on the safe side

* Fri May 13 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-2.20110513
- 20110513 qtwebkit-2.2 branch snapshot
- cleanup deps
- drop -Werror

* Thu May 12 2011 Than Ngo <than@redhat.com> - 2.2-1
- 2.2-tp1
- gstreamer is now default, drop unneeded phonon patch

* Fri Apr 22 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-4
- javascriptcore -debuginfo too (#667175)

* Fri Apr 22 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-3
- Provides: qt(4)-webkit(-devel) = 2:%%version...

* Thu Apr 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-2
- -devel: Conflicts: qt-devel < 1:4.7.2-9 (qt_webkit_version.pri)
- drop old/deprecated Obsoletes/Provides: WebKit-qt
- use modified, less gigantic tarball
- patch to use phonon instead of QtMultimediaKit
- patch pluginpath for /usr/lib{,64}/mozilla/plugins-wrapped

* Tue Apr 19 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-1
- 2.1

* Mon Nov 08 2010 Than Ngo <than@redhat.com> - 2.0-2
- fix webkit to export symbol correctly

* Tue Nov 02 2010 Rex Dieter <rdieter@fedoraproject.org> 2.0-1
- 2.0 (as released with qt-4.7.0)

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.1.week32
- first try, borrowing a lot from debian/kubuntu packaging
