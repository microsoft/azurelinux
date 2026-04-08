# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (c) 2016 Dave Love, Liverpool University
# Copyright (c) 2018 Dave Love, University of Manchester
# MIT licence, per Fedora policy.

# This flag prevents the linkage to libptscotch.so
%undefine _ld_as_needed

%bcond_without mpich

%if 0%{?fedora} >= 40
%ifarch %{ix86}
%bcond_with openmpi
%else
%bcond_without openmpi
%endif
%else
%bcond_without openmpi
%endif
%if 0%{?rhel} || 0%{?rhel} >= 9
%bcond_with colamd
%else
%bcond_without colamd
%endif

%if %{with openmpi}
%global openmpi openmpi
%else
%global openmpi %nil
%endif
%if %{with mpich}
%global mpich mpich
%else
%global mpich %nil
%endif

# Following scalapack
%bcond_without optimized_blas

%global blaslib flexiblas

# Choose if using 64-bit integers for indexing sparse matrices
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%bcond_with index64
%endif

%if %{with index64}
%global OPENBLASLINK -lflexiblas64
%global OPENBLASLIB /libflexiblas64.so
%else
%global OPENBLASLINK -lflexiblas
%global OPENBLASLIB /libflexiblas.so
%endif

%bcond_without check

# Enable CombBLAS support
%bcond_with CombBLAS

# RHEL8 does not provide Metis64
%if %{with index64}
BuildRequires: metis64-devel
%global METISLINK -lmetis64
%global METISLIB %{_libdir}/libmetis64.so
%global METISINC %{_includedir}/metis64.h
%else
BuildRequires: metis-devel
%global METISLINK -lmetis
%global METISLIB %{_libdir}/libmetis.so
%global METISINC %{_includedir}/metis.h
%endif

Name: superlu_dist
Version: 8.2.0
Release: 10%{?dist}
Epoch:   1
Summary: Solution of large, sparse, nonsymmetric systems of linear equations
# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
URL: http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
Source0: https://github.com/xiaoyeli/superlu_dist/archive/v%version/%name-%version.tar.gz

Patch0: %name-%version-fix-release-number.patch
Patch1: %name-fix_pkgconfig_creation.patch
Patch3: %name-scotch_parmetis.patch

# Longer tests take 1000 sec or timeout, so don't run them
Patch4: %name-only_short_tests.patch

BuildRequires: scotch-devel
BuildRequires: gcc-c++, dos2unix, chrpath
BuildRequires: cmake
%if %{with optimized_blas}
BuildRequires: %{blaslib}-devel
%endif
%if %{with colamd}
BuildRequires: suitesparse-devel
%endif


%global desc \
SuperLU is a general purpose library for the direct solution of large,\
sparse, nonsymmetric systems of linear equations.  The library is\
written in C and is callable from either C or Fortran program.  It\
uses MPI, OpenMP and CUDA to support various forms of parallelism.  It\
supports both real and complex datatypes, both single and double\
precision, and 64-bit integer indexing.  The library routines performs\
an LU decomposition with partial pivoting and triangular system solves\
through forward and back substitution.  The LU factorization routines\
can handle non-square matrices but the triangular solves are performed\
only for square matrices.  The matrix columns may be preordered\
(before factorization) either through library or user supplied\
routines.  This preordering for sparsity is completely separate from\
the factorization.  Working precision iterative refinement subroutines\
are provided for improved backward stability.  Routines are also\
provided to equilibrate the system, estimate the condition number,\
calculate the relative backward error, and estimate error bounds for\
the refined solutions.\
\
This version uses MPI and OpenMP.

%description
%desc

%if %{with openmpi}
%package openmpi
Summary:       Solution of large, sparse, nonsymmetric systems of linear equations - openmpi
BuildRequires: openmpi-devel
# ptscotch-openmpi-devel-parmetis unavailable on rhel8 ??
BuildRequires: ptscotch-openmpi-devel >= 6.0.5 %{!?el8:ptscotch-openmpi-devel-parmetis >= 6.0.5}
%if %{with CombBLAS}
BuildRequires: combblas-openmpi-devel >= 2.0.0
%endif
Requires:      gcc-gfortran%{?_isa}

%description openmpi
%desc
This is the openmpi version.


