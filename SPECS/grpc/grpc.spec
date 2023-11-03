Summary:        Open source remote procedure call (RPC) framework
Name:           grpc
Version:        1.42.0
Release:        7%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.grpc.io
Source0:        https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-submodules.tar.gz
BuildRequires:  abseil-cpp-devel
BuildRequires:  c-ares-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  protobuf-devel
BuildRequires:  re2-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(openssl)
BuildRequires:  ninja-build
Requires:       abseil-cpp
Requires:       c-ares
Requires:       openssl
Requires:       protobuf
Requires:       zlib

# Python
BuildRequires:      build-essential
BuildRequires:      python3-devel
BuildRequires:      python3-Cython
BuildRequires:      python3-six
BuildRequires:      python3-wheel
BuildRequires:      python3-setuptools
BuildRequires:      python3-protobuf


%description
gRPC is a modern, open source, high-performance remote procedure call (RPC) framework that can run anywhere. It enables client and server applications to communicate transparently, and simplifies the building of connected systems.

%package devel
Summary:        Development files for grpc
Requires:       %{name} = %{version}-%{release}
Requires:       protobuf-devel

%description devel
The grpc-devel package contains the header files and libraries
needed to develop programs that use grpc.

%package plugins
Summary:        Plugins files for grpc
Requires:       %{name} = %{version}-%{release}
Requires:       protobuf


%description plugins
The grpc-plugins package contains the grpc plugins.

%package -n python3-grpcio
Summary:        Python language bindings for gRPC
Requires:       %{name} = %{version}-%{release}
Requires:       python3-six
%{?python_provide:%python_provide python3-grpcio}

%description -n python3-grpcio
Python language bindings for gRPC.


%prep
%setup -q -n %{name}-%{version}
%setup -T -D -a 1

%build
# Updating used C++ version to be compatible with the build dependencies.
# Without this fix 'grpc' compiles with C++11 against 'abseil-cpp' headers,
# which generate a different set of APIs than the ones provided by the BR 'abseil-cpp'.
CXX_VERSION=$(c++ -dM -E -x c++ /dev/null | grep -oP "(?<=__cplusplus \d{2})\d{2}")

mkdir -p cmake/build
pushd cmake/build
%cmake ../.. -GNinja                         \
   -DgRPC_INSTALL=ON                         \
   -DBUILD_SHARED_LIBS=ON                    \
   -DCMAKE_BUILD_TYPE=Release                \
   -DCMAKE_CXX_STANDARD=$CXX_VERSION         \
   -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}    \
   -DgRPC_ABSL_PROVIDER:STRING='package'     \
   -DgRPC_CARES_PROVIDER:STRING='package'    \
   -DgRPC_PROTOBUF_PROVIDER:STRING='package' \
   -DgRPC_RE2_PROVIDER:STRING='package'      \
   -DgRPC_SSL_PROVIDER:STRING='package'      \
   -DgRPC_ZLIB_PROVIDER:STRING='package'
%cmake_build 
popd
#uncommenting below line causes the whole build to get stuck in aarch64 machine 
#py3_build

%install
pushd cmake/build
%cmake_install
popd

#python
export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export GRPC_PYTHON_BUILD_SYSTEM_RE2=True
export GRPC_PYTHON_BUILD_SYSTEM_ABSL=True
#uncommenting below line causes the whole build to get stuck in aarch64 machine 
#py3_install
#using macros causes build to get stuck forever
%{__python3} setup.py install -O1 --root %{buildroot}

%files
%license LICENSE
%{_libdir}/*.so.*
%{_datadir}/grpc/roots.pem

%files devel
%{_includedir}/grpc
%{_includedir}/grpc++
%{_includedir}/grpcpp
%{_libdir}/libaddress_sorting.so
%{_libdir}/libgpr.so
%{_libdir}/libgrpc++.so
%{_libdir}/libgrpc++_alts.so
%{_libdir}/libgrpc++_error_details.so
%{_libdir}/libgrpc++_reflection.so
%{_libdir}/libgrpc++_unsecure.so
%{_libdir}/libgrpc.so
%{_libdir}/libgrpc_plugin_support.so
%{_libdir}/libgrpc_unsecure.so
%{_libdir}/libgrpcpp_channelz.so
%{_libdir}/libupb.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/*

%files plugins
%license LICENSE
%{_bindir}/grpc_*_plugin


%files -n python3-grpcio
%license LICENSE
%{python3_sitearch}/grpc
%{python3_sitearch}/grpcio-%{version}-py%{python3_version}.egg-info


%changelog
* Thu Oct 19 2023 Dan Streetman <ddstreet@ieee.org> - 1.42.0-7
- Bump release to rebuild with updated version of Go.

* Thu Jun 22 2023 Reuben Olinsky <reubeno@microsoft.com> - 1.42.0-6
- Add cmake modules to grpc-devel package.

* Tue May 31 2023 Dallas Delaney <dadelan@microsoft.com> - 1.42.0-5
- Rebuild against c-ares to Fix CVE-2023-32067, CVE-2023-31130, CVE-2023-31147

* Tue Feb 28 2023 Riken Maharjan <rmaharjan@microsoft.com> - 1.42.0-4
- Add grpcio for aarch64.

* Wed Nov 09 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.42.0-3
- Add 'python3-grpcio' subpackage using Fedora 37 spec for guidance.

* Thu Jun 30 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.42.0-2
- Bumping release to rebuild with latest 'abseil-cpp'.

* Mon Nov 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.42.0-1
- Updated to version 1.42.0.
- Overwritten hard-coded compilation with C++11 to use CBL-Mariner defaults.
- Using pre-installed "re2" and "abseil-cpp" instead of building them.

* Fri Nov 12 2021 Andrew Phelps <anphel@microsoft.com> - 1.41.1-1
- Update to version 1.41.1

* Wed Nov 03 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 1.35.0-6
- Bringing back the "libaddress_sorting" library.

* Tue Sep 28 2021 Andrew Phelps <anphel@microsoft.com> - 1.35.0-5
- Explicitly provide grpc-devel files to avoid packaging conflicts with re2-devel.

* Mon Jun 21 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.35.0-4
- Switch to system package for protobuf dependency.

* Wed Apr 28 2021 Nick Samson <nick.samson@microsoft.com> - 1.35.0-3
- Switch to system package for c-ares dependency.

* Fri Mar 26 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 1.35.0-2
- Switch to system provided packages for zlib and openssl.

* Mon Mar 08 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 1.35.0-1
- Original version for CBL-Mariner. License Verified.
