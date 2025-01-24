%global debug_package %{nil}
%define name_github   HvLoader
%ifarch x86_64
%global buildarch x86_64

# edk2-stable202402
%define GITDATE        20240524
%define GITCOMMIT      3e722403cd16

%endif
Summary:        Signed HvLoader.efi for %{buildarch} systems
Name:           edk2-hvloader-signed-%{buildarch}
Version:        %{GITDATE}git%{GITCOMMIT}
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/microsoft/HvLoader
# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        edk2-hvloader-%{version}-%{release}.%{buildarch}.rpm
Source1:        HvLoader.efi
ExclusiveArch:  x86_64

%description
This package contains the HvLoader EFI binary signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%package -n     edk2-hvloader
Summary:        HvLoader.efi is an EFI application for loading an external hypervisor loader.
Group:          Applications/System

%description -n edk2-hvloader
HvLoader.efi is an EFI application for loading an external hypervisor loader.

HvLoader.efi loads a given hypervisor loader binary (DLL, EFI, etc.), and 
calls it's entry point passing HvLoader.efi ImageHandle. This way the 
hypervisor loader binary has access to HvLoader.efi's command line options,
and use those as configuration parameters. The first HvLoader.efi command line
option is the path to hypervisor loader binary.

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed HvLoader binary
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./boot/efi/HvLoader.efi

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%files -n edk2-hvloader
%license MdeModulePkg/Application/%{name_github}-%{version}/LICENSE
/boot/efi/HvLoader.efi

%changelog
* Fri Jan 24 2025 Cameron Baird <cameronbaird@microsoft.com> - 20240524git3e722403cd16-4
- Original version for Azure Linux.
- License verified
