# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%global cmake_blas_flags -DBLA_VENDOR=FlexiBLAS
%else
%global blaslib openblas
%global blasvar o
%global cmake_blas_flags -DBLAS_LIBRARIES=%{_libdir}/lib%{blaslib}%{blasvar}.so
%endif

%bcond mingw %{undefined rhel}
%bcond sparsehash %{undefined rhel}
%bcond suitesparse %{undefined rhel}
%bcond SuperLU %{undefined rhel}
%bcond scotch %{undefined rhel}
%bcond metis %{undefined rhel}

Name:           eigen3
Version:        3.4.0
Release: 19%{?dist}
Summary:        A lightweight C++ template library for vector and matrix math

License:        Apache-2.0 AND MPL-2.0 AND LGPL-2.0-or-later AND BSD-3-Clause AND Minpack
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
Source0:        https://gitlab.com/libeigen/eigen/-/archive/%{version}/eigen-%{version}.tar.bz2
# For mingw, read the comment in the file for details
Source1:        mingw_TryRunResults.cmake

BuildRequires:  %{blaslib}-devel
BuildRequires:  fftw-devel
%if 0
# for OpenGL in unit tests, disabled by default
BuildRequires:  glew-devel
%endif
BuildRequires:  gmp-devel
%if 0
# only used in benchmarks, not used in the RPM build
BuildRequires:  gsl-devel
%endif
BuildRequires:  mpfr-devel
BuildRequires:  gcc-gfortran
%if %{with sparsehash}
BuildRequires:  sparsehash-devel
%endif
%if %{with suitesparse}
BuildRequires:  suitesparse-devel
%endif
%if %{with SuperLU}
BuildRequires:  SuperLU-devel
%endif
%if %{with scotch}
BuildRequires:  scotch-devel
%endif
%if %{with metis}
BuildRequires:  metis-devel
%endif

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  tex(latex)

%if %{with mingw}
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-gcc-gfortran
BuildRequires:  mingw32-fftw
BuildRequires:  mingw32-gmp
BuildRequires:  mingw32-mpfr

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-gcc-gfortran
BuildRequires:  mingw64-fftw
BuildRequires:  mingw64-gmp
BuildRequires:  mingw64-mpfr
%endif

%description
%{summary}.


%package devel
Summary:        A lightweight C++ template library for vector and matrix math
BuildArch:      noarch
# -devel subpkg only atm, compat with other distros
Provides:       %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides:       %{name}-static = %{version}-%{release}

%description devel
%{summary}.

%package doc
Summary:        Developer documentation for Eigen
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%description doc
Developer documentation for Eigen.

%if %{with mingw}
# Mingw32
%package -n mingw32-%{name}
Summary:        %{summary}
BuildArch:      noarch

%description -n mingw32-%{name}
%{summary}

# Mingw64
%package -n mingw64-%{name}
Summary:        %{summary}
BuildArch:      noarch

%description -n mingw64-%{name}
%{summary}
%endif


%prep
%autosetup -p1 -n eigen-%{version}


%build
# Native build
%cmake \
    -DINCLUDE_INSTALL_DIR=%{_includedir}/%{name} \
    -DCMAKEPACKAGE_INSTALL_DIR=%{_datadir}/cmake/%{name} \
    %{cmake_blas_flags} \
%if %{with SuperLU}
    -DSUPERLU_INCLUDES=%{_includedir}/SuperLU \
%endif
%if %{with scotch}
    -DSCOTCH_INCLUDES=%{_includedir} -DSCOTCH_LIBRARIES="scotch" \
%endif
%if %{with metis}
    -DMETIS_INCLUDES=%{_includedir} -DMETIS_LIBRARIES="metis" \
%endif
    -DEIGEN_TEST_CXX11=ON

%cmake_build
%cmake_build --target doc

rm -f %{_vpath_builddir}/doc/html/installdox
rm -f %{_vpath_builddir}/doc/html/unsupported/installdox

%if %{with mingw}
# MinGW build
MINGW32_CMAKE_ARGS="-DINCLUDE_INSTALL_DIR=%{mingw32_includedir}/%{name} -DCMAKEPACKAGE_INSTALL_DIR=%{mingw32_datadir}/cmake/%{name}" \
MINGW64_CMAKE_ARGS="-DINCLUDE_INSTALL_DIR=%{mingw64_includedir}/%{name} -DCMAKEPACKAGE_INSTALL_DIR=%{mingw64_datadir}/cmake/%{name}" \
%mingw_cmake -C%{SOURCE1} -DEIGEN_BUILD_PKGCONFIG:BOOL=ON -DEIGEN_TEST_CXX11=ON
%endif


