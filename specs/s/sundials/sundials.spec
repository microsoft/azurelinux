## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

## Debug builds?
%bcond_with debug
#

# Enable pthread support
%bcond_with pthread
#

#define _legacy_common_support 1
#https://github.com/LLNL/sundials/issues/97
%define _lto_cflags %{nil}

%global with_mpich 1
%if 0%{?fedora} >= 40
%ifarch %{ix86}
%global with_openmpi 0
%else
%global with_openmpi 1
%endif
%else
%global with_openmpi 1
%endif
%if 0%{?flatpak}
%global with_mpich 0
%global with_openmpi 0
%endif

## BLAS ##
%if 0%{?fedora} || 0%{?rhel} >= 9
%global blaslib flexiblas
%global blasvar %{nil}
%else
%global blaslib openblas
%global blasvar o
%endif
###########

%global with_hypre 1
%ifarch x86_64
%global with_openmpicheck 1
%global with_mpichcheck 0
%endif
###########
%global with_sercheck 1

## PETSc ##
%global with_petsc 1
###########

## SuperLUMT ##
%global with_superlumt 1
###########

## superlu_dist ##
%global with_superludist 0
###########

%if 0%{?rhel} && 0%{?rhel} >= 9
# KLU support
%global with_klu   1
%global with_klu64 1
##########
# Fortran
%if 0%{?with_klu64}
%global with_fortran 1
%endif
%if 0%{?with_klu}
%global with_fortran 0
%endif
##########
%endif
%if 0%{?fedora}
%ifarch s390x x86_64 %{power64} aarch64 riscv64
%global with_klu64 1
%global with_fortran 1
%endif
%ifarch %{arm} %{ix86}
%global with_klu 1
%global with_fortran 0
%endif
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
%global with_klu 1
%global with_fortran 0
%endif
##########
# SOVERSIONs (*_SOVERSION from CMakeLists.txt):
%global arkodelib_SOVERSION 6
%global cvodelib_SOVERSION 7
%global cvodeslib_SOVERSION 7
%global idalib_SOVERSION 7
%global idaslib_SOVERSION 6
%global kinsollib_SOVERSION 7
#global cpodeslib_SOVERSION 0
%global nveclib_SOVERSION 7
%global sunmatrixlib_SOVERSION 5
%global sunlinsollib_SOVERSION 5
%global sunnonlinsollib_SOVERSION 4
%global sundialslib_SOVERSION 7

Summary:    Suite of nonlinear solvers
Name:       sundials
Version:    7.3.0
Release:    %autorelease
License:    BSD-3-Clause
URL:        https://computation.llnl.gov/projects/%{name}/
Source0:    https://github.com/LLNL/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

# This patch rename superLUMT library
Patch0:     %{name}-5.5.0-set_superlumt_name.patch

# This patch rename superLUMT64 library
Patch1:     %{name}-5.5.0-set_superlumt64_name.patch

Patch2:     %{name}-change_petsc_variable.patch
Patch3:     %{name}-klu64.patch

BuildRequires: make
%if 0%{?with_fortran}
BuildRequires: gcc-gfortran
%endif
BuildRequires: python3-devel
BuildRequires: gcc, gcc-c++
%if 0%{?epel}
BuildRequires: epel-rpm-macros
%endif
BuildRequires: cmake >= 3.10
BuildRequires: %{blaslib}-devel
%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64 riscv64
BuildRequires: SuperLUMT64-devel
%endif
%ifarch %{arm} %{ix86}
BuildRequires: SuperLUMT-devel
%endif
%endif

# KLU support
%if 0%{?with_klu64}
BuildRequires: suitesparse64-devel
%endif
%if 0%{?with_klu}
BuildRequires: suitesparse-devel
%endif
##########

%if 0%{?with_fortran}
BuildRequires: gcc-gfortran%{?_isa}
%endif

%description
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.

SUNDIALS was implemented with the goal of providing robust time integrators
and nonlinear solvers that can easily be incorporated into existing simulation
codes. The primary design goals were to require minimal information from the
user, allow users to easily supply their own data structures underneath the
solvers, and allow for easy incorporation of user-supplied linear solvers and
preconditioners. 

%package devel
Summary:    Suite of nonlinear solvers (developer files)
Requires:   %{name}%{?_isa} = %{version}-%{release}
Provides:   %{name}-fortran-static = %{version}-%{release}
%description devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the developer files (.so file, header files).
#############################################################################
#########
%if 0%{?with_openmpi}
%package openmpi
Summary:    Suite of nonlinear solvers
BuildRequires: openmpi-devel
BuildRequires: hypre-openmpi-devel
%if 0%{?with_petsc}
BuildRequires: petsc-openmpi-devel >= 3.10
BuildRequires: scalapack-openmpi-devel
BuildRequires: hdf5-openmpi-devel
%endif
%if 0%{?with_superludist}
BuildRequires: superlu_dist-openmpi-devel
%endif

%if 0%{?with_fortran}
BuildRequires: gcc-gfortran%{?_isa}
%endif

%description openmpi
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel OpenMPI libraries.

%package openmpi-devel
Summary:    Suite of nonlinear solvers
Requires:   %{name}-openmpi%{?_isa} = %{version}-%{release}
Provides:   %{name}-openmpi-fortran-static = %{version}-%{release}
%description openmpi-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel OpenMPI devel libraries and
header files.

%if 0%{?with_fortran}
Requires: gcc-gfortran%{?_isa}
%endif

%endif
######
###############################################################################
######
%if 0%{?with_mpich}
%package mpich
Summary:    Suite of nonlinear solvers
BuildRequires: mpich-devel
BuildRequires: hypre-mpich-devel
%if 0%{?with_petsc}
BuildRequires: petsc-mpich-devel >= 3.10
BuildRequires: scalapack-mpich-devel
BuildRequires: hdf5-mpich-devel
%endif
%if 0%{?with_superludist}
BuildRequires: superlu_dist-mpich-devel
%endif

%if 0%{?with_fortran}
BuildRequires: gcc-gfortran%{?_isa}
%endif

%description mpich
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH libraries.

%package mpich-devel
Summary:    Suite of nonlinear solvers
Requires:   %{name}-mpich%{?_isa} = %{version}-%{release}
Provides:   %{name}-mpich-fortran-static = %{version}-%{release}
%description mpich-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH devel libraries and
header files.

%if 0%{?with_fortran}
Requires: gcc-gfortran%{?_isa}
%endif

%endif
######
#############################################################################

%package doc
Summary:    Suite of nonlinear solvers (documentation)
BuildArch: noarch
Obsoletes: sundials-doc < 0:6.6.2-5
%description doc
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the documentation files.

%prep
%setup -qc

pushd %{name}-%{version}

%ifarch s390x x86_64 %{power64} aarch64 riscv64
%patch 1 -p0 -b .set_superlumt64_name
%endif
%ifarch %{arm} %{ix86}
%patch 0 -p0 -b .set_superlumt_name
%endif

%if 0%{?with_klu64}
%patch 3 -p1 -b .klu64
%endif

mv src/arkode/README.md src/README-arkode.md
mv src/cvode/README.md src/README-cvode.md
mv src/cvodes/README.md src/README-cvodes.md
mv src/ida/README.md src/README-ida.md
mv src/idas/README.md src/README.idas.md
mv src/kinsol/README.md src/README-kinsol.md
popd

