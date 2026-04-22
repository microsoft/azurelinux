# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1

# Disable libwebp-java subpackage for RHEL builds
%bcond enable_java %[!0%{?rhel}]

%if %{with enable_java}
%ifarch %{java_arches}
%bcond_without java
%else
%bcond_with java
%endif
%else
%bcond_with java
%endif

%if 0%{?rhel}
%bcond_with mingw
%else
%bcond_without mingw
%endif

Name:          libwebp
Version:       1.6.0
Release: 3%{?dist}
URL:           http://webmproject.org/
Summary:       Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:       Apache-2.0 AND LicenseRef-scancode-google-patent-license-webm AND BSD-3-Clause AND FSFULLRWD
Source0:       http://downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz
Source1:       libwebp_jni_example.java
# Fix build with freeglut
Patch0:        libwebp-freeglut.patch
# Add version suffix to mingw libraries
Patch1:        libwebp-mingw-libsuffix.patch
# Fix cmake module install location
Patch2:        libwebp-cmakedir.patch
# Kill rpath
Patch3:        libwebp-rpath.patch

BuildRequires: cmake
BuildRequires: freeglut-devel
BuildRequires: gcc
BuildRequires: giflib-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
%if %{with java}
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: swig
%endif

%if %{with mingw}
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-giflib
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-libjpeg

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-giflib
BuildRequires:  mingw64-libpng
BuildRequires:  mingw64-libjpeg
%endif


%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package tools
Summary:       The WebP command line tools
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package devel
Summary:       Development files for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%if %{with java}
%package java
Summary:       Java bindings for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      java-headless
Requires:      jpackage-utils

%description java
Java bindings for libwebp.
%endif


%if %{with mingw}
%package -n mingw32-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw32-%{name}
MinGW Windows %{name} library.


%package -n mingw64-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw64-%{name}
MinGW Windows %{name} library.


%{?mingw_debug_package}
%endif


%prep
%autosetup -p1


%build
# Native build
%cmake
%cmake_build

%if %{with mingw}
# MinGW build
%mingw_cmake -DWEBP_BUILD_VWEBP=OFF
%mingw_make_build
%endif

%if %{with java}
# SWIG generated Java bindings
cp %{SOURCE1} .
cd swig
rm -rf libwebp.jar libwebp_java_wrap.c
mkdir -p java/com/google/webp
swig -ignoremissing -I../src -java \
    -package com.google.webp  \
    -outdir java/com/google/webp \
    -o libwebp_java_wrap.c libwebp.swig

gcc %{__global_ldflags} %{optflags} -shared \
    -I/usr/lib/jvm/java/include \
    -I/usr/lib/jvm/java/include/linux \
    -I../src \
    -L../%{_vpath_builddir} -lwebp libwebp_java_wrap.c \
    -o libwebp_jni.so

cd java
javac com/google/webp/libwebp.java
jar cvf ../libwebp.jar com/google/webp/*.class
%endif


%install
# Native build
%cmake_install

%if %{with mingw}
# MinGW build
%mingw_make_install
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}
%endif

find "%{buildroot}/%{_libdir}" -type f -name "*.la" -delete

%if %{with java}
# SWIG generated Java bindings
mkdir -p %{buildroot}/%{_libdir}/%{name}-java
cp swig/*.jar swig/*.so %{buildroot}/%{_libdir}/%{name}-java/
%endif


%{?mingw_debug_install_post}


%check
%ctest


%files
%doc README.md PATENTS NEWS AUTHORS
%license COPYING
%{_libdir}/%{name}.so.7*
%{_libdir}/%{name}decoder.so.3*
%{_libdir}/%{name}demux.so.2*
%{_libdir}/%{name}mux.so.3*
%{_libdir}/libsharpyuv.so.0*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/%{name}decoder.so
%{_libdir}/%{name}demux.so
%{_libdir}/%{name}mux.so
%{_libdir}/libsharpyuv.so
%{_includedir}/webp/
%{_libdir}/pkgconfig/libwebp.pc
%{_libdir}/pkgconfig/libwebpdecoder.pc
%{_libdir}/pkgconfig/libwebpdemux.pc
%{_libdir}/pkgconfig/libwebpmux.pc
%{_libdir}/pkgconfig/libsharpyuv.pc
%{_libdir}/cmake/WebP/

%files tools
%{_bindir}/cwebp
%{_bindir}/dwebp
%{_bindir}/gif2webp
%{_bindir}/img2webp
%{_bindir}/webpinfo
%{_bindir}/webpmux
%{_bindir}/vwebp
%{_mandir}/man*/*

