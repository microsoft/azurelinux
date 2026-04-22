# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*- sh-shell: rpm -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

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
Version:	20.0.0
Release: 11%{?dist}
Summary:	A toolbox for accelerated data interchange and in-memory processing
License:	Apache-2.0
URL:		https://arrow.apache.org/
Requires:	%{name}-doc = %{version}-%{release}
Source0:	https://downloads.apache.org/arrow/arrow-%{version}/apache-arrow-%{version}.tar.gz
Patch0001:	0001-python-pyarrow-tests-read_record_patch.py.patch
Patch0002:	0002-python-pyarrow-tests-test_ipc.py.patch

# Apache ORC (liborc) has numerous compile errors and apparently assumes
# a 64-bit build and runtime environment. This is only consumer of the liborc
# package, and in turn the only consumers of this and liborc are Ceph, which
# is also 64-bit only, and rdal.
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
BuildRequires:	glog-devel
BuildRequires:	grpc-devel
BuildRequires:	grpc-plugins
BuildRequires:	libzstd-devel
BuildRequires:	lz4-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-numpy
BuildRequires:	python%{python3_pkgversion}-Cython
BuildRequires:	python%{python3_pkgversion}-pandas
BuildRequires:	python%{python3_pkgversion}-pytest
BuildRequires:	python%{python3_pkgversion}-hypothesis
BuildRequires:	python%{python3_pkgversion}-pytzdata
BuildRequires:	xsimd-devel
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
BuildRequires:	liborc-devel
%if %{with use_gandiva}
BuildRequires:	llvm-devel
BuildRequires:	ncurses-devel
%endif
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc

# Additional pyarrow build requirements; see also %%generate_buildrequires
BuildRequires:  python3dist(cffi)

# python3-pyarrow provides bogus library SONAME provides
# https://bugzilla.redhat.com/show_bug.cgi?id=2326774
%global __provides_exclude (^libarrow_python(_[^.]+)?|.cpython-.*)\\.so.*$
%global __requires_exclude ^libarrow_python(_[^.]+)?\\.so.*$

%description
Apache Arrow defines a language-independent columnar memory
format for flat and hierarchical data, organized for efficient
analytic operations on modern hardware like CPUs and GPUs. The
Arrow memory format also supports zero-copy reads for lightning-
fast data access without serialization overhead

