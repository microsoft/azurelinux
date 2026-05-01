# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The additional linker flags break binary qt5-qtwebkits packages.
# https://bugzilla.redhat.com/show_bug.cgi?id=2046931
%undefine _package_note_flags

%global qt_module qtwebkit

%global _hardened_build 1

%global prerel alpha4
%global prerel_tag -%{prerel}

## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global add_to_license_files() \
        mkdir -p _license_files ; \
        cp -p %1 _license_files/$(echo '%1' | sed -e 's!/!.!g')

Name:           qt5-%{qt_module}
Version:        5.212.0
Release:        0.95%{?prerel}%{?dist}
Summary:        Qt5 - QtWebKit components

License:        LGPL-2.0-only AND BSD-3-Clause
URL:            https://github.com/qtwebkit/qtwebkit
Source0:        https://github.com/qtwebkit/qtwebkit/releases/download/%{qt_module}-%{version}%{?prerel_tag}/%{qt_module}-%{version}%{?prerel_tag}.tar.xz

# Patch for new CMake policy CMP0071 to explicitly use old behaviour.
Patch2:         qtwebkit-5.212.0_cmake_cmp0071.patch
Patch3:         qtwebkit-5.212.0-json.patch
Patch4:         qtwebkit-bison37.patch
Patch5:         qt5-qtwebkit-glib-2.68.patch
Patch6:         qtwebkit-icu68.patch
# From https://github.com/WebKit/WebKit/commit/c7d19a492d97f9282a546831beb918e03315f6ef
# Ruby 3.2 removes Object#=~ completely
Patch7:         webkit-offlineasm-warnings-ruby27.patch
Patch8:         qtwebkit-cstdint.patch
Patch9:         qtwebkit-fix-build-gcc14.patch
Patch10:        qtwebkit-icu76.patch

# Enable RISC-V (riscv64)
Patch11:        https://github.com/qtwebkit/qtwebkit/commit/d9824ec806b6c6171862a7ba758fc28e6a20aada.patch

BuildRequires: make
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  pkgconfig(fontconfig)
%if 0%{?rhel} != 8
BuildRequires:  pkgconfig(libwoff2dec)
%endif
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  gperf
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  hyphen-devel
BuildRequires:  pkgconfig(icu-i18n) pkgconfig(icu-uc)
BuildRequires:  libjpeg-devel
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gstreamer-gl-1.0)
BuildRequires:  pkgconfig(gstreamer-mpegts-1.0)
BuildRequires:  perl-generators
BuildRequires:  perl(File::Copy)
BuildRequires:  python3
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
%if ! 0%{?bootstrap}
BuildRequires:  qt5-qtlocation-devel
BuildRequires:  qt5-qtsensors-devel
BuildRequires:  qt5-qtwebchannel-devel
%endif
BuildRequires:  pkgconfig(ruby)
BuildRequires:  rubygems
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
# workaround bad embedded png files, https://bugzilla.redhat.com/1639422
BuildRequires:  findutils
BuildRequires:  pngcrush

BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  qt5-qtdeclarative-private-devel
%{?_qt5:Requires: qt5-qtdeclarative%{?_isa} = %{_qt5_version}}


# filter qml provides
%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

# We're supposed to specify versions here, but these crap Google libs don't do
# normal releases. Accordingly, they're not suitable to be system libs.
Provides:       bundled(angle)
Provides:       bundled(brotli)
Provides:       bundled(woff2)


%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
Requires:       qt5-qtdeclarative-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
BuildRequires: qt5-qdoc
BuildRequires: qt5-qhelpgenerator
BuildArch: noarch

%description doc
%{summary}.
%endif


%prep
%autosetup -p1 -n %{qt_module}-%{version}%{?prerel_tag}

# find/fix pngs with "libpng warning: iCCP: known incorrect sRGB profile"
find -name \*.png | xargs -n1 pngcrush -ow -fix

# ppc64le failed once with
# make[2]: *** No rule to make target 'Source/WebCore/Resources/textAreaResizeCorner.png', needed by 'Source/WebKit/qrc_WebCore.cpp'.  Stop.
test -f Source/WebCore/Resources/textAreaResizeCorner.png


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}
%define _package_note_flags %{nil}

