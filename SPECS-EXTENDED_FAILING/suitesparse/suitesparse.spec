Vendor:         Microsoft Corporation
Distribution:   Mariner
%global amd_version_major 2
%global btf_version_major 1
%global camd_version_major 2
%global ccolamd_version_major 2
%global cholmod_version_major 3
%global colamd_version_major 2
%global csparse_version_major 3
%global cxsparse_version_major 3
%global klu_version_major 1
%global ldl_version_major 2
%global rbio_version_major 2
%global spqr_version_major 2
%global SuiteSparse_config_major 5
%global umfpack_version_major 5

### CXSparse is a superset of CSparse, and the two share common header
### names, so it does not make sense to build both. CXSparse is built
### by default, but CSparse can be built instead by defining
### enable_csparse as 1 below.
%global enable_csparse 0

# Whether to build a separate version of libraries linked against an ILP64 BLAS
%if 0%{?__isa_bits} == 64
%global build64 1
%endif
 
Name:           suitesparse
Version:        5.4.0
Release:        4%{?dist}
Summary:        A collection of sparse matrix libraries

License:        (LGPLv2+ or BSD) and LGPLv2+ and GPLv2+
URL:            http://faculty.cse.tamu.edu/davis/suitesparse.html
Source0:        http://faculty.cse.tamu.edu/davis/SuiteSparse/SuiteSparse-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++

BuildRequires:  metis-devel
BuildRequires:  openblas-devel
BuildRequires:  tbb-devel
BuildRequires:  hardlink

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
pushd SuiteSparse
  # Remove bundled metis
  rm -r metis*
  # Makefiles look for metis.h specifically
  ln -s %{_includedir}/metis/*.h include/

  # Fix pragma ivdep so gcc understands it.
  for fil in $(grep -Frl 'pragma ivdep' .); do
    sed -i.orig 's/pragma ivdep/pragma GCC ivdep/' $fil
    touch -r ${fil}.orig $fil
    rm -f ${fil}.orig
  done

  # drop non-standard -O3 and duplicate -fexceptions from default CFLAGS
  sed -i -e '/^  CF =/ s/ -O3 -fexceptions//' SuiteSparse_config/SuiteSparse_config.mk

  # Allow adding a suffix to the library name
  sed -i -e '/SO.*=/s/$(LIBRARY).so/$(LIBRARY)$(LIBRARY_SUFFIX).so/' \
         -e '/AR_TARGET *=/s/$(LIBRARY).a/$(LIBRARY)$(LIBRARY_SUFFIX).a/' SuiteSparse_config/SuiteSparse_config.mk
  sed -i -e 's/-l\(amd\|btf\|camd\|ccolamd\|cholmod\|colamd\|csparse\|cxsparse\|klu\|ldl\|rbio\|spqr\|suitesparseconfig\|umfpack\)/-l\1$(LIBRARY_SUFFIX)/g' \
    $(find -name Makefile\* -o -name \*.mk)
popd
%if 0%{?build64}
cp -a SuiteSparse SuiteSparse64
cp -a SuiteSparse SuiteSparse64_
%endif

%build
export AUTOCC=no
export CC=gcc

for build in SuiteSparse %{?build64:SuiteSparse64 SuiteSparse64_}
do
  pushd $build

  # TODO - Try to use upstream makefile - will build more components
  mkdir -p Doc/{AMD,BTF,CAMD,CCOLAMD,CHOLMOD,COLAMD,KLU,LDL,UMFPACK,SPQR,RBio} Include

  export CFLAGS="$RPM_OPT_FLAGS -I%{_includedir}/metis"
  export LAPACK=""
  # Set flags for ILP64 build
  if [ $build = SuiteSparse64 ]
  then
     export CFLAGS="$CFLAGS -DBLAS64"
     export BLAS=-lopenblas64
     export LIBRARY_SUFFIX=64
  elif [ $build = SuiteSparse64_ ]
  then
     export CFLAGS="$CFLAGS -DBLAS64 -DSUN64"
     export BLAS=-lopenblas64_
     export LIBRARY_SUFFIX=64_
  else
     export BLAS=-lopenblas
  fi   
   
  # SuiteSparse_config needs to come first
  pushd SuiteSparse_config
    %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    cp -p *.h ../Include
  popd

  pushd AMD
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/License.txt Doc/lesser.txt Doc/ChangeLog Doc/*.pdf ../Doc/AMD
  popd

  pushd BTF
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/* ../Doc/BTF
  popd

  pushd CAMD
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/ChangeLog Doc/License.txt Doc/*.pdf ../Doc/CAMD
  popd

  pushd CCOLAMD
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/* ../Doc/CCOLAMD
  popd

  pushd COLAMD
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/* ../Doc/COLAMD
  popd

  pushd CHOLMOD
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/*.pdf ../Doc/CHOLMOD
    cp -p Cholesky/lesser.txt ../Doc/CHOLMOD/Cholesky_License.txt
    cp -p Core/lesser.txt ../Doc/CHOLMOD/Core_License.txt
    cp -p MatrixOps/gpl.txt ../Doc/CHOLMOD/MatrixOps_License.txt
    cp -p Partition/lesser.txt ../Doc/CHOLMOD/Partition_License.txt
    cp -p Supernodal/gpl.txt ../Doc/CHOLMOD/Supernodal_License.txt
  popd

  %if "%{?enable_csparse}" == "1"
  pushd CSparse
    pushd Source
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
      cp -p cs.h ../../Include
    popd
    mkdir ../Doc/CSparse/
    cp -p Doc/* ../Doc/CSparse
  popd

  %else
  pushd CXSparse
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/cs.h ../Include
    mkdir ../Doc/CXSparse/
    cp -p Doc/* ../Doc/CXSparse
  popd
  %endif

  pushd KLU
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/lesser.txt ../Doc/KLU
  popd

  pushd LDL
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/ChangeLog Doc/lesser.txt Doc/*.pdf ../Doc/LDL
  popd

  pushd UMFPACK
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/License.txt Doc/ChangeLog Doc/gpl.txt Doc/*.pdf ../Doc/UMFPACK
  popd

  pushd SPQR
    pushd Lib
      %make_build CFLAGS="$CFLAGS -DHAVE_TBB -DNPARTITION" TBB=-ltbb BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h* ../Include
    cp -p README{,_SPQR}.txt
    cp -p README_SPQR.txt Doc/* ../Doc/SPQR
  popd

  pushd RBio
    pushd Lib
      %make_build CFLAGS="$CFLAGS" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX"
    popd
    cp -p Include/*.h ../Include
    cp -p README.txt Doc/ChangeLog Doc/License.txt ../Doc/RBio
  popd

  popd
done

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
cp -a SuiteSparse/Include/*.{h,hpp} ${RPM_BUILD_ROOT}%{_includedir}/%{name}/
for build in SuiteSparse %{?build64:SuiteSparse64 SuiteSparse64_}
do
  pushd $build
    cp -a */Lib/*.a lib/*.so* ${RPM_BUILD_ROOT}%{_libdir}/
    chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/*.so.*

    # collect licenses in one place to ship as base package documentation
    rm -rf Licenses
    mkdir Licenses
    find */ -iname lesser.txt -o -iname license.txt -o -iname gpl.txt -o \
        -iname license | while read f; do
            b="${f%%/*}"
            r="${f#$b}"
            x="$(echo "$r" | sed 's|/doc/|/|gi')"
            install -m0644 -D "$f" "./Licenses/$b/$x"
        done

    # hardlink duplicate documentation files
    hardlink -cv Docs/ Licenses/
  popd
