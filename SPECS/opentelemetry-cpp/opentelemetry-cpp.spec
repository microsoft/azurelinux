Summary:        The OpenTelemetry C++ Client
Name:           opentelemetry-cpp
Version:	1.10.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/open-telemetry/opentelemetry-cpp
Source0:        https://github.com/open-telemetry/opentelemetry-cpp/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gtest-devel
BuildRequires:  gmock-devel

%description
The official OpenTelemetry CPP client

%prep
%autosetup -p1

%build
mkdir build && cd build
%cmake -DWITH_BENCHMARK=OFF ..
%make_build

%install
%make_install -C build

%check
%make_build -C build check

%files
%license LICENSE
%{_includedir}/opentelemetry/*
%{_libdir}/cmake/opentelemetry-cpp/*
%{_libdir}/libopentelemetry_common.so
%{_libdir}/libopentelemetry_exporter_in_memory.so
%{_libdir}/libopentelemetry_exporter_ostream_metrics.so
%{_libdir}/libopentelemetry_exporter_ostream_span.so
%{_libdir}/libopentelemetry_metrics.so
%{_libdir}/libopentelemetry_resources.so
%{_libdir}/libopentelemetry_trace.so
%{_libdir}/libopentelemetry_version.so

%changelog
* Mon Jul 17 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.10.0-1
- Original version for CBL-Mariner
- License Verified
