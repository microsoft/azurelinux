## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This flag breaks the linkage among libraries
%undefine _ld_as_needed

%global genname superlumt
%global majorver 4.0
%global soname_version %{majorver}.1

Name: SuperLUMT
Version: %{majorver}.1
Release: %autorelease
Summary: Single precision real SuperLU routines for shared memory parallel machines
License: BSD-3-Clause
URL: https://portal.nersc.gov/project/sparse/superlu/
Source0: https://github.com/xiaoyeli/superlu_mt/archive/refs/tags/v%{majorver}.1/superlu_mt-%{majorver}.1.tar.gz

BuildRequires: make
BuildRequires: pkgconfig(flexiblas)
BuildRequires: pkgconfig
BuildRequires: tcsh
BuildRequires: gcc
Requires: %{name}-common = %{version}-%{release}

# Patches to build shared object libraries
# and files for testing
Patch0: %{name}-build_shared.patch
Patch1: %{name}-fix_testsuite.patch
Patch2: %{name}64-build_shared.patch
Patch3: %{name}64-fix_testsuite.patch
Patch4: %{name}-fix_examples.patch
Patch5: %{name}64-fix_examples.patch
Patch6: %{name}-fix_several_prototype_errors.patch

%description
Subroutines to solve sparse linear systems for shared memory parallel machines.
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.


%package double
Summary: Double precision real SuperLU routines for shared memory parallel machines
Requires: %{name}-common = %{version}-%{release}
%description double
This package contains double precision real SuperLU routines library
by SuperLUMT.


%package complex
Summary: Single precision complex SuperLU routines for shared memory parallel machines
Requires: %{name}-common = %{version}-%{release}
%description complex
This package contains single precision complex routines library by SuperLUMT.


%package complex16
Summary: Double precision complex SuperLU routines for shared memory parallel machines
Requires: %{name}-common = %{version}-%{release}
%description complex16
This package contains double precision complex routines library by SuperLUMT.


%package devel
Summary: The SuperLUMT headers and development-related files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-double%{?_isa} = %{version}-%{release}
Requires: %{name}-complex%{?_isa} = %{version}-%{release}
Requires: %{name}-complex16%{?_isa} = %{version}-%{release}

%description devel
Shared links and header files used by SuperLUMT.

########################################################
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%package -n SuperLUMT64
Summary: Single precision real SuperLU routines (64bit INTEGER)

BuildRequires: pkgconfig(flexiblas)
Requires: %{name}-common = %{version}-%{release}
%description -n SuperLUMT64
Subroutines to solve sparse linear systems for shared memory parallel machines
(64bit INTEGER).
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.


%package -n SuperLUMT64-double
Summary: Double precision real SuperLU routines (64bit INTEGER)

Requires: %{name}-common = %{version}-%{release}
%description -n SuperLUMT64-double
This package contains double precision real SuperLU routines library
by SuperLUMT (64bit INTEGER).


%package -n SuperLUMT64-complex
Summary: Single precision complex SuperLU routines (64bit INTEGER)
Requires: %{name}-common = %{version}-%{release}
%description -n SuperLUMT64-complex
This package contains single precision complex routines library by SuperLUMT
(64bit INTEGER).


%package -n SuperLUMT64-complex16
Summary: Double precision complex SuperLU routines (64bit INTEGER)
Requires: %{name}-common = %{version}-%{release}
%description -n SuperLUMT64-complex16
This package contains double precision complex routines library
by SuperLUMT (64bit INTEGER).

%package -n SuperLUMT64-devel
Summary: The MUMPS headers and development-related files (64bit INTEGER)
Requires: SuperLUMT64%{?_isa} = %{version}-%{release}
Requires: SuperLUMT64-double%{?_isa} = %{version}-%{release}
Requires: SuperLUMT64-complex%{?_isa} = %{version}-%{release}
Requires: SuperLUMT64-complex16%{?_isa} = %{version}-%{release}

%description -n SuperLUMT64-devel
Shared links, header files for %{name} (64bit INTEGER).
%endif
##########################################################

%package common
Summary: Documentation files for SuperLUMT

BuildArch: noarch
%description common
This package contains common documentation files for SuperLUMT.

%prep
%setup -q -n superlu_mt-%{majorver}.1

