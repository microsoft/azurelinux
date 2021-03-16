Summary:        Open source remote procedure call (RPC) framework 
Name:           grpc
Version:        1.35.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
#Source0:        https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
URL:            https://www.grpc.io

# A buildable grpc environment needs functioning submodules that do not work from the archive download
# To recreate the tar.gz run the following
#  git clone -b RELEASE_TAG_HERE https://github.com/grpc/grpc
#  pushd grpc
#  git submodule update --init
#  popd
#  sudo mv grpc grpc-%{version}
#  sudo tar -cvf grpc-%{version}.tar.gz grpc-%{version}/

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  gcc

%description
gRPC is a modern, open source, high-performance remote procedure call (RPC) framework that can run anywhere. It enables client and server applications to communicate transparently, and simplifies the building of connected systems.

%package devel
Summary:        Development files for grpc
Requires:       %{name} = %{version}-%{release}

%description devel
The grpc-devel package contains the header files and libraries
needed to develop programs that use grpc.

%package plugins
Summary:        Plugins files for grpc
Requires:       %{name} = %{version}-%{release}
Requires:       protobuf-compiler

%description plugins
The grpc-plugins package contains the grpc plugins.

%prep
%autosetup

%build
mkdir -p cmake/build
cd cmake/build
cmake ../.. -DgRPC_INSTALL=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}
%make_build

%install
cd cmake/build
%make_install
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name '*.cmake' -delete

%files
%license LICENSE
%{_libdir}/*.so.*
%{_lib64dir}/*.so.*
%{_mandir}/man3/*.3*
%{_datadir}/grpc/roots.pem
%exclude %{_datadir}/pkgconfig/zlib.pc

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_lib64dir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_lib64dir}/pkgconfig/*.pc

%files plugins
%license LICENSE
%{_bindir}/grpc_*_plugin
%exclude %{_bindir}/acountry
%exclude %{_bindir}/ahost
%exclude %{_bindir}/adig
%exclude %{_bindir}/protoc*

%changelog
* Mon Mar 08 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 1.35.0-1
- Original version for CBL-Mariner. License Verified
