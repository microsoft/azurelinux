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
 
Name:		libarrow
Version:	15.0.0
Release:	1%{?dist}
Summary:	A toolbox for accelerated data interchange and in-memory processing
License:	Apache-2.0
URL:		https://arrow.apache.org/
Requires:	%{name}-doc = %{version}-%{release}
Source0:	https://dist.apache.org/repos/dist/release/arrow/arrow-%{version}/apache-arrow-%{version}.tar.gz
Patch0001:	0001-python-pyproject.toml.patch
 
# Apache ORC (liborc) has numerous compile errors and apparently assumes
# a 64-bit build and runtime environment. This is only consumer of the liborc
# package, and in turn the only consumer of this and liborc is Ceph, which
# is also 64-bit only
%{!?python3_pkgversion: %global python3_pkgversion 3}
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
%autosetup -p1 -n apache-arrow-%{version}
# We do not need to (nor can we) build for an old version of numpy:
sed -r -i 's/(oldest-supported-)(numpy)/\2/' python/pyproject.toml
 

 
%build
pushd cpp
%cmake \
  -DARROW_FLIGHT:BOOL=ON \
  -DARROW_ORC=ON \
  -DARROW_PARQUET:BOOL=ON \
  -DARROW_PYTHON:BOOL=ON \
  -DARROW_JEMALLOC:BOOL=OFF \
  -DARROW_SIMD_LEVEL:STRING='NONE' \
  -DARROW_WITH_BROTLI:BOOL=ON \
  -DARROW_WITH_BZ2:BOOL=ON \
  -DARROW_WITH_LZ4:BOOL=ON \
  -DARROW_WITH_SNAPPY:BOOL=ON \
  -DARROW_WITH_GRPC=OFF \
  -DARROW_WITH_ZLIB:BOOL=ON \
  -DARROW_WITH_ZSTD:BOOL=ON \
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
%{_libdir}/pkgconfig/arrow-orc.pc
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
 
