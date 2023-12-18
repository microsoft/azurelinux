%global runtime_make_vars       DEFSTATICRESOURCEMGMT=true \\\
                                SKIP_GO_VERSION_CHECK=1

%global agent_make_vars         LIBC=gnu \\\
                                SECURITY_POLICY=yes

%global debug_package %{nil}

Name:         kata-cc-qemu
Version:      0.6.2
Release:      1%{?dist}
Summary:      Kata Confidential Containers for KVM-QEMU SEV-SNP Setup
License:      ASL 2.0
Vendor:       Microsoft Corporation
URL:          https://github.com/microsoft/kata-containers
Source0:      https://github.com/microsoft/kata-containers/archive/refs/tags/cc-%{version}.tar.gz#/kata-containers-cc-%{version}.tar.gz
Source1:      https://github.com/microsoft/kata-containers/archive/refs/tags/kata-containers-cc-%{version}.tar.gz
Source2:      %{name}-%{version}-cargo.tar.gz
Source3:      mariner-coco-build-uvm.sh
Patch0:       keep-uvm-rootfs-dependencies.patch

ExclusiveArch: x86_64

BuildRequires:  golang
BuildRequires:  make
BuildRequires:  protobuf-compiler
BuildRequires:  dracut
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  git
BuildRequires:  sudo
BuildRequires:  perl-FindBin
BuildRequires:  perl-lib
BuildRequires:  libseccomp-devel
BuildRequires:  openssl-devel
BuildRequires:  clang
BuildRequires:  device-mapper-devel
BuildRequires:  cmake
BuildRequires:  fuse-devel
BuildRequires:  kernel-kvm-snp-devel
Requires:  kernel-kvm-snp
Requires:  moby-containerd-cc
Requires:  qemu-virtiofsd

%description
Kata Confidential Containers.

# This subpackage is used to build the uvm and therefore has dependencies on the kernel-uvm(-cvm) binaries
%package tools
Summary:        Kata CC tools package for building UVM components
Requires:       cargo
Requires:       qemu-img
Requires:       parted
Requires:       curl
Requires:       veritysetup
Requires:       opa >= 0.50.2
Requires:       kernel-kvm-snp

%description tools
This package contains the UVM osbuilder files

%prep
%autosetup -p1 -n %{name}-%{version}
pushd %{_builddir}/%{name}-%{version}
tar -xf %{SOURCE2}
popd

%build
export PATH=$PATH:"$(pwd)/go/bin"
export GOPATH="$(pwd)/go"
export OPENSSL_NO_VENDOR=1

# kata shim/runtime
pushd %{_builddir}/%{name}-%{version}/src/runtime
%make_build %{runtime_make_vars}
popd

# agent
pushd %{_builddir}/%{name}-%{version}/src/agent
%make_build %{agent_make_vars}
popd

# tardev snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter
make
chmod +x target/release/tardev-snapshotter
popd

# overlay
pushd %{_builddir}/%{name}-%{version}/src/overlay
cargo build --release
popd

# utarfs
pushd %{_builddir}/%{name}-%{version}/src/utarfs
cargo build --release
popd

# Build the guest kernel from kata-containers/tools/packaging/kernel utility
echo "Building guest kernel"
export PATH="$PATH:$GOPATH/bin"
pushd %{_builddir}/%{name}-%{version}/tools/packaging/kernel
echo "CONFIG_MODULES=y" >> configs/fragments/x86_64/snp/snp.conf
echo "CONFIG_MODULE_UNLOAD=y" >> configs/fragments/x86_64/snp/snp.conf
sed -i '/CONFIG_CRYPTO_FIPS/d' configs/fragments/common/crypto.conf
KATA_BUILD_CC=yes ./build-kernel.sh -a x86_64 -x snp setup
KATA_BUILD_CC=yes ./build-kernel.sh -a x86_64 -x snp build
sudo -E PATH="${PATH}" ./build-kernel.sh -x snp install
pushd $(ls | grep kata-linux)
GUESTKERNELDIR=$PWD
GUESTKERNELVERSION=$(cat include/config/kernel.release)
sudo -E PATH=$PATH make modules_install
popd
popd

