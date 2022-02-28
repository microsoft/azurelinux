Vendor:         Microsoft Corporation
Distribution:   Mariner
%global shortver	3
%global mediumver	%{shortver}.9

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%global arch64 1
%else
%global arch64 0
%endif

Summary: Numerical linear algebra package libraries
Name: lapack
Version: %{mediumver}.0
Release: 7%{?dist}
License: BSD
URL: http://www.netlib.org/lapack/
Source0: https://github.com/Reference-LAPACK/lapack/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: http://www.netlib.org/lapack/manpages.tgz
Source2: Makefile.blas
Source3: Makefile.lapack
Source4: http://www.netlib.org/lapack/lapackqref.ps
Source5: http://www.netlib.org/blas/blasqr.ps
Source6: Makefile.cblas
Patch3: lapack-3.9.0-make.inc.patch
Patch4: lapack-3.9.0-lapacke-shared.patch
Patch5: lapack-3.4.1-lapacke-disable-testing-functions.patch
Patch6: lapack-3.5.0-lapacke-matgenobj.patch
Patch7: lapack-3.9.0-lapacke-tmglib.patch
# Bugzilla 1814756
Patch8: https://github.com/Reference-LAPACK/lapack/commit/87536aa3c8bb0af00f66088fb6ac05d87509e011.patch
BuildRequires: gcc-gfortran, gawk
BuildRequires: make
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
%setup -q
%setup -q -D -T -a1
%patch3 -p1 -b .fedora
%patch4 -p1 -b .shared
# %patch5 -p1 -b .disable-functions
# %patch6 -p1 -b .matgenobj
%patch7 -p1 -b .tmglib
%patch8 -p1 -b .bz1814756

mkdir manpages
mv man/ manpages/

cp -f INSTALL/make.inc.gfortran make.inc
cp -f %{SOURCE2} BLAS/SRC/Makefile
cp -f %{SOURCE3} SRC/Makefile
cp -f %{SOURCE6} CBLAS/src/Makefile

sed -i "s|@SHORTVER@|%{shortver}|g" BLAS/SRC/Makefile
sed -i "s|@SHORTVER@|%{shortver}|g" SRC/Makefile
sed -i "s|@SHORTVER@|%{shortver}|g" LAPACKE/Makefile
sed -i "s|@SHORTVER@|%{shortver}|g" CBLAS/src/Makefile
sed -i "s|@LONGVER@|%{version}|g" BLAS/SRC/Makefile
sed -i "s|@LONGVER@|%{version}|g" SRC/Makefile
sed -i "s|@LONGVER@|%{version}|g" LAPACKE/Makefile
sed -i "s|@LONGVER@|%{version}|g" CBLAS/src/Makefile

%build
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -frecursive --no-optimize-sibling-calls"
RPM_OPT_O_FLAGS=$(echo $RPM_OPT_FLAGS | sed 's|-O2|-O0|')
export FC=gfortran

# Build BLAS
pushd BLAS/SRC
FFLAGS="$RPM_OPT_O_FLAGS" make dcabs1.o
FFLAGS="$RPM_OPT_FLAGS" CFLAGS="$RPM_OPT_FLAGS" make static
cp libblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fPIC" make dcabs1.o
FFLAGS="$RPM_OPT_FLAGS -fPIC" CFLAGS="$RPM_OPT_FLAGS -fPIC" LDFLAGS="%{build_ldflags}" make shared
cp libblas.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
%if 0%{?arch64}
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fdefault-integer-8" make dcabs1.o
FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS" make static
cp libblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/libblas64.a
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" make dcabs1.o
FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC" LDFLAGS="%{build_ldflags}" make shared
cp libblas.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/libblas64.so.%{version}
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fdefault-integer-8" make dcabs1.o
SYMBOLSUFFIX="64_" FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS" make static
cp libblas64_.a ${RPM_BUILD_DIR}/%{name}-%{version}/libblas64_.a
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" make dcabs1.o
SYMBOLSUFFIX="64_" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC" LDFLAGS="%{build_ldflags}" make shared
cp libblas64_.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/libblas64_.so.%{version}
%endif
popd

