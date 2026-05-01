# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# The reference qt5-qtbase version: qt5 angle modifications from this qt5-qtbase version are used
%global qtrefver 5.15.2

# qt5-qtbase-5.15.2 uses ANGLE chromium/3280:
# https://chromium.googlesource.com/angle/angle/+/chromium/3280
%global commit 57ea533f79a7a30224ea641785cbd7a9485d33ed
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapshot_rev_short %(echo %snapshot_rev | cut -c1-6)

Name:           mingw-angleproject
Version:        3280
Release:        15.git%{shortcommit}%{?dist}
Summary:        Almost Native Graphics Layer Engine

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://chromium.googlesource.com/angle/angle
BuildArch:      noarch

# commit=%%commit
# shortcommit=$(echo ${commit:0:7})
# git clone https://chromium.googlesource.com/angle/angle
# (cd angle && git archive --format=tar --prefix=angle-$shortcommit/ $commit | gzip > ../angle-$shortcommit.tar.gz)
Source0:        angle-%{shortcommit}.tar.gz
# Additional source files taken from Qt5
Source1:        https://github.com/qt/qtbase/raw/v%{qtrefver}/src/3rdparty/angle/src/libGLESv2/libGLESv2_mingw32.def
Source2:        https://github.com/qt/qtbase/raw/v%{qtrefver}/src/3rdparty/angle/src/libGLESv2/libGLESv2.def
Source3:        https://github.com/qt/qtbase/raw/v%{qtrefver}/src/3rdparty/angle/src/libEGL/libEGL_mingw32.def
Source4:        https://github.com/qt/qtbase/raw/v%{qtrefver}/src/3rdparty/angle/src/libEGL/libEGL.def

BuildRequires:  gyp
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  python3

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc-c++

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc-c++

# Patches taken from Qt5
# https://github.com/qt/qtbase/tree/v%%{qtrefver}/src/angle/patches
Patch0:         0001-ANGLE-Use-pixel-sizes-in-the-XAML-swap-chain.patch
Patch1:         0001-Fix-build-for-MinGW.patch
Patch2:         0002-ANGLE-Add-support-for-querying-platform-device.patch
Patch3:         0002-ANGLE-Fix-build-for-ARM.patch
Patch4:         0003-ANGLE-Fix-Windows-Store-D3D-Trim-and-Level-9-require.patch
Patch5:         0004-ANGLE-fix-usage-of-shared-handles-for-WinRT-applicat.patch
Patch6:         0005-ANGLE-Fix-initialization-of-zero-sized-window.patch
Patch7:         0006-ANGLE-Fix-flickering-on-resize-when-D3D9-is-used.patch
Patch8:         0007-ANGLE-Fix-resizing-of-windows.patch
Patch9:         0008-ANGLE-winrt-Do-full-screen-update-if-the-the-window-.patch
Patch10:        0009-Revert-Fix-scanForWantedComponents-not-ignoring-attr.patch
Patch11:        0010-ANGLE-Disable-multisampling-to-avoid-crash-in-Qt-app.patch
Patch12:        0011-ANGLE-Fix-build-for-ARM64.patch
Patch13:        0012-ANGLE-Dynamically-load-D3D-compiler-from-a-list.patch
Patch14:        0013-ANGLE-clean-up-displays-on-dll-unload.patch
Patch15:        0014-ANGLE-Backport-fix-for-compilation-on-mingw-64bit-wi.patch
Patch16:        0015-ANGLE-Invalidate-client-window-area-when-resizing-sw.patch
Patch17:        0016-ANGLE-Fix-severe-performance-regression.patch
Patch18:        0017-ANGLE-Fix-resizing-of-windows-Take-2.patch
Patch19:        0018-ANGLE-d3d11-Do-not-register-windows-message-hooks-fo.patch


# Make sure an import library is created and the .def file is used when linking, add missing link libraries
Patch100:       angle_libs.patch

# Fix GLsizeiptr and GLintptr typedefs to match those defined in qopenglext.h
Patch101:       angle_ptrdiff.patch

# Ensure versioned python is invoked
Patch102:       angle_python3.patch

# Don't build vulkan support
Patch103:       angle_novulkan.patch

# Fix gcc11 build
Patch104:       angle_gcc11.patch

# Fix gcc13 build
Patch105:       angle_gcc13.patch


%description
ANGLE is a conformant implementation of the OpenGL ES 2.0 specification that
is hardware‐accelerated via Direct3D. ANGLE v1.0.772 was certified compliant
by passing the ES 2.0.3 conformance tests in October 2011. ANGLE also provides
an implementation of the EGL 1.4 specification.

