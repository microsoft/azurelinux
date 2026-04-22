# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (C) 2018  Dave love, University of Manchester
# Licence as for the package source

# The full tests are very time-consuming
%bcond_with fulltest

# We need to manipulate the built *.so.%%sover
%global sover .4.0.0
%global soshort .4

%if 0%{?el7}
# Use devtoolset for avx512 support
%ifnarch ppc64le ppc64
%global dts 9
%endif
%endif

# Both these are necessary to avoid asm error
# error: bp cannot be used in ‘asm’ here
# Fixme: patch to localize this
%undefine _include_frame_pointers
%define _lto_cflags %{nil}

Name:		blis
Version:	2.0
Release: 3%{?dist}
Summary:	BLAS-like Library Instantiation Software Framework
License:	BSD-3-Clause
URL:		https://github.com/flame/blis
%if 0%{?commit}
Source0:	https://github.com/flame/blis/archive/%commit/%name-%shortcommit.tar.gz
%else
Source0:	https://github.com/flame/blis/archive/%version/%name-%version.tar.gz
%endif
BuildRequires:	perl
BuildRequires:	%{?dts:devtoolset-%{?dts}-binutils devtoolset-%{?dts}-}gcc
BuildRequires:	python3-devel gcc-gfortran chrpath
BuildRequires:	make
# memkind is currently only relevant for KNL as far as I know, but
# might be relevant in future for other targets with HBM.  It needs
# updating in el7.  It should support other targets, but only x86_64
# is packaged.
%ifarch x86_64
# removed from RHEL10
%if 0%{?el8}%{?el9}%{?fedora}
BuildRequires: memkind-devel
%endif
%endif

%global desc \
BLIS is a portable software framework for instantiating\
high-performance BLAS-like dense linear algebra libraries.  The\
framework was designed to isolate essential kernels of computation\
that, when optimized, immediately enable optimized implementations of\
most of its commonly used and computationally intensive operations.\
While BLIS exports a new BLAS-like API, it also includes a BLAS\
compatibility layer which gives application developers access to BLIS\
implementations via traditional BLAS routine calls.\
\
This packaging contains automatically-dispatched\
architecture-optimized kernels for some targets, notably recent x86_64.

%description
%desc

This is the serial version.


%package	devel
Summary:	Development files for %name
Requires:	%name%{?_isa} = %version-%release
Requires:	%name-openmp%{?_isa} = %version-%release
Requires:	%name-threads%{?_isa} = %version-%release
%if 0%{?__isa_bits} == 64
Requires:	%name-serial64%{?_isa} = %version-%release
Requires:	%name-openmp64%{?_isa} = %version-%release
Requires:	%name-threads64%{?_isa} = %version-%release
%endif

%description	devel
The %name-devel package contains libraries and header files for
developing applications that use %name.

%package serial64
Summary:	BLAS-like Library Instantiation Software Framework - 64-bit

%description serial64
%desc

This is the serial version with a 64-bit integer interface.

%package openmp
Summary:	BLAS-like Library Instantiation Software Framework - OpenMP

%description openmp
%desc

This is the OpenMP-parallelized version.

%package openmp64
Summary:	BLAS-like Library Instantiation Software Framework - OpenMP, 64-bit

%description openmp64
%desc

This is the OpenMP-parallelized version with a 64-bit integer interface.

# A pthreads version is necessary for Python (numpy) according to
# Debian openblas.
%package threads
Summary:	BLAS-like Library Instantiation Software Framework - pthreads

%description threads
%desc

This is the pthreads-parallelized version.

%package threads64
Summary:	BLAS-like Library Instantiation Software Framework - pthreads, 64-bit

%description threads64
%desc

This is the pthreads-parallelized version with a 64-bit integer interface.

%package srpm-macros
Summary:	BLIS architecture macros
BuildArch:	noarch

%description srpm-macros
BLIS architecture macros.


%prep
%setup -q %{?commit: -n %name-%commit}
# The soversion changed in release 0.7.0, but abipkgdiff suggests it
# shouldn't have, since only undocumented interfaces have changed from
# 0.6.0: removed bli_thread_get_env, bli_thread_init_rntm; indirect
# sub-types in bli_addd_ex; ARCH enum in bli_arch_query_id.
#echo %sover | awk -F. '{printf("%s\n%s.%s\n", $2,$3,$4)}' >so_version

