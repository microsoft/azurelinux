%global runtime_make_vars       DEFSERVICEOFFLOAD=true \\\
                                SKIP_GO_VERSION_CHECK=1

%global agent_make_vars         LIBC=gnu

%global debug_package %{nil}

Name:         kata-containers-cc
Version:      0.1.0
Release:      10%{?dist}
Summary:      Kata Confidential Containers
License:      ASL 2.0
Group:        Virtualization/Libraries
Vendor:       Microsoft Corporation
Distribution: Mariner
URL:          https://github.com/microsoft/kata-containers
Source0:      https://github.com/microsoft/kata-containers/archive/refs/tags/cc-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:      https://github.com/microsoft/kata-containers/archive/refs/tags/%{name}-%{version}.tar.gz

Source2:      mariner-coco-build-uvm-image.sh
Source3:      mariner-coco-build-uvm-image.service
Source4:      containerd-for-cc-override.conf
Source5:      runtime.yaml
Source6:      pause-image.sh
Source7:      pause-image.service

ExclusiveArch: x86_64

BuildRequires:  golang
BuildRequires:  make
BuildRequires:  systemd
BuildRequires:  gcc
BuildRequires:  protobuf-compiler
BuildRequires:  mariner-release
BuildRequires:  dracut
BuildRequires:  busybox
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  git
BuildRequires:  sudo
BuildRequires:  curl
BuildRequires:  openssl-devel
BuildRequires:  iptables-devel
BuildRequires:  wget
BuildRequires:  perl-FindBin
BuildRequires:  perl-lib
BuildRequires:  libseccomp-devel
BuildRequires:  kernel-uvm-devel
BuildRequires:  parted
BuildRequires:  opa >= 0.50.2

Requires:  systemd
Requires:  iptables
Requires:  parted
Requires:  qemu-img
Requires:  opa
Requires:  kernel-uvm

%description
Kata Confidential Containers.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
export PATH=$PATH:"$(pwd)/go/bin"
export GOPATH="$(pwd)/go"

# Runtime
pushd %{_builddir}/%{name}-%{version}/src/runtime
%make_build %{runtime_make_vars}
popd

# Tardev snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter
make
chmod +x target/release/tardev-snapshotter
popd