%if %{with java}
%files java
%doc libwebp_jni_example.java
%{_libdir}/%{name}-java/
%endif

%if %{with mingw}
%files -n mingw32-libwebp
%license PATENTS COPYING
%{mingw32_bindir}/cwebp.exe
%{mingw32_bindir}/dwebp.exe
%{mingw32_bindir}/gif2webp.exe
%{mingw32_bindir}/img2webp.exe
%{mingw32_bindir}/webpinfo.exe
%{mingw32_bindir}/webpmux.exe
%{mingw32_bindir}/libwebp-7.dll
%{mingw32_bindir}/libwebpdecoder-3.dll
%{mingw32_bindir}/libwebpdemux-2.dll
%{mingw32_bindir}/libwebpmux-3.dll
%{mingw32_bindir}/libsharpyuv-0.dll
%{mingw32_includedir}/webp/
%{mingw32_libdir}/pkgconfig/libwebp.pc
%{mingw32_libdir}/pkgconfig/libwebpdecoder.pc
%{mingw32_libdir}/pkgconfig/libwebpdemux.pc
%{mingw32_libdir}/pkgconfig/libwebpmux.pc
%{mingw32_libdir}/pkgconfig/libsharpyuv.pc
%{mingw32_libdir}/cmake/WebP/
%{mingw32_libdir}/libwebp.dll.a
%{mingw32_libdir}/libwebpdecoder.dll.a
%{mingw32_libdir}/libwebpdemux.dll.a
%{mingw32_libdir}/libwebpmux.dll.a
%{mingw32_libdir}/libsharpyuv.dll.a

%files -n mingw64-libwebp
%license PATENTS COPYING
%{mingw64_bindir}/cwebp.exe
%{mingw64_bindir}/dwebp.exe
%{mingw64_bindir}/gif2webp.exe
%{mingw64_bindir}/img2webp.exe
%{mingw64_bindir}/webpinfo.exe
%{mingw64_bindir}/webpmux.exe
%{mingw64_bindir}/libwebp-7.dll
%{mingw64_bindir}/libwebpdecoder-3.dll
%{mingw64_bindir}/libwebpdemux-2.dll
%{mingw64_bindir}/libwebpmux-3.dll
%{mingw64_bindir}/libsharpyuv-0.dll
%{mingw64_includedir}/webp/
%{mingw64_libdir}/pkgconfig/libwebp.pc
%{mingw64_libdir}/pkgconfig/libwebpdecoder.pc
%{mingw64_libdir}/pkgconfig/libwebpdemux.pc
%{mingw64_libdir}/pkgconfig/libwebpmux.pc
%{mingw64_libdir}/pkgconfig/libsharpyuv.pc
%{mingw64_libdir}/cmake/WebP/
%{mingw64_libdir}/libwebp.dll.a
%{mingw64_libdir}/libwebpdecoder.dll.a
%{mingw64_libdir}/libwebpdemux.dll.a
%{mingw64_libdir}/libwebpmux.dll.a
%{mingw64_libdir}/libsharpyuv.dll.a
%endif


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Sandro Mani <manisandro@gmail.com> - 1.6.0-1
- Update to 1.6.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Sandro Mani <manisandro@gmail.com> - 1.5.0-1
- Update to 1.5.0

* Thu Aug 8 2024 Martin Stransky <stransky@redhat.com> - 1.4.0-4
- Added libwebp explicit dependency to libwebp-tools package

* Thu Aug 1 2024 Martin Stransky <stransky@redhat.com> - 1.4.0-3
- Disable libwebp-java on RHEL

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Apr 14 2024 Sandro Mani <manisandro@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Wed Feb 14 2024 Martin Stransky <stransky@redhat.com> - 1.3.2-5
- Migrated to SPDX license

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 28 2023 Sandro Mani <manisandro@gmail.com> - 1.3.2-2
- Backport upstream fix for CVE-2023-5129

* Mon Sep 18 2023 Sandro Mani <manisandro@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Wed Sep 13 2023 Boudhayan Bhattacharya <bbhtt.zn0i8@slmail.me> - 1.3.1-3
- Add patch for CVE-2023-4863 ref rhbz#2238543

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Sandro Mani <manisandro@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Sandro Mani <manisandro@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Thu Sep 22 2022 Sandro Mani <manisandro@gmail.com> - 1.2.4-2
- Add libwebp_libsuffix.patch

* Sun Aug 07 2022 Sandro Mani <manisandro@gmail.com> - 1.2.4-1
- Update to 1.2.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Sandro Mani <manisandro@gmail.com> - 1.2.3-1
- Update to 1.2.3

