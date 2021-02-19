Summary:        Prebuilt aarch64-mariner-linux-gnu cross compiling toolchain
Name:           aarch64-mariner-linux-gnu-prebuilt-toolchain
Version:        0.1.0
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
AutoReqProv:    no
ExclusiveArch:  x86_64
Source0:        %{name}-%{version}.tar.gz

%description
Prebuilt aarch64-mariner-linux-gnu cross compiling toolchain

%prep
%autosetup -c

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