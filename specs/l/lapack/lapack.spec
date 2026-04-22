# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Something in the debuginfo process is stripping the custom 64_ symbols out of lapack64_ and blas64_
%global debug_package %{nil}

%global shortver	3
%global mediumver	%{shortver}.12

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%global arch64 1
%else
%global arch64 0
%endif

Summary: Numerical linear algebra package libraries
Name: lapack
Version: %{mediumver}.0
Release: 11%{?dist}
License: BSD-3-Clause-Open-MPI
URL: http://www.netlib.org/lapack/
Source0: https://github.com/Reference-LAPACK/lapack/archive/v%{version}.tar.gz
Source1: http://www.netlib.org/lapack/manpages.tgz
Source4: http://www.netlib.org/lapack/lapackqref.ps
Source5: http://www.netlib.org/blas/blasqr.ps
# https://github.com/Reference-LAPACK/lapack/pull/959
Patch0: lapack-3.12.0-fix-dmd-issues.patch
BuildRequires: gcc-gfortran, gawk
BuildRequires: make, cmake
# There isn't any c++ code here, but cmake checks for a working c++ compiler?
BuildRequires: gcc-c++
Requires: blas%{?_isa} = %{version}-%{release}

%global _description_lapack %{expand:
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran90 and built with gcc.
}

%global _description_blas %{expand:
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra.
}

%description %_description_lapack

%package devel
Summary: LAPACK development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: blas-devel%{?_isa} = %{version}-%{release}
%if 0%{?arch64}
Requires: %{name}64%{?_isa} = %{version}-%{release}
Requires: %{name}64_%{?_isa} = %{version}-%{release}
%endif

%description devel
LAPACK development libraries (shared).

%package static
Summary: LAPACK static libraries
Requires: lapack-devel%{?_isa} = %{version}-%{release}

%description static
LAPACK static libraries.

%package -n blas
Summary: The Basic Linear Algebra Subprograms library

%description -n blas %_description_blas

%package -n blas-devel
Summary: BLAS development libraries
Requires: blas%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran
%if 0%{?arch64}
Requires: blas64%{?_isa} = %{version}-%{release}
Requires: blas64_%{?_isa} = %{version}-%{release}
%endif

%description -n blas-devel
BLAS development libraries (shared).

%package -n blas-static
Summary: BLAS static libraries
Requires: blas-devel%{?_isa} = %{version}-%{release}

%description -n blas-static
BLAS static libraries.

%if 0%{?arch64}
%package -n lapack64
Summary: Numerical linear algebra package libraries
Requires: blas64%{?_isa} = %{version}-%{release}

%description -n lapack64 %_description_lapack
This build has 64bit INTEGER support.

%package -n blas64
Summary: The Basic Linear Algebra Subprograms library (64bit INTEGER)

%description -n blas64 %_description_blas
This build has 64bit INTEGER support.

%package -n lapack64_
Summary: Numerical linear algebra package libraries
Requires: blas64_%{?_isa} = %{version}-%{release}

%description -n lapack64_ %_description_lapack
This build has 64bit INTEGER support and a symbol name suffix.

%package -n blas64_
Summary: The Basic Linear Algebra Subprograms library (64bit INTEGER)

%description -n blas64_ %_description_blas
This build has 64bit INTEGER support and a symbol name suffix.
%endif

%prep
%setup -q -n %{name}-%{version}
%setup -q -n %{name}-%{version} -D -T -a1
%patch -P0 -p1

mkdir manpages
mv man/ manpages/

# clean up weird mac osx barf
rm -rf manpages/man/man3/.*.3


%build
%global common_flags -DCMAKE_SKIP_RPATH:BOOL=ON -DBUILD_DEPRECATED=ON -DLAPACKE=ON -DLAPACKE_WITH_TMG=ON -DCBLAS=ON

# shared normal
%cmake %{common_flags} -DBUILD_SHARED_LIBS=ON
%cmake_build
mv %_vpath_builddir %_vpath_builddir-SHARED

