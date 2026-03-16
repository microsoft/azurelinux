%global amd_version_major 3
%global btf_version_major 2
%global camd_version_major 3
%global ccolamd_version_major 3
%global cholmod_version_major 5
%global colamd_version_major 3
%global csparse_version_major 4
%global cxsparse_version_major 4
%global gpuqrengine_version_major 3
%global graphblas_version_major 10
%global klu_cholmod_version_major 2
%global klu_version_major 2
%global lagraph_version_major 1
%global lagraphx_version_major 1
%global ldl_version_major 3
%global paru_version_major 1
%global rbio_version_major 4
%global spex_version_major 3
%global spqr_version_major 4
%global SuiteSparse_config_major 7
%global SuiteSparse_gpuruntime_major 3
%global SuiteSparse_metis_major 5
%global umfpack_version_major 6

### CXSparse is a superset of CSparse, and the two share common header
### names, so it does not make sense to build both. CXSparse is built
### by default, but CSparse can be built instead by defining
### enable_csparse as 1 below.
%global enable_csparse 0

# Whether to build a separate version of libraries linked against an ILP64 BLAS
%if 0%{?__isa_bits} == 64
%global build64 1
%endif

%global suitesparse_builds SuiteSparse %{?build64:SuiteSparse64 SuiteSparse64_}

%global blaslib openblas

# SuiteSparse uses a modified version of metis, so use it
%bcond_with system_metis

%global commit 6ab1e9eb9e67264218ffbdfc25010650da449a39

Name:           suitesparse
Version:        7.11.0
Release:        1%{?dist}
Summary:        A collection of sparse matrix libraries
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# See LICENSE.txt for a breakdown of all licenses:
# Shipped modules licenses:
# * AMD      - BSD-3-Clause
# * BTF      - LGPL-2.1-or-later
# * CAMD     - BSD-3-Clause
# * COLAMD   - BSD-3-Clause
# * CCOLAMD  - BSD-3-Clause
# * CHOLMOD  - LGPL-2.1-or-later AND GPL-2.0-or-later
# * CSparse  - LGPL-2.1-or-later AND BSD-3-Clause
# * CXSparse - LGPL-2.1-or-later AND BSD-3-Clause
# * KLU      - LGPL-2.1-or-later
# * LDL      - LGPL-2.1-or-later
# * RBio     - GPL-2.0-or-later
# * SPQR     - GPL-2.0-or-later
# * UMFPACK  - GPL-2.0-or-later
#
# Not shipped modules licenses:
# * GPUQREngine            - GPL-2.0-or-later
# * GraphBLAS              - Apache-2.0 AND GPL-3.0-or-later
# * SLIP_LU                - LGPL-3.0-or-later OR GPL-2.0-or-later OR (LGPL-3.0-or-later AND GPL-2.0-or-later)
# * MATLAB_Tools           - BSD-3-Clause AND GPL-2.0-or-later
# * Mongoose               - GPL-3.0-only
# * ssget                  - BSD-3-Clause
# * SuiteSparse_GPURuntime - GPL-2.0-or-later

License:        BSD-3-Clause AND LGPL-2.1-or-later AND GPL-2.0-or-later
URL:            http://faculty.cse.tamu.edu/davis/suitesparse.html
Source0:        https://github.com/DrTimothyAldenDavis/SuiteSparse/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  make

BuildRequires:  gmp-devel
%if %{with system_metis}
BuildRequires:  metis-devel
%else
Provides:       bundled(metis) = 5.1.0
%endif
BuildRequires:  %{blaslib}-devel
BuildRequires:  mpfr-devel
# openblas is still required for 64-bit suffixed versions
BuildRequires:  openblas-devel
BuildRequires:  lapack-devel
BuildRequires:  mpfr-devel
BuildRequires:  tbb-devel
BuildRequires:  hardlink

# Not packaged in Fedora
Provides:       bundled(cpu_features) = 0.6.0
# GraphBLAS redefines malloc() so must use bundled versions
Provides:       bundled(lz4) = 1.9.3
Provides:       bundled(zstd) = 1.5.5

