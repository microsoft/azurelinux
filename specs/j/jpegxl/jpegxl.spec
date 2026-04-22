## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# epel 8 need this other already have it
%undefine __cmake_in_source_build

# developper recommendation
%global toolchain clang

# Uncomment for special build to rebuild aom on bumped soname.
#global new_soname 1
%global sover_old 0.10
%global sover 0.11

%bcond_with gimp_plugin
%if 0%{?fedora}
%bcond_without tcmalloc
%endif

%global common_description %{expand:
This package contains a reference implementation of JPEG XL (encoder and
decoder).}

Name:           jpegxl
Epoch:          1
Version:        0.11.1
Release:        %autorelease %{?new_soname:-p -e 0~sonamebump}
Summary:        JPEG XL image format reference implementation

# Main library: BSD
# lodepng: zlib
# sjpeg: ASL 2.0
# skcms: BSD
License:        BSD-3-Clause AND Apache-2.0 AND Zlib
URL:            https://jpeg.org/jpegxl/
Source0:        https://github.com/libjxl/libjxl/archive/v%{version}/%{name}-%{version}.tar.gz

# set VERSION and run ./update_third_party.sh to get Source1 and Source2
Source1:        third_party-%{version}.tar.gz
Source2:        testdata-%{version}.tar.gz

BuildRequires:  asciidoc
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  clang
BuildRequires:  giflib-devel
%if %{with tcmalloc}
BuildRequires:  gperftools-devel
%endif
BuildRequires:  ninja-build
%if %{with gimp_plugin}
BuildRequires:  pkgconfig(gimp-3.0)
%endif
## sjpeg examples are not built
#BuildRequires:  (pkgconfig(glut) or pkgconfig(freeglut))
BuildRequires:  gtest-devel
BuildRequires:  gflags-devel
BuildRequires:  gmock-devel
BuildRequires:  pkgconfig(libhwy)
BuildRequires:  pkgconfig(libbrotlicommon)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
## benchmark tools are not built
#BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(OpenEXR)
## viewers are not built
#BuildRequires:  extra-cmake-modules
#BuildRequires:  pkgconfig(Qt5)
#BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(zlib)
# epel 8 need this other already have it
BuildRequires:  python3-devel
%if 0%{?new_soname}
BuildRequires:  libjxl < %{epoch}:%{version}
%endif

# No official release
Provides:       bundled(sjpeg) = 0-0.1.20230608gite5ab130
# Build system is Bazel, which is not packaged by Fedora
Provides:       bundled(skcms) = 0-0.1.20240122git51b7f2a

%description
%common_description

%package     -n libjxl-utils
Summary:        Utilities for manipulating JPEG XL images
Recommends:     gimp-jxl-plugin   = %{epoch}:%{version}-%{release}
Provides:       jpegxl-utils = %{epoch}:%{version}-%{release}
Obsoletes:      jpegxl-utils < 0.3.7-5

%description -n libjxl-utils
%{common_description}

%package     -n libjxl-devtools
Summary:        Development tools for JPEG-XL
Requires:       libjxl%{?_isa} = %{epoch}:%{version}-%{release}

%description -n libjxl-devtools
%{common_description}

Development tools for JPEG-XL

%package        doc
Summary:        Documentation for JPEG-XL
BuildArch:      noarch

%description    doc
%{common_description}

Documentation for JPEG-XL.

%package     -n libjxl
Summary:        Library files for JPEG-XL
Requires:       shared-mime-info
Provides:       jpegxl-libs = %{epoch}:%{version}-%{release}
Obsoletes:      jpegxl-libs < 0.3.7-5
Obsoletes:      jxl-pixbuf-loader < %{epoch}:%{version}-%{release}
%if %{without gimp_plugin}
Obsoletes:      gimp-jxl-plugin < 1:0.10.3-4
%endif

%description -n libjxl
%{common_description}

Library files for JPEG-XL.

%package     -n libjxl-devel
Summary:        Development files for JPEG-XL
Requires:       libjxl%{?_isa} = %{epoch}:%{version}-%{release}
Provides:       jpegxl-devel = %{epoch}:%{version}-%{release}
Obsoletes:      jpegxl-devel < 0.3.7-5

%description -n libjxl-devel
%{common_description}

Development files for JPEG-XL.

%if %{with gimp_plugin}
%package     -n gimp-jxl-plugin
Summary:        A plugin for loading and saving JPEG-XL images
Requires:       gimp

%description -n gimp-jxl-plugin
This is a GIMP plugin for loading and saving JPEG-XL images.
%endif

%prep
%autosetup -p1 -n libjxl-%{version}
rm -rf testdata/ third_party/
%setup -q -T -D -a 1 -a 2 -n libjxl-%{version}