# static normal
%cmake %{common_flags} -DBUILD_SHARED_LIBS=OFF
%cmake_build
mv %_vpath_builddir %_vpath_builddir-STATIC

%if 0%{?arch64}
# shared 64
%cmake %{common_flags} -DBUILD_SHARED_LIBS=ON -DBUILD_INDEX64=ON
%cmake_build
mv %_vpath_builddir %_vpath_builddir-SHARED64

# static 64
%cmake %{common_flags} -DBUILD_SHARED_LIBS=OFF -DBUILD_INDEX64=ON
%cmake_build
mv %_vpath_builddir %_vpath_builddir-STATIC64

# This is not an Easter Egg. Just a scrambled egg.
# The first person to see this scrambled egg and point it out to spot@fedoraproject.org explicitly will get $20 USD.

# shared 64 SUFFIX
sed -i 's|64"|64_"|g' CMakeLists.txt
%cmake %{common_flags} -DBUILD_SHARED_LIBS=ON -DBUILD_INDEX64=ON
%cmake_build
mv %_vpath_builddir %_vpath_builddir-SHARED64SUFFIX

# static 64 SUFFIX
%cmake %{common_flags} -DBUILD_SHARED_LIBS=OFF -DBUILD_INDEX64=ON
%cmake_build
mv %_vpath_builddir %_vpath_builddir-STATIC64SUFFIX

# Undo the 64_ suffix
sed -i 's|64_"|64"|g' CMakeLists.txt
%endif

cp -p %{SOURCE4} lapackqref.ps
cp -p %{SOURCE5} blasqr.ps

%install
%if 0%{?arch64}
for t in SHARED STATIC SHARED64 STATIC64; do
%else
for t in SHARED STATIC; do
%endif
	mv %_vpath_builddir-$t %_vpath_builddir
	%cmake_install
	mv %_vpath_builddir %_vpath_builddir-$t
done

%if 0%{?arch64}
# Set the suffix
sed -i 's|64"|64_"|g' CMakeLists.txt
for t in SHARED64SUFFIX STATIC64SUFFIX; do
	mv %_vpath_builddir-$t %_vpath_builddir
	%cmake_install
	mv %_vpath_builddir %_vpath_builddir-$t
done

pushd %{buildroot}%{_libdir}
for name in blas cblas lapack lapacke; do
	for i in `readelf -Ws lib${name}64_.so.%{version} | awk '{print $8}' | grep -v GLIBC |grep -v GFORTRAN |grep -v "Name" `; do echo "$i" "${i}64_"; done > ${name}-suffix.def.dirty
	sort -n ${name}-suffix.def.dirty | uniq > ${name}-suffix.def
	objcopy --redefine-syms ${name}-suffix.def lib${name}64_.so.%{version} lib${name}64_.so.%{version}.fixed
	rm -rf lib${name}64_.so.%{version}
	mv lib${name}64_.so.%{version}.fixed lib${name}64_.so.%{version}
done

for name in blas cblas lapack lapacke; do
	for i in `nm lib${name}64_.a |grep " T " | awk '{print $3}'`; do echo "$i" "${i}64_"; done > ${name}-static-suffix.def.dirty
	sort -n ${name}-static-suffix.def.dirty | uniq > ${name}-static-suffix.def
	objcopy --redefine-syms ${name}-static-suffix.def lib${name}64_.a lib${name}64_.a.fixed
	rm -rf lib${name}64_.a
	mv lib${name}64_.a.fixed lib${name}64_.a
done
popd

