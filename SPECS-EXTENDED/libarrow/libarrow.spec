%define _unpackaged_files_terminate_build 0 
%bcond_without use_flight
%bcond_with use_plasma
%bcond_with use_gandiva
%bcond_with use_mimalloc
%bcond_without use_ninja
# TODO: Enable this. This works on local but is fragile on GitHub Actions and
# Travis CI.
%bcond_with use_s3
%bcond_without have_rapidjson
%bcond_without have_re2
%bcond_without have_utf8proc
 
Name:	libarrow
Version:	15.0.0
Release:	5%{?dist}
Summary:	A toolbox for accelerated data interchange and in-memory processing
License:	Apache-2.0
URL:		https://arrow.apache.org/
Requires:	%{name}-doc = %{version}-%{release}
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:       https://github.com/apache/arrow/archive/refs/tags/apache-arrow-%{version}.tar.gz#/libarrow-%{version}.tar.gz
Patch0001: 0001-python-pyproject.toml.patch
 
# Apache ORC (liborc) has numerous compile errors and apparently assumes
# a 64-bit build and runtime environment. This is only consumer of the liborc
# package, and in turn the only consumer of this and liborc is Ceph, which
# is also 64-bit only
ExcludeArch:	%{ix86} %{arm}
BuildRequires:	bison
BuildRequires:	boost-devel
BuildRequires:	brotli-devel
BuildRequires:	bzip2-devel
BuildRequires:	cmake
%if %{with use_ninja}
BuildRequires:	ninja-build
%endif
BuildRequires:	meson
%if %{with use_s3}
BuildRequires:	curl-devel
%endif
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:	gflags-devel
BuildRequires:	libzstd-devel
BuildRequires:	lz4-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	python3-numpy
BuildRequires:	python3-Cython
BuildRequires:	abseil-cpp-devel
BuildRequires:	c-ares-devel
BuildRequires:	thrift-devel
%if %{with have_rapidjson}
BuildRequires:	rapidjson-devel
%endif
%if %{with have_re2}
BuildRequires:	re2-devel
%endif
BuildRequires:	snappy-devel
%if %{with have_utf8proc}
BuildRequires:	utf8proc-devel
%endif
BuildRequires:	zlib-devel
#BuildRequires:	liborc-devel
%if %{with use_gandiva}
BuildRequires:	llvm-devel
BuildRequires:	ncurses-devel
%endif
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
 
# Additional pyarrow build requirements; see also %%generate_buildrequires
BuildRequires:  python3dist(cffi)
 
%description
Apache Arrow defines a language-independent columnar memory
format for flat and hierarchical data, organized for efficient
analytic operations on modern hardware like CPUs and GPUs. The
Arrow memory format also supports zero-copy reads for lightning-
fast data access without serialization overhead

#--------------------------------------------------------------------
 
%package doc
Summary:	Documentation files for Apache Arrow C++
BuildArch:	noarch
 
%description doc
Documentation files for Apache Arrow C++.
 
#--------------------------------------------------------------------
 
%package devel
Summary:	Libraries and header files for Apache Arrow C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	brotli-devel
Requires:	bzip2-devel
Requires:	libzstd-devel
Requires:	lz4-devel
Requires:	openssl-devel
%if %{with have_rapidjson}
Requires:	rapidjson-devel
%endif
%if %{with have_re2}
Requires:	re2-devel
%endif
Requires:	snappy-devel
%if %{with have_utf8proc}
Requires:	utf8proc-devel
%endif
Requires:	zlib-devel
 
%description devel
Libraries and header files for Apache Arrow C++.

#--------------------------------------------------------------------
 
%package -n parquet-libs
Summary:	Runtime libraries for Apache Parquet C++
Requires:	boost-program-options
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}
Requires:	openssl
 
%description -n parquet-libs
This package contains the libraries for Apache Parquet C++.
 
#--------------------------------------------------------------------

%package -n parquet-libs-devel
Summary:	Libraries and header files for Apache Parquet C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	parquet-libs%{?_isa} = %{version}-%{release}
Requires:	zlib-devel
 
%description -n parquet-libs-devel
Libraries and header files for Apache Parquet C++.
 
#--------------------------------------------------------------------

%prep
%autosetup -p1 -n arrow-apache-arrow-%{version}
# We do not need to (nor can we) build for an old version of numpy:
sed -r -i 's/(oldest-supported-)(numpy)/\2/' python/pyproject.toml
 