%files
%{_libdir}/libarrow.so.*
%exclude %{python3_sitearch}/benchmarks/*
%exclude %{python3_sitearch}/cmake_modules/*
%exclude %{python3_sitearch}/examples/*
%exclude %{python3_sitearch}/scripts/*

#--------------------------------------------------------------------

%package doc
Summary:	Documentation files for Apache Arrow C++
BuildArch:	noarch

%description doc
Documentation files for Apache Arrow C++.

Obsoletes:	%{name}-glib-doc < %{version}-%{release}
Obsoletes:	%{name}-dataset-glib-doc < %{version}-%{release}
Obsoletes:	%{name}-parquet-glib-doc < %{version}-%{release}
Obsoletes:	plasma-glib-doc < %{version}-%{release}
Obsoletes:	gandiva-glib-doc < %{version}-%{release}

%files doc
%license LICENSE.txt
%doc README.md NOTICE.txt
%exclude %{_docdir}/arrow/

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
%exclude %{_libdir}/cmake/Arrow/FindorcAlt.cmake
%exclude %{_libdir}/cmake/Arrow/FindSnappyAlt.cmake
%exclude %{_libdir}/cmake/Arrow/Findre2Alt.cmake
%exclude %{_libdir}/cmake/Arrow/Findutf8proc.cmake
%exclude %{_libdir}/cmake/Arrow/FindzstdAlt.cmake
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
%{_datadir}/gdb/auto-load%{_libdir}/libarrow.so.*-gdb.py

#--------------------------------------------------------------------

%package dataset-libs
Summary:	C++ library to read and write semantic datasets
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description dataset-libs
This package contains the libraries for Apache Arrow dataset.

%files dataset-libs
%{_libdir}/libarrow_dataset.so.*

#--------------------------------------------------------------------

%package dataset-devel
Summary:	Libraries and header files for Apache Arrow dataset
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-libs%{?_isa} = %{version}-%{release}

%description dataset-devel
Libraries and header files for Apache Arrow dataset.

%files dataset-devel
%dir %{_includedir}/arrow/dataset/
     %{_includedir}/arrow/dataset/*
%{_libdir}/cmake/ArrowDataset/*.cmake
%{_libdir}/libarrow_dataset.so
%{_libdir}/pkgconfig/arrow-dataset.pc

#--------------------------------------------------------------------

%package acero-libs
Summary:	C++ library for fast data transport
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description acero-libs
This package contains the libraries for Apache Arrow Acero.

%files acero-libs
%{_libdir}/libarrow_acero.so.*

#--------------------------------------------------------------------

%package acero-devel
Summary:	Libraries for Apache Arrow Acero
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-flight-libs%{?_isa} = %{version}-%{release}

%description acero-devel
Libraries and header files for Apache Arrow Acero.

%files acero-devel
%{_libdir}/cmake/ArrowAcero/*.cmake
%{_libdir}/libarrow_acero.so
%{_libdir}/pkgconfig/arrow-acero.pc

#--------------------------------------------------------------------

%if %{with use_flight}
%package flight-libs
Summary:	C++ library for fast data transport
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description flight-libs
This package contains the libraries for Apache Arrow Flight.

%files flight-libs
%{_libdir}/libarrow_flight.so.*
%{_libdir}/libarrow-flight-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/ArrowFlight-1.0.typelib

#--------------------------------------------------------------------

%package flight-devel
Summary:	Libraries and header files for Apache Arrow Flight
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-flight-libs%{?_isa} = %{version}-%{release}

%description flight-devel
Libraries and header files for Apache Arrow Flight.

%files flight-devel
%dir %{_includedir}/arrow/flight/
     %{_includedir}/arrow/flight/*
%dir %{_includedir}/arrow-flight-glib/
     %{_includedir}/arrow-flight-glib/*
%{_libdir}/cmake/ArrowFlight/*.cmake
%{_libdir}/libarrow_flight.so
%{_libdir}/libarrow-flight-glib.so
%{_libdir}/pkgconfig/arrow-flight.pc
%{_libdir}/pkgconfig/arrow-flight-glib.pc
%endif

#--------------------------------------------------------------------

%if %{with use_gandiva}
%package -n gandiva-libs
Summary:	C++ library for compiling and evaluating expressions
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}
Requires:	ncurses-libs

%description -n gandiva-libs
This package contains the libraries for Gandiva.

%files -n gandiva-libs
%{_libdir}/libgandiva.so.*

#--------------------------------------------------------------------

%package -n gandiva-devel
Summary:	Libraries and header files for Gandiva
Requires:	gandiva-libs%{?_isa} = %{version}-%{release}
Requires:	llvm-devel

%description -n gandiva-devel
Libraries and header files for Gandiva.

%files -n gandiva-devel
%dir %{_includedir}/gandiva/
     %{_includedir}/gandiva/
%{_libdir}/cmake/Gandiva/*.cmake
%{_libdir}/libgandiva.so
%{_libdir}/pkgconfig/gandiva.pc
%endif

#--------------------------------------------------------------------

%package python-libs
Summary:	Python integration library for Apache Arrow
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python%{python3_pkgversion}-numpy

%description python-libs
This package contains the Python integration library for Apache Arrow.

%files python-libs
%{python3_sitearch}/pyarrow/libarrow_python.so

#--------------------------------------------------------------------

%package python-devel
Summary:	Libraries and header files for Python integration library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-libs%{?_isa} = %{version}-%{release}
Requires:	python%{python3_pkgversion}-devel

%description python-devel
Libraries and header files for Python integration library for Apache Arrow.

%files python-devel
%dir %{python3_sitearch}/pyarrow/include/arrow/python
     %{python3_sitearch}/pyarrow/include/arrow/python/*
%exclude %{python3_sitearch}/pyarrow/include/arrow/python/flight.h

#--------------------------------------------------------------------

%if %{with use_flight}
%package python-flight-libs
Summary:	Python integration library for Apache Arrow Flight
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-flight-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description python-flight-libs
This package contains the Python integration library for Apache Arrow Flight.

%files python-flight-libs
%{python3_sitearch}/pyarrow/libarrow_python_flight.so

#--------------------------------------------------------------------

%package python-flight-devel
Summary:	Libraries and header files for Python integration
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-flight-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-python-flight-libs%{?_isa} = %{version}-%{release}

%description python-flight-devel
Libraries and header files for Python integration library for
Apache Arrow Flight.

%files python-flight-devel
%{python3_sitearch}/pyarrow/include/arrow/python/flight.h
%endif

%if %{with use_plasma}
#--------------------------------------------------------------------

%package -n plasma-libs
Summary:	Runtime libraries for Plasma in-memory object store
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n plasma-libs
This package contains the libraries for Plasma in-memory object store.

%files -n plasma-libs
%{_libdir}/libplasma.so.*

#--------------------------------------------------------------------

%package -n plasma-store-server
Summary:	Server for Plasma in-memory object store
Requires:	plasma-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n plasma-store-server
This package contains the server for Plasma in-memory object store.

%files -n plasma-store-server
%{_bindir}/plasma-store-server

#--------------------------------------------------------------------

%package -n plasma-libs-devel
Summary:	Libraries and header files for Plasma in-memory object store
Requires:	plasma-libs%{?_isa} = %{version}-%{release}
# plasma-devel a.k.a. kdelibs-devel provides
# conflicts with all versions of plasma-devel %%{_libdir}/libplasma.so
BuildConflicts: plasma-devel
# conflicts with all versions of plasma-workspace-devel %%{_includedir}/*
BuildConflicts: plasma-workspace-devel

%description -n plasma-libs-devel
Libraries and header files for Plasma in-memory object store.

%files -n plasma-libs-devel
%dir %{_includedir}/plasma/
     %{_includedir}/plasma/*
%{_libdir}/cmake/Arrow/Plasma*.cmake
%{_libdir}/libplasma.so
%{_libdir}/pkgconfig/plasma*.pc

%endif
#--------------------------------------------------------------------

%package -n parquet-libs
Summary:	Runtime libraries for Apache Parquet C++
Requires:	boost-program-options
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n parquet-libs
This package contains the libraries for Apache Parquet C++.

%files -n parquet-libs
%{_libdir}/libparquet.so.*

#--------------------------------------------------------------------

%package -n parquet-libs-devel
Summary:	Libraries and header files for Apache Parquet C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	parquet-libs%{?_isa} = %{version}-%{release}
Requires:	zlib-devel

%description -n parquet-libs-devel
Libraries and header files for Apache Parquet C++.

%files -n parquet-libs-devel
%dir %{_includedir}/parquet/
     %{_includedir}/parquet/*
%{_libdir}/cmake/Parquet/*.cmake
%{_libdir}/libparquet.so
%{_libdir}/pkgconfig/parquet*.pc

#--------------------------------------------------------------------

%package glib-libs
Summary:	Runtime libraries for Apache Arrow GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description glib-libs
This package contains the libraries for Apache Arrow GLib.

%files glib-libs
%{_libdir}/libarrow-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Arrow-1.0.typelib

#--------------------------------------------------------------------

%package glib-devel
Summary:	Libraries and header files for Apache Arrow GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
Requires:	gobject-introspection-devel

%description glib-devel
Libraries and header files for Apache Arrow GLib.

%files glib-devel
%dir %{_includedir}/arrow-glib/
     %{_includedir}/arrow-glib/*
%{_libdir}/libarrow-glib.so
%{_libdir}/pkgconfig/arrow-glib.pc
%{_libdir}/pkgconfig/arrow-orc-glib.pc
%dir %{_datadir}/arrow-glib/
     %{_datadir}/arrow-glib/*
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Arrow-1.0.gir
     %{_datadir}/gir-1.0/ArrowFlight-1.0.gir

#--------------------------------------------------------------------

%package dataset-glib-libs
Summary:	Runtime libraries for Apache Arrow dataset GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description dataset-glib-libs
This package contains the libraries for Apache Arrow dataset GLib.

%files dataset-glib-libs
%{_libdir}/libarrow-dataset-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/ArrowDataset-1.0.typelib

#--------------------------------------------------------------------

%package dataset-glib-devel
Summary:	Libraries and header files for Apache Arrow dataset GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-dataset-glib-libs%{?_isa} = %{version}-%{release}

%description dataset-glib-devel
Libraries and header files for Apache Arrow dataset GLib.

%files dataset-glib-devel
%dir %{_includedir}/arrow-dataset-glib/
     %{_includedir}/arrow-dataset-glib/*
%{_libdir}/libarrow-dataset-glib.so
%{_libdir}/pkgconfig/arrow-dataset-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/ArrowDataset-1.0.gir

#--------------------------------------------------------------------

%if %{with use_gandiva}
%package -n gandiva-glib-libs
Summary:	Runtime libraries for Gandiva GLib
Requires:	gandiva-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n gandiva-glib-libs
This package contains the libraries for Gandiva GLib.

%files -n gandiva-glib-libs
%{_libdir}/libgandiva-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Gandiva-1.0.typelib

#--------------------------------------------------------------------

%package -n gandiva-glib-devel
Summary:	Libraries and header files for Gandiva GLib
Requires:	gandiva-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}

%description -n gandiva-glib-devel
Libraries and header files for Gandiva GLib.

%files -n gandiva-glib-devel
%dir %{_includedir}/gandiva-glib/
     %{_includedir}/gandiva-glib/*
%{_libdir}/libgandiva-glib.so
%{_libdir}/pkgconfig/gandiva-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Gandiva-1.0.gir
%endif

%if %{with use_plasma}
#--------------------------------------------------------------------

%package -n plasma-glib-libs
Summary:	Runtime libraries for Plasma GLib
Requires:	plasma-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n plasma-glib-libs
This package contains the libraries for Plasma GLib.

%files -n plasma-glib-libs
%{_libdir}/libplasma-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Plasma-1.0.typelib

#--------------------------------------------------------------------

%package -n plasma-glib-devel
Summary:	Libraries and header files for Plasma GLib
Requires:	plasma-devel%{?_isa} = %{version}-%{release}
Requires:	plasma-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}

%description -n plasma-glib-devel
Libraries and header files for Plasma GLib.

%files -n plasma-glib-devel
%dir %{_includedir}/plasma-glib/
     %{_includedir}/plasma-glib/*
%{_libdir}/libplasma-glib.so
%{_libdir}/pkgconfig/plasma-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Plasma-1.0.gir
%endif

#--------------------------------------------------------------------

%package -n parquet-glib-libs
Summary:	Runtime libraries for Apache Parquet GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	parquet-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-doc = %{version}-%{release}

%description -n parquet-glib-libs
This package contains the libraries for Apache Parquet GLib.

%files -n parquet-glib-libs
%{_libdir}/libparquet-glib.so.*
%dir %{_libdir}/girepository-1.0/
     %{_libdir}/girepository-1.0/Parquet-1.0.typelib

#--------------------------------------------------------------------

%package -n parquet-glib-devel
Summary:	Libraries and header files for Apache Parquet GLib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	parquet-libs-devel%{?_isa} = %{version}-%{release}
Requires:	parquet-glib-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib-devel%{?_isa} = %{version}-%{release}

%description -n parquet-glib-devel
Libraries and header files for Apache Parquet GLib.

%files -n parquet-glib-devel
%dir %{_includedir}/parquet-glib/
     %{_includedir}/parquet-glib/*
%{_libdir}/libparquet-glib.so
%{_libdir}/pkgconfig/parquet-glib.pc
%dir %{_datadir}/gir-1.0/
     %{_datadir}/gir-1.0/Parquet-1.0.gir

#--------------------------------------------------------------------

%package -n python3-pyarrow
Summary: Python library for Apache Arrow

%description -n python3-pyarrow
Python library for Apache Arrow

%files -n python3-pyarrow -f %{pyproject_files}
%exclude %{python3_sitearch}/pyarrow/lib_api.h
%exclude %{python3_sitearch}/pyarrow/include

#--------------------------------------------------------------------

%package -n python3-pyarrow-devel
Summary: Development files for python3-pyarrow

Requires:       python3-pyarrow%{?_isa} = %{version}-%{release}

%description -n python3-pyarrow-devel
Development files for python3-pyarrow

%files -n python3-pyarrow-devel
%{python3_sitearch}/pyarrow/lib_api.h
%{python3_sitearch}/pyarrow/include

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n apache-arrow-%{version}
# We do not need to (nor can we) build for an old version of numpy:
sed -r -i 's/(oldest-supported-)(numpy)/\2/' python/pyproject.toml

%generate_buildrequires
pushd python >/dev/null
export SETUPTOOLS_SCM_VERSION_WRITE_TO_PREFIX="python"
%pyproject_buildrequires
popd >/dev/null

%build
pushd cpp
%cmake \
%if %{with use_flight}
  -DARROW_FLIGHT:BOOL=ON \
%endif
%if %{with use_gandiva}
  -DARROW_GANDIVA:BOOL=ON \
%endif
%if %{with use_mimalloc}
  -DARROW_MIMALLOC:BOOL=ON \
%else
  -DARROW_MIMALLOC:BOOL=OFF \
%endif
  -DARROW_ORC=ON \
  -DARROW_PARQUET:BOOL=ON \
%if %{with use_plasma}
  -DARROW_PLASMA:BOOL=ON \
%endif
  -DARROW_PYTHON:BOOL=ON \
  -DARROW_JEMALLOC:BOOL=OFF \
  -DARROW_SIMD_LEVEL:STRING='NONE' \
  -DGRPC_SOURCE="SYSTEM" \
  -Dxsimd_SOURCE="SYSTEM" \
%if %{with use_s3}
  -DARROW_S3:BOOL=ON \
%endif
  -DARROW_WITH_BROTLI:BOOL=ON \
  -DARROW_WITH_BZ2:BOOL=ON \
  -DARROW_WITH_LZ4:BOOL=ON \
  -DARROW_WITH_SNAPPY:BOOL=ON \
  -DARROW_WITH_ZLIB:BOOL=ON \
  -DARROW_WITH_ZSTD:BOOL=ON \
  -DARROW_USE_XSIMD:BOOL=ON \
  -DARROW_BUILD_STATIC:BOOL=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_COLOR_MAKEFILE:BOOL=OFF \
  -DARROW_USE_CCACHE:BOOL=OFF \
  -DCMAKE_UNITY_BUILD:BOOL=ON \
  -DPARQUET_REQUIRE_ENCRYPTION:BOOL=ON \
  -DPythonInterp_FIND_VERSION:BOOL=ON \
  -DPythonInterp_FIND_VERSION_MAJOR=3 \
%if %{with use_ninja}
  -GNinja
%endif

export VERBOSE=1
export GCC_COLORS=
%cmake_build
popd

pushd c_glib
%meson \
  -Darrow_cpp_build_dir=../cpp/%{_vpath_builddir} \
  -Darrow_cpp_build_type=relwithdebinfo \
  -Dgtk_doc=true
%meson_build
popd

# hack alert. install libarrow somewhere (temporary) so that python
# (i.e. pyarrow) can build against it. If someone knows how to invoke
# cmake or # pyproject_wheel using the bits in ../cpp instead, that
# would be preferable to this.
pushd cpp
DESTDIR="/tmp" %__cmake --install "%{__cmake_builddir}"
popd

pushd python
export \
  CMAKE_PREFIX_PATH=/tmp%{_prefix} \
  PYARROW_BUNDLE_ARROW_CPP_HEADERS=1 \
  PYARROW_BUNDLE_PLASMA_EXECUTABLE=0 \
  PYARROW_WITH_DATASET=1 \
  PYARROW_WITH_FLIGHT=1 \
  PYARROW_WITH_PARQUET=1 \
  PYARROW_WITH_PARQUET_ENCRYPTION=1 \
  %{?with_use_plasma:PYARROW_WITH_PLASMA=1} \
  %{?with_use_gandiva:PYARROW_WITH_GANDIVA=1} \
  PYARROW_PARALLEL=%{_smp_build_ncpus} \
  PYARROW_INSTALL_TESTS=0 \
  SETUPTOOLS_SCM_VERSION_WRITE_TO_PREFIX="python"
%pyproject_wheel
popd
rm -rf /tmp%{_prefix}

#--------------------------------------------------------------------

%install

pushd python
export PYARROW_INSTALL_TESTS=0
%pyproject_install
%pyproject_save_files pyarrow
popd

pushd c_glib
%meson_install
popd

pushd cpp
%cmake_install
popd


%check
export LD_LIBRARY_PATH='%{buildroot}%{_libdir}'
# While https://github.com/apache/arrow/pull/13904 partially fixes
# https://issues.apache.org/jira/browse/ARROW-17389, conftest.py is still
# installed. We must skip testing it because it would import pytest.
#
# Additionally, skip subpackages corresponding to missing optional
# functionality.
%{pyproject_check_import \
    -e 'pyarrow.conftest' \
    -e 'pyarrow.orc' -e 'pyarrow._orc' \
    %{?!with_use_plasma:-e 'pyarrow.plasma' -e 'pyarrow._plasma'} \
    -e 'pyarrow.substrait' -e 'pyarrow._substrait' \
    -e 'pyarrow.cuda' \
    -e 'pyarrow.libarrow_python' -e 'pyarrow._libarrow_python' \
    -e 'pyarrow.libarrow_python_flight' -e 'pyarrow._libarrow_python_flight' \
    -e 'pyarrow.libarrow_python_parquet_encryption' \
    -e 'pyarrow.tests.read_record_batch' -e 'pyarrow.tests.test_cuda' \
    -e 'pyarrow.tests.test_cuda_numba_interop' -e 'pyarrow.tests.test_jvm'}

#--------------------------------------------------------------------

%changelog
* Mon Jan 12 2026  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 20.0.0-10
- Arrow 20.0.0, rebuild with ORC (liborc) 2.1.4

* Wed Sep 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20.0.0-9
- Arrow 20.0.0, rebuild with Python 3.14.0rc3, abseil-cpp-20250814.0-1
- rhbz#2396709

* Mon Sep 22 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 20.0.0-8
- Arrow 20.0.0, rebuild with Python, abseil-cpp-202514.1-1
- rhbz#2396709

* Mon Sep 22 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 20.0.0-7
- Arrow 20.0.0, rebuild with Python
- rhbz#2396709

* Wed Sep 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20.0.0-6
- Rebuilt for abseil-cpp 20250814.0

* Mon Aug 18 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 20.0.0-5
- Arrow 20.0.0, rebuild with Python 3.14.0rc2
- rhbz#2389167

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 20.0.0-3
- Arrow 20.0.0, rebuild with ORC (liborc) 2.1.3

* Wed Jul 9 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 20.0.0-2
- Arrow 20.0.0 GA f43-build-side-114791 and Python-3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 19.0.1-6
- Rebuilt for Python 3.14

* Mon May 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 19.0.1-5
- Rebuilt for abseil-cpp 20250512.0

* Thu May 8 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 19.0.1-3
- Arrow 19.0.1, rebuild with liborc-2.1.2-1

* Mon Apr 28 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 20.0.0-1
- Arrow 20.0.0 GA f43-build-side-110906

* Sat Apr 19 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 19.0.1-3
- Arrow 19.0.1, w/ liborc-2.1.1-2 (orc-format-1.1.0) again

* Fri Apr 18 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 19.0.1-2
- Arrow 19.0.1, w/ liborc-2.1.1-2 (orc-format-1.1.0)

* Thu Mar 13 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 19.0.1-1
- Arrow 19.0.1 GA, w/ liborc-2.1.1-1

* Tue Feb 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 19.0.0-2
- Rebuilt for abseil-cpp-20250127.0

* Fri Feb 7 2025  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 19.0.0-1
- Arrow 19.0.0 GA

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Orion Poplawski <orion@nwra.com> - 18.0.0-3
- Rebuild with numpy 2.0

* Fri Nov 22 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 16.0.0-1
- Arrow 18.0.0 GA

* Thu Nov 21 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 16.1.0-12
- Arrow 16.1.0, rebuild with liborc-2.0.3
- revert testing PR

* Sun Nov 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 16.1.0-11
- Filter out bogus Provides/Requires from python3-pyarrow; fixes RHBZ#2326774

* Mon Oct 7 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 16.1.0-10
- Arrow 16.1.0, rebuild with utf8proc 2.9.0

* Thu Oct 3 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 16.1.0-9
- Arrow 16.1.0, rebuild with liborc-2.0.2

* Sun Aug 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 16.1.0-8
- Rebuilt for abseil-cpp-20240722.0

* Thu Aug 15 2024 Marek Kasik <mkasik@redhat.com> - 16.1.0-7
- Rebuild for re2 20240702

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 16.1.0-5
- Arrow 16.1.0, rebuild with liborc-2.0.1 (after liborc1 -> liborc2)

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 16.1.0-4
- Rebuilt for Python 3.13

* Sun Jun 02 2024 Orion Poplawski <orion@nwra.com> - 16.1.0-3
- Rebuild with thrift 0.20

* Thu May 16 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 16.1.0-2
- Remove extraneous openssl dependencies

* Tue May 14 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 16.1.0-1
- Arrow 16.1.0 GA

* Mon Apr 22 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 16.0.0-1
- Arrow 16.0.0 GA
- N.B. See https://github.com/apache/arrow/issues/40604, it appears that
  the ABI break is not (will not be) fixed.

* Mon Mar 25 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 15.0.2-3
- rebuild with liborc-2.0.0-2 (liborc1 -> liborc2)

* Wed Mar 20 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 15.0.2-2
- rhbz#2269811, fix ABI break
- partial revert of https://github.com/apache/arrow/pull/39866

* Tue Mar 19 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 15.0.2-1
- Arrow 15.0.2 GA
- Note: The ABI break reported https://github.com/apache/arrow/issues/40604 
  (bz 2269811) does NOT appear to be addressed in this release.

* Fri Mar 15 2024  Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 15.0.1-1
- Arrow 15.0.1 GA, w/ liborc 2.0.0

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

