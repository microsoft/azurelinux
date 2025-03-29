%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Azure Linux image customization tool
Name:           prism
Version:        0.13.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/microsoft/azure-linux-image-tools
Source0:        https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/azure-linux-image-tools-%{version}.tar.gz
#BuildRequires: golang >= 1.23.6
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
%ifarch x86_64
Requires: grub2-pc
%endif
Requires: systemd-ukify

# %description below is sourced from the "Overview" section of the Prism documentation:
# https://microsoft.github.io/azure-linux-image-tools/imagecustomizer/README.html
# Please refer to the docs to keep updated.
%description
Prism is a tool that can take an existing generic Azure Linux image and modify it to
be suited for particular scenario.

Prism uses chroot (and loopback block devices) to customize the image. This is the same
technology used to build the Azure Linux images, along with most other Linux distros.
This is in contrast to some other image customization tools, like Packer, which customize
the image by booting it inside a VM.

There are a number of advantages and disadvantages to the chroot approach to customizing images.

Advantages:

- Lower overhead, since you don't need to boot up and shutdown the OS.
- More precision when making changes, since you won't see any side effects that come
  from the OS running.
- The image has fewer requirements (e.g. ssh doesn't need to be installed).

Disadvantages:

- Not all Linux tools play nicely when run under chroot.
  For example, while it is possible to install Kubernetes using Image Customizer,
  initialization of a Kubernetes cluster node must be done while the OS is running
  (e.g. using cloud-init).

%prep
%autosetup -n azure-linux-image-tools-%{version}

%build
export GOPATH=%{our_gopath}
make -C ./toolkit go-imagecustomizer REBUILD_TOOLS=y

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 toolkit/out/tools/imagecustomizer %{buildroot}%{_bindir}/imagecustomizer

%check
go test -C toolkit/tools ./...

%files
%{_bindir}/imagecustomizer
%license LICENSE

%changelog
* Thu Mar 13 2025 Elaine Zhao <elainezhao@microsoft.com> - 0.13.0-1
- Original version for Azure Linux.
- License verified.