pushd /usr/src/linux-headers*
header_dir=$(basename $PWD)
KERNEL_VER=${header_dir#"linux-headers-"}
KERNEL_MODULE_VER=${KERNEL_VER%%-*}
popd

# Kernel modules
pushd %{_builddir}/%{name}-%{version}/src/tarfs
make KDIR=/usr/src/linux-headers-$KERNEL_VER
make KDIR=/usr/src/linux-headers-$KERNEL_VER install
popd
%define KERNEL_MODULES_DIR %{_builddir}/%{name}-%{version}/src/tarfs/_install/lib/modules/$KERNEL_MODULE_VER

# Agent
pushd %{_builddir}/%{name}-%{version}/src/agent
%make_build %{agent_make_vars}
popd

# UVM rootfs
pushd %{_builddir}/%{name}-%{version}/tools/osbuilder
gcc -O2 ./image-builder/nsdax.gpl.c -o ./image-builder/nsdax

sudo -E PATH=$PATH \
 GOPATH="$(sudo readlink -f %{_builddir}/%{name}-%{version}/src/runtime/go)" \
 AGENT_SOURCE_BIN="$(sudo readlink -f %{_builddir}/%{name}-%{version}/src/agent/target/x86_64-unknown-linux-gnu/debug/kata-agent)" \
 make DISTRO=mariner KERNEL_MODULES_DIR=%{KERNEL_MODULES_DIR} rootfs

rootfs_path="%{_builddir}/%{name}-%{version}/tools/osbuilder/mariner_rootfs"

depmod -a -b ${rootfs_path} $KERNEL_MODULE_VER

# Install agent service
pushd %{_builddir}/%{name}-%{version}/src/agent
sudo -E PATH=$PATH make install-services DESTDIR="${rootfs_path}"
popd

# The previous command doesn't include kata-agent.service and
# kata-containers.target in the rootfs, for an unknown reason.
sudo cp %{_builddir}/%{name}-%{version}/src/agent/kata-containers.target  mariner_rootfs/usr/lib/systemd/system/
sudo cp %{_builddir}/%{name}-%{version}/src/agent/kata-agent.service.in   mariner_rootfs/usr/lib/systemd/system/kata-agent.service
sudo sed -i 's/@BINDIR@\/@AGENT_NAME@/\/usr\/bin\/kata-agent/g' mariner_rootfs/usr/lib/systemd/system/kata-agent.service

# The UVM rootfs will be used to build an img file at the first Host boot.
tar cf mariner-uvm-rootfs.tar.gz mariner_rootfs

popd

%install
%define coco_path opt/confidential-containers
%define coco_bin %{coco_path}/bin
%define defaults_kata %{coco_path}/share/defaults/kata-containers
%define share_kata %{coco_path}/share/kata-containers

# Symlinks for cc binaries
mkdir -p %{buildroot}/%{coco_bin}
mkdir -p %{buildroot}/%{coco_path}/libexec
mkdir -p %{buildroot}/etc/systemd/system/containerd.service.d/
ln -s /usr/bin/cloud-hypervisor %{buildroot}/%{coco_bin}/cloud-hypervisor
ln -s /usr/bin/containerd %{buildroot}/%{coco_bin}/containerd
ln -sf /usr/libexec/virtiofsd %{buildroot}/%{coco_path}/libexec/virtiofsd
install -D -m 0644 %{SOURCE4} %{buildroot}/etc/systemd/system/containerd.service.d/containerd-for-cc-override.conf

find %{buildroot}/etc

# Runtime
pushd %{_builddir}/%{name}-%{version}/src/runtime
install -D -m 0755 containerd-shim-kata-v2 %{buildroot}/usr/local/bin/containerd-shim-kata-cc-v2
install -D -m 0755 kata-monitor %{buildroot}/%{coco_bin}/kata-monitor
install -D -m 0755 kata-runtime %{buildroot}/%{coco_bin}/kata-runtime
install -D -m 0755 data/kata-collect-data.sh %{buildroot}/%{coco_bin}/kata-collect-data.sh

install -D -m 0644 config/configuration-clh.toml %{buildroot}/%{defaults_kata}/configuration-clh.toml
ln -s configuration-clh.toml %{buildroot}/%{defaults_kata}/configuration.toml
sed -i 's|/usr|/opt/confidential-containers|g' %{buildroot}/%{defaults_kata}/configuration-clh.toml
popd

# Tardev-snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter/
sed -i -e 's/containerd.service/kubelet.service/g' tardev-snapshotter.service
install -m 0644 -D -t %{buildroot}%{_unitdir} tardev-snapshotter.service
install -D -m 0755 target/release/tardev-snapshotter  %{buildroot}/usr/bin/tardev-snapshotter

popd

# The UVM rootfs will be used to build an img file at the first host boot.
install -D -m 0755 %{_builddir}/%{name}-%{version}/tools/osbuilder/scripts/lib.sh                   %{buildroot}/%{share_kata}/scripts/lib.sh
install -D -m 0755 %{_builddir}/%{name}-%{version}/tools/osbuilder/image-builder/image_builder.sh   %{buildroot}/%{share_kata}/scripts/image_builder.sh
install -D -m 0755 %{_builddir}/%{name}-%{version}/tools/osbuilder/image-builder/nsdax              %{buildroot}/%{share_kata}/scripts/nsdax
install -D -m 0644 %{_builddir}/%{name}-%{version}/tools/osbuilder/mariner-uvm-rootfs.tar.gz        %{buildroot}/opt/mariner/share/uvm/mariner-uvm-rootfs.tar.gz

install -D -m 0755 %{SOURCE2} %{buildroot}/opt/mariner/share/uvm/mariner-coco-build-uvm-image.sh
install -D -m 0755 %{SOURCE6} %{buildroot}/opt/mariner/share/uvm/pause-image.sh
install -D -m 0644 %{SOURCE5} %{buildroot}/runtime.yaml

install -m 0644 -D -t %{buildroot}%{_unitdir} %{SOURCE3}
install -m 0644 -D -t %{buildroot}%{_unitdir} %{SOURCE7}

%preun
%systemd_preun tardev-snapshotter.service
%systemd_preun mariner-coco-build-uvm-image.service

%postun
%systemd_postun tardev-snapshotter.service
%systemd_postun mariner-coco-build-uvm-image.service

%post
%systemd_post tardev-snapshotter.service
%systemd_post mariner-coco-build-uvm-image.service

%files
/opt/*
/etc/systemd/system/containerd.service.d/containerd-for-cc-override.conf
/runtime.yaml
/usr/bin/tardev-snapshotter
/usr/local/bin/containerd-shim-kata-cc-v2

%{_unitdir}/tardev-snapshotter.service
%{_unitdir}/mariner-coco-build-uvm-image.service
%{_unitdir}/pause-image.service

%license LICENSE
%doc CONTRIBUTING.md
%doc README.md


%changelog
*   Wed Apr 5 2023 Dallas Delaney <dadelan@microsoft.com> 0.1.0-10
-   Add changes from cc-msft-prototypes
-   License verified.
-   Original version for CBL-Mariner

*   Thu Mar 2 2023 Dallas Delaney <dadelan@microsoft.com> 0.1.0-9
-   Fix configuration paths

*   Wed Mar 1 2023 Dallas Delaney <dadelan@microsoft.com> 0.1.0-8
-   Build from source

*   Fri Feb 17 2023 Mitch Zhu <mitchzhu@microsoft.com> 0.1.0-7
-   Port over kata-cc spec update

*   Wed Jan 18 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-6
-   Build kata UVM image

*   Mon Jan 16 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-5
-   Build kata runtime from source code

*   Mon Jan 16 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-4
-   Build kata-agent from source code

*   Thu Jan 12 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-3
-   Install /usr/local/bin/containerd-shim-kata-clh-v2

*   Thu Jan 12 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-2
-   Mariner-based host configuration

*   Tue Oct 25 2022 Dallas Delaney <dadelan@microsoft.com> 0.1.0-1
-   Initial rpm data and spec added
