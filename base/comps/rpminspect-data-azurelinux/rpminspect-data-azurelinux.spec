Name:           rpminspect-data-azurelinux
Version:        1.0
Release:        %autorelease
Summary:        Azure Linux configuration for rpminspect
License:        CC0-1.0 AND CC-BY-4.0
BuildArch:      noarch
Source0:        azurelinux.yaml
Source1:        azurelinux-fileinfo
Source2:        azurelinux-capabilities

Requires:       rpminspect
Requires:       rpminspect-data-generic >= 2.1
Requires:       clamav-data

%description
This package provides the Azure Linux rpminspect configuration. It uses the
generic vendor-data template for structural RPM inspections, plus curated
Azure Linux fileinfo and capabilities allow-lists. License inspection is
disabled until Azure Linux provides curated license policy data.

%install
install -Dpm 0644 %{SOURCE0} %{buildroot}%{_datadir}/rpminspect/azurelinux.yaml
# rpminspect only reads VENDOR_DATA_DIR/rpminspect.yaml without -c; make this
# policy the default so plain `rpminspect <RPM>` selects it.
ln -s azurelinux.yaml %{buildroot}%{_datadir}/rpminspect/rpminspect.yaml
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/rpminspect/fileinfo/AZURELINUX4
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_datadir}/rpminspect/capabilities/AZURELINUX4

%files
%{_datadir}/rpminspect/azurelinux.yaml
%{_datadir}/rpminspect/rpminspect.yaml
%{_datadir}/rpminspect/fileinfo/AZURELINUX4
%{_datadir}/rpminspect/capabilities/AZURELINUX4

%changelog
%autochangelog
