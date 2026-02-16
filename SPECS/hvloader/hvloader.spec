%define  debug_package %{nil}
%define  name_github   HvLoader
%define  edk2_tag      edk2-stable202305
Summary:        HvLoader.efi is an EFI application for loading an external hypervisor loader.
Name:           hvloader
Version:        1.0.1
Release:        18%{?dist}
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
Patch2:         CVE-2024-5535.patch
Patch3:         CVE-2023-45230.patch
Patch4:         CVE-2023-45229.patch
Patch5:         CVE-2023-45231.patch
Patch6:         CVE-2023-45232_CVE-2023-45233.patch
Patch7:         CVE-2023-45234.patch
Patch8:         CVE-2023-45235.patch
Patch9:         CVE-2023-2650.patch
Patch10:        CVE-2023-0465.patch
Patch11:        CVE-2024-0727.patch
Patch12:        CVE-2023-3817.patch
Patch13:        CVE-2023-5678.patch
Patch14:        vendored-openssl-1.1.1-Only-free-the-read-buffers-if-we-re-not-using-them.patch
Patch15:        CVE-2022-36763_CVE-2023-36764.patch
Patch16:        CVE-2022-36765.patch
Patch17:        CVE-2023-45237.patch
Patch18:        CVE-2023-45236.patch
Patch19:        CVE-2024-38796.patch
Patch20:        CVE-2025-3770.patch
Patch21:        CVE-2025-2296.patch
Patch22:        CVE-2025-2295.patch
Patch23:        CVE-2025-69419.patch
Patch24:        CVE-2025-69420.patch
Patch25:        CVE-2025-69421.patch
Patch26:        CVE-2026-22795.patch
Patch27:        CVE-2025-68160.patch
Patch28:        CVE-2025-69418.patch
Patch29:        CVE-2026-22796.nopatch


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
* Sun Feb 15 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-18
- Patch for CVE-2025-68160, CVE-2025-69418
- Add nopatch for CVE-2026-22796(CVE-2026-22795 already has the fix)

* Mon Feb 09 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-17
- Patch for CVE-2026-22795, CVE-2025-69421, CVE-2025-69420, CVE-2025-69419

* Tue Jan 06 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-16
- Patch for CVE-2025-2295

* Thu Nov 20 2025 Jyoti kanase <v-jykanase@microsoft.com> - 1.0.1-15
- Patch for CVE-2025-2296

* Tue Aug 12 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-14
- Patch for CVE-2025-3770

* Tue May 13 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.0.1-13
- Fix CVE-2024-38796 with an upstream patch

* Tue Apr 29 2025 Mayank Singh <mayansingh@microsoft.com> - 1.0.1-12
- Fix CVE-2023-45236 and CVE-2023-45237 with an upstream patch

* Fri Apr 25 2025 Mayank Singh <mayansingh@microsoft.com> - 1.0.1-11
- Fix CVE-2022-36763, CVE-2022-36764 and CVE-2022-36765 with an upstream patch

* Tue Mar 25 2025 Tobias Brick <tobiasb@microsoft.com> - 1.0.1-10
- Patch vendored openssl to only free read buffers if not in use.

* Fri Mar 21 2025 Daniel McIlvaney <damcilva@microsoft.com> - 1.0.1-9
- Reconcile merge issue

* Mon Mar 03 2025 Sreeniavsulu Malavathula <v-smalavathu@microsoft.com> - 1.0.1-8
- Add patch for CVE-2023-2650.patch
- Add patch for CVE-2023-0465.patch
- Add patch for CVE-2024-0727.patch
- Add patch for CVE-2023-3817.patch
- Add patch for CVE-2023-5678.patch

* Fri Feb 21 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 1.0.1-7
- Add patch to resolve CVE-2023-45230
- Add patch to resolve CVE-2023-45229
- Add patch to resolve CVE-2023-45231
- Add patch to resolve CVE-2023-45232 and CVE-2023-45233
- Add patch to resolve CVE-2023-45234
- Add patch to resolve CVE-2023-45235

* Mon Nov 25 2024 Zhichun Wan <zhichunwan@microsoft.com> - 1.0.1-6
- Add patch to resolve CVE-2024-5535

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
