## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Broken package_note links in rules and variables files
# Disabling this functionality
%undefine _package_note_file

# Disable LTO
%global _lto_cflags %{nil}

# Python binding and its testing
%bcond_without python

# petsc4py test fails with MPICH for "No PMIx server was reachable, but a PMI1/2 was detected"
%if %{with python}
%bcond_with pycheck
%endif

# PETSc fails yet on s390x
# Abort(76) on node 1 (rank 0 in comm 16): application called MPI_Abort(MPI_COMM_SELF, 76) - process 0
%ifnarch s390x
%bcond_without check
%else
%bcond_with check
%endif

%global pymodule_name petsc4py
%global pymodule_version %{version}
#

## Debug builds ?
%bcond_with debug
#

## Fix Epoch in EPEL9
%if 0%{?el9}
%global epoch 1
%else
%global epoch 0
%endif

%ifarch %{ix86}
%bcond_with openmpi
%else
%bcond_without openmpi
%endif
%bcond_without mpich

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%bcond_without arch64
%else
%bcond_with arch64
%endif

%bcond_without blas
%if %{with arch64}
%bcond_without blas64
%endif

%global blaslib flexiblas
%global blasvar %{nil}

#
## MUMPS support
%bcond_without mumps_serial
#
## Sundials needs mpi ?
%bcond_with sundials_serial
#
%bcond_without superlu
#

## Suitesparse
%bcond_with suitesparse
%bcond_with suitesparse64
#

## SuperLUDIST needs parmetis
%bcond_without superludist >= 6.3.0
%bcond_with cgns
%bcond_without hdf5
%bcond_with superlumt
#

## Tetgen
%bcond_with tetgen
#

## Metis
%bcond_without metis
%bcond_without metis64
#

# 'scalapack' is required by 'MUMPS'
%if %{with openmpi}
%bcond_without mpi
# PETSC-3.* is incompatible with Sundials 3+
%bcond_with sundials
%bcond_without scalapack
%bcond_without mumps
%bcond_without ptscotch
%bcond_without hypre
%endif

%if %{with mpich}
%bcond_without mpi
# PETSC-3.* is incompatible with Sundials 3+
%bcond_with sundials
%bcond_without scalapack
%bcond_without mumps
%bcond_without ptscotch
%bcond_without hypre
%endif

%global petsc_build_options \\\
 %if %{with debug} \
 CFLAGS="-O0 -g -Wl,-z,now -fPIC" CXXFLAGS="-O0 -g -Wl,-z,now -fPIC" FFLAGS="-O0 -g -Wl,-z,now -fPIC -I%{_libdir}/gfortran/modules" COPTFLAGS="-O0 -g -Wl,-z,now" \\\
  CXXOPTFLAGS="-O0 -g -Wl,-z,now" FOPTFLAGS="-O0 -g -Wl,-z,now -I%{_libdir}/gfortran/modules" LDFLAGS="$LDFLAGS -fPIC" \\\
  FCFLAGS="-O0 -g -Wl,-z,now -fPIC -I%{_libdir}/gfortran/modules" \\\
 %else \
 CFLAGS="$CFLAGS -O3" CXXFLAGS="$CXXFLAGS -O3" FFLAGS="$FFLAGS -O3" LDFLAGS="$LDFLAGS" \\\
  COPTFLAGS="$CFLAGS -O3" CXXOPTFLAGS="$CXXFLAGS -O3 -std=gnu++17" FOPTFLAGS="$FFLAGS -O3" \\\
  FCFLAGS="$FFLAGS -O3" \\\
 %endif \
 --CC_LINKER_FLAGS="$LDFLAGS" \\\
 --FC_LINKER_FLAGS="$LDFLAGS -lgfortran" \\\
 --with-default-arch=0 --with-make=1 \\\
 --with-cmake-exec=%{_bindir}/cmake --with-ctest-exec=%{_bindir}/ctest \\\
 --with-single-library=1 \\\
 --with-precision=double \\\
 --with-petsc-arch=%{_arch} \\\
 --with-clanguage=C \\\
 --with-shared-libraries=1 \\\
 --with-fortran-interfaces=1 \\\
 --with-windows-graphics=0 \\\
 --CC=gcc \\\
 --FC=gfortran \\\
 --CXX=g++ \\\
 --with-shared-ld=ld \\\
 --with-pic=1 \\\
 --with-clib-autodetect=0 \\\
 --with-fortranlib-autodetect=0 \\\
 --with-threadsafety=0 --with-log=1 \\\
 --with-mkl_sparse=0 \\\
 --with-mkl_sparse_optimize=0 \\\
 --with-mkl_cpardiso=0 \\\
 --with-mkl_pardiso=0 \\\
 --with-python=0 \\\
 --with-cxxlib-autodetect=1 \\\
 %if %{with debug} \
  --with-debugging=1 \\\
 %else \
  --with-debugging=0 \\\
 %endif \
 %if %{with mumps_serial} \
  --with-mumps-serial=1 \\\
 %endif \
  --with-mpi=0 \\\
 %if %{with hdf5} \
  --with-hdf5=1 \\\
  --with-hdf5-include= \\\
  --with-hdf5-lib="-lhdf5 -lhdf5_hl" \\\
 %endif \
 %if %{with cgns} \
  --with-cgns=0 \\\
 %endif \
  --with-x=1 \\\
  --with-openmp=0 \\\
  --with-hwloc=0 \\\
  --with-ssl=0 \\\
 %if %{with sundials_serial} \
  --with-sundials=1 \\\
  --with-sundials-include=%{_includedir} \\\
  --with-sundials-lib="-lsundials_nvecserial -lsundials_cvode" \\\
 %endif \
 %ifarch %{valgrind_arches} \
  --with-valgrind=1 \\\
 %endif \
  --with-pthread=1