# The following changes of optflags ietc. are adapted from webkitgtk4 package, which
# is mostly similar to this one...
#
# Increase the DIE limit so our debuginfo packages can be size-optimized.
# This previously decreased the size for x86_64 from ~5G to ~1.1G, but as of
# 2022 it's more like 850 MB -> 675 MB. This requires lots of RAM on the
# builders, so only do this for x86_64 and aarch64 to avoid overwhelming
# builders with less RAM.
# https://bugzilla.redhat.com/show_bug.cgi?id=1456261
%global _dwz_max_die_limit_x86_64 250000000
%global _dwz_max_die_limit_aarch64 250000000

# Require 32 GB of RAM per vCPU for debuginfo processing. 16 GB is not enough.
%global _find_debuginfo_opts %limit_build -m 32768

# Decrease debuginfo even on ix86 because of:
# https://bugs.webkit.org/show_bug.cgi?id=140176
%ifarch s390 s390x %{arm} %{ix86} ppc %{power64} %{mips} riscv64
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

%ifarch ppc
# Use linker flag -relax to get WebKit build under ppc(32) with JIT disabled
%global optflags %{optflags} -Wl,-relax
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags} -fpermissive" ; export CXXFLAGS ;
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;}

%ifarch riscv64
export LDFLAGS="${LDFLAGS} -latomic"
%endif

# We cannot use default cmake macro here as it overwrites some settings queried
# by qtwebkit cmake from qmake
%cmake \
       -DPORT=Qt \
       -DCMAKE_BUILD_TYPE=Release \
       -DENABLE_TOOLS=OFF \
       -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
       -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
       -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
       -DLIBEXEC_INSTALL_DIR=%{_qt5_libexecdir} \
       -DECM_MKSPECS_INSTALL_DIR=%{_qt5_archdatadir}/mkspecs/modules \
       -DQML_INSTALL_DIR=%{_qt5_archdatadir}/qml \
       -DKDE_INSTALL_INCLUDEDIR=%{_qt5_headerdir} \
%ifarch s390 s390x ppc %{power64} riscv64
       -DENABLE_JIT=OFF \
%endif
%ifarch s390 s390x ppc %{power64}
       -DUSE_SYSTEM_MALLOC=ON \
%endif
       %{?docs:-DGENERATE_DOCUMENTATION=ON} \
       -DPYTHON_EXECUTABLE:PATH="%{__python3}"

%cmake_build

%if 0%{?docs}
%make_build docs
%endif


%install
%cmake_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# fix pkgconfig files
#sed -i '/Name/a Description: Qt5 WebKit module' %{buildroot}%{_libdir}/pkgconfig/Qt5WebKit.pc
#sed -i "s,Cflags: -I%{_qt5_libdir}/qt5/../../include/qt5/Qt5WebKit,Cflags: -I%{_qt5_headerdir}/QtWebKit,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKit.pc
# strictly speaking, this isn't *wrong*, but can made more readable, so let's do that
sed -i "s,Libs: -L%{_qt5_libdir}/qt5/../ -lQt5WebKit,Libs: -L%{_qt5_libdir} -lQt5WebKit ,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKit.pc

#sed -i '/Name/a Description: Qt5 WebKitWidgets module' %{buildroot}%{_libdir}/pkgconfig/Qt5WebKitWidgets.pc
#sed -i "s,Cflags: -I%{_qt5_libdir}/qt5/../../include/qt5/Qt5WebKitWidgets,Cflags: -I%{_qt5_headerdir}/QtWebKitWidgets,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKitWidgets.pc
sed -i "s,Libs: -L%{_qt5_libdir}/qt5/../ -lQt5WebKitWidgets,Libs: -L%{_qt5_libdir} -lQt5WebKitWidgets ,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKitWidgets.pc

# Finally, copy over and rename various files for %%license inclusion
%add_to_license_files Source/JavaScriptCore/COPYING.LIB
%add_to_license_files Source/JavaScriptCore/icu/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/compiler/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/murmurhash/LICENSE
%add_to_license_files Source/WebCore/icu/LICENSE
%add_to_license_files Source/WebCore/LICENSE-APPLE
%add_to_license_files Source/WebCore/LICENSE-LGPL-2
%add_to_license_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CodeMirror/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/Esprima/LICENSE
%add_to_license_files Source/WTF/icu/LICENSE
%add_to_license_files Source/WTF/wtf/dtoa/COPYING
%add_to_license_files Source/WTF/wtf/dtoa/LICENSE


