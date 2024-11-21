Summary:        The OpenTelemetry C++ Client
Name:           opentelemetry-cpp
Version:        1.14.2
Release:       	1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/open-telemetry/opentelemetry-cpp
Source0:        https://github.com/open-telemetry/opentelemetry-cpp/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Standard proto files source: https://github.com/open-telemetry/opentelemetry-proto
Source1:        opentelemetry-proto-1.1.0.tar.gz
BuildRequires:  c-ares-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  gmock-devel
BuildRequires:  grpc-devel
BuildRequires:  grpc-plugins
BuildRequires:  gtest-devel
BuildRequires:  abseil-cpp-devel
BuildRequires:  nlohmann-json-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-static
BuildRequires:  protobuf-c-devel
BuildRequires:  re2-devel
BuildRequires:	systemd-devel
Requires:       abseil-cpp

%description
The official OpenTelemetry CPP client

%package devel
Summary:        Development Libraries for OpenTelemetry CPP client
Group:          Development/Libraries
Requires:       opentelemetry-cpp = %{version}-%{release}

%description devel
Development Libraries for OpenTelemetry CPP client

%prep
%autosetup -p1
mkdir -p third_party/opentelemetry-proto
tar xf %{SOURCE1} -C third_party/opentelemetry-proto --strip-components=1

%build
mkdir build && cd build
%cmake \
	-DCMAKE_POSITION_INDEPENDENT_CODE=ON \
	-DOPENTELEMETRY_INSTALL=ON \
	-DWITH_BENCHMARK=OFF \
	-DWITH_NO_DEPRECATED_CODE=ON \
	-DWITH_OTLP_GRPC=ON \
	-DWITH_OTLP_HTTP=ON \
	-DWITH_ABSEIL=ON \
	-DWITH_STL=ON \
	-DWITH_ZPAGES=ON \
	-DOTELCPP_PROTO_PATH=../third_party/opentelemetry-proto \
	..

%make_build

%install
%make_install -C build

%check
%make_build -C build test

%files
%license LICENSE
%{_libdir}/libopentelemetry_*.so

%files devel
%{_libdir}/pkgconfig/opentelemetry_*.pc
%{_includedir}/opentelemetry/*
%{_libdir}/cmake/opentelemetry-cpp/*

%changelog
* Mon Mar 18 2024 Betty Lakes <bettylakes@microsoft.com> - 1.14.2-1
- Upgrade to 1.14.2
- Upgrade opentelemetry-proto to 1.1.0

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.10.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jul 17 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.10.0-1
- Original version for CBL-Mariner
- License Verified