%global petsc_mpibuild_options \\\
 %if %{with debug} \
 CFLAGS="-O0 -g -Wl,-z,now -fPIC" CXXFLAGS="-O0 -g -Wl,-z,now -fPIC" FFLAGS="-O0 -g -Wl,-z,now -fPIC -I${MPI_FORTRAN_MOD_DIR}" COPTFLAGS="-O0 -g -Wl,-z,now" \\\
  CXXOPTFLAGS="-O0 -g -Wl,-z,now" FOPTFLAGS="-O0 -g -Wl,-z,now -I${MPI_FORTRAN_MOD_DIR}" LDFLAGS="$LDFLAGS -fPIC" \\\
  FCFLAGS="-O0 -g -Wl,-z,now -fPIC -I${MPI_FORTRAN_MOD_DIR}" \\\
 %else \
 CFLAGS="$CFLAGS -O3" CXXFLAGS="$CXXFLAGS -O3" FFLAGS="$FFLAGS -O3" LDFLAGS="$LDFLAGS" \\\
  COPTFLAGS="$CFLAGS -O3" CXXOPTFLAGS="$CXXFLAGS -O3 -std=gnu++17" FOPTFLAGS="$FFLAGS -O3" \\\
  FCFLAGS="$FFLAGS -O3" \\\
 %endif \
  --CC_LINKER_FLAGS="$LDFLAGS" \\\
  --with-default-arch=0 --with-make=1 \\\
  --with-cmake-exec=%{_bindir}/cmake --with-ctest-exec=%{_bindir}/ctest \\\
  --with-single-library=1 \\\
  --with-precision=double \\\
  --with-petsc-arch=%{_arch} \\\
  --with-clanguage=C \\\
  --with-shared-libraries=1 \\\
  --with-fortran-interfaces=1 \\\
  --with-windows-graphics=0 \\\
  --with-cc=${MPI_BIN}/mpicc \\\
  --with-cxx=${MPI_BIN}/mpicxx \\\
  --with-fc=${MPI_BIN}/mpif90 \\\
  --with-shared-ld=ld \\\
  --with-pic=1 \\\
  --with-clib-autodetect=0 \\\
  --with-fortranlib-autodetect=0 \\\
  --with-mkl_sparse=0 \\\
  --with-mkl_sparse_optimize=0 \\\
  --with-mkl_cpardiso=0 \\\
  --with-mkl_pardiso=0 \\\
 %if %{with python} \
  --with-python=1 \\\
  --with-python-exec=%{__python3} \\\
  --with-petsc4py=1 \\\
  --with-petsc4py-test-np=2 \\\
 %endif \
  --with-cxxlib-autodetect=1 \\\
   %if %{with debug} \
  --with-debugging=1 \\\
 %else \
  --with-debugging=0 \\\
 %endif \
  --with-threadsafety=0 --with-log=1 \\\
 %if %{with scalapack} \
  --with-scalapack=1 \\\
  --with-scalapack-lib="-L$MPI_LIB -lscalapack" \\\
  --with-scalapck-include="" \\\
 %endif \
 %if %{with mpi} \
  --with-mpi=1 \\\
 %endif \
 %if %{with cgns} \
  --with-cgns=1 \\\
  --with-cgns-include=%{_includedir} \\\
  --with-cgns-lib=-lcgns \\\
 %endif \
 %if %{with hdf5} \
  --with-hdf5=1 \\\
  --with-hdf5-include= \\\
  --with-hdf5-lib="-L$MPI_LIB -lhdf5 -lhdf5_hl" \\\
 %endif \
 %if %{with ptscotch} \
  --with-bison=1 \\\
  --with-bison-exec=%{_bindir}/bison \\\
  --with-ptscotch=1 \\\
  %if 0%{?rhel} \
  --with-ptscotch-include=$MPI_INCLUDE \\\
  %else \
  --with-ptscotch-include=$MPI_INCLUDE/scotch \\\
  %endif \
  --with-ptscotch-lib="-L$MPI_LIB -lptscotch -lscotch -lptscotcherr -lscotcherr" \\\
 %endif \
 %if %{with mumps} \
  --with-mumps=1 \\\
 %endif \
 %if %{with sundials} \
  --with-sundials=1 \\\
  --with-sundials-include=$MPI_INCLUDE \\\
  --with-sundials-lib=-lsundials_nvecparallel \\\
 %endif \
 %if %{with superludist} \
  --with-superlu_dist=1 \\\
  --with-superlu_dist-include=$MPI_INCLUDE/superlu_dist \\\
  --with-superlu_dist-lib=-lsuperlu_dist \\\
 %endif \
  --with-x=1 \\\
  --with-openmp=0 \\\
  --with-hwloc=0 \\\
  --with-ssl=0 \\\
 %if %{with hypre} \
  --with-hypre=1 \\\
  --with-hypre-include=$MPI_INCLUDE/hypre \\\
  --with-hypre-lib="-L$MPI_LIB -lHYPRE" \\\
 %endif \
 %if %{with fftw} \
  --with-fftw=1 \\\
  --with-fftw-include= \\\
  --with-fftw-lib="-L$MPI_LIB -lfftw3_mpi -lfftw3" \\\
 %endif \
 %ifarch %{valgrind_arches} \
  --with-valgrind=1 \\\
 %endif \
  --with-pthread=1
  
%global mpichversion %(rpm -qi mpich | awk -F': ' '/Version/ {print $2}')
%global openmpiversion %(rpm -qi openmpi | awk -F': ' '/Version/ {print $2}')
%global majorver 3
%global releasever %{majorver}.23

Name:    petsc
Summary: Portable Extensible Toolkit for Scientific Computation
Version: %{releasever}.6
Release: %autorelease
License: BSD-2-Clause
URL:     https://petsc.org/
Source0: https://web.cels.anl.gov/projects/%{name}/download/release-snapshots/%{name}-with-docs-%{version}.tar.gz

# These files have been generated by Cython-3.0.6
# PETSC-3.20+ needs Cython-3.0.0, these files are used in EPEL9
Source1: %{name}-3.20-PETSc_cython3.0.6.c
Source2: %{name}-3.20-PETSc_cython3.0.6.h
Source3: %{name}-3.20-PETSc_api_cython3.0.6.h

## Remove rpath flags
Patch0:  %{name}-3.21.1-no-rpath.patch

## Rename library name for 64-bit integer package
Patch1:  %{name}-lib64.patch
Patch3:  %{name}-3.19.4-fix_mumps_includes.patch
Patch4:  %{name}-3.21.1-fix_metis64.patch
Patch6:  %{name}-3.14.1-fix_pkgconfig_file.patch
Patch7:  %{name}-3.22.2-avoid_fake_MKL_detection.patch

## Fix tests for Python-3.14+
Patch8:  https://gitlab.com/%{name}/%{name}/-/merge_requests/8680.patch

%if %{with superlu}
BuildRequires: SuperLU-devel >= 5.2.0
%endif
%if %{with superlumt}
BuildRequires: SuperLUMT-devel
%endif
%if %{with mumps_serial}
BuildRequires: MUMPS-devel
%endif
%if %{with metis}
BuildRequires: metis-devel >= 5.1.0
%endif
%if %{with suitesparse}
BuildRequires: suitesparse-devel >= 5.6.0
%endif
%if %{with blas}
BuildRequires: %{blaslib}-devel
%endif
BuildRequires: bison-devel, bison
BuildRequires: chrpath
BuildRequires: gcc, gcc-c++, cmake
BuildRequires: gcc-gfortran
BuildRequires: make
BuildRequires: libX11-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: pcre2-devel
%if %{with hdf5}
BuildRequires: hdf5-devel
%endif
%if %{with cgns}
BuildRequires: cgnslib-devel
BuildRequires: hdf5-devel
%endif
BuildRequires: tcsh
%if %{with tetgen}
BuildRequires: tetgen-devel
%endif
BuildRequires: xorg-x11-server-Xvfb
%ifarch %{valgrind_arches}
BuildRequires: valgrind
%endif

%description
PETSc, pronounced PET-see (the S is silent), is a suite of data structures
and routines for the scalable (parallel) solution of scientific applications
modeled by partial differential equations.

%package devel
Summary:    Portable Extensible Toolkit for Scientific Computation (developer files)
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran%{?_isa}
%description devel
Portable Extensible Toolkit for Scientific Computation (developer files).

%package doc
Summary:    Portable Extensible Toolkit for Scientific Computation (documentation files)
BuildRequires: python3-sphinx
BuildArch:  noarch
%description doc
Portable Extensible Toolkit for Scientific Computation.
PDF and HTML documentation files.

%if %{with arch64}
%package -n petsc64
Summary: Portable Extensible Toolkit for Scientific Computation (64bit INTEGER)
%if %{with metis64}
BuildRequires: metis64-devel >= 5.1.0
%endif

%description -n petsc64
PETSc, pronounced PET-see (the S is silent), is a suite of data structures
and routines for the scalable (parallel) solution of scientific applications
modeled by partial differential equations (64bit INTEGER).

%package -n petsc64-devel
Requires:   %{name}64%{?_isa} = %{version}-%{release}
Requires:   gcc-gfortran%{?_isa}
Summary:    Portable Extensible Toolkit for Scientific Computation (64bit INTEGER)

