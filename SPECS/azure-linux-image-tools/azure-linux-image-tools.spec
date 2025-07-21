%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Azure Linux Image Tools
Name:           azure-linux-image-tools
Version:        0.15.0
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/microsoft/azure-linux-image-tools/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# We can use the generate-source-tarball.sh script in the given folder along with the package version to build the tarball automatically.
# In case we need to re-build this file manually:
#   1. wget https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod tidy
#   5. go mod vendor
#   6. tar  --sort=name \
#           --mtime="2025-07-18 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor-1.tar.gz
Patch0:         skip-license-scan.patch
BuildRequires: golang >= 1.24.1
BuildRequires: systemd-udev
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
# Requires: oras
# Requires: azurelinux-repos-cloud-native

%description
The Azure Linux Image Customizer is a tool that can take an
existing generic Azure Linux image and modify it to be suited for a particular
scenario. By providing an Azure Linux base image, users can also supply a config
file specifying how they want the image to be customized. For example, this
could include the installation of certain RPMs, updating the SELinux mode, and
enabling DM-Verity.

%prep
%autosetup -n %{name}-%{version} -p1
rm -rf toolkit/tools/vendor
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
%{_bindir}/imagecustomizer

%changelog
* Tue Jul 15 2025 Lanze Liu <lanzeliu@microsoft.com> 0.15.0-1
- Original version for Azure Linux (license: MIT).
- License verified.
