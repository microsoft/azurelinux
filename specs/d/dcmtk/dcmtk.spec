# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Notes on soname versioning
# There's absolutely no guarantee of ABI stability, so a soname bump is
# included for every new release:
# https://github.com/DCMTK/dcmtk/blob/master/CMake/dcmtkPrepare.cmake#L37

# Odd number releases are dev snapshots, so we will stick to even number
# (official releases) only.

%global abi_version 19

%bcond_with charls2

Name: dcmtk
Summary: Offis DICOM Toolkit (DCMTK)
Version: 3.6.9

# soname version is "abi_version.version"
# https://github.com/DCMTK/dcmtk/blob/master/CMake/dcmtkPrepare.cmake#L78
%global soname_version %{abi_version}.%{version}

Release: 3%{?dist}

# see licenses-3.6.9.txt for license breakdown
License: BSD-3-Clause and Apache-2.0 and BSD-2-Clause and (WTFPL or MIT) and GPL-3.0-or-later and ISC and MIT
Source: https://dicom.offis.de/download/dcmtk/dcmtk369/dcmtk-%{version}.tar.gz
URL: http://dicom.offis.de/dcmtk.php.en

# Downstream fixes
# Use bundled charls version and wait until upstream ports to new charls version
# charls version 2 includes a regression: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=923433
%if %{with charls2}
# not merged upstream yet: https://github.com/DCMTK/dcmtk/pull/18
# were generated against 3.6.7, not yet updated for 3.6.8
Patch:      0001-Use-system-CharLS-include.patch
Patch:      0002-Add-FindCharLS.patch
Patch:      0003-Find-and-include-CharLS.patch
Patch:      0004-Use-cmake-suggested-locations-for-CharLS.patch
Patch:      0005-Correct-CharLS-API-call.patch
Patch:      0006-Remove-reference-to-bundled-CharLS.patch
Patch:      0007-Update-JLS_ERROR-to-jpegls_error-in-CharLS-usage.patch
Patch:      0008-Correct-JpegLsReadHeader-arguments.patch
Patch:      0009-Update-JlsParameters-for-new-CharLS.patch
Patch:      0010-Correct-JpegLsDecode-arguments-for-CharLS-2.patch
Patch:      0011-Update-ilv-for-new-CharLS.patch
Patch:      0012-Correct-extra-include-for-CharLS.patch
Patch:      0013-Update-errors-to-use-enum-class-in-CharLS-2.patch
Patch:      0014-Define-BYTE-for-CharLS.patch
Patch:      0015-Update-colorTransformation-for-CharLS-2.patch
Patch:      0016-Update-JpegLsEncode-for-CharLS-2.patch
%endif

# Upstream fixes, backported to 3.6.9:
# https://github.com/sanjayankur31/dcmtk/tree/fedora-3.6.9

# Increase sleep in tests
# https://forum.dcmtk.org/viewtopic.php?t=5084
Patch:      0001-Increase-sleep-for-tests.patch

# place in correct locations
Patch:      0002-chore-undo-changes-to-standard-dirs.patch

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git-core
BuildRequires: cmake
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libxml2-devel
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: zlib-devel
%if %{with charls2}
BuildRequires: CharLS-devel >= 2.0.0
%endif
BuildRequires: doxygen

%description
DCMTK is a collection of libraries and applications implementing large
parts the DICOM standard. It includes software for examining,
constructing and converting DICOM image files, handling offline media,
sending and receiving images over a network connection, as well as
demonstrative image storage and worklist servers. DCMTK is is written
in a mixture of ANSI C and C++.  It comes in complete source code and
is made available as "open source" software. This package includes
multiple fixes taken from the "patched DCMTK" project.

Install DCMTK if you are working with DICOM format medical image files.

%package devel
Summary: Development Libraries and Headers for dcmtk
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{with charls2}
Requires: CharLS-devel%{?_isa}
%endif
Requires: libpng-devel%{?_isa}
Requires: libtiff-devel%{?_isa}

%description devel
Development Libraries and Headers for dcmtk.  You only need to install
this if you are developing programs that use the dcmtk libraries.

