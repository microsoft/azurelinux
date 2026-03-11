%bcond_with check

%global goarch %{_arch}
%ifarch x86_64
%global goarch amd64
%endif
%ifarch aarch64
%global goarch arm64
%endif

%define with_cross  0

%define with_validate  0

%define with_grub  0

# https://github.com/coreos/ignition
%global goipath         github.com/coreos/ignition
%global gomodulesmode   GO111MODULE=on
Version:                2.22.0

%global golicenses      LICENSE
%global godocs          README.md docs/
%global dracutlibdir %{_prefix}/lib/dracut

Name:           ignition
Release:        1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        First boot installer and configuration tool

# Upstream license specification: Apache-2.0
License:        Apache-2.0
URL:            %{gourl}
Source0:        https://github.com/coreos/ignition/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-sed-s-coreos-flatcar.patch
Patch1:         0002-config-add-ignition-translation.patch
Patch2:         0003-mod-add-flatcar-ignition-0.36.2.patch
Patch3:         0004-sum-go-mod-tidy.patch
Patch4:         0005-vendor-go-mod-vendor.patch
Patch5:         0006-config-v3_6-convert-ignition-2.x-to-3.x.patch
Patch6:         0007-internal-prv-cmdline-backport-flatcar-patch.patch
Patch7:         0008-provider-qemu-apply-fw_cfg-patch.patch
Patch8:         0009-config-3_6-test-add-ignition-2.x-test-cases.patch
Patch9:         0010-internal-disk-fs-ignore-fs-format-mismatches-for-the.patch
Patch10:        0011-VMware-Fix-guestinfo.-.config.data-and-.config.url-v.patch
Patch11:        0012-config-version-handle-configuration-version-1.patch
Patch12:        0013-config-util-add-cloud-init-detection-to-initial-pars.patch
Patch13:        0014-Revert-drop-OEM-URI-support.patch
Patch14:        0015-internal-resource-url-support-btrfs-as-OEM-partition.patch
Patch15:        0016-translation-support-OEM-and-oem.patch
Patch16:        0017-revert-internal-oem-drop-noop-OEMs.patch
Patch17:        0018-docs-Add-re-added-platforms-to-docs-to-pass-tests.patch
Patch18:        0019-usr-share-oem-oem.patch
Patch19:        0020-internal-exec-stages-mount-Mount-oem.patch

BuildRequires: libblkid-devel
BuildRequires: systemd-rpm-macros
BuildRequires: go-rpm-macros
BuildRequires: golang

ExcludeArch: %{ix86}

# Requires for 'disks' stage
%if 0%{?fedora}
Recommends: btrfs-progs
%endif
Requires: dosfstools
Requires: gdisk
Requires: dracut

%description
Ignition is a utility used to manipulate systems during the initramfs.
This includes partitioning disks, formatting partitions, writing files
(regular files, systemd units, etc.), and configuring users. On first
boot, Ignition reads its configuration from a source of truth (remote
URL, network metadata service, hypervisor bridge, etc.) and applies
the configuration.

%if 0%{?with_validate}
############## validate subpackage ##############

%package validate

Summary:  Validation tool for Ignition configs
License:  Apache-2.0

%description validate
Ignition is a utility used to manipulate systems during the initramfs.
This includes partitioning disks, formatting partitions, writing files
(regular files, systemd units, etc.), and configuring users. On first
boot, Ignition reads its configuration from a source of truth (remote
URL, network metadata service, hypervisor bridge, etc.) and applies
the configuration.

This package contains a tool for validating Ignition configurations.

%endif

%if 0%{?with_grub}
############## grub subpackage ##############

%package grub
Summary:  Enablement glue for bootupd's grub2 config
License:  Apache-2.0

# `ignition-grub` is a rename `ignition-ignition-grub` so let's obsolete `ignition-ignition-grub`
Obsoletes: ignition-ignition-grub < 2.13.0-4