%if 0%{?with_openmpi}
cp -a sundials-%{version} buildopenmpi_dir
%endif
%if 0%{?with_mpich}
cp -a sundials-%{version} buildmpich_dir
%endif

%build

%global _smp_ncpus_max 1

mkdir -p sundials-%{version}/build

export LIBBLASLINK=-l%{blaslib}%{blasvar}
export INCBLAS=%{_includedir}/%{blaslib}

%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64 riscv64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%endif


%if %{with debug}
%undefine _hardened_build
export CFLAGS=" -fPIC"
export FFLAGS=" -fPIC"
export FCFLAGS=" -fPIC"
%{_bindir}/cmake -B sundials-%{version}/build -S sundials-%{version} \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_CXX_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK" \
%else
export CFLAGS="%{build_cflags}"
export FFLAGS="%{build_fflags} -fPIC"
%cmake -B sundials-%{version}/build -S sundials-%{version} \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
%endif
%if 0%{?with_klu64}
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu64.so \
 -DAMD_LIBRARY=%{_libdir}/libamd64.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf64.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd64.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%endif
%if 0%{?with_klu}
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu.so \
 -DAMD_LIBRARY=%{_libdir}/libamd.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%endif
 -DSUNDIALS_BUILD_WITH_PROFILING:BOOL=OFF \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK" \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
 -DLAPACK_ENABLE:BOOL=OFF \
 -DCMAKE_MODULE_LINKER_FLAGS:STRING="%{__global_ldflags}" \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python3} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=ON \
 -DMPI_ENABLE:BOOL=OFF \
%if 0%{?with_fortran}
 -DF77_INTERFACE_ENABLE:BOOL=ON \
 -DEXAMPLES_ENABLE_F77:BOOL=ON \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DF2003_INTERFACE_ENABLE:BOOL=ON \
%endif
 -DEXAMPLES_ENABLE_F90:BOOL=ON \
 -DFortran_INSTALL_MODDIR:PATH=%{_fmoddir}/%{name} \
%endif
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
%if %{with pthread}
 -DPTHREAD_ENABLE:BOOL=ON \
%endif
 -DSUNDIALS_PRECISION:STRING=double \
%if 0%{?with_superlumt}
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
 -DSUPERLUDIST_ENABLE:BOOL=OFF \
 -DHYPRE_ENABLE:BOOL=OFF \
 -DEXAMPLES_INSTALL:BOOL=OFF \
 -DSUNDIALS_BUILD_WITH_MONITORING:BOOL=ON -Wno-dev

%define _vpath_builddir sundials-%{version}/build
%cmake_build

#############################################################################
#######
%if 0%{?with_openmpi}

mkdir -p buildopenmpi_dir/build
%{_openmpi_load}

## Blas
export LIBBLASLINK=-l%{blaslib}%{blasvar}
export INCBLAS=%{_includedir}/%{blaslib}
##

## SuperLUMT
%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64 riscv64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%endif

## Hypre
%if 0%{?with_hypre}
export LIBHYPRELINK="-L$MPI_LIB -lHYPRE"
%endif
##

# Force MPI compilers
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
%if 0%{?fedora}
export FC=$MPI_BIN/mpifort
%else
export FC=$MPI_BIN/mpif77
%endif
##

%if %{with debug}
%undefine _hardened_build
export CFLAGS=" -fPIC"
export FFLAGS=" -fPIC"
export FCFLAGS=" -fPIC"
%{_bindir}/cmake -B buildopenmpi_dir/build -S buildopenmpi_dir \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_CXX_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%else
export CFLAGS="%{build_cflags}"
export FFLAGS="%{build_fflags} -fPIC"
%cmake -B buildopenmpi_dir/build -S buildopenmpi_dir \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
%endif
%if 0%{?with_klu64}
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu64.so \
 -DAMD_LIBRARY=%{_libdir}/libamd64.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf64.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd64.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
 -DPETSC_ENABLE:BOOL=OFF \
%endif
%if 0%{?with_klu}
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu.so \
 -DAMD_LIBRARY=%{_libdir}/libamd.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%if 0%{?with_petsc}
 -DPETSC_ENABLE:BOOL=ON \
 -DPETSC_INCLUDES:PATH=$MPI_INCLUDE/petsc \
 -DPETSC_LIBRARIES:PATH=$MPI_LIB/libpetsc.so \
 -DPETSC_EXECUTABLE_RUNS:BOOL=ON \
%endif
%endif
 -DSUNDIALS_BUILD_WITH_PROFILING:BOOL=OFF \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
 -DMPI_INCLUDE_PATH:PATH=$MPI_INCLUDE \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE \
 -DLAPACK_ENABLE:BOOL=OFF \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}/openmpi/lib \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python3} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=ON \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
%if 0%{?with_fortran}
%if 0%{?fedora}
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpifort \
%else
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpif77 \
%endif
 -DF77_INTERFACE_ENABLE:BOOL=ON \
 -DEXAMPLES_ENABLE_F77:BOOL=ON \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DF2003_INTERFACE_ENABLE:BOOL=ON \
%endif
 -DEXAMPLES_ENABLE_F90:BOOL=ON \
 -DFortran_INSTALL_MODDIR:PATH=$MPI_FORTRAN_MOD_DIR/%{name} \
%endif
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
%if %{with pthread}
 -DPTHREAD_ENABLE:BOOL=ON \
%endif
%if 0%{?with_superlumt}
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
%if 0%{?with_superludist}
 -DSUPERLUDIST_ENABLE:BOOL=ON \
 -DSUPERLUDIST_INCLUDE_DIR:PATH=$MPI_INCLUDE/superlu_dist \
 -DSUPERLUDIST_LIBRARY_DIR:PATH=$MPI_LIB \
 -DSUPERLUDIST_LIBRARIES:STRING=libsuperlu_dist.so \
%endif
%if 0%{?with_hypre}
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=$MPI_INCLUDE/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DEXAMPLES_INSTALL:BOOL=OFF \
 -DSUNDIALS_BUILD_WITH_MONITORING:BOOL=ON -Wno-dev

%define _vpath_builddir buildopenmpi_dir/build
%cmake_build
%{_openmpi_unload}
%endif
######
###########################################################################

%if 0%{?with_mpich}

mkdir -p buildmpich_dir/build
%{_mpich_load}

## Blas
export LIBBLASLINK=-l%{blaslib}%{blasvar}
export INCBLAS=%{_includedir}/%{blaslib}
##

## SuperLUMT
%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64 riscv64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%endif

## Hypre
%if 0%{?with_hypre}
export LIBHYPRELINK="-L$MPI_LIB -lHYPRE"
%endif
##

# Force MPI compilers
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
%if 0%{?fedora}
export FC=$MPI_BIN/mpifort
%else
export FC=$MPI_BIN/mpif77
%endif
##

