# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 40
%ifarch %{ix86}
%bcond_with openmpi
%else
%bcond_without openmpi
%endif
%else
%bcond_without openmpi
%endif

# openmpi3 only exists in RHEL7
# and not on ppc ppc64
%if 0%{?rhel} == 7
%ifarch ppc ppc64
  %bcond_with openmpi3
%else
  %bcond_without openmpi3
%endif
%else
  %bcond_with openmpi3
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
%ifarch ppc ppc64 s390 s390x
  # No mpich in RHEL < 7 for these arches
  %bcond_with mpich
%else
  %bcond_without mpich
%endif
%else
  # Enable mpich on RHEL >= 7 and on Fedora
  %bcond_without mpich
%endif

%bcond_without optimized_blas

%if "%{?_lib}" == "lib64"
%global _cmake_lib_suffix64 -DLIB_SUFFIX=64
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%if %{with optimized_blas}
%global blasflags -DBLA_VENDOR=FlexiBLAS
%else
%global blasflags -DBLA_VENDOR=Generic
%endif
%else
%global blaslib openblas
%if %{with optimized_blas}
%global blasflags -DLAPACK_LIBRARIES=-l%{blaslib} -DBLAS_LIBRARIES=-l%{blaslib}
%else
%global blasflags -DLAPACK_LIBRARIES=-llapack -DBLAS_LIBRARIES=-lblas
%endif
%endif

Summary: A subset of LAPACK routines redesigned for heterogeneous computing
Name: scalapack
Version: 2.2.2
Release: 5%{?dist}
License: BSD-3-Clause-Open-MPI
URL: http://www.netlib.org/scalapack/
Source0: https://github.com/Reference-ScaLAPACK/scalapack/archive/v%{version}.tar.gz
BuildRequires: cmake
%if %{with optimized_blas}
BuildRequires: %{blaslib}-devel
%else
BuildRequires: lapack-devel
BuildRequires: blas-devel
%endif
BuildRequires: gcc-gfortran, glibc-devel
%if %{with mpich}
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires: mpich-devel
%else
BuildRequires: mpich-devel-static
%endif
%endif
%if %{with openmpi}
BuildRequires: openmpi-devel
%endif
%if %{with openmpi3}
BuildRequires: openmpi3-devel
%endif
Patch1: scalapack-2.2.2-fix-libsuffix.patch
Patch2: scalapack-2.2.2-fix-cmake-minimum.patch

%description
The ScaLAPACK (or Scalable LAPACK) library includes a subset 
of LAPACK routines redesigned for distributed memory MIMD 
parallel computers. It is currently written in a 
Single-Program-Multiple-Data style using explicit message 
passing for inter-processor communication. It assumes 
matrices are laid out in a two-dimensional block cyclic 
decomposition.

ScaLAPACK is designed for heterogeneous computing and is 
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on 
block-partitioned algorithms in order to minimize the frequency 
of data movement between different levels of the memory hierarchy. 
(For such machines, the memory hierarchy includes the off-processor 
memory of other processors, in addition to the hierarchy of registers, 
cache, and local memory on each processor.) The fundamental building 
blocks of the ScaLAPACK library are distributed memory versions (PBLAS) 
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra 
Communication Subprograms (BLACS) for communication tasks that arise 
frequently in parallel linear algebra computations. In the ScaLAPACK 
routines, all inter-processor communication occurs within the PBLAS and the 
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK 
routines resemble their LAPACK equivalents as much as possible. 

%package common
Summary: Common files for scalapack
# The blacs symbols live in libscalapack
Provides: blacs-common = %{version}-%{release}
Obsoletes: blacs-common <= 2.0.2

%description common
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains common files which are not specific
to any MPI implementation.

%if %{with mpich}

%package mpich
Summary: ScaLAPACK libraries compiled against mpich
Requires: %{name}-common = %{version}-%{release}
Requires: mpich
Provides: %{name}-mpich2 = %{version}-%{release}
Obsoletes: %{name}-mpich2 < 1.7.5-19
# This is a lie, but something needs to obsolete it.
Provides: %{name}-lam = %{version}-%{release}
Obsoletes: %{name}-lam <= 1.7.5-7
# The blacs symbols live in libscalapack
Provides: blacs-mpich = %{version}-%{release}
Obsoletes: blacs-mpich <= 2.0.2

