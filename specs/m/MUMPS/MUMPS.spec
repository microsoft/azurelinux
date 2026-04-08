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

## Define libraries' destination
%global _incmpidir %{_includedir}/openmpi-%{_arch}
%global _libmpidir %{_libdir}/openmpi/lib
%global _incmpichdir %{_includedir}/mpich-%{_arch}
%global _libmpichdir %{_libdir}/mpich/lib

%global soname_version 5.7

# Prevent broken links 
%undefine _ld_as_needed

# Due to OpenMPI-5.0 dropping in i686
%if 0%{?rhel} || 0%{?fedora}
%ifarch %{ix86}
%global with_openmpi 0
%global with_openmpi_check 0
%else
%global with_openmpi 1
%global with_openmpi_check 1
%endif
# rhbz#2225803
%ifnarch s390x
%global with_mpich_check 1
%else
%global with_mpich_check 0
%endif
%global with_mpich 1
%endif

## Due to rhbz#1744780
%if 0%{?rhel}
%global with_mpich 1
%global with_mpich_check 1
%global with_openmpi 1
%global with_openmpi_check 1
%endif

# Workarounf for GCC-10
# https://gcc.gnu.org/gcc-10/porting_to.html
%if 0%{?fedora} || 0%{?rhel} >= 9
%global build_fflags %{build_fflags} -fallow-argument-mismatch
%endif

Name: MUMPS
Version: %{soname_version}.3
Release: %autorelease
Summary: A MUltifrontal Massively Parallel sparse direct Solver
License: CECILL-C
URL: https://mumps-solver.org
Source0: https://mumps-solver.org/%{name}_%{version}.tar.gz

# Custom Makefile changed for Fedora and built from Make.inc/Makefile.gfortran.PAR in the source.
Source1: %{name}-Makefile.par.inc

# Custom Makefile changed for Fedora and built from Make.inc/Makefile.gfortran.SEQ in the source.
Source2: %{name}-Makefile.seq.inc

# These patches create static and shared versions of pord, sequential and mumps libraries
# They are changed for Fedora and  derive from patches for Debian on 
# http://bazaar.launchpad.net/~ubuntu-branches/ubuntu/raring/mumps/raring/files/head:/debian/patches/
Patch0: %{name}-examples-mpilibs.patch
Patch1: %{name}-shared-pord.patch
Patch2: %{name}-shared.patch
Patch3: %{name}-shared-seq.patch

BuildRequires: make
BuildRequires: gcc-gfortran
BuildRequires: gcc
BuildRequires: pkgconfig(flexiblas)
BuildRequires: metis-devel
BuildRequires: scotch-devel >= 7.0.1
BuildRequires: scotch-devel-metis >= 7.0.1

BuildRequires: openssh-clients
BuildRequires: hwloc-devel
Requires:      %{name}-common = %{version}-%{release}

Obsoletes: %{name}-openmp < 0:5.4.0-1

%description
MUMPS implements a direct solver for large sparse linear systems, with a
particular focus on symmetric positive definite matrices.  It can
operate on distributed matrices e.g. over a cluster.  It has Fortran and
C interfaces, and can interface with ordering tools such as Scotch.

%package devel
Summary: The MUMPS headers and development-related files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran%{?_isa}
Requires: %{name}-srpm-macros = %{version}-%{release}
# FlexiBLAS takes advantage of openblas-openmp by default.
# OpenMP sub-package will be obsoleted in future.
Obsoletes: %{name}-openmp-devel < 0:5.4.0-1

%description devel
Shared links and header files.
This package contains dummy MPI header file 
including symbols used by MUMPS.

%package examples
Summary: The MUMPS common illustrative test programs
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
This package contains common illustrative
test programs about how MUMPS can be used.

%package common
Summary: Documentation files for MUMPS
BuildArch: noarch
%description common
This package contains common documentation files for MUMPS.

%package srpm-macros
Summary: Additional RPM macros for MUMPS
BuildArch: noarch
%description srpm-macros
Additional RPM macros for MUMPS.

########################################################
%if 0%{?with_openmpi}
%package openmpi
Summary: MUMPS libraries compiled against openmpi