%if %{with debug}
%undefine _hardened_build
export CFLAGS=" -fPIC"
export FFLAGS=" -fPIC"
export FCFLAGS=" -fPIC"
%{_bindir}/cmake -B buildmpich_dir/build -S buildmpich_dir \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_CXX_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%else
export CFLAGS="%{build_cflags}"
export FFLAGS="%{build_fflags} -fPIC"
%cmake -B buildmpich_dir/build -S buildmpich_dir \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
%endif
%if 0%{?with_klu64}
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu64.so \
 -DAMD_LIBRARY=%{_libdir}/libamd64.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf64.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd64.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
 -DPETSC_ENABLE:BOOL=OFF \
%endif
%if 0%{?with_klu}
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu.so \
 -DAMD_LIBRARY=%{_libdir}/libamd.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%if 0%{?with_petsc}
 -DPETSC_ENABLE:BOOL=ON \
 -DPETSC_INCLUDES:PATH=$MPI_INCLUDE/petsc \
 -DPETSC_LIBRARIES:PATH=$MPI_LIB/libpetsc.so \
 -DPETSC_EXECUTABLE_RUNS:BOOL=ON \
%endif
%endif
 -DSUNDIALS_BUILD_WITH_PROFILING:BOOL=OFF \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
 -DLAPACK_ENABLE:BOOL=OFF \
 -DMPI_INCLUDE_PATH:PATH=$MPI_INCLUDE \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}/mpich/lib \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python3} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=ON \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
%if 0%{?with_fortran}
%if 0%{?fedora}
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpifort \
%else
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpif77 \
%endif
 -DF77_INTERFACE_ENABLE:BOOL=ON \
 -DEXAMPLES_ENABLE_F77:BOOL=ON \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DF2003_INTERFACE_ENABLE:BOOL=ON \
%endif
 -DEXAMPLES_ENABLE_F90:BOOL=ON \
 -DFortran_INSTALL_MODDIR:PATH=$MPI_FORTRAN_MOD_DIR/%{name} \
%endif
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
%if %{with pthread}
 -DPTHREAD_ENABLE:BOOL=ON \
%endif
%if 0%{?with_superlumt}
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
%if 0%{?with_superludist}
 -DSUPERLUDIST_ENABLE:BOOL=ON \
 -DSUPERLUDIST_INCLUDE_DIR:PATH=$MPI_INCLUDE/superlu_dist \
 -DSUPERLUDIST_LIBRARY_DIR:PATH=$MPI_LIB \
 -DSUPERLUDIST_LIBRARIES:STRING=libsuperlu_dist.so \
%endif
%if 0%{?with_hypre}
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=$MPI_INCLUDE/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DEXAMPLES_INSTALL:BOOL=OFF \
 -DSUNDIALS_BUILD_WITH_MONITORING:BOOL=ON -Wno-dev

%define _vpath_builddir buildmpich_dir/build
%cmake_build
%{_mpich_unload}
%endif
######
#############################################################################

%install
%if 0%{?with_openmpi}
%{_openmpi_load}
%define _vpath_builddir buildopenmpi_dir/build
%cmake_install
rm -f %{buildroot}$MPI_INCLUDE/sundials/LICENSE
rm -f %{buildroot}$MPI_INCLUDE/sundials/NOTICE
%{_openmpi_unload}
%endif

%if 0%{?with_mpich}
%{_mpich_load}
%define _vpath_builddir buildmpich_dir/build
%cmake_install
rm -f %{buildroot}$MPI_INCLUDE/sundials/LICENSE
rm -f %{buildroot}$MPI_INCLUDE/sundials/NOTICE
%{_mpich_unload}
%endif

%define _vpath_builddir sundials-%{version}/build
%cmake_install

# Remove files in bad position
rm -f %{buildroot}%{_prefix}/LICENSE
rm -f %{buildroot}%{_includedir}/sundials/LICENSE
rm -f %{buildroot}%{_includedir}/sundials/NOTICE

%check
%if 0%{?with_openmpi}
%if 0%{?with_openmpicheck}
%{_openmpi_load}
%define _vpath_builddir buildopenmpi_dir/build
%if %{with debug}
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
%ctest -- -VV --output-on-failure --debug
%else
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
%ctest -E 'test_sunlinsol_superlumt'
%endif
%{_openmpi_unload}
%endif
## if with_openmpicheck
%endif
## if with_openmpi

%if 0%{?with_mpich}
%if 0%{?with_mpichcheck}
%{_mpich_load}
%define _vpath_builddir buildmpich_dir/build
%if %{with debug}
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
%ctest -- -VV --output-on-failure --debug
%else
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
%ctest -E 'test_sunlinsol_superlumt'
%endif
%{_mpich_unload}
%endif
## if with_mpichcheck
%endif
## if with_mpich

%if 0%{?with_sercheck}
%define _vpath_builddir sundials-%{version}/build
%if %{with debug}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_libdir}
%ctest -- -VV --output-on-failure --debug
%else
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_libdir}
%ctest -E 'test_sunlinsol_superlumt'
%endif
%endif
## if with_sercheck

%files
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/src/README-arkode.md
%doc sundials-%{version}/src/README-cvode.md
%doc sundials-%{version}/src/README-cvodes.md
%doc sundials-%{version}/src/README-ida.md
%doc sundials-%{version}/src/README.idas.md
%doc sundials-%{version}/src/README-kinsol.md
%doc sundials-%{version}/NOTICE
%{_libdir}/libsundials_core.so.%{sundialslib_SOVERSION}*
%{_libdir}/libsundials_arkode*.so.%{arkodelib_SOVERSION}*
%{_libdir}/libsundials_cvode*.so.%{cvodelib_SOVERSION}*
%{_libdir}/libsundials_ida.so.%{idalib_SOVERSION}*
%{_libdir}/libsundials_idas.so.%{idaslib_SOVERSION}*
%{_libdir}/libsundials_kinsol.so.%{kinsollib_SOVERSION}*
%{_libdir}/libsundials_nvecopenmp.so.%{nveclib_SOVERSION}*
%{_libdir}/libsundials_nvecmanyvector.so.%{nveclib_SOVERSION}*
%if %{with pthread}
%{_libdir}/libsundials_nvecpthreads.so.%{nveclib_SOVERSION}*
%endif
%{_libdir}/libsundials_nvecserial.so.%{nveclib_SOVERSION}*
%{_libdir}/libsundials_sunlinsol*.so.%{sunlinsollib_SOVERSION}*
%{_libdir}/libsundials_sunmatrix*.so.%{sunmatrixlib_SOVERSION}*
%{_libdir}/libsundials_sunnonlinsol*.so.%{sunnonlinsollib_SOVERSION}*
%if 0%{?with_fortran}
%{_libdir}/libsundials_f*[_mod].so.*
%endif

