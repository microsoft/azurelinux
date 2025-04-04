%global debug_package   %{nil}

Summary:        Azure Linux OpenTelemetry Collector Distribution
Name:           azl-otel-collector
Version:        0.123.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/open-telemetry/opentelemetry-collector # Upstream repository
Source0:        https://azurelinuxsrcstorage.blob.core.windows.net/sources/core/azl-otel-collector-0.123.0-1.tar.gz
Source1:        %{name}-%{version}-vendor-1.tar.gz
BuildRequires:  golang

%description
Azure Linux OpenTelemetry Collector is a custom distribution of the
OpenTelemetry Collector. It contains a subset of the components from the
https://github.com/open-telemetry/opentelemetry-collector-contrib repository and
also includes receivers developed by the Azure Linux team.

%prep
%autosetup -n azl-otel-collector
tar -xf %{SOURCE1} --no-same-owner
%build
export CGO_ENABLED=0
make azl-otelcol BUILDTAGS="netgo osusergo static_build" LDFLAGS="-s -w" TRIMPATH=1

%install
mkdir -p "%{buildroot}/%{_bindir}"
install -D -m0755 bin/azl-otelcol %{buildroot}/%{_bindir}

%files
%{_bindir}/azl-otelcol
%license LICENSE


%changelog
* Thu Mar 27 2025 Adit Jha <aditjha@microsoft.com> - 0.123.0-1
- Original version for Azure Linux
- License Verified