ANGLE is used as the default WebGL backend for both Google Chrome and
Mozilla Firefox on Windows platforms. Chrome uses ANGLE for all graphics
rendering on Windows, including the accelerated Canvas2D implementation
and the Native Client sandbox environment.

Portions of the ANGLE shader compiler are used as a shader validator and
translator by WebGL implementations across multiple platforms. It is used
on Mac OS X, Linux, and in mobile variants of the browsers. Having one shader
validator helps to ensure that a consistent set of GLSL ES shaders are
accepted across browsers and platforms. The shader translator can be used
to translate shaders to other shading languages, and to optionally apply
shader modifications to work around bugs or quirks in the native graphics
drivers. The translator targets Desktop GLSL, Direct3D HLSL, and even ESSL
for native GLES2 platforms.


%{?mingw_debug_package}


# Win32
%package -n mingw32-angleproject
Summary:        Almost Native Graphics Layer Engine for Win32

%description -n mingw32-angleproject
ANGLE is a conformant implementation of the OpenGL ES 2.0 specification that
is hardware‐accelerated via Direct3D. ANGLE v1.0.772 was certified compliant
by passing the ES 2.0.3 conformance tests in October 2011. ANGLE also provides
an implementation of the EGL 1.4 specification.

ANGLE is used as the default WebGL backend for both Google Chrome and
Mozilla Firefox on Windows platforms. Chrome uses ANGLE for all graphics
rendering on Windows, including the accelerated Canvas2D implementation
and the Native Client sandbox environment.

Portions of the ANGLE shader compiler are used as a shader validator and
translator by WebGL implementations across multiple platforms. It is used
on Mac OS X, Linux, and in mobile variants of the browsers. Having one shader
validator helps to ensure that a consistent set of GLSL ES shaders are
accepted across browsers and platforms. The shader translator can be used
to translate shaders to other shading languages, and to optionally apply
shader modifications to work around bugs or quirks in the native graphics
drivers. The translator targets Desktop GLSL, Direct3D HLSL, and even ESSL
for native GLES2 platforms.


%package -n mingw32-angleproject-static
Summary:       Static version of the mingw32-angleproject library
Requires:      mingw32-angleproject = %{version}-%{release}

%description -n mingw32-angleproject-static
Static version of the mingw32-angleproject library.


# Win64
%package -n mingw64-angleproject
Summary:        Almost Native Graphics Layer Engine for Win64

%description -n mingw64-angleproject
ANGLE is a conformant implementation of the OpenGL ES 2.0 specification that
is hardware‐accelerated via Direct3D. ANGLE v1.0.772 was certified compliant
by passing the ES 2.0.3 conformance tests in October 2011. ANGLE also provides
an implementation of the EGL 1.4 specification.

ANGLE is used as the default WebGL backend for both Google Chrome and
Mozilla Firefox on Windows platforms. Chrome uses ANGLE for all graphics
rendering on Windows, including the accelerated Canvas2D implementation
and the Native Client sandbox environment.

Portions of the ANGLE shader compiler are used as a shader validator and
translator by WebGL implementations across multiple platforms. It is used
on Mac OS X, Linux, and in mobile variants of the browsers. Having one shader
validator helps to ensure that a consistent set of GLSL ES shaders are
accepted across browsers and platforms. The shader translator can be used
to translate shaders to other shading languages, and to optionally apply
shader modifications to work around bugs or quirks in the native graphics
drivers. The translator targets Desktop GLSL, Direct3D HLSL, and even ESSL
for native GLES2 platforms.


%package -n mingw64-angleproject-static
Summary:       Static version of the mingw32-angleproject library
Requires:      mingw64-angleproject = %{version}-%{release}

%description -n mingw64-angleproject-static
Static version of the mingw64-angleproject library.


%prep
%setup -q -n angle-%{shortcommit}
# Install additional .def files
cp -a %{SOURCE1} src/libGLESv2/libGLESv2_mingw32.def
cp -a %{SOURCE2} src/libGLESv2/libGLESv2_mingw64.def
cp -a %{SOURCE3} src/libEGL/libEGL_mingw32.def
cp -a %{SOURCE4} src/libEGL/libEGL_mingw64.def

%patch 0 -p4
%patch 1 -p4
%patch 2 -p4
%patch 3 -p4
%patch 4 -p4
%patch 5 -p4
%patch 6 -p4
%patch 7 -p4
%patch 8 -p4
%patch 9 -p4
%patch 10 -p4
%patch 11 -p4
%patch 12 -p4
%patch 13 -p4
%patch 14 -p4
%patch 15 -p4
%patch 16 -p4
%patch 17 -p4
%patch 18 -p4
%patch 19 -p4