%build
export CC=clang CXX=clang++
%cmake  -DENABLE_CCACHE=1 \
        -DBUILD_TESTING=ON \
        -DINSTALL_GTEST:BOOL=OFF \
        -DJPEGXL_ENABLE_BENCHMARK:BOOL=OFF \
        -DJPEGXL_ENABLE_PLUGINS:BOOL=ON \
        -DJPEGXL_ENABLE_PLUGIN_GDKPIXBUF:BOOL=OFF \
        -DJPEGXL_FORCE_SYSTEM_BROTLI:BOOL=ON \
        -DJPEGXL_FORCE_SYSTEM_GTEST:BOOL=ON \
        -DJPEGXL_FORCE_SYSTEM_HWY:BOOL=ON \
        -DJPEGXL_WARNINGS_AS_ERRORS:BOOL=OFF \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DBUNDLE_LIBPNG_DEFAULT:BOOL=OFF \
        -DBUNDLE_GFLAGS_DEFAULT:BOOL=OFF \
        -DJPEGXL_ENABLE_DEVTOOLS=ON
%cmake_build -- all doc

%install
%cmake_install
#rm -v %{buildroot}%{_libdir}/*.a

%if 0%{?new_soname}
cp -p %{_libdir}/libjxl.so.%{sover_old}*     \
  %{_libdir}/libjxl_threads.so.%{sover_old}* \
  %{_libdir}/libjxl_cms.so.%{sover_old}* \
  %{buildroot}%{_libdir}
%endif

%check
%ifarch s390x
# https://github.com/libjxl/libjxl/issues/3629
%ctest -E 'DecodeTest\.(ProgressionTestLosslessAlpha|FlushTestLosslessProgressiveAlpha)|EncodeTest\.FrameSettingsTest|JxlTest\.RoundtripAlpha(Resampling(OnlyAlpha)?|16)|JxlTest\.RoundtripProgressive(Level2Slow)?|ModularTest\.RoundtripLossy(DeltaPalette|16)?|RoundtripLossless/ModularTestParam\.RoundtripLossless/1bitSqueeze|RoundtripLossless/ModularTestParam\.RoundtripLossless/(1|2[01467]|30)bitSqueeze|PassesTest\.ProgressiveDownsample2DegradesCorrectly(Grayscale)?'
%else
%ctest
%endif

%files -n libjxl-utils
%doc CONTRIBUTING.md CONTRIBUTORS README.md
%{_bindir}/cjxl
%{_bindir}/djxl
%{_bindir}/jxlinfo
%{_mandir}/man1/cjxl.1*
%{_mandir}/man1/djxl.1*

%files -n libjxl-devtools
%{_bindir}/djxl_fuzzer_corpus
%{_bindir}/butteraugli_main
%{_bindir}/decode_and_encode
%{_bindir}/display_to_hlg
%{_bindir}/exr_to_pq
%{_bindir}/icc_simplify
%{_bindir}/pq_to_hlg
%{_bindir}/render_hlg
%{_bindir}/tone_map
%{_bindir}/texture_to_cube
%{_bindir}/generate_lut_template
%{_bindir}/ssimulacra_main
%{_bindir}/ssimulacra2
%{_bindir}/xyb_range
%{_bindir}/jxl_from_tree
%{_bindir}/local_tone_map