%build
pushd cpp
%cmake \
  -DARROW_WITH_PROTOBUF=OFF \
  -DARROW_FLIGHT:BOOL=OFF \
  -DARROW_ORC=OFF \
  -DARROW_PARQUET:BOOL=ON \
  -DARROW_PYTHON:BOOL=ON \
  -DARROW_JEMALLOC:BOOL=OFF \
  -DARROW_SIMD_LEVEL=NONE \
  -DARROW_RUNTIME_SIMD_LEVEL=NONE \
  -DGRPC_SOURCE=SYSTEM \
  -Dxsimd_SOURCE=SYSTEM \
  -DARROW_WITH_BROTLI:BOOL=ON \
  -DARROW_WITH_BZ2:BOOL=ON \
  -DARROW_WITH_LZ4:BOOL=ON \
  -DARROW_WITH_SNAPPY:BOOL=ON \
  -DARROW_WITH_ZLIB:BOOL=ON \
  -DARROW_WITH_ZSTD:BOOL=OFF \
  -DARROW_USE_XSIMD:BOOL=ON \
  -DARROW_BUILD_STATIC:BOOL=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_COLOR_MAKEFILE:BOOL=OFF \
  -DARROW_USE_CCACHE:BOOL=OFF \
  -DCMAKE_UNITY_BUILD:BOOL=ON \
  -DPARQUET_REQUIRE_ENCRYPTION:BOOL=ON \
  -DPythonInterp_FIND_VERSION:BOOL=ON \
  -DPythonInterp_FIND_VERSION_MAJOR=3 \

 
export VERBOSE=1
export GCC_COLORS=
%cmake_build
popd
rm -rf /tmp/usr
 
#--------------------------------------------------------------------
%install
  
pushd cpp
%cmake_install
popd
#--------------------------------------------------------------------

%files
%{_libdir}/libarrow.so.*

%files doc
%license LICENSE.txt
%doc README.md NOTICE.txt
%exclude %{_docdir}/arrow/
 