%description mpich
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK libraries compiled with mpich.

%package mpich-devel
Summary: Development libraries for ScaLAPACK (mpich)
Requires: %{name}-mpich = %{version}-%{release}
Requires: mpich-devel
Provides: %{name}-lam-devel = %{version}-%{release}
Obsoletes: %{name}-lam-devel <= 1.7.5-7
Provides: %{name}-mpich2-devel = %{version}-%{release}
Obsoletes: %{name}-mpich2-devel < 1.7.5-19
# The blacs symbols live in libscalapack
Provides: blacs-mpich-devel = %{version}-%{release}
Obsoletes: blacs-mpich-devel <= 2.0.2

%description mpich-devel
This package contains development libraries for ScaLAPACK, compiled against mpich.

%package mpich-static
Summary: Static libraries for ScaLAPACK (mpich)
Provides: %{name}-lam-static = %{version}-%{release}
Obsoletes: %{name}-lam-static <= 1.7.5-7
Requires: %{name}-mpich-devel = %{version}-%{release}
Provides: %{name}-mpich2-static = %{version}-%{release}
Obsoletes: %{name}-mpich2-static < 1.7.5-19
# The blacs symbols live in libscalapack
Provides: blacs-mpich-static = %{version}-%{release}
Obsoletes: blacs-mpich-static <= 2.0.2

%description mpich-static
This package contains static libraries for ScaLAPACK, compiled against mpich.

%endif

%if %{with openmpi}
%package openmpi
Summary: ScaLAPACK libraries compiled against openmpi
Requires: %{name}-common = %{version}-%{release}
Requires: openmpi
# The blacs symbols live in libscalapack
Provides: blacs-openmpi = %{version}-%{release}
Obsoletes: blacs-openmpi <= 2.0.2

%description openmpi
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK libraries compiled with openmpi.

%package openmpi-devel
Summary: Development libraries for ScaLAPACK (openmpi)
Requires: %{name}-openmpi = %{version}-%{release}
Requires: openmpi-devel
# The blacs symbols live in libscalapack
Provides: blacs-openmpi-devel = %{version}-%{release}
Obsoletes: blacs-openmpi-devel <= 2.0.2

%description openmpi-devel
This package contains development libraries for ScaLAPACK, compiled against openmpi.

%package openmpi-static
Summary: Static libraries for ScaLAPACK (openmpi)
Requires: %{name}-openmpi-devel = %{version}-%{release}
# The blacs symbols live in libscalapack
Provides: blacs-openmpi-static = %{version}-%{release}
Obsoletes: blacs-openmpi-static <= 2.0.2

%description openmpi-static
This package contains static libraries for ScaLAPACK, compiled against openmpi.
%endif

%if %{with openmpi3}
%package openmpi3
Summary: ScaLAPACK libraries compiled against openmpi3
Requires: %{name}-common = %{version}-%{release}
Requires: openmpi3
# The blacs symbols live in libscalapack
Provides: blacs-openmpi3 = %{version}-%{release}
Obsoletes: blacs-openmpi3 <= 2.0.2

%description openmpi3
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK libraries compiled with openmpi3.

%package openmpi3-devel
Summary: Development libraries for ScaLAPACK (openmpi3)
Requires: %{name}-openmpi3 = %{version}-%{release}
Requires: openmpi3-devel
# The blacs symbols live in libscalapack
Provides: blacs-openmpi3-devel = %{version}-%{release}
Obsoletes: blacs-openmpi3-devel <= 2.0.2

%description openmpi3-devel
This package contains development libraries for ScaLAPACK, compiled against openmpi3.

%package openmpi3-static
Summary: Static libraries for ScaLAPACK (openmpi3)
Requires: %{name}-openmpi3-devel = %{version}-%{release}
# The blacs symbols live in libscalapack
Provides: blacs-openmpi3-static = %{version}-%{release}
Obsoletes: blacs-openmpi3-static <= 2.0.2

%description openmpi3-static
This package contains static libraries for ScaLAPACK, compiled against openmpi3.
%endif

%prep
%setup -q -c -n %{name}-%{version}
%patch -P1 -p1 -b .libsuffix
%patch -P2 -p1 -b .fix-cmake-minimum