%patch 100 -p1
%patch 101 -p1
%patch 102 -p1
%patch 103 -p1
%patch 104 -p1
%patch 105 -p1

# Executing .bat scripts on Linux is a no-go so make this a no-op
echo "" > src/copy_compiler_dll.bat
chmod +x src/copy_compiler_dll.bat


%build
# This project uses the gyp build system and various hacks are required to get this project built.
# Therefore the regular Fedora MinGW RPM macros can't be used for this package.

# The gyp build system always uses the environment variable RPM_OPT_FLAGS when it's set
# For MinGW we don't want this, so unset this environment variable
unset RPM_OPT_FLAGS

COMMON_CXXFLAGS="-msse2 -DUNICODE -D_UNICODE -D_USE_MATH_DEFINES \
    -I../include -I../sysinclude -I../src -I../src/common/third_party/base"

for target in win32 win64 ; do
    mkdir build_$target
    pushd build_$target
        if [ "$target" = "win32" ] ; then
            export CXX=%{mingw32_cxx}
            export AR=%{mingw32_ar}
            export CXXFLAGS="%{mingw32_cflags} $COMMON_CXXFLAGS"
            export LDFLAGS="%{mingw32_ldflags}"
        else
            export CXX=%{mingw64_cxx}
            export AR=%{mingw64_ar}
            export CXXFLAGS="%{mingw64_cflags} $COMMON_CXXFLAGS"
            export LDFLAGS="%{mingw64_ldflags}"
        fi

        V=1 gyp --build=Release -D use_ozone=0 -D use_x11=0 -D OS=win -D TARGET=$target -D MSVS_VERSION='' --depth . -I ../gyp/common.gypi ../src/angle.gyp
    popd
done


%install
# The gyp build system doesn't know how to install files
# and gives libraries invalid filenames.. *sigh*
install -Dpm 0755 build_win32/out/Release/src/libGLESv2.so %{buildroot}%{mingw32_bindir}/libGLESv2.dll
install -Dpm 0755 build_win64/out/Release/src/libGLESv2.so %{buildroot}%{mingw64_bindir}/libGLESv2.dll

install -Dpm 0755 build_win32/out/Release/src/libEGL.so %{buildroot}%{mingw32_bindir}/libEGL.dll
install -Dpm 0755 build_win64/out/Release/src/libEGL.so %{buildroot}%{mingw64_bindir}/libEGL.dll

install -Dpm 0644 build_win32/libGLESv2.dll.a %{buildroot}%{mingw32_libdir}/libGLESv2.dll.a
install -Dpm 0644 build_win64/libGLESv2.dll.a %{buildroot}%{mingw64_libdir}/libGLESv2.dll.a

install -Dpm 0644 build_win32/libEGL.dll.a %{buildroot}%{mingw32_libdir}/libEGL.dll.a
install -Dpm 0644 build_win64/libEGL.dll.a %{buildroot}%{mingw64_libdir}/libEGL.dll.a

install -Dpm 0644 build_win32/out/Release/src/libGLESv2_static.a %{buildroot}%{mingw32_libdir}/libGLESv2.a
install -Dpm 0644 build_win64/out/Release/src/libGLESv2_static.a %{buildroot}%{mingw64_libdir}/libGLESv2.a

install -Dpm 0644 build_win32/out/Release/src/libEGL_static.a %{buildroot}%{mingw32_libdir}/libEGL.a
install -Dpm 0644 build_win64/out/Release/src/libEGL_static.a %{buildroot}%{mingw64_libdir}/libEGL.a