ln -s libblas.so.%{version} libblas.so
%if 0%{?arch64}
ln -s libblas64.so.%{version} libblas64.so
ln -s libblas64_.so.%{version} libblas64_.so
%endif

# Build CBLAS
cp CBLAS/include/cblas_mangling_with_flags.h.in CBLAS/include/cblas_mangling.h
pushd CBLAS/src
FFLAGS="$RPM_OPT_FLAGS" CFLAGS="$RPM_OPT_FLAGS -I../include" make static
cp libcblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/
make clean
FFLAGS="$RPM_OPT_FLAGS -fPIC" CFLAGS="$RPM_OPT_FLAGS -fPIC -I../include" LDFLAGS="%{build_ldflags}" make shared
cp libcblas.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
%if 0%{?arch64}
make clean
FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -I../include" make static
cp libcblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/libcblas64.a
make clean
FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC -I../include" LDFLAGS="%{build_ldflags}" make shared
cp libcblas.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/libcblas64.so.%{version}
make clean
SYMBOLSUFFIX="64_" FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -I../include" make static
cp libcblas64_.a ${RPM_BUILD_DIR}/%{name}-%{version}/libcblas64_.a
make clean
SYMBOLSUFFIX="64_" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC -I../include" LDFLAGS="%{build_ldflags}" make shared
cp libcblas64_.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/libcblas64_.so.%{version}
%endif
popd

ln -s libcblas.so.%{version} libcblas.so
%if 0%{?arch64}
ln -s libcblas64.so.%{version} libcblas64.so
ln -s libcblas64_.so.%{version} libcblas64_.so
%endif

# Build the static dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS" FFLAGS="$RPM_OPT_FLAGS"
popd

# Build the static lapack library
pushd SRC
make FFLAGS="$RPM_OPT_FLAGS" CFLAGS="$RPM_OPT_FLAGS" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

# Build the static with pic dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fPIC" FFLAGS="$RPM_OPT_FLAGS -fPIC"
popd

# Build the static with pic lapack library
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fPIC" CFLAGS="$RPM_OPT_FLAGS -fPIC" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack_pic.a
popd

%if 0%{?arch64}
# Build the static dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fdefault-integer-8" FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8"
popd

# Build the static lapack library
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack64.a
popd

# Build the static with pic dlamch, dsecnd, lsame, second, slamch bits (64bit INTEGER)
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8"
popd

# Build the static with pic lapack library (64bit INTEGER)
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack_pic64.a
popd

# Build the static dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fdefault-integer-8" FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8"
popd

# Build the static lapack library
pushd SRC
make clean
make SYMBOLSUFFIX="64_" FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS" static
cp liblapack64_.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack64_.a
popd

# Build the static with pic dlamch, dsecnd, lsame, second, slamch bits (64bit INTEGER)
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8"
popd

# Build the static with pic lapack library (64bit INTEGER)
pushd SRC
make clean
make SYMBOLSUFFIX="64_" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC" static
cp liblapack64_.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack_pic64_.a
popd
%endif

# Build the shared dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fPIC" FFLAGS="$RPM_OPT_FLAGS -fPIC"
popd

# Build the shared lapack library
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fPIC" CFLAGS="$RPM_OPT_FLAGS -fPIC" LDFLAGS="%{build_ldflags}" shared
cp liblapack.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

%if 0%{?arch64}
# Build the shared dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8"
popd

# Build the shared lapack library
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" LDFLAGS="%{build_ldflags}" shared
cp liblapack.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack64.so.%{version}
popd

# Build the shared dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8"
popd

# Build the shared lapack library
pushd SRC
make clean
make SYMBOLSUFFIX="64_" FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" LDFLAGS="%{build_ldflags}" shared
cp liblapack64_.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack64_.so.%{version}
popd
%endif

ln -s liblapack.so.%{version} liblapack.so
%if 0%{?arch64}
ln -s liblapack64.so.%{version} liblapack64.so
ln -s liblapack64_.so.%{version} liblapack64_.so
%endif