# fix incorrect version in CMakeLists.txt
sed -i 's|2.2.1|%{version}|g' %{name}-%{version}/CMakeLists.txt

for i in %{?with_mpich:mpich} %{?with_openmpi:openmpi} %{?with_openmpi3:openmpi3}; do
  cp -a %{name}-%{version} %{name}-%{version}-$i
done

%build
%global build_type_safety_c 0
CC="$CC -std=gnu89"
%global build_fflags %(echo %build_fflags -fallow-argument-mismatch| sed 's|-Werror=format-security||g')
%global dobuild() \
cd %{name}-%{version}-$MPI_COMPILER_NAME ; \
%ifarch i686 \
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_STATIC_LIBS:BOOL=ON -DMPI_BASE_DIR=%{_libdir}/$MPI_COMPILER_NAME %{blasflags}; \
%cmake_build ;\
%cmake -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF -DMPI_BASE_DIR=%{_libdir}/$MPI_COMPILER_NAME %{blasflags}; \
%cmake_build ;\
%else \
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_STATIC_LIBS:BOOL=ON -DMPI_BASE_DIR=%{_libdir}/$MPI_COMPILER_NAME %{blasflags} %{?_cmake_lib_suffix64}; \
%cmake_build ;\
%cmake -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF -DMPI_BASE_DIR=%{_libdir}/$MPI_COMPILER_NAME %{blasflags} %{?_cmake_lib_suffix64}; \
%cmake_build ;\
%endif \
cd ..

%if %{with mpich}
# Build mpich version
export MPI_COMPILER_NAME=mpich
%{_mpich_load}
%dobuild
%{_mpich_unload}
%endif

%if %{with openmpi}
# Build OpenMPI version
export MPI_COMPILER_NAME=openmpi
%{_openmpi_load}
%dobuild
%{_openmpi_unload}
%endif

%if %{with openmpi3}
# Build OpenMPI3 version
export MPI_COMPILER_NAME=openmpi3
%{_openmpi3_load}
%dobuild
%{_openmpi3_unload}
%endif

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/cmake
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

for i in %{?with_mpich:mpich} %{?with_openmpi:openmpi} %{?with_openmpi3:openmpi3}; do
  mkdir -p %{buildroot}%{_libdir}/$i/lib/
  pushd %{name}-%{version}-$i
  %cmake_install
  cp -f %{_vpath_builddir}/lib/libscalapack.a %{buildroot}%{_libdir}/$i/lib/
  popd
  mkdir -p %{buildroot}%{_includedir}/$i-%{_arch}/
  # This file is independent of the MPI compiler used, but it is poorly named
  # So we'll put it in %{_includedir}/blacs/
  mkdir -p %{buildroot}%{_includedir}/blacs/
  install -p %{name}-%{version}-$i/BLACS/SRC/Bdef.h %{buildroot}%{_includedir}/blacs/

  for f in *.so*; do
    mv %{buildroot}%{_libdir}/$f %{buildroot}%{_libdir}/$i/lib/
  done
  mv %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_libdir}/$i/lib/
done

# Copy docs
cd %{name}-%{version}
cp -f README ../

# Fixup .pc files
%if %{with openmpi}
sed -i 's|mpi|ompi|g' %{buildroot}%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc
sed -i 's|L%{_libdir}|L${libdir}|' %{buildroot}%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc
sed -i 's|prefix=/usr|prefix=/usr/%{_lib}/openmpi|' %{buildroot}%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc
sed -i 's|libdir=%{_libdir}|libdir=${prefix}/lib|' %{buildroot}%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc
%endif

%if %{with mpich}
sed -i 's|mpi|mpich|g' %{buildroot}%{_libdir}/mpich/lib/pkgconfig/scalapack.pc
sed -i 's|L%{_libdir}|L${libdir}|' %{buildroot}%{_libdir}/mpich/lib/pkgconfig/scalapack.pc
sed -i 's|libdir=%{_libdir}|libdir=%{_libdir}/mpich/lib|' %{buildroot}%{_libdir}/mpich/lib/pkgconfig/scalapack.pc
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
# The above conditional allows us to do this only for flexiblas. openblas doesn't have a pc.
%if %{with optimized_blas}
%if %{with openmpi}
sed -i 's|lapack blas|flexiblas|g' %{buildroot}%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc
%endif
%if %{with mpich}
sed -i 's|lapack blas|flexiblas|g' %{buildroot}%{_libdir}/mpich/lib/pkgconfig/scalapack.pc
%endif
#openblas3 doesn't exist for modern fedora or rhel >= 9.
%endif
%endif

