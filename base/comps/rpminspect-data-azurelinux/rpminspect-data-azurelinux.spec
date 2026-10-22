Name:           rpminspect-data-azurelinux
Version:        1.0
Release:        %autorelease
Summary:        Azure Linux configuration for rpminspect
License:        CC0-1.0
BuildArch:      noarch
Source0:        azurelinux.yaml

Requires:       rpminspect
Requires:       rpminspect-data-generic = 2.1

%description
This package provides the Azure Linux rpminspect configuration. It uses the
generic vendor-data template for structural RPM inspections. License inspection
is disabled until Azure Linux provides curated license policy data.

%install
install -Dpm 0644 %{SOURCE0} %{buildroot}%{_datadir}/rpminspect/azurelinux.yaml

%files
%{_datadir}/rpminspect/azurelinux.yaml

%changelog