Obsoletes:      umfpack <= 5.0.1
Obsoletes:      ufsparse <= 2.1.1
Provides:       ufsparse = %{version}-%{release}

%description
suitesparse is a collection of libraries for computations involving sparse
matrices.  The package includes the following libraries:
  AMD                 approximate minimum degree ordering
  BTF                 permutation to block triangular form (beta)
  CAMD                constrained approximate minimum degree ordering
  COLAMD              column approximate minimum degree ordering
  CCOLAMD             constrained column approximate minimum degree ordering
  CHOLMOD             sparse Cholesky factorization
  CSparse             a concise sparse matrix package
  CXSparse            CSparse extended: complex matrix, int and long int support
  KLU                 sparse LU factorization, primarily for circuit simulation
  LDL                 a simple LDL factorization
  SQPR                a multithread, multifrontal, rank-revealing sparse QR
                      factorization method
  UMFPACK             sparse LU factorization
  SuiteSparse_config  configuration file for all the above packages.
  RBio                read/write files in Rutherford/Boeing format


%package devel
Summary:        Development headers for SuiteSparse
Requires:       %{name} = %{version}-%{release}
Obsoletes:      umfpack-devel <= 5.0.1
Obsoletes:      ufsparse-devel <= 2.1.1
Provides:       ufsparse-devel = %{version}-%{release}

%description devel
The suitesparse-devel package contains files needed for developing
applications which use the suitesparse libraries.


%package static
Summary:        Static version of SuiteSparse libraries
Requires:       %{name}-devel = %{version}-%{release}
Provides:       ufsparse-static = %{version}-%{release}

%description static
The suitesparse-static package contains the statically linkable
version of the suitesparse libraries.


%if 0%{?build64}
%package -n %{name}64
Summary:        A collection of sparse matrix libraries (ILP64 version)

%description -n %{name}64
The suitesparse collection compiled against an ILP64 BLAS library.


%package -n %{name}64-devel
Summary:        Development headers for SuiteSparse (ILP64 version)
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}64 = %{version}-%{release}

%description -n %{name}64-devel
The suitesparse64-devel package contains files needed for developing
applications which use the suitesparse libraries (ILP64 version).


%package -n %{name}64-static
Summary:        Static version of SuiteSparse libraries (ILP64 version)
Requires:       %{name}-devel = %{version}-%{release}

%description -n %{name}64-static
The suitesparse64-static package contains the statically linkable
version of the suitesparse libraries (ILP64 version).


%package -n %{name}64_
Summary:        A collection of sparse matrix libraries (ILP64 version)

%description -n %{name}64_
The suitesparse collection compiled against an ILP64 BLAS library.


%package -n %{name}64_-devel
Summary:        Development headers for SuiteSparse (ILP64 version)
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}64_ = %{version}-%{release}

%description -n %{name}64_-devel
The suitesparse64_-devel package contains files needed for developing
applications which use the suitesparse libraries (ILP64 version) compiled
against a BLAS library with the "64_" symbol name suffix (see openblas-*64_
packages).


%package -n %{name}64_-static
Summary:        Static version of SuiteSparse libraries (ILP64 version)
Requires:       %{name}-devel = %{version}-%{release}

%description -n %{name}64_-static
The suitesparse64_-static package contains the statically linkable
version of the suitesparse libraries (ILP64 version) compiled against a
BLAS library with the "64_" symbol name suffix (see openblas-*64_ packages).
%endif


%package doc
Summary:        Documentation files for SuiteSparse
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.


%prep
%setup -c -q
mkdir Doc Licenses
pushd SuiteSparse-%{version}
#patch 0 -p1 -b .postfix
%if !0%{?enable_csparse}
  sed -i -e /CSparse/d Makefile
%endif
  # Build fails
  sed -i -e /Mongoose/d Makefile
%if %{with system_metis}
  # Remove bundled metis
  rm -r SuiteSparse_metis
  # SuiteSparse looks for SuiteSparse_metis.h specifically
  ln -s %{_includedir}/metis/metis.h include/SuiteSparse_metis.h