%build
%{?dts:. /opt/rh/devtoolset-%{?dts}/enable}
case %_arch in
x86_64) arch=x86_64 ;;
# a57 runs on all aarch64 and the optimized micro-kernel should be a
# better default than generic.
# Fixme:  Include my changes for arm and ppc micro-arch dispatch.
aarch64) arch=cortexa57 ;;
armv7hl) arch=cortexa9 ;;	# Similarly to aarch64
*) arch=generic ;;
esac

# Hardening flags might be expected to affect performance, but appear
# not to.  With the f29 set and gcc 8 (but measured on EL6) for
# Haswell, a 5000×5000 DGEMM ran at 158295±565 MFLops with
# CFLAGS=$RPM_OPT_FLAGS and 158289±414 MFlops with no CFLAGS specified.
# Add back -O3, overridden by -O2 in RPM_OPT_FLAGS.
# -funsafe-math-optimizations vectorizes more, and passes tests
# <https://github.com/flame/blis/issues/259#issuecomment-463657085>
%global confflags --enable-debug=opt --disable-static --enable-shared --enable-verbose-make --enable-cblas
export CFLAGS="$RPM_OPT_FLAGS -O3 -funsafe-math-optimizations" LDFLAGS="%{?__global_ldflags}"
export PYTHON=%python3		# Needed by both configure and make

# It's not an autotools configure
./configure --prefix=$(pwd)/o %confflags -t openmp $arch
%make_build SOFLAGS="-shared -Wl,-soname=libbliso.so%sover"
make install

./configure --prefix=$(pwd)/p %confflags -t pthreads $arch
%make_build SOFLAGS="-shared -Wl,-soname=libblisp.so%sover"
make install

# Rename the libraries per soname and generate BLAS_compatible ones
mkdir -p blisblas{,o,p,64,o64,p64}
for d in o p; do
  cd $d/lib
  f=libblis.so%sover
  mv $f ${f/./$d.}
  ln -s libblis$d.so%sover libblis$d.so
  ln -s libblis$d.so%sover  libblis$d.so%soshort
  rm libblis.*
  cd ../..
  cc -shared -Wl,-soname=libblas.so.3 -L$(pwd)/$d/lib -lblis$d -o blisblas$d/libblas.so.3 $LDFLAGS
  ln -s libblas.so.3 blisblas$d/libblas.so
done

%if 0%{?__isa_bits} == 64

./configure --prefix=$(pwd)/64 %confflags -b 64 $arch
%make_build SOFLAGS="-shared -Wl,-soname=libblis64.so%sover"
make install

./configure --prefix=$(pwd)/o64 %confflags -b 64 -t openmp $arch
%make_build SOFLAGS="-shared -Wl,-soname=libbliso64.so%sover"
make install

./configure --prefix=$(pwd)/p64 %confflags -b 64 -t pthreads $arch
%make_build SOFLAGS="-shared -Wl,-soname=libblisp64.so%sover"
make install

for d in 64 o64 p64; do
  cd $d/lib
  f=libblis.so%sover
  mv $f ${f/./$d.}
  ln -s libblis$d.so%sover libblis$d.so
  ln -s libblis$d.so%sover libblis$d.so%soshort
  rm -f libblis.*
  cd ../..
  cc -shared -Wl,-soname=libblas64.so.3 -L$(pwd)/$d/lib -lblis$d -o blisblas$d/libblas64.so.3 $LDFLAGS
  ln -s libblas64.so.3 blisblas$d/libblas64.so
done

%endif

# done last for the benefit of check
./configure --prefix=$(pwd)/serial %confflags $arch
%make_build
make install
cc -shared -Wl,-soname=libblas.so.3 -L$(pwd)/serial/lib -lblis -o blisblas/libblas.so.3 $LDFLAGS
ln -s libblas.so.3 blisblas/libblas.so


%install
mkdir -p %buildroot%_libdir %buildroot%_includedir