mkdir -p %{buildroot}%{mingw32_includedir}
cp -a include/* %{buildroot}%{mingw32_includedir}/
rm -rf %{buildroot}%{mingw32_includedir}/{platform,export.h}

mkdir -p %{buildroot}%{mingw64_includedir}
cp -a include/* %{buildroot}%{mingw64_includedir}/
rm -rf %{buildroot}%{mingw64_includedir}/{platform,export.h}

# Drop khrplatform.h, it is shipped by mingw-headers
rm -f %{buildroot}%{mingw32_includedir}/KHR/khrplatform.h
rmdir %{buildroot}%{mingw32_includedir}/KHR/
rm -f %{buildroot}%{mingw64_includedir}/KHR/khrplatform.h
rmdir %{buildroot}%{mingw64_includedir}/KHR/


%files -n mingw32-angleproject
%license LICENSE
%{mingw32_bindir}/libEGL.dll
%{mingw32_bindir}/libGLESv2.dll
%{mingw32_includedir}/EGL
%{mingw32_includedir}/GLES2
%{mingw32_includedir}/GLES3
%{mingw32_includedir}/GLSLANG
%{mingw32_includedir}/angle_gl.h
%{mingw32_includedir}/angle_windowsstore.h
%{mingw32_libdir}/libEGL.dll.a
%{mingw32_libdir}/libGLESv2.dll.a

%files -n mingw32-angleproject-static
%{mingw32_libdir}/libEGL.a
%{mingw32_libdir}/libGLESv2.a

%files -n mingw64-angleproject
%license LICENSE
%{mingw64_bindir}/libEGL.dll
%{mingw64_bindir}/libGLESv2.dll
%{mingw64_includedir}/EGL
%{mingw64_includedir}/GLES2
%{mingw64_includedir}/GLES3
%{mingw64_includedir}/GLSLANG
%{mingw64_includedir}/angle_gl.h
%{mingw64_includedir}/angle_windowsstore.h
%{mingw64_libdir}/libEGL.dll.a
%{mingw64_libdir}/libGLESv2.dll.a

%files -n mingw64-angleproject-static
%{mingw64_libdir}/libEGL.a
%{mingw64_libdir}/libGLESv2.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3280-15.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 08 2025 Sandro Mani <manisandro@gmail.com> - 3280-14.git57ea533
- Rebuild against correct crt

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3280-13.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 3280-12.git57ea533
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3280-11.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3280-10.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3280-9.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3280-8.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3280-7.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3280-6.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3280-5.git57ea533
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3280-4.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3280-3.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3280-2.git57ea533
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Sandro Mani <manisandro@gmail.com> - 0.0.29-git57ea533
- Update to ANGLE 3280
- Switch to python3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.28.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 19 2020 Sandro Mani <manisandro@gmail.com> - 0-0.27.git8613f49
- Drop khrplatform.h, it is shipped by mingw-headers

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.26.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 0-0.25.git8613f49
- Rebuild (Changes/Mingw32GccDwarf2)
- Add missing BR: python27

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.24.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.23.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.22.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.21.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.20.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Sandro Mani <manisandro@gmail.com> - 0-0.19.git8613f49
- Fix incorrect def files for x64

* Thu Jun 29 2017 Sandro Mani <manisandro@gmail.com> - 0-0.18.git8613f49
- Fix angle_ptrdiff.patch to include stddef.h instead of cstddef

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.17.git8613f49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Sandro Mani <manisandro@gmail.com> - 0-0.16.git8613f49
- Update to git 8613f49

* Sat May 07 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.15.git.30d6c2.20141113
- Fix FTBFS against GCC 6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14.git.30d6c2.20141113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.13.git.30d6c2.20141113
- Use GCC constructors instead of DllMain to avoid conflicts in the static library (RHBZ #1257630)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.12.git.30d6c2.20141113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.11.git.30d6c2.20141113
- Update to 20141113 snapshot (git revision 30d6c2)
- Include all patches which were used by the Qt5 fork
- Reverted some recent commits as they break mingw-qt5-qtwebkit 5.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.10.svn2215.20130517
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb  4 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.9.svn2215.20130517
- Automatically LoadLibrary("d3dcompiler_43.dll") when no other D3D compiler is
  already loaded yet. Fixes RHBZ #1057983
- Make sure the libraries are built with debugging symbols
- Rebuild against latest mingw-w64 (fixes Windows XP compatibility, RHBZ #1054481)

* Fri Jan 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.8.svn2215.20130517
- Rebuilt against latest mingw-w64 to fix Windows XP compatibility (RHBZ #1054481)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.7.svn2215.20130517
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 18 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.6.svn2215.20130517
- Export various symbols from the hlsl translator static library in the
  libGLESv2.dll shared library as they are needed by mingw-qt5-qtwebkit.
  The symbols in question are marked as NONAME (hidden)

* Fri May 17 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.5.svn2215.20130517
- Update to 20130517 snapshot (r2215)

* Thu Apr  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.4.svn1561.20121214
- Added another workaround due to the fact that the gyp
  build system doesn't properly support cross-compilation
  Fixes FTBFS against latest gyp

* Fri Jan 25 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.3.svn1561.20121214
- Added license
- Resolved various rpmlint warnings
- Prefix the release tag with '0.'

* Mon Dec 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.2.svn1561.20121214
- Added -static subpackages

* Fri Dec 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.1.svn1561.20121214
- Initial release

