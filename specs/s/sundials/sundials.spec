## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 7.3.0-5
- Latest state for sundials

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

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-34
- Bump build release number

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-33
- Fix installed files in EPEL9

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-32
- Disable PETSc in EPEL9

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-31
- Enable only KLU64 in EPEL9

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-30
- Fix klu64 libraries

* Fri Mar 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-29
- Fix PETSc support in EPEL9

* Sat Feb 25 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-28
- Disable superlu_dist support

* Sat Feb 25 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-27
- Rebuild (rhbz#2171312)| Enable KLU-64 in EPEL9 (rhbz#20673760)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 14 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-25
- Enable KLU support in EPEL9

* Wed Jan 04 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-24
- Build in EPEL9| Disable KLU support in EPEL9

* Sun Nov 13 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-23
- Use single job with ctest /2

* Sun Nov 13 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-22
- Use single job with ctest

* Sun Nov 13 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-21
- Enable OpenMPI tests

* Sat Oct 29 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-20
- Disable OpenMPI tests

* Sat Oct 29 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-19
- Use multiple jobs for testing

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 23 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-17
- Disable test_sunlinsol_klu of serial library

* Sat Apr 23 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-16
- Disable test_sunlinsol_klu

* Sat Apr 23 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-15
- Rebuild for PETSc-3.17.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-13
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support on epel8
  /4

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-12
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support /3

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-11
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support /2

* Sat Nov 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-10
- Rebuild for MPI upgrades on epel8 | Enable suitesparse support

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-9
- Disable debug build |Exclude test_sunnonlinsol_petscsnes

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-8
- Enable debug build

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-7
- Build on epel8 |MPI builds on epel8

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-6
- Build on epel8 |Enable PETSc support

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-5
- Build on epel8 |Disable KLU support in epel8

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-4
- Build on epel8 |Remove old lines in SPEC file

* Sat Nov 06 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.8.0-3
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