BuildRequires: openmpi-devel
BuildRequires: blacs-openmpi-devel
BuildRequires: scalapack-openmpi-devel
#BuildRequires: metis-devel
BuildRequires: ptscotch-openmpi-devel >= 7.0.1
BuildRequires: ptscotch-openmpi-devel-parmetis >= 7.0.1
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif
Requires: %{name}-common = %{version}-%{release}
Requires: openmpi%{?_isa}
Requires: scalapack-openmpi%{?_isa}
Requires: ptscotch-openmpi%{?_isa} >= 7.0.1

%description openmpi
MUMPS libraries compiled against openmpi.

%package openmpi-devel
Summary: The MUMPS headers and development-related files
BuildRequires: openmpi-devel
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran%{?_isa}
Requires: %{name}-srpm-macros = %{version}-%{release}
%if 0%{?fedora}
Requires: rpm-mpi-hooks
%endif
%description openmpi-devel
Shared links, header files for MUMPS.

%package openmpi-examples
Summary: The MUMPS OpenMPI common illustrative test programs
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: openmpi
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif

%description openmpi-examples
This package contains common illustrative
test programs about how MUMPS-openmpi can be used.
%endif
##########################################################

########################################################
%if 0%{?with_mpich}
%package mpich
Summary: MUMPS libraries compiled against MPICH

BuildRequires: mpich-devel
BuildRequires: blacs-mpich-devel
BuildRequires: scalapack-mpich-devel
#BuildRequires: metis-devel
BuildRequires: ptscotch-mpich-devel >= 7.0.1
BuildRequires: ptscotch-mpich-devel-parmetis >= 7.0.1
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif
Requires: %{name}-common = %{version}-%{release}
Requires: mpich%{?_isa}
Requires: scalapack-mpich%{?_isa}
Requires: ptscotch-mpich%{?_isa} >= 7.0.1

%description mpich
MUMPS libraries compiled against MPICH.

%package mpich-devel
Summary: The MUMPS headers and development-related files
BuildRequires: mpich-devel
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-srpm-macros = %{version}-%{release}
%if 0%{?fedora}
Requires: rpm-mpi-hooks
%endif
%description mpich-devel
Shared links, header files for MUMPS.

%package mpich-examples
Summary: The MUMPS MPICH common illustrative test programs
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran%{?_isa}
Requires: mpich
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif
%description mpich-examples
This package contains common illustrative
test programs about how MUMPS-mpich can be used.
%endif
##########################################################

%prep
%setup -q -n %{name}_%{version}

%patch -P 0 -p1 -b .examples-mpilibs
%patch -P 1 -p1 -b .shared-pord
%patch -P 2 -p1 -b .shared

mv examples/README examples/README-examples

%build

#######################################################
## Build MPI version
rm -f Makefile.inc
%if 0%{?with_openmpi}
%{_openmpi_load}
cp -f %{SOURCE1} Makefile.inc

%if 0%{?fedora}
%global mpif77_cflags %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --cflags ompi-f77)
%global mpif77_libs %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --libs ompi-f77)
%global mpifort_cflags %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --cflags ompi-fort)
%global mpifort_libs %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --libs ompi-fort)
%global mpic_libs %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --libs ompi)
%endif
%if 0%{?rhel}
%global mpif77_cflags -I%{_incmpidir}
%global mpif77_libs -lmpi_mpifh
%global mpifort_cflags -I%{_incmpidir}
%global mpifort_libs -lmpi_mpifh
%global mpic_libs -lmpi
%endif

# Set build flags macro
sed -e 's|@@FFLAGS@@|%{build_fflags} -fPIC -Dscotch -Dmetis -Dptscotch -DWITHOUT_PTHREAD -DINTSIZE32 -I${MPI_FORTRAN_MOD_DIR}|g' -i Makefile.inc
sed -e 's|@@CFLAGS@@|%{build_cflags} -fPIC -Dscotch -Dmetis -Dptscotch -DWITHOUT_PTHREAD -DINTSIZE32|g' -i Makefile.inc
sed -e 's|@@LDFLAGS@@|%{__global_ldflags}|g' -i Makefile.inc
sed -e 's|@@MPICLIB@@|-lmpi|g' -i Makefile.inc

%if 0%{?rhel}
sed -e 's|@@MPIFORTRANLIB@@|-L%{_libmpidir} -Wl,-rpath -Wl,%{_libmpidir} %{mpif77_libs}|g' -i Makefile.inc
%endif