%endif

  # Fix pragma ivdep so gcc understands it.
  for fil in $(grep -Frl 'pragma ivdep' .); do
    sed -i.orig 's/pragma ivdep/pragma GCC ivdep/' $fil
    touch -r ${fil}.orig $fil
    rm -f ${fil}.orig
  done

  # drop non-standard -O3
  sed -i -e '/OPTS.*-O3/d' CHOLMOD/SuiteSparse_metis/GKlib/GKlibSystem.cmake

  # collect docs and licenses in one place to ship
  find -iname lesser.txt -o -iname lesserv3.txt -o -iname license.txt -o \
    -iname gpl.txt -o -iname GPLv2.txt -o -iname CONTRIBUTOR-LICENSE.txt -o -iname "SuiteSparse Individual Contributor License Agreement (20241011).pdf" -o -iname license \
    -a -not -type d | while read f; do
        b="${f%%/*}"
        r="${f#$b}"
        x="$(echo "$r" | sed 's|/doc/|/|gi')"
        install -m0644 -D "$f" "../Licenses/$b/$x"
    done

    # Copy documentation files but EXCLUDE License.txt, gpl.txt, GPLv2.txt, lesserv3.txt
  find . -type f \( \
          -iname "*.pdf" -o \
          -iname "ChangeLog" -o \
          -iname "README*" -o \
          -iname "*.txt" \
      \) \
      ! -iname "License.txt" \
      ! -iname "gpl.txt" \
      ! -iname "GPLv2.txt" \
      ! -iname "lesserv3.txt" \
      ! -iname "CONTRIBUTOR-LICENSE.txt" \
      ! -iname "SuiteSparse Individual Contributor License Agreement (20241011).pdf" \
  | while read f; do
      b="${f%%/*}"
      r="${f#$b}"
      x="$(echo "$r" | sed 's|/doc/|/|gi')"
      install -m0644 -D "$f" "../Doc/$b/$x"
  done
popd
%if 0%{?build64}
cp -al SuiteSparse-%{version} SuiteSparse64-%{version}
cp -al SuiteSparse-%{version} SuiteSparse64_-%{version}
%endif

# hardlink duplicate documentation files
hardlink -cv Licenses/

%build
# FindSuiteSparse_config looks for "build"
%global _vpath_builddir build
for build in %{suitesparse_builds}
do
  pushd $build-%{version}
    %set_build_flags
    CMAKE_OPTIONS="-DCMAKE_C_FLAGS_RELEASE:STRING=-DNDEBUG -DCMAKE_CXX_FLAGS_RELEASE:STRING=-DNDEBUG -DCMAKE_Fortran_FLAGS_RELEASE:STRING=-DNDEBUG -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
                   -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCOMPACT=ON"
%if %{with system_metis}
    CMAKE_OPTIONS="$CMAKE_OPTIONS -DSUITESPARSE_METIS_FOUND=true -DSUITESPARSE_METIS_INCLUDE_DIR=%{_includedir}/metis -DSUITESPARSE_METIS_LIBRARIES=%{_libdir}/libmetis.so"
%endif
    # Set flags for ILP64 build
    if [ $build = SuiteSparse64 ]
    then
       CMAKE_OPTIONS="$CMAKE_OPTIONS -DSUITESPARSE_INCLUDEDIR_POSTFIX=$build -DSUITESPARSE_PKGFILEDIR=%{_libdir}/$build -DCMAKE_RELEASE_POSTFIX=64 -DBLA_VENDOR=OpenBLAS -DALLOW_64BIT_BLAS=yes"
       export CFLAGS="$CFLAGS -DBLAS_OPENBLAS_64"
    elif [ $build = SuiteSparse64_ ]
    then
       CMAKE_OPTIONS="$CMAKE_OPTIONS -DSUITESPARSE_INCLUDEDIR_POSTFIX=$build -DSUITESPARSE_PKGFILEDIR=%{_libdir}/$build -DCMAKE_RELEASE_POSTFIX=64_ -DBLA_VENDOR=OpenBLAS -DALLOW_64BIT_BLAS=yes -DBLAS_LIBRARIES=%{_libdir}/libopenblas64_.so"
       export CFLAGS="$CFLAGS -DBLAS_OPENBLAS_64"
    else
       CMAKE_OPTIONS="$CMAKE_OPTIONS -DSUITESPARSE_INCLUDEDIR_POSTFIX=suitesparse -DBLA_VENDOR=OpenBLAS"
    fi   
    %make_build CMAKE_OPTIONS="$CMAKE_OPTIONS" JOBS=%{_smp_build_ncpus}
  popd