# Build the lapacke libraries
make FFLAGS="$RPM_OPT_FLAGS -fPIC" FFLAGS_NOOPT="$RPM_OPT_O_FLAGS -fPIC" tmglib
pushd LAPACKE
make clean
make CFLAGS="$RPM_OPT_FLAGS" BUILD_DEPRECATED="true" lapacke
make clean
make CFLAGS="$RPM_OPT_FLAGS -fPIC" BUILD_DEPRECATED="true" LDFLAGS="%{build_ldflags}" shlib
# cp liblapacke.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

cp -p %{SOURCE4} lapackqref.ps
cp -p %{SOURCE5} blasqr.ps

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man3
chmod 755 %{buildroot}%{_mandir}/man3

for f in liblapack.so.%{version} libblas.so.%{version} libcblas.so.%{version} liblapacke.so.%{version} \
         libblas.a libcblas.a liblapack.a liblapack_pic.a liblapacke.a; do
  cp -f $f ${RPM_BUILD_ROOT}%{_libdir}/$f
done

%if 0%{?arch64}
for f in liblapack64.so.%{version} libblas64.so.%{version} libcblas64.so.%{version} \
         liblapack64_.so.%{version} libblas64_.so.%{version} libcblas64_.so.%{version} \
         libblas64.a libcblas64.a liblapack64.a liblapack_pic64.a \
         libblas64_.a libcblas64_.a liblapack64_.a liblapack_pic64_.a; do
  cp -f $f ${RPM_BUILD_ROOT}%{_libdir}/$f
done
%endif

# Blas manpages
pushd manpages/
mkdir -p blas/man/man3
cd man/man3/
mv caxpy.f.3 caxpy.3 ccopy.f.3 ccopy.3 cdotc.f.3 cdotc.3 cdotu.f.3 cdotu.3 cgbmv.f.3 cgbmv.3 \
cgemm.f.3 cgemm.3 cgemv.f.3 cgemv.3 cgerc.f.3 cgerc.3 cgeru.f.3 cgeru.3 chbmv.f.3 chbmv.3 \
chemm.f.3 chemm.3 chemv.f.3 chemv.3 cher.f.3 cher.3 cher2.f.3 cher2.3 cher2k.f.3 cher2k.3 \
cherk.f.3 cherk.3 chpmv.f.3 chpmv.3 chpr.f.3 chpr.3 chpr2.f.3 chpr2.3 crotg.f.3 crotg.3 \
cscal.f.3 cscal.3 csrot.f.3 csrot.3 csscal.f.3 csscal.3 cswap.f.3 cswap.3 csymm.f.3 \
csymm.3 csyr2k.f.3 csyr2k.3 csyrk.f.3 csyrk.3 ctbmv.f.3 ctbmv.3 ctbsv.f.3 ctbsv.3 ctpmv.f.3 \
ctpmv.3 ctpsv.f.3 ctpsv.3 ctrmm.f.3 ctrmm.3 ctrmv.f.3 ctrmv.3 ctrsm.f.3 ctrsm.3 ctrsv.f.3 \
ctrsv.3 dasum.f.3 dasum.3 daxpy.f.3 daxpy.3 dcabs1.f.3 dcabs1.3 dcopy.f.3 dcopy.3 ddot.f.3 \
ddot.3 dgbmv.f.3 dgbmv.3 dgemm.f.3 dgemm.3 dgemv.f.3 dgemv.3 dger.f.3 dger.3 dnrm2.f.3 \
dnrm2.3 drot.f.3 drot.3 drotg.f.3 drotg.3 drotm.f.3 drotm.3 drotmg.f.3 drotmg.3 dsbmv.f.3 \
dsbmv.3 dscal.f.3 dscal.3 dsdot.f.3 dsdot.3 dspmv.f.3 dspmv.3 dspr.f.3 dspr.3 dspr2.f.3 \
dspr2.3 dswap.f.3 dswap.3 dsymm.f.3 dsymm.3 dsymv.f.3 dsymv.3 dsyr.f.3 dsyr.3 dsyr2.f.3 \
dsyr2.3 dsyr2k.f.3 dsyr2k.3 dsyrk.f.3 dsyrk.3 dtbmv.f.3 dtbmv.3 dtbsv.f.3 dtbsv.3 dtpmv.f.3 \
dtpmv.3 dtpsv.f.3 dtpsv.3 dtrmm.f.3 dtrmm.3 dtrmv.f.3 dtrmv.3 dtrsm.f.3 dtrsm.3 dtrsv.f.3 \
dtrsv.3 dzasum.f.3 dzasum.3 dznrm2.f.3 dznrm2.3 icamax.f.3 icamax.3 idamax.f.3 idamax.3 \
isamax.f.3 isamax.3 izamax.f.3 izamax.3 lsame.3 sasum.f.3 sasum.3 saxpy.f.3 saxpy.3 \
scabs1.f.3 scabs1.3 scasum.f.3 scasum.3 scnrm2.f.3 scnrm2.3 scopy.f.3 scopy.3 sdot.f.3 sdot.3 \
sdsdot.f.3 sdsdot.3 sgbmv.f.3 sgbmv.3 sgemm.f.3 sgemm.3 sgemv.f.3 sgemv.3 sger.f.3 sger.3 \
snrm2.f.3 snrm2.3 srot.f.3 srot.3 srotg.f.3 srotg.3 srotm.f.3 srotm.3 srotmg.f.3 srotmg.3 \
ssbmv.f.3 ssbmv.3 sscal.f.3 sscal.3 sspmv.f.3 sspmv.3 sspr.f.3 sspr.3 sspr2.f.3 sspr2.3 \
sswap.f.3 sswap.3 ssymm.f.3 ssymm.3 ssymv.f.3 ssymv.3 ssyr.f.3 ssyr.3 ssyr2.f.3 ssyr2.3 \
ssyr2k.f.3 ssyr2k.3 ssyrk.f.3 ssyrk.3 stbmv.f.3 stbmv.3 stbsv.f.3 stbsv.3 stpmv.f.3 stpmv.3 \
stpsv.f.3 stpsv.3 strmm.f.3 strmm.3 strmv.f.3 strmv.3 strsm.f.3 strsm.3 strsv.f.3 strsv.3 \
xerbla.3 xerbla_array.3 zaxpy.f.3 zaxpy.3 zcopy.f.3 zcopy.3 \
zdotc.f.3 zdotc.3 zdotu.f.3 zdotu.3 zdrot.f.3 zdrot.3 zdscal.f.3 zdscal.3 zgbmv.f.3 zgbmv.3 \
zgemm.f.3 zgemm.3 zgemv.f.3 zgemv.3 zgerc.f.3 zgerc.3 zgeru.f.3 zgeru.3 zhbmv.f.3 zhbmv.3 \
zhemm.f.3 zhemm.3 zhemv.f.3 zhemv.3 zher.f.3 zher.3 zher2.f.3 zher2.3 zher2k.f.3 zher2k.3 \
zherk.f.3 zherk.3 zhpmv.f.3 zhpmv.3 zhpr.f.3 zhpr.3 zhpr2.f.3 zhpr2.3 zrotg.f.3 zrotg.3 \
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

