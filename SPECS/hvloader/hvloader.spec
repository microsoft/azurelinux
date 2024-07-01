%define  debug_package %{nil}
%define  name_github   HvLoader
%define  edk2_tag      edk2-stable202305
Summary:        HvLoader.efi is an EFI application for loading an external hypervisor loader.
Name:           hvloader
Version:        1.0.1
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/microsoft/HvLoader
Source0:        https://github.com/microsoft/HvLoader/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Instructions to generate edk2 submodules: https://github.com/tianocore/edk2/tree/edk2-stable202302?tab=readme-ov-file#submodules
Source1:        https://github.com/tianocore/edk2/archive/refs/tags/%{edk2_tag}.tar.gz#/%{edk2_tag}-submodules.tar.gz
Source2:        target-x86.txt
Patch0:         CVE-2024-1298.patch
Patch1:         CVE-2023-0464.patch
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
ExclusiveArch:  x86_64

%description
HvLoader.efi is an EFI application for loading an external hypervisor loader.

HvLoader.efi loads a given hypervisor loader binary (DLL, EFI, etc.), and 
calls it's entry point passing HvLoader.efi ImageHandle. This way the 
hypervisor loader binary has access to HvLoader.efi's command line options,
and use those as configuration parameters. The first HvLoader.efi command line
option is the path to hypervisor loader binary.

%prep
%autosetup -a 0 -a 1 -c "%{name}-%{version}" -p1
set -x
ls -l
mv %{name_github}-%{version} MdeModulePkg/Application

%build
export EDK_TOOLS_PATH=$(pwd)/BaseTools
source ./edksetup.sh
make -C BaseTools
sed -i '/MdeModulePkg\/Application\/HelloWorld\/HelloWorld.inf/a \ \ MdeModulePkg\/Application\/%{name_github}-%{version}/HvLoader.inf' MdeModulePkg/MdeModulePkg.dsc
cp %{SOURCE2} Conf/target.txt
build -p MdeModulePkg/MdeModulePkg.dsc -m MdeModulePkg/Application/%{name_github}-%{version}/HvLoader.inf

%install
mkdir -p %{buildroot}/boot/efi
cp ./Build/MdeModule/RELEASE_GCC5/X64/MdeModulePkg/Application/%{name_github}-%{version}/%{name_github}/OUTPUT/HvLoader.efi %{buildroot}/boot/efi

%files
%license MdeModulePkg/Application/%{name_github}-%{version}/LICENSE
/boot/efi/HvLoader.efi

%changelog
* Wed Jun 19 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-5
- Add patch to resolve CVE-2023-0464

* Thu Jun 06 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-4
- Add patch to resolve CVE-2024-1298

* Fri May 31 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-3
- Update edk2_tag to edk2-stable202305
- Publish edk2-stable202305-submodules source 
- Correct the resolution of openssl related CVEs (CVE-2023-0286, CVE-2023-0215, CVE-2022-4450, CVE-2022-4304) that were not successfully addressed in the previous update

* Wed May 08 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-2
- Update edk2_tag to edk2-stable202302
- Publish edk2-stable202302-submodules source
- Address openssl related CVEs (CVE-2023-0286, CVE-2023-0215, CVE-2022-4450, CVE-2022-4304)

* Tue May 02 2023 Cameron Baird <cameronbaird@microsoft.com> - 1.0.1-1
- Add hvloader.spec
- License verified
- Original version for CBL-Mariner