done

%install
for build in %{suitesparse_builds}
do
  pushd $build-%{version}
    %make_install
  popd
done

%check
# Build demos as a check
for build in %{suitesparse_builds}
do
  pushd $build-%{version}
    make install DESTDIR=%{buildroot}
  popd
done

%files
%license Licenses
%{_libdir}/libamd.so.%{amd_version_major}*
%{_libdir}/libbtf.so.%{btf_version_major}*
%{_libdir}/libcamd.so.%{camd_version_major}*
%{_libdir}/libccolamd.so.%{ccolamd_version_major}*
%{_libdir}/libcholmod.so.%{cholmod_version_major}*
%{_libdir}/libcolamd.so.%{colamd_version_major}*
%if "%{?enable_csparse}" == "1"
%{_libdir}/libcsparse.so.%{csparse_version_major}*
%endif
%{_libdir}/libcxsparse.so.%{cxsparse_version_major}*
%{_libdir}/libgraphblas.so.%{graphblas_version_major}*
%{_libdir}/libklu_cholmod.so.%{klu_cholmod_version_major}*
%{_libdir}/libklu.so.%{klu_version_major}*
%{_libdir}/liblagraph.so.%{lagraph_version_major}*
%{_libdir}/liblagraphx.so.%{lagraphx_version_major}*
%{_libdir}/libldl.so.%{ldl_version_major}*
%{_libdir}/libparu.so.%{paru_version_major}*
%{_libdir}/librbio.so.%{rbio_version_major}*
%{_libdir}/libspex.so.%{spex_version_major}*
%{_libdir}/libspexpython.so.%{spex_version_major}*
%{_libdir}/libspqr.so.%{spqr_version_major}*
%{_libdir}/libsuitesparseconfig.so.%{SuiteSparse_config_major}*
%{_libdir}/libumfpack.so.%{umfpack_version_major}*

%files devel
%{_includedir}/%{name}/
%{_libdir}/cmake/AMD/
%{_libdir}/cmake/BTF/
%{_libdir}/cmake/CAMD/
%{_libdir}/cmake/CCOLAMD/
%{_libdir}/cmake/CHOLMOD/
%{_libdir}/cmake/COLAMD/
%{_libdir}/cmake/CXSparse/
%{_libdir}/cmake/GraphBLAS/
%{_libdir}/cmake/KLU/
%{_libdir}/cmake/KLU_CHOLMOD/
%{_libdir}/cmake/LAGraph/
%{_libdir}/cmake/LDL/
%{_libdir}/cmake/ParU/
%{_libdir}/cmake/RBio/
%{_libdir}/cmake/SPEX/
%{_libdir}/cmake/SPQR/
%{_libdir}/cmake/SuiteSparse_config/
%{_libdir}/cmake/SuiteSparse/
%{_libdir}/cmake/UMFPACK/
%exclude %{_libdir}/cmake/*/*_static*.cmake
%{_libdir}/pkgconfig/AMD.pc
%{_libdir}/pkgconfig/BTF.pc
%{_libdir}/pkgconfig/CAMD.pc
%{_libdir}/pkgconfig/CCOLAMD.pc
%{_libdir}/pkgconfig/CHOLMOD.pc
%{_libdir}/pkgconfig/COLAMD.pc
%{_libdir}/pkgconfig/CXSparse.pc
%{_libdir}/pkgconfig/GraphBLAS.pc
%{_libdir}/pkgconfig/KLU.pc
%{_libdir}/pkgconfig/KLU_CHOLMOD.pc
%{_libdir}/pkgconfig/LAGraph.pc
%{_libdir}/pkgconfig/LDL.pc
%{_libdir}/pkgconfig/ParU.pc
%{_libdir}/pkgconfig/RBio.pc
%{_libdir}/pkgconfig/SPEX.pc
%{_libdir}/pkgconfig/SPQR.pc
%{_libdir}/pkgconfig/SuiteSparse_config.pc
%{_libdir}/pkgconfig/UMFPACK.pc
%{_libdir}/lib*.so
%if 0%{?build64}
%exclude %{_libdir}/lib*64*.so
%endif

%files static
%{_libdir}/cmake/*/*_static*.cmake
%{_libdir}/lib*.a
%if 0%{?build64}
%exclude %{_libdir}/lib*64*.a
%endif

