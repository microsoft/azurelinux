%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Prism
Name:           image-customizer
Version:        0.12.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/microsoft/azure-linux-image-tools
Source0:        https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/azure-linux-image-tools-%{version}.tar.gz
BuildArch: noarch
BuildRequires: golang >= 1.20
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
go mod tidy
go build -o %{_builddir}/image-customizer .

%install
mkdir -p %{buildroot}/usr/local/bin/
install -m 755 %{_builddir}/image-customizer %{buildroot}/usr/local/bin/image-customizer

%files
/usr/local/bin/image-customizer

%changelog
* Wed Mar 12 2025 Elaine Zhao <elainezhao@microsoft.com> - 0.12.0-1
- Original version for Azure Linux.