%install
%cmake_install
%if %{with mingw}
%mingw_make_install
%endif


%check
# Building tests takes ages
# cmake_build --target buildtests
# ctest


%files devel
%license COPYING.README COPYING.APACHE COPYING.BSD COPYING.MPL2 COPYING.GPL COPYING.LGPL COPYING.MINPACK
%{_includedir}/%{name}
%{_datadir}/cmake/%{name}
%{_datadir}/pkgconfig/%{name}.pc

%files doc
%doc %{_vpath_builddir}/doc/html

%if %{with mingw}
%files -n mingw32-%{name}
%license COPYING.BSD COPYING.LGPL COPYING.MPL2 COPYING.README
%{mingw32_includedir}/%{name}
%{mingw32_datadir}/pkgconfig/%{name}.pc
%{mingw32_datadir}/cmake/%{name}/

%files -n mingw64-%{name}
%license COPYING.BSD COPYING.LGPL COPYING.MPL2 COPYING.README
%{mingw64_includedir}/%{name}
%{mingw64_datadir}/pkgconfig/%{name}.pc
%{mingw64_datadir}/cmake/%{name}/
%endif


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 Orion Poplawski <orion@nwra.com> - 3.4.0-15
- Rebuild with suitesparse 7.6.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.4.0-12
- Drop unused glew build dependency

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.4.0-10
- Avoid extra test dependencies in RHEL builds

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Sandro Mani <manisandro@gmail.com> - 3.4.0-8
- Drop eigen_mma.patch

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.4.0-6
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 3.4.0-5
- Add mingw subpackages

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Sep 12 2021 Rich Mattes <richmattes@gmail.com> - 3.4.0-3
- Apply MMA patch unconditionally, and edit patch to only define MMA disable on
  __PPC64__ (rhbz#2003362)

* Wed Aug 25 2021 Sandro Mani <manisandro@gmail.com> - 3.4.0-2
- Temporarily disable EIGEN_ALTIVEC_DISABLE_MMA on PPC64le

* Thu Aug 19 2021 Sandro Mani <manisandro@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Björn Esser <besser82@fedoraproject.org> - 3.3.9-6
- Properly set BLA_VENDOR to FlexiBLAS for cmake >= 3.19

* Wed Jun 02 2021 Jiri Kucera <jkucera@redhat.com> - 3.3.9-5
- Add missing Minpack license
  Resolves: #1965214

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Jan Grulich <jgrulich@redhat.com> - 3.3.9-3
- Drop qt dependency on RHEL 8 and higher

* Tue Jan 19 2021 Sandro Mani <manisandro@gmail.com> - 3.3.9-2
- Backport fix for conflicting declarations of log1p

* Sun Dec 06 2020 Sandro Mani <manisandro@gmail.com> - 3.3.9-1
- Update to 3.3.9

* Mon Oct 05 2020 Sandro Mani <manisandro@gmail.com> - 3.3.8-2
- Drop reference to undefined Eigen::eigen_assert_exception

* Mon Oct 05 2020 Sandro Mani <manisandro@gmail.com> - 3.3.8-1
- Update to 3.3.8

* Tue Sep 01 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.7-7
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Sat Aug 29 2020 Fabio Valentini <decathorpe@gmail.com> - 3.3.7-6
- Adapt to CMake macros changes in fedora 33+.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 25 2018 Sandro Mani <manisandro@gmail.com> - 3.3.7-1
- Update to 3.3.7
- Modernize spec
- Add doc

* Mon Dec 10 2018 Sandro Mani <manisandro@gmail.com> - 3.3.6-1
- Update to 3.3.6

* Thu Sep 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 3.3.5-2
- backport upstream fix for step FTBFS (#1619860)

* Thu Jul 26 2018 Sandro Mani <manisandro@gmail.com> - 3.3.5-1
- Update to 3.3.5

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Björn Esser <besser82@fedoraproject.org> - 3.3.4-6
- Fix compilation of Jacobi rotations with ARM NEON, some
  specializations of internal::conj_helper were missing

* Sun Feb 18 2018 Sandro Mani <manisandro@gmail.com> - 3.3.4-5
- Add missing BR: gcc-c++, make

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Sandro Mani <manisandro@gmail.com> - 3.3.4-1
- Update to 3.3.4

* Wed Feb 22 2017 Sandro Mani <manisandro@gmail.com> - 3.3.3-1
- Update to 3.3.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 22 2017 Sandro Mani <manisandro@gmail.com> - 3.3.2-1
- Update to 3.3.2

* Wed Dec 28 2016 Rich Mattes <richmattes@gmail.com> - 3.3.1-1
- Update to 3.3.1 (rhbz#1408538)

* Wed Nov 23 2016 Rich Mattes <richmattes@gmail.com> - 3.3.0-1
- Update to 3.3.0
- Stop renaming tarball - just use upstream tarball

* Tue Oct 04 2016 Sandro Mani <manisandro@gmail.com> - 3.2.10-1
- Update to 3.2.10

* Tue Jul 19 2016 Sandro Mani <manisandro@gmail.com> - 3.2.9-1
- Update to 3.2.9

* Sat Feb 20 2016 Sandro Mani <manisandro@gmail.com> - 3.2.8-1
- Update to 3.2.8

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Sandro Mani <manisandro@gmail.com> - 3.2.7-3
- Again: Fix incorrect include path in pkgconfig file

* Fri Nov 06 2015 Sandro Mani <manisandro@gmail.com> - 3.2.7-2
- Fix incorrect include path in pkgconfig file

* Thu Nov 05 2015 Sandro Mani <manisandro@gmail.com> - 3.2.7-1
- Update to release 3.2.7

* Thu Oct 01 2015 Sandro Mani <manisandro@gmail.com> - 3.2.6-1
- Update to release 3.2.6

* Fri Aug 21 2015 Rich Mattes <richmattes@gmail.com> - 3.2.5-2
- Apply patch to install FindEigen3.cmake

* Tue Jun 16 2015 Sandro Mani <manisandro@gmail.com> - 3.2.5-1
- Update to release 3.2.5

* Thu Jan 22 2015 Sandro Mani <manisandro@gmail.com> - 3.2.4-1
- Update to release 3.2.4

* Mon Jan 05 2015 Rich Mattes <richmattes@gmail.com> - 3.2.3-2
- Backport upstream Rotation2D fix

* Thu Dec 18 2014 Sandro Mani <manisandro@gmail.com> - 3.2.3-1
- Update to release 3.2.3
- Drop upstreamed eigen3-ppc64.patch

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Sandro Mani <manisandro@gmail.com> - 3.2.2-1
- Update to release 3.2.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-4
- Add ppc64 support

* Thu Feb 27 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-3
- Make doc package noarch

* Thu Feb 27 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-2
- Split off doc to a separate package

* Wed Feb 26 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-1
- Udpate to release 3.2.1

* Sun Aug 11 2013 Sandro Mani <manisandro@gmail.com> - 3.2-3
- Build and run tests
- Drop -DBLAS_LIBRARIES_DIR, not used
- Add some BR to enable tests of corresponding backends
- spec cleanup

* Wed Jul 24 2013 Sandro Mani <manisandro@gmail.com> - 3.2-1
- Update to release 3.2

* Sat Jun 29 2013 Rich Mattes <richmattes@gmail.com> - 3.1.3-2
- Add upstream patch to fix malloc/free bugs (rhbz#978971)

* Fri Apr 19 2013 Sandro Mani <manisandro@gmail.com> - 3.1.3-1
- Update to release 3.1.3
- Add patch for unused typedefs warning with gcc4.8

* Tue Mar 05 2013 Rich Mattes <richmattes@gmail.com> - 3.1.2-1
- Update to release 3.1.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 28 2012 Tim Niemueller <tim@niemueller.de> - 3.0.6-1
- Update to release 3.0.6 (fixes GCC 4.7 warnings)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Rich Mattes <richmattes@gmail.com> - 3.0.5-1
- Update to release 3.0.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Rich Mattes <richmattes@gmail.com> - 3.0.4-1
- Update to release 3.0.4

* Tue Nov 15 2011 Rich Mattes <richmattes@gmail.com> - 3.0.3-1
- Update to release 3.0.3

* Sun Apr 17 2011 Rich Mattes <richmattes@gmail.com> - 3.0.0-2
- Patched sources to fix build failure
- Removed fixes made upstream
- Added project name to source tarball filename

* Sat Mar 26 2011 Rich Mattes <richmattes@gmail.com> - 3.0.0-1
- Update to release 3.0.0

* Tue Jan 25 2011 Rich Mattes <richmattes@gmail.com> - 3.0-0.2.beta2
- Change blas-devel buildrequirement to atlas-devel
- Don't make the built-in experimental blas library

* Mon Jan 24 2011 Rich Mattes <richmattes@gmail.com> - 3.0-0.1.beta2
- Initial package