%package openmpi-devel
Summary: Development files for %name-openmpi
Requires: openmpi-devel%{?_isa}
Requires: %name-openmpi%{?_isa} = %{epoch}:%version-%release
Provides: %name-openmpi-static = %{epoch}:%version-%release

%description openmpi-devel
Development files for %name-openmpi
%endif


%package doc
Summary: Documentation for %name
BuildArch: noarch

%description doc
Documentation for %name

%if %{with mpich}
%package mpich
Summary:       Solution of large, sparse, nonsymmetric systems of linear equations - mpich
BuildRequires: mpich-devel
BuildRequires: ptscotch-mpich-devel  >= 6.0.5
BuildRequires: ptscotch-mpich-devel-parmetis  >= 6.0.5
%if %{with CombBLAS}
BuildRequires: combblas-mpich-devel >= 2.0.0
%endif
Requires:      gcc-gfortran%{?_isa}

%description mpich
%desc
This is the mpich version.


%package mpich-devel
Summary: Development files for %name-mpich
Requires: mpich-devel%{?_isa}
Requires: ptscotch-mpich-devel%{?_isa} ptscotch-mpich-devel-parmetis%{?_isa}
Requires: %name-mpich%{?_isa} = %{epoch}:%version-%release
Provides: %name-mpich-static = %{epoch}:%version-%release

%description mpich-devel
Development files for %name-mpich
%endif


%prep
%autosetup -n superlu_dist-%version -N

dos2unix CMakeLists.txt
%patch -P 0 -p1 -b .backup
%patch -P 1 -p1 -b .fix_pkgconfig_creation
%patch -P 4 -p1 -b .only_short_tests

%build
%if %{with openmpi}
%{_openmpi_load}
mkdir -p build/openmpi
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
export CFLAGS="%optflags -std=gnu17 -DPRNTlevel=0 -DDEBUGlevel=0"
export CXXFLAGS="%optflags -std=gnu++17 -I$MPI_INCLUDE"
export LDFLAGS="%build_ldflags -L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit"
%cmake -B build/openmpi -DCMAKE_BUILD_TYPE:STRING=Release \
 -DBUILD_STATIC_LIBS:BOOL=FALSE \
 -DCMAKE_Fortran_COMPILER:FILEPATH=$MPI_BIN/mpifort \
 -DMPIEXEC_EXECUTABLE:FILEPATH=$MPI_BIN/mpiexec \
%if %{with CombBLAS}
 -DTPL_COMBBLAS_INCLUDE_DIRS:PATH="$MPI_INCLUDE/CombBLAS;$MPI_INCLUDE/CombBLAS/3DSpGEMM;$MPI_INCLUDE/CombBLAS/Applications;$MPI_INCLUDE/CombBLAS/BipartiteMatchings" \
 -DTPL_COMBBLAS_LIBRARIES:STRING=$MPI_LIB/libCombBLAS.so -DTPL_ENABLE_COMBBLASLIB:BOOL=ON \
%endif
%if %{with colamd}
 -DTPL_ENABLE_COLAMD=ON -DTPL_COLAMD_INCLUDE_DIRS:PATH=%{_includedir}/suitesparse -DTPL_COLAMD_LIBRARIES:STRING=%{_libdir}/libcolamd.so \
 -DMPI_C_LINK_FLAGS:STRING="-L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit -L%{_libdir} %{METISLINK} -lscotch -lcolamd" \
%else
 -DTPL_ENABLE_COLAMD=OFF \
 -DMPI_C_LINK_FLAGS:STRING="-L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit -L%{_libdir} %{METISLINK} -lscotch" \
%endif
 -DTPL_ENABLE_INTERNAL_BLASLIB:BOOL=OFF -DTPL_BLAS_LIBRARIES:FILEPATH=%{_libdir}%{OPENBLASLIB} -DTPL_ENABLE_LAPACKLIB:BOOL=OFF -DTPL_LAPACK_LIBRARIES:BOOL=OFF \
 -DMPI_C_HEADER_DIR:PATH="$MPI_INCLUDE -I%{METISINC}" \
 -DMPI_CXX_LINK_FLAGS:STRING="-L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit -L%{_libdir} %{METISLINK} -lscotch -fopenmp" \
%if 0%{?fedora}
 -DTPL_PARMETIS_INCLUDE_DIRS:PATH=$MPI_INCLUDE \
 -DTPL_PARMETIS_LIBRARIES:STRING="$MPI_LIB/libptscotchparmetis.so;%{METISLIB}" \
