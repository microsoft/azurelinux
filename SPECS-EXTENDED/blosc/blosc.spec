Summary:        High performance compressor optimized for binary data
Name:           blosc
Version:        1.21.4
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/Blosc/c-blosc
Source:         https://github.com/Blosc/c-blosc/archive/v%{version}/blosc-%{version}.tar.gz
Patch0:         %{name}-gcc11.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libzstd-devel
BuildRequires:  lz4-devel
BuildRequires:  snappy-devel
BuildRequires:  zlib-devel

%description
Blosc is a compression library designed to transmit data to the processor
cache faster than the traditional non-compressed memory fetch.
Compression ratios are not very high, but the decompression is very fast.
Blosc is meant not only to reduce the size of large datasets on-disk or
in-memory, but also to accelerate memory-bound computations.

%package devel
Summary:        Header files and libraries for Blosc development
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The blosc-devel package contains the header files and libraries needed
to develop programs that use the blosc meta-compressor.

%prep
%autosetup -n c-%{name}-%{version} -p1
rm -r internal-complibs/lz4* internal-complibs/zstd*

# Fix rpath issue
sed -i '1i  set\(CMAKE_SKIP_RPATH true\)' bench/CMakeLists.txt

# Fix cmake detection of pthreads
sed -i '1i  set\(CMAKE_POSITION_INDEPENDENT_CODE TRUE\)' CMakeLists.txt

# https://github.com/Blosc/c-blosc/issues/190
sed -i 's|lib/pkgconfig|%{_lib}/pkgconfig|' CMakeLists.txt

# Add python shebang and permission
sed -i '1i  #!%{_bindir}/python3' bench/plot-speeds.py

%build
# Use the proper library path and SSE2 instruction on 64bits systems
%cmake \
    -DBUILD_STATIC:BOOL=OFF \
    -DPREFER_EXTERNAL_LZ4:BOOL=ON \
    -DTEST_INCLUDE_BENCH_SUITE:BOOL=OFF \
    -DDEACTIVATE_SNAPPY:BOOL=OFF \
    -DPREFER_EXTERNAL_ZLIB:BOOL=ON \
    -DPREFER_EXTERNAL_ZSTD:BOOL=ON

%cmake_build

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%ctest

%install
%cmake_install

%files
%exclude %{_pkgdocdir}/bench/
%license LICENSES/*
%doc README.md ANNOUNCE.rst RELEASE_NOTES.rst README*.rst
%{_libdir}/libblosc.so.1*

%files devel
%{_libdir}/libblosc.so
%{_libdir}/pkgconfig/blosc.pc
%{_includedir}/blosc.h
%{_includedir}/blosc-export.h

%changelog
* Thu Aug 10 2023 Archana Choudhary <archana1@microsoft.com> - 1.21.4-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.
- Remove subpackage bench

* Sat May 20 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.21.4-1
- Version 1.21.4 (rhbz#2207738)

* Mon Jan 02 2023 jonathanspw <jonathan@almalinux.org> - 1.21.2-1
- update to 1.21.2 rhbz#2152010

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 07 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.21.1-1
- Version 1.21.1 (fixes rhbz#2011655)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 13 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.21.0-1
- Update to latest version (#1742237)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 15 2020 Jeff Law <law@redhat.com> - 1.20.1-2
- Prevent inlining, cloning and ipa analysis of sw32_ and _sw32 functions

* Wed Sep  9 20:41:44 MDT 2020 Orion Poplawski <orion@nwra.com> - 1.20.1-1
- Update to 1.20.1

* Tue Aug 11 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.19.0-4
- Fix build for new CMake macros (#1863272)
- Re-enable Snappy support (#1867915)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.19.0-1
- Update to latest version (#1742237)

* Sat May 23 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.18.1-1
- Update to latest version (#1742237)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct  3 2019 Orion Poplawski <orion@nwra.com> - 1.17.0-1
- Update to 1.17.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May  4 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.16.3-1
- Update to latest version (#1671929)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.14.4-1
- Update to latest version (#1609768)

* Thu Jul 19 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.14.3-1
- Update to latest version (#1539013)
- Drop obsolete ldconfig invocations

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.13.3-1
- Update to latest version (#1536731)

* Thu Jan 18 2018 Jan Beran <jberan@redhat.com> - 1.13.1-1

* New version using Python 3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.11.3-1
- Update to latest version
- Build against external zstd
- A pkgconfig file is now provided

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 07 2016 Than Ngo <than@redhat.com> - 1.11.1-2
- Fix the bigendian issue which causes build failure in PyTables (bz#1379123)

* Sun Nov  6 2016 Orion Poplawski <orion@cora.nwra.com> - 1.11.1-1
- Update to 1.11.1 (#1361777)
- Run cmake in %%build

* Mon Sep 26 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.10.1-2
- rebuilt for matplotlib-2.0.0

* Thu Jul 28 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 1.10.1-1
- Update to latest version (#1323008)

* Thu Jul 14 2016 Thibault North <tnorth@fedoraproject.org> - 1.9.3-1
- Update to 1.9.3 (#1211599)
- Remove 32-bits test patch now integrated

* Mon May 16 2016 Orion Poplawski <orion@cora.nwra.com> - 1.9.0-1
- Update to 1.9.0 (#1211599)
- Update URL
- Disable parallel build
- Run all tests
- Ship license files

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.6.1-1
- Update to 1.6.1 (#1211599)

* Mon Apr 20 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.4-1
- Update to 1.5.4 (#1211599)

* Tue Jan 06 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.2-1
- Update to 1.5.2 (#1115808)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 22 2014 Thibault North <tnorth@fedoraproject.org> - 1.3.5-1
- Update to 1.3.5

* Fri Mar 21 2014 Thibault North <tnorth@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4

* Tue Jan 07 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.0-1.rc2
- Attempt to package new version

* Tue Oct 22 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-9
- Fix flags and bench compilation

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-8
- Fix docdir for F<20 and remove sse flag

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-7
- Use install instead of cp, more fixes

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-6
- Fixes

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-5
- Use pkgdocdir, various fixes.

* Mon Oct 21 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-4
- Fix docdir, add blosc-bench subpackage

* Fri Oct 18 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-3
- Fixes (thanks Zbigniew Jędrzejewski-Szmek)

* Wed Oct 16 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-2
- Various fixes

* Fri Sep 20 2013 Thibault North <tnorth@fedoraproject.org> - 1.2.3-1
- Sync upstream

* Fri Mar 22 2013 Thibault North <tnorth@fedoraproject.org> - 1.1.6-1
- Initial package
