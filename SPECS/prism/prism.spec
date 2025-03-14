%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Azure Linux image customization tool
Name:           prism
Version:        0.12.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/microsoft/azure-linux-image-tools
Source0:        https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/azure-linux-image-tools-%{version}.tar.gz
BuildArch: x86_64
#BuildRequires: golang >= 1.21
Requires: qemu-img
Requires: rpm
Requires: coreutils
Requires: util-linux
Requires: systemd
Requires: openssl
Requires: sed
Requires: createrepo_c
Requires: squashfs-tools
Requires: cdrkit
Requires: parted
Requires: e2fsprogs
Requires: dosfstools
Requires: xfsprogs
Requires: zstd
Requires: veritysetup
Requires: grub2
Requires: grub2-pc
Requires: systemd-ukify

%description
The Image Customizer is a tool that can take an existing generic Azure Linux image 
and modify it to be suited for particular scenario.

The Image Customizer uses chroot (and loopback block devices) to customize the image. 
This is the same technology used to build the Azure Linux images, along with most other
Linux distros. This is in contrast to some other image customization tools, like Packer, 
which customize the image by booting it inside a VM.

%prep
%autosetup -n azure-linux-image-tools-%{version}

%build
export GOPATH=%{our_gopath}
cd toolkit/tools/imagecustomizer
go build -o %{_builddir}/imagecustomizer .

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_builddir}/imagecustomizer %{buildroot}%{_bindir}/imagecustomizer

%files
%{_bindir}/imagecustomizer
%license LICENSE

%changelog
* Thu Mar 13 2025 Elaine Zhao <elainezhao@microsoft.com> - 0.12.0-1
- Original version for Azure Linux.
- License verified.