# Build tarfs kernel modules
pushd %{_builddir}/%{name}-%{version}/src/tarfs
make KDIR=$GUESTKERNELDIR
make KDIR=$GUESTKERNELDIR install
popd
%global KERNEL_MODULES_DIR %{_builddir}/%{name}-%{version}/src/tarfs/_install/lib/modules/${GUESTKERNELVERSION}

%install
%define coco_path     /opt/confidential-containers
%define coco_bin      %{coco_path}/bin
%define defaults_kata %{coco_path}/share/defaults/kata-containers
%define share_kata    %{coco_path}/share/kata-containers
%define osbuilder     %{coco_path}/uvm

mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/scripts
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/initrd-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/image-builder
mkdir -p %{buildroot}%{osbuilder}/ci

# kernel modules
cp -aR %{KERNEL_MODULES_DIR} %{buildroot}%{osbuilder}

# osbuilder
pushd %{_builddir}/%{name}-%{version}
rm tools/osbuilder/.gitignore
rm tools/osbuilder/rootfs-builder/.gitignore

install -D -m 0755 %{SOURCE3}           %{buildroot}%{osbuilder}/mariner-coco-build-uvm.sh
install -D -m 0644 VERSION              %{buildroot}%{osbuilder}/VERSION
install -D -m 0644 ci/install_yq.sh     %{buildroot}%{osbuilder}/ci/install_yq.sh
install -D -m 0644 versions.yaml        %{buildroot}%{osbuilder}/versions.yaml
install -D -m 0644 tools/osbuilder/Makefile  %{buildroot}%{osbuilder}/tools/osbuilder/Makefile

sed -i 's#distro_config_dir="${script_dir}/${distro}#distro_config_dir="${script_dir}/cbl-mariner#g' tools/osbuilder/rootfs-builder/rootfs.sh
cp -aR tools/osbuilder/rootfs-builder   %{buildroot}%{osbuilder}/tools/osbuilder
cp -aR tools/osbuilder/initrd-builder   %{buildroot}%{osbuilder}/tools/osbuilder
cp -aR tools/osbuilder/scripts          %{buildroot}%{osbuilder}/tools/osbuilder
popd

mkdir -p %{buildroot}%{coco_bin}
mkdir -p %{buildroot}%{share_kata}
mkdir -p %{buildroot}%{coco_path}/libexec
mkdir -p %{buildroot}/etc/systemd/system/containerd.service.d/

ln -sf /usr/libexec/virtiofsd %{buildroot}/%{coco_path}/libexec/virtiofsd

find %{buildroot}/etc

# agent
pushd %{_builddir}/%{name}-%{version}/src/agent
mkdir -p %{buildroot}%{osbuilder}/src/agent/samples/policy
cp -aR samples/policy/all-allowed         %{buildroot}%{osbuilder}/src/agent/samples/policy
install -D -m 0755 kata-containers.target %{buildroot}%{osbuilder}/kata-containers.target
install -D -m 0755 kata-agent.service.in  %{buildroot}%{osbuilder}/kata-agent.service.in
install -D -m 0755 coco-opa.service       %{buildroot}%{osbuilder}/coco-opa.service
install -D -m 0755 target/x86_64-unknown-linux-gnu/release/kata-agent %{buildroot}%{osbuilder}/kata-agent
popd

# runtime/shim
pushd %{_builddir}/%{name}-%{version}/src/runtime
install -D -m 0755 containerd-shim-kata-v2 %{buildroot}/usr/local/bin/containerd-shim-kata-cc-v2
install -D -m 0755 kata-monitor %{buildroot}%{coco_bin}/kata-monitor
install -D -m 0755 kata-runtime %{buildroot}%{coco_bin}/kata-runtime
install -D -m 0755 data/kata-collect-data.sh %{buildroot}%{coco_bin}/kata-collect-data.sh

# Note: we deploy two configurations - the additional one is for policy/snapshotter testing w/o SEV SNP or IGVM
install -D -m 0644 config/configuration-qemu.toml %{buildroot}/%{defaults_kata}/configuration-clh.toml
install -D -m 0644 config/configuration-qemu.toml %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml

# adapt upstream config files
# change paths with locations specific to our distribution
sed -i 's/kernel = "\/usr\/share\/kata-containers\/vmlinux.container"/kernel = "\/usr\/share\/kata-containers\/vmlinuz-snp.container"/' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i "s|path = \"/usr/bin/qemu-system-x86_64\"|path = \"$current_directory/AMDSEV/usr/local/bin/qemu-system-x86_64\"|" %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^image = /# image = /' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^# initrd = /initrd = /' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^# confidential_guest = true/confidential_guest = true/' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^# sev_snp_guest = true/sev_snp_guest = true/' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i "s|valid_hypervisor_paths = \[\"/usr/bin/qemu-system-x86_64\"\]|valid_hypervisor_paths = [\"$current_directory/AMDSEV/usr/local/bin/qemu-system-x86_64\"]|" %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i "s|firmware = \"\"|firmware = \"$current_directory/AMDSEV/ovmf/Build/OvmfX64/DEBUG_GCC5/FV/OVMF.fd\"|" %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/shared_fs = "virtio-fs"/shared_fs = "virtio-9p"/' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^virtio_fs_daemon =/# virtio_fs_daemon =/' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^#disable_image_nvdimm = /disable_image_nvdimm = /' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^#file_mem_backend = ""/file_mem_backend = ""/' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's/^#disable_nesting_checks = true/disable_nesting_checks = true/'%{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
popd

# tardev-snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter/
sed -i -e 's/containerd.service/kubelet.service/g' tardev-snapshotter.service
install -m 0644 -D -t %{buildroot}%{_unitdir} tardev-snapshotter.service
install -D -m 0755 target/release/tardev-snapshotter  %{buildroot}/usr/bin/tardev-snapshotter
popd

# overlay
pushd %{_builddir}/%{name}-%{version}/src/overlay/
install -D -m 0755 target/release/kata-overlay  %{buildroot}/usr/bin/kata-overlay
popd

# utarfs
pushd %{_builddir}/%{name}-%{version}/src/utarfs/
install -D -m 0755 target/release/utarfs  %{buildroot}/usr/sbin/mount.tar
popd

install -D -m 0755 %{_builddir}/%{name}-%{version}/tools/osbuilder/image-builder/image_builder.sh   %{buildroot}%{osbuilder}/tools/osbuilder/image-builder/image_builder.sh
install -D -m 0755 %{_builddir}/%{name}-%{version}/tools/osbuilder/image-builder/nsdax.gpl.c        %{buildroot}%{osbuilder}/tools/osbuilder/image-builder/nsdax.gpl.c

%preun
%systemd_preun tardev-snapshotter.service

%postun
%systemd_postun tardev-snapshotter.service

%post
%systemd_post tardev-snapshotter.service

%files
%{share_kata}/vmlinux.container
%{coco_bin}/kata-collect-data.sh
%{coco_bin}/kata-monitor
%{coco_bin}/kata-runtime

%{defaults_kata}/configuration*.toml
%{coco_path}/libexec/virtiofsd

%{_bindir}/tardev-snapshotter
%{_bindir}/kata-overlay
%{_sbindir}/mount.tar
%{_unitdir}/tardev-snapshotter.service
%{_prefix}/local/bin/containerd-shim-kata-cc-v2

%license LICENSE
%doc CONTRIBUTING.md
%doc README.md

%files tools
%dir %{osbuilder}/src/agent/samples/policy/all-allowed
%{osbuilder}/src/agent/samples/policy/all-allowed/all-allowed.rego

%{osbuilder}/mariner-coco-build-uvm.sh
%{osbuilder}/kata-containers.target
%{osbuilder}/kata-agent.service.in
%{osbuilder}/coco-opa.service
%{osbuilder}/kata-agent
%{osbuilder}/ci/install_yq.sh

%{osbuilder}/VERSION
%{osbuilder}/versions.yaml

%dir %{osbuilder}/modules
%dir %{osbuilder}/tools
%{osbuilder}/modules/*
%{osbuilder}/tools/*

# remove some scripts we don't use
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/alpine
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/centos
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/clearlinux
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/debian
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/template
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/ubuntu

%changelog
* Mon Dec 18 2023 Archana Choudhary <archana1@microsoft.com> - 0.6.2-1
- Initial spec