%if 0%{?build64}
%files -n %{name}64
%license Licenses
%{_libdir}/libamd64.so.%{amd_version_major}*
%{_libdir}/libbtf64.so.%{btf_version_major}*
%{_libdir}/libcamd64.so.%{camd_version_major}*
%{_libdir}/libccolamd64.so.%{ccolamd_version_major}*
%{_libdir}/libcholmod64.so.%{cholmod_version_major}*
%{_libdir}/libcolamd64.so.%{colamd_version_major}*
%if "%{?enable_csparse}" == "1"
%{_libdir}/libcsparse64.so.%{csparse_version_major}*
%endif
%{_libdir}/libcxsparse64.so.%{cxsparse_version_major}*
%{_libdir}/libgraphblas64.so.%{graphblas_version_major}*
%{_libdir}/libklu_cholmod64.so.%{klu_cholmod_version_major}*
%{_libdir}/libklu64.so.%{klu_version_major}*
%{_libdir}/liblagraph64.so.%{lagraph_version_major}*
%{_libdir}/liblagraphx64.so.%{lagraphx_version_major}*
%{_libdir}/libldl64.so.%{ldl_version_major}*
%{_libdir}/libparu64.so.%{paru_version_major}*
%{_libdir}/librbio64.so.%{rbio_version_major}*
%{_libdir}/libspex64.so.%{spex_version_major}*
%{_libdir}/libspexpython64.so.%{spex_version_major}*
%{_libdir}/libspqr64.so.%{spqr_version_major}*
%{_libdir}/libsuitesparseconfig64.so.%{SuiteSparse_config_major}*
%{_libdir}/libumfpack64.so.%{umfpack_version_major}*

%files -n %{name}64-devel
%{_includedir}/SuiteSparse64/
%{_libdir}/lib*64.so
%{_libdir}/SuiteSparse64

%files -n %{name}64-static
%{_libdir}/lib*64.a

%files -n %{name}64_
%license Licenses
%{_libdir}/libamd64_.so.%{amd_version_major}*
%{_libdir}/libbtf64_.so.%{btf_version_major}*
%{_libdir}/libcamd64_.so.%{camd_version_major}*
%{_libdir}/libccolamd64_.so.%{ccolamd_version_major}*
%{_libdir}/libcholmod64_.so.%{cholmod_version_major}*
%{_libdir}/libcolamd64_.so.%{colamd_version_major}*
%if "%{?enable_csparse}" == "1"
%{_libdir}/libcsparse64_.so.%{csparse_version_major}*
%endif
%{_libdir}/libcxsparse64_.so.%{cxsparse_version_major}*
%{_libdir}/libgraphblas64_.so.%{graphblas_version_major}*
%{_libdir}/libklu_cholmod64_.so.%{klu_cholmod_version_major}*
%{_libdir}/libklu64_.so.%{klu_version_major}*
%{_libdir}/liblagraph64_.so.%{lagraph_version_major}*
%{_libdir}/liblagraphx64_.so.%{lagraphx_version_major}*
%{_libdir}/libldl64_.so.%{ldl_version_major}*
%{_libdir}/libparu64_.so.%{paru_version_major}*
%{_libdir}/librbio64_.so.%{rbio_version_major}*
%{_libdir}/libspex64_.so.%{spex_version_major}*
%{_libdir}/libspexpython64_.so.%{spex_version_major}*
%{_libdir}/libspqr64_.so.%{spqr_version_major}*
%{_libdir}/libsuitesparseconfig64_.so.%{SuiteSparse_config_major}*
%{_libdir}/libumfpack64_.so.%{umfpack_version_major}*