%check
# verify Qt5WebKit cflags non-use of -I/.../Qt5WebKit
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test -z "$(pkg-config --cflags Qt5WebKit | grep Qt5WebKit)"


%ldconfig_scriptlets

%files
%license LICENSE.LGPLv21 _license_files/*
%{_qt5_libdir}/libQt5WebKit.so.5*
%{_qt5_libdir}/libQt5WebKitWidgets.so.5*
%{_qt5_libexecdir}/QtWebNetworkProcess
%{_qt5_libexecdir}/QtWebPluginProcess
%{_qt5_libexecdir}/QtWebProcess
%{_qt5_libexecdir}/QtWebStorageProcess
%{_qt5_archdatadir}/qml/QtWebKit/

%files devel
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri


%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtwebkit.qch
%{_qt5_docdir}/qtwebkit/
%endif


%changelog
* Tue Nov 04 2025 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.95alpha4
- Rebuild (qt5)

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 5.212.0-0.94alpha4
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.93alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 26 2025 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.92alpha4
- Rebuild (qt5)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.91alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.90alpha4
- Rebuild (qt5)

* Wed Sep 04 2024 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.89alpha4
- Rebuild (qt5)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.88alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.87alpha4
- Rebuild (qt5)

* Sat May 25 2024 Fabio Valentini <decathorpe@gmail.com> - 5.212.0-0.86alpha4
- Rebuild for gstreamer-plugins-bad 1.24.

* Thu Mar 14 2024 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.85alpha4
- Rebuild (qt5)

* Thu Feb 29 2024 David Abdurachmanov <david.abdurachmanov@gmail.com> - 5.212.0-0.84alpha4
- add support for RISC-V (riscv64)

* Tue Feb 06 2024 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.83alpha4
- Fix build with GCC 14

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.82alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.81alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.80alpha4
- Rebuild (qt5)

* Sun Oct 08 2023 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.79alpha4
- Rebuild (qt5)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.78alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 5.212.0-0.77alpha4
- Rebuilt for ICU 73.2

* Wed Jun 14 2023 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.76alpha4
- Rebuild (qt5)

* Wed Apr 12 2023 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.75alpha4
- Rebuild (qt5)

* Mon Feb 20 2023 Than Ngo <than@redhat.com> - 5.212.0-0.74alpha4
- migrated to SPDX license
- fixed FTBFS

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.73alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.72alpha4
- Rebuild (qt5)

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.71alpha4
- Rebuild for ICU 72

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.70alpha4
- Rebuild (qt5)

* Tue Oct 18 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.212.0-0.69.alpha4
- Patch for offlineasm to support ruby 3.2 wrt Object#=~ removal

* Wed Sep 21 2022 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.68.alpha4
- Rebuild (qt5)

* Tue Aug 02 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.212.0-0.67.alpha4
- Rebuilt for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.66.alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.65.alpha4
- Rebuild (qt5)

* Thu May 19 2022 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.64.alpha4
- Rebuild (qt5)

* Tue Mar 08 2022 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.63.alpha4
- Rebuild (qt5)

* Wed Feb 09 2022 Than Ngo <than@redhat.com> - 5.212.0-0.62.alpha4
- disable _package_note_flags because it breaks qt5-qtwebkit


* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.61.alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.60.alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 31 2021 Than Ngo <than@redhat.com> - 5.212.0-0.59.alpha4
- fix FTBFS against glib >= 2.68
- fix macro definitions TRUE,FALSE

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.58.alpha4
- Rebuild for ICU 69

* Mon May 10 2021 Jonathan Wakely <jwakely@redhat.com> - 5.212.0-0.57.alpha4
- Rebuilt for removed libstdc++ symbols (#1937698)

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 5.212.0-0.56.alpha4
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.55.alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 07:56:08 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.54.alpha4
- Rebuild for qtbase with -no-reduce-relocations option

* Fri Nov 20 13:29:15 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.53.alpha4
- Rebuild (qt5)

* Fri Sep 11 2020 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.52.alpha4
- rebuild (qt5)

* Thu Aug 27 2020 Than Ngo <than@redhat.com> - 5.212.0-0.51.alpha4
- Fixed #1863719, FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.50.alpha4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.49.alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 5.212.0-0.48.alpha4
- Disable LTO

* Wed Jun 03 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.47.alpha4
- rebuild (python39)

* Sun May 17 2020 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.46.alpha4
- Rebuild for ICU 67

* Sat May 16 2020 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.45.alpha4
- Rebuild for ICU 67

* Fri Apr 24 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.44.alpha4
- 5.212.0-alpha4
- use python3 (#1807535)

* Sun Apr 05 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.43.alpha3
- rebuild (qt5)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.42.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.41.alpha3
- rebuild (qt5)

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.40.alpha3
- rebuild (qt5)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.39.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.38.alpha3
- rebuild

* Tue Jul 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.37.alpha3
- 5.212.0 alpha 3

* Tue Jun 11 2019 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.36.alpha2
- rebuild (qt5)

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.35.alpha2
- rebuild (qt5)

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.34.alpha2
- rebuild (qt5)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.33.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.32.alpha2
- Rebuild for ICU 63

* Tue Dec 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.31.alpha
- rebuild (qt5)

* Sat Nov 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.30.alpha
- QtWebkit bundles malformed PNG files (#1639422)

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.29.alpha2
- rebuild (qt5)

* Tue Aug 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.28.alpha2
- revert to real package names for core qt5 deps

* Wed Jul 25 2018 Christian Dersch <lupinix@fedoraproject.org> - 5.212.0-0.27.alpha2
- Disable annobin for now, workaround for RHBZ #1608549

* Tue Jul 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.26.alpha2
- backport some pkgconfig-related upstream fixes
- use %%ldconfig_scriptlets

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.25.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.24.alpha2
- Rebuild for ICU 62

* Wed Jun 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.23.alpha2
- rebuild (qt5)

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.22.alpha2
- rebuild (qt5)
- workaround gcc8 FTBFS with -fpermissive (#1582954)

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.21.alpha2
- Rebuild for ICU 61.1

* Fri Feb 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.20.alpha2
- Bad ES6 Proxy object for QT platform breaks scudcloud (#1513091)

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.19.alpha2
- rebuild (qt5)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.18.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Jan Grulich <jgrulich@redhat.com> - 5.212.0-0.17.alpha2
- rebuild (qt5)

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 5.212.0-0.16.alpha2
- Rebuild for ICU 60.1

* Sun Nov 26 2017 Björn Esser <besser82@fedoraproject.org> - 5.212.0-0.15.alpha2
- Add patch2 to fix CMake warnings
- Add patch3 to fix build (missing src file caused by typo)
- Add missing BuildRequires

* Sun Nov 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.14.alpha2
- rebuild (qt5)

* Thu Oct 26 2017 Vít Ondruch <vondruch@redhat.com> - 5.212.0-0.13.alpha2
- Drop explicit dependency on rubypick.

* Tue Oct 24 2017 Christian Dersch <lupinix@mailbox.org> - 5.212.0-0.12.alpha2
- Added patch to fix null pointer dereference (#1470778)

* Mon Oct 23 2017 Christian Dersch <lupinix@mailbox.org> - 5.212.0-0.11.alpha2
- Added patch to fix issue with pagewidth (#1502332)

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.10.alpha2
- rebuild (qt5)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.9.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.212.0-0.8.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.7.alpha2
- rebuild against newer gcc/ppc64le (#1470692)

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.212.0-0.6.alpha2
- rebuild (qt-5.9.1)

* Mon Jul 10 2017 Christian Dersch <lupinix@mailbox.org> - 5.212.0-0.5.alpha2
- replaced ugly pkgconfig provides workaround with proper pkgconfig fixes
- general spec fixes

* Thu Jun 22 2017 Christian Dersch <lupinix@mailbox.org> - 5.212.0-0.4.alpha2
- BR: pkg-config

* Wed Jun 21 2017 Christian Dersch <lupinix@mailbox.org> - 5.212.0-0.3.alpha2
- ensure that we do a release build

* Wed Jun 21 2017 Christian Dersch <lupinix@mailbox.org> - 5.212.0-0.2.alpha2
- few spec adjustments

* Sun Jun 18 2017 Christian Dersch <lupinix@mailbox.org> - 5.212.0-0.1.alpha2
- switch to maintained annulen branch of qtwebkit

* Sat Jun 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-1
- 5.9.0 (final)

* Sun May 28 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Release candidate community

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.0-0.beta.3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Wed May 10 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Community beta3

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-1
- 5.8.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 5.7.1-4
- Rebuild (libwebp)

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-3
- filter qml provides, BR: qtdeclarative python expicitly

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- drop BR: cmake (handled by qt5-rpm-macros now)
- 5.7.1 dec5 snapshot

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Compiled with gcc

* Wed Jun 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release ( non git, official package )

* Tue Jun 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-2.b889f46git
- rebuild (glibc)

* Thu Jun 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-1.b889f46git
- 5.6.1 branch snapshot, plus a couple post-5.6.1 5.6 branch fixes

* Thu Jun 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-9
- rebuild (qtbase)

* Wed May 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-8
- use pristine upstream (community) sources

* Wed Apr 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-7
- rebuild (icu)

* Sun Apr 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-6
- BR: qt5-qtbase-private-devel qt5-qtdeclarative-private-devel

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 5.6.0-5
- rebuild for ICU 57.1

* Wed Apr  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5.6.0-4
- Update ruby deps to ensure all bits are present

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Mon Feb 29 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.12.rc
- fix sources

* Wed Feb 24 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.11.rc
- Fix the trap caused by rpmdev-bumpspec

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.10.rc
- Update to final RC

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.9
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.7
- BR: cmake, use %%license

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 5.6.0-0.6
- Rebuilt for libwebp soname bump

* Sun Dec 13 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.5
- Update beta code

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-0.4
- restore bootstrap macro, omit more optional BR's/features in bootstrap mode
- drop (unused) system_angle support
- include -qdoc builddep only in -doc subpkg

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.3
- Official beta release

* Sun Dec 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.2
- (re)add bootstrap macro support

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 5.5.1-4
- rebuild for ICU 56.1

* Fri Oct 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-3
- drop (unused) system_angle support/patches

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-4
- -docs: BuildRequires: qt5-qhelpgenerator, standardize bootstrapping

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- tighten deps (#1233829)

* Mon Jul 13 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.0-2
- add 5.5.0-1 changelog
- BR: qt5-qtwebchannel-devel
- (re)enable docs

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-1
- New final upstream release Qt 5.5.0

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-6
- Rebuilt for GCC 5 C++11 ABI change

* Fri Apr 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-5
- -doc: drop dep on main pkg, not strictly required

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-4
- QtWebKit logs visited URLs to WebpageIcons.db in private browsing mode (#1204795,#1204798)

* Wed Mar 18 2015 Than Ngo <than@redhat.com> - 5.4.1-3
- fix build failure with new gcc5

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Tue Feb 17 2015 Than Ngo <than@redhat.com> 5.4.0-4
- fix GMutexLocker build problem

* Tue Feb 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- rebuild (gcc5)

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 5.4.0-2
- rebuild for ICU 54.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.5.rc
- 5.4.0-rc

* Tue Nov 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.4.beta
- use gst1 only fc21+ (and el8+) only

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.beta
- fix hardening, use new %%qmake_qt5 macro

* Sat Nov 01 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- enable hardened build, out-of-src tree build

* Sat Oct 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 5.3.1-3
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-4
- use standard (same as qtbase) .prl sanitation

* Fri May 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- no rpath, drop chrpath hacks
- BR: qt5-qtlocation qt5-qtsensors

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- rebuild (libicu)

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Sun Feb 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- Add AArch64 support to qtwebkit (#1056160)

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- rebuild (libwebp)

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Thu Nov 28 2013 Dan Horák <dan[at]danny.cz> 5.2.0-0.6.beta1
- disable JIT on secondary arches, fix build with JIT disabled (#1034940)

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg
- use gstreamer1 (where available)

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Tue Aug 20 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-8
- qt5-qtjsbackend only supports ix86, x86_64 and arm

* Fri Aug 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-7
- use bundled angleproject (until system version passes review)

* Fri Jun 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-6
- %%doc ChangeLog VERSION
- %%doc Source/WebCore/LICENSE*
- squash more rpaths

* Fri May 17 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-5
- unbundle angleproject code

* Wed May 15 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- BR: perl(version) perl(Digest::MD5) pkgconfig(xslt)
- deal with bundled code
- add (commented) upstream link http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
  to clarify licensing

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- -devel: Requires: qt5-qtdeclarative-devel

* Fri Apr 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- BR: qt5-qtdeclarative-devel

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- .prl love
- BR: pkgconfig(gl)

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