%description -n petsc64-devel
Portable Extensible Toolkit for Scientific Computation (developer files)
(64bit INTEGER).
%endif

#############################################################################
#########
%if %{with openmpi}
%package openmpi
Summary:    Portable Extensible Toolkit for Scientific Computation (OpenMPI)
BuildRequires: openmpi-devel
%if %{with hdf5}
BuildRequires: hdf5-openmpi-devel
%endif
%if %{with cgns}
BuildRequires: cgnslib-devel
BuildRequires: hdf5-openmpi-devel
%endif
%if %{with ptscotch}
BuildRequires: ptscotch-openmpi-devel
%endif
%if %{with scalapack}
BuildRequires: scalapack-openmpi-devel
%if 0%{?rhel}
BuildRequires: blacs-openmpi-devel
%endif
%endif
%if %{with mumps}
BuildRequires: MUMPS-openmpi-devel
%endif
%if %{with sundials}
BuildRequires: sundials-openmpi-devel
%endif
%if %{with superludist}
BuildRequires: superlu_dist-openmpi-devel >= 6.3.0
%endif
%if %{with fftw}
BuildRequires: fftw-devel
BuildRequires: fftw-openmpi-devel
%endif
%if %{with hypre}
BuildRequires: hypre-openmpi-devel >= 2.32.0
%endif

%description openmpi
PETSc, pronounced PET-see (the S is silent), is a suite of data structures
and routines for the scalable (parallel) solution of scientific applications
modeled by partial differential equations.

%package openmpi-devel
Summary:    Portable Extensible Toolkit for Scientific Computation (OpenMPI)
Requires:   %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires:   openmpi-devel%{?_isa} >= %{epoch}:4.1.5
Requires:   hdf5-openmpi-devel%{?_isa}
%description openmpi-devel
Portable Extensible Toolkit for Scientific Computation (developer files).

%if %{with python}
%package -n     python3-%{name}-openmpi
Summary:        Python3 bindings for OpenMPI PETSc
%py_provides    python3-%{name}-openmpi

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  hdf5-openmpi-devel
BuildRequires:  scalapack-openmpi-devel
BuildRequires:  ptscotch-openmpi-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-Cython
Requires:       petsc-openmpi%{?_isa}
Requires:       hdf5-openmpi%{?_isa}
Requires:       scalapack-openmpi%{?_isa}
Requires:       ptscotch-openmpi%{?_isa}
Requires:       openmpi%{?_isa} >= %{epoch}:4.1.5
Requires:       MUMPS-openmpi%{?_isa}

Obsoletes:      %{pymodule_name}-openmpi < 0:3.14.0-3
Obsoletes:      python3-%{pymodule_name}-openmpi < 0:3.14.0-3
Provides:       python3-%{pymodule_name}-openmpi = 0:%{pymodule_version}-%{release}
Provides:       python-%{pymodule_name}-openmpi = 0:%{pymodule_version}-%{release}
Provides:       %{pymodule_name}-openmpi = 0:%{pymodule_version}-%{release}

%description -n python3-%{name}-openmpi
This package provides Python3 bindings for OpenMPI PETSc,
the Portable, Extensible Toolkit for Scientific Computation.
%endif
%endif
######
###############################################################################
######
%if %{with mpich}
%package mpich
Summary:    Portable Extensible Toolkit for Scientific Computation (MPICH)
BuildRequires: mpich-devel
%if %{with hdf5}
BuildRequires: hdf5-mpich-devel
%endif
%if %{with cgns}
BuildRequires: cgnslib-devel
BuildRequires: hdf5-mpich-devel
%endif
%if %{with ptscotch}
BuildRequires: ptscotch-mpich-devel
%endif
%if %{with scalapack}
BuildRequires: scalapack-mpich-devel
%if 0%{?rhel}
BuildRequires: blacs-mpich-devel
%endif
%endif
%if %{with mumps}
BuildRequires: MUMPS-mpich-devel
%endif
%if %{with sundials}
BuildRequires: sundials-mpich-devel
%endif
%if %{with superludist}
BuildRequires: superlu_dist-mpich-devel >= 6.3.0
%endif
%if %{with hypre}
BuildRequires: hypre-mpich-devel >= 2.32.0
%endif
%if %{with fftw}
BuildRequires: fftw-devel
BuildRequires: fftw-mpich-devel
%endif
Requires:   mpich%{?_isa} >= %{epoch}:4.1.1

%description mpich
PETSc, pronounced PET-see (the S is silent), is a suite of data structures
and routines for the scalable (parallel) solution of scientific applications
modeled by partial differential equations.

%package mpich-devel
Summary:    Portable Extensible Toolkit for Scientific Computation (MPICH)
Requires:   %{name}-mpich%{?_isa} = %{version}-%{release}
Requires:   mpich-devel%{?_isa} >= %{epoch}:4.1.1
Requires:   hdf5-mpich-devel%{?_isa}
%description mpich-devel
Portable Extensible Toolkit for Scientific Computation (developer files).

%if %{with python}
%package -n     python3-%{name}-mpich
Summary:        Python3 bindings for MPICH PETSc
%py_provides    python3-%{name}-mpich

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  hdf5-mpich-devel
BuildRequires:  scalapack-mpich-devel
BuildRequires:  ptscotch-mpich-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-pip
BuildRequires:  python3-Cython
Requires:       petsc-mpich%{?_isa}
Requires:       hdf5-mpich%{?_isa}
Requires:       scalapack-mpich%{?_isa}
Requires:       ptscotch-mpich%{?_isa}
Requires:       mpich%{?_isa} >= %{epoch}:4.1.1
Requires:       MUMPS-mpich%{?_isa}

Obsoletes:      %{pymodule_name}-mpich < 0:3.14.0-3
Obsoletes:      python3-%{pymodule_name}-mpich < 0:3.14.0-3
Provides:       python3-%{pymodule_name}-mpich = 0:%{pymodule_version}-%{release}
Provides:       python-%{pymodule_name}-mpich = 0:%{pymodule_version}-%{release}
Provides:       %{pymodule_name}-mpich = 0:%{pymodule_version}-%{release}

%description -n python3-%{name}-mpich
This package provides Python3 bindings for MPICH PETSc,
the Portable, Extensible Toolkit for Scientific Computation.
%endif
%endif
######
#############################################################################

%prep
%setup -qc

