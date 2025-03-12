%global debug_package %{nil}
Summary:        Prism
Name:           prism
Version:        0.12.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/microsoft/azure-linux-image-tools
Source0:        Source0: https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch: noarch
BuildRequires: rpm-build
BuildRequires: curl
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
curl -L -o %{name} %{SOURCE0}
chmod +x %{name}

%install
mkdir -p %{buildroot}/usr/local/bin/
install -m 755 image-customizer %{buildroot}/usr/local/bin/image-customizer

%files
/usr/local/bin/image-customizer
%license LICENSE
%doc README.md

%changelog
* Wed Mar 12 2025 Elaine Zhao <elainezhao@microsoft.com> - 0.12.0-1
- Original version for Azure Linux.