%files devel
%{_libdir}/*.a
%{_libdir}/libsundials_core.so
%{_libdir}/libsundials_ida*.so
%{_libdir}/libsundials_cvode*.so
%{_libdir}/libsundials_arkode*.so
%{_libdir}/libsundials_kinsol.so
%{_libdir}/libsundials_nvecserial.so
%{_libdir}/libsundials_nvecopenmp.so
%{_libdir}/libsundials_nvecmanyvector.so
%{_libdir}/cmake/sundials/
%if %{with pthread}
%{_libdir}/libsundials_nvecpthreads.so
%endif
%{_libdir}/libsundials_sunmatrix*.so
%{_libdir}/libsundials_sunlinsol*.so
%{_libdir}/libsundials_sunnonlinsol*.so
%if 0%{?with_fortran}
%{_libdir}/libsundials_f*[_mod].so
%{_fmoddir}/%{name}/
%if %{with pthread}
%{_libdir}/libsundials_fnvecpthreads.so
%endif
%if 0%{?with_superlumt}
%{_libdir}/libsundials_sunlinsolsuperlumt.so
%endif
%endif
%{_includedir}/nvector/
%{_includedir}/sunmatrix/
%{_includedir}/sunadjointcheckpointscheme/
%{_includedir}/sunnonlinsol/
%{_includedir}/sunlinsol/
%{_includedir}/sunadaptcontroller/
%{_includedir}/sunmemory/
%{_includedir}/arkode/
%{_includedir}/cvode/
%{_includedir}/cvodes/
%{_includedir}/ida/
%{_includedir}/idas/
%{_includedir}/kinsol/
%dir %{_includedir}/sundials
%{_includedir}/sundials/priv/
%{_includedir}/sundials/sundials_adjointcheckpointscheme.h
%{_includedir}/sundials/sundials_adjointstepper.h
%{_includedir}/sundials/sundials_stepper.h
%{_includedir}/sundials/sundials_export.h
%{_includedir}/sundials/sundials_band.h
%{_includedir}/sundials/sundials_dense.h
%{_includedir}/sundials/sundials_direct.h
%{_includedir}/sundials/sundials_futils.h
%{_includedir}/sundials/sundials_iterative.h
%{_includedir}/sundials/sundials_linearsolver.h
%{_includedir}/sundials/sundials_math.h
%{_includedir}/sundials/sundials_matrix.h
%{_includedir}/sundials/sundials_memory.h
%{_includedir}/sundials/sundials_nonlinearsolver.h
%{_includedir}/sundials/sundials_mpi_types.h
%{_includedir}/sundials/sundials_nvector.h
%{_includedir}/sundials/sundials_types.h
%{_includedir}/sundials/sundials_version.h
%{_includedir}/sundials/sundials_config.h
%{_includedir}/sundials/sundials_base.hpp
%{_includedir}/sundials/sundials_context.h
%{_includedir}/sundials/sundials_context.hpp
%{_includedir}/sundials/sundials_convertibleto.hpp
%{_includedir}/sundials/sundials_linearsolver.hpp
%{_includedir}/sundials/sundials_logger.h
%{_includedir}/sundials/sundials_matrix.hpp
%{_includedir}/sundials/sundials_memory.hpp
%{_includedir}/sundials/sundials_nonlinearsolver.hpp
%{_includedir}/sundials/sundials_nvector.hpp
%{_includedir}/sundials/sundials_profiler.h
%{_includedir}/sundials/sundials_adaptcontroller.h
%{_includedir}/sundials/sundials_profiler.hpp
%{_includedir}/sundials/sundials_core.h*
%{_includedir}/sundials/sundials_errors.h
%{_includedir}/sundials/sundials_types_deprecated.h

%if 0%{?with_openmpi}
%files openmpi
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/src/README-arkode.md
%doc sundials-%{version}/src/README-cvode.md
%doc sundials-%{version}/src/README-cvodes.md
%doc sundials-%{version}/src/README-ida.md
%doc sundials-%{version}/src/README.idas.md
%doc sundials-%{version}/src/README-kinsol.md
%doc sundials-%{version}/NOTICE
%{_libdir}/openmpi/lib/libsundials_nvecparallel.so.*
%{_libdir}/openmpi/lib/libsundials_nvecparhyp.so.*
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/openmpi/lib/libsundials_nvecpetsc.so.*
%{_libdir}/openmpi/lib/libsundials_sunnonlinsolpetscsnes.so.*
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/openmpi/lib/libsundials_nvecmpipthreads.so.*
%endif
%{_libdir}/openmpi/lib/libsundials_nvecmpiplusx.so.*
%{_libdir}/openmpi/lib/libsundials_core.so.*
%{_libdir}/openmpi/lib/libsundials_kinsol.so.*
%{_libdir}/openmpi/lib/libsundials_ida*.so.*
%{_libdir}/openmpi/lib/libsundials_cvode*.so.*
%{_libdir}/openmpi/lib/libsundials_arkode*.so.*
%{_libdir}/openmpi/lib/libsundials_nvecserial.so.*
%{_libdir}/openmpi/lib/libsundials_nvecopenmp.so.*
%{_libdir}/openmpi/lib/libsundials_sunmatrix*.so.*
%{_libdir}/openmpi/lib/libsundials_sunlinsol*.so.*
%{_libdir}/openmpi/lib/libsundials_sunnonlinsol*.so.*
%{_libdir}/openmpi/lib/libsundials_nvecmanyvector.so.*
%{_libdir}/openmpi/lib/libsundials_nvecmpimanyvector.so.*
%if %{with pthread}
%{_libdir}/openmpi/lib/libsundials_nvecpthreads.so.*
%endif
%if 0%{?with_fortran}
%{_libdir}/openmpi/lib/libsundials_f*[_mod].so.*
%endif

%files openmpi-devel
%{_libdir}/openmpi/lib/*.a
%{_includedir}/openmpi-%{_arch}/nvector/
%{_includedir}/openmpi-%{_arch}/sundials/
%{_includedir}/openmpi-%{_arch}/arkode/
%{_includedir}/openmpi-%{_arch}/cvode/
%{_includedir}/openmpi-%{_arch}/cvodes/
%{_includedir}/openmpi-%{_arch}/ida/
%{_includedir}/openmpi-%{_arch}/idas/
%{_includedir}/openmpi-%{_arch}/kinsol/
%{_includedir}/openmpi-%{_arch}/sunadjointcheckpointscheme/
%{_includedir}/openmpi-%{_arch}/sunlinsol/
%{_includedir}/openmpi-%{_arch}/sunmatrix/
%{_includedir}/openmpi-%{_arch}/sunnonlinsol/
%{_includedir}/openmpi-%{_arch}/sunmemory/
%{_includedir}/openmpi-%{_arch}/sunadaptcontroller/
%if 0%{?with_fortran}
%{_fmoddir}/openmpi/%{name}/
%{_libdir}/openmpi/lib/libsundials_f*[_mod].so
%endif
%{_libdir}/openmpi/lib/libsundials_nvecparallel.so
%{_libdir}/openmpi/lib/libsundials_nvecparhyp.so
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/openmpi/lib/libsundials_nvecpetsc.so
%{_libdir}/openmpi/lib/libsundials_sunnonlinsolpetscsnes.so
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/openmpi/lib/libsundials_nvecmpipthreads.so
%{_libdir}/openmpi/lib/libsundials_nvecpthreads.so
%endif
%{_libdir}/openmpi/lib/libsundials_nvecmpiplusx.so
%{_libdir}/openmpi/lib/libsundials_core.so
%{_libdir}/openmpi/lib/libsundials_kinsol.so
%{_libdir}/openmpi/lib/libsundials_ida*.so
%{_libdir}/openmpi/lib/libsundials_cvode*.so
%{_libdir}/openmpi/lib/libsundials_arkode*.so
%{_libdir}/openmpi/lib/libsundials_nvecserial.so
%{_libdir}/openmpi/lib/libsundials_nvecopenmp.so
%{_libdir}/openmpi/lib/libsundials_sunmatrix*.so
%{_libdir}/openmpi/lib/libsundials_sunlinsol*.so
%{_libdir}/openmpi/lib/libsundials_sunnonlinsol*.so
%{_libdir}/openmpi/lib/libsundials_nvecmanyvector.so
%{_libdir}/openmpi/lib/libsundials_nvecmpimanyvector.so
%{_libdir}/openmpi/lib/cmake/sundials/
%endif

%if 0%{?with_mpich}
%files mpich
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/src/README-arkode.md
%doc sundials-%{version}/src/README-cvode.md
%doc sundials-%{version}/src/README-cvodes.md
%doc sundials-%{version}/src/README-ida.md
%doc sundials-%{version}/src/README.idas.md
%doc sundials-%{version}/src/README-kinsol.md
%doc sundials-%{version}/NOTICE
%{_libdir}/mpich/lib/libsundials_nvecparallel.so.*
%{_libdir}/mpich/lib/libsundials_nvecparhyp.so.*
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/mpich/lib/libsundials_nvecpetsc.so.*
%{_libdir}/mpich/lib/libsundials_sunnonlinsolpetscsnes.so.*
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/mpich/lib/libsundials_nvecmpipthreads.so.*
%endif
%{_libdir}/mpich/lib/libsundials_nvecmpiplusx.so.*
%{_libdir}/mpich/lib/libsundials_core.so.*
%{_libdir}/mpich/lib/libsundials_kinsol.so.*
%{_libdir}/mpich/lib/libsundials_ida*.so.*
%{_libdir}/mpich/lib/libsundials_cvode*.so.*
%{_libdir}/mpich/lib/libsundials_arkode*.so.*
%{_libdir}/mpich/lib/libsundials_nvecserial.so.*
%{_libdir}/mpich/lib/libsundials_nvecopenmp.so.*
%{_libdir}/mpich/lib/libsundials_sunmatrix*.so.*
%{_libdir}/mpich/lib/libsundials_sunlinsol*.so.*
%{_libdir}/mpich/lib/libsundials_sunnonlinsol*.so.*
%{_libdir}/mpich/lib/libsundials_nvecmanyvector.so.*
%{_libdir}/mpich/lib/libsundials_nvecmpimanyvector.so.*
%if %{with pthread}
%{_libdir}/mpich/lib/libsundials_nvecpthreads.so.*
%endif
%if 0%{?with_fortran}
%{_libdir}/mpich/lib/libsundials_f*[_mod].so.*
%endif


%files mpich-devel
%{_includedir}/mpich-%{_arch}/nvector/
%{_includedir}/mpich-%{_arch}/sundials/
%{_includedir}/mpich-%{_arch}/arkode/
%{_includedir}/mpich-%{_arch}/cvode/
%{_includedir}/mpich-%{_arch}/cvodes/
%{_includedir}/mpich-%{_arch}/ida/
%{_includedir}/mpich-%{_arch}/idas/
%{_includedir}/mpich-%{_arch}/kinsol/
%{_includedir}/mpich-%{_arch}/sunadjointcheckpointscheme/
%{_includedir}/mpich-%{_arch}/sunlinsol/
%{_includedir}/mpich-%{_arch}/sunmatrix/
%{_includedir}/mpich-%{_arch}/sunnonlinsol/
%{_includedir}/mpich-%{_arch}/sunmemory/
%{_includedir}/mpich-%{_arch}/sunadaptcontroller/
%if 0%{?with_fortran}
%{_fmoddir}/mpich/%{name}/
%{_libdir}/mpich/lib/libsundials_f*[_mod].so
%endif
%{_libdir}/mpich/lib/*.a
%{_libdir}/mpich/lib/libsundials_nvecparallel.so
%{_libdir}/mpich/lib/libsundials_nvecparhyp.so
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/mpich/lib/libsundials_nvecpetsc.so
%{_libdir}/mpich/lib/libsundials_sunnonlinsolpetscsnes.so
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/mpich/lib/libsundials_nvecmpipthreads.so
%{_libdir}/mpich/lib/libsundials_nvecpthreads.so
%endif
%{_libdir}/mpich/lib/libsundials_nvecmpiplusx.so
%{_libdir}/mpich/lib/libsundials_core.so
%{_libdir}/mpich/lib/libsundials_kinsol.so
%{_libdir}/mpich/lib/libsundials_ida*.so
%{_libdir}/mpich/lib/libsundials_cvode*.so
%{_libdir}/mpich/lib/libsundials_arkode*.so
%{_libdir}/mpich/lib/libsundials_nvecserial.so
%{_libdir}/mpich/lib/libsundials_nvecopenmp.so
%{_libdir}/mpich/lib/libsundials_sunmatrix*.so
%{_libdir}/mpich/lib/libsundials_sunlinsol*.so
%{_libdir}/mpich/lib/libsundials_sunnonlinsol*.so
%{_libdir}/mpich/lib/libsundials_nvecmanyvector.so
%{_libdir}/mpich/lib/libsundials_nvecmpimanyvector.so
%{_libdir}/mpich/lib/cmake/sundials/
%endif

%files doc
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/NOTICE
%doc sundials-%{version}/doc/arkode/*.pdf
%doc sundials-%{version}/doc/ida*/*.pdf
%doc sundials-%{version}/doc/cvode*/*.pdf
%doc sundials-%{version}/doc/kinsol/*.pdf


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 7.3.0-5
- test: add initial lock files

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 20 2025 Antonio Trande <sagitter@fedoraproject.org> - 7.3.0-3
- Fix rhbz#2381140

* Fri May 09 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 7.3.0-2
- Fix flatpak build

* Sun Apr 27 2025 Antonio Trande <sagitter@fedoraproject.org> - 7.3.0-1
- Release 7.3.0

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 7.1.1-2
- Install sundials_futils.h file

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 7.1.1-1
- Release 7.1.1

* Sun Nov 10 2024 Songsong Zhang <u2fsdgvkx1@gmail.com> - 6.7.0-5
- Add SuperLUMT BuildRequires for RISC-V

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 6.7.0-3
- Rebuild for SuperLUMT-4.0.1

* Tue Apr 23 2024 David Bold <dave@ipp.mpg.de> - 6.7.0-2
- Only the -devel packages should pull in gcc

* Fri Mar 01 2024 Antonio Trande <sagitter@fedoraproject.org> - 6.7.0-1
- Release 6.7.0

* Sun Feb 04 2024 Orion Poplawski <orion@nwra.com> - 6.6.2-7
- Rebuild with suitesparse 7.6.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Antonio Trande <sagitter@fedoraproject.org> - 6.6.2-5
- Fix Obsoletes tag

* Fri Jan 19 2024 Antonio Trande <sagitter@fedoraproject.org> - 6.6.2-4
- Fix rhbz#2258767

* Sat Nov 11 2023 Orion Poplawski <orion@nwra.com> - 6.6.2-3
- Apply upstream patch to fix sonames

* Wed Nov 08 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.6.2-2
- Disable openmpi builds in i686 architecture

* Wed Nov 08 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.6.2-1
- Release 6.6.2

* Sun Oct 15 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.6.1-3
- Release 6.6.1| Add missing header file

* Sun Oct 15 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.6.1-2
- Release 6.6.1| PDF guides not installed

* Sun Oct 15 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.6.1-1
- Release 6.6.1

* Sun Aug 13 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.5.1-7
- Rebuild for petsc-3.19.4| Disable MPICH tests

* Sun Jul 23 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.5.1-6
- Active SUNDIALS_BUILD_WITH_PROFILING option

* Sun Jul 23 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.5.1-5
- Set _smp_ncpus_max equal to 1 for all architectures

* Sun Jul 23 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.5.1-4
- Set _smp_ncpus_max equal to 2 for all architectures

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 19 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.5.1-2
- Fix ctest commands

* Wed Apr 19 2023 Antonio Trande <sagitter@fedoraproject.org> - 6.5.1-1
- Release 6.5.1

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-32
- Bump build release number

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-31
- Fix installed files in EPEL9

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-30
- Disable PETSc in EPEL9

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-29
- Enable only KLU64 in EPEL9

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-28
- Fix klu64 libraries

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-27
- Fix PETSc support in EPEL9

* Sat Feb 25 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-26
- Disable superlu_dist support

* Sat Feb 25 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-25
- Rebuild (rhbz#2171312)| Enable KLU-64 in EPEL9 (rhbz#20673760)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 14 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-23
- Enable KLU support in EPEL9

* Wed Jan 04 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-22
- Build in EPEL9| Disable KLU support in EPEL9

* Sun Nov 13 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-21
- Use single job with ctest /2

* Sun Nov 13 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-20
- Use single job with ctest

* Sun Nov 13 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-19
- Enable OpenMPI tests

* Sat Oct 29 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-18
- Disable OpenMPI tests

* Sat Oct 29 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-17
- Use multiple jobs for testing

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 23 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-15
- Disable test_sunlinsol_klu of serial library

* Sat Apr 23 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-14
- Disable test_sunlinsol_klu

* Sat Apr 23 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-13
- Rebuild for PETSc-3.17.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-11
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support on epel8
  /4

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-10
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support /3

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-9
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support /2

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-8
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-7
- Disable debug build |Exclude test_sunnonlinsol_petscsnes

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-6
- Enable debug build

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-5
- Build on epel8 |MPI builds on epel8

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-4
- Build on epel8 |Enable PETSc support

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-3
- Build on epel8 |Disable KLU support in epel8

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-2
- Build on epel8 |Remove old lines in SPEC file

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-1
- Build on epel8

* Thu Sep 24 2020 Troy Dawson <tdawson@redhat.com> - 4.1.0-33
- remove package.cfg per new epel-playground policy

* Sun Apr 26 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-32
- Merge branch 'f32' into epel8

* Sun Apr 26 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-31
- Fix rhbz#1828004

* Fri Sep 20 2019 Orion Poplawski <orion@nwra.com> - 4.1.0-30
- Rebuild for hyper-2.17.0

* Mon Sep 09 2019 Orion Poplawski <orion@nwra.com> - 4.1.0-29
- Merge branch 'master' into epel8

* Mon Sep 09 2019 Orion Poplawski <orion@nwra.com> - 4.1.0-28
- Drop no longer needed BR on rsh; Only use dts for EL7

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-26
- Do not use devtoolset as runtime dependence

* Sat Jun 29 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-25
- Use devtoolset-8 on epel

* Fri Jun 28 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-24
- PETSc needs HDF5| Patched for disabling the PETSc tests of CMake

* Fri Jun 28 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-23
- Do not use curly brackets under %%%%files| Rebuild for petsc-3.11.3

* Thu Apr 25 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-22
- Reorganization of the files

* Tue Apr 23 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-21
- Exclude MPI tests on s390x

* Tue Apr 23 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-20
- Release 4.1.0|Use Python3

* Wed Feb 20 2019 sagitter <sagitter@fedoraproject.org>
- Tests disabled

* Wed Feb 20 2019 sagitter <sagitter@fedoraproject.org>
- Serial/MPI libraries are now separated

* Wed Feb 20 2019 sagitter <sagitter@fedoraproject.org>
- Tests of MPI libraries disabled for 'not enough slots available' errors

* Tue Feb 19 2019 sagitter <sagitter@fedoraproject.org>
- Debugging builds

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com>
- Rebuild for openmpi 3.1.3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 02 2018 sagitter <sagitter@fedoraproject.org>
- Use with_openmpicheck macro

* Sun Dec 02 2018 sagitter <sagitter@fedoraproject.org>
- PETSc support is now re-enabled (rhbz#1639646)

* Thu Nov 08 2018 sagitter <sagitter@fedoraproject.org>
- Update to 3.2.1

* Mon Oct 15 2018 sagitter <sagitter@fedoraproject.org>
- Update to 3.2.0

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Switch back to python2

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Switch to python3

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Exclude test_nvector_mpi_4 on s390x

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Update to 3.1.2; enable PETSC support.

* Mon Jul 16 2018 sagitter <sagitter@fedoraproject.org>
- Add gcc gcc-c++ BR

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 sagitter <sagitter@fedoraproject.org>
- Fix Oboletes tag

* Wed Jun 06 2018 sagitter <sagitter@fedoraproject.org>
- Use SuperLUMT64 on 64bit systems

* Mon May 14 2018 sagitter <sagitter@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1

* Fri May 04 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-5
- Rebuild for hypre-2.14.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-3
- Use %%%%ldconfig_scriptlets

* Wed Jan 31 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-2
- Rebuild for GCC-8

* Sun Jan 28 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Wed Nov 15 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-5
- Define Hypre libraries

* Wed Nov 15 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-4
- Define builds for Hypre libraries

* Wed Nov 15 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-3
- Fix shared-linker flags

* Thu Nov 09 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-2
- Remove sub-packages

* Wed Nov 08 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 sagitter <sagitter@fedoraproject.org> - 2.7.0-14
- Build OpenMPI libraries on EPEL

* Fri Mar 03 2017 sagitter <sagitter@fedoraproject.org> - 2.7.0-13
- Set builds for s390x

* Fri Mar 03 2017 sagitter <sagitter@fedoraproject.org> - 2.7.0-12
- Add KLU support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 01 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-10
- New architectures

* Mon Oct 24 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-9
- Fix builds of MPICH libraries

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.7.0-8
- Rebuild for openmpi 2.0

* Mon Oct 17 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-7
- Set debug builds

* Thu Oct 06 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-6
- SuperLUMT support condizionalized

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-5
- Provide static files

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-4
- Enabled SuperLUMT and HYPRE support

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-3
- Enabled SuperLUMT and HYPRE support

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-2
- Enabled SuperLUMT and HYPRE support

* Thu Sep 29 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Sun Mar 27 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-19
- Typos fixed

* Sat Mar 26 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-18
- Enabled OpenMP support

* Sun Mar 20 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.2-17
- Add lapack-devel requires to -devel package

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-15
- Fixed pthread flags

* Sun Jan 17 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-14
- MPICH libraries enabled

* Thu Dec 31 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-13
- Exclude pkgconfig for OpenMPI libs on s390

* Wed Dec 30 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-12
- All Fortran libraries moved to default library paths;fixed pkgconfig
  files

* Thu Nov 12 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-11
- Fixes for EPEL7

* Thu Nov 12 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-10
- OpenMPI Fortran lib tests not compiled on F<23

* Thu Nov 12 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-9
- Hardened builds on <F23

* Thu Oct 15 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-8
- Rebuilt for cmake 3.4.0

* Sun Sep 20 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-7
- Performed even tests of the parallel-libraries on ix86 arches

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-6
- Rebuild for openmpi 1.10.0

* Fri Aug 28 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.2-5
- Rebuild for rpm-mpi-hooks-3-2

* Sat Aug 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.2-4
- Rebuild for MPI provides

* Tue Aug 11 2015 Sandro Mani <manisandro@gmail.com> - 2.6.2-3
- RPM MPI Requires Provides

* Tue Aug 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-2
- Added rsh as BR for EPEL7

* Tue Aug 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Fri Jun 19 2015 Dennis Gilmore <dennis@ausil.us> - 2.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-7
- openmpi tests disabled on ix86 %%%%{arm} (BZ#1201901)

* Sat May 09 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-6
- Excluded kinKrylovDemo_ls test for aarch64

* Fri Apr 17 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-5
- Performed parallel/serial tests

* Fri Apr 17 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-4
- Performed parallel/serial tests

* Fri Apr 17 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-3
- Fixed ldconfig scriptlets

* Sat Apr 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-2
- Built OpenMPI/Fortran libraries with threading support

* Tue Mar 31 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.1-1
- Update to version 2.6.1
- Minor bugfixes

* Mon Mar 30 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-2
- Ensure the shared libraries are linked correctly

* Sun Mar 29 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
- Drop patches that are not needed anymore

* Mon Aug 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-7
- Fixed patches used in the previous build
- Fixes bug #1105767

* Sun Jun 08 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-6
- Fixed patches used in the previous build
- Fixes bug #1105767

* Thu May 22 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-5
- added patches to fix bugs #926583 and #1037342

* Thu May 22 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-4
- added patches to fix bugs #926583 and #1037342

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Dan Horák <dan@danny.cz> - 2.5.0-2
- openmpi not available s390(x)

* Sat Jan 26 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.5.0-1
- upstream release 2.5.0
- enable parallel build
- drop obsolete patch

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 2.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-8
- dist-git conversion

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 2.3.0-7
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Mon Jul 27 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Ville Skyttä <scop@fedoraproject.org> - 2.3.0-4
- Note bug number for the previous commit.

* Wed Nov 05 2008 Ville Skyttä <scop@fedoraproject.org> - 2.3.0-3
- Fix Patch0:/%%patch mismatch.

* Tue Feb 19 2008 Jesse Keating <jkeating@fedoraproject.org> - 2.3.0-2
- Autorebuild for GCC 4.3

* Tue Aug 07 2007 John Pye <jpye@fedoraproject.org> - 2.3.0-1
- first upload of reviewed package.

* Sun Apr 26 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-7
- Fix rhbz#1828004

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-5
- Workaround for GCC-10 (-fcommon)

* Sun Jan 05 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-4
- New rebuild

* Sat Dec 21 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-3
- Rebuild for petsc-3.11.3 on EPEL7

* Fri Oct 18 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-2
- Rebuild for petsc-3.12.0

* Sun Apr 26 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-1
- Disable MPI tests on EPEL8

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-2
- Build on epel8

* Wed Oct 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-1
- Release 5.8.0

* Mon Jul 26 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.7.0-4
- Disable debug mode| Modify ctest commands

* Mon Jul 26 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.7.0-3
- Enable debug mode

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 24 2021 Antonio T <sagitter@fedoraproject.org> - 5.7.0-1
- Release 5.7.0

* Sun Feb 21 2021 Antonio T <sagitter@fedoraproject.org> - 5.6.1-4
- Fix the lists of installed files

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Tom Stellard <tstellar@redhat.com> - 5.6.1-2
- Add BuildRequires: make

* Tue Jan 05 2021 Antonio T <sagitter@fedoraproject.org> - 5.6.1-1
- Release 5.6.1

* Thu Dec 10 2020 Antonio T <sagitter@fedoraproject.org> - 5.5.0-5
- Modify sed commands

* Thu Dec 10 2020 Antonio T <sagitter@fedoraproject.org> - 5.5.0-4
- Modify CMake options

* Fri Nov 20 2020 Antonio T <sagitter@fedoraproject.org> - 5.5.0-3
- Release 5.5.0| Fix library paths/2

* Fri Nov 20 2020 Antonio T <sagitter@fedoraproject.org> - 5.5.0-2
- Release 5.5.0| Fix library paths

* Fri Nov 20 2020 Antonio T <sagitter@fedoraproject.org> - 5.5.0-1
- Release 5.5.0

* Sat Oct 03 2020 sagitter <sagitter@fedoraproject.org> - 5.4.0-1
- Release 5.4.0

* Mon Aug 24 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-15
- Increase build release number

* Mon Aug 24 2020 Troy Dawson <tdawson@fedoraproject.org> - 5.3.0-14
- Minor conditional tweak for ELN

* Sat Aug 22 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-13
- Reorganize installed files/4

* Sat Aug 22 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-12
- Reorganize installed files/3

* Sat Aug 22 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-11
- Reorganize installed files/2

* Sat Aug 22 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-10
- Reorganize installed files

* Sat Aug 22 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-9
- Disable LTO

* Sat Aug 22 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-8
- Fix ldflags

* Thu Aug 20 2020 Iñaki Úcar <iucar@fedoraproject.org> - 5.3.0-7
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Tue Aug 04 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-6
- Undo latest change

* Tue Aug 04 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-5
- Undefine ld_as_needed flag

* Tue Aug 04 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-4
- Enable __cmake_in_source_build

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 28 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-1
- Release 5.3.0

* Sat May 23 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-10
- Fix release number

* Sat May 23 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-9
- Add OMPI_MCA_rmaps_base_oversubscribe=yes option to prevent ctest
  failures due to insufficient number of slots

* Sat May 23 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-8
- Add  option to prevent Usage

* Fri May 22 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-7
- Re-organize installed files

* Fri May 22 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-6
- Fix installation of config.h files (rhbz#1839131)

* Fri Apr 24 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-5
- Fix packaging of all libraries

* Fri Apr 24 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-4
- Fix rhbz#1827675

* Fri Apr 10 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-3
- Downgrade jobs of CTest commands

* Fri Apr 10 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-2
- Remove never built release (5.1.0)

* Fri Apr 10 2020 sagitter <sagitter@fedoraproject.org> - 5.2.0-1
- Release 5.2.0| Use -fcommon flag workaround for GCC-10

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-32
- Workaround for GCC-10 (-fcommon)

* Sun Jan 05 2020 sagitter <sagitter@fedoraproject.org> - 4.1.0-31
- New rebuild

* Sat Dec 21 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-30
- Rebuild for petsc-3.11.3 on EPEL7

* Fri Oct 18 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-29
- Rebuild for petsc-3.12.0

* Mon Sep 09 2019 Orion Poplawski <orion@nwra.com> - 4.1.0-28
- Drop no longer needed BR on rsh; Only use dts for EL7

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-26
- Do not use devtoolset as runtime dependence

* Sat Jun 29 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-25
- Use devtoolset-8 on epel

* Fri Jun 28 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-24
- PETSc needs HDF5| Patched for disabling the PETSc tests of CMake

* Fri Jun 28 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-23
- Do not use curly brackets under %%%%files| Rebuild for petsc-3.11.3

* Thu Apr 25 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-22
- Reorganization of the files

* Tue Apr 23 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-21
- Exclude MPI tests on s390x

* Tue Apr 23 2019 sagitter <sagitter@fedoraproject.org> - 4.1.0-20
- Release 4.1.0|Use Python3

* Wed Feb 20 2019 sagitter <sagitter@fedoraproject.org>
- Tests disabled

* Wed Feb 20 2019 sagitter <sagitter@fedoraproject.org>
- Serial/MPI libraries are now separated

* Wed Feb 20 2019 sagitter <sagitter@fedoraproject.org>
- Tests of MPI libraries disabled for 'not enough slots available' errors

* Tue Feb 19 2019 sagitter <sagitter@fedoraproject.org>
- Debugging builds

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com>
- Rebuild for openmpi 3.1.3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 02 2018 sagitter <sagitter@fedoraproject.org>
- Use with_openmpicheck macro

* Sun Dec 02 2018 sagitter <sagitter@fedoraproject.org>
- PETSc support is now re-enabled (rhbz#1639646)

* Thu Nov 08 2018 sagitter <sagitter@fedoraproject.org>
- Update to 3.2.1

* Mon Oct 15 2018 sagitter <sagitter@fedoraproject.org>
- Update to 3.2.0

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Switch back to python2

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Switch to python3

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Exclude test_nvector_mpi_4 on s390x

* Wed Sep 05 2018 sagitter <sagitter@fedoraproject.org>
- Update to 3.1.2; enable PETSC support.

* Mon Jul 16 2018 sagitter <sagitter@fedoraproject.org>
- Add gcc gcc-c++ BR

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 sagitter <sagitter@fedoraproject.org>
- Fix Oboletes tag

* Wed Jun 06 2018 sagitter <sagitter@fedoraproject.org>
- Use SuperLUMT64 on 64bit systems

* Mon May 14 2018 sagitter <sagitter@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1

* Fri May 04 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-5
- Rebuild for hypre-2.14.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-3
- Use %%%%ldconfig_scriptlets

* Wed Jan 31 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-2
- Rebuild for GCC-8

* Sun Jan 28 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Wed Nov 15 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-5
- Define Hypre libraries

* Wed Nov 15 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-4
- Define builds for Hypre libraries

* Wed Nov 15 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-3
- Fix shared-linker flags

* Thu Nov 09 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-2
- Remove sub-packages

* Wed Nov 08 2017 sagitter <sagitter@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 sagitter <sagitter@fedoraproject.org> - 2.7.0-14
- Build OpenMPI libraries on EPEL

* Fri Mar 03 2017 sagitter <sagitter@fedoraproject.org> - 2.7.0-13
- Set builds for s390x

* Fri Mar 03 2017 sagitter <sagitter@fedoraproject.org> - 2.7.0-12
- Add KLU support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 01 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-10
- New architectures

* Mon Oct 24 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-9
- Fix builds of MPICH libraries

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.7.0-8
- Rebuild for openmpi 2.0

* Mon Oct 17 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-7
- Set debug builds

* Thu Oct 06 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-6
- SuperLUMT support condizionalized

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-5
- Provide static files

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-4
- Enabled SuperLUMT and HYPRE support

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-3
- Enabled SuperLUMT and HYPRE support

* Tue Oct 04 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-2
- Enabled SuperLUMT and HYPRE support

* Thu Sep 29 2016 sagitter <sagitter@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Sun Mar 27 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-19
- Typos fixed

* Sat Mar 26 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-18
- Enabled OpenMP support

* Sun Mar 20 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.2-17
- Add lapack-devel requires to -devel package

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-15
- Fixed pthread flags

* Sun Jan 17 2016 sagitter <sagitter@fedoraproject.org> - 2.6.2-14
- MPICH libraries enabled

* Thu Dec 31 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-13
- Exclude pkgconfig for OpenMPI libs on s390

* Wed Dec 30 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-12
- All Fortran libraries moved to default library paths;fixed pkgconfig
  files

* Thu Nov 12 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-11
- Fixes for EPEL7

* Thu Nov 12 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-10
- OpenMPI Fortran lib tests not compiled on F<23

* Thu Nov 12 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-9
- Hardened builds on <F23

* Thu Oct 15 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-8
- Rebuilt for cmake 3.4.0

* Sun Sep 20 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-7
- Performed even tests of the parallel-libraries on ix86 arches

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-6
- Rebuild for openmpi 1.10.0

* Fri Aug 28 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.2-5
- Rebuild for rpm-mpi-hooks-3-2

* Sat Aug 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.2-4
- Rebuild for MPI provides

* Tue Aug 11 2015 Sandro Mani <manisandro@gmail.com> - 2.6.2-3
- RPM MPI Requires Provides

* Tue Aug 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-2
- Added rsh as BR for EPEL7

* Tue Aug 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Fri Jun 19 2015 Dennis Gilmore <dennis@ausil.us> - 2.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-7
- openmpi tests disabled on ix86 %%%%{arm} (BZ#1201901)

* Sat May 09 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-6
- Excluded kinKrylovDemo_ls test for aarch64

* Fri Apr 17 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-5
- Performed parallel/serial tests

* Fri Apr 17 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-4
- Performed parallel/serial tests

* Fri Apr 17 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-3
- Fixed ldconfig scriptlets

* Sat Apr 04 2015 sagitter <sagitter@fedoraproject.org> - 2.6.1-2
- Built OpenMPI/Fortran libraries with threading support

* Tue Mar 31 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.1-1
- Update to version 2.6.1
- Minor bugfixes

* Mon Mar 30 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-2
- Ensure the shared libraries are linked correctly

* Sun Mar 29 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
- Drop patches that are not needed anymore

* Mon Aug 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-7
- Fixed patches used in the previous build
- Fixes bug #1105767

* Sun Jun 08 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-6
- Fixed patches used in the previous build
- Fixes bug #1105767

* Thu May 22 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-5
- added patches to fix bugs #926583 and #1037342

* Thu May 22 2014 nonamedotc <nonamedotc@fedoraproject.org> - 2.5.0-4
- added patches to fix bugs #926583 and #1037342

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Dan Horák <dan@danny.cz> - 2.5.0-2
- openmpi not available s390(x)

* Sat Jan 26 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.5.0-1
- upstream release 2.5.0
- enable parallel build
- drop obsolete patch

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 2.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-8
- dist-git conversion

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 2.3.0-7
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Mon Jul 27 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Ville Skyttä <scop@fedoraproject.org> - 2.3.0-4
- Note bug number for the previous commit.

* Wed Nov 05 2008 Ville Skyttä <scop@fedoraproject.org> - 2.3.0-3
- Fix Patch0:/%%patch mismatch.

* Tue Feb 19 2008 Jesse Keating <jkeating@fedoraproject.org> - 2.3.0-2
- Autorebuild for GCC 4.3

* Tue Aug 07 2007 John Pye <jpye@fedoraproject.org> - 2.3.0-1
- first upload of reviewed package.
## END: Generated by rpmautospec