%files common
%doc README
%{_includedir}/blacs/
%{_libdir}/cmake/%{name}-%{version}/

%if %{with mpich}
%files mpich
%{_libdir}/mpich/lib/libscalapack.so.2.2
%{_libdir}/mpich/lib/libscalapack.so.2.2.2

%files mpich-devel
%{_includedir}/mpich-%{_arch}/
%{_libdir}/mpich/lib/libscalapack.so
%{_libdir}/mpich/lib/pkgconfig/scalapack.pc

%files mpich-static
%{_libdir}/mpich/lib/libscalapack.a
%endif

%if %{with openmpi}
%files openmpi
%{_libdir}/openmpi/lib/libscalapack.so.2.2
%{_libdir}/openmpi/lib/libscalapack.so.2.2.2

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}/
%{_libdir}/openmpi/lib/libscalapack.so
%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc

%files openmpi-static
%{_libdir}/openmpi/lib/libscalapack.a
%endif

%if %{with openmpi3}
%files openmpi3
%{_libdir}/openmpi3/lib/libscalapack.so.2.2
%{_libdir}/openmpi3/lib/libscalapack.so.2.2.2

%files openmpi3-devel
%{_includedir}/openmpi3-%{_arch}/
%{_libdir}/openmpi3/lib/libscalapack.so
%{_libdir}/openmpi3/lib/pkgconfig/scalapack.pc

%files openmpi3-static
%{_libdir}/openmpi3/lib/libscalapack.a
%endif

%changelog
* Tue Aug  5 2025 Tom Callaway <spot@fedoraproject.org> - 2.2.2-5
- conditionalize use of %_cmake_lib_suffix64 so we don't try to use it on i686

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 14 2025 David Bold <davidsch@fedoraproject.org> - 2.2.2-3
- Do not glob soname

* Mon Mar 10 2025 Tom Callaway <spot@fedoraproject.org> - 2.2.2-2
- more .pc fixes

* Mon Mar  3 2025 Tom Callaway <spot@fedoraproject.org> - 2.2.2-1
- update to 2.2.2
- fix hardcoded versioning (with sed, not patch)
- fixup .pc file
- fix old minimum cmake version which breaks the build

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul  1 2024 Tom Callaway <spot@fedoraproject.org> - 2.2.0-9
- fix license tag (thanks to Diaeresis)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 29 2023 Orion Poplawski <orion@nwra.com> - 2.2.0-7
- Rebuild for openmpi 5.0.0, drops support for i686

