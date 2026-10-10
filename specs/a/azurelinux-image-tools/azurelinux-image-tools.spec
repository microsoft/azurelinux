## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define our_gopath %{_topdir}/.gopath

# These binaries are built with CGO_ENABLED=0 via a plain `go build` (no %%gobuild/go-rpm-macros).
# Their embedded DWARF debug info only references GOPATH/module-cache source paths that don't
# exist in the buildroot, so find-debuginfo.sh produces an empty debugsourcefiles.list, which
# rpmbuild then rejects as an empty %%files manifest. Disable debuginfo package generation.
%global debug_package %{nil}

Summary:        Azure Linux Image Tools
Name:           azurelinux-image-tools
Version:        1.7.0
Release:        %autorelease
License:        MIT
URL:            https://github.com/microsoft/azure-linux-image-tools/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/microsoft/azure-linux-image-tools/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Use generate_source_tarball.sh (via `azldev comp prepare-sources`) with the package version to build this tarball.
#
Source1:        %{name}-%{version}-vendor.tar.gz
BuildRequires: golang >= 1.26
BuildRequires: e2fsprogs
BuildRequires: systemd-udev
# Upstream's Makefile unconditionally runs `go test ./...` on the internal packages as a
# prerequisite of the go-imagecustomizer/go-osmodifier build targets; userutils_test.go
# shells out to the `openssl` CLI (passwd -6), which isn't present in the minimal stage2
# buildroot by default.
BuildRequires: openssl
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
# AzL: cdrkit (upstream's 3.0 runtime dep, providing the `mkisofs` binary used for live-ISO
# generation) does not exist in azl4. xorriso (from libisoburn) registers an `alternatives`-
# managed /usr/bin/mkisofs -> xorrisofs, which is a drop-in substitute.
Requires: xorriso
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
Requires: systemd-ukify
%ifarch x86_64
Requires: grub2-pc
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
%autosetup -a1 -p1 -n azure-linux-image-tools-%{version}

%build
export GOPATH=%{our_gopath}
export GOFLAGS="-mod=vendor"
export GOEXPERIMENT=ms_nocgo_opensslcrypto
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
%{_libdir}/imagecustomizer/telemetry_hopper.py
%{_libdir}/imagecustomizer/telemetry-requirements.txt

%files osmodifier
%license LICENSE
%{_bindir}/osmodifier

%changelog
## START: Generated by rpmautospec
* Wed Oct 07 2026 Binu Jose Philip <binujp@gmail.com> - 1.7.0-2
- feat(azurelinux-image-tools): add local component to onboard
  imagecustomizer

* Thu Jan 01 1970 azldev <> - 1.7.0-1
- Initial sources
## END: Generated by rpmautospec
