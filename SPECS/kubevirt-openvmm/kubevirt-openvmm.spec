#
# spec file for package kubevirt-openvmm
#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#

%define _missing_build_ids_terminate_build 0

%global sha 9f115538e7
%global msvm_version 26.0.37

Summary:        Container native virtualization
Name:           kubevirt-openvmm
Version:        0.1.0
Release:        4%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Management
URL:            https://github.com/microsoft/kubevirt
Source0:        https://github.com/microsoft/kubevirt/archive/refs/tags/build-%{sha}.tar.gz#/%{name}-%{sha}.tar.gz
%ifarch x86_64
Source1:        https://github.com/microsoft/mu_msvm/releases/download/v%{msvm_version}/firmware-RELEASE-X64-VS2022.tar.gz
Source2:        x64.json
Source3:        x64-confidential.json
%endif
# TODO: Remove the patch below when the following PR is merged:
# https://github.com/microsoft/kubevirt/pull/36
Patch0:         0001-Change-openvmm-binary-path-to-usr-bin-openvmm.patch

%global debug_package %{nil}
BuildRequires:  swtpm-tools
BuildRequires:  glibc-devel
BuildRequires:  glibc-static >= 2.38-21%{?dist}
BuildRequires:  golang >= 1.26
BuildRequires:  golang-packaging
BuildRequires:  pkgconfig
BuildRequires:  rsync
BuildRequires:  sed
BuildRequires:  pkgconfig(libnbd)
BuildRequires:  pkgconfig(libvirt)
ExclusiveArch:  x86_64 aarch64

%description
Kubevirt is a virtual machine management add-on for Kubernetes

%package        virtctl
Summary:        Client for managing kubevirt
Group:          System/Packages

%description    virtctl
The virtctl client is a command-line utility for managing container native virtualization resources

%package        virt-api
Summary:        Kubevirt API server
Group:          System/Packages

%description    virt-api
The virt-api package provides the kubernetes API extension for kubevirt

%package        container-disk
Summary:        Container disk for kubevirt
Group:          System/Packages

%description    container-disk
The containter-disk package provides a container disk functionality for kubevirt

%package        virt-controller
Summary:        Controller for kubevirt
Group:          System/Packages

%description    virt-controller
The virt-controller package provides a controller for kubevirt

%package        virt-exportproxy
Summary:        Export proxy for kubevirt
Group:          System/Packages

%description    virt-exportproxy
The virt-exportproxy package provides a proxy for kubevirt to pass
requests to virt-exportserver

%package        virt-exportserver
Summary:        Export server for kubevirt
Group:          System/Packages

%description    virt-exportserver
The virt-exportserver package provides an http server for kubevirt to
serve the data of VirtualMachineExport resource in different formats

%package        virt-handler
Summary:        Handler component for kubevirt
Group:          System/Packages

%description    virt-handler
The virt-handler package provides a handler for kubevirt

%package        virt-launcher
Summary:        Launcher component for kubevirt
Group:          System/Packages
# Starting from v1.1.0, KubeVirt ships /usr/bin/virt-tail which conflicts with
# the respective guestfs tool.
Conflicts:      guestfs-tools

%description    virt-launcher
The virt-launcher package provides a launcher for kubevirt

%package        virt-operator
Summary:        Operator component for kubevirt
Group:          System/Packages

%description    virt-operator
The virt-opertor package provides an operator for kubevirt CRD

%package        pr-helper-conf
Summary:        Configuration files for persistent reservation helper
Group:          System/Packages

%description    pr-helper-conf
The pr-helper-conf package provides configuration files for persistent
reservation helper

%package        sidecar-shim
Summary:        Sidecar shim for kubevirt hook sidecars
Group:          System/Packages

%description    sidecar-shim
The sidecar-shim package provides the sidecar shim binary for kubevirt.
It handles gRPC communication between hook sidecars and the main
virt-launcher container, allowing custom modifications to VM definitions.

%package        tests
Summary:        Kubevirt functional tests
Group:          System/Packages

%description    tests
The package provides Kubevirt end-to-end tests.

%prep
%autosetup -p1 -n kubevirt-build-%{sha}

%build
mkdir -p go/src/kubevirt.io go/pkg
ln -s ../../../ go/src/kubevirt.io/kubevirt
export GOPATH=${PWD}/go
export GOFLAGS="-buildmode=pie"
cd ${GOPATH}/src/kubevirt.io/kubevirt
env \
KUBEVIRT_GO_BASE_PKGDIR="${GOPATH}/pkg" \
KUBEVIRT_VERSION=%{version} \
KUBEVIRT_SOURCE_DATE_EPOCH="$(date -r LICENSE +%s)" \
KUBEVIRT_GIT_COMMIT='%{sha}' \
KUBEVIRT_GIT_VERSION='v%{version}' \
KUBEVIRT_GIT_TREE_STATE="clean" \
build_tests="true" \
./hack/build-go.sh install \
    cmd/virt-api \
    cmd/virt-chroot \
    cmd/virt-controller \
    cmd/virt-exportproxy \
    cmd/virt-exportserver \
    cmd/virt-freezer \
    cmd/virt-handler \
    cmd/virt-launcher \
    cmd/virt-launcher-monitor \
    cmd/virt-operator \
    cmd/virt-probe \
    cmd/virt-tail \
    cmd/virtctl \
    cmd/sidecars \
    %{nil}