* Wed Aug 16 2023 Florian Weimer <fweimer@redhat.com> - 2.2.0-6
- Set build_type_safety_c to 0 (#2178710)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 15 2023 Arjun Shankar <arjun@redhat.com> - 2.2.0-4
- Build in C89 mode (#2178710)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Tom Callaway <spot@fedoraproject.org> 2.2.0-1
- update to 2.2.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Björn Esser <besser82@fedoraproject.org> - 2.1.0-9
- Properly set BLA_VENDOR to FlexiBLAS for cmake >= 3.19

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 28 2020 Iñaki Úcar <iucar@fedoraproject.org> - 2.1.0-7
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Thu Aug  6 2020 Tom Callaway <spot@fedoraproject.org> - 2.1.0-6
- use new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 17 2020 Tom Callaway <spot@fedoraproject.org> - 2.1.0-3
- fix openmpi .pc file

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Tom Callaway <spot@fedoraproject.org> - 2.1.0-1
- update to 2.1.0

* Sun Nov 17 2019 Tom Callaway <spot@fedoraproject.org> - 2.1-1
- update to 2.1

* Tue Sep 17 2019 Dave love <loveshack@fedoraproject.org> - 2.0.2-31
- Don't BR lapack with openblas (#1753250)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 12 2019 Tom Callaway <spot@fedoraproject.org> - 2.0.2-29
- add openmpi3 subpackaging for epel7

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 2.0.2-28
- Rebuild for openmpi 3.1.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.0.2-24
- Rebuilt for GCC-8.0.1.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.2-21
- Rebuild for libgfortran.so.4

* Tue Nov 29 2016 Dan Horák <dan[at]danny.cz> - 2.0.2-20
- still use blas if openblas is not available

* Mon Nov 28 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.2-19
- build against openblas

* Tue Oct 25 2016 Dan Horák <dan[at]danny.cz> - 2.0.2-18
- enable build on s390(x) and fix the logic for alt-arches in Fedora

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.2-17
- Rebuild for openmpi 2.0

* Fri Aug 26 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.2-16
- conditionalize mpich cases on old rhel arches

* Thu Jul 28 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.2-15
- fix scalapack shared library to properly have blacs inside it
- add explicit openmpi/mpich requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.2-13
- use global instead of define

* Tue Jan 19 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.2-12
- Make blacs-openmpi require blacs-common (bug #1299939)

* Mon Jan 18 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.2-11.1
- inherit fixes from master branch into epel7
- rebuild against current libmpi in epel7

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0.2-11
- Rebuild for openmpi 1.10.0

* Sat Aug 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.2-10
- Rebuild for MPI provides

* Sun Jul 26 2015 Sandro Mani <manisandro@gmail.com> - 2.0.2-9
- Rebuild for RPM MPI Requires Provides Change

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Mar 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 2.0.2-7
- Rebuild for changed mpich libraries

* Thu Dec 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.2-6
- add missing functions (thanks to d.love<at>liverpool.ac.uk)

* Thu Sep  4 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.0.2-5
- rebuild for changed library inside openmpi (#1135728)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  1 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.2-3
- explictly link to other dependent libs

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 3 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.2-1
- update to 2.0.2
- subpackage blacs

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Deji Akingunola <dakingun@gmail.com> - 1.7.5-19
- Rename mpich2 sub-packages to mpich and rebuild for mpich-3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Tom Callaway <spot@fedoraproject.org> - 1.7.5-17
- rebuild for new mpich2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 03 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.7.5-14
- Bump spec.

* Wed Aug 03 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.7.5-13
- Honor MPI guidelines wrt placement of libraries.
- Drop unnecessary module file.
- A few rpmlint fixes.

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 1.7.5-12
- Rebuild for mpich2 soname bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Deji Akingunola <dakingun@gmail.com> - 1.7.5-11
- Rebuild for both mpich2 and openmpi updates

* Wed Jul  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.5-10
- Move all BuildRequires to the top of the spec file
- -static packages now Require matching -devel package, they're not very useful otherwise

* Tue Dec 15 2009 Deji Akingunola <dakingun@gmail.com> - 1.7.5-9
- Buildrequire mpich2-devel-static

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.5-8
- drop lam support (Provides/Obsoletes by mpich2, which is a hack, but something's gotta do it)
- move static libs to static subpackages (resolves bz 545150)

* Thu Aug  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.5-7
- rework package to handle all supported MPI environments in Fedora

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-4
- incorporate Deji Akingunola's changes (bz 462424)
- build against openmpi instead of lam

* Tue Jul  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-3
- fix compile against new lam paths

* Wed Feb 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-2
- rebuild for new gcc

* Mon Aug 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-1.1
- rebuild for BuildID

* Thu Jan 18 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-1
- bump to 1.7.5

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-4
- I said "BR" not "R". Stupid packager.

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-3
- fix BR: lam-devel

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-2
- fix 64bit patch

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-1
- bump to 1.7.4

* Wed Mar  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-13
- lam moved into _libdir/lam... need to fix patches

* Wed Mar  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-12
- set -fPIC as NOOPT

* Sun Feb 26 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-11
- fix 64 bit builds
- enable shared libraries
- split package into base and devel

* Tue Feb 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-10
- Incorporate Andrew Gormanly's fixes

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-9
- fix BR

* Mon Dec 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-8
- rebuild for gcc4.1

* Sun May 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-7
- 64 bit library fix

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-6
- remove hardcoded dist tags

* Sun May  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-4
- fix broken patch for fc-3 branch

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-3
- use dist tag
- fix fc3 BuildRequires

* Tue Apr 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-2
- fix buildroot
- add gcc-gfortran to BuildRequires (gcc-g77 for fc3)

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-1
- initial package creation
