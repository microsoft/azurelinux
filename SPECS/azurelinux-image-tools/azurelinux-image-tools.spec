%define our_gopath %{_topdir}/.gopath

Summary:        Azure Linux Image Tools
Name:           azurelinux-image-tools
Version:        1.1.0
Release:        2%{?dist}
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
Source1:        %{name}-%{version}-vendor.tar.gz
BuildRequires: golang < 1.25
BuildRequires: systemd-udev
Requires: %{name}-imagecustomizer = %{version}-%{release}

%description
Azure Linux Image Tools. This package provides the Azure Linux Image Customizer tool
and its dependencies for customizing Azure Linux images.

%package imagecustomizer
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
Requires: btrfs-progs
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

%description imagecustomizer
The Azure Linux Image Customizer is a tool that can take an
existing generic Azure Linux image and modify it to be suited for a particular
scenario. By providing an Azure Linux base image, users can also supply a config
file specifying how they want the image to be customized. For example, this
could include the installation of certain RPMs, updating the SELinux mode, and
enabling DM-Verity.

%package osmodifier
Summary: OS Modifier

%description osmodifier
The Azure Linux OS Modifier is a tool that can modify an OS.

%prep
%autosetup -p1 -n azure-linux-image-tools-%{version}
tar -xf %{SOURCE1} --no-same-owner

%build
export GOPATH=%{our_gopath}
export GOFLAGS="-mod=vendor"
make -C toolkit go-imagecustomizer REBUILD_TOOLS=y SKIP_LICENSE_SCAN=y IMAGE_CUSTOMIZER_VERSION_PREVIEW=
make -C toolkit go-osmodifier REBUILD_TOOLS=y SKIP_LICENSE_SCAN=y

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 toolkit/out/tools/imagecustomizer %{buildroot}%{_bindir}/imagecustomizer
install -p -m 0755 toolkit/out/tools/osmodifier %{buildroot}%{_bindir}/osmodifier

# Install container support files for imagecustomizer subpackage
# These files are used when building the imagecustomizer container
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/imagecustomizer

# Copy container scripts to component-specific lib directory (internal binaries)
install -p -m 0755 toolkit/tools/imagecustomizer/container/entrypoint.sh %{buildroot}%{_libdir}/imagecustomizer/entrypoint.sh
install -p -m 0755 toolkit/tools/imagecustomizer/container/run.sh %{buildroot}%{_libdir}/imagecustomizer/run.sh
install -p -m 0755 toolkit/scripts/telemetry_hopper/telemetry_hopper.py %{buildroot}%{_libdir}/imagecustomizer/telemetry_hopper.py
install -p -m 0644 toolkit/scripts/telemetry_hopper/requirements.txt %{buildroot}%{_libdir}/imagecustomizer/telemetry-requirements.txt

%check
go test -C toolkit/tools ./...

%files

%files imagecustomizer
%license LICENSE
%{_bindir}/imagecustomizer
# Container support files - internal binaries stored in component lib directory
%{_libdir}/imagecustomizer/entrypoint.sh
%{_libdir}/imagecustomizer/run.sh
%{_libdir}/imagecustomizer/telemetry_hopper.py
%{_libdir}/imagecustomizer/telemetry-requirements.txt

%files osmodifier
%license LICENSE
%{_bindir}/osmodifier

%changelog
* Fri Feb 13 2026 Brian Fjeldstad <bfjelds@microsoft.com> 1.1.0-2
- Add osmodifier

* Mon Dec 8 2025 Chris Gunn <chrisgun@microsoft.com> 1.1.0-1
- Upgrade to version 1.1.0

* Wed Sep 24 2025 Lanze Liu <lanzeliu@microsoft.com> 1.0.0-1
- Upgrade to GA version 1.0.0-1

* Wed Sep 3 2025 Lanze Liu <lanzeliu@microsoft.com> 0.19.0-1
- Upgrade the version.
- Fixed imagecustomizer container files location to comply with RPM packaging guidelines
- Moved container dependency files from /etc to /usr/lib/imagecustomizer/

* Sun Aug 31 2025 Andrew Phelps <anphel@microsoft.com> - 0.18.0-2
- Set BR for golang to < 1.25

* Wed Aug 20 2025 Lanze Liu <lanzeliu@microsoft.com> 0.18.0-1
- Original version for Azure Linux (license: MIT).
- License verified.