find manpages/man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > lapackmans

cp -f manpages/blas/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3
#cp -f manpages/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3

# Cblas headers
mkdir -p %{buildroot}%{_includedir}/cblas/
cp -a CBLAS/include/*.h %{buildroot}%{_includedir}/cblas/

# Lapacke headers
mkdir -p %{buildroot}%{_includedir}/lapacke/
cp -a LAPACKE/include/*.h %{buildroot}%{_includedir}/lapacke/

pushd %{buildroot}%{_libdir}
ln -sf liblapack.so.%{version} liblapack.so
ln -sf liblapack.so.%{version} liblapack.so.%{shortver}
ln -sf liblapack.so.%{version} liblapack.so.%{mediumver}
ln -sf libblas.so.%{version} libblas.so
ln -sf libblas.so.%{version} libblas.so.%{shortver}
ln -sf libblas.so.%{version} libblas.so.%{mediumver}
ln -sf libcblas.so.%{version} libcblas.so
ln -sf libcblas.so.%{version} libcblas.so.%{shortver}
ln -sf libcblas.so.%{version} libcblas.so.%{mediumver}
ln -sf liblapacke.so.%{version} liblapacke.so
ln -sf liblapacke.so.%{version} liblapacke.so.%{shortver}
ln -sf liblapacke.so.%{version} liblapacke.so.%{mediumver}
%if 0%{?arch64}
ln -sf liblapack64.so.%{version} liblapack64.so
ln -sf liblapack64.so.%{version} liblapack64.so.%{shortver}
ln -sf liblapack64.so.%{version} liblapack64.so.%{mediumver}
ln -sf libblas64.so.%{version} libblas64.so
ln -sf libblas64.so.%{version} libblas64.so.%{shortver}
ln -sf libblas64.so.%{version} libblas64.so.%{mediumver}
ln -sf libcblas64.so.%{version} libcblas64.so
ln -sf libcblas64.so.%{version} libcblas64.so.%{shortver}
ln -sf libcblas64.so.%{version} libcblas64.so.%{mediumver}
ln -sf liblapack64_.so.%{version} liblapack64_.so
ln -sf liblapack64_.so.%{version} liblapack64_.so.%{shortver}
ln -sf liblapack64_.so.%{version} liblapack64_.so.%{mediumver}
ln -sf libblas64_.so.%{version} libblas64_.so
ln -sf libblas64_.so.%{version} libblas64_.so.%{shortver}
ln -sf libblas64_.so.%{version} libblas64_.so.%{mediumver}
ln -sf libcblas64_.so.%{version} libcblas64_.so
ln -sf libcblas64_.so.%{version} libcblas64_.so.%{shortver}
ln -sf libcblas64_.so.%{version} libcblas64_.so.%{mediumver}
%endif
popd

# pkgconfig
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
cp -a lapack.pc.in %{buildroot}%{_libdir}/pkgconfig/lapack.pc
sed -i 's|@CMAKE_INSTALL_FULL_LIBDIR@|%{_libdir}|g' %{buildroot}%{_libdir}/pkgconfig/lapack.pc
sed -i 's|@CMAKE_INSTALL_FULL_INCLUDEDIR@|%{_includedir}|g' %{buildroot}%{_libdir}/pkgconfig/lapack.pc
sed -i 's|@LAPACK_VERSION@|%{version}|g' %{buildroot}%{_libdir}/pkgconfig/lapack.pc
%if 0%{?arch64}
cp -a %{buildroot}%{_libdir}/pkgconfig/lapack.pc %{buildroot}%{_libdir}/pkgconfig/lapack64.pc
sed -i 's|-llapack|-llapack64|g' %{buildroot}%{_libdir}/pkgconfig/lapack64.pc
sed -i 's|blas|blas64|g' %{buildroot}%{_libdir}/pkgconfig/lapack64.pc
cp -a %{buildroot}%{_libdir}/pkgconfig/lapack.pc %{buildroot}%{_libdir}/pkgconfig/lapack64_.pc
sed -i 's|-llapack|-llapack64_|g' %{buildroot}%{_libdir}/pkgconfig/lapack64_.pc
sed -i 's|blas|blas64_|g' %{buildroot}%{_libdir}/pkgconfig/lapack64_.pc
%endif
cp -a BLAS/blas.pc.in %{buildroot}%{_libdir}/pkgconfig/blas.pc
sed -i 's|@CMAKE_INSTALL_FULL_LIBDIR@|%{_libdir}|g' %{buildroot}%{_libdir}/pkgconfig/blas.pc
sed -i 's|@CMAKE_INSTALL_FULL_INCLUDEDIR@|%{_includedir}|g' %{buildroot}%{_libdir}/pkgconfig/blas.pc
sed -i 's|@LAPACK_VERSION@|%{version}|g' %{buildroot}%{_libdir}/pkgconfig/blas.pc
%if 0%{?arch64}
cp -a %{buildroot}%{_libdir}/pkgconfig/blas.pc %{buildroot}%{_libdir}/pkgconfig/blas64.pc
sed -i 's|-lblas|-lblas64|g' %{buildroot}%{_libdir}/pkgconfig/blas64.pc
cp -a %{buildroot}%{_libdir}/pkgconfig/blas.pc %{buildroot}%{_libdir}/pkgconfig/blas64_.pc
sed -i 's|-lblas|-lblas64_|g' %{buildroot}%{_libdir}/pkgconfig/blas64_.pc
%endif
cp -a LAPACKE/lapacke.pc.in %{buildroot}%{_libdir}/pkgconfig/lapacke.pc
sed -i 's|@CMAKE_INSTALL_FULL_LIBDIR@|%{_libdir}|g' %{buildroot}%{_libdir}/pkgconfig/lapacke.pc
sed -i 's|@CMAKE_INSTALL_FULL_INCLUDEDIR@|%{_includedir}/lapacke|g' %{buildroot}%{_libdir}/pkgconfig/lapacke.pc
sed -i 's|@LAPACK_VERSION@|%{version}|g' %{buildroot}%{_libdir}/pkgconfig/lapacke.pc
cp -a CBLAS/cblas.pc.in %{buildroot}%{_libdir}/pkgconfig/cblas.pc
sed -i 's|@CMAKE_INSTALL_FULL_LIBDIR@|%{_libdir}|g' %{buildroot}%{_libdir}/pkgconfig/cblas.pc
sed -i 's|@CMAKE_INSTALL_FULL_INCLUDEDIR@|%{_includedir}/cblas|g' %{buildroot}%{_libdir}/pkgconfig/cblas.pc
sed -i 's|@LAPACK_VERSION@|%{version}|g' %{buildroot}%{_libdir}/pkgconfig/cblas.pc
%if 0%{?arch64}
cp -a %{buildroot}%{_libdir}/pkgconfig/cblas.pc %{buildroot}%{_libdir}/pkgconfig/cblas64.pc
sed -i 's|-lcblas|-lcblas64|g' %{buildroot}%{_libdir}/pkgconfig/cblas64.pc
sed -i 's|Requires.private: blas|Requires.private: blas64|g' %{buildroot}%{_libdir}/pkgconfig/cblas64.pc
cp -a %{buildroot}%{_libdir}/pkgconfig/cblas.pc %{buildroot}%{_libdir}/pkgconfig/cblas64_.pc
sed -i 's|-lcblas|-lcblas64_|g' %{buildroot}%{_libdir}/pkgconfig/cblas64_.pc
sed -i 's|Requires.private: blas|Requires.private: blas64_|g' %{buildroot}%{_libdir}/pkgconfig/cblas64_.pc
%endif

%ldconfig_scriptlets

%ldconfig_scriptlets -n blas

%if 0%{?arch64}
%ldconfig_scriptlets -n lapack64
%ldconfig_scriptlets -n lapack64_

%ldconfig_scriptlets -n blas64
%ldconfig_scriptlets -n blas64_
%endif

%files
%doc README.md LICENSE lapackqref.ps
%{_libdir}/liblapack.so.*
%{_libdir}/liblapacke.so.*

%files devel
%{_includedir}/lapacke/
%{_libdir}/liblapack.so
%{_libdir}/liblapacke.so
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/pkgconfig/lapacke.pc
%if 0%{?arch64}
%{_libdir}/liblapack64.so
%{_libdir}/pkgconfig/lapack64.pc
%{_libdir}/liblapack64_.so
%{_libdir}/pkgconfig/lapack64_.pc
%endif

%files static
%{_libdir}/liblapack.a
%{_libdir}/liblapack_pic.a
%{_libdir}/liblapacke.a
%if 0%{?arch64}
%{_libdir}/liblapack64.a
%{_libdir}/liblapack_pic64.a
%{_libdir}/liblapack64_.a
%{_libdir}/liblapack_pic64_.a
%endif

%files -n blas -f blasmans
%doc blasqr.ps LICENSE
%{_libdir}/libblas.so.*
%{_libdir}/libcblas.so.*

%files -n blas-devel
%{_includedir}/cblas/
%{_libdir}/libblas.so
%{_libdir}/libcblas.so
%{_libdir}/pkgconfig/blas.pc
%{_libdir}/pkgconfig/cblas.pc
%if 0%{?arch64}
%{_libdir}/libblas64.so
%{_libdir}/libcblas64.so
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

%files -n blas64_
%doc LICENSE
%{_libdir}/libblas64_.so.*
%{_libdir}/libcblas64_.so.*

%files -n lapack64_
%doc README.md LICENSE
%{_libdir}/liblapack64_.so.*
%endif

%changelog
* Tue Sep 14 2021 Muhammad Falak <mwani@microsoft.com> - 3.9.0-7
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Avoid shiping manpages for 'lapack' as it hangs build.

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
