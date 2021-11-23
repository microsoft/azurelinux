Summary:        Open source remote procedure call (RPC) framework
Name:           grpc
Version:        1.41.1
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.grpc.io
Source0:        https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz
# A buildable grpc environment needs functioning submodules that do not work from the archive download
# To recreate the tar.gz run the following:
#  git clone -b RELEASE_TAG_HERE --depth 1 https://github.com/grpc/grpc
#  pushd grpc
#  git submodule update --depth 1 --init
#  popd
#  mv grpc grpc-%%{version}
#  tar  --sort=name \
#       --mtime="2021-04-26 00:00Z" \
#       --owner=0 --group=0 --numeric-owner \
#       --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#       -cf grpc-%%{version}.tar.gz grpc-%%{version}/
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
BuildRequires:  abseil-cpp-devel
BuildRequires:  c-ares-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  openssl-devel
BuildRequires:  protobuf-devel
BuildRequires:  re2-devel
BuildRequires:  zlib-devel

Requires:       abseil-cpp
Requires:       c-ares
Requires:       openssl
Requires:       protobuf
Requires:       zlib

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

%prep
%autosetup
# fix issue compiling absl with gcc11
sed -i 's/std::max(SIGSTKSZ/std::max<size_t>(SIGSTKSZ/g' third_party/abseil-cpp/absl/debugging/failure_signal_handler.cc

%build
mkdir -p cmake/build
cd cmake/build
cmake ../.. -DgRPC_INSTALL=ON                \
   -DBUILD_SHARED_LIBS=ON                    \
   -DCMAKE_BUILD_TYPE=Release                \
   -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}    \
   -DgRPC_ABSL_PROVIDER:STRING='package'    \
   -DgRPC_CARES_PROVIDER:STRING='package'    \
   -DgRPC_PROTOBUF_PROVIDER:STRING='package' \
   -DgRPC_RE2_PROVIDER:STRING='package'      \
   -DgRPC_SSL_PROVIDER:STRING='package'      \
   -DgRPC_ZLIB_PROVIDER:STRING='package'
%make_build

%install
cd cmake/build
%make_install
find %{buildroot} -name '*.cmake' -delete

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

%files plugins
%license LICENSE
%{_bindir}/grpc_*_plugin

%changelog
* Mon Nov 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.41.1-2
- Use pre-installed "re2" and "abseil-cpp" instead of building them.

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
