#
# spec file for package kubevirt
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global debug_package %{nil}
Summary:        Container native virtualization
Name:           kubevirt
Version:        0.51.0
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Management
URL:            https://github.com/kubevirt/kubevirt
#Source0:       https://github.com/kubevirt/kubevirt/archive/refs/tags/v0.51.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        disks-images-provider.yaml
BuildRequires:  glibc-devel
BuildRequires:  golang
BuildRequires:  golang-packaging
BuildRequires:  pkg-config
BuildRequires:  rsync
BuildRequires:  sed
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

%package        virt-handler
Summary:        Handler component for kubevirt
Group:          System/Packages

%description    virt-handler
The virt-handler package provides a handler for kubevirt

%package        virt-launcher
Summary:        Launcher component for kubevirt
Group:          System/Packages

%description    virt-launcher
The virt-launcher package provides a launcher for kubevirt

%package        virt-operator
Summary:        Operator component for kubevirt
Group:          System/Packages

%description    virt-operator
The virt-opertor package provides an operator for kubevirt CRD

%package        tests
Summary:        Kubevirt functional tests
Group:          System/Packages

%description    tests
The package provides Kubevirt end-to-end tests.

%prep
%autosetup -p1

%build
export GOFLAGS="-buildmode=pie"
KUBEVIRT_VERSION=%{version} \
KUBEVIRT_SOURCE_DATE_EPOCH="$(date -r LICENSE +%{s})" \
KUBEVIRT_GIT_COMMIT='v%{version}' \
KUBEVIRT_GIT_VERSION='v%{version}' \
KUBEVIRT_GIT_TREE_STATE="clean" \
build_tests="true" \
./hack/build-go.sh install \
    cmd/virt-api \
    cmd/virt-chroot \
    cmd/virt-controller \
    cmd/virt-freezer \
    cmd/virt-handler \
    cmd/virt-launcher \
    cmd/virt-operator \
    cmd/virt-probe \
    cmd/virtctl \
    %{nil}

%install
mkdir -p %{buildroot}%{_bindir}

install -p -m 0755 _out/cmd/container-disk-v2alpha/container-disk %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virtctl/virtctl %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-api/virt-api %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-controller/virt-controller %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-chroot/virt-chroot %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-handler/virt-handler %{buildroot}%{_bindir}/
install -p -m 0555 _out/cmd/virt-launcher/virt-launcher %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-freezer/virt-freezer %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-probe/virt-probe %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-operator/virt-operator %{buildroot}%{_bindir}/
install -p -m 0755 _out/tests/tests.test %{buildroot}%{_bindir}/virt-tests
install -p -m 0755 cmd/virt-launcher/node-labeller/node-labeller.sh %{buildroot}%{_bindir}/

# virt-launcher configurations
install -p -m 0644 cmd/virt-launcher/qemu.conf %{buildroot}%{_datadir}/
install -p -m 0644 cmd/virt-launcher/libvirtd.conf %{buildroot}%{_datadir}/
install -p -m 0644 cmd/virt-launcher/nsswitch.conf %{buildroot}%{_datadir}/


# virt-launcher SELinux policy needs to land in virt-handler container
install -p -m 0644 cmd/virt-handler/virt_launcher.cil %{buildroot}/

# Install network stuff
mkdir -p %{buildroot}%{_datadir}/kube-virt/virt-handler
install -p -m 0644 cmd/virt-handler/nsswitch.conf %{buildroot}%{_datadir}/kube-virt/virt-handler/
install -p -m 0644 cmd/virt-handler/ipv4-nat.nft %{buildroot}%{_datadir}/kube-virt/virt-handler/
install -p -m 0644 cmd/virt-handler/ipv6-nat.nft %{buildroot}%{_datadir}/kube-virt/virt-handler/

%files -n kubevirt

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

%files virt-handler
%license LICENSE
%doc README.md
%dir %{_datadir}/kube-virt
%dir %{_datadir}/kube-virt/virt-handler
%{_bindir}/virt-handler
%{_bindir}/virt-chroot
%{_datadir}/kube-virt/virt-handler
/virt_launcher.cil

%files virt-launcher
%license LICENSE
%doc README.md
%{_bindir}/virt-launcher
%{_bindir}/virt-freezer
%{_bindir}/virt-probe
%{_bindir}/node-labeller.sh
%{_datadir}/qemu.conf
%{_datadir}/libvirtd.conf
%{_datadir}/nsswitch.conf

%files virt-operator
%license LICENSE
%doc README.md
%{_bindir}/virt-operator

%files tests
%license LICENSE
%doc README.md
%dir %{_datadir}/kube-virt
%{_bindir}/virt-tests

%changelog
#FIXME: First changelog entry header failed to parse
* Thu Jul 14 2022 Kanika Nema <kanikanema@microsoft.com> 0.51.0
- Initial CBL-Mariner import from openSUSE (license: same as "License" tag)
- Initial changes to build for Mariner
- License verified
* Thu Jan 01 1970  <> - --1