rm -fr SRC/mc64ad.f.bak
find . -type f | sed -e "/TESTING/d" | xargs chmod a-x
# Remove the shippped executables from EXAMPLE
find EXAMPLE -type f | while read file
do
   [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || :
done

mkdir -p lib

# Duplicating of examples source code
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
cp -a EXAMPLE EXAMPLE64
%endif

%patch -P 0 -p0
%patch -P 1 -p0
%patch -P 4 -p0
%patch -P 6 -p1

%build
cp -p MAKE_INC/make.linux.openmp make.inc
sed -i -e "s|-O3|$RPM_OPT_FLAGS -std=gnu17|" \
make.inc

## Build lib ##########################################
export LIBBLASLINK=-lflexiblas
export LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK"

make -j1 \
 SONAME=%{majorver} \
 BLASLIB="-L%{_libdir} $LIBBLASLINK" \
 PREDEFS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0" \
 NOOPTS="-O0 -fPIC -fopenmp $LIBBLASLINK" \
 CDEFS=-DAdd_ \
 FFLAGS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -fopenmp -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0" \
 FORTRAN=gfortran \
 LOADER=gcc \
 CC=gcc \
 CFLAGS="$RPM_OPT_FLAGS -std=gnu17 $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0" \
 LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK" \
 MATHLIB=-lm \
 MPLIB= -C SRC single double complex complex16
 
cp -p SRC/libsuperlumt_*.so.%{majorver} lib/
cp -p SRC/libsuperlumt_*.so lib/

# Make example files
export LIBBLASLINK=-lflexiblas
export LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK"

make -j1 \
 SONAME=%{majorver} \
 BLASLIB="-L%{_libdir} $LIBBLASLINK" \
 PREDEFS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0" \
 NOOPTS="-O0 -fPIC -fopenmp $LIBBLASLINK" \
 CDEFS=-DAdd_ \
 FFLAGS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -fopenmp -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0" \
 FORTRAN=gfortran \
 LOADER=gcc \
 LOADOPTS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0" \
 CC=gcc \
 CFLAGS="$RPM_OPT_FLAGS -std=gnu17 $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0" \
 LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK" \
 MATHLIB=-lm \
 MPLIB= -C EXAMPLE single double complex complex16

make -C SRC clean
make -C TESTING/MATGEN clean
#######################################################

## Build 64 ##########################################
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
# Reverting previous patches
# and patch again for new libraries
patch -R -p0 < %{PATCH0}
patch -R -p0 < %{PATCH1}
patch -p0 < %{PATCH2}
patch -p0 < %{PATCH3}
patch -p0 < %{PATCH5}

export LIBBLASLINK=-lflexiblas64
export LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK"

make -j1 \
 SONAME=%{majorver} \
 BLASLIB="-L%{_libdir} $LIBBLASLINK" \
 PREDEFS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0 -D_LONGINT" \
 NOOPTS="-O0 -fPIC -fopenmp $LIBBLASLINK" \
 CDEFS=-DAdd_ \
 FFLAGS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -fopenmp -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0 -fdefault-integer-8" \
 FORTRAN=gfortran \
 CFLAGS="$RPM_OPT_FLAGS -std=gnu17 $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0 -D_LONGINT" \
 LOADER=gcc \
 CC=gcc \
 LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK" \
 MATHLIB=-lm \
 MPLIB= -C SRC single double complex complex16

cp -p SRC/libsuperlumt64_*.so.%{majorver} lib/
cp -p SRC/libsuperlumt64_*.so lib/

# Make example files

export LIBBLASLINK=-lflexiblas64
export LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK"

make -j1 \
 SONAME=%{majorver} \
 BLASLIB="-L%{_libdir} $LIBBLASLINK" \
 PREDEFS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0 -D_LONGINT" \
 NOOPTS="-O0 -fPIC -fopenmp $LIBBLASLINK" \
 CDEFS=-DAdd_ \
 FFLAGS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -fopenmp -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0 -fdefault-integer-8" \
 FORTRAN=gfortran \
 CFLAGS="$RPM_OPT_FLAGS -std=gnu17 $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0 -D_LONGINT" \
 LOADER=gcc \
 LOADOPTS="$RPM_OPT_FLAGS $LDFLAGS -fPIC -D__OPENMP -DPRNTlevel=0 -DDEBUGlevel=0 -D_LONGINT" \
 CC=gcc \
 LDFLAGS="%{__global_ldflags} -lgomp $LIBBLASLINK" \
 MATHLIB=-lm \
 MPLIB= -C EXAMPLE64 single double complex complex16
%endif

%check
pushd EXAMPLE
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_libdir}
./pslinsol < big.rua
./pdlinsol < big.rua
./pclinsol < cmat
./pzlinsol < cmat
./pslinsolx < big.rua
./pdlinsolx < big.rua
./pclinsolx < cmat
./pzlinsolx < cmat
./pslinsolx1 < big.rua
./pdlinsolx1 < big.rua
./pclinsolx1 < cmat
./pzlinsolx1 < cmat
popd

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
pushd EXAMPLE64
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_libdir}
./pslinsol < big.rua
./pdlinsol < big.rua
./pclinsol < cmat
./pzlinsol < cmat
popd
%endif

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
cp -P lib/libsuperlumt_*.so.%{majorver} %{buildroot}%{_libdir}/
install -p SRC/*.h %{buildroot}%{_includedir}/%{name}/
chmod a-x %{buildroot}%{_includedir}/%{name}/*.h
cp -P lib/libsuperlumt_*.so %{buildroot}%{_libdir}/

for i in s d c z
do
 ln -sf  libsuperlumt_${i}.so.%{majorver} %{buildroot}%{_libdir}/libsuperlumt_${i}.so
done

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
cp -P lib/libsuperlumt64_*.so.%{majorver} %{buildroot}%{_libdir}/
cp -P lib/libsuperlumt64_*.so %{buildroot}%{_libdir}/

for i in s d c z
do
 ln -sf  libsuperlumt64_${i}.so.%{majorver} %{buildroot}%{_libdir}/libsuperlumt64_${i}.so
done
%endif

%files
%{_libdir}/libsuperlumt_s.so.%{majorver}

%files double
%{_libdir}/libsuperlumt_d.so.%{majorver}

%files complex
%{_libdir}/libsuperlumt_c.so.%{majorver}

%files complex16
%{_libdir}/libsuperlumt_z.so.%{majorver}

%files devel
%{_includedir}/%{name}/
%{_libdir}/libsuperlumt_*.so

########################################################
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%files -n SuperLUMT64
%{_libdir}/libsuperlumt64_s.so.%{majorver}

%files -n SuperLUMT64-double
%{_libdir}/libsuperlumt64_d.so.%{majorver}

%files -n SuperLUMT64-complex
%{_libdir}/libsuperlumt64_c.so.%{majorver}

%files -n SuperLUMT64-complex16
%{_libdir}/libsuperlumt64_z.so.%{majorver}

%files -n SuperLUMT64-devel
%{_includedir}/%{name}/
%{_libdir}/libsuperlumt64_*.so
%endif
#######################################################

%files common
%license License.txt
%doc DOC README

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 4.0.1-7
- test: add initial lock files

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Antonio Trande <sagitter@fedoraproject.org> - 4.0.1-5
- Fix GCC15 builds

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 4.0.1-2
- Rebuild i686 rpms

* Sun May 19 2024 Antonio Trande <sagitter@fedoraproject.org> - 4.0.1-1
- Release 4.0.1

* Sat May 18 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.1.0-45
- Fix patch commands

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Florian Weimer <fweimer@redhat.com> - 3.1.0-40
- C99 compatibility fixes

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Tom Stellard <tstellar@redhat.com> - 3.1.0-34
- Add BuildRequires: make

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-33
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 25 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.1.0-31
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Sat Mar 21 2020 sagitter <sagitter@fedoraproject.org> - 3.1.0-30
- Do not mix-up pthread and openmp support

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 sagitter <sagitter@fedoraproject.org> - 3.1.0-28
- Remove -gomp flags

* Thu Oct 24 2019 sagitter <sagitter@fedoraproject.org> - 3.1.0-27
- Optimize OpenMP flags

* Wed Oct 23 2019 sagitter <sagitter@fedoraproject.org> - 3.1.0-26
- Undefine --as-needed link option

* Sat Sep 07 2019 Orion Poplawski <orion@nwra.com> - 3.1.0-25
- Only need dts for EL7

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 29 2019 sagitter <sagitter@fedoraproject.org> - 3.1.0-23
- Downgrading Make's jobs

* Sat Jun 29 2019 sagitter <sagitter@fedoraproject.org> - 3.1.0-22
- Use devtoolset-8 on epel

* Tue Feb 19 2019 sagitter <sagitter@fedoraproject.org> - 3.1.0-21
- Use openblas always

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.1.0-19
- Fix RHEL conditions

* Thu Aug 23 2018 Peter Robinson <pbrobinson@gmail.com> - 3.1.0-18
- Drop group, Build on all arches

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 21 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-16
- Add gcc BR

* Thu Feb 15 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-15
- Use %%%%ldconfig_scriptlets

* Thu Feb 15 2018 sagitter <sagitter@fedoraproject.org> - 3.1.0-14
- Rebuild for libsbml-5.16.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 30 2017 sagitter <sagitter@fedoraproject.org> - 3.1.0-12
- Rebuild against openblas

* Wed Aug 16 2017 sagitter <sagitter@fedoraproject.org> - 3.1.0-11
- Rebuild for lapack 3.7.1 (move to 64_ suffix)

* Wed Aug 16 2017 sagitter <sagitter@fedoraproject.org> - 3.1.0-10
- Rebuild for lapack 3.7.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-9
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 05 2016 sagitter <sagitter@fedoraproject.org> - 3.1.0-6
- Built against blas on s390x (bz#1382071)

* Fri Aug 12 2016 Peter Robinson <pbrobinson@gmail.com> - 3.1.0-5
- Update to the latest openblas arch list

* Wed May 04 2016 sagitter <sagitter@fedoraproject.org> - 3.1.0-4
- Dropped Fortran dependencies

* Wed May 04 2016 sagitter <sagitter@fedoraproject.org> - 3.1.0-3
- Dropped Fortran dependiencies

* Thu Apr 14 2016 sagitter <sagitter@fedoraproject.org> - 3.1.0-2
- Excluded ppc64le arch

* Tue Apr 12 2016 sagitter <sagitter@fedoraproject.org> - 3.1.0-1
- New package (bz#1322846)
## END: Generated by rpmautospec