env DOCKER_PREFIX=$reg_path DOCKER_TAG=%{version}-%{release} KUBEVIRT_NO_BAZEL=true ./hack/build-manifests.sh

%install
mkdir -p %{buildroot}%{_bindir}

install -p -m 0755 _out/cmd/container-disk-v2alpha/container-disk %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virtctl/virtctl %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-api/virt-api %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-controller/virt-controller %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-chroot/virt-chroot %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-exportproxy/virt-exportproxy %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-exportserver/virt-exportserver %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-handler/virt-handler %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-launcher/virt-launcher %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-launcher-monitor/virt-launcher-monitor %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-freezer/virt-freezer %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-probe/virt-probe %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-tail/virt-tail %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-operator/virt-operator %{buildroot}%{_bindir}/
install -p -m 0755 _out/tests/tests.test %{buildroot}%{_bindir}/virt-tests
install -p -m 0755 cmd/virt-launcher/node-labeller/node-labeller.sh %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/sidecars/sidecars %{buildroot}%{_bindir}/sidecar-shim

# Install network stuff
mkdir -p %{buildroot}%{_datadir}/kube-virt/virt-handler
install -p -m 0644 cmd/virt-handler/nsswitch.conf %{buildroot}%{_datadir}/kube-virt/virt-handler/

# Persistent reservation helper configuration files
mkdir -p %{buildroot}%{_datadir}/kube-virt/pr-helper
install -p -m 0644 cmd/pr-helper/multipath.conf %{buildroot}%{_datadir}/kube-virt/pr-helper/

# Configuration files for libvirt
mkdir -p %{buildroot}%{_datadir}/kube-virt/virt-launcher
install -p -m 0644 cmd/virt-launcher/virtqemud.conf %{buildroot}%{_datadir}/kube-virt/virt-launcher
install -p -m 0644 cmd/virt-launcher/qemu.conf %{buildroot}%{_datadir}/kube-virt/virt-launcher

# Temporary OpenVMM firmware and UEFI templates until their long-term
# packaging design is implemented.
%ifarch x86_64
mkdir -p %{buildroot}/openvmm
tar -xOf %{SOURCE1} ./FV/MSVM.fd > %{buildroot}/openvmm/MSVM.fd
chmod 0644 %{buildroot}/openvmm/MSVM.fd
install -D -p -m 0644 %{SOURCE2} %{buildroot}/openvmm/uefi-templates/x64.json
install -D -p -m 0644 %{SOURCE3} %{buildroot}/openvmm/uefi-templates/x64-confidential.json
%endif

%files virtctl
%license LICENSE
%doc README.md
%{_bindir}/virtctl

%files virt-api
%license LICENSE
%doc README.md
%{_bindir}/virt-api

%files container-disk
%license LICENSE
%doc README.md
%{_bindir}/container-disk

%files virt-controller
%license LICENSE
%doc README.md
%{_bindir}/virt-controller

%files virt-exportproxy
%license LICENSE
%doc README.md
%{_bindir}/virt-exportproxy

%files virt-exportserver
%license LICENSE
%doc README.md
%{_bindir}/virt-exportserver

%files virt-handler
%license LICENSE
%doc README.md
%dir %{_datadir}/kube-virt
%{_datadir}/kube-virt/virt-handler
%{_bindir}/virt-handler
%{_bindir}/virt-chroot

%files virt-launcher
%license LICENSE
%doc README.md
%dir %{_datadir}/kube-virt
%dir %{_datadir}/kube-virt/virt-launcher
%{_bindir}/virt-launcher
%{_bindir}/virt-launcher-monitor
%{_bindir}/virt-freezer
%{_bindir}/virt-probe
%{_bindir}/virt-tail
%{_bindir}/node-labeller.sh
%{_datadir}/kube-virt/virt-launcher
%ifarch x86_64
%dir /openvmm
/openvmm/MSVM.fd
%dir /openvmm/uefi-templates
/openvmm/uefi-templates/x64.json
/openvmm/uefi-templates/x64-confidential.json
%endif

%files virt-operator
%license LICENSE
%doc README.md
%{_bindir}/virt-operator

%files pr-helper-conf
%license LICENSE
%doc README.md
%dir %{_datadir}/kube-virt
%dir %{_datadir}/kube-virt/pr-helper
%{_datadir}/kube-virt/pr-helper/multipath.conf

%files sidecar-shim
%license LICENSE
%doc README.md
%{_bindir}/sidecar-shim

%files tests
%license LICENSE
%doc README.md
%dir %{_datadir}/kube-virt
%{_bindir}/virt-tests

%changelog
* Wed Oct 07 2026 Harshit Gupta <guptaharshit@microsoft.com> - 0.1.0-4
- Remove -N from autosetup command so that patches can be applied

* Wed Oct 07 2026 Harshit Gupta <guptaharshit@microsoft.com> - 0.1.0-3
- Add temporary x86 OpenVMM firmware and UEFI templates

* Tue Oct 06 2026 Harshit Gupta <guptaharshit@microsoft.com> - 0.1.0-2
- Add patch to update OpenVMM binary path to what openvmm RPM installs

* Tue Oct 06 2026 Microsoft Corporation <linux@microsoft.com> - 0.1.0-1
- Original version for Azure Linux
