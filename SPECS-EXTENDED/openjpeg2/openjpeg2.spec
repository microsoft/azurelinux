Vendor:         Microsoft Corporation
Distribution:   Mariner
# Conformance tests disabled by default since it requires 1 GB of test data
#global runcheck 1

#global optional_components 1

# https://bugzilla.redhat.com/show_bug.cgi?id=1751749
%global _target_platform %{_vendor}-%{_target_os}

Name:           openjpeg2
Version:        2.3.1
Release:        12%{?dist}
Summary:        C-Library for JPEG 2000

# windirent.h is MIT, the rest is BSD
License:        BSD and MIT
URL:            https://github.com/uclouvain/openjpeg
Source0:        https://github.com/uclouvain/openjpeg/archive/v%{version}/openjpeg-%{version}.tar.gz
%if 0%{?runcheck}
# git clone git@github.com:uclouvain/openjpeg-data.git
Source1:        data.tar.xz
%endif

# Rename tool names to avoid conflicts with openjpeg-1.x
Patch0:         openjpeg2_opj2.patch
# Backport patch for CVE 2020-6851
# https://github.com/uclouvain/openjpeg/issues/1228
Patch1:         openjpeg2_CVE-2020-6851.patch
# Backport patch for CVE 2020-8112
# https://github.com/uclouvain/openjpeg/pull/1232/commits/05f9b91e60debda0e83977e5e63b2e66486f7074
Patch2:         openjpeg2_CVE-2020-8112.patch
# Backport patch for CVE-2020-27814
# https://github.com/uclouvain/openjpeg/commit/eaa098b59b346cb88e4d10d505061f669d7134fc
Patch3:         openjpeg2_CVE-2020-27814.patch
# Backport patch for CVE-2020-27824
# https://github.com/uclouvain/openjpeg/pull/1292/commits/6daf5f3e1ec6eff03b7982889874a3de6617db8d
Patch4:         openjpeg2_CVE-2020-27824.patch
# Backport patch for CVE-2020-27823
# https://github.com/uclouvain/openjpeg/commit/b2072402b7e14d22bba6fb8cde2a1e9996e9a919
Patch5:         openjpeg2_CVE-2020-27823.patch
# Backport patch for CVE-2020-27841
# https://github.com/rouault/openjpeg/commit/00383e162ae2f8fc951f5745bf1011771acb8dce
Patch6:         openjpeg2_CVE-2020-27841.patch
# Backport patch for CVE-2020-27842
# https://github.com/uclouvain/openjpeg/pull/1296/commits/fbd30b064f8f9607d500437b6fedc41431fd6cdc
Patch7:         openjpeg2_CVE-2020-27842.patch
# Backport patch for CVE-2020-27843
# https://github.com/rouault/openjpeg/commit/38d661a3897052c7ff0b39b30c29cb067e130121
Patch8:         openjpeg2_CVE-2020-27843.patch
# Backport patch for CVE-2020-27845
# https://github.com/uclouvain/openjpeg/commit/8f5aff1dff510a964d3901d0fba281abec98ab63
Patch9:         openjpeg2_CVE-2020-27845.patch


BuildRequires:  cmake
# The library itself is C only, but there is some optional C++ stuff, hence the project is not marked as C-only in cmake and hence cmake looks for a c++ compiler
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  lcms2-devel
BuildRequires:  doxygen

%if 0%{?optional_components}
BuildRequires:  java-devel
BuildRequires:  xerces-j2
%endif

%description
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains
* JPEG 2000 codec compliant with the Part 1 of the standard (Class-1 Profile-1
  compliance).
* JP2 (JPEG 2000 standard Part 2 - Handling of JP2 boxes and extended multiple
  component transforms for multispectral and hyperspectral imagery)


%package devel
Summary:        Development files for OpenJPEG 2
Requires:       %{name}%{?_isa} = %{version}-%{release}
# OpenJPEGTargets.cmake refers to the tools
Requires:       %{name}-tools%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use OpenJPEG 2.