%files doc
%doc doc/*.md
%doc %{_vpath_builddir}/html
%license LICENSE

%files -n libjxl
%license LICENSE
%{_libdir}/libjxl.so.%{sover}*
%{_libdir}/libjxl_threads.so.%{sover}*
%{_libdir}/libjxl_cms.so.%{sover}*
%if 0%{?new_soname}
%{_libdir}/libjxl.so.%{sover_old}*
%{_libdir}/libjxl_threads.so.%{sover_old}*
%{_libdir}/libjxl_cms.so.%{sover_old}*
%endif
%{_datadir}/mime/packages/image-jxl.xml

%files -n libjxl-devel
%doc CONTRIBUTING.md
%{_includedir}/jxl/
%{_libdir}/libjxl.so
%{_libdir}/libjxl_threads.so
%{_libdir}/libjxl_cms.so
%{_libdir}/libjxl_extras_codec.a
%{_libdir}/pkgconfig/libjxl.pc
%{_libdir}/pkgconfig/libjxl_threads.pc
%{_libdir}/pkgconfig/libjxl_cms.pc

%if %{with gimp_plugin}
%files -n gimp-jxl-plugin
%license LICENSE
%{_libdir}/gimp/2.0/plug-ins/file-jxl/
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1:0.11.1-8
- Latest state for jpegxl

* Sun Dec 07 2025 Robert-André Mauchin <eclipseo@mauchin.fr> - 1:0.11.1-7
- Fix FTBFS with Clang 22

* Mon Oct 13 2025 Fabio Valentini <decathorpe@gmail.com> - 1:0.11.1-6
- Move jxl-pixbuf-loader Obsoletes to the correct subpackage

* Fri Sep 05 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 1:0.11.1-5
- Disable the pixbuf loader and thumbnailer

* Tue Aug 12 2025 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1:0.11.1-4
- enable tests

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 04 2025 Sérgio M. Basto <sergio@serjux.com> - 1:0.11.1-2
- un-bootstrap

* Sun Feb 02 2025 Sérgio M. Basto <sergio@serjux.com> - 1:0.11.1-0.1.0~sonamebump
- Update to 0.11.1 upstream release
- Resolves: rhbz#2312322

* Thu Jan 30 2025 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.4-1
- Update jpegxl to 0.10.4

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.10.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 29 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.3-5
- Fix upgrade path

* Thu Sep 19 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.3-4
- Disable gimp_plugin, jpegxl don't support Gimp 3 yet

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 07 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.3-2
- Fix generation of third_party sources

* Sun Jul 07 2024 Packit <hello@packit.dev> - 1:0.10.3-1
- Update to 0.10.3 upstream release
- Resolves: rhbz#2295526

* Sun Jul 07 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-6
- Configure Packit for release automation

* Tue Apr 23 2024 Orion Poplawski <orion@nwra.com> - 1:0.10.2-5
- Rebuild for openexr 3.2.4

* Wed Apr 17 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-4
- BR pkgconfig(lcms2) directly to fix build on eln

* Mon Mar 25 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-3
- un-bootstrap

* Wed Mar 13 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-0.2.0~sonamebump
- fix the build

* Wed Mar 13 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-0.1.0~sonamebump
- bootstrap 0.10.2 to start soname bump of jpegxl

* Wed Feb 14 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.9.2-2
- un-bootstrap jpegxl

* Wed Feb 14 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.9.2-0.1.0~sonamebump
- bootstrap 0.9.2 to build aom

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:0.8.2-3
- Drop unused build dependencies

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.8.2-1
- Update jpegxl to 0.8.2

* Tue Jun 20 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:0.8.1-3
- Disable unused Qt5 build dependencies

* Sun Jun 18 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.8.1-2
- unbootrap soname

* Mon Apr 03 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.8.1-0.1.0~sonamebump
- Update to 0.8.1 with new soname
- Drop patches because they are already in the code
- Add update_third_party.sh helper script

* Mon Apr 03 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.7.0-7
- fix epel8 builds

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 27 2022 Miroslav Suchý <msuchy@fedoraproject.org> - 1:0.7.0-5
- add epoch back

* Sat Nov 19 2022 Robert-André Mauchin <zebob.m@gmail.com>
- Convert to SPDX

* Sun Sep 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1:0.7.0-3
- Fix typo

* Sun Sep 25 2022 Robert-André Mauchin <zebob.m@gmail.com>
- Add Epoch to Provides. Close: rhbz#2129592

* Sun Sep 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1:0.7.0-1
- Fix update path (bump Epoch). Close: rhbz#2129592

* Sat Sep 24 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Sun Sep 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0rc-1
- Update to 0.7.0rc

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0~pre1-0.3.0~sonamebump
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0~pre1-0.2.0~sonamebump
- Unbootstrap

* Sun Jun 19 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0~pre1-0.1.0~sonamebump
- Update to prerelease 0.7.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.1-8
- Adapt for EPEL9

* Fri Dec 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.1-7
- Remove clang reference in favor of gcc-c++

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-6
- Drop manual release override

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-6
- Add manual release override

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-4
- Rebuild without soname bootstrap

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-3
- Fix BuildRequires when bumping soname

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-2
- Set explicit soname

* Sun Nov 21 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.1-1
- Update to 0.6.1 Close: rhbz#2018648

* Sat Oct 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5-3
- Rebuild for OpenEXR/Imath 3.1

* Tue Sep 07 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.5-2
- Rebuild. Close: rhbz#1997038

* Thu Aug 19 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.5-1
- Update to 0.5 Close: rhbz#1994433

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Adam Williamson <awilliam@redhat.com> - 0.3.7-3
- libs: drop Recommends: gimp-jxl-plugin to avoid pulling GIMP into Workstation

* Mon May 31 21:07:22 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.7-2
- Use Clang instead of GCC due to vector conversion strictness of GCC
- Disable LTO on arm due to Clang 12.0.0 bug
- Close: rhbz#1922638

* Mon May 17 20:49:39 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.7-1
- Update to 0.3.7

* Sat Jan 30 17:10:24 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3-1
- Update to 0.3

* Sat Dec 12 03:45:24 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.1.1-1
- Update to 0.1.1

* Wed Jul 15 17:00:49 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.0.1-0.1.20200715git0a46d01c
- Initial RPM

## END: Generated by rpmautospec
