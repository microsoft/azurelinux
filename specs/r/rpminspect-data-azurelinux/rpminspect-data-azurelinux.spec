## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

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