%files devel
%dir %{_includedir}/arrow/
     %{_includedir}/arrow/*
%exclude %{_includedir}/arrow/dataset/
%if %{with use_flight}
%exclude %{_includedir}/arrow/flight/
%exclude %{_includedir}/arrow-flight-glib
%endif
%exclude %{_libdir}/cmake/Arrow/FindBrotliAlt.cmake
%exclude %{_libdir}/cmake/Arrow/Findlz4Alt.cmake
%exclude %{_libdir}/cmake/Arrow/FindORC.cmake
%exclude %{_libdir}/cmake/Arrow/FindorcAlt.cmake
%exclude %{_libdir}/cmake/Arrow/FindSnappyAlt.cmake
%exclude %{_libdir}/cmake/Arrow/FindgRPCAlt.cmake
%exclude %{_libdir}/cmake/Arrow/Findre2Alt.cmake
%exclude %{_libdir}/cmake/Arrow/Findutf8proc.cmake
%exclude %{_libdir}/cmake/Arrow/FindzstdAlt.cmake
%exclude %{_libdir}/cmake/Arrow/FindThriftAlt.cmake
%exclude %{_libdir}/cmake/Arrow/FindOpenSSLAlt.cmake
%exclude %{_libdir}/cmake/Arrow/FindProtobufAlt.cmake
%dir %{_libdir}/cmake/Arrow/
     %{_libdir}/cmake/Arrow/ArrowConfig*.cmake
     %{_libdir}/cmake/Arrow/ArrowOptions.cmake
     %{_libdir}/cmake/Arrow/ArrowTargets*.cmake
     %{_libdir}/cmake/Arrow/arrow-config.cmake
%{_libdir}/libarrow.so
%{_libdir}/pkgconfig/arrow-compute.pc
%{_libdir}/pkgconfig/arrow-csv.pc
%{_libdir}/pkgconfig/arrow-filesystem.pc
%{_libdir}/pkgconfig/arrow-json.pc
%{_libdir}/pkgconfig/arrow.pc
%{_datadir}/arrow/gdb/gdb_arrow.py
#%{_datadir}/gdb/auto-load/usr/lib64/libarrow.so.*-gdb.py


%files -n parquet-libs
%{_libdir}/libparquet.so.*

%files -n parquet-libs-devel
%dir %{_includedir}/parquet/
     %{_includedir}/parquet/*
%{_libdir}/cmake/Parquet/*.cmake
%{_libdir}/libparquet.so
%{_libdir}/pkgconfig/parquet*.pc
 
%changelog
* Mon May 20 2024 Henry Beberman <henry.beberman@microsoft.com> - 15.0.0-5
- Move to using source tarball from GitHub releases.

* Fri Mar 22 2024 Himaja Kesari <himajakesari@microsoft.com> - 15.0.0-4
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- License verified.

* Sat Feb 24 2024 Paul Wouters <paul.wouters@aiven.io> - 15.0.0-3
- Rebuilt for libre2.so.11 bump
 
* Sun Feb 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 15.0.0-2
- Rebuilt for abseil-cpp-20240116.0
 
* Thu Jan 25 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 15.0.0-1
- Arrow 15.0.0 GA
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Tue Dec 19 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 14.0.2-1
- Arrow 14.0.2 GA
 
* Wed Nov 15 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 14.0.1-2
- Arrow 14.0.1, rebuild for f40-build-side-76708, liborc
 
* Thu Nov 9 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 14.0.1-1
- Arrow 14.0.1 GA, rhbz#2248695
 
* Wed Nov 1 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 14.0.0-2
- Rebuild for ceph for gtest 1.14.0
 
* Wed Nov 1 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 14.0.0-1
- Arrow 14.0.0 GA, rhbz#2244967, and w/ Cython3 again
 
* Tue Aug 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 13.0.0-3
- Rebuilt for abseil-cpp-20230802.0
 
* Thu Aug 24 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 13.0.0-2
- Arrow 13.0.0, source from https://archive.apache.org/dist/arrow/
 
* Tue Aug 1 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 13.0.0-1
- Arrow 13.0.0 GA, rhbz#2224127
- and back to cython 0.29.31
 
* Tue Jul 25 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 12.0.1-6
- rebuild with Cython 3
 
* Mon Jul 24 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 12.0.1-5
- for some reason the rebuild did not use Cython 3, despite the lack of a
  BR selecting 0.29 or 3.0. Which was fortuitous because it fails to build
  with Cython 3. (see https://github.com/apache/arrow/issues/36857).
  Explicitly pinning cython to 0.29 temporarily while awaiting a fix.
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Sun Jun 18 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 12.0.1-3
- Rebuilt for Python 3.12 and thrift-0.15.0
 
* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 12.0.1-2
- Rebuilt for Python 3.12
 
* Wed Jun 14 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 12.0.1-1
- Arrow 12.0.1 GA
 
* Mon May 1 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 12.0.0-1
- Arrow 12.0.0 GA
 
* Wed Mar 22 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 11.0.0-2
- Arrow 11.0.0, rebuild with abseil-cpp 20230125.1
 
* Thu Feb 9 2023  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 11.0.0-1
- Arrow 11.0.0 GA
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Mon Dec 5 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 10.0.1-2
- Arrow 10.0.1, rebuild with xsimd-10, liborc-1.8.1
 
* Thu Dec 1 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 10.0.1-1
- Arrow 10.0.1 GA
 
* Fri Nov 11 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com>
- SPDX migration
 
* Wed Sep 7 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 9.0.0-7
- Arrow 9.0.0, rebuild with xsimd 9.0.1
 
* Sun Sep 4 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 9.0.0-6
- Arrow 9.0.0, rebuild with liborc 1.8.0
 
* Mon Aug 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 9.0.0-5
- Update pyarrow test patch (PR#13904)
 
* Mon Aug 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 9.0.0-4
- Rebuilt for grpc 1.48.0
 
* Wed Aug 17 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 9.0.0-3
- Use %%pyproject_save_files to fix pyarrow metadata
- Use generated BR’s for pyarrow
- Add import-only “smoke tests” for pyarrow
- Stop requiring SSE4.2 on x86-family platforms
- Correct ARROW_WITH_XSIMD; should be ARROW_USE_XSIMD
- Enable more optional functionality in pyarrow
- Fix pyarrow tests installed despite PYARROW_INSTALL_TESTS=0
 
* Wed Aug 10 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 9.0.0-2
- Arrow 9.0.0, enable python, i.e. python3-pyarrow, subpackage
 
* Wed Aug 3 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 9.0.0-1
- Arrow 9.0.0 GA
 
* Thu Jul 21 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 8.0.1-1
- Arrow 8.0.1 GA
 
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Wed May 18 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 8.0.0-3
- rebuild with xsimd-8.1.0
 
* Mon May 16 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 8.0.0-2
- rebuild with grpc-1.46.1
 
* Sun May 8 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 8.0.0-1
- Arrow 8.0.0 GA
 
* Thu Jan 13 2022  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 7.0.0-1
- New upstream release.