%if 0%{?fedora}
sed -e 's|@@MPIFORTRANLIB@@|%{mpifort_libs}|g' -i Makefile.inc
%endif

MUMPS_MPI=openmpi
MUMPS_INCDIR=-I$MPI_INCLUDE
LMETISDIR=%{_libdir}
LMETIS="-lmetis -L$MPI_LIB -lptscotchparmetis"
IMETIS=-I%{_includedir}
#IMETIS=-I$MPI_LIB/scotch
SCOTCHDIR=$MPI_LIB
ISCOTCH=-I$MPI_INCLUDE/scotch
LSCOTCH=" -L$MPI_LIB -lesmumps -lscotch -lscotcherr -lptesmumps -lptscotch -lptscotcherr"
IPORD=" -I$PWD/PORD/include/"
LPORD=" -L$PWD/PORD/lib -lpord"
FPIC_OPT=-fPIC

%if 0%{?rhel} && 0%{?rhel} < 9
export MPIBLACSLIBS="-L$MPI_LIB -lmpiblacs"
%else
export MPIBLACSLIBS=""
%endif
export MPI_COMPILER_NAME=openmpi
export LD_LIBRARY_PATH="$MPI_LIB:%{_libdir}"
export LDFLAGS="%{__global_ldflags}"

mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/lib
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/examples
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/modules

export LIBBLAS="-L%{_libdir} -lflexiblas"
export INCBLAS=-I%{_includedir}/flexiblas

make all \
 SONAME_VERSION=%{soname_version} \
 CC=$MPI_BIN/mpicc \
 FC=$MPI_BIN/mpif77 \
 FL=$MPI_BIN/mpif77 \
 MUMPS_MPI="$MUMPS_MPI" \
 MUMPS_INCDIR="$MUMPS_INCDIR $INCBLAS" \
 MUMPS_LIBF77="${LIBBLAS} -L$MPI_LIB -Wl,-rpath -Wl,$MPI_LIB %{mpic_libs} $MPIFORTRANSLIB -lscalapack $MPIBLACSLIBS" \
 LMETISDIR="$LMETISDIR" LMETIS="$LMETIS" IMETIS="$IMETIS" \
 SCOTCHDIR=$SCOTCHDIR \
 ISCOTCH=$ISCOTCH \
 LSCOTCH="$LSCOTCH" \
 IPORD="$IPORD" \
 LPORD="$LPORD" \
 OPTL="%{__global_ldflags}"
