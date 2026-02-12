%global debug_package %{nil}
%define name_github   HvLoader
%ifarch x86_64
%global buildarch x86_64
%endif
Summary:        Signed HvLoader.efi for %{buildarch} systems
Name:           hvloader-signed-%{buildarch}
Version:        1.0.1
Release:        17%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
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
Source0:        hvloader-%{version}-%{release}.%{buildarch}.rpm
Source1:        HvLoader.efi
ExclusiveArch:  x86_64

%description
This package contains the HvLoader EFI binary signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%package -n     hvloader
Summary:        HvLoader.efi is an EFI application for loading an external hypervisor loader.
Group:          Applications/System

%description -n hvloader
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

%files -n hvloader
%license MdeModulePkg/Application/%{name_github}-%{version}/LICENSE
/boot/efi/HvLoader.efi

%changelog
<<<<<<< HEAD
* Mon Feb 02 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-17
=======
* Mon Feb 09 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-17
>>>>>>> 4f89bd840 ([AutoPR- Security] Patch hvloader for CVE-2026-22795, CVE-2025-69421, CVE-2025-69420, CVE-2025-69419 [HIGH] (#15767))
- Bump release for consistency with hvloader spec.

* Tue Jan 06 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-16
- Bump release for consistency with hvloader spec.

* Thu Nov 20 2025 Jyoti kanase <v-jykanase@microsoft.com> - 1.0.1-15
- Bump release for consistency with hvloader spec.

* Tue Aug 12 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.0.1-14
- Bump release for consistency with hvloader spec.

* Tue May 13 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.0.1-13
- Bump release for consistency with hvloader spec.

* Tue Apr 29 2025 Mayank Singh <mayansingh@microsoft.com> - 1.0.1-12
- Bump release for consistency with hvloader spec.

* Fri Apr 25 2025 Mayank Singh <mayansingh@microsoft.com> - 1.0.1-11
- Bump release for consistency with hvloader spec.

* Wed Mar 26 2025 Tobias Brick <tobiasb@microsoft.com> - 1.0.1-10
- Bump release for consistency with hvloader spec.

* Fri Mar 21 2025 Daniel McIlvaney <damcilva@microsoft.com> - 1.0.1-9
- Update version for consistency with hvloader spec

* Tue Mar 04 2025 Sreeniavsulu Malavathula <v-smalavathu@microsoft.com> - 1.0.1-8
- Update version for consistency with hvloader spec

* Mon Feb 24 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 1.0.1-7
- Update version for consistency with hvloader spec

* Mon Nov 25 2024 Zhichun Wan <zhichunwan@microsoft.com> - 1.0.1-6
- Update version for consistency with hvloader spec

* Wed Jun 19 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-5
- Update version for consistency with hvloader spec

* Thu Jun 06 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-4
- Update version for consistency with hvloader spec

* Fri May 31 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-3
- Update version for consistency with hvloader spec

* Fri May 10 2024 Archana Choudhary <archana1@microsoft.com> - 1.0.1-2
- Update version for consistency with hvloader spec

* Thu Jan 04 2024 Cameron Baird <cameronbaird@microsoft.com> - 1.0.1-1
- Original version for CBL-Mariner.
- License verified
