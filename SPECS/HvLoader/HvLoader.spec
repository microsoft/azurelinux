%define  debug_package %{nil}
Summary:        HvLoader.efi is an EFI application for loading an external hypervisor loader.
Name:           HvLoader
Version:        1.0.0
Release:        1%{?dist}
License:        BSD-2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
# TODO - find good location for source
URL:            https://github.com/Camelron/HvLoader
Source0:        https://github.com/tianocore/edk2/archive/refs/tags/edk2-stable202211.tar.gz#/edk2-submodules.tar.gz
Source1:        https://github.com/Camelron/HvLoader/releases/download/v1.0.0/HvLoader-1.0.0.tar.gz#/%{name}-%{version}.tar.gz
Source2:        target.txt
BuildRequires:  bc
BuildRequires:  gcc
BuildRequires:  build-essential
BuildRequires:  gcc-c++
BuildRequires:  genisoimage
BuildRequires:  acpica-tools
BuildRequires:  libuuid-devel
BuildRequires:  nasm
BuildRequires:  python3
BuildRequires:  python3-devel

%description
HvLoader.efi is an EFI application for loading an external hypervisor loader.

HvLoader.efi loads a given hypervisor loader binary (DLL, EFI, etc.), and 
calls it's entry point passing HvLoader.efi ImageHandle. This way the 
hypervisor loader binary has access to HvLoader.efi's command line options,
and use those as configuration parameters. The first HvLoader.efi command line
option is the path to hypervisor loader binary.

%prep
%setup -q -a 1 -c
mv %{name}-%{version} MdeModulePkg/Application

%build
export EDK_TOOLS_PATH=$(pwd)/BaseTools
source ./edksetup.sh
make -C BaseTools
sed -i '/MdeModulePkg\/Application\/HelloWorld\/HelloWorld.inf/a \ \ MdeModulePkg\/Application\/%{name}-%{version}/HvLoader.inf' MdeModulePkg/MdeModulePkg.dsc
cp %{SOURCE2} Conf/target.txt
build -p MdeModulePkg/MdeModulePkg.dsc -m MdeModulePkg/Application/%{name}-%{version}/HvLoader.inf
echo "done with code $?"

%install
echo "install :)"
mkdir -p %{buildroot}/boot/efi
cp ./Build/MdeModule/RELEASE_GCC5/X64/MdeModulePkg/Application/HvLoader-1.0.0/HvLoader/OUTPUT/HvLoader.efi %{buildroot}/boot/efi

%files
/boot/efi/HvLoader.efi

%changelog
* Thu Jan 26 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.0.0-1
- Add HvLoader.spec
- License verified
- Original version for CBL-Mariner