%files -n %{name}64_-devel
%{_includedir}/SuiteSparse64_/
%{_libdir}/lib*64_.so
%{_libdir}/SuiteSparse64_

%files -n %{name}64_-static
%{_libdir}/lib*64_.a
%endif

%files doc
%doc Doc/*

%changelog
* Mon Dec 15 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 7.11.0-1
- Upgrade to 7.11.0 (Reference: Fedora 42)
- License verified

* Mon Nov 28 2022 Muhammad Falak <mwani@microsoft.com> - 5.4.0-5
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.4.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 14 2019 Orion Poplawski <orion@nwra.com> - 5.4.0-2
- Build ILP64 version (bugz#1294200)

* Sun Sep 29 2019 Orion Poplawski <orion@nwra.com> - 5.4.0-1
- Update to 5.4.0
- Use upstream shared library builds
- Build with metis
- Explicitly list libraries and soname versions

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 13 2019 Kalev Lember <klember@redhat.com> - 4.4.6-19
- Use __global_ldflags when building tests

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 13 2018 Jerry James <loganjerry@gmail.com> - 4.4.6-17
- Rebuild for tbb 2019_U1

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 4.4.6-16
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.6-15
- Rebuild for new binutils

* Mon Jul 16 2018 Dominik Mierzejewski <rpm@greysector.net> - 4.4.6-14
- use openblas instead of atlas (#1506933)
- enable parallel make for faster builds and drop duplicate -fPIC
- drop non-standard -O3 and duplicate -fexceptions from default CFLAGS
- build and run demos in check section
- drop redundant ldconfig scriptlets

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Nils Philippsen <nils@tiptoe.de> - 4.4.6-12
- require gcc, gcc-c++ for building

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 07 2016 Dan Horák <dan[at]danny.cz> - 4.4.6-7
- Rebuild with fixed tbb on s390x (#1379632)

* Thu Sep 22 2016 Jerry James <loganjerry@gmail.com> - 4.4.6-6
- Rebuild for tbb 2017
- tbb is available for all arches now

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jerry James <loganjerry@gmail.com> - 4.4.6-4
- Rebuild for tbb 4.4u2

* Mon Jan 4 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.6-3
- Use %%{?__global_ldflags} when linking

* Mon Jan 4 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.6-2
- Update to 4.4.6

* Wed Aug 26 2015 Nils Philippsen <nils@redhat.com> - 4.4.5-2
- AMD is dual-licensed (LGPLv2+ or BSD)

* Wed Aug 26 2015 Nils Philippsen <nils@redhat.com> - 4.4.5-1
- version 4.4.5
- use %%license for licenses

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Nils Philippsen <nils@redhat.com> - 4.4.4-1
- update component versions

* Wed Jun 10 2015 Nils Philippsen <nils@redhat.com> - 4.4.4-1
- version 4.4.4
- fix URLs
- remove obsolete patches
- drop specifying and cleaning of buildroot

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.3.1-5
- Rebuilt for GCC 5 C++11 ABI change

* Tue Oct 14 2014 Peter Robinson <pbrobinson@fedoraproject.org> 4.3.1-4
- Only s390 doesn't have tbb

* Mon Sep 15 2014 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-3
- Change patch to move math.h include into SuiteSparse_config.c
- Fix linkage and library file permission issues

* Sat Sep 13 2014 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-2
- Add patch to allow octave compilation

* Mon Sep 08 2014 Clément David <c.david86@gmail.com> - 4.3.1-1
- Update to release 4.3.1. 

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Nils Philippsen <nils@redhat.com> - 4.2.2-2
- ship licenses as documentation in the base package
- hardlink duplicate documentation/license files

* Thu Dec 05 2013 Nils Philippsen <nils@redhat.com> - 4.2.1-1
- version 4.2.1

* Fri Sep 20 2013 Nils Philippsen <nils@redhat.com> - 4.0.2-7
- build against atlas 3.10.x

* Tue Sep 03 2013 Nils Philippsen <nils@redhat.com> - 4.0.2-6
- include C++ headers (#1001943)
- fix bogus dates in changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Petr Machata <pmachata@redhat.com> - 4.0.2-4
- Rebuild for TBB memory barrier bug

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Nils Philippsen <nils@redhat.com> - 4.0.2-2
- explicitly link libsuitesparseconfig where necessary

* Fri Nov 16 2012 Deji Akingunola <dakingun@gmail.com> - 4.0.2-1
- Update to 4.0.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> - 3.6.1-2
- fix build without TBB

* Fri Sep 23 2011 Deji Akingunola <dakingun@gmail.com> - 3.6.1-1
- Update to 3.6.1
- Fix undefine symbols in libspqr

* Sun Feb 13 2011 Deji Akingunola <dakingun@gmail.com> - 3.6.0-3
- Fix a couple of undefined reference errors in umfpack and Rbio (#677061)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Deji Akingunola <dakingun@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Deji Akingunola <dakingun@gmail.com> - 3.4.0-1
- Update to version 3.4.0.

* Tue May 19 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 3.3.0-2
- Split documentation into separate -doc subpackage (resolves BZ#492451).

* Mon Apr 27 2009 Deji Akingunola <dakingun@gmail.com> - 3.3.0-1
- Update to release 3.3.0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Deji Akingunola <dakingun@gmail.com> - 3.2.0-5
- More fixes for the undefined symbol issue (BZ #475411)

* Sat Dec 20 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-4
- Also build SPQR
- Further fixes for BZ #475411

* Wed Dec 17 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-3
- Rearrange the spec
- Link in necessary libs when making shared CHOLMOD lib (BZ #475411)
- Link with ATLAS' blas and lapack libs

* Wed Dec 17 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-2
- Rebuild for updated atlas

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-1
- New upstream version

* Mon Mar  3 2008 Quentin Spencer <qspencer@users.sourceforge.net> 3.1.0-1
- Update to release 3.1.0. 

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.0-4
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-3
- Update license tag. Fix minor issues found by rpmlint.

* Fri Aug 24 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-2
- Rebuild for F8.

* Tue Jul  3 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-1
- Change package name to match upstream, including provides and obsoletes.
- New release. Numerous changes in build to reflect source reorganization.
- Moved static libs into separate package.

* Mon Oct 16 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.1-1
- New release, and package name change from UFsparse to SuiteSparse. Fixes
  bug #210846. Keep the ufsparse package name for now.

* Thu Sep  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.0-1
- New release. Increment versions of some libraries.
- Rearrange and clean up spec file so all definitions are in one place.

* Mon Aug  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.0.0-1
- New release.
- Build newly added CAMD library.
- Misc minor spec changes.

* Tue Mar  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.2-1
- New release.
- Build newly added library CXSparse (but not CSparse--see comments
  in build section).

* Wed Feb 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 0.93-2
- Rebuild for Fedora Extras 5.

* Thu Feb  9 2006 Quentin Spencer <qspencer@users.sourceforge.net> 0.93-1
- New release. Remove old patch.

* Wed Dec 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.92-2
- Add patch0--fixes LDL/Makefile so CFLAGS are used when compiling ldl.a.

* Wed Dec 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.92-1
- Update to Dec 8 2005 version.

* Tue Oct 25 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.91-2
- Rebuild.

* Tue Oct 18 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.91-1
- New upstream release, incorporating previous patches
- chmod the build directory to ensure all headers are world readable

* Fri Oct 07 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.9-3
- Build cholmod, but disable METIS using -DNPARTITION flag.

* Sat Oct 01 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.9-2
- Modify description, other modifications for import into FE.
- Add dist tag, cosmetic changes.

* Thu Sep 08 2005 David Bateman <dbateman@free.fr> 0.9-1
- First version.
