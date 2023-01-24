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
Source0:        https://github.com/Camelron/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  edk2
BuildRequires:  make
BuildRequires:  build-essential
BuildRequires:  libuuid-devel
BuildRequires:  nasm

%description
HvLoader.efi is an EFI application for loading an external hypervisor loader.

HvLoader.efi loads a given hypervisor loader binary (DLL, EFI, etc.), and calls it's entry point passing HvLoader.efi ImageHandle. This way the hypervisor loader binary has access to HvLoader.efi's command line options, and use those as configuration parameters. The first HvLoader.efi command line option is the path to hypervisor loader binary.

%prep
%autosetup

%build
%make_build

%install
mkdir -p %{buildroot}%{_bindir}/
install -p -m 755 pigz %{buildroot}%{_bindir}/
install -p -m 755 unpigz %{buildroot}%{_bindir}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license README
%{_bindir}/pigz
%{_bindir}/unpigz

%changelog
* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-2
- Fixing invalid source URL.
* Tue Feb 09 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.6-1
- Update pigz to 2.6
- Change source url to GitHub.
* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.5-1
- Add pigz spec
- License verified
- Original version for CBL-Mariner