%description grub
This package contains the grub2 config which is compatable with bootupd.
%endif

%prep
%forgeautosetup -p1

%build
export LDFLAGS="-X github.com/flatcar/ignition/v2/internal/version.Raw=%{version} -X github.com/flatcar/ignition/v2/internal/distro.selinuxRelabel=false "
export GOFLAGS="-mod=vendor"

echo "Building ignition..."
go build -ldflags "${LDFLAGS:-}" -o ./ignition internal/main.go

%if 0%{?with_validate}
echo "Building ignition-validate..."
go build -ldflags "${LDFLAGS:-}" -o ./ignition-validate validate/main.go

%global gocrossbuild go build -ldflags "${LDFLAGS:-}" -B 0x$(cat /dev/urandom | tr -d -c '0-9a-f' | head -c16)" -a -v -x
%endif

%if 0%{?with_cross}
echo "Building statically-linked Linux ignition-validate..."
GOEXPERIMENT= CGO_ENABLED=0 GOARCH=%{goarch} GOOS=linux %gocrossbuild -o ./ignition-validate-%{_target_cpu}-unknown-linux-gnu-static validate/main.go
GOEXPERIMENT= CGO_ENABLED=0 GOARCH=s390x GOOS=linux %gocrossbuild -o ./ignition-validate-s390x-unknown-linux-gnu-static validate/main.go
GOEXPERIMENT= CGO_ENABLED=0 GOARCH=ppc64le GOOS=linux %gocrossbuild -o ./ignition-validate-ppc64le-unknown-linux-gnu-static validate/main.go

echo "Building macOS ignition-validate..."
GOEXPERIMENT= GOARCH=%{goarch} GOOS=darwin %gocrossbuild -o ./ignition-validate-%{_target_cpu}-apple-darwin validate/main.go

%ifarch x86_64
echo "Building Windows ignition-validate..."
GOEXPERIMENT= GOARCH=amd64 GOOS=windows %gocrossbuild -o ./ignition-validate-%{_target_cpu}-pc-windows-gnu.exe validate/main.go
%endif
%endif

%install
install -m 0755 -d %{buildroot}/%{_libexecdir}

%if 0%{?with_grub}
# grub
install -d -p %{buildroot}%{_prefix}/lib/bootupd/grub2-static/configs.d
install -p -m 0644 grub2/05_ignition.cfg  %{buildroot}%{_prefix}/lib/bootupd/grub2-static/configs.d/
%endif

# ignition
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 ./ignition %{buildroot}%{_bindir}
%if 0%{?with_validate}
install -p -m 0755 ./ignition-validate %{buildroot}%{_bindir}
%endif


ln -rsf %{buildroot}%{_bindir}/ignition %{buildroot}%{_libexecdir}/ignition-rmcfg

%if 0%{?with_cross}
install -d -p %{buildroot}%{_datadir}/ignition
install -p -m 0644 ./ignition-validate-* %{buildroot}%{_datadir}/ignition
%endif

%if %{with check}
%check
sed -i '34d' ./test
sed -i '/Checking gofmt/,+5d' ./test
VERSION=%{version} GOARCH=%{goarch} ./test
%endif

%files
%license %{golicenses}
%doc %{godocs}
%{_libexecdir}/ignition-rmcfg
%{_bindir}/ignition

%if 0%{?with_validate}
%files validate
%doc README.md
%license %{golicenses}
%{_bindir}/ignition-validate
%if 0%{?with_cross}
%dir %{_datadir}/ignition
%{_datadir}/ignition/ignition-validate-*
%endif
%endif

%if 0%{?with_grub}
%files grub
%doc README.md
%license %{golicenses}
%{_prefix}/lib/bootupd/grub2-static/configs.d/05_ignition.cfg
%endif

%changelog
* Fri Jan 16 2026 Sumit Jena <v-sumitjena@microsoft.com> - 2.22.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
