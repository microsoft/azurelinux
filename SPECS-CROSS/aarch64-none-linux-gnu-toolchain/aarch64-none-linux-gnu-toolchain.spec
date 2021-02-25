Summary:        Prebuilt aarch64-none-linux-gnu cross compiling toolchain
Name:           aarch64-none-linux-gnu-toolchain
Version:        0.1.0
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
AutoReqProv:    no
ExclusiveArch:  x86_64
URL:            https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads
Source0:        gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnu.tar.xz

%description
Prebuilt aarch64-none-linux-gnu cross compiling toolchain from Linaro/ARM

%prep
%autosetup -c -p1

%build

%install
install -d %{buildroot}/opt/cross
cp -r * %{buildroot}/opt/cross

%files
%defattr(-,root,root)
/opt/cross/*

%changelog
* Fri Feb 19 2021 Chris Co <chrco@microsoft.com> 0.1.0-1
- Initial version