cp -a {serial,o,p}/lib/* %buildroot%_libdir
mv serial/include/blis %buildroot%_includedir
for d in o p; do
  cp -a $d/include/blis %buildroot%_includedir/blis$d
done
%if 0%{?__isa_bits} == 64
cp -a {64,o64,p64}/lib/* %buildroot%_libdir
for d in 64 o64 p64; do
  cp -a $d/include/blis %buildroot%_includedir/blis$d
done
%endif
# Needed for debuginfo processing
chmod +x %buildroot%_libdir/*.so.*
cp -a blisblas* %buildroot%_libdir
# This is quite large.
gzip CHANGELOG
chrpath -d %buildroot%_libdir/*.so.*

cat <<EOF >README.Fedora
Fedora BLIS packaging
---------------------

Similarly to the OpenBLAS packaging, as well as the serial library
(libblis), there are versions named with suffix "o" using OpenMP, and
suffix "p" using pthreads.  Also, on 64-bit targets, there are
versions built with 64-bit integer interfaces, which have suffix "64".
Thus "libblaso64" is built for 64-bit integers and OpenMP
parallelization.  The cblas interface is included in each version.

For the BLAS interface, BLIS and OpenBLAS are expected to have similar
performance where they are optimized for the same micro-architectures,
but do show some performance differences in either direction.  BLIS
supports AVX512 on KNL and SKX, which OpenBLAS currently doesn't, and
will be more than twice as fast on such systems, which are the main
targets for this packaging.  BLIS' non-BLAS interface is obviously a
potential advantage generally, but it isn't currently used by any
Fedora packages.

There are shared library shims in %_libdir/blisblas* for each version
that provide sonames libblas.so.3 or libblas64.so.3 and so may be
linked dynamically instead of the reference libblas.  You can use an
ldconfig file so that this will be done automatically if the blis or
blis64 packages are installed, which will usually be a lot faster than
the reference version.  Otherwise, setting
LD_LIBRARY_PATH=%_libdir/blisblaso, say, will cause a binary
dynamically linked against libblas to run with the OpenMP BLIS version
instead, to allow multiple threads to be used.  The shims could be
extended to substitute the atlas and openblas libraries, but those can
be overridden by running with LD_PRELOAD=%_libdir/libblis.so%sover in
the environment.

Runtime dispatch on the micro-architecture is currently only available
on x86_64.  aarch64 will use cortexa57 instructions.  Other
architectures use the "generic" target, so OpenBLAS will be faster on
any of them that it supports (arm, power64, ix86, and s390x in Fedora).

The blis-srpm-macros package defines RPM macro %blis_opt_arches for
the architectures with optimized implementations in case the list is
extended in future.

EOF

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
mkdir -p %buildroot%macrosdir
cat <<EOF >%buildroot%macrosdir/macros.blis-srpm
# Architectures for for BLIS has an optimized implementation
%blis_opt_arches x86_64 aarch64
EOF


%check
%{?dts:. /opt/rh/devtoolset-%{?dts}/enable}
# A quick check which tests the Fortran BLAS interface with gfortran,
# unlike the "test" or "check" targets.
# Fixme: check a 64-bit version where relevant
gfortran -o dblat blastest/src/fortran/dblat3.f -Lblisblas -Lserial/lib -lblas -lblis
LD_LIBRARY_PATH=$(pwd)/serial/lib:$(pwd)/blisblas ./dblat <<+ || { cat dblat3.summ && false; }
'dblat3.summ'
6
'dblat3.snap'
-1
F
T
T
16.0
7
0 1 2 3 7 31 63
3
0.0 1.0 0.7
3
0.0 1.0 1.3
DGEMM  T
DSYMM  F
+

export LD_LIBRARY_PATH=`pwd`/serial/lib
%if %{with fulltest}
%make_build test
%else
%make_build check
%endif


%ldconfig_scriptlets
%ldconfig_scriptlets openmp
%ldconfig_scriptlets serial64
%ldconfig_scriptlets openmp64
%ldconfig_scriptlets threads
%ldconfig_scriptlets threads64

%global docs CHANGELOG.gz CREDITS README.md README.Fedora

%files
%doc %docs
%license LICENSE
%{_libdir}/libblis.so%{soshort}*
%{_libdir}/blisblas

%files openmp
%doc %docs
%license LICENSE
%{_libdir}/libbliso.so%{soshort}*
%{_libdir}/blisblaso

%files threads
%doc %docs
%license LICENSE
%{_libdir}/libblisp.so%{soshort}*
%{_libdir}/blisblasp

%if 0%{?__isa_bits} == 64

%files serial64
%doc %docs
%license LICENSE
%{_libdir}/libblis64.so%{soshort}*
%{_libdir}/blisblas64

%files openmp64
%doc %docs
%license LICENSE
%{_libdir}/libbliso64.so%{soshort}*
%{_libdir}/blisblaso64

%files threads64
%doc %docs
%license LICENSE
%{_libdir}/libblisp64.so%{soshort}*
%{_libdir}/blisblasp64

%endif

%files devel
%doc examples
%{_includedir}/*
%{_libdir}/libblis*.so

%files srpm-macros
%{macrosdir}/macros.blis-srpm

%changelog
* Tue Jul 29 2025 Dave Love <loveshack@fedoraproject.org> - 2.0-2
- Avoid memkind on EL10

* Tue Jul 29 2025 Dave Love <loveshack@fedoraproject.org> - 2.0-1
- Update to v. 2.0
- Fixes FTBFS with GCC 15 (#2336444)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Dave Love <loveshack@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0
- Drop patch
- Turn off LTO and keeping frame pointers

* Wed Sep 20 2023 Dave Love <loveshack@fedoraproject.org> - 0.7.0-13
- Don't BR /usr/bin/python (#2237696)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 28 2023  <vagrant@rhel8.localdomain> - 0.7.0-11
- Use SPDX licence tag

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Aug 16 2020 Dave Love <loveshack@fedoraproject.org> - 0.7.0-6
- Fix libblas64 soname

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul  6 2020 Dave Love <loveshack@fedoraproject.org> - 0.7.0-4
- Change conditional BR of memkind-devel

* Wed Jul  1 2020 Dave Love <loveshack@fedoraproject.org> - 0.7.0-3
- Patch to build 64-, not 32-bit version on s390x (#1852549)

* Wed May 27 2020 Dave Love <loveshack@fedoraproject.org> - 0.7.0-2
- Revert build for arches that don't actually have memkind packages

* Wed May 20 2020 Dave Love <loveshack@fedoraproject.org> - 0.7.0-1
- New version
- Drop patch
- Maybe use devtoolset-9

* Sun Mar 15 2020 Dave love <loveshack@fedoraproject.org> - 0.6.0-5
- Use cortexa9 config on arm32, rather than generic

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Dave love <loveshack@fedoraproject.org> - 0.6.0-4
- Patch to avoid popen (security)
- Replace patch1 with upstream change

* Sat Aug 17 2019 Dave love <loveshack@fedoraproject.org> - 0.6.0-3
- Patch out use of simd pragma
- Use devtoolset-8, not -6 on el6/7
- Fix dblat3 test

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun  4 2019 Dave Love <loveshack@fedoraproject.org> - 0.6.0-1
- New version

* Thu Feb 14 2019 Dave Love <loveshack@fedoraproject.org> - 0.5.1-2
- Allow rebuilding for EPEL
- This version fixes #1674701
- Use -funsafe-math-optimizations

* Sun Feb  3 2019 Dave Love <loveshack@fedoraproject.org> - 0.5.1-1
- New version with soname bump
- arm/arm64 families removed

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov  8 2018 Dave Love <loveshack@fedoraproject.org> - 0.5.0-1
- New version
- Drop python3 patch

* Thu Oct  4 2018 Dave Love <loveshack@fedoraproject.org> - 0.4.1-2
- Use LDFLAGS for BLAS shims
- Add srpm-macros package
- Don't override -O3 in CFLAGS
- Maybe use devtoolset in %%check
- Remove ld.so.conf files for blisblas libraries

* Tue Sep 11 2018 Dave Love <loveshack@fedoraproject.org> - 0.4.1-1
- New version
- Fix running el6 check
- Use default compilation flags
- Use chrpath, %%ldconfig_scriptlets

* Wed Aug 15 2018 Dave Love <loveshack@fedoraproject.org> - 0.4.0-1
- New version, with soname bump, build adjusted

* Mon Jun 18 2018 Dave Love <loveshack@fedoraproject.org> - 0.3.2-7
- Use python3 explicitly, with patch

* Tue Jun  5 2018 Dave Love <loveshack@fedoraproject.org> - 0.3.2-6
- Initial version for Fedora