%package devel-docs
Summary:        Developer documentation for OpenJPEG 2
BuildArch:      noarch

%description devel-docs
The %{name}-devel-docs package contains documentation files for developing
applications that use OpenJPEG 2.


%package tools
Summary:        OpenJPEG 2 command line tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Command line tools for JPEG 2000 file manipulation, using OpenJPEG2:
 * opj2_compress
 * opj2_decompress
 * opj2_dump

%if 0%{?optional_components}
##### MJ2 #####

%package mj2
Summary:        OpenJPEG2 MJ2 module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description mj2
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the MJ2 module (JPEG 2000 standard Part 3)


%package mj2-devel
Summary:        Development files for OpenJPEG2 MJ2 module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-mj2%{?_isa} = %{version}-%{release}

%description mj2-devel
Development files for OpenJPEG2 MJ2 module


%package mj2-tools
Summary:        OpenJPEG2 MJ2 module command line tools
Requires:       %{name}-mj2%{?_isa} = %{version}-%{release}

%description mj2-tools
OpenJPEG2 MJ2 module command line tools

##### JPWL #####

%package jpwl
Summary:        OpenJPEG2 JPWL module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description jpwl
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JPWL (JPEG 2000 standard Part 11 - Jpeg 2000 Wireless)


%package jpwl-devel
Summary:        Development files for OpenJPEG2 JPWL module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-jpwl%{?_isa} = %{version}-%{release}

%description jpwl-devel
Development files for OpenJPEG2 JPWL module


%package jpwl-tools
Summary:        OpenJPEG2 JPWL module command line tools
Requires:       %{name}-jpwl%{?_isa} = %{version}-%{release}

%description jpwl-tools
OpenJPEG2 JPWL module command line tools

##### JPIP #####

%package jpip
Summary:        OpenJPEG2 JPIP module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description jpip
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JPWL (JPEG 2000 standard Part 9 - Jpeg 2000 Interactive Protocol)


%package jpip-devel
Summary:        Development files for OpenJPEG2 JPIP module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-jpwl%{?_isa} = %{version}-%{release}

%description jpip-devel
Development files for OpenJPEG2 JPIP module


%package jpip-tools
Summary:        OpenJPEG2 JPIP module command line tools
Requires:       %{name}-jpip%{?_isa} = %{version}-%{release}
Requires:       jpackage-utils
Requires:       java

%description jpip-tools
OpenJPEG2 JPIP module command line tools

##### JP3D #####

%package jp3d
Summary:        OpenJPEG2 JP3D module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description jp3d
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JP3D (JPEG 2000 standard Part 10 - Jpeg 2000 3D)


%package jp3d-devel
Summary:        Development files for OpenJPEG2 JP3D module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-jp3d%{?_isa} = %{version}-%{release}

%description jp3d-devel
Development files for OpenJPEG2 JP3D module


%package jp3d-tools
Summary:        OpenJPEG2 JP3D module command line tools
Requires:       %{name}-jp3d%{?_isa} = %{version}-%{release}

%description jp3d-tools
OpenJPEG2 JP3D module command line tools
%endif


%prep
%autosetup -p1 -n openjpeg-%{version} %{?runcheck:-a 1}

# Remove all third party libraries just to be sure
find thirdparty/ -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;


%build
# TODO: Consider
# -DBUILD_JPIP_SERVER=ON -DBUILD_JAVA=ON
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DOPENJPEG_INSTALL_LIB_DIR=%{_lib} \
    %{?optional_components:-DBUILD_MJ2=ON -DBUILD_JPWL=ON -DBUILD_JPIP=ON -DBUILD_JP3D=ON} \
    -DBUILD_DOC=ON \
    -DBUILD_STATIC_LIBS=OFF \
    -DBUILD_SHARED_LIBS=ON \
    %{?runcheck:-DBUILD_TESTING:BOOL=ON -DOPJ_DATA_ROOT=$PWD/../data}

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_mandir}/man1/opj_compress.1 %{buildroot}%{_mandir}/man1/opj2_compress.1
mv %{buildroot}%{_mandir}/man1/opj_decompress.1 %{buildroot}%{_mandir}/man1/opj2_decompress.1
mv %{buildroot}%{_mandir}/man1/opj_dump.1 %{buildroot}%{_mandir}/man1/opj2_dump.1

