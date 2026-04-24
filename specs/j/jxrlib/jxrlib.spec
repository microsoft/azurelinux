# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jxrlib
Version:        1.1
Release: 33%{?dist}
Summary:        Open source implementation of jpegxr

# See JPEGXR_DPK_Spec_1.0.doc. Upstream request for plain text license file at
# https://jxrlib.codeplex.com/workitem/13
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://jxrlib.codeplex.com/
Source0:        http://jxrlib.codeplex.com/downloads/get/685249#/jxrlib_%(echo %{version} | tr . _).tar.gz
# Use CMake to build to facilitate creation of shared libraries
# See https://jxrlib.codeplex.com/workitem/13
Source1:        CMakeLists.txt
# Converted from shipped doc/JPEGXR_DPK_Spec_1.doc
# libreoffice --headless --convert-to pdf doc/JPEGXR_DPK_Spec_1.0.doc
Source2:        JPEGXR_DPK_Spec_1.0.pdf

# Fix various warnings, upstreamable
# See https://jxrlib.codeplex.com/workitem/13
Patch0:         jxrlib_warnings.patch
# Mingw build fixes
Patch1:         jxrlib_mingw.patch

BuildRequires:  cmake
BuildRequires:  gcc

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc


%description
This is an open source implementation of the jpegxr image format standard.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n mingw32-%{name}
Summary:       MinGW Windows JPEG XR library
BuildArch:     noarch

%description -n mingw32-%{name}
MinGW Windows JPEG XR library.


%package -n mingw64-%{name}
Summary:       MinGW Windows JPEG XR library
BuildArch:     noarch

%description -n mingw64-%{name}
MinGW Windows JPEG XR library.


%{?mingw_debug_package}


%prep
%setup -q -n %{name}

# Sanitize charset and line endings
for file in `find . -type f -name '*.c' -or -name '*.h' -or -name '*.txt'`; do
  iconv --from=ISO-8859-15 --to=UTF-8 $file > $file.new && \
  sed -i 's|\r||g' $file.new && \
  touch -r $file $file.new && mv $file.new $file
done

%patch -P0 -p1
%patch -P1 -p1

# Remove shipped binaries
rm -rf bin

cp -a %{SOURCE1} .
cp -a %{SOURCE2} doc


%build
# Native build
%cmake
%cmake_build

# MinGW build
%mingw_cmake
%mingw_make_build


%install
%cmake_install
%mingw_make_install

# Delete guiddef.h which conflicts with guiddef.h shipped by mingw-headers
rm -f %{buildroot}%{mingw32_includedir}/jxrlib/guiddef.h
rm -f %{buildroot}%{mingw64_includedir}/jxrlib/guiddef.h


%mingw_debug_install_post


%files
%doc doc/readme.txt doc/JPEGXR_DPK_Spec_1.0.pdf
%{_bindir}/JxrEncApp
%{_bindir}/JxrDecApp
%{_libdir}/libjpegxr.so.*
%{_libdir}/libjxrglue.so.*

%files devel
%{_includedir}/jxrlib/
%{_libdir}/libjpegxr.so
%{_libdir}/libjxrglue.so

%files -n mingw32-%{name}
%{mingw32_bindir}/libjpegxr.dll
%{mingw32_bindir}/libjxrglue.dll
%{mingw32_bindir}/JxrDecApp.exe
%{mingw32_bindir}/JxrEncApp.exe
%{mingw32_includedir}/jxrlib/
%{mingw32_libdir}/libjpegxr.dll.a
%{mingw32_libdir}/libjxrglue.dll.a

%files -n mingw64-%{name}
%{mingw64_bindir}/libjpegxr.dll
%{mingw64_bindir}/libjxrglue.dll
%{mingw64_bindir}/JxrDecApp.exe
%{mingw64_bindir}/JxrEncApp.exe
%{mingw64_includedir}/jxrlib/
%{mingw64_libdir}/libjpegxr.dll.a
%{mingw64_libdir}/libjxrglue.dll.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Sandro Mani <manisandro@gmail.com> - 1.1-31
- Increase minimum cmake version to 3.5
- Port CMakeLists.txt to GNUInstallDirs

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1-29
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 05 2022 Sandro Mani <manisandro@gmail.com> - 1.1-23
- Don't install guiddef.h for mingw

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.1-21
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.1-20
- Make mingw subpackages noarch

* Sun Feb 20 2022 Sandro Mani <manisandro@gmail.com> - 1.1-19
- Add mingw subpackege

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 18 2018 Sandro Mani <manisandro@gmail.com> - 1.1-10
- Add missing BR: gcc, make

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 11 2015 Sandro Mani <manisandro@gmail.com> - 1.1-4
- Fix typo in jxrlib_warnings.patch

* Tue Sep 08 2015 Sandro Mani <manisandro@gmail.com> - 1.1-3
- Add Patch0 and Source1 upstream links
- Ship pdf variant of JPEGXR_DPK_Spec_1.0.doc in %%doc
- Remove bin folder

* Tue Sep 08 2015 Sandro Mani <manisandro@gmail.com> - 1.1-2
- Comments for Patch0 and Source1

* Wed Sep 02 2015 Sandro Mani <manisandro@gmail.com> - 1.1-1
- Initial package
