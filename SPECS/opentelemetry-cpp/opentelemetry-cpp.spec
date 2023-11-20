Summary:        The OpenTelemetry C++ Client
Name:           opentelemetry-cpp
Version:        1.10.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/open-telemetry/opentelemetry-cpp
Source0:        https://github.com/open-telemetry/opentelemetry-cpp/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Standard proto files source: https://github.com/open-telemetry/opentelemetry-proto
Source1:        opentelemetry-proto-1.0.0.tar.gz
BuildRequires:  c-ares-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  gmock-devel
BuildRequires:  grpc-devel
BuildRequires:  grpc-plugins
BuildRequires:  gtest-devel
BuildRequires:  nlohmann-json-devel
BuildRequires:  protobuf-devel
BuildRequires:  re2-devel

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
%{_libdir}/libopentelemetry_common.so
%{_libdir}/libopentelemetry_exporter_in_memory.so
%{_libdir}/libopentelemetry_exporter_ostream_metrics.so
%{_libdir}/libopentelemetry_exporter_ostream_span.so
%{_libdir}/libopentelemetry_exporter_otlp_grpc_client.so
%{_libdir}/libopentelemetry_exporter_otlp_grpc_log.so
%{_libdir}/libopentelemetry_exporter_otlp_grpc_metrics.so
%{_libdir}/libopentelemetry_exporter_otlp_grpc.so
%{_libdir}/libopentelemetry_exporter_otlp_http_client.so
%{_libdir}/libopentelemetry_exporter_otlp_http_metric.so
%{_libdir}/libopentelemetry_exporter_otlp_http.so
%{_libdir}/libopentelemetry_http_client_curl.so
%{_libdir}/libopentelemetry_metrics.so
%{_libdir}/libopentelemetry_otlp_recordable.so
%{_libdir}/libopentelemetry_proto_grpc.so
%{_libdir}/libopentelemetry_proto.so
%{_libdir}/libopentelemetry_resources.so
%{_libdir}/libopentelemetry_trace.so
%{_libdir}/libopentelemetry_version.so
%{_libdir}/libopentelemetry_zpages.so

%files devel
%{_includedir}/opentelemetry/*
%{_libdir}/cmake/opentelemetry-cpp/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.10.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jul 17 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.10.0-1
- Original version for CBL-Mariner
- License Verified