* Tue Jul 05 2022 Sandro Mani <manisandro@gmail.com> - 1.2.2-6
- Limit -java subpackage to %%java_arches

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.2.2-5
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.2.2-4
- Make mingw subpackages noarch

* Sat Feb 19 2022 Sandro Mani <manisandro@gmail.com> - 1.2.2-3
- Add mingw subpackage

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.2.2-2
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Sandro Mani <manisandro@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Thu Jan 06 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.1-3
- Drop aarch64 CFLAGS FTB workaround

* Sun Jan 02 2022 Dennis Gilmore <dennis@ausil.us> - 1.2.2-2
- do not disable neon support

* Sun Aug 15 2021 Sandro Mani <manisandro@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 01 2021 Sandro Mani <manisandro@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.1.0-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon May 18 2020 Sandro Mani <manisandro@gmail.com> - 1.1.0-3
- Don't manually and incorrectly install vwebp, Makefile already does it correctly (#1836640)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Sandro Mani <manisandro@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Tue Sep 17 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.0.3-3
- Rebuilt for new freeglut

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Sandro Mani <manisandro@gmail.com> - 1.0.3-1
- Update to 1.0.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Sandro Mani <manisandro@gmail.com> - 1.0.2-1
- Update to 1.0.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Sandro Mani <manisandro@gmail.com> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 27 2018 Sandro Mani <manisandro@gmail.com> - 0.6.1-8
- Fix LDFLAGS not passed when building libwebp_jni.so (#1548718)

* Mon Feb 26 2018 Sandro Mani <manisandro@gmail.com> - 0.6.1-7
- More big-endian fixes

* Fri Feb 16 2018 Sandro Mani <manisandro@gmail.com> - 0.6.1-6
- Backport another big-endian fix

* Fri Feb 16 2018 Sandro Mani <manisandro@gmail.com> - 0.6.1-5
- Backport upstream big-endian fix

* Tue Feb 13 2018 Sandro Mani <manisandro@gmail.com> - 0.6.1-4
- Rebuild (giflib)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.1-2
- Switch to %%ldconfig_scriptlets

* Thu Nov 30 2017 Sandro Mani <manisandro@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Thu Dec 22 2016 Sandro Mani <manisandro@gmail.com> - 0.5.2-1
- Update to 0.5.2

* Sat Oct 29 2016 Sandro Mani <manisandro@gmail.com> - 0.5.1-2
- Backport e2affacc35f1df6cc3b1a9fa0ceff5ce2d0cce83 (CVE-2016-9085, rhbz#1389338)

* Fri Aug 12 2016 Sandro Mani <manisandro@gmail.com> - 0.5.1-1
- upstream release 0.5.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Sandro Mani <manisandro@gmail.com> - 0.5.0-1
- upstream release 0.5.0

* Fri Oct 30 2015 Sandro Mani <manisandro@gmail.com> - 0.4.4-1
- upstream release 0.4.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Sandro Mani <manisandro@gmail.com> - 0.4.3-2
- Add BuildRequires: freeglut-devel to build vwebp

* Thu Mar 12 2015 Sandro Mani <manisandro@gmail.com> - 0.4.3-1
- upstream release 0.4.3

* Fri Oct 17 2014 Sandro Mani <manisandro@gmail.com> - 0.4.2-1
- upstream release 0.4.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.1-2
- Use frename-registers cflag to fix FTBFS on aarch64

* Tue Aug 05 2014 Sandro Mani <manisandro@gmail.com> - 0.4.1-1
- upstream release 0.4.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Jaromir Capik <jcapik@redhat.com> - 0.4.0-3
- Fixing endian checks (#962091)
- Fixing FTPBS caused by rpath presence

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.4.0-2
- Use Requires: java-headless rebuild (#1067528)

* Thu Jan 02 2014 Sandro Mani <manisandro@gmail.com> - 0.4.0-1
- upstream release 0.4.0

* Wed Oct 02 2013 Sandro Mani <manisandro@gmail.com> - 0.3.1-2
- enable webpdemux

* Sun Aug 04 2013 Sandro Mani <manisandro@gmail.com> - 0.3.1-1
- upstream release 0.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.3.0-1
- upstream release 0.3.0
- enable gif2webp
- add build requires on giflib-devel and libtiff-devel
- use make_install and hardened macros
- list binaries explicitly

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.2.1-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 27 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.1-1
- new upstream release 0.2.1

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.1.3-3
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.3-1
- Several spec improvements by Scott Tsai <scottt.tw@gmail.com>

* Wed May 25 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.2-1
- Initial spec. Based on openSUSE one