# cleanup defs
rm -rf %{buildroot}%{_libdir}/*.def*
%endif

mkdir -p %{buildroot}%{_mandir}/man3
chmod 755 %{buildroot}%{_mandir}/man3

# Blas manpages
pushd manpages/
mkdir -p blas/man/man3
cd man/man3/
mv caxpy.f.3 caxpy.3 ccopy.f.3 ccopy.3 cdotc.f.3 cdotc.3 cdotu.f.3 cdotu.3 cgbmv.f.3 cgbmv.3 \
cgemm.f.3 cgemm.3 cgemv.f.3 cgemv.3 cgerc.f.3 cgerc.3 cgeru.f.3 cgeru.3 chbmv.f.3 chbmv.3 \
chemm.f.3 chemm.3 chemv.f.3 chemv.3 cher.f.3 cher.3 cher2.f.3 cher2.3 cher2k.f.3 cher2k.3 \
cherk.f.3 cherk.3 chpmv.f.3 chpmv.3 chpr.f.3 chpr.3 chpr2.f.3 chpr2.3 \
cscal.f.3 cscal.3 csrot.f.3 csrot.3 csscal.f.3 csscal.3 cswap.f.3 cswap.3 csymm.f.3 \
csymm.3 csyr2k.f.3 csyr2k.3 csyrk.f.3 csyrk.3 ctbmv.f.3 ctbmv.3 ctbsv.f.3 ctbsv.3 ctpmv.f.3 \
ctpmv.3 ctpsv.f.3 ctpsv.3 ctrmm.f.3 ctrmm.3 ctrmv.f.3 ctrmv.3 ctrsm.f.3 ctrsm.3 ctrsv.f.3 \
ctrsv.3 dasum.f.3 dasum.3 daxpy.f.3 daxpy.3 dcabs1.f.3 dcabs1.3 dcopy.f.3 dcopy.3 ddot.f.3 \
ddot.3 dgbmv.f.3 dgbmv.3 dgemm.f.3 dgemm.3 dgemv.f.3 dgemv.3 dger.f.3 dger.3 \
drot.f.3 drot.3 drotm.f.3 drotm.3 drotmg.f.3 drotmg.3 dsbmv.f.3 \
dsbmv.3 dscal.f.3 dscal.3 dsdot.f.3 dsdot.3 dspmv.f.3 dspmv.3 dspr.f.3 dspr.3 dspr2.f.3 \
dspr2.3 dswap.f.3 dswap.3 dsymm.f.3 dsymm.3 dsymv.f.3 dsymv.3 dsyr.f.3 dsyr.3 dsyr2.f.3 \
dsyr2.3 dsyr2k.f.3 dsyr2k.3 dsyrk.f.3 dsyrk.3 dtbmv.f.3 dtbmv.3 dtbsv.f.3 dtbsv.3 dtpmv.f.3 \
dtpmv.3 dtpsv.f.3 dtpsv.3 dtrmm.f.3 dtrmm.3 dtrmv.f.3 dtrmv.3 dtrsm.f.3 dtrsm.3 dtrsv.f.3 \
dtrsv.3 dzasum.f.3 dzasum.3 icamax.f.3 icamax.3 idamax.f.3 idamax.3 \
isamax.f.3 isamax.3 izamax.f.3 izamax.3 lsame.3 sasum.f.3 sasum.3 saxpy.f.3 saxpy.3 \
scabs1.f.3 scabs1.3 scasum.f.3 scasum.3 scopy.f.3 scopy.3 sdot.f.3 sdot.3 \
sdsdot.f.3 sdsdot.3 sgbmv.f.3 sgbmv.3 sgemm.f.3 sgemm.3 sgemv.f.3 sgemv.3 sger.f.3 sger.3 \
srot.f.3 srot.3 srotm.f.3 srotm.3 srotmg.f.3 srotmg.3 \
ssbmv.f.3 ssbmv.3 sscal.f.3 sscal.3 sspmv.f.3 sspmv.3 sspr.f.3 sspr.3 sspr2.f.3 sspr2.3 \
sswap.f.3 sswap.3 ssymm.f.3 ssymm.3 ssymv.f.3 ssymv.3 ssyr.f.3 ssyr.3 ssyr2.f.3 ssyr2.3 \
ssyr2k.f.3 ssyr2k.3 ssyrk.f.3 ssyrk.3 stbmv.f.3 stbmv.3 stbsv.f.3 stbsv.3 stpmv.f.3 stpmv.3 \
stpsv.f.3 stpsv.3 strmm.f.3 strmm.3 strmv.f.3 strmv.3 strsm.f.3 strsm.3 strsv.f.3 strsv.3 \
xerbla.3 xerbla_array.3 zaxpy.f.3 zaxpy.3 zcopy.f.3 zcopy.3 \
zdotc.f.3 zdotc.3 zdotu.f.3 zdotu.3 zdrot.f.3 zdrot.3 zdscal.f.3 zdscal.3 zgbmv.f.3 zgbmv.3 \
zgemm.f.3 zgemm.3 zgemv.f.3 zgemv.3 zgerc.f.3 zgerc.3 zgeru.f.3 zgeru.3 zhbmv.f.3 zhbmv.3 \
zhemm.f.3 zhemm.3 zhemv.f.3 zhemv.3 zher.f.3 zher.3 zher2.f.3 zher2.3 zher2k.f.3 zher2k.3 \
zherk.f.3 zherk.3 zhpmv.f.3 zhpmv.3 zhpr.f.3 zhpr.3 zhpr2.f.3 zhpr2.3 \
zscal.f.3 zscal.3 zswap.f.3 zswap.3 zsymm.f.3 zsymm.3 zsyr2k.f.3 zsyr2k.3 zsyrk.f.3 zsyrk.3 \
ztbmv.f.3 ztbmv.3 ztbsv.f.3 ztbsv.3 ztpmv.f.3 ztpmv.3 ztpsv.f.3 ztpsv.3 ztrmm.f.3 ztrmm.3 \
ztrmv.f.3 ztrmv.3 ztrsm.f.3 ztrsm.3 ztrsv.f.3 ztrsv.3 ../../blas/man/man3
cd ../..
popd

find manpages/blas/man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > blasmans

# remove weird man pages
pushd manpages/man/man3
rm -rf _Users_julie*
popd

# rename conflicting man pages
pushd manpages/man/man3
mv isnan.3 lapack-isnan.3
popd

find manpages/man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > lapackmans

cp -f manpages/blas/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3
cp -f manpages/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3

%ldconfig_scriptlets

%ldconfig_scriptlets -n blas

%if 0%{?arch64}
%ldconfig_scriptlets -n lapack64
%ldconfig_scriptlets -n lapack64_

%ldconfig_scriptlets -n blas64
%ldconfig_scriptlets -n blas64_
%endif

%files -f lapackmans
%doc README.md LICENSE lapackqref.ps
%{_libdir}/liblapack.so.*
%{_libdir}/liblapacke.so.*
%{_libdir}/libtmglib.so.*

%files devel
%{_includedir}/lapack*.h
%{_libdir}/liblapack.so
%{_libdir}/liblapacke.so
%{_libdir}/libtmglib.so
%{_libdir}/cmake/lapack-*
%{_libdir}/cmake/lapacke-*
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/pkgconfig/lapacke.pc
%if 0%{?arch64}
%{_libdir}/liblapack64.so
%{_libdir}/liblapacke64.so
%{_libdir}/libtmglib64.so
%{_libdir}/cmake/lapack64-*
%{_libdir}/cmake/lapacke64-*
%{_libdir}/pkgconfig/lapack64.pc
%{_libdir}/pkgconfig/lapacke64.pc
%{_libdir}/liblapack64_.so
%{_libdir}/liblapacke64_.so
%{_libdir}/libtmglib64_.so
%{_libdir}/cmake/lapack64_-*
%{_libdir}/cmake/lapacke64_-*
%{_libdir}/pkgconfig/lapack64_.pc
%{_libdir}/pkgconfig/lapacke64_.pc
%endif

%files static
%{_libdir}/liblapack.a
%{_libdir}/liblapacke.a
%{_libdir}/libtmglib.a
%if 0%{?arch64}
%{_libdir}/liblapack64.a
%{_libdir}/liblapack64_.a
%{_libdir}/liblapacke64.a
%{_libdir}/liblapacke64_.a
%{_libdir}/libtmglib64.a
%{_libdir}/libtmglib64_.a
%endif

%files -n blas -f blasmans
%doc blasqr.ps LICENSE
%{_libdir}/libblas.so.*
%{_libdir}/libcblas.so.*

%files -n blas-devel
%{_includedir}/cblas*.h
%{_libdir}/libblas.so
%{_libdir}/libcblas.so
%{_libdir}/cmake/cblas-*
%{_libdir}/pkgconfig/blas.pc
%{_libdir}/pkgconfig/cblas.pc
%if 0%{?arch64}
%{_libdir}/libblas64.so
%{_libdir}/libcblas64.so
%{_libdir}/cmake/cblas64*
%{_libdir}/pkgconfig/blas64.pc
%{_libdir}/pkgconfig/cblas64.pc
%{_libdir}/libblas64_.so
%{_libdir}/libcblas64_.so
%{_libdir}/pkgconfig/blas64_.pc
%{_libdir}/pkgconfig/cblas64_.pc
%endif

%files -n blas-static
%{_libdir}/libblas.a
%{_libdir}/libcblas.a
%if 0%{?arch64}
%{_libdir}/libblas64.a
%{_libdir}/libcblas64.a
%{_libdir}/libblas64_.a
%{_libdir}/libcblas64_.a
%endif

%if 0%{?arch64}
%files -n blas64
%doc LICENSE
%{_libdir}/libblas64.so.*
%{_libdir}/libcblas64.so.*

%files -n lapack64
%doc README.md LICENSE
%{_libdir}/liblapack64.so.*
%{_libdir}/liblapacke64.so.*
%{_libdir}/libtmglib64.so.*

%files -n blas64_
%doc LICENSE
%{_libdir}/libblas64_.so.*
%{_libdir}/libcblas64_.so.*

%files -n lapack64_
%doc README.md LICENSE
%{_libdir}/liblapack64_.so.*
%{_libdir}/liblapacke64_.so.*
%{_libdir}/libtmglib64_.so.*
%endif

%changelog
* Thu Aug 07 2025 Iñaki Úcar <iucar@fedoraproject.org> - 3.12.0-10
- Build 64-bit LAPACKE versions
- Fix 64_ variants to provide suffixes instead of prefixes, as stated
- Drop duplicated _pic libraries

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug  7 2024 Tom Callaway <spot@fedoraproject.org> - 3.12.0-7
- add upstream patch to fix DMD issues (thanks Iñaki Úcar)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 13 2024 Tom Callaway <spot@fedoraproject.org> - 3.12.0-5
- Add explicit requires to the devel subpackages (thanks to Jakub Martisko)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Tom Callaway <spot@fedoraproject.org> - 3.12.0-2
- rename isnan.3 to lapack-isnan.3 to avoid conflict with man-pages package

* Thu Jan  4 2024 Tom Callaway <spot@fedoraproject.org> - 3.12.0-1
- update to 3.12.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun  1 2023 Tom Callaway <spot@fedoraproject.org> - 3.11.0-4
- apply upstream fix to https://github.com/Reference-LAPACK/lapack/issues/763

* Fri May 19 2023 Iñaki Úcar <iucar@fedoraproject.org> - 3.11.0-3
- Adapt license tag to SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Tom Callaway <spot@fedoraproject.org> - 3.11.0-1
- update to 3.11.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 24 2022 Tom Callaway <spot@fedoraproject.org> - 3.10.1-1
- update to 3.10.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec  8 2021 Tom Callaway <spot@fedoraproject.org> - 3.10.0-4
- Fix out of bounds read in *larrv, CVE-2021-4048

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul  1 2021 Tom Callaway <spot@fedoraproject.org> - 3.10.0-2
- rename conflicting manpages (bz1978346)

* Wed Jun 30 2021 Tom Callaway <spot@fedoraproject.org> - 3.10.0-1
- update to 3.10.0

* Fri Apr  9 2021 Tom Callaway <spot@fedoraproject.org> - 3.9.1-1
- 3.9.1
- use upstream cmake build (no more hacked up Makefiles, huzzah)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 21 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.9.0-4
- make separate packages for 64-bit versions with and without suffix (bz1295965)

* Thu Mar 19 2020 Tom Callaway <spot@fedoraproject.org> - 3.9.0-3
- apply upstream fix for accidental removal of deprecated symbols from header file

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Tom Callaway <spot@fedoraproject.org> - 3.9.0-1
- update to 3.9.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Tom Callaway <spot@fedoraproject.org> - 3.8.0-12
- use --no-optimize-sibling-calls to work around gfortran issues

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Tom Callaway <spot@fedoraproject.org> - 3.8.0-9
- explicitly link liblapacke.so with liblapack to remove undefined-non-weak-symbols

* Mon Mar  5 2018 Tom Callaway <spot@fedoraproject.org> - 3.8.0-8
- use LDFLAGS for shared libs

* Mon Feb 26 2018 Tom Callaway <spot@fedoraproject.org> - 3.8.0-7
- add missing aawork functions back to lapacke makefile (bz1549262)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Björn Esser <besser82@fedoraproject.org> - 3.8.0-5
- Rebuilt for GCC8

* Wed Jan  3 2018 Tom Callaway <spot@fedoraproject.org> - 3.8.0-4
- fix cblas

* Mon Dec  4 2017 Tom Callaway <spot@fedoraproject.org> - 3.8.0-3
- build cblas
- include pkgconfig files.

* Fri Nov 17 2017 Tom Callaway <spot@fedoraproject.org> - 3.8.0-2
- add ilaenv2stage

* Wed Nov 15 2017 Tom Callaway <spot@fedoraproject.org> - 3.8.0-1
- update to 3.8.0

* Mon Aug 14 2017 Tom Callaway <spot@fedoraproject.org> - 3.7.1-5
- rename 64_ libraries to lib*64_*

* Fri Aug 11 2017 Tom Callaway <spot@fedoraproject.org> - 3.7.1-4
- move to 64_ suffix and symbol mangling (bz1295965)

* Thu Aug 10 2017 Tom Callaway <spot@fedoraproject.org> - 3.7.1-3
- include DSLASRC and ZCLASRC

* Wed Aug  9 2017 Tom Callaway <spot@fedoraproject.org> - 3.7.1-2
- fixup Makefile.lapack to include new stuff

* Tue Aug  1 2017 Tom Callaway <spot@fedoraproject.org> - 3.7.1-1
- update to 3.7.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Björn Esser <besser82@fedoraproject.org> - 3.6.1-3
- Rebuilt for GCC-7

* Mon Oct 10 2016 Tom Callaway <spot@fedoraproject.org> - 3.6.1-2
- properly set NOOPT flags during lapacke compile (thanks to sorear2@gmail.com)

* Wed Jul  6 2016 Tom Callaway <spot@fedoraproject.org> - 3.6.1-1
- update to 3.6.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Tom Callaway <spot@fedoraproject.org> - 3.6.0-6
- fix lapack Makefile to rebuild every file on every pass (thanks to adm.fkt.physik <at> tu-dortmund.de)

* Thu Dec  3 2015 Tom Callaway <spot@fedoraproject.org> - 3.6.0-5
- fix lapache static lib to include TMGLIB bits

* Wed Dec  2 2015 Tom Callaway <spot@fedoraproject.org> - 3.6.0-4
- build deprecated functions for lapacke (RHBZ #1287405)

* Sat Nov 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.6.0-3
- build deprecated functions also (RHBZ #1286349)

* Thu Nov 19 2015 Tom Callaway <spot@fedoraproject.org> - 3.6.0-2
- add missing functions, resolves bz1282958

* Tue Nov 17 2015 Tom Callaway <spot@fedoraproject.org> - 3.6.0-1
- update to 3.6.0

* Fri Sep 11 2015 Tom Callaway <spot@fedoraproject.org> - 3.5.0-12
- fix missing dependencies between subpackages
- delete broken and wrongly installed manpages
- fix isa_bits conditional

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 18 2014 Susi Lehtola <jussilehtola@fedoraproject.org> 3.5.0-10
- Add the -frecursive flag so that the functions are thread safe.

* Mon Oct 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.5.0-9
- Use generic macro to detect 64 bit platforms

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul  7 2014 Tom Callaway <spot@fedoraproject.org> - 3.5.0-7
- apply BLAS fixes from R

* Thu Jun 19 2014 Tom Callaway <spot@fedoraproject.org> - 3.5.0-6
- compile in tmglib object files, not static lib

* Wed Jun 18 2014 Tom Callaway <spot@fedoraproject.org> - 3.5.0-5
- link tmglib into lapacke

* Tue Jun 17 2014 Tom Callaway <spot@fedoraproject.org> - 3.5.0-4
- include matgen_obj items in lapacke library

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.5.0-2
- Don't include manual page directories (#1089412).
- Use standard group System Environment/Libraries in runtime library packages.

* Mon Nov 18 2013 Tom Callaway <spot@fedoraproject.org> - 3.5.0-1
- update to 3.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.2-2
- clean out non-free example files from source tarball

* Thu Feb 21 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.2-1
- update to 3.4.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.1-4
- fix 64bit sonames

* Fri Jan  4 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.1-3
- enable 64bit INTEGER variant subpackages

* Wed Oct 24 2012 Tom Callaway <spot@fedoraproject.org> - 3.4.1-2
- fix issue where lapacke was linking to testing functions (bz860332)

* Thu Sep 06 2012 Orion Poplawski <orion@cora.nwra.com> - 3.4.1-1
- Update to 3.4.1
- Rebase lapacke shared lib patch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Tom Callaway <spot@fedoraproject.org> - 3.4.0-1
- update to 3.4.0
- build and include lapacke

* Thu Jun 02 2011 Tom Callaway <spot@fedoraproject.org> - 3.3.1-1
- update to 3.3.1
- create /usr/share/man/manl/ as 0755 and own it in lapack and blas (bz634369)
- spec file cleanup

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 3.2.2-2
- fix a typo in Makefile.lapack causing #615618

* Wed Jul  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.2-1
- update to 3.2.2
- properly include license text
- static subpackages depend on -devel (they're not useful without it)
- clean up makefiles
- pass on version into makefiles, rather than manually hacking on each update

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-4
- Move static libs to static subpackages (resolves bz 545143)

* Fri Sep  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-3
- use RPM_OPT_O_FLAGS (-O0) everywhere necessary, drop RPM_OPT_SIZE_FLAGS (-Os) (bz 520518)

* Thu Aug 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-2
- don't enable xblas yet

* Fri Aug 14 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-1
- update to 3.2.1, spec file cleanups

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.1.1-7
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.1-4
- fix missing dependencies (bz 442915)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.1-3
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.1-2
- fix license (BSD)
- rebuild for BuildID

* Fri May 25 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.1-1
- bump to 3.1.1

* Fri Jan  5 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-4
- fix bugzillas 219740,219741

* Wed Dec 20 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-3
- make clean everywhere

* Wed Dec 20 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-2
- fix the Makefiles

* Tue Nov 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-1
- bump to 3.1.0

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-38
- bump for fc-6

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-37
- bump for FC5

* Mon Dec 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-36
- bump for gcc4.1

* Tue Nov 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-35
- try not to patch files that do not exist

* Tue Nov 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-34
- finish fixing bz 143340

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-33
- fix bz 169558

* Wed Sep 28 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-32
- move to latest upstream 3.0 tarballs
- add 8 missing BLAS functions from upstream blas tarball (bz 143340)

* Thu Sep 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-31
- actually install liblapack_pic.a

* Wed Sep 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-30
- make -devel packages
- make liblapack_pic.a package
- use dist tag

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-29
- package moves to Fedora Extras, gcc4

* Tue Dec 21 2004 Ivana Varekova <varekova@redhat.com>
- fix bug #143420 problem with compiler optimalizations

* Tue Nov 30 2004 Ivana Varekova <varekova@redhat.com>
- fix bug #138683 problem with compilation

* Thu Nov 11 2004 Ivana Varekova <varekova@redhat.com>
- fix build problem bug #138447

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Dec 31 2003 Jeff Johnson <jbj@jbj.org> 3.0-23
- link -lg2c explicitly into liblapack and libblas (#109079).

* Wed Aug 20 2003 Jeremy Katz <katzj@redhat.com> 3.0-22
- nuke -man subpackages (#97506)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Nov 10 2002 Jeff Johnson <jbj@redhat.com> 3.0-19
- rebuild with x86_64.

* Thu Jul 18 2002 Trond Eivind Glomsrod <teg@redhat.com> 3.0-18
- Remove an empty man page (#63569)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May  1 2002 Trond Eivind Glomsrod <teg@redhat.com> 3.0-15
- Rebuild

* Thu Feb 21 2002 Trond Eivind Glomsrod <teg@redhat.com> 3.0-14
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Aug 13 2001 Trond Eivind Glomsrod <teg@redhat.com> 3.0-12
- The man-pages for xerbla and lsame were in blas-man and lapack-man (#51605)

* Fri Jun  8 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Reenable optimization for IA64

* Fri May 25 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Add all patches from the LAPACK site as of 2001-05-25
- Use this workaround for IA64 instead
- Remove SPARC workaround
- Don't exclude IA64

* Thu Dec 07 2000 Trond Eivind Glomsrod <teg@redhat.com>
- rebuild for main distribution

* Mon Nov 20 2000 Trond Eivind Glomsrod <teg@redhat.com>
- add the LAPACK Quick Reference Guide to the docs
- add the BLAS Quick Reference Guide to the docs

* Tue Aug 01 2000 Trond Eivind Glomsrod <teg@redhat.com>
- fix lack of ldconfig in postuninstall script

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Trond Eivind Glomsrod <teg@redhat.com>
- updated with the latest updates (new tarfile..) from netlib

* Thu Jun 15 2000 Trond Eivind Glomsrod <teg@redhat.com>
- use %%{_mandir}
- added some flags to work around SPARC compiler bug

* Wed Jan 19 2000 Tim Powers <timp@redhat.com>
- bzipped sources to conserve space

* Tue Jan  4 2000 Jeff Johnson <jbj@redhat.com>
- build for PowerTools 6.2.

* Sat Dec 25 1999 Joachim Frieben <jfrieben@hotmail.com>
- updated to version v3.0 + update as of Tue Nov 30 1999

* Sat Oct 23 1999 Joachim Frieben <jfrieben@hotmail.com>
- updated Red Hat makefiles to v3.0

* Mon Aug 2 1999 Tim Powers <timp@redhat.com>
- updated to v3.0
- built for 6.1

* Mon Apr 12 1999 Michael Maher <mike@redhat.com>
- built package for 6.0

* Sat Oct 24 1998 Jeff Johnson <jbj@redhat.com>
- new description/summary text.

* Fri Jul 17 1998 Jeff Johnson <jbj@redhat.com>
- repackage for powertools.

* Sun Feb 15 1998 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
 [lapack-2.0-9]
 - No code updates, just built with a customized rpm -
   this should make dependencies right.

* Sat Feb 07 1998 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
 [lapack-2.0-8]
 - Total rewrite of the spec file
 - Added my own makefiles - libs should build better,
   static libs should work (and be faster than they
	would be if they had worked earlier ;)
 - No patch necessary anymore.
 - Renamed lapack-blas and lapack-blas-man to
   blas and blas-man. "Obsoletes:" tag added.
   (oh - and as always: Dedicated to the girl I
   love, Eline Skirnisdottir)

* Sat Dec 06 1997 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
 [lapack-2.0-7]
  - added a dependency to glibc, so people don't try with libc5

* Thu Nov 20 1997 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
  [lapack-2.0-6]
  - removed etime.c
  - compiled with egcs, and for glibc 2.0

* Sun Oct 12 1997 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
  [lapack-2.0-5]
  - added a changelog
  - cleaned up building of shared libs
  - now uses a BuildRoot
  - cleaned up the specfile