%endif
%if %{with index64}
 -DXSDK_INDEX_SIZE=64 \
%else
 -DXSDK_INDEX_SIZE=32 \
%endif
 -DTPL_ENABLE_PARMETISLIB:BOOL=OFF \
 -Denable_double:BOOL=ON -Denable_complex16:BOOL=ON \
 -Denable_examples:BOOL=ON -Denable_tests:BOOL=ON -DBUILD_TESTING:BOOL=ON \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_BINDIR:PATH=$MPI_BIN -DCMAKE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE/%{name} \
 -DCMAKE_INSTALL_LIBDIR:PATH=$MPI_LIB -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON

%make_build V=1 -C build/openmpi
%{_openmpi_unload}
%endif

%if %{with mpich}
%{_mpich_load}
mkdir -p build/mpich
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
export CFLAGS="%optflags -std=gnu17 -DPRNTlevel=0 -DDEBUGlevel=0"
export CXXFLAGS="%optflags -std=gnu++17 -I$MPI_INCLUDE"
export LDFLAGS="%build_ldflags -L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit"
%cmake -B build/mpich -DCMAKE_BUILD_TYPE:STRING=Release \
 -DBUILD_STATIC_LIBS:BOOL=FALSE \
 -DCMAKE_Fortran_COMPILER:FILEPATH=$MPI_BIN/mpifort \
 -DMPIEXEC_EXECUTABLE:FILEPATH=$MPI_BIN/mpiexec \
%if %{with CombBLAS}
 -DTPL_COMBBLAS_INCLUDE_DIRS:PATH="$MPI_INCLUDE/CombBLAS;$MPI_INCLUDE/CombBLAS/3DSpGEMM;$MPI_INCLUDE/CombBLAS/Applications;$MPI_INCLUDE/CombBLAS/BipartiteMatchings" \
 -DTPL_COMBBLAS_LIBRARIES:STRING=$MPI_LIB/libCombBLAS.so -DTPL_ENABLE_COMBBLASLIB:BOOL=ON \
%endif
%if %{with colamd}
 -DTPL_ENABLE_COLAMD=ON -DTPL_COLAMD_INCLUDE_DIRS:PATH=%{_includedir}/suitesparse -DTPL_COLAMD_LIBRARIES:STRING=%{_libdir}/libcolamd.so \
 -DMPI_C_LINK_FLAGS:STRING="-L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit -L%{_libdir} %{METISLINK} -lscotch -lcolamd" \
%else
 -DTPL_ENABLE_COLAMD=OFF \
 -DMPI_C_LINK_FLAGS:STRING="-L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit -L%{_libdir} %{METISLINK} -lscotch" \
%endif
 -DTPL_ENABLE_INTERNAL_BLASLIB:BOOL=OFF -DTPL_BLAS_LIBRARIES:FILEPATH=%{_libdir}%{OPENBLASLIB} -DTPL_ENABLE_LAPACKLIB:BOOL=OFF -DTPL_LAPACK_LIBRARIES:BOOL=OFF \
 -DMPI_C_HEADER_DIR:PATH="$MPI_INCLUDE -I%{METISINC}" \
 -DMPI_CXX_LINK_FLAGS:STRING="-L$MPI_LIB -lptscotch -lptscotcherr -lptscotcherrexit -L%{_libdir} %{METISLINK} -lscotch" \
%if 0%{?fedora}
 -DTPL_PARMETIS_INCLUDE_DIRS:PATH=$MPI_INCLUDE \
 -DTPL_PARMETIS_LIBRARIES:STRING="$MPI_LIB/libptscotchparmetis.so;%{METISLIB}" \
%endif
%if %{with index64}
 -DXSDK_INDEX_SIZE=64 \
%else
 -DXSDK_INDEX_SIZE=32 \
%endif
 -DTPL_ENABLE_PARMETISLIB:BOOL=OFF \
 -Denable_double:BOOL=ON -Denable_complex16:BOOL=ON \
 -Denable_examples:BOOL=ON -Denable_tests:BOOL=ON -DBUILD_TESTING:BOOL=ON \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_BINDIR:PATH=$MPI_BIN -DCMAKE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE/%{name} \
 -DCMAKE_INSTALL_LIBDIR:PATH=$MPI_LIB -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON

%make_build -C build/mpich
%{_mpich_unload}
%endif