%{_openmpi_unload}
cp -pr lib/* %{name}-%{version}-$MPI_COMPILER_NAME/lib
cp -pr examples/* %{name}-%{version}-$MPI_COMPILER_NAME/examples
rm -rf lib/*
cp -a include %{name}-%{version}-$MPI_COMPILER_NAME/
cp -pr src/*.mod %{name}-%{version}-$MPI_COMPILER_NAME/modules
make clean
%endif

######################################################
#######################################################
## Build MPICH version
%if 0%{?with_mpich}
rm -f Makefile.inc
cp -f %{SOURCE1} Makefile.inc

# -DBLR_MT needs OpenMP
sed -e 's| -DBLR_MT||g' -i Makefile.inc

%{_mpich_load}
%global mpif77_cflags %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --cflags mpich)
%global mpif77_libs %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --libs mpich)
%global mpifort_cflags %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --cflags mpich)
%global mpifort_libs %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --libs mpich)
%global mpich_libs %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --libs mpich)

# Set build flags macro
sed -e 's|@@FFLAGS@@|%{build_fflags} -fPIC -Dscotch -Dmetis -Dptscotch -DWITHOUT_PTHREAD -DINTSIZE32 -I${MPI_FORTRAN_MOD_DIR}|g' -i Makefile.inc
sed -e 's|@@LDFLAGS@@|%{__global_ldflags}|g' -i Makefile.inc
sed -e 's|@@CFLAGS@@|%{build_cflags} -fPIC -Dscotch -Dmetis -Dptscotch -DWITHOUT_PTHREAD -DINTSIZE32|g' -i Makefile.inc
sed -e 's|@@MPICLIB@@|-lmpich|g' -i Makefile.inc
sed -e 's|@@MPIFORTRANLIB@@|%{mpifort_libs}|g' -i Makefile.inc

MUMPS_MPI=mpich
MUMPS_INCDIR=-I$MPI_INCLUDE
LMETISDIR=$MPI_LIB
LMETIS="-lmetis -L$MPI_LIB -lptscotchparmetis"
IMETIS=-I%{_includedir}
#IMETIS=-I$MPI_LIB/scotch
SCOTCHDIR=$MPI_LIB
ISCOTCH=-I$MPI_INCLUDE/scotch
LSCOTCH="-L$MPI_LIB -lesmumps -lscotch -lscotcherr -lptesmumps -lptscotch -lptscotcherr"
export IPORD=" -I$PWD/PORD/include/"
export LPORD=" -L$PWD/PORD/lib -lpord"
FPIC_OPT=-fPIC

%if 0%{?rhel} && 0%{?rhel} < 9
export MPIBLACSLIBS="-L$MPI_LIB -lmpiblacs"
%else
export MPIBLACSLIBS=""
%endif
export MPI_COMPILER_NAME=mpich
export LD_LIBRARY_PATH=$MPI_LIB:%{_libdir}
export LDFLAGS="%{__global_ldflags}"

mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/lib
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/examples
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/modules

export LIBBLAS="-L%{_libdir} -lflexiblas"
export INCBLAS=-I%{_includedir}/flexiblas

make all \
 SONAME_VERSION=%{soname_version} \
 CC=$MPI_BIN/mpicc \
 FC=$MPI_BIN/mpif77 \
 FL=$MPI_BIN/mpif77 \
 MUMPS_MPI="$MUMPS_MPI" \
 MUMPS_INCDIR="$MUMPS_INCDIR $INCBLAS" \
 MUMPS_LIBF77="${LIBBLAS} -L$MPI_LIB %{mpich_libs} $MPIFORTRANSLIB -lscalapack $MPIBLACSLIBS" \
 LMETISDIR="$LMETISDIR" LMETIS="$LMETIS" IMETIS="$IMETIS" \
 SCOTCHDIR=$SCOTCHDIR \
 ISCOTCH=$ISCOTCH \
 LSCOTCH="$LSCOTCH" \
 IPORD="$IPORD" \
 LPORD="$LPORD" \
 OPTL="%{__global_ldflags}"
%{_mpich_unload}
cp -pr lib/* %{name}-%{version}-$MPI_COMPILER_NAME/lib
cp -pr examples/* %{name}-%{version}-$MPI_COMPILER_NAME/examples
cp -a include %{name}-%{version}-$MPI_COMPILER_NAME/
rm -rf lib/*
cp -pr src/*.mod %{name}-%{version}-$MPI_COMPILER_NAME/modules
make clean
%endif

######################################################

patch -p1 < %{PATCH3}

## Build serial version
rm -f Makefile.inc
cp -f %{SOURCE2} Makefile.inc

# -DBLR_MT needs OpenMP
sed -e 's| -DBLR_MT||g' -i Makefile.inc

# Set build flags macro
sed -e 's|@@FFLAGS@@|%{build_fflags} -fPIC -Dscotch -Dmetis -DWITHOUT_PTHREAD -DINTSIZE32|g' -i Makefile.inc
sed -e 's|@@LDFLAGS@@|%{__global_ldflags}|g' -i Makefile.inc
sed -e 's|@@CFLAGS@@|%{build_cflags} -fPIC -Dscotch -Dmetis -DWITHOUT_PTHREAD -DINTSIZE32|g' -i Makefile.inc


mkdir -p %{name}-%{version}/lib
mkdir -p %{name}-%{version}/examples
mkdir -p %{name}-%{version}/modules

IPORD=" -I$PWD/PORD/include/"
LPORD=" -L$PWD/PORD/lib -lpord"
FPIC_OPT=-fPIC

export LIBBLAS="-L%{_libdir} -lflexiblas"
export INCBLAS=-I%{_includedir}/flexiblas

export LDFLAGS="%{__global_ldflags}"
make all \
 SONAME_VERSION=%{soname_version} \
 CC=gcc \
 FC=gfortran \
 FL=gfortran \
 MUMPS_LIBF77="${LIBBLAS}" \
 LIBBLAS="${LIBBLAS}" \
 LIBOTHERS=" -lpthread" \
 LIBSEQ="-L../libseq -lmpiseq" \
 INCSEQ="-I../libseq $INCBLAS" \
 LMETISDIR=%{_libdir} \
 IMETIS=-I%{_includedir} \
 LMETIS="-L%{_libdir} -lmetis -lscotchmetis" \
 SCOTCHDIR=%{_prefix} \
 ISCOTCH=-I%{_includedir}/scotch \
 LSCOTCH=" -L%{_libdir} -lesmumps -lscotch -lscotcherr" \
 IPORD="$IPORD" \
 LPORD="$LPORD" \
 OPTL="%{__global_ldflags}"
make -C examples
cp -pr lib/* %{name}-%{version}/lib
cp -pr examples/* %{name}-%{version}/examples
cp -a include %{name}-%{version}/
rm -rf lib/*
cp -pr src/*.mod %{name}-%{version}/modules
make clean
#######################################################

# Make sure documentation is using Unicode.
iconv -f iso8859-1 -t utf-8 README > README-t && mv README-t README

%check
# Running test programs
pushd %{name}-%{version}/examples
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
 ./ssimpletest < input_simpletest_real
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
 ./dsimpletest < input_simpletest_real
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
 ./csimpletest < input_simpletest_cmplx
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
 ./zsimpletest < input_simpletest_cmplx
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
 ./c_example
popd

%if 0%{?with_openmpi_check}
%{_openmpi_load}
pushd %{name}-%{version}-openmpi/examples
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT$MPI_LIB
./ssimpletest < input_simpletest_real
./dsimpletest < input_simpletest_real
./csimpletest < input_simpletest_cmplx
./zsimpletest < input_simpletest_cmplx
mpirun -np 3 ./c_example
popd
%{_openmpi_unload}
%endif

%if 0%{?with_mpich_check}
%{_mpich_load}
pushd %{name}-%{version}-mpich/examples
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT$MPI_LIB
./ssimpletest < input_simpletest_real
./dsimpletest < input_simpletest_real
./csimpletest < input_simpletest_cmplx
./zsimpletest < input_simpletest_cmplx
mpirun -np 3 ./c_example
popd
%{_mpich_unload}
%endif

%install

#########################################################
%if 0%{?with_openmpi}
%{_openmpi_load}
mkdir -p $RPM_BUILD_ROOT$MPI_LIB
mkdir -p $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples
mkdir -p $RPM_BUILD_ROOT$MPI_INCLUDE
mkdir -p $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}

# Install libraries.
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*-*.so $RPM_BUILD_ROOT$MPI_LIB

# Install development files.
install -cpm 755 %{name}-%{version}-openmpi/lib/libmumps_common.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*mumps.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*mumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/libpord.so $RPM_BUILD_ROOT$MPI_LIB

# Make symbolic links instead hard-link 
ln -sf libsmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libsmumps.so
ln -sf libcmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libcmumps.so
ln -sf libzmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libzmumps.so
ln -sf libdmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libdmumps.so
ln -sf libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libmumps_common.so
ln -sf libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libpord.so

install -cpm 755 %{name}-%{version}-openmpi/examples/?simpletest $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-openmpi/examples/input_* $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-openmpi/examples/README-* $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples

install -cpm 644 %{name}-%{version}-openmpi/include/*.h $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 PORD/include/* $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 %{name}-%{version}-openmpi/modules/* $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}/
%{_openmpi_unload}
%endif
##########################################################

#########################################################
%if 0%{?with_mpich}
%{_mpich_load}
mkdir -p $RPM_BUILD_ROOT$MPI_LIB
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples
mkdir -p $RPM_BUILD_ROOT$MPI_INCLUDE
mkdir -p $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}

# Install libraries.
install -cpm 755 %{name}-%{version}-mpich/lib/lib*-*.so $RPM_BUILD_ROOT$MPI_LIB

# Install development files.
install -cpm 755 %{name}-%{version}-mpich/lib/libmumps_common.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/lib*mumps.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/lib*mumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/libpord.so $RPM_BUILD_ROOT$MPI_LIB

# Make symbolic links instead hard-link 
ln -sf libsmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libsmumps.so
ln -sf libcmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libcmumps.so
ln -sf libzmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libzmumps.so
ln -sf libdmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libdmumps.so
ln -sf libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libmumps_common.so
ln -sf libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libpord.so

install -cpm 755 %{name}-%{version}-mpich/examples/?simpletest $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-mpich/examples/input_* $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-mpich/examples/README-* $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples

install -cpm 644 %{name}-%{version}-mpich/include/*.h $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 PORD/include/* $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 %{name}-%{version}-mpich/modules/* $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}/
%{_mpich_unload}
%endif
##########################################################

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_fmoddir}/%{name}-%{version}

# Install libraries.
install -cpm 755 %{name}-%{version}/lib/lib*-*.so $RPM_BUILD_ROOT%{_libdir}/

# Make symbolic links instead hard-link 
ln -sf libsmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libsmumps.so
ln -sf libcmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libcmumps.so
ln -sf libzmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libzmumps.so
ln -sf libdmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libdmumps.so
ln -sf libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libmumps_common.so
ln -sf libpord-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libpord.so
ln -sf libmpiseq-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libmpiseq.so

install -cpm 755 %{name}-%{version}/examples/?simpletest $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 755 %{name}-%{version}/examples/input_* $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 755 %{name}-%{version}/examples/README-* $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 644 %{name}-%{version}/modules/* $RPM_BUILD_ROOT%{_fmoddir}/%{name}-%{version}/

install -cpm 644 %{name}-%{version}/include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -cpm 644 libseq/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -cpm 644 PORD/include/* $RPM_BUILD_ROOT%{_includedir}/%{name}

# rpm macro for version checking
mkdir -p $RPM_BUILD_ROOT%{_rpmmacrodir}
cat > $RPM_BUILD_ROOT%{_rpmmacrodir}/macros.MUMPS <<EOF
# MUMPS version is
%%_MUMPS_version %{version}
EOF

#######################################################
%if 0%{?with_openmpi}
%files openmpi
%{_libmpidir}/libpord-%{soname_version}.so
%{_libmpidir}/lib?mumps-%{soname_version}.so
%{_libmpidir}/libmumps_common-%{soname_version}.so

%files openmpi-devel
%{_incmpidir}/*.h
%{_libmpidir}/lib?mumps.so
%{_libmpidir}/libmumps_common.so
%{_libmpidir}/libpord.so
%{_fmoddir}/openmpi/%{name}-%{version}/

%files openmpi-examples
%{_libdir}/openmpi/%{name}-%{version}-examples/
%endif
#######################################################

#######################################################
%if 0%{?with_mpich}
%files mpich
%{_libmpichdir}/libpord-%{soname_version}.so
%{_libmpichdir}/lib?mumps-%{soname_version}.so
%{_libmpichdir}/libmumps_common-%{soname_version}.so

%files mpich-devel
%{_incmpichdir}/*.h
%{_libmpichdir}/lib?mumps.so
%{_libmpichdir}/libmumps_common.so
%{_libmpichdir}/libpord.so
%{_fmoddir}/mpich/%{name}-%{version}/

%files mpich-examples
%{_libdir}/mpich/%{name}-%{version}-examples/
%endif
#######################################################

%files
%{_libdir}/libpord-%{soname_version}.so
%{_libdir}/libmpiseq-%{soname_version}.so
%{_libdir}/lib?mumps-%{soname_version}.so
%{_libdir}/libmumps_common-%{soname_version}.so

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_fmoddir}/%{name}-%{version}/
%{_libdir}/lib?mumps.so
%{_libdir}/libmumps_common.so
%{_libdir}/libpord.so
%{_libdir}/libmpiseq.so

%files examples
%{_libexecdir}/%{name}-%{version}/

%files common
%doc doc/*.pdf ChangeLog README
%license LICENSE

%files srpm-macros
%{_rpmmacrodir}/macros.MUMPS

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 5.7.3-5
- Latest state for MUMPS

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 06 2025 Ralf Corsépius <corsepiu@fedoraproject.org> - 5.7.3-3
- Rebuild for scalapack SONAME change.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 5.7.3-1
- Release 5.7.3

* Fri Aug 16 2024 Sandro Mani <manisandro@gmail.com> - 5.6.2-9
- Rebuild (scotch-7.0.4)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 28 2024 Antonio Trande <sagitter@fedoraproject.org> - 5.6.2-7
- Use rhel macro instead of eln (rhbz#2271816)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Antonio Trande <sagitter@fedoraproject.org> - 5.6.2-4
- Re-organize conditional macros

* Fri Jan 05 2024 Antonio Trande <sagitter@fedoraproject.org> - 5.6.2-3
- Disable MPICH tests

* Fri Jan 05 2024 Antonio Trande <sagitter@fedoraproject.org> - 5.6.2-2
- Disable MPICH tests

* Fri Jan 05 2024 Antonio Trande <sagitter@fedoraproject.org> - 5.6.2-1
- Release 5.6.2

* Thu Aug 17 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.5.1-8
- Fix patch commands

* Thu Aug 17 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.5.1-7
- Rebuild for Scotch-7.0.4

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.5.1-5
- Rebuild for Scotch-7

* Tue Feb 21 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.5.1-4
- Disable OpenMPI tests in Fedora 38+ i686 |Erase typo

* Tue Feb 21 2023 Antonio Trande <sagitter@fedoraproject.org>
- Disable OpenMPI tests in Fedora 38+ i686

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 25 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.5.1-1
- Release 5.5.1

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Antonio Trande <sagitter@fedoraproject.org> - 5.5.0-1
- Release 5.5.0| Fix ELN builds

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Sep 11 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.4.1-1
- Release 5.4.1

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Antonio Trande <sagitter@fedoraproject.org> - 5.4.0-1
- Release 5.4.0

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Tom Stellard <tstellar@redhat.com> - 5.3.5-2
- Add BuildRequires: make

* Sun Nov 15 2020 Antonio T <sagitter@fedoraproject.org> - 5.3.5-1
- Release 5.3.5

* Wed Oct 07 2020 sagitter <sagitter@fedoraproject.org> - 5.3.4-1
- Release 5.3.4

* Sun Aug 16 2020 sagitter <sagitter@fedoraproject.org> - 5.3.3-2
- Add a macro to detect the MUMPS version

* Tue Aug 04 2020 sagitter <sagitter@fedoraproject.org> - 5.3.3-1
- Release 5.3.3

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 25 2020 sagitter <sagitter@fedoraproject.org> - 5.3.1-5
- Some notes about openmp sub-package

* Sat Jul 25 2020 Iñaki Úcar <iucar@fedoraproject.org> - 5.3.1-4
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Fri Jul 17 2020 Merlin Mathesius <mmathesi@redhat.com> - 5.3.1-3
- Minor conditional fixes for ELN

* Sat Jun 13 2020 sagitter <sagitter@fedoraproject.org> - 5.3.1-2
- Modified for building on ELN

* Mon Apr 13 2020 sagitter <sagitter@fedoraproject.org> - 5.3.1-1
- Release 5.3.1

* Fri Apr 10 2020 sagitter <sagitter@fedoraproject.org> - 5.3.0-1
- Release 5.3.0

* Wed Apr 08 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-16
- Fix check macros

* Wed Apr 08 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-15
- Fix rhbz#1819796 on epel8

* Thu Apr 02 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-14
- Fix rhbz#1819796

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-12
- Fix OpenMP build flags for GCC-10

* Sat Jan 25 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-11
- Workaround for GCC-10

* Wed Jan 01 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-10
- Explicate ptscotch runtime dependencies

* Wed Jan 01 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-9
- Use libmpiblacs separately with scalapack-2.1.*

* Wed Jan 01 2020 sagitter <sagitter@fedoraproject.org> - 5.2.1-8
- Use libmpiblacs separately on EPEL 7+

* Mon Nov 18 2019 Tom Callaway <spot@fedoraproject.org> - 5.2.1-6
- add BR: hwloc-devel

* Mon Nov 18 2019 Tom Callaway <spot@fedoraproject.org> - 5.2.1-5
- rebuild for scalapack 2.1

* Tue Sep 10 2019 Orion Poplawski <orion@nwra.com> - 5.2.1-4
- Allow openmpi to run with more processes than cores

* Tue Sep 10 2019 Orion Poplawski <orion@nwra.com> - 5.2.1-3
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
