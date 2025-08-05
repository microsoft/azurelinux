%define our_gopath %{_topdir}/.gopath

Summary:        Azure Linux Image Tools
Name:           azure-linux-image-tools
Version:        0.16.0
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/microsoft/azure-linux-image-tools/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Use generate_source_tarball.sh script with the package version to build this tarball.
#
Source1:        %{name}-%{version}-vendor-test.tar.gz
BuildRequires: golang >= 1.24.1
BuildRequires: systemd-udev
Requires: imagecustomizer = %{version}-%{release}

%description
Azure Linux Image Tools. This package provides the Azure Linux Image Customizer tool
and its dependencies for customizing Azure Linux images.

%package -n imagecustomizer
Summary: Image Customizer
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
Requires: binutils
Requires: lsof
Requires: python3
Requires: python3-pip
Requires: jq
%ifarch x86_64
Requires: grub2-pc
Requires: systemd-ukify
%endif

%description -n imagecustomizer
The Azure Linux Image Customizer is a tool that can take an
existing generic Azure Linux image and modify it to be suited for a particular
scenario. By providing an Azure Linux base image, users can also supply a config
file specifying how they want the image to be customized. For example, this
could include the installation of certain RPMs, updating the SELinux mode, and
enabling DM-Verity.

%prep
%autosetup -p1
tar -xf %{SOURCE1} --no-same-owner -C toolkit/tools

%build
export GOPATH=%{our_gopath}
export GOFLAGS="-mod=vendor"
make -C toolkit go-imagecustomizer REBUILD_TOOLS=y SKIP_LICENSE_SCAN=y

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 toolkit/out/tools/imagecustomizer %{buildroot}%{_bindir}/imagecustomizer

%check
go test -C toolkit/tools ./...

%files
%license LICENSE

%files -n imagecustomizer
%license LICENSE
%{_bindir}/imagecustomizer

%changelog
* Fri Jul 25 2025 Lanze Liu <lanzeliu@microsoft.com> 0.16.0-1
- Original version for Azure Linux (license: MIT).
- License verified.