%install
%if %{with openmpi}
%{_openmpi_load}
%make_install -C build/openmpi
# Make sure all header files are installed
install -m644 SRC/*.h %buildroot$MPI_INCLUDE/superlu_dist/
rm -rf %buildroot$MPI_LIB/EXAMPLE
rm -rf %buildroot$MPI_LIB/superlu_dist/FORTRAN/CMakeFiles
chrpath -r $MPI_LIB %buildroot$MPI_LIB/libsuperlu_dist*.so*
%{_openmpi_unload}
%endif

%if %{with mpich}
%{_mpich_load}
%make_install -C build/mpich
# Make sure all header files are installed
install -m644 SRC/*.h %buildroot$MPI_INCLUDE/superlu_dist/

rm -rf %buildroot$MPI_LIB/EXAMPLE
rm -rf %buildroot$MPI_LIB/superlu_dist/FORTRAN/CMakeFiles
chrpath -r $MPI_LIB %buildroot$MPI_LIB/libsuperlu_dist*.so*
%{_mpich_unload}
%endif

%if %{with check}
%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%if %{with openmpi}
%{_openmpi_load}
# Waiting for excluding OpenMPI support in i686
%ifnarch %{ix86}
#mpirun -n 4 -v ../build/openmpi/EXAMPLE/pddrive -r 2 -c 2 g20.rua
%ctest -- --test-dir build/openmpi -VV
%endif
%{_openmpi_unload}
%endif

%ifnarch s390x
%if %{with mpich}
%{_mpich_load}
#mpirun -n 4 -v ../build/mpich/EXAMPLE/pddrive -r 2 -c 2 g20.rua
%ctest -- --test-dir build/mpich -VV
%{_mpich_unload}
%endif
%endif
%endif
# Check

%if %{with openmpi}
%files openmpi
%license License.txt
%_libdir/openmpi/lib/*.so.8
%_libdir/openmpi/lib/*.so.%{version}

%files openmpi-devel
%_libdir/openmpi/lib/*.so
%_libdir/openmpi/lib/*.a
%_libdir/openmpi/lib/pkgconfig/*.pc
%_includedir/openmpi-%_arch/superlu_dist/
%endif

%files doc
%license License.txt
%doc DOC/ug.pdf EXAMPLE

%if %{with mpich}
%files mpich
%license License.txt
%_libdir/mpich/lib/*.so.8
%_libdir/mpich/lib/*.so.%{version}

%files mpich-devel
%_libdir/mpich/lib/*.so
%_libdir/mpich/lib/*.a
%_libdir/mpich/lib/pkgconfig/*.pc
%_includedir/mpich-%_arch/superlu_dist/
%endif


%changelog
* Tue Aug 12 2025 Dave Love <loveshack@fedoraproject.org> - 1:8.2.0-10
- Fix #2276427

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 21 2025 Antonio Trande <sagitter@fedoraproject.org> - 1:8.2.0-8
- Fix GCC15 builds

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1:8.2.0-6
- convert license to SPDX

* Fri Aug 16 2024 Sandro Mani <manisandro@gmail.com> - 1:8.2.0-5
- Rebuild (scotch-7.0.4)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 Orion Poplawski <orion@nwra.com> - 1:8.2.0-3
- Rebuild with suitesparse 7.6.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Antonio Trande <sagitter@fedoraproject.org> - 1:8.2.0-1
- Release 8.2.0

* Thu Aug 17 2023 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.2-6
- Rebuild for scotch-7.0.4

* Sun Aug 06 2023 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.2-5
- Remove manual build method
- Modernize patch commands

* Sun Aug 06 2023 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.2-4
- Exclude mpich tests on s390x

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 18 2023 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.2-2
- Disable index64 builds

* Thu Apr 13 2023 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.2-1
- Release 8.1.2

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.1-2
- Disable colamd support in epel9

* Sun Oct 02 2022 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.1-1
- Release 8.1.1
- Enable colamd support

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Antonio Trande <sagitter@fedoraproject.org> - 1:8.1.0-1
- Release 8.1.0
- Remove obsolete conditional macros

* Sun May 29 2022 Antonio Trande <sagitter@fedoraproject.org> - 1:8.0.0-1
- Release 8.0.0
- Provide static libraries

* Sat Apr 16 2022 Antonio Trande <sagitter@fedoraproject.org> - 1:7.2.0-3
- Enable complex16 libraries

* Fri Apr 15 2022 Antonio Trande <sagitter@fedoraproject.org> - 1:7.2.0-2
- Make sure installing all header libraries

* Sat Apr 02 2022 Antonio Trande <sagitter@fedoraproject.org> - 1:7.2.0-1
- Release 7.2.0
- Enable CombBLAS support
- Add CMake build method
- Specific index_size

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 28 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1:6.1.1-6
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.1-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 13 2020 Dave Love <loveshack@fedoraproject.org> - 1:6.1.1-3
- Introduce epoch and revert incompatible change to 6.3.1

* Thu Apr  9 2020 Dave Love <loveshack@fedoraproject.org> - 6.3.1-1
- New version

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 12 2019 Dave Love <loveshack@fedoraproject.org> - 6.1.1-1
- New version

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 6.1.0-2
- Rebuild for openmpi 3.1.3

* Sun Feb 03 2019 Antonio Trande <sagitter@fedoraproject.org> - 6.1.0-1
- Release 6.1.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 16 2018 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-3
- libsuperlu_dist is a C++ library, link with mpicxx
- Allow oversubscription with openmpi in tests

* Thu Nov 29 2018 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-2
- Re-enable tests - seem to be working with openmpi 2.1.6rc1

* Wed Nov 21 2018 Dave Love <loveshack@fedoraproject.org> - 6.0.0-1
- New version
- Avoid tests

* Thu Jul 19 2018 Sandro Mani <manisandro@gmail.com> - 5.4.0-3
- Rebuild (scotch)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Dave Love <loveshack@fedoraproject.org> - 5.4.0-1
- New version

* Thu Apr 26 2018 Dave Love <loveshack@fedoraproject.org> - 5.3.0-3
- Require ptscotch-mpich-devel-parmetis

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Dave Love <loveshack@fedoraproject.org> - 5.3.0-1
- New version
- Update sovar
- Drop patch

* Sun Nov  5 2017 Dave Love <loveshack@fedoraproject.org> - 5.2.2-2
- Link againt ptscothmetis et al

* Tue Oct 31 2017 Dave Love <loveshack@fedoraproject.org> - 5.2.2-1
- New version
- Drop output and cmake patches
- Update soname minor version (added function)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun  9 2017 Dave Love <loveshack@fedoraproject.org> - 5.1.3-6
- Maybe use openblas_arches instead

* Thu Jun  8 2017 Dave Love <loveshack@fedoraproject.org> - 5.1.3-5
- Fix up mpich-devel requirement for el7 7.3
- Avoid openblas on s3909(x)

* Sat Jun  3 2017 Dave Love <loveshack@fedoraproject.org> - 5.1.3-4
- Fix mpich conditional
- Build for openmpi on s390 f25+

* Tue Apr 18 2017 Dave Love <loveshack@fedoraproject.org> - 5.1.3-3
- Rebuild for fix to rhbz #1435690

* Wed Apr 12 2017 Dave Love <loveshack@fedoraproject.org> - 5.1.3-2
- Fix EXAMPLES clean up

* Wed Apr 12 2017 Dave Love <loveshack@fedoraproject.org> - 5.1.3-1
- Exclude check on power64 and fix the mpich conditional

* Wed Mar  8 2017 Dave Love <loveshack@fedoraproject.org> - 5.1.3-1
- New version

* Fri Nov 25 2016 Dave Love <loveshack@fedoraproject.org> - 5.1.2-3
- Use optflags, __global_ldflags

* Thu Nov 17 2016 Dave Love <loveshack@fedoraproject.org> - 5.1.2-2
- Patch to avoid large diagnostic output

* Thu Oct 27 2016 Dave Love <loveshack@fedoraproject.org> - 5.1.2-1
- New version
- Drop the OpenMP patch

* Sat Oct 22 2016 Dave Love <loveshack@fedoraproject.org> - 5.1.1-3
- Fix soname

* Wed Oct 19 2016 Dave Love <loveshack@fedoraproject.org> - 5.1.1-2
- Conditionalize openmpi

* Mon Oct 17 2016 Dave Love <loveshack@fedoraproject.org> - 5.1.1-1
- New version
- Drop some patches and use ptscotch to replace parmetis
- Add mpich version
- Make -doc package

* Fri Nov 20 2015 Dave Love <loveshack@fedoraproject.org> - 4.2-1
- Initial version