%prep
%autosetup -n %{name}-%{version} -p1 -S git

%if %{with charls2}
# Remove bundled libraries
rm -rf dcmjpls/libcharls/
%endif

# Fix permissions
find . -type f -name "*.h" -exec chmod 0644 '{}' \;
find . -type f -name "*.cc" -exec chmod 0644 '{}' \;

%build
export CFLAGS="%{optflags} -fPIC -Wno-error=deprecated-declarations"
export CXXFLAGS="%{optflags} -fPIC -Wno-error=deprecated-declarations"
export LDFLAGS="%{__global_ldflags} -fPIC"
%cmake -DCMAKE_BUILD_TYPE:STRING="Release" \
 -DDCMTK_INSTALL_LIBDIR=%{_lib} \
 -DDCMTK_INSTALL_CMKDIR=%{_lib}/cmake/%{name} \
 -DCMAKE_INSTALL_DOCDIR:PATH=%{_pkgdocdir} \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
 -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
 -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
 -DCMAKE_INSTALL_DATADIR:PATH=share \
 -DBUILD_APPS:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON \
 -DBUILD_SINGLE_SHARED_LIBRARY:BOOL=OFF \
 -DDCMTK_WITH_OPENSSL:BOOL=ON \
 -DDCMTK_WITH_PNG:BOOL=ON \
 -DDCMTK_WITH_PRIVATE_TAGS:BOOL=ON \
 -DDCMTK_WITH_TIFF:BOOL=ON \
 -DDCMTK_WITH_XML:BOOL=ON \
 -DDCMTK_WITH_CHARLS:BOOL=ON \
 -DDCMTK_WITH_ZLIB:BOOL=ON \
 -DDCMTK_ENABLE_CXX11:BOOL=ON \
 -Wno-dev
%cmake_build

%install
%cmake_install

# Remove zero-lenght file
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/wlistdb/OFFIS/lockfile

%ldconfig_scriptlets

%check
# ppc64le, s390x: remove dcmtls_scp_tls and dcmtls_scp_pool_tls that sporadically fails
%ifarch ppc64le s390x
rm -rf %{_vpath_builddir}/dcmtls/tests/
%endif
%ctest

