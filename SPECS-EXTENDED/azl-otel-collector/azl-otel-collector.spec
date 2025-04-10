%global debug_package   %{nil}

Summary:        Azure Linux OpenTelemetry Collector Distribution
Name:           azl-otel-collector
Version:        0.123.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/microsoft/azl-otel-collector
Source0:        https://azurelinuxsrcstorage.blob.core.windows.net/sources/core/azl-otel-collector-0.123.0-3.tar.gz
Source1:        %{name}-%{version}-vendor-1.tar.gz
Source2:        azl-otel-collector.service
BuildRequires:  golang
BuildRequires:  systemd-rpm-macros
# Include the smartmontools package needed by the smartdata receiver in the collector
Requires:       smartmontools
Requires(post): systemd
Conflicts:      azl-otel-collector
%{?systemd_requires}


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
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/azl-otel-collector.service
install -D -m 0644 config/default-config.yaml %{buildroot}%{_sysconfdir}/azl-otel-collector/config.yaml

%preun
%systemd_preun azl-otel-collector.service

%post
%systemd_post azl-otel-collector.service

%postun
%systemd_postun_with_restart azl-otel-collector.service

%files
%{_bindir}/azl-otelcol
%dir %{_sysconfdir}/azl-otel-collector
%{_sysconfdir}/azl-otel-collector/config.yaml
%{_unitdir}/azl-otel-collector.service
%license LICENSE



%changelog
* Thu Apr 10 2025 Adit Jha <aditjha@microsoft.com> - 0.123.0-1
- Original version for Azure Linux
- License Verified