# Docs are installed through %%doc
rm -rf %{buildroot}%{_datadir}/doc/

%if 0%{?optional_components}
# Move the jar to the correct place
mkdir -p %{buildroot}%{_javadir}
mv %{buildroot}%{_datadir}/opj_jpip_viewer.jar %{buildroot}%{_javadir}/opj2_jpip_viewer.jar
cat > %{buildroot}%{_bindir}/opj2_jpip_viewer <<EOF
java -jar %{_javadir}/opj2_jpip_viewer.jar "$@"
EOF
chmod +x %{buildroot}%{_bindir}/opj2_jpip_viewer
%endif


%ldconfig_scriptlets


%check
%if 0%{?runcheck}
%ctest
%endif


%files
%{!?_licensedir:%global license %doc}
%license LICENSE
%doc AUTHORS.md NEWS.md README.md THANKS.md
%{_libdir}/libopenjp2.so.*
%{_mandir}/man3/libopenjp2.3*

%files devel
%dir %{_includedir}/openjpeg-2.3/
%{_includedir}/openjpeg-2.3/openjpeg.h
%{_includedir}/openjpeg-2.3/opj_config.h
%{_includedir}/openjpeg-2.3/opj_stdint.h
%{_libdir}/libopenjp2.so
%{_libdir}/openjpeg-2.3/
%{_libdir}/pkgconfig/libopenjp2.pc

%files devel-docs
%doc %{__cmake_builddir}/doc/html

%files tools
%{_bindir}/opj2_compress
%{_bindir}/opj2_decompress
%{_bindir}/opj2_dump
%{_mandir}/man1/opj2_compress.1*
%{_mandir}/man1/opj2_decompress.1*
%{_mandir}/man1/opj2_dump.1*

%if 0%{?optional_components}
%files mj2
%{_libdir}/libopenmj2.so.*

%files mj2-devel
%{_libdir}/libopenmj2.so

%files mj2-tools
%{_bindir}/opj2_mj2*

%files jpwl
%{_libdir}/libopenjpwl.so.*

%files jpwl-devel
%{_libdir}/libopenjpwl.so
%{_libdir}/pkgconfig/libopenjpwl.pc

%files jpwl-tools
%{_bindir}/opj2_jpwl*

%files jpip
%{_libdir}/libopenjpip.so.*

%files jpip-devel
%{_libdir}/libopenjpip.so
%{_libdir}/pkgconfig/libopenjpip.pc

%files jpip-tools
%{_bindir}/opj2_jpip*
%{_bindir}/opj2_dec_server
%{_javadir}/opj2_jpip_viewer.jar

%files jp3d
%{_libdir}/libopenjp3d.so.*

%files jp3d-devel
%{_includedir}/openjpeg-2.0/openjp3d.h
%{_libdir}/libopenjp3d.so
%{_libdir}/pkgconfig/libopenjp3d.pc

%files jp3d-tools
%{_bindir}/opj2_jp3d*
%endif


%changelog
* Fri Mar 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.1-12
- Bumping release to re-build with newer 'libtiff' libraries.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.1-11
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Dec 17 2020 Sandro Mani <manisandro@gmail.com> - 2.3.1-10
* Backport patches for CVE-2020-27841, CVE-2020-27842, CVE-2020-27843, CVE-2020-27845

* Thu Dec 10 2020 Sandro Mani <manisandro@gmail.com> - 2.3.1-9
* Backport patches for CVE-2020-27824 and CVE-2020-27823