%files
%license COPYRIGHT
%{_pkgdocdir}/
%{_bindir}/*
%{_libdir}/libdcmfg.so.%{soname_version}
%{_libdir}/libcmr.so.%{abi_version}
%{_libdir}/libcmr.so.%{soname_version}
%{_libdir}/libdcmdata.so.%{abi_version}
%{_libdir}/libdcmdata.so.%{soname_version}
%{_libdir}/libdcmdsig.so.%{abi_version}
%{_libdir}/libdcmdsig.so.%{soname_version}
%{_libdir}/libdcmect.so.%{abi_version}
%{_libdir}/libdcmect.so.%{soname_version}
%{_libdir}/libdcmfg.so.%{abi_version}
%{_libdir}/libdcmimage.so.%{abi_version}
%{_libdir}/libdcmimage.so.%{soname_version}
%{_libdir}/libdcmimgle.so.%{abi_version}
%{_libdir}/libdcmimgle.so.%{soname_version}
%{_libdir}/libdcmiod.so.%{abi_version}
%{_libdir}/libdcmiod.so.%{soname_version}
%{_libdir}/libdcmjpeg.so.%{abi_version}
%{_libdir}/libdcmjpeg.so.%{soname_version}
%{_libdir}/libdcmjpls.so.%{abi_version}
%{_libdir}/libdcmjpls.so.%{soname_version}
%{_libdir}/libdcmnet.so.%{abi_version}
%{_libdir}/libdcmnet.so.%{soname_version}
%{_libdir}/libdcmpmap.so.%{abi_version}
%{_libdir}/libdcmpmap.so.%{soname_version}
%{_libdir}/libdcmpstat.so.%{abi_version}
%{_libdir}/libdcmpstat.so.%{soname_version}
%{_libdir}/libdcmqrdb.so.%{abi_version}
%{_libdir}/libdcmqrdb.so.%{soname_version}
%{_libdir}/libdcmrt.so.%{abi_version}
%{_libdir}/libdcmrt.so.%{soname_version}
%{_libdir}/libdcmseg.so.%{abi_version}
%{_libdir}/libdcmseg.so.%{soname_version}
%{_libdir}/libdcmsr.so.%{abi_version}
%{_libdir}/libdcmsr.so.%{soname_version}
%{_libdir}/libdcmtkcharls.so.%{abi_version}
%{_libdir}/libdcmtkcharls.so.%{soname_version}
%{_libdir}/libdcmtls.so.%{abi_version}
%{_libdir}/libdcmtls.so.%{soname_version}
%{_libdir}/libdcmtract.so.%{abi_version}
%{_libdir}/libdcmtract.so.%{soname_version}
%{_libdir}/libdcmwlm.so.%{abi_version}
%{_libdir}/libdcmwlm.so.%{soname_version}
%{_libdir}/libdcmxml.so.%{abi_version}
%{_libdir}/libdcmxml.so.%{soname_version}
%{_libdir}/libi2d.so.%{abi_version}
%{_libdir}/libi2d.so.%{soname_version}
%{_libdir}/libijg16.so.%{abi_version}
%{_libdir}/libijg16.so.%{soname_version}
%{_libdir}/libijg12.so.%{abi_version}
%{_libdir}/libijg12.so.%{soname_version}
%{_libdir}/libijg8.so.%{abi_version}
%{_libdir}/libijg8.so.%{soname_version}
%{_libdir}/liboficonv.so.%{abi_version}
%{_libdir}/liboficonv.so.%{soname_version}
%{_libdir}/liboflog.so.%{abi_version}
%{_libdir}/liboflog.so.%{soname_version}
%{_libdir}/libofstd.so.%{abi_version}
%{_libdir}/libofstd.so.%{soname_version}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/consolog.cfg
%config(noreplace) %{_sysconfdir}/%{name}/dcmpstat.cfg
%config(noreplace) %{_sysconfdir}/%{name}/dcmqrprf.cfg
%config(noreplace) %{_sysconfdir}/%{name}/dcmqrscp.cfg
%config(noreplace) %{_sysconfdir}/%{name}/printers.cfg
%config(noreplace) %{_sysconfdir}/%{name}/storescp.cfg
%config(noreplace) %{_sysconfdir}/%{name}/storescu.cfg
%config(noreplace) %{_sysconfdir}/%{name}/filelog.cfg
%config(noreplace) %{_sysconfdir}/%{name}/logger.cfg
%{_datadir}/%{name}/
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/
%{_libdir}/libcmr.so
%{_libdir}/libdcmdata.so
%{_libdir}/libdcmdsig.so
%{_libdir}/libdcmect.so
%{_libdir}/libdcmfg.so
%{_libdir}/libdcmimgle.so
%{_libdir}/libdcmimage.so
%{_libdir}/libdcmiod.so
%{_libdir}/libdcmjpeg.so
%{_libdir}/libdcmjpls.so
%{_libdir}/libdcmnet.so
%{_libdir}/libdcmpmap.so
%{_libdir}/libdcmpstat.so
%{_libdir}/libdcmqrdb.so
%{_libdir}/libdcmrt.so
%{_libdir}/libdcmseg.so
%{_libdir}/libdcmsr.so
%{_libdir}/libdcmtkcharls.so
%{_libdir}/libdcmtls.so
%{_libdir}/libdcmtract.so
%{_libdir}/libdcmwlm.so
%{_libdir}/libdcmxml.so
%{_libdir}/libi2d.so
%{_libdir}/libijg16.so
%{_libdir}/libijg12.so
%{_libdir}/libijg8.so
%{_libdir}/liboficonv.so
%{_libdir}/liboflog.so
%{_libdir}/libofstd.so

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 20 2025 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.9-2
- Update license to SPDX identifiers

* Mon Feb 10 2025 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.9-1
- Update to 3.6.9 (rh#2297944)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 3.6.7-8
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 02 2023 Carl George <carl@george.computer> - 3.6.7-3
- Backport fix for CVE-2022-43272, resolves rhbz#2150930

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 02 2022 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.7-1
- Update to 3.6.7

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 25 2022 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.6-11
- Disable sporadically failing test on s390x also

* Mon Apr 25 2022 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.6-10
- Use bundled charls

* Mon Apr 25 2022 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.6-9
- Temporarily allow use of deprecated flags to fix build with openssl 3.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.6.6-7
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 09 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.6-6
- Explicitly set ABI version in shared objects
- Include note about lack of ABI compatibility
- Include note about versioning scheme

* Wed Aug 04 2021 Alessio <alciregi@fedoraproject.org> - 3.6.6-5
- Removed dcmtls_scp_tls and dcmtls_scp_pool_tls from ppc64le because sporadically fail

* Tue Aug 03 2021 Alessio <alciregi@fedoraproject.org> - 3.6.6-4
- Added patch to solve endianess test

* Wed Jul 28 2021 Alessio <alciregi@fedoraproject.org> - 3.6.6-3
- Added patch to increase sleep time in the dcmtls_scp_pool_tls test

* Sat Jul 24 2021 Alessio <alciregi@fedoraproject.org> - 3.6.6-1
- Release 3.6.6

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.6.4-10
- Fix RHBZ#1827255 (Manual pages installed at the wrong path)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 04 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.4-8
- Update cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 06 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.4-4
- Update to use CharLS v2

* Fri Sep 06 2019 Devrim Gündüz <devrim@gunduz.org> - 3.6.4-3
- Rebuild for new CharLS

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 09 2019 Antonio Trande <sagitterATfedoraproject.org> - 3.6.4-1
- Release 3.6.4
- Use %%_pkgdocdir
- Active modern C++ support
- Enable tests

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6.2-2
- Switch to %%ldconfig_scriptlets

* Sun Dec 10 2017 Jens Lody <fedora@jenslody.de> - 3.6.2-1
- Update to 3.6.2, fixes rhbz #1440439.
- Do not use deprecated tcp-wrappers, fixes rhbz #1518760.

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 3.6.1-8
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.6.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Dec 15 2014 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.1-1
- Upgraded to new upstream version.
- Various fixes to the specfile
- Fixes CVE-2013-6825 dcmtk: possible privilege escalation if setuid() fails

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.0-16
- General spec cleanup
- Move libs into _lib and remove ldd config file
- Fixes versioned doc dir as per BZ993719
- Bump up release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.0-14
- Added more requires to devel package as per BZ922937
- Added _isa to explicit requires

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 01 2012 Jon Ciesla <limburgher@gmail.com> - 3.6.0-12
- FTBFS, BZ 819236.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-10
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.6.0-8
- Rebuild for new libpng

* Thu Oct 20 2011 Dan Horák <dan[at]danny.cz> 3.6.0-7
- skip the EOL conversion step, files are correct (FTBFS due a change in dos2unix)

* Wed Oct 19 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-6
- Added explicit require for CharLS-devel as requested in #745277

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-5
- Fixed dir ownership

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-4
- Added doxygen BR

* Tue Mar 22 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-3
- Fixed soname generation for residual modules

* Mon Mar 21 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-2
- Fixed shared library generation
- Fixed patch schema numbering

* Sun Mar 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-1
- Removed bundled charls
- Rebased on public dcmtk git repository

* Thu Feb 3 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.1-1.20110203git
- Updated to new version
- Added patch to fix shared lib generation

* Tue Oct 19 2010 Mario Ceresa <mrceresa@fedoraproject.org> 3.5.4-4
- Adding soname's to generated lib

* Mon Mar 15 2010 Andy Loening <loening@alum dot mit dot edu> 3.5.4-3
- updates for packaging with fedora core
- multiple fixes/enhancements from pdcmtk version 48

* Sat Jan 02 2010 Andy Loening <loening@ alum dot mit dot edu> 3.5.4-2
- tlslayer.cc patch for openssl 1.0

* Thu Feb 02 2006 Andy Loening <loening @ alum dot mit dot edu> 3.5.4-1
- initial build