%if %{with python}
rm -rf %{name}-%{version}/src/binding/petsc4py/src/*.egg-info

%if 0%{?fedora}
for i in `find . -name 'setup.py' -o -name 'configure' -o -name '*.py'`; do
%py3_shebang_fix $i
done
%endif
%endif

pushd %{name}-%{version}
%patch -P 7 -p1 -b .backup
%if 0%{?fedora} > 42
%patch -P 8 -p1 -b .backup
%endif
popd

# Remove pregenerated Cython C sources
pushd %{name}-%{version}
rm -vf $(grep -rl '/\* Generated by Cython')
popd

%if %{with arch64}
cp -a %{name}-%{version} build64
pushd build64
%patch -P 1 -p0 -b .backup
%if %{with metis64}
%patch -P 4 -p1 -b .metis64
%endif
popd
%endif

pushd %{name}-%{version}
%patch -P 0 -p0 -b .backup
%patch -P 6 -p1 -b .backup
popd

%if %{with openmpi}
cp -a %{name}-%{version} buildopenmpi_dir
%if 0%{?rhel}
cp %{SOURCE1} buildopenmpi_dir/src/binding/petsc4py/src/petsc4py/PETSc.c
cp %{SOURCE2} buildopenmpi_dir/src/binding/petsc4py/src/petsc4py/PETSc.h
cp %{SOURCE3} buildopenmpi_dir/src/binding/petsc4py/src/petsc4py/PETSc_api.h
%endif
%endif

%if %{with mpich}
cp -a %{name}-%{version} buildmpich_dir
%if 0%{?rhel}
cp %{SOURCE1} buildmpich_dir/src/binding/petsc4py/src/petsc4py/PETSc.c
cp %{SOURCE2} buildmpich_dir/src/binding/petsc4py/src/petsc4py/PETSc.h
cp %{SOURCE3} buildmpich_dir/src/binding/petsc4py/src/petsc4py/PETSc_api.h
%endif
%endif

# Do NOT move up this patch
pushd %{name}-%{version}
%patch -P 3 -p1 -b .backup
popd

#generate_buildrequires
#pushd buildopenmpi_dir/src/binding/petsc4py
#pyproject_buildrequires
#popd

%build
pushd %{name}-%{version}
%configure --with-cc=gcc --with-cxx=g++ --with-fc=gfortran \
 %{petsc_build_options} \
 --with-64-bit-indices=0 \
%if %{with blas}
 --with-blaslapack=1 --with-blaslapack-lib=-l%{blaslib}%{blasvar} --with-blaslapack-include=%{_includedir}/%{blaslib} \
%endif
%if %{with metis}
 --with-metis=1 \
%endif
%if %{with tetgen}
 --with-tetgen=1 \
 --with-tetgen-lib=-ltetgen \
%endif
%if %{with superlu}
 --with-superlu=1 \
 --with-superlu-include=%{_includedir}/SuperLU \
 --with-superlu-lib=-lsuperlu \
%endif
%if %{with suitesparse}
 --with-suitesparse=1 \
 --with-suitesparse-include=%{_includedir}/suitesparse \
 --with-suitesparse-lib="-lumfpack -lklu -lcholmod -lamd"
%endif
#cat config.log && exit 1
##

make V=1 PETSC_DIR=%{_builddir}/%{name}-%{version}/%{name}-%{version} PETSC_ARCH=%{_arch} all
popd

%if %{with arch64}
pushd build64
%configure --with-cc=gcc --with-cxx=g++ --with-fc=gfortran \
 %{petsc_build_options} \
 --with-64-bit-indices=1 \
%if %{with metis64}
 --with-metis=1 \
%endif
%if %{with blas64}
 --with-blaslapack=1 --with-blaslapack-lib=-l%{blaslib}%{blasvar}64 --with-blaslapack-include=%{_includedir}/%{blaslib} \
%endif
%if %{with suitesparse64}
 --with-suitesparse=1 \
 --with-suitesparse-include=%{_includedir}/suitesparse \
 --with-suitesparse-lib="-lumfpack64 -lklu64 -lcholmod64 -lamd64"
%endif
##

make V=1 PETSC_DIR=%{_builddir}/%{name}-%{version}/build64 PETSC_ARCH=%{_arch} all
popd
%endif

%if %{with openmpi}
cd buildopenmpi_dir

%{_openmpi_load}
export CC=mpicc
export CXX=mpic++
export FC=mpifort
%configure --with-cc=mpicc --with-cxx=mpic++ --with-fc=mpifort \
 --FC_LINKER_FLAGS="$LDFLAGS -lgfortran -lmpi_mpifh" \
 --LIBS=" -lmpi -lmpi_mpifh" \
 %{petsc_mpibuild_options} \
 --C_VERSION=%{openmpiversion} \
 --CXX_VERSION=%{openmpiversion} \
 --FC_VERSION=%{openmpiversion} \
%if %{with metis}
 --with-metis=1 \
%endif
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 --with-64-bit-indices=0 \
%endif
%if %{with blas}
 --with-blaslapack=1 --with-blaslapack-lib=-l%{blaslib}%{blasvar} --with-blaslapack-include=%{_includedir}/%{blaslib} \
%endif
#cat config.log
#exit 1

make V=1 PETSC_DIR=%{_builddir}/%{name}-%{version}/buildopenmpi_dir PETSC_ARCH=%{_arch} all
 
%if %{with python}
pushd src/binding/petsc4py
export PETSC_ARCH=%{_arch}
export PETSC_DIR=../../../
#pyproject_wheel
%py3_build
unset PETSC_ARCH
unset PETSC_DIR
popd
%endif

%{_openmpi_unload}
cd ..
%endif

%if %{with mpich}
cd buildmpich_dir

%{_mpich_load}
export CC=mpicc
export CXX=mpic++
export FC=mpifort
%configure --with-cc=mpicc --with-cxx=mpic++ --with-fc=mpifort \
 --FC_LINKER_FLAGS="$LDFLAGS -lgfortran -lfmpich -lmpichf90" \
 --LIBS=" -lmpich -lfmpich -lmpichf90" \
 %{petsc_mpibuild_options} \
 --C_VERSION=%{mpichversion} \
 --CXX_VERSION=%{mpichversion} \
 --FC_VERSION=%{mpichversion} \
%if %{with metis}
 --with-metis=1 \
%endif
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 --with-64-bit-indices=0 \
%endif
%if %{with blas}
 --with-blaslapack=1 --with-blaslapack-lib=-l%{blaslib}%{blasvar} --with-blaslapack-include=%{_includedir}/%{blaslib} \
%endif
#cat config.log
#exit 1

make V=1 PETSC_DIR=%{_builddir}/%{name}-%{version}/buildmpich_dir PETSC_ARCH=%{_arch} all

%if %{with python}
pushd src/binding/petsc4py
export PETSC_ARCH=%{_arch}
export PETSC_DIR=../../../
#pyproject_wheel
%py3_build
unset PETSC_ARCH
unset PETSC_DIR
popd
%endif

%{_mpich_unload}
cd ..
%endif

%install
pushd %{name}-%{version}
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_fmoddir}/%{name}
mkdir -p %{buildroot}%{_libdir}/%{name}/conf

install -pm 755 %{_arch}/lib/libpetsc.* %{buildroot}%{_libdir}
ln -sf libpetsc.so.%{version} %{buildroot}%{_libdir}/libpetsc.so
ln -sf libpetsc.so.%{version} %{buildroot}%{_libdir}/libpetsc.so.%{releasever}
ln -sf libpetsc.so.%{version} %{buildroot}%{_libdir}/libpetsc.so.%{majorver}

install -pm 644 %{_arch}/include/*.h %{buildroot}%{_includedir}/%{name}/
install -pm 644 %{_arch}/include/*.mod %{buildroot}%{_fmoddir}/%{name}/
cp -a include/* %{buildroot}%{_includedir}/%{name}/

cp -a %{_arch}/lib/pkgconfig %{buildroot}%{_libdir}/
sed -e 's|${prefix}/lib|${prefix}/%{_lib}|g' -i %{buildroot}%{_libdir}/pkgconfig/PETSc.pc
ln -srf %{_libdir}/pkgconfig/PETSc.pc %{buildroot}%{_libdir}/pkgconfig/petsc.pc

install -pm 644 %{_arch}/lib/petsc/conf/petscrules %{buildroot}%{_libdir}/%{name}/conf/
install -pm 644 %{_arch}/lib/petsc/conf/petscvariables %{buildroot}%{_libdir}/%{name}/conf/
install -pm 644 lib/petsc/conf/rules %{buildroot}%{_libdir}/%{name}/conf/
install -pm 644 lib/petsc/conf/variables %{buildroot}%{_libdir}/%{name}/conf/
sed -e 's|%{_builddir}/%{name}-%{version}/%{name}-%{version}|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscvariables
sed -e 's|%{_builddir}/%{name}-%{version}/%{name}-%{version}/%{_arch}/|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscvariables
sed -e 's|-L%{_prefix}/%{_arch}/lib|-L%{_libdir}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscvariables
sed -e 's|-I%{_prefix}/%{_arch}/include|-I%{_includedir}/%{name} -I%{_fmoddir}/%{name}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscvariables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}|g' -i %{buildroot}%{_libdir}/%{name}/conf/variables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}|g' -i %{buildroot}%{_libdir}/%{name}/conf/rules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscrules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscvariables
popd

%if %{with arch64}
pushd build64
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}/%{name}64
mkdir -p %{buildroot}%{_fmoddir}/%{name}64
mkdir -p %{buildroot}%{_libdir}/%{name}64/conf
mkdir -p %{buildroot}%{_libdir}/pkgconfig

install -pm 755 %{_arch}/lib/libpetsc64.* %{buildroot}%{_libdir}
ln -sf libpetsc64.so.%{version} %{buildroot}%{_libdir}/libpetsc64.so
ln -sf libpetsc64.so.%{version} %{buildroot}%{_libdir}/libpetsc64.so.%{releasever}
ln -sf libpetsc64.so.%{version} %{buildroot}%{_libdir}/libpetsc64.so.%{majorver}

install -pm 644 %{_arch}/include/*.h %{buildroot}%{_includedir}/%{name}64/
install -pm 644 %{_arch}/include/*.mod %{buildroot}%{_fmoddir}/%{name}64/
cp -a include/* %{buildroot}%{_includedir}/%{name}64/

cp -p %{_arch}/lib/pkgconfig/PETSc.pc %{buildroot}%{_libdir}/pkgconfig/PETSc64.pc
cp -p %{_arch}/lib/pkgconfig/PETSc.pc %{buildroot}%{_libdir}/pkgconfig/petsc64.pc
sed -e 's|${prefix}/lib|${prefix}/%{_lib}|g' -i %{buildroot}%{_libdir}/pkgconfig/PETSc64.pc
sed -e 's|${prefix}/lib|${prefix}/%{_lib}|g' -i %{buildroot}%{_libdir}/pkgconfig/petsc64.pc

install -pm 644 %{_arch}/lib/petsc/conf/petscrules %{buildroot}%{_libdir}/%{name}64/conf/
install -pm 644 %{_arch}/lib/petsc/conf/petscvariables %{buildroot}%{_libdir}/%{name}64/conf/
install -pm 644 lib/petsc/conf/rules %{buildroot}%{_libdir}/%{name}64/conf/
install -pm 644 lib/petsc/conf/variables %{buildroot}%{_libdir}/%{name}64/conf/
sed -e 's|%{_builddir}/%{name}-%{version}/build64|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}64/conf/petscvariables
sed -e 's|%{_builddir}/%{name}-%{version}/build64/%{_arch}/|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}64/conf/petscvariables
sed -e 's|-L%{_prefix}/%{_arch}/lib|-L%{_libdir}|g' -i %{buildroot}%{_libdir}/%{name}64/conf/petscvariables
sed -e 's|-I%{_prefix}/%{_arch}/include/|-I%{_includedir}/%{name}64 -I%{_fmoddir}/%{name}64|g' -i %{buildroot}%{_libdir}/%{name}64/conf/petscvariables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}|g' -i %{buildroot}%{_libdir}/%{name}64/conf/variables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}|g' -i %{buildroot}%{_libdir}/%{name}64/conf/rules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscrules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}%{_libdir}/%{name}/conf/petscvariables
popd
%endif

%if %{with openmpi}
cd buildopenmpi_dir
%{_openmpi_load}
mkdir -p %{buildroot}$MPI_LIB %{buildroot}$MPI_INCLUDE/%{name}
mkdir -p %{buildroot}$MPI_FORTRAN_MOD_DIR/%{name}
mkdir -p %{buildroot}$MPI_LIB/%{name}/conf

install -pm 755 %{_arch}/lib/libpetsc.* %{buildroot}$MPI_LIB
ln -sf libpetsc.so.%{version} %{buildroot}$MPI_LIB/libpetsc.so
ln -sf libpetsc.so.%{version} %{buildroot}$MPI_LIB/libpetsc.so.%{releasever}
ln -sf libpetsc.so.%{version} %{buildroot}$MPI_LIB/libpetsc.so.%{majorver}

install -pm 644 %{_arch}/include/*.h %{buildroot}$MPI_INCLUDE/%{name}/
install -pm 644 %{_arch}/include/*.mod %{buildroot}$MPI_FORTRAN_MOD_DIR/%{name}/
cp -a include/* %{buildroot}$MPI_INCLUDE/%{name}/

cp -a %{_arch}/lib/pkgconfig %{buildroot}$MPI_LIB/
sed -e 's|-I${includedir}/petsc|-I%{_includedir}/openmpi-%{_arch}/petsc|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|-L${libdir}|-L%{_libdir}/openmpi/lib|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|ldflag_rpath=-L|ldflag_rpath=-L%{_libdir}/openmpi/lib|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|-lpetsc|-lpetsc -lhdf5|' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|${prefix}/lib|${prefix}/%{_lib}/openmpi/lib|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
ln -srf $MPI_LIB/pkgconfig/PETSc.pc %{buildroot}$MPI_LIB/pkgconfig/petsc.pc

install -pm 644 %{_arch}/lib/petsc/conf/petscrules %{buildroot}$MPI_LIB/%{name}/conf/
install -pm 644 %{_arch}/lib/petsc/conf/petscvariables %{buildroot}$MPI_LIB/%{name}/conf/
install -pm 644 lib/petsc/conf/rules %{buildroot}$MPI_LIB/%{name}/conf/
install -pm 644 lib/petsc/conf/variables %{buildroot}$MPI_LIB/%{name}/conf/
sed -e 's|%{_builddir}/%{name}-%{version}/buildopenmpi_dir|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|%{_builddir}/%{name}-%{version}/buildopenmpi_dir/%{_arch}/|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|-L%{_prefix}/%{_arch}/lib|-L%{_libdir}/openmpi/lib|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|-I%{_prefix}/%{_arch}/include|-I%{_includedir}/openmpi-%{_arch}/%{name} -I%{_fmoddir}/openmpi/%{name}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}/openmpi/lib|g' -i %{buildroot}$MPI_LIB/%{name}/conf/variables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}/openmpi/lib|g' -i %{buildroot}$MPI_LIB/%{name}/conf/rules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscrules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables

%if %{with python}
pushd src/binding/petsc4py
export PETSC_ARCH=%{_arch}
export PETSC_DIR=../../../
#pyproject_install
%py3_install
unset PETSC_ARCH
unset PETSC_DIR
popd

# Install petsc4py files into MPI directories
%if 0%{?rhel}
MPI_PYTHON3_SITEARCH=%{python3_sitearch}/openmpi
%endif

mkdir -p %{buildroot}$MPI_PYTHON3_SITEARCH
cp -a %{buildroot}%{python3_sitearch}/%{pymodule_name} %{buildroot}$MPI_PYTHON3_SITEARCH/
rm -rf %{buildroot}%{python3_sitearch}/%{pymodule_name}
cp -a %{buildroot}%{python3_sitearch}/%{pymodule_name}-%{pymodule_version}-py%{python3_version}.egg-info %{buildroot}$MPI_PYTHON3_SITEARCH/
rm -rf %{buildroot}%{python3_sitearch}/%{pymodule_name}-%{pymodule_version}-py%{python3_version}.egg-info

chrpath -r $MPI_LIB %{buildroot}$MPI_PYTHON3_SITEARCH/%{pymodule_name}/lib/%{_arch}/*.so
%endif
%{_openmpi_unload}
cd ..
%endif

%if %{with mpich}
cd buildmpich_dir
%{_mpich_load}
mkdir -p %{buildroot}$MPI_LIB %{buildroot}$MPI_INCLUDE/%{name}
mkdir -p %{buildroot}$MPI_FORTRAN_MOD_DIR/%{name}
mkdir -p %{buildroot}$MPI_LIB/%{name}/conf

install -pm 755 %{_arch}/lib/libpetsc.* %{buildroot}$MPI_LIB
ln -sf libpetsc.so.%{version} %{buildroot}$MPI_LIB/libpetsc.so
ln -sf libpetsc.so.%{version} %{buildroot}$MPI_LIB/libpetsc.so.%{releasever}
ln -sf libpetsc.so.%{version} %{buildroot}$MPI_LIB/libpetsc.so.%{majorver}

install -pm 644 %{_arch}/include/*.h %{buildroot}$MPI_INCLUDE/%{name}/
install -pm 644 %{_arch}/include/*.mod %{buildroot}$MPI_FORTRAN_MOD_DIR/%{name}/
cp -a include/* %{buildroot}$MPI_INCLUDE/%{name}/

cp -a %{_arch}/lib/pkgconfig %{buildroot}$MPI_LIB/
sed -e 's|-I${includedir}/petsc|-I%{_includedir}/mpich-%{_arch}/petsc|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|-L${libdir}|-L%{_libdir}/mpich/lib|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|ldflag_rpath=-L|ldflag_rpath=-L%{_libdir}/mpich/lib|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|-lpetsc|-lpetsc -lhdf5|' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
sed -e 's|${prefix}/lib|${prefix}/%{_lib}/mpich/lib|g' -i %{buildroot}$MPI_LIB/pkgconfig/PETSc.pc
ln -srf $MPI_LIB/pkgconfig/PETSc.pc %{buildroot}$MPI_LIB/pkgconfig/petsc.pc

install -pm 644 %{_arch}/lib/petsc/conf/petscrules %{buildroot}$MPI_LIB/%{name}/conf/
install -pm 644 %{_arch}/lib/petsc/conf/petscvariables %{buildroot}$MPI_LIB/%{name}/conf/
install -pm 644 lib/petsc/conf/rules %{buildroot}$MPI_LIB/%{name}/conf/
install -pm 644 lib/petsc/conf/variables %{buildroot}$MPI_LIB/%{name}/conf/
sed -e 's|%{_builddir}/%{name}-%{version}/buildmpich_dir|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|%{_builddir}/%{name}-%{version}/buildmpich_dir/%{_arch}/|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|-L%{_prefix}/%{_arch}/lib|-L%{_libdir}/mpich/lib|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|-I%{_prefix}/%{_arch}/include|-I%{_includedir}/mpich-%{_arch}/%{name} -I%{_fmoddir}/mpich/%{name}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}/mpich/lib|g' -i %{buildroot}$MPI_LIB/%{name}/conf/variables
sed -e 's|${PETSC_DIR}/${PETSC_ARCH}/lib|%{_libdir}/mpich/lib|g' -i %{buildroot}$MPI_LIB/%{name}/conf/rules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscrules
sed -e 's|${PETSC_DIR}|%{_prefix}|g' -i %{buildroot}$MPI_LIB/%{name}/conf/petscvariables

%if %{with python}
pushd src/binding/petsc4py
export PETSC_ARCH=%{_arch}
export PETSC_DIR=../../../
#pyproject_install
%py3_install
unset PETSC_ARCH
unset PETSC_DIR
popd

# Install petsc4py files into MPI directories
%if 0%{?rhel}
MPI_PYTHON3_SITEARCH=%{python3_sitearch}/mpich
%endif

mkdir -p %{buildroot}$MPI_PYTHON3_SITEARCH
cp -a %{buildroot}%{python3_sitearch}/%{pymodule_name} %{buildroot}$MPI_PYTHON3_SITEARCH/
rm -rf %{buildroot}%{python3_sitearch}/%{pymodule_name}
cp -a %{buildroot}%{python3_sitearch}/%{pymodule_name}-%{pymodule_version}-py%{python3_version}.egg-info %{buildroot}$MPI_PYTHON3_SITEARCH/
rm -rf %{buildroot}%{python3_sitearch}/%{pymodule_name}-%{pymodule_version}-py%{python3_version}.egg-info

chrpath -r $MPI_LIB %{buildroot}$MPI_PYTHON3_SITEARCH/%{pymodule_name}/lib/%{_arch}/*.so
%endif
%{_mpich_unload}
cd ..
%endif

# Move html documentation in _pkgdocdir
pushd %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_pkgdocdir}/headers
for i in `find . -name "*.h.html" -type f -print`; do
    mv $i %{buildroot}%{_pkgdocdir}/headers
done
for i in `find . -name "*.html" -type f -print`; do
    mv $i %{buildroot}%{_pkgdocdir}/headers
done
find . -name "Makefile" -type f -print | xargs /bin/rm -f
popd
cp -a %{name}-%{version}/docs/* %{buildroot}%{_pkgdocdir}
#

%check

%if %{with openmpi}
%if %{with python}
%if %{with pycheck}
pushd buildopenmpi_dir
%{_openmpi_load}
export PETSC_ARCH=%{_arch}
export PETSC_DIR=./
export PYTHONPATH=%{buildroot}$MPI_PYTHON3_SITEARCH
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB
export MPIEXEC=$MPI_BIN/mpiexec
export PMIX_MCA_gds=hash
export PMIX_MCA_psec=native
make V=0 petsc4pytest PETSC4PY_NP=4
#pytest
unset PETSC_ARCH
unset PETSC_DIR
%{_openmpi_unload}
popd
%endif
%endif

%if %{with check}
pushd buildopenmpi_dir
%{_openmpi_load}
export PETSC_DIR=%{_builddir}/%{name}-%{version}/buildopenmpi_dir
export PETSC_ARCH=%{_arch}
export PYTHONPATH=%{buildroot}$MPI_PYTHON3_SITEARCH
export LD_LIBRARY_PATH=${PETSC_DIR}/${PETSC_ARCH}/lib
export MPI_INTERFACE_HOSTNAME=localhost
export OMPI_MCA_btl_base_warn_component_unused=0
export wPETSC_DIR=./
export DATAFILESPATH=%{_builddir}/%{name}-%{version}/buildopenmpi_dir/share/petsc/datafiles
export OMPI_PRTERUN=$MPI_BIN/prterun
export MPIEXEC=$MPI_BIN/mpiexec
export LD_PRELOAD=%{buildroot}$MPI_LIB/libpetsc.so
%if %{with debug}
%ifarch %{valgrind_arches}
export PETSCVALGRIND_OPTIONS=" --tool=memcheck --leak-check=yes --track-origins=yes"
%endif
export CFLAGS="-O0 -g -Wl,-z,now -fPIC"
export CXXFLAGS="-O0 -g -Wl,-z,now -fPIC"
export FFLAGS="-O0 -g -Wl,-z,now -fPIC -I${MPI_FORTRAN_MOD_DIR}"
export TESTFLAGS="-o"
xvfb-run -a make alltests V=1 %{?valgrind_arches:VALGRIND=1} TIMEOUT=240
xvfb-run -a make print-test test-fail=1 | tr ' ' '\n' | sort
%else
xvfb-run -a make check V=1 NP=4
%endif
%{_openmpi_unload}
popd
%endif
%endif

%if %{with mpich}
%if %{with python}
%if %{with pycheck}
pushd buildmpich_dir
%{_mpich_load}
export PETSC_ARCH=%{_arch}
export PETSC_DIR=./
export PYTHONPATH=%{buildroot}$MPI_PYTHON3_SITEARCH
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB
export MPIEXEC=$MPI_BIN/mpiexec
export PMIX_MCA_gds=hash
export PMIX_MCA_psec=native
make V=0 petsc4pytest PETSC4PY_NP=4
unset PETSC_ARCH
unset PETSC_DIR
%{_mpich_unload}
popd
%endif
%endif

%if %{with check}
pushd buildmpich_dir
%{_mpich_load}
export PETSC_DIR=%{_builddir}/%{name}-%{version}/buildmpich_dir
export PETSC_ARCH=%{_arch}
export LD_LIBRARY_PATH=${PETSC_DIR}/${PETSC_ARCH}/lib
export PYTHONPATH=%{buildroot}$MPI_PYTHON3_SITEARCH
export MPI_INTERFACE_HOSTNAME=localhost
export OMPI_MCA_btl_base_warn_component_unused=0
export wPETSC_DIR=./
export DATAFILESPATH=%{_builddir}/%{name}-%{version}/buildmpich_dir/share/petsc/datafiles
export MPIEXEC=$MPI_BIN/mpiexec
export LD_PRELOAD=%{buildroot}$MPI_LIB/libpetsc.so
%if %{with debug}
%ifarch %{valgrind_arches}
export PETSCVALGRIND_OPTIONS=" --tool=memcheck --leak-check=yes --track-origins=yes"
%endif
export CFLAGS="-O0 -g -Wl,-z,now -fPIC"
export CXXFLAGS="-O0 -g -Wl,-z,now -fPIC"
export FFLAGS="-O0 -g -Wl,-z,now -fPIC -I${MPI_FORTRAN_MOD_DIR}"
xvfb-run -a make alltests V=1 %{?valgrind_arches:VALGRIND=1} TIMEOUT=240
xvfb-run -a make print-test test-fail=1 | tr ' ' '\n' | sort
%else
xvfb-run -a make check V=1 NP=4
%endif
%{_mpich_unload}
popd
%endif
%endif

%if %{with check}
pushd %{name}-%{version}
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/%{name}-%{version}/%{_arch}/lib
export PETSC_DIR=%{_builddir}/%{name}-%{version}/%{name}-%{version}
export PETSC_ARCH=%{_arch}
export wPETSC_DIR=./
export DATAFILESPATH=%{_builddir}/%{name}-%{version}/%{name}-%{version}/share/petsc/datafiles
export MPIEXEC=$MPI_BIN/mpiexec
export LD_PRELOAD=%{buildroot}%{_libdir}/libpetsc.so
%if %{with debug}
%ifarch %{valgrind_arches}
export PETSCVALGRIND_OPTIONS=" --tool=memcheck --leak-check=yes --track-origins=yes"
%endif
export CFLAGS="-O0 -g -Wl,-z,now -fPIC"
export CXXFLAGS="-O0 -g -Wl,-z,now -fPIC"
export FFLAGS="-O0 -g -Wl,-z,now -fPIC -I%{_libdir}/gfortran/modules"
xvfb-run -a make alltests V=1 %{?valgrind_arches:VALGRIND=1} TIMEOUT=240
xvfb-run -a make print-test test-fail=1 | tr ' ' '\n' | sort
%else
xvfb-run -a make check V=1
%endif
popd

%if %{with arch64}
pushd build64
export LD_LIBRARY_PATH=%{_libdir}:%{_builddir}/%{name}-%{version}/build64/%{_arch}/lib
export PETSC_DIR=%{_builddir}/%{name}-%{version}/build64
export PETSC_ARCH=%{_arch}
export wPETSC_DIR=./
export DATAFILESPATH=%{_builddir}/%{name}-%{version}/build64/share/petsc/datafiles
export MPIEXEC=$MPI_BIN/mpiexec

## 'make test' needs to link against -lpetsc
ln -s %{_builddir}/%{name}-%{version}/build64/%{_arch}/lib/libpetsc64.so %{_builddir}/%{name}-%{version}/build64/%{_arch}/lib/libpetsc.so
export LD_PRELOAD=%{_builddir}/%{name}-%{version}/build64/%{_arch}/lib/libpetsc.so

%if %{with debug}
%ifarch %{valgrind_arches}
export PETSCVALGRIND_OPTIONS=" --tool=memcheck --leak-check=yes --track-origins=yes"
%endif
export CFLAGS="-O0 -g -Wl,-z,now -fPIC"
export CXXFLAGS="-O0 -g -Wl,-z,now -fPIC"
export FFLAGS="-O0 -g -Wl,-z,now -fPIC -I%{_libdir}/gfortran/modules"
xvfb-run -a make alltests V=1 %{?valgrind_arches:VALGRIND=1} TIMEOUT=240
xvfb-run -a make print-test test-fail=1 | tr ' ' '\n' | sort
%else
xvfb-run -a make check V=0
%endif
popd
%endif
%endif

%files
%license %{name}-%{version}/LICENSE
%{_libdir}/libpetsc.so.3
%{_libdir}/libpetsc.so.%{releasever}
%{_libdir}/libpetsc.so.%{version}

%files devel
%{_libdir}/pkgconfig/PETSc.pc
%{_libdir}/pkgconfig/petsc.pc
%{_libdir}/%{name}/
%{_libdir}/libpetsc.so
%{_includedir}/%{name}/
%{_fmoddir}/%{name}/

%files doc
%license %{name}-%{version}/LICENSE
%{_pkgdocdir}/

%if %{with arch64}
%files -n petsc64
%license build64/LICENSE
%{_libdir}/libpetsc64.so.3
%{_libdir}/libpetsc64.so.%{releasever}
%{_libdir}/libpetsc64.so.%{version}

%files -n petsc64-devel
%{_libdir}/pkgconfig/PETSc64.pc
%{_libdir}/pkgconfig/petsc64.pc
%{_libdir}/%{name}64/
%{_libdir}/libpetsc64.so
%{_includedir}/%{name}64/
%{_fmoddir}/%{name}64/
%endif

%if %{with openmpi}
%files openmpi
%license buildopenmpi_dir/LICENSE
%{_libdir}/openmpi/lib/libpetsc.so.3
%{_libdir}/openmpi/lib/libpetsc.so.%{releasever}
%{_libdir}/openmpi/lib/libpetsc.so.%{version}

%files openmpi-devel
%{_libdir}/openmpi/lib/libpetsc.so
%{_libdir}/openmpi/lib/%{name}/
%{_libdir}/openmpi/lib/pkgconfig/PETSc.pc
%{_libdir}/openmpi/lib/pkgconfig/petsc.pc
%{_includedir}/openmpi-%{_arch}/%{name}/
%{_fmoddir}/openmpi/%{name}/

%if %{with python}
%files -n python3-%{name}-openmpi
%{python3_sitearch}/openmpi/%{pymodule_name}/
%{python3_sitearch}/openmpi/%{pymodule_name}-%{pymodule_version}-py%{python3_version}.egg-info
%endif
%endif

%if %{with mpich}
%files mpich
%license buildmpich_dir/LICENSE
%{_libdir}/mpich/lib/libpetsc.so.3
%{_libdir}/mpich/lib/libpetsc.so.%{releasever}
%{_libdir}/mpich/lib/libpetsc.so.%{version}

%files mpich-devel
%{_libdir}/mpich/lib/libpetsc.so
%{_libdir}/mpich/lib/%{name}/
%{_libdir}/mpich/lib/pkgconfig/PETSc.pc
%{_libdir}/mpich/lib/pkgconfig/petsc.pc
%{_includedir}/mpich-%{_arch}/%{name}/
%{_fmoddir}/mpich/%{name}/

%if %{with python}
%files -n python3-%{name}-mpich
%{python3_sitearch}/mpich/%{pymodule_name}/
%{python3_sitearch}/mpich/%{pymodule_name}-%{pymodule_version}-py%{python3_version}.egg-info
%endif
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 3.23.6-6
- Latest state for petsc

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.23.6-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Sat Sep 06 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.6-4
- Disable python tests

* Thu Sep 04 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.6-3
- Modify Python test commands

* Tue Sep 02 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.6-2
- Exclude pytest

* Tue Sep 02 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.6-1
- Release 3.23.6| Fix Python-3.14 tests

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.23.5-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 12 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.5-5
- Disable testing on s390x

* Tue Aug 12 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.5-4
- Remove unused sed command

* Tue Aug 12 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.5-3
- Switch back to old py3_build py_install (rhbz#2387582) | See bug ticket
  2377370

* Sat Aug 09 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.5-2
- Build petsc64

* Sat Aug 09 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.5-1
- Release 3.23.5

* Thu Aug 07 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.3-8
- Set PYTHONPATH

* Thu Aug 07 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.3-7
- Disable petsc4py tests temporarily

* Wed Aug 06 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.3-6
- Fix Buildrequires packages

* Wed Aug 06 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.3-5
- Fix rhbz#2377370

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.3-3
- Disable petsc4py tests

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.23.3-2
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.3-1
- Release 3.23.3

* Sat May 10 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.2-1
- Release 3.23.0 (rhbz#2365411)

* Thu May 01 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.1-1
- Release 3.23.1

* Sun Apr 27 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.23.0-1
- Release 3.23.0

* Thu Apr 10 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.22.5-1
- Release 3.22.5

* Mon Mar 31 2025 Andrea Bolognani <abologna@redhat.com> - 3.22.4-4
- Fix valgrind checks

* Sun Mar 30 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.22.4-3
- Fix ricsv64 builds

* Thu Mar 06 2025 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.22.4-2
- Rebuild for scalapack SONAME change.

* Sun Mar 02 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.22.4-1
- Release 3.22.4

* Fri Jan 31 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.22.3-1
- Release 3.22.3

* Sun Jan 19 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.22.2-7
- Use valgrind correctly

* Sun Jan 19 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.22.2-6
- Make make check more verbose

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 30 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.22.2-4
- Fix popd commands

* Sun Dec 29 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.22.2-3
- Disable testing on s390x

* Sun Dec 29 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.22.2-2
- Simplify PETSc's libraries testing

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.22.2-1
- Release 3.22.2|Rebuild for MUMPS-5.7.3|Silence test verbosity

* Fri Nov 22 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-14
- Rebuild for openmpi-5.0.6 (rhbz#2328137)

* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 3.20.6-13
- Rebuild for hdf5 1.14.5

* Fri Sep 13 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-12
- Rebuild for MPICH-4.2.2

* Thu Sep 05 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-11
- Rebuild for SuperLU-7.0.0

* Fri Aug 16 2024 Sandro Mani <manisandro@gmail.com> - 3.20.6-10
- Rebuild (scotch-7.0.4)

* Tue Aug 06 2024 David Bold <dave@ipp.mpg.de> - 3.20.6-9
- Fix configure script for python3.13

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 3.20.6-7
- Rebuilt for Python 3.13

* Fri Apr 26 2024 Orion Poplawski <orion@nwra.com> - 3.20.6-6
- Rebuild for openmpi 5.0.3

* Sun Apr 21 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-5
- Rebuild for MPICH-4.2.1

* Wed Apr 10 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-4
- Release number bump

* Mon Apr 01 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-3
- Reload Cython3 files for EPEL9 builds

* Mon Apr 01 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-2
- Fix Scotch MPI include directories in RHEL

* Sun Mar 31 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.6-1
- Release 3.20.6 (rhbz#2272217)

* Mon Mar 04 2024 David Abdurachmanov <davidlt@rivosinc.com> - 3.20.5-3
- Properly check for valgrind support

* Sat Mar 02 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.5-2
- Release 3.20.5 (rhbz#2266220) |Drop incorporated patch

* Sat Mar 02 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.5-1
- Release 3.20.5 (rhbz#2266220)

* Thu Feb 08 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.4-4
- Move up patch #8

* Thu Feb 08 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.4-3
- Fix upstream bug #1542

* Tue Feb 06 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.4-2
- Patched for using metis64

* Tue Feb 06 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.4-1
- Release 3.20.4

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 06 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.20.2-5
- Rebuild for MUMPS-5.6.2

* Sun Dec 24 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.20.2-4
- Rebuild for openmpi-5.0.1

* Sat Dec 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.20.2-3
- Rebuild for superlu_dist-8.2.0

* Sun Dec 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.20.2-2
- Fix License tag

* Sun Dec 03 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.20.2-1
- Release 3.20.2

* Sun Nov 05 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.20.1-2
- Disable Python test for missing epydoc module

* Wed Nov 01 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.20.1-1
- Release 3.20.1

* Sun Oct 29 2023 Orion Poplawski <orion@nwra.com> - 3.20.0-4
- Properly conditionalize the python mpi sub-packages

* Sun Oct 29 2023 Orion Poplawski <orion@nwra.com> - 3.20.0-3
- Rework conditional

* Sun Oct 29 2023 Orion Poplawski <orion@nwra.com> - 3.20.0-2
- Rebuild for openmpi 5.0.0, drops support for i686

* Sun Oct 15 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.20.0-1
- Release 3.20.0

* Fri Sep 29 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.6-1
- Release 3.19.6| Fix ELN builds

* Fri Aug 18 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-9
- Disable petsc4py's tests

* Thu Aug 17 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-8
- Rebuild for Scotch-7.0.4| Enable tests

* Thu Aug 17 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-7
- Rebuild for Scotch-7.0.4

* Sun Aug 13 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-6
- Remove superfluous source archive

* Fri Aug 11 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-5
- Release 3.19.4 | Fix BR packages

* Fri Aug 11 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-4
- Release 3.19.4 | Fix Cython requirement 2

* Fri Aug 11 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-3
- Release 3.19.4 | Fix Cython requirement

* Fri Aug 11 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-2
- Release 3.19.4 | Exclude removing pre-generated Cython files

* Thu Aug 10 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.19.4-1
- Release 3.19.4

* Sat Jul 29 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-17
- Fix macros

* Wed Jul 26 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-16
- Add python-wheel BR

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.18.5-14
- Rebuild for mpich-4.1.2

* Sat Jul 15 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-13
- Rebuild for SuperLU-6.0.0| Re-enable tests

* Thu Jul 06 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-12
- Disable tests

* Thu Jun 22 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-11
- Update patch for Python-3.12| Enable python tests on Power64 builds

* Wed Jun 21 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-10
- Patched for Python-3.12

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 3.18.5-9
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-8
- Enable tests

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.18.5-7
- Rebuilt for Python 3.12

* Wed May 24 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.18.5-6
- Disable tests
## END: Generated by rpmautospec