done


%check
export AUTOCC=no
export CC=gcc
TESTDIRS="AMD CAMD CCOLAMD CHOLMOD COLAMD KLU LDL SPQR RBio UMFPACK"
%if "%{?enable_csparse}" == "1"
TESTDIRS="$TESTDIRS CSparse"
%else
TESTDIRS="$TESTDIRS CXSparse"
%endif
for build in SuiteSparse %{?build64:SuiteSparse64 SuiteSparse64_}
do
  pushd $build
    export CFLAGS="$RPM_OPT_FLAGS -I%{_includedir}/metis"
    export LAPACK=""
    # Set flags for ILP64 build
    if [ $build = SuiteSparse64 ]
    then
       export CFLAGS="$CFLAGS -DBLAS64"
       export BLAS=-lopenblas64
       export LIBRARY_SUFFIX=64
    elif [ $build = SuiteSparse64_ ]
    then
       export CFLAGS="$CFLAGS -DBLAS64 -DSUN64"
       export BLAS=-lopenblas64_
       export LIBRARY_SUFFIX=64_
    else
       export BLAS=-lopenblas
    fi   

    for d in $TESTDIRS ; do
        %make_build -C $d/Demo CFLAGS="$CFLAGS" LIB="%{?__global_ldflags} -lm -lrt" BLAS="$BLAS" LIBRARY_SUFFIX="$LIBRARY_SUFFIX" SPQR_CONFIG=-DHAVE_TBB TBB=-ltbb
    done
  popd
done

%files
%license SuiteSparse/Licenses
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
%{_libdir}/libklu.so.%{klu_version_major}*
%{_libdir}/libldl.so.%{ldl_version_major}*
%{_libdir}/librbio.so.%{rbio_version_major}*
%{_libdir}/libspqr.so.%{spqr_version_major}*
%{_libdir}/libsuitesparseconfig.so.%{SuiteSparse_config_major}*
%{_libdir}/libumfpack.so.%{umfpack_version_major}*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib*.so
%exclude %{_libdir}/lib*64*.so

%files static
%{_libdir}/lib*.a
%exclude %{_libdir}/lib*64*.a

%if 0%{?build64}
%files -n %{name}64
%license SuiteSparse64/Licenses
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
%{_libdir}/libklu64.so.%{klu_version_major}*
%{_libdir}/libldl64.so.%{ldl_version_major}*
%{_libdir}/librbio64.so.%{rbio_version_major}*
%{_libdir}/libspqr64.so.%{spqr_version_major}*
%{_libdir}/libsuitesparseconfig64.so.%{SuiteSparse_config_major}*
%{_libdir}/libumfpack64.so.%{umfpack_version_major}*

%files -n %{name}64-devel
%{_libdir}/lib*64.so

%files -n %{name}64-static
%{_libdir}/lib*64.a

%files -n %{name}64_
%license SuiteSparse64_/Licenses
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
%{_libdir}/libklu64_.so.%{klu_version_major}*
%{_libdir}/libldl64_.so.%{ldl_version_major}*
%{_libdir}/librbio64_.so.%{rbio_version_major}*
%{_libdir}/libspqr64_.so.%{spqr_version_major}*
%{_libdir}/libsuitesparseconfig64_.so.%{SuiteSparse_config_major}*
%{_libdir}/libumfpack64_.so.%{umfpack_version_major}*

%files -n %{name}64_-devel
%{_libdir}/lib*64_.so

%files -n %{name}64_-static
%{_libdir}/lib*64_.a
%endif

%files doc
%doc SuiteSparse/Doc/*

%changelog
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
