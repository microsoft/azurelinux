Summary:        Azure Linux OpenTelemetry Collector Distribution
Name:           otel-collector
Version:        0.121.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/open-telemetry/opentelemetry-collector
Source0:        https://github.com/open-telemetry/opentelemetry-collector/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor-1.tar.gz
BuildRequires:  golang

%description
Azure Linux OpenTelemetry Collector is a custom distribution of the
OpenTelemetry Collector. It contains a subset of the components from the
https://github.com/open-telemetry/opentelemetry-collector-contrib repository and
also includes receivers developed by the Azure Linux team.

%prep
%autosetup -n otel-collector-%{version}
tar -xf %{SOURCE1} --no-same-owner

%build
pushd cmd/otelcorecol && CGO_ENABLED=0 go build -mod=vendor -ldflags="-s -w" -trimpath -o ./bin/otel-collector -tags "netgo" ./cmd/otelcorecol && popd

%install
mkdir -p "%{buildroot}/%{_bindir}"
install -D -m0755 bin/otel-collector %{buildroot}/%{_bindir}

%files
%{_bindir}/otel-collector
%license LICENSE


%changelog
* Thu Mar 27 2025 Adit Jha <aditjha@microsoft.com> - 0.121.0-1
- Original version for Azure Linux
- License Verified