* Sat Nov 28 2020 Sandro Mani <manisandro@gmail.com> - 2.3.1-8
- Backport patch for CVE-2020-27814

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Feb 13 2020 Sandro Mani <manisandro@gmail.com> - 2.3.1-6
- Backport patch for CVE 2020-8112

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Sandro Mani <manisandro@gmail.com> - 2.3.1-4
- Backport patch for CVE 2020-6851

* Wed Oct 02 2019 Sandro Mani <manisandro@gmail.com> - 2.3.1-3
- Fix unbundling 3rd party libraries (#1757822)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 02 2019 Sandro Mani <manisandro@gmail.com> - 2.3.1-1
- Update to 2.3.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 20 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-10
- Backport patches for CVE-2018-18088, CVE-2018-6616

* Thu Oct 04 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-9
- Backport patch for CVE-2018-5785 (#1537758)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-7
- BR: gcc-c++

* Mon Feb 19 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-6
- Add missing BR: gcc, make

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.3.0-4
- Switch to %%ldconfig_scriptlets

* Mon Dec 25 2017 Sandro Mani <manisandro@gmail.com> - 2.3.0-3
- Rename tool names at cmake level to ensure OpenJPEGTargets.cmake refers to the renamed files

* Mon Dec 25 2017 Sandro Mani <manisandro@gmail.com> - 2.3.0-2
- Use BUILD_STATIC_LIBS=OFF instead of deleting the static library after build

* Thu Oct 05 2017 Sandro Mani <manisandro@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Thu Sep 07 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-4
- Backport fix for CVE-2017-14039

* Thu Aug 31 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-3
- Backport more security fixes, including for CVE-2017-14041 and CVE-2017-14040

* Thu Aug 31 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-2
- Backport patch for CVE-2017-12982

* Thu Aug 10 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 17 2016 Sandro Mani <manisandro@gmail.com> - 2.1.2-3
- Add patch for CVE-2016-9580 (#1405128) and CVE-2016-9581 (#1405135)

* Thu Dec 08 2016 Sandro Mani <manisandro@gmail.com> - 2.1.2-2
- Add patch for CVE-2016-9572 (#1402714) and CVE-2016-9573 (#1402711)

* Wed Sep 28 2016 Sandro Mani <manisandro@gmail.com> - 2.1.2-1
- Update to 2.1.2
- Fixes: CVE-2016-7445

* Fri Sep 09 2016 Sandro Mani <manisandro@gmail.com> - 2.1.1-3
- Backport: Add sanity check for tile coordinates (#1374337)

* Fri Sep 09 2016 Sandro Mani <manisandro@gmail.com> - 2.1.1-2
- Backport fixes for CVE-2016-7163

* Wed Jul 06 2016 Sandro Mani <manisandro@gmail.com> - 2.1.1-1
- Update to 2.1.1
- Fixes: CVE-2016-3183, CVE-2016-3181, CVE-2016-3182, CVE-2016-4796, CVE-2016-4797, CVE-2015-8871

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 01 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-7
- Backport fix for possible double-free (#1267983)

* Tue Sep 15 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-6
- Backport fix for use after free vulnerability (#1263359)

* Thu Jun 25 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-5
- Add openjpeg2_bigendian.patch (#1232739)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Sandro Mani <manisandro@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Wed Apr 16 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-5
- Switch to official 2.0 release and backport pkg-config patch

* Thu Apr 10 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-4.svn20140403
- Replace define with global
- Fix #define optional_components 1S typo
- Fix %%(pwd) -> $PWD for test data
- Added some BR for optional components
- Include opj2_jpip_viewer.jar in %%files

* Wed Apr 09 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-3.svn20140403
- Fix source url
- Fix mixed tabs and spaces
- Fix description too long

* Wed Apr 09 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-2.svn20140403
- Remove thirdparty libraries folder in prep
- Own %%{_libdir}/openjpeg-2.0/
- Fix Requires
- Add missing ldconfig
- Add possibility to run conformance tests if desired
 
* Thu Apr 03 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-1.svn20140403
- Initial package
