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


Summary:        Container native virtualization
Name:           kubevirt
Version:        0.59.0
Release:        12%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Management
URL:            https://github.com/kubevirt/kubevirt
Source0:        https://github.com/kubevirt/kubevirt/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        disks-images-provider.yaml
# Nexus team needs these to-be-upstreamed patches for the operator Edge to work
# correctly.
Patch0:         Cleanup-housekeeping-cgroup-on-vm-del.patch
Patch1:         Allocate-2-cpu-for-the-emulator-thread.patch
Patch2:         Hotplug_detach_grace_period.patch
%global debug_package %{nil}
BuildRequires:  glibc-devel
BuildRequires:  glibc-static >= 2.38-1%{?dist}
BuildRequires:  golang
BuildRequires:  golang-packaging
BuildRequires:  pkgconfig
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
export GOFLAGS+=" -buildmode=pie"
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
    cmd/virt-launcher-monitor \
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
install -p -m 0555 _out/cmd/virt-launcher-monitor/virt-launcher-monitor %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-freezer/virt-freezer %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-probe/virt-probe %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/virt-operator/virt-operator %{buildroot}%{_bindir}/
install -p -m 0755 _out/tests/tests.test %{buildroot}%{_bindir}/virt-tests
install -p -m 0755 cmd/virt-launcher/node-labeller/node-labeller.sh %{buildroot}%{_bindir}/

# virt-launcher configurations
mkdir -p %{buildroot}%{_datadir}/kube-virt/virt-launcher
install -p -m 0644 cmd/virt-launcher/qemu.conf %{buildroot}%{_datadir}/kube-virt/virt-launcher/
install -p -m 0644 cmd/virt-launcher/virtqemud.conf %{buildroot}%{_datadir}/kube-virt/virt-launcher/
install -p -m 0644 cmd/virt-launcher/nsswitch.conf %{buildroot}%{_datadir}/kube-virt/virt-launcher/


# virt-launcher SELinux policy needs to land in virt-handler container
install -p -m 0644 cmd/virt-handler/virt_launcher.cil %{buildroot}/

# Install network stuff
mkdir -p %{buildroot}%{_datadir}/kube-virt/virt-handler
install -p -m 0644 cmd/virt-handler/nsswitch.conf %{buildroot}%{_datadir}/kube-virt/virt-handler/

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
%dir %{_datadir}/kube-virt
%dir %{_datadir}/kube-virt/virt-launcher
%{_bindir}/virt-launcher
%{_bindir}/virt-launcher-monitor
%{_bindir}/virt-freezer
%{_bindir}/virt-probe
%{_bindir}/node-labeller.sh
%{_datadir}/kube-virt/virt-launcher

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
* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> - 0.59.0-11
- Bump release to rebuild against glibc 2.35-6

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.59.0-10
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.59.0-9
- Bump release to rebuild with updated version of Go.

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.59.0-8
- Bump release to rebuild against glibc 2.35-5

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.59.0-7
- Bump release to rebuild with go 1.19.12

* Wed Jul 14 2023 Andrew Phelps <anphel@microsoft.com> - 0.59.0-6
- Bump release to rebuild against glibc 2.35-4

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.59.0-5
- Bump release to rebuild with go 1.19.11

* Fri Jun 30 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 0.59.0-4
- Patch 0.59.0 with Operator Nexus patch for hotplug volume detachment IO errors

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.59.0-3
- Bump release to rebuild with go 1.19.10

* Fri May 12 2023 Kanika Nema <kanikanema@microsoft.com> - 0.59.0-2
- Patch 0.59.0 with Operator Nexus patches 

* Fri May 05 2023 Kanika Nema <kanikanema@microsoft.com> - 0.59.0-1
- Upgrade to v0.59.0 

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.58.0-7
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.58.0-6
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.58.0-5
- Bump release to rebuild with go 1.19.6

* Mon Feb 13 2023 Kanika Nema <kanikanema@microsoft.com> - 0.58.0-4
- Add an upstream patch (from v0.59.0-alpha2) without which virt-handler
  containers don't start.

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.58.0-3
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.58.0-2
- Bump release to rebuild with go 1.19.4

* Mon Dec 26 2022 Kanika Nema <kanikanema@microsoft.com> - 0.58.0-1
- Upgrade to 0.58.0
- Build new component virt-launcher-monitor.

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.55.1-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.55.1-3
- Adding missing "%{?dist}" to "glibc-static" BR.

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.55.1-2
- Bump release to rebuild with go 1.18.8

* Thu Sep 22 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.55.1-1
- Upgrade to 0.55.1

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.51.0-2
- Bump release to rebuild against Go 1.18.5

* Thu Jul 14 2022 Kanika Nema <kanikanema@microsoft.com> - 0.51.0-1
- License verified
- Initial changes to build for Mariner
- Initial CBL-Mariner import from openSUSE TumbleWeed (license: same as "License" tag)

* Thu Mar 10 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.51.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.51.0

* Fri Feb 11 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.50.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.50.0

* Wed Jan 19 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Pack nft rules and nsswitch.conf for virt-handler
- Drop kubevirt-psp-caasp.yaml and cleanup the spec

* Wed Jan 12 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.49.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.49.0
  Includes the fix for CVE-2021-43565 (bsc#1193930)

* Thu Dec 16 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.48.1
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.48.1

* Fri Dec  3 2021 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Enable build on aarch64

* Fri Nov 26 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Detect SLE15 SP4 build environment

* Fri Nov 12 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.47.1
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.47.1

* Tue Oct 19 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Pack only kubevirt-{operator,cr}.yaml into manifests
- Include manifests/testing/* into tests package
- Use disks-images-provider.yaml from upstream

* Mon Oct 11 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.46.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.46.0
- Drop upstreamed patch 0001-Specify-format-of-the-backing-image.patch

* Thu Sep  9 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.45.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.45.0

* Fri Aug 27 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Fix issue with recent qemu-img
  0001-Specify-format-of-the-backing-image.patch

* Fri Aug 27 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.44.1
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.44.1

* Mon Aug  9 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.44.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.44.0

* Mon Jul 12 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Drop upstreamed patch 0002-Don-t-use-Bazel-in-build-manifests.sh.patch
- Install node-labeller.sh in %%{_bindir}
- Update to version 0.43.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.43.0

* Wed Jun 30 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Generate meta info for containers during rpm build

* Wed Jun  9 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Use registry.suse.com as the default fallback for sle
- Rename macro registry_path to kubevirt_registry_path
- Switch to golang 1.16
- Drop 0001-Don-t-build-virtctl-for-darwin-and-windows.patch
- Drop --skipj2 arg for build-manifests.sh
- Update to version 0.42.1
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.42.1

* Fri Jun  4 2021 Fabian Vogt <fvogt@suse.com>
- Also specify the registry in kubevirt_containers_meta

* Thu May 20 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Use git format-patch:
  0001-Don-t-build-virtctl-for-darwin-and-windows.patch
  0002-Don-t-use-Bazel-in-build-manifests.sh.patch
- Drop patches:
  dont-build-virtctl-darwin.patch
  dont-use-bazel-in-build-manifests.patch
  fix-double-free-of-VirDomain.patch

* Thu May 20 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.41.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.41.0

* Tue May 18 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Drop fix-virsh-domcapabilities-error.patch (bsc#1185119)

* Mon May 17 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Do not package OLM manifests

* Thu May  6 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Install virt-launcher SELinux policy (bsc#1185714)

* Thu Apr 29 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Include release number into docker tag
- Add kubevirt_containers_meta build service

* Thu Apr 29 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Set default reg_path='registry.opensuse.org/kubevirt'
- Add _constraints file with disk requirements

* Fri Apr 23 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Fix virt-launcher crash
  fix-double-free-of-VirDomain.patch

* Tue Apr 20 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Fix issue when calling `virsh-domcapabilities`
  fix-virsh-domcapabilities-error.patch

* Tue Apr 20 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Package node-labeller.sh along with virt-launcher

* Mon Apr 19 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 0.40.0
  Release notes https://github.com/kubevirt/kubevirt/releases/tag/v0.40.0

* Mon Apr 19 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Disable changelog generation via tar_scm service (too verbose)

* Thu Apr 15 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Drop csv-generator

* Wed Apr  7 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update registry path

* Wed Mar  3 2021 vasily.ulyanov@suse.com
- Update to version 0.38.1:
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../kubevirt/WORKSPACE -dry-run=false
  * Expose field name 'ipFamily' for k8s < 1.20
  * Bump k8s deps to 0.20.2
  * verify that VMIs can be started with images not owned by qemu provided by FS PVC
  * change ownership of the image provided by a filesystem PVC to qemu
  * virt-launcher's FSGroup functional test is obsolete
  * virt-controller: Remove FSGroup from Pod
  * cloudinit.GenerateLocalData: defer removal of temp files
  * rpm: update `make rpm-deps`
  * launcher / handler rpm: add tar as pod dependency
  * cloudinit.GenerateLocalData: drop ineffectual assignment
  * tests/config_test: fix ineffectual assignment to err
  * pkg/virt-handler/migration-proxy/migration-proxy_test: fix ineffectual assignment to err
  * tests/replicaset_test: fix ineffectual assignment to err
  * pkg/virt-launcher/virtwrap/access-credentials/access_credentials_test: fix ineffectual assignment to err
  * tests/vnc_test: fix ineffectual assignment to err
  * pkg/virt-handler/isolation/isolation_test: fix ineffectual assignment to err
  * pkg/virt-controller/watch/migration: fix ineffectual assignment to err
  * tools/vms-generator/utils/utils: fix ineffectual assignment to err
  * tests/vmi_gpu_test: fix ineffectual assignment to err
  * pkg/virt-handler/cache/cache_test:fix ineffectual assignment to err
  * pkg/virt-launcher/virtwrap/manager_test:fix ineffectual assignment to err
  * multus, tests: assert error does not happen
  * Bump bazeldnf to v0.0.15
  * pkg/virt-handler/cmd-client/client_test:fix ineffectual assignment to err
  * pkg/virt-operator/creation/components/secrets_test: fix ineffectual assignment to err
  * tests/infra_test.go: fix ineffectual assignment to err
  * tests/vmipreset_test: fix ineffectual assignment to err
  * func tests, multus: getting the kubevirtClient must be done first
  * func tests, multus: execute BeforeAll before BeforeEach
  * document the interface between hostdev device plugins and kubevirt
  * Refactor methods to reduce their Cognitive Complexity
  * Define a constant instead of duplicating literal
  * Refactor method to reduce its Cognitive Complexity
  * Define a constant instead of duplicating literals
  * Refactor method to reduce its Cognitive Complexity
  * Add a nested comment indicating about an empty function
  * Define a constant instead of duplicating a literal
  * Refactor methods to reduce their Cognitive Complexity
  * Increase subresource pod test execution timeout
  * Add Nvidia as a KubeVirt ADOPTOR
  * ipv4, network tests: refactor the masquerade test table
  * controller, virtinformers: Define the unexpected error once
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../kubevirt/WORKSPACE -dry-run=false
  * Converter: Handle 'float' memory
  * Tests: Ensure cpu/memory in requests/limits allow int/float
  * virt-launcher: Support (non-)transitional virtio-balloon
  * rpm: Bump libvirt and QEMU
  * tests/utils: fix ineffectual assignment to ok
  * tests/utils: fix ineffectual assignment to err
  * tests/utils: fix ineffectual assignment to scale
  * pkg/container-disk/container-disk_test: fix ineffectual assignment to path
  * pkg/virt-launcher/virtwrap/network/common: fix ineffectual assignment to err
  * tests/vm_test: fix ineffectual assignment to err
  * tests/vm_watch_test: fix ineffectual assignment to cmdName
  * pkg/virt-handler/hotplug-disk/mount_test: fix ineffectual assignment to err
  * pkg/virt-handler/hotplug-disk/mount_test: fix ineffectual assignment to res
  * tests/reporter/kubernetes: fix ineffectual assignment to err
  * pkg/virt-launcher/virtwrap/access-credentials: fix ineffectual assignment to err
  * pkg/virt-launcher/virtwrap/access-credentials: fix ineffectual assignment to output
  * pkg/virt-handler/vm_test: fix ineffectual assignment to err
  * tools/util/marshaller: fix ineffectual assignment to err
  * pkg/virt-handler/device-manager/mediated_device_test: fix ineffectual assignment to err
  * tests/restore_test: fix ineffectual assignment to restore
  * removing trello reference as its no longer used
  * Adjust e2e test which checks for the scsi controller
  * consider scsi controllers in virtio version decisions
  * Bump kubevirtci, now hosted on quay.io
  * network: BindMechanism receiver name consistency
  * MacvtapBindMechanism.loadCachedInterface fix arg name
  * Clean error message for not migratable VMI
  * Fix detection of previous release version in operator func test
  * Alert when less than 2 KVM nodes available
  * Fix a datavolume collision
  * Remove danielBelenky from reviewers
  * KubeVirt is now released on quay.io only
  * [virt-operator] load new certificates earlier
  * Keepalive function for travis to prevent timeout due to inactivity on stdout
  * Fix limits/requests to accept int again
  * network: rename NetworkInterface and PodInterface
  * network: drop NetworkInterface.Unplug
  * network: eliminate mocking of SetupPodNetworkPhase2
  * network: make SetupPodNetworkPhase1 into a constant function
  * network: rename {Bridge,Masquerade,Macvtap,Slirp}PodInterface
  * network: rename getNetworkClass
  * network: rename getNetworkInterfaceFactory
  * fix review English phrasing
  * virt-api/webhooks: test newly-renamed function
  * virt-api/webhooks: simplify and rename ServiceAccount-matching function
  * split sync resources into multiple functions and files
  * tests: Test guest restart after migration
  * Normalize DNS search domains to lower-case
  * Revert "Fix typos in log output"
  * tests: After migration test is not invoked
  * virt-launcher: [masquerade] pass a MAC to the vm accroding to the spec only
  * virt-launcher: [masquerade] Stop filtering dhcp reuqests by vm MAC
  * Example code for gosec fix
  * Update gosec.md
  * guidelines for using gosec analysis tool
  * docs/devel/networking: unbreak URL
  * Add virtctl image-upload usage for WaitForFirstConsumer DVs
  * Add error message on virtctl image-upload to WaitForFirstConsumer DataVolume
  * bump bazeldnf
  * Fix typos in log output
  * Extend isolation test to cover IsMounted method
  * Wrap mountinfo parsing common code into a function
  * start virt-launchers with a non-default log verbosity
  * change virt-controller log verbosity on relevant config changes
  * change virt-api log verbosity on relevant config changes
  * change virt-handlers log verbosity on relevant config changes
  * add default log verbosity values to cluster config
  * allow registering multiple callbacks for config changes
  * add a logVerbosity struct to set KubeVirt components log verbosity
  * Remove travis-ci logic for pushing to quay app registery
  * Make mutating webhooks required
  * Bump bazeldnf to a version with its own ldd implementation
  * Add tests
  * Fix typo
  * Fix some typo in docs
  * Add alert for insufficient number of nodes with KVM resources
  * Remove dockerhub-related travis jobs and credentials
  * Make `make build-functest` work without nested bazel invocation
  * Compile template-manifestor with bazel
  * Invoke shfmt from bazel
  * Add gofmt to our vendor tree
  * kubevirtci, Bump kubevirtci
  * Bump bazeldnf to 0.0.10 to better deal with bad repomd mirrors
  * Allow setting user local bazelrc settings.
  * Update Quay credentials in travis config
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../kubevirt/WORKSPACE -dry-run=false
  * tests: make client in hello world job UDP wait for response
  * wait for host responding to ping, in some cases the first two pings fail, now instead we wait for a specific amount of time
  * Increase time to wait for failed connection
  * virt-controller: increase the number of VMI controller threads
  * sriov, tests: xfail vlan test
  * network: simplify getNetworkInterfaceFactory
  * network: drop long-unused plugFunction
  * network: drop long-unused qemuArgCacheFile
  * network: rename constant to primaryPodInterfaceName
  * network: drop global podInterfaceName variable
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../kubevirt/WORKSPACE -dry-run=false
  * add vi-minimal to base packages for containers
  * Additional hotplug functional tests
  * Add unit test for PCI address parsing
  * Escape dot '\.' in PCI_ADDRESS_PATTERN
  * Move ParsePciAddress function to hardware utils
  * Bump bazeldnf to fix rpm verification
  * Drop references to kubevirt-host-device-plugin-config cfgMap
  * Check if block devices are ready. If not ensure that the block device major and minor is allowed in the virt-launcher pod. Enable functional tests that were failing due to permission issues
  * Reviewers update: Adding EdDev as a code reviewer
  * virt-launcher/handler: move Macvtap discovery of MTU and target
  * virt-launcher/handler: Macvtap shouldn't use vif cache
  * Fix Open Shift SCC permissions to allow attachment pods to use host network. Fix selinux to be on container level instead of pod level.
  * Use the array value instead of a new variable when possible
  * eliminate the usage of interface address in decorateConfig()
  * allocate new variable and don't use the originsl s.domain.Spec.Devices.Interfaces
  * fix some tabs/spaces mess
  * Fix memory aliasing in for loop - taking the address of loop variable is dangerous
  * ENV VAR for client-go scheme registration version
  * Give kubevirt pods more time to become ready
  * Fix PV selector for windos and rhel PVCs
  * Make storage tests fit for parallel execution
  * Use the new nfsserver library in the migration tests
  * Create windows and rhel PV within the corresponding tests
  * Prepare our framework in utils for parallel storage test execution
  * Move nfs server rendering to its own package and adjust memory requests
  * Add a ginkgo matcher library especially for kubevirt
  * Prepare image provider for parallel execution
  * Code Review edits
  * Bump kubevirtci
  * Stick with virtio model on the ballooning device
  * Tablet input device only exists as virtio 1.0
  * virtio-serial controllers need the model set too
  * Add virtio-transitional e2e test
  * Extract converter into its own subpackage
  * Unit test for choosing virtio-transitional
  * Make the converter aware of virtio model preferences
  * Add a global VMI flag to the API to fall back to virtio_transitional
  * tests, xfail: Change XFail API to wrap the expected failure
  * Don't override the e2e kubevirt config by default in the e2e tests
  * virt-launcher/handler: remove the tap device from the VIF cache
  * Use virt-handler image as base for multus tests
  * Explicitly build libvirt-devel tars
  * Remove no longer needed go_library definition
  * Allow qemu to bind to privileged ports for slirp
  * Docuement how RPM verification can be done
  * Add a RPM verification target
  * Bump to bazeldnf with improved RPM verification
  * fix logos dependency
  * Add GPG keys to repo.yaml
  * Update RPMs
  * Avoid dependency flipping
  * add ps binary
  * Update dependency update documentation
  * Remove old libvirt-devel dependencies in WORKSPACE
  * Prepare binary containers for bazeldnf built content
  * Start using bazeldnf RPMs for building and testing
  * Add RPMs
  * Add repo.yaml files
  * Add a script to resolve RPM dependencies
  * Document new kubevirt handling of WaitForFirstConsumer DataVolumes
  * Fix support for camelCase userData and networkData labels
  * virt-launcher: Remove unused arg from GetDomainSpecWithRuntimeInfo
  * Extend VMI count metric to include osinfo
  * fix: change url and label name for "good-first-issue" on CONTRIBUTING.md
  Added patch: dont-use-bazel-in-build-manifests.patch

* Mon Feb 15 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Add building of virt-tests

* Wed Jan 20 2021 jfehlig@suse.com
- Update to version 0.37.0:
  * Remove travis-ci logic for pushing to quay app registery
  * Update Quay credentials in travis config
  * MacvtapPodInterface.setCachedInterface: fix arg name
  * make generate: 2021 edition
  * tests, dhcpv6: verify connectivity survives after migration
  * tests, dhcpv6: use python server instead of nc
  * tests, dhcpv6: start dhcpv6 client, config d.route & prefix via console
  * tests, dhcpv6: use fedora vms for masquerade ipv6 connectiviy tests
  * tests: split masquerade connectivity tests to ipv4 and ipv6
  * tests: remove libnet.WithIPv6 from ipv4 only dhcp test
  * dhcpv6: unit tests
  * dhcpv6: Extracting the build of the server response to a separate method
  * dhcpv6: Add the request iana to the response
  * dhcpv6: reply to dhcp solict with rapid commit
  * add ipv6 address to VIF.String
  * dhcpv6: run only for masquerade
  * dhcpv6: introduce prepareDHCPv6Modifiers
  * dhcpv6: Allow dhcpv6 server to run without CAP_NET_RAW
  * dhcpv6: handle requests from client - adding DUID and IANA options
  * virt-launcher: vendor dhcpv6
  * virt-launcher: introduce dhcpv6
  * Extend version functional tests
  * Set --stamp as default build flag
  * imageupload: improve nosec comment
  * cloud-init: test that GenerateLocalData can run twice
  * cloud-init, GenerateLocalData: simplify staging replacement
  * tests, ping: increase default amount of packets
  * cloud-init, GenerateLocalData: drop redundant diskutils.RemoveFile call
  * cloud-init, GenerateLocalData: drop ambiguous comment
  * add use case Signed-off-by: xiaobo <zeng.xiaobo@h3c.com>
  * add use case Signed-off-by: xiaobo <zeng.xiaobo@h3c.com>
  * add use case Signed-off-by: xiaobo <zeng.xiaobo@h3c.com>
  * add use case Signed-off-by: xiaobo <zeng.xiaobo@h3c.com>
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../kubevirt/WORKSPACE -dry-run=false
  * Document dependency update flows
  * Newer curl version don't allow headerless HTTP
  * Build all test images in kubervirt/kubevirt
  * Add managed RPMs and remove unmanaged RPMs
  * Add repo.yaml files
  * Add bazeldnf dependencies
  * Add a script to resolve RPM dependencies
  * virt-launcher, converter: Extract SRIOV hostdev creation
  * virt-launcher, converter: Refactor network indexing
  * virt-launcher, converter: Refactor iface multi queue
  * tests, vmi_multus: test Sriov with Vlan
  * Don't overwrite user-provided GOFLAGS
  * Handle btrfs subvolumes when parsing mountinfo
  * Add mount info test cases
  * Add testdata for mount info tests
  * Cleanup duplicated code
  * Refactor containerdisk mount code
  * tests,sriov:make createSriovVms recieve network names
  * tests, sriov: remove un-needed function.
  * tests: sriov: extract NAD creation to a helper
  * tests, utils, delete vmi waiting: assert on err
  * Preapre build environment for bazeldnf
  * use placement api for assinging virt-handler pod
  * virt-launcher, libvirt: Free (all) domain resources
  * Generate release manifests using quay images
  * Add maiqueb to code-reviewers list
  * Update vendored dependencies
  * Update versions of some dependencies
  * only validate status of vm, vmi, and vmi migration objects
  * This fixes a race condition between unmounting a file system volume and detaching a disk from the running VM. In certain conditions it would attempt to unmount before the disk was fully detached causing the unmount to error and preventing the VM sync from fully detaching. This moves the unmount to after the sync, so this race never happens.
  * smbios, sidecar hook, tests: assert the hook version is advertised
  * smbios cmd: set the version parameter as mandatory
  * examples, hooks: correct the vmi-sidecar-hook example
  * add kubernetes os nodeSelector to injectPlacementMetadata
  * virt-launcher, converter: Set SRIOV device as unmanaged
  * tests, sriov: XFail IPv4 connectivity test
  * Append rootfs mount to containerdisk base path
  * Narrow down watcher select which waits for object states
  * Fix Eventually which used the time out as description
  * Remove unused functions: GenerateSelfSignedCertKey and GenerateSelfSignedCertKeyWithFixtures
  * use filepath.Clean for two fixed path parameter functions
  * virt-launcher, converter: Remove vCPU dependency on queue limits
  * add Kubermatic to adopters list
  * manager_test: add err check for ioutil.TempDir
  * windows_test: remove duplicate code
  * cleanup tempfiles for manager_test
  * cleanup tempfiles for common_test
  * Functional test to verify vmis are migratable after update to from latest KubeVirt official release
  * update libvirt base container to rhel-av 8.3
  * Unit test to verify evaculation controller generated migration object fields
  * evacuation informer should only observe the creation of migration objects it created
  * cloud-init: Allow populate networkData alone
  * tests, sriov: XFail IPv6 connectivity test
  * dev guide, networking: net_raw cap is not required by virt-launcher
  * Revert "dev guide, networking: no capabilities are required"
  * Make sure to use all supported versions for status subresource
  * Update csv gen logic for v1 api
  * Update hardcoded references to v1alpha3 in unit tests
  * Update unit tests to account for aggregated api server registration for v1 API
  * Update functional tests that had hardcoded references to v1alpha3
  * Add functional tests to verify vm creation using all supported API versions
  * Add v1 api version
  * Revert "linux capabilities: remove CAP_NET_ADMIN"
  * Revert "libvirt, mtu: do not perform any network config on the launcher"
  * move kv update validation webhook to operator validation configuration
  * Fix test id for io mode test
  * update listtype markers for kubevirt pci host devices
  * Fix gosec unhandled errors in delete.go & create.go
  * Cleanup k8s jobs from test namespaces
  * If the fedora login expecter is stuck, retry
  * tests, multus: Change 3rd network SRIOV vnic name
  * tests, sriov: Centralize SRIOV network names
  * tests, multus: Fix IP address configuration
  * tests, Use RandName for creating random VMI names
  * Fail detection and handling when EFI without SB is not available
  * Add unit test covering GetDomainSpec fallback behavior
  * Reject --access-mode ReadOnlyMany when uploading an image.
  * Consume nightly build images from quay
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../kubevirt/WORKSPACE -dry-run=false
  * Fix failing unit tests for new GetDomain logic
  * Remove race condition from GetDomain check
  * Fix timed domain resync
  * fix patch for removing infra and workloads from KV
  * add webhook to validate kubevirt CR updates  - only allow updates to workloads key if no vmis are running
  * tests, sriov: Retry ping if it fails
  * tests, libvmi, vmi: shorten random vm names #2
  * tests, gpu: Do not mount /sys/devices/ for SRIOV devices
  * VMI configuration test: fix disk cache modes testing
  * fix gosec g204: Subprocess launched with variable
  * Removed unused function readProcCmdline()
  * Enable and fix tests
  * Fix gosec issue of: Potential file inclusion via variable
  Dropped patch: fix-goflags-overwrite.patch

* Mon Dec 21 2020 jfehlig@suse.com
- Update to version 0.36.0:
  * Functional test to verify vmis are migratable after update to from latest KubeVirt official release
  * update libvirt base container to rhel-av 8.3
  * dev guide, networking: net_raw cap is not required by virt-launcher
  * Revert "dev guide, networking: no capabilities are required"
  * Revert "linux capabilities: remove CAP_NET_ADMIN"
  * Revert "libvirt, mtu: do not perform any network config on the launcher"
  * Fail detection and handling when EFI without SB is not available
  * Add unit test covering GetDomainSpec fallback behavior
  * Fix failing unit tests for new GetDomain logic
  * Remove race condition from GetDomain check
  * Fix timed domain resync
  * Update ADOPTERS.md
  * tests, utils: shorten name of random VMs
  * Move some datavolume tests to the ceph lane
  * Old kubevirt released don't support CDIs WaitForFirstCustomer
  * Let virtiofs consider WaitForFirstCustomer setting of CDI
  * Use Immediate bind on negative PVC Datavolume tests
  * Enable WaitForCustomer CDI feature gate by default
  * Generate v1beta1 client for CDI
  * Don't try to hotplug waitForFirstCustomer PVCs
  * Fix access credential unit tests
  * Ensure that our service accounts can always update the VMI status
  * Update to a libvirt image with a newer seabios.
  * adjust pci address tests to consider the new virtio-iscsi controller
  * Remove AfterEach cleanup so we can capture VM/VMI state in overal aftereach cleanup instead of losing it.
  * Disable complex tests for now.
  * HotplugVolumes feature gate
  * Set grace period on attachment pod to 0 to have faster removal of the volumes when not removed by the controller. Added functional test to ensure the VMI goes into failed state when attachment pod is deleted. Added functional test to ensure the VMI is no longer migrateable after a volume is hotplugged.
  * Added functional tests with block volumes. Fixed functional attachment logic.
  * Added VMI attach/detach functional tests. Increased timeout on tests. Fixed typo in reason message
  * Fixed bug in how device names were calculated. Added functional test that adds a bunch of volumes, removes one, add a different one, and expects the device name to be the one just removed. Then adds the removed one back and expects the device name to be a new one. Added unit tests.
  * Improve error messaging during hotplug subresource add/removew
  * Fixes issue with VolumeRequests validation on the VM
  * Fix some issues pointed out in review. Fixed functional test with 5 adds and deletes. Added new functional test to test various adds and deletes.
  * Addes abilty to watch for libvirt device add/remove events for hotplug volumes
  * Updated and added functional tests. Added storage directory for storage related functional tests similar to networking. Fixed various issues found by the functional tests.
  * Attach disk to VM
  * VM controller unit tests for volume hotplug
  * Ensure we only add/remove volume operations are only performed if needed
  * Volume add/remove subresource unit tests
  * VolumeRequest validation unit tests
  * Validation logic for VM VolumeRequests
  * Hotplug VM Functional Tests
  * Add VM controller logic for handling volume add/remove requests
  * Add hotplug subresource api endpoints
  * Implemented virt-handler changes: Bind mount File System PV into virtlauncher pod. Expose block PV in virtlauncher pod. Added volume mounter struct to keep track of mounts. Added unit tests for volume mounter
  * Change phase/message/reason from hotplug struct to main VolumeStatus struct. Address some review comments
  * Automatically add virtio-scsi controller to all VMIs.
  * Updated vmi controller to separate sync and status update to follow KubeVirt guidelines. Updated unit test tests to match and added some extra unit tests for the new status update function.
  * Updated update-admission webhook to include verifying the structure of disks and volumes as well as call the create admission verifier to ensure nothing else slips through.
  * Added attachment pod life cycle functions to vmi-controller. Added unit tests for new functions
  * Attachment POD life-cycle code, including updating VMI status.
  * Update VMI admission webhook to allow modification of the disks and volumes section of the VMI Spec. This modification is needed to allow for disk hotplugging to happen. Only internal KubeVirt Service Accounts are eligible to modify the spec. Once we have the appropriate sub resources, users can call those to have it modify the spec on their behalf
  * macvtap, migration, tests: add a test w/ traffic
  * tests, network: Remove vmi Status ip normalization
  * tests, sriov: Use cloud-init to set IPv6 by MAC
  * tests, multus: Use network-data at bridge-cni test
  * tests, libnet: Add Match feature and expression builder to networkData
  * Update feature gate setup to new CDI version (now on CDI CR)
  * Reuse datavolumes already found in listMatchingDataVolumes for increased consistency between sync and updateStatus
  * Update test_id:5252 to run with WFFC enabled
  * check PVC if it waits for first consumer
  * Remove API phase "Provisioning"
  * Handle the DV in WaitForFirstConsumer phase by starting the "consumer-pod".
  * Remove sysctl binary dependency
  * Bump atlassian/bazel-tools
  * tests, network: Fix race condition GA test
  * virt-handler, status: Do not include the IP prefix consistently
  * Allow to run subset of rules for gosec
  * tests, dual stack: split probes tests to test per IP-Family
  * bump kubevirtci
  * Add ADOPTERS
  * make generate && make deps-update
  * bump cdi to 1.26.1 (from 1.25.0)
  * dev guide, networking: no capabilities are required
  * Increase CDI deployment timeout
  * expose, tests: fix early shutdown of `nc` TCP connections
  * Fix misspellings
  * Fixes race condition in func test
  * Properly handle failures when starting the qemu agent access credential watcher
  * Ignore warnings during vmi startup in access cred functests
  * Update access credential documentation and openapi markers
  * access credential sync events
  * Remove authorized_key file merging.
  * Report access credential status as a condition on the VMI
  * Revise access credential authorized_key file merging
  * Provide list of users for ssh auth instead of files
  * Make the authorized keys files list required for qemu guest agent propagation
  * Add unit tests to validate secret propagation watching
  * UserPassword access credential webhook validation and unit tests
  * unit tests for agent access credential injection
  * functional test for user/password credentials
  * Addition of UserPassword access credentials
  * Functional tests for access credential ssh key propagation
  * Reload dynamic access credentials based on secrets using fsnotify
  * Introducing the accessCredentials api for dynamic ssh public key injection
  * virt-launcher, agent-poller: Start poller with short intervals
  * virt-launcher, agent-poller: Refactor the Poll method
  * tests, login: Remove tests/login.go
  * test, login: Remove LoginToAlpine from login.go
  * tests, ipv6: Configure VMI IPv6 through console only when needed
  * test, login: Move loggedin expecter to console package
  * virt-launcher: Improve libvirtd debug log filters
  * tests, login: Move login.go to console/login.go
  * virt-handler, sriov: Add network name in VMI interface status
  * fix gosec issue of g204: subprocess launched with function call as argument or cmd arguments
  * Fix for flake CI test
  * Use the correct emulator prefix for qemu cleanup steps
  * Fix hardcoded qemu-kvm occurance in a migration test
  * Remove in some tests the assumption  of hardcoded qemu emulators
  * Explicitly set virtio-scsi on the scsi controller
  * WORKSPACE: Update libvirt container
  * Switch to use anew  global close() function in pkg/util Fix typos and remove extra comments
  * tests, console: Remove VMIExpecterFactory
  * Fix double migration during node drain
  * test, network: Add bridge binding + ga test
  * networking, tests: also check the MTU of the tap device
  * tests, libvmi: Remove interface,network config from NewFedora
  * linux capabilities: remove CAP_NET_ADMIN
  * libvirt, tap: create the tap device w/ the same user as libvirt
  * mtu, tuntap: set link MTU when creating the tap device
  * libvirt, mtu: do not perform any network config on the launcher
  * net admin: disabling tx checksum offloading on virt-handler
  * Add a log message if we pick up a new CA bundle
  * Increase rotate intervall
  * tests, multus, sriov: Refactor tests
  * Update bazel files
  * Switch to use named return errors to allow updating the error from defered function
  * Fix gosec issue: Deferring unsafe close() When deferring a close() we don't have a chance to check the error returned from the close() call itself. For RW files we treat the error similar to a write() error , for RO files we only log an error message
  * Mirror PVC struct
  * Add function test to validate IO mode settings
  * Set IO to native also for pre-allocated file disks
  * Switch to use a common function GetImage and remove GetImage from manager.go
  * Use qemu-img in order to identify sparse files and get image info
  * Set the IO mode to 'native' when possible for better performance
  * test, cloudinit: Use "json" annotation instead of "yaml"
  * tests, multus, sriov: Fix flakiness due to race between ga and test
  * tests, multus, sriov: Add validatePodKubevirtResourceName
  * tests, multus, sriov: Add missing error check
  * tests, multus, sriov: Fix checking for the same network twice
  * image-upload: wait up to 5 min for PVC and Pod
  * Remove domain label from kubevirt_vmi_memory_unused_bytes
  * gosec - fix CWE 326
  * virt-launcher: drop CAP_NET_RAW from compute container
  * virt-launcher, dhcp: Avoid using SO_BINDTODEVICE on the dhcp server
  * agent-poller, test: Extract AsyncAgentStore tests to new file
  * agent-poller, test: Rename agent poller test
  * tests, console: Require at least two batchers for the safe expector
  * tests, console: Introduce SafeExpectBatchWithResponse
  * tests, console: Replace some NewExpecter usages
  * tests, console: Change NetBootExpecter to not return an expecter
  * tests, login: Replace the Alpine login helper
  * tests, login: Replace the Cirros login helper
  * tests, login: Check privileged console prompt
  * tests, login: Replace the Fedora login helper
  * tests: Use LoginTo* helpers in waitUntilVMIReady
  * updated the technical description
  * Add enp0s3 to approvers list
  * Change file permissions on binary directory
  * docs: Fix documentation for useEmulation flag
  * virt-config: Fix tests for KubeVirt CR
  * virt-config: Drop stopChan
  * removed the word place-holder
  * fix gosec sha1 week cryptographic issues
  * Fix gosec md5 weak cryptographic primitive
  * Fix shell formatting, fix entrypoint path
  * Disable Virtio-FS Metadata Cache
  * Add Igor Bezukh to test approvers
  * Fix permissions tests for VMs
  * lock device plugings maps during device controller shutdown
  * dp: verify that host devices topology is being correctly reported
  * update the API fields so it be complient with API rules.
  * testutils: remove unnecessary changes to the config mock
  * tests: move the soundcard test out of the GPU module
  * Add a "GPU" passthrough functional test
  * update unittests to use kubevirt CR and remove remove hostDevConfigMapInformer
  * remove the hostDevConfigMapInformer, get host devices from KubeVirt CRD
  * request host devices on vmiPod as well
  * make sure that permitted host device config is working as expected
  * add unit tests to veriy host devices assignment
  * device-manager: clear permitted device list before parsing
  * device-manager: added mdev tests + misc fixes
  * device-manager: improve the PCI tests
  * device-manager: misc post-rebase fixes
  * add GetInitialized to pci and mdev device plugings
  * add HostDevices feature gate
  * device-manager: add static tests for PCI device discovery functions
  * device-manager: few cosmetic fixes
  * make sure that vmis can request only permitted gpus
  * tests: return hostDevConfigMapInformer as part of the NewFakeClusterConfig
  * device-manager: mock PCI device info getters for tests
  * Fix device controller static tests to match the new API
  * Move the check for permanent device plugins to list creation Instead of always adding them to the list and then ignoring   them later
  * Add a lock to ensure device plugins won't be started/stopped multiple times in parallel Also fix some typos and avoid an active loop
  * close device plugin channel is a safe manner
  * introduce a ControlledDevice struct for the device controller to keep dpi stop chan
  * Fix ignored static DPs, fix typos and remove defer Stop() in Start()
  * Refactor permanent device plugin code
  * dynamically start and start device plugings for permitted/banned devices
  * propagate hostDevConfigMapInformer to device controller
  * virt-launcher: handle allocated host devices using a single map
  * reject specs with non-permitted HostDevice and GPU resources
  * convert HostDevices and GPUs to libvirt hostdev for pci and mdevs
  * collect PCI and MDEVs made available for assignement by the device plugins
  * add alias to libvirt hostdev struct
  * separate ResourceNameToEnvvar to utils
  * add device plugings for permitted devices which are present on the nodes
  * add a device plugin for mediated devices
  * add a device plugin for pci devices
  * add virt-config to device controller
  * add a HostDevices api schema
  * add TopologyInfo to out device plugin api
  * rename the device manager controller for kvm controller
  * introduce a new hostDevConfigMapInformer
  * handle the kubevirt-host-device-plugin-config config map
  * Add PermittedHostDevices type to support a new kubevirt-host-device-plugin-config configmap
  * Revert "Merge pull request #4470 from oshoval/fix_sriov"
  * tests, Fix CDIInsecureRegistryConfig logic
  * tests: LoggedInCirrosExpecter can return a nil expecter in case of error, with these changes we call Close on the returned expecter if the error is nil.
  * tests, sriov: Do not mount /sys/devices/ for SRIOV devices
  * virt-launcher: remove redundant cidr from dhcp server address
  * tests, sriov: Fix the helper that waits for a vmi to start
  * tests, Fix SRIOV UpdateCDIConfigMap panic
  * add unit test
  * Enhancement #4365 [virt-controller] Remove redundant initcontainer when there is no ContainerDisk defined in VM
  * Consolidate shell script files into functions
  * Create main shell scripts to call from the ci-config
  * Fix comment typos
  * Add scripts for nightly master deploy
  * Move code for downloads and test execution into scripts
  * ensure the virt-handler killer pod has gone
  * audit the usage of unsafe pointers
  * Set leader metric after controller is functional Add a unit test for this
  * Define side effects class on our webhooks
  * Improved the Technical Overview description
  * changed: VM has only one VMI
  * Included a figure to illustrate the components architecture
  * Included a little bit more details in the virt-launcher description
  * Included a little bit more details in the virt-handler description
  * Included a little bit more details in the virt-controller description
  * Make the name of components bold
  * Improved the Technical Overview description
  * Fixed typo

* Fri Nov 13 2020 James Fehlig <jfehlig@suse.com>
- Fix -buildmode=pie
  fix-goflags-overwrite.patch, dont-build-virtctl-darwin.patch

* Tue Nov 10 2020 jfehlig@suse.com
- Update to version 0.35.0:
  * sriov lane: skip flaky tests until their issue is resolved
  * add an independent claclulation of required vcpus for mem overhead calculation
  * adjust memory overhead calculating by adding a static 10Mi
  * move guest cpu topology modification to vmi mutator webhook
  * Ensure that we restore the cdi-insecure-registry configmap in tests
  * Add test_ids_cnv_2.5
  * dual stack, expose, tests: remove batchv1.Job duplicated code
  * test, waitvmi: Add context mechanism to WaitUntilVMIReadAsync
  * dual stack, expose, tests: skip on non dual stack clusters
  * dual stack, expose, tests: port VM service tests
  * tests, multus-tests, SRIOV: configure IP based on MAC or name
  * Catch goroutine panic with GinkgoRecover in tests
  * tests, multus_tests: make helpers return an error
  * dual stack, expose, tests: port VMIRS cluster IP service test
  * dual stack, expose, tests: port UDP services test
  * dual stack, tests: ping first on helloWorld{UDP|HTTP} jobs
  * dual stack, expose, tests: port the VMI service test cases
  * Bump kubevirtci
  * make generate and make deps-updateand update test import
  * Bump CDI to 1.25.0
  * Reduce the cluster size a little
  * dual stack, expose, tests: get the IP addr from a DNS name
  * bump kubevirtci: get latest sriov provider
  * Infra test made invalid assumptions about cluster composition
  * Fix panic when endpoints were empty.
  * dual-stack, virtctl: expose ipv6 services
  * Remove 'string' from json tag to preserve type information in our API
  * automation: cancel CDI insecure registries cehck on sriov lane
  * Emit an event if we detect terminating pods
  * tests, pausing_test: change long process test
  * test, infra_test, Adapt tests to support dual stack
  * tests: remove `IsRunningOnKindInfraIPv6`
  * fix wrong logic in SetDriverCacheMode log message
  * Revise functional test to verify 440 read only image
  * Build container disks with 440 mode and 107:107 ownership
  * Add e2e test for replacing terminating pods immediately
  * Bump kubevirtci
  * test: Remove all the usages of `IsRunningOnKindInfraIPv6`
  * Disable service links on virt-launcher Pod
  * tests, infra-test, Remove unneeded vmi creation
  * infra_test, Refactor tests to use a DescribeTable
  * infra_test, Add validation of errors
  * Fix flaky timezone test
  * Let VMIRS react to terminating pods of VMIs
  * Let the VMI indicate when Pods are terminating
  * functests, macvtap, migration: successful macvtap VMI migration
  * functests, migration: move some asserter subset to common helpers
  * functests, macvtap, multus: use libvmi Cirros VMI factory
  * functests, macvtap, multus: schedule the VMs in the same node
  * tests: update the `StartVmOnNode` method to return the started VMI
  * examples, macvtap, multus: add example for macvtap VMI
  * macvtap, admitter: macvtap requires multus network
  * functests, macvtap, multus: add connectivity test between VMs
  * macvtap: feature gate macvtap feature
  * functests, multus: refactor `configInterface` to allow sudo
  * functests, macvtap, multus: add test with a custom MAC address
  * tests: remove all net-attach-defs on test cleanup
  * automation, macvtap: restrict macvtap func tests to multus lanes
  * unit tests, macvtap, multus: introduce macvtap
  * macvtap, multus: add macvtap BindingMechanism
  * improving PCI configuration tests
  * Template the cdi namespace
  * add dev registry as insecure registry to cdi
  * Update testing infra to cdi 1.23.7 in order to bring in registry import fixes
  * Datavolume container registry import test
  * CONTRIBUTING: point developers to kubevirt-dev slack
  * rebase
  * Remove incorrect listtype
  * fix 1.19 lane
  * Propagate error from patchValidation
  * rebase
  * reduce scope to vm/vmi
  * Remove +listType=map from tolerations This marker also requires //+listMapKey which can't be resonable set at this moment. (All fields are optional and missing default)
  * update builder
  * review
  * Add missing markers
  * Test verifying kubectl explain works
  * Adding test verifying crds are structural
  * Use controller-gen to generate validations for crds
  * test if crds for operator are correct
  * adding tools for generating correct validation
  * cleaning generated desc. and nullable fields in status
  * adding patching of crds for operator
  * adding markers for controller-gen
  * tests, restore tests: check on successful commands
  * Fix gosec issue: week random generator
  * Bump kubevirtci
  * It is not always bad for VolumeSnapshot to have an error
  * Fix artifacts in gosec target
  * tests, infra-test, Refactor node selection
  * Do not change vnc socket's permission to 0444
  * tests, infra-test, Fix node updates
  * tests, infra-test, Add missing break when selecting a node
  * tests, pausing test: increase time for long process
  * tests, login: expect fedora full prompt
  * tests, migration, stress-test: remove doubled `\n`
  * tests, re-factoring: use safe expect-bathcer and prompt Expression
  * tests, infra-test, Add missing check on AfterEach
  * tests, infra_test, Add missing assign when removing taints
  * Don't parallelize cluster-sync dependencies
  * hack: Print cluster-* script name when complete
  * Point to kubevirtci for new providers.
  * Update documentation to refer to scripts having moved to cluster-up/
  * Update docs that refer to kubevirt-config ConfigMap to use kubevirt CR
  * tests: Add missing asserts to the vmi-configuration tests
  * Adapt conformance tests to support migration.
  * automation: remove ipv6 lane
  * Set read only for our demo container disks and verify their mode does not change at runtime
  * Attempt to use whatever permissions a container disk has applied to it without mutating the file
  * rebase + fix compile error due to another PR
  * set the label for downwardAPI test in the test itself
  * Move AddDownwardAPIVolumeWithLabel to be public, add downwardAPI disk to the migration test
  * add downwardAPI volume in the test instead of in the helper
  * delete commented out line
  * Adding function tests (for make functest)
  * remove rule violation
  * support  DownwardAPI volum source
  * Fix typos and formatting
  * tests/utils: remove 'IsIPv6Cluster' function
  * tests, iscsi: remove iSCSI PVC tests IPv6 cluster skips
  * VM status to report whether volumes support snapshots.
  * tests, network: Relocate VMI/POD IP validation w/ Guest Agent
  * Fix pull-kubevirt-apidocs
  * tests: Render pods in the test namespace
  * tests, iscsi: change 'CreateISCSITargetPOD' to return pod
  * Lift the e2e test parallel run restriction for fedora guests
  * Give the CI nodes two more GB of memory
  * Adjust bump script to use tagged kubevirtci releases
  * tests, console: Rename functions to fit the new package
  * tests, ping: Move ping under libnet package
  * tests, expecter: Create a console helper package
  * Bump kubevirtci
  * Mirror new dependencies
  * update builder image
  * tests, networkpolicy: Wait for VMIs readiness in parallel
  * Exclude .git and _ci-configs at bazel's goimports
  * multi-queue: cap the maximum number of queues
  * Add 2.x QEMU Guest Agents to the list of supported versions
  * Update to fedora 31 as base image.
  * Add test_id for post-copy migration with Guest Agent Test
  * dual stack, services, tests: enclose test setup in a `By` clause
  * dual stack, services, tests: really check connectivity exists
  * dual-stack, tests: skip IPv6 test on non-dual stack clusters
  * dual stack, services, tests: unify the `Job` cleanup solution
  * dual stack, services: provide more explicit info on test execution
  * tests: test the masquerade bridge has the correct mtu
  * virt-handler/launcher: Set the pod iface mtu on the bridge
  * restore backwards compatiblity with api group/version on DataVolumeTemplates spec
  * Add short readme
  * multi-queue, tests: assuret we can request a VM with a single vCPU
  * api: update the API description of the NetworkInterfaceMultiqueue flag
  * tap-device, multi-queue: enforce single-queue tap
  * Delete kubevirt service accounts from default privileged SCC
  * Added helper function to return all kubevirt service account users
  * Removing redundant tests related to SCC users modification
  * Added unit tests for SCC users modification upon upgrade.
  * Remove kubevirt service accounts from default privileged SCC
  * tests, nfs: avoid failures in afterEach of a skipped test
  * test, nfs: Change CreateNFSTargetPOD to return a Pod
  * tests, dualstack: don't stop nfs tests cleanup in case of an error
  * tests, dualstack: use IPFamily instead of boolean to mark tests
  * tests, dualstack: introduce SkipWhenNotDualStackCluster
  * tests, dual stack: Adapt tests using NFSTargetPOD to support dual stack
  * docs: Fix the ginkgo flags usage example
  * Properly exit if kubevirt does not get ready on cluster-sync
  * Rework logic so it is easier to understand what is happening
  * fix restore controller memory corruption
  * Allow PVC as volume source with a DV populating the PVC. Before this was not allowed because we could not be sure that the PVC was fully populated. This commit checks the DV to ensure the PVC is fully populated.
  * Save a nice cluster-overview to the artifacts
  * Disable goveralls debug output
  * Take time in cert tests after CA generation
  * Use coverage merge tool for goveralls
  * Introduce a tool to merge coverage reports
  * Enable atomic count, race detection and fix races
  * Move coverage reports over to bazel
  * Use a proper cc_library for libvirt dependencies
  * Auto-generate Help message from /metrics endpoint to docs/metrics.md
  * tests, libnet: Relocate validation to libnet
  * tests, libnet: Move cloud-init net and dns to libnet
  * Fix flaky rename test
  * Run Travis CI only on selected branches, remove sudo flag
  * tests, infra-test, Solve CI flakiness due to update conflict
  * Fix flaky unpause tests
  * Refactor .json files to go file
  * Mark networking conformance tests
  * Fail only when new issue comes up
  * Fix high severity&confidence issues
  * Add gosec to project
  * Fix display of virtctl help text for other usages
  * tests, libvmi: Introduce CloudInit NoCloud Network Data
  * functest for PR #4132
  * Fix coexistance of scsi and sata drives

* Mon Nov  9 2020 James Fehlig <jfehlig@suse.com>
- spec: Add rpmlintrc to filter statically-linked-binary warning
  for container-disk binary. The binary must be statically linked
  since it runs in a scratch container.

* Fri Nov  6 2020 James Fehlig <jfehlig@suse.com>
- spec: Generate the registry path for kubevirt-operator.yaml at
  build time. Prjconf macro 'registry_path' can be used to
  override registry path to the KubeVirt container images
- spec: Add kubevirt-psp-caasp.yaml, a PSP based on CaaSP
  privileged PSP, to the manifests subpackage
- spec: Don't add component name to DOCKER_PREFIX passed to
  build-manifests.sh

* Sat Oct 31 2020 Jan Zerebecki <jzerebecki@suse.com>
- Add package with built YAML manifests used to install kubevirt

* Thu Oct 29 2020 James Fehlig <jfehlig@suse.com>
- spec: Remove needless use of chmod and build-copy-artifacts.sh

* Fri Oct 23 2020 James Fehlig <jfehlig@suse.com>
- spec: Fix typo in date command

* Wed Oct  7 2020 jfehlig@suse.com
- Update to version 0.34.0:
  * jsc#ECO-2411
  * Add mirrored dependencies to WORKSPACE
  * Mark networking conformance tests
  * restore backwards compatiblity with api group/version on DataVolumeTemplates spec
  * Revert "move all tests to use kv config"
  * Revert "update config message to specify which resource type it is using"
  * Revert "test usage of configmap configuration"
  * Revert "update build file"
  * Revert "convert postcopy tests to use KubeVirt CR"
  * Rework logic so it is easier to understand what is happening
  * Allow PVC as volume source with a DV populating the PVC. Before this was not allowed because we could not be sure that the PVC was fully populated. This commit checks the DV to ensure the PVC is fully populated.
  * vmi, sriov: Enable to set the PCI address on a SRIOV iface
  * Don't discard bazel platform cache on virtctl cross-compilation
  * convert postcopy tests to use KubeVirt CR
  * fix autoconverge test
  * remove using BeforeAll in vmi configuration tests
  * generated openapi spec
  * clean up
  * start prom server earlier in the virt-handler process so health check returns without EOF error
  * change kubevirt config type MemBalloon
  * dump kubevirt cr in ci artifacts
  * cpuRequest can not be type string since when the resource is patched it will fail to parse the units
  * change bool to pointer to know unset vs value set to false
  * update build file
  * test usage of configmap configuration
  * update config message to specify which resource type it is using
  * move all tests to use kv config
  * virt-launcher, Add mechanism to guard add/delete events channel
  * Generated artifacts
  * Add functional tests for missing subresource RBAC rules
  * Allow admins and editors of a namespace to [un]pause a VMI
  * Add dummy status to DataVolumeTemplate objects to maintain backwards compatibility
  * Add functional test to validate api compatiblity during update
  * changed migration test to use table
  * only log event if migration is stuck during post copy migration
  * change api from MigrationMode to AllowPostCopy
  * switch to post copy migration if not completed with in acceptableCompletionTime
  * update openapi spec
  * add NFS migration test with postcopy
  * remove vmiHasLocalStorage function
  * fix migration tests
  * remove reject postcopy for storage test
  * remove nested vmi migration configuration
  * change usePostCopy to migrationMode
  * move when mode is set
  * allow for postcopy migration
  * maybe fix flakes test
  * vendor in 1.23.5 CDI to hand golden namespace use case
  * Validate network interface name
  * tests, utils: Check events watcher type before casting
  * Add readiness and health probes to virt-handler
  * Removes unusable fields from vm DataVolumeTemplates
  * virt-launcher, Remove unneeded log
  * virt-launcher, Remove double domain event sending
  * virt-launcher, Fix Guest Agent updates causing an event handling deadlock
  * selinux: always build KubeVirt with selinux support
  * Run make generate
  * Adjust ceph-rook focus for e2e tests
  * wrong apiVersion used for VirtualMachineRestore owner references
  * update init container unit tests to validate container-disk pre-pull
  * add container disk images also as init containers in order to guarantee they are pulled before virt-launcher starts
  * add '--no-op' option to container-disk entry point for pre-pull logic
  * Make the nogo check pass
  * Make kubevirt compile with bazel 3.4.1
  * Update builder image to bazel 3.4.1
  * wait for vmi-killer pod to start before moving on
  * Document basic parallel-test execution needs
  * Integrate the junit merger into the parallel functest execution
  * Add a tool to merge partial junit results
  * Don't set the namespace in the VMI factory
  * Run most of the VMI lifecycle tests in parallel
  * Run kubectl related tests in parallel
  * Hugepages are limited, run the relevant tests not in parallel
  * Make version and vm-watch tests execute in parallel
  * Don't check terminating pods if they pick up config changes
  * Run container disk tests in parallel
  * Run expose tests in parallel
  * Run probe tests in parallel
  * Allow running VMI Preset tests in parallel
  * Run most of the cloud-init tests in parallel
  * Make subresource tests part of the parallel test suite
  * Adjust subresource access tests to new test service accounts
  * Reference the default namespace directly
  * Add a skip check for a migration tests if enough nodes are available
  * Make access tests parallel executable
  * More parallel tests
  * Resolve test-namespace name in the test
  * Allow VM tests to run in parallel
  * Allow console tests to run in parallel
  * Allow the headless service tests for VMIs to run in parallel
  * Allow tests in vmi_configuration_test to run in parallel
  * Make it possible to set the number of parallel executors
  * Increase slow test threashold to 60 seconds
  * Ensure that --skip and --focus flags are only passed onces
  * Change build environment to execute ginkgo in parallel
  * Let the ginkgo reporter log where it will dump artifacts
  * Split setup and teardown code between parallel and synchronized steps
  * Consume the ginkgo binary from the vendor folder
  * Mark all tests as have to be run in serial
  * fix typos
  * docs: Update for k8s-1.18 as default provider
  * Add option to log BIOS output to serial and use it to test for bootable NICs
  * Migrate VMI when its pod is marked for eviction
  * Intercept evictions on virt-launcher pods
  * Support testing kubevirt on RHCOS
  * Update kubevirtci to latest commit
  * create tap device: add multiqueue support to netlink
  * set vmipod cpu request based on guest vcpus and cpu_allocation_ratio
  * allow to set a cpu allocation ratio in kubevirt config
  * Test IDs for Node Placement tests
  * only focus on tests that require rook-ceph for rook-ceph lane
  * When filtering or aggregating metrics around the state label, having it exposed as a human readable state makes it a lot easier to understand, and thus, easier to get the desirable information. This PR changes kubevirt_vmi_vcpu_seconds' state label to a human readable string
  * libvirt: disable PXE rom on interfaces with no boot order Except for virtio interfaces for which a rom is implicitely loaded
  * Keep conformance artifacts on the top level
  * tap device: use netlink instead of songgao's water lib
  * netlink: update vendor folder
  * bazel: update netlink dependency
  * Release func tests on every release
  * Add missing test ids
  * Fix sync of generated client-go to master
  * flaky pause test: make long-running process longer and quieter
  * switch virtiofs tests to use datavolume
  * test that vitriofs file written in the guest is present in the pod
  * functional test to verify that virtiofs is enabled
  * update generated files
  * virtiofs requires virt-launcher selinux policy changes
  * enable virtiofsd debug logs be setting by setting virtiofsdDebugLogs label
  * handle filesystem virtiofs devices
  * vmis with virtiofs require memory backing shared access
  * allow CAP_SYS_ADMIN when the experimental virtiofs is required
  * add a filesystem device schema element
  * add a memorybacking access schema element
  * Adding feature gate for experimental virtiofs support
  * selinux: allow creating VMIs on nodes without selinux
  * examples, vmi-masquerade: correct userData script
  * tests: change hostdisk tmp path to /var/provision
  * Bump kubevirtci to start testing k8s-1.19 provider
  * Fix ACPI doc string
  * Add functest for KVM hidden
  * Support hiding KVM MSR from guest
  * add snapshot APIGroup to aggregate cluster rules
  * tests, networkpolicy: Add ports 80/81 tier1 http tests
  * tests, vmi_servers: Add `HTTPServer.Start` and `TCPServer.Start` method to bypass LoggedIn
  * Bring openapi spec in sync
  * Fix logical error in affinity copy logic
  * Add optional validation marker for new fields
  * Update functional tests to match new object layout
  * Fix unit tests for new object layout
  * Fix injectPlacementMetadata to accept ComponentConfig objects
  * Generated Artifacts
  * Introduce ComponentConfig to contain NodePlacement
  * Functional tests exercising placement logic
  * Unit tests to ensure correctness of injectPlacementMetadata
  * Merge Affinity, Tolerations and NodeSelectors from NodePlacement to podSpecs
  * Generated artifacts
  * Define NodePlacement for workloads and infra
  * Port NodePlacement from HCO
  * tests, libvmi: Add ports to InterfaceDeviceWithMasqueradeBinding
  * Add conformance automation and manifest publishing
  * SELinux: merge .cil policies and add a lot of comments
  * vnc: use generic VNC client on comments
  * vnc: remove unused FLAG const
  * tests: re-enable couple of certificate functests
  * network, tests: check IPv6 probes on dual stack network configs
  * probes, tests: provide a TCP/HTTP server running on an helper pod
  * network, tests: move the HTTP/TCP server creation to a separate file
  * probes, tests: create ready/not ready asserter functions
  * probes, tests: encapsulate VMI creation into a function
  * probes, tests: have probe creation helpers
  * tests, network: correct the string length
  * probes, tests: exclusively use cirros VMIs on the probes tests
  * network, tests: delete the leaked Jobs on the test tear down
  * network, tests: ping first, then connect on helloWorld jobs
  * network, tests: use assert / failed connectivity checks
  * network, tests: add dual stack masquerade binding service tests
  * network, tests: prepare for multiple binding / dual stack configs
  * network, tests: move services functests to dedicated module
  * tests, libvmi: provide a minimal CirrOS VMI via the libvmi factory
  * fmt updates
  * Adjust timelines and verbage to reflect feedback
  * Fix release scripts git email and name variables
  * New release documentation
  * Replace outdated release announce script with new tool
  * We introduced our `Pach` type which collides with kubernetes type. By default kube-openapi takes only last part of type/model definition. So type "kubevirt.io/client-go/api/v1.Patch" ends up -> "v1.Patch" & "k8s.io/apimachinery/pkg/apis/meta/v1.Patch" -> "v1.Patch".
  * dual-stack, tests: actively check the cluster for dual stack conf
  * dual stack, tests: check if the cluster is dual stack
  * Add creation of bazelrc for running unnested in prow
  * virt-chroot: use sysfs node for getenforce instead of less-reliable go-selinux
  * selinux: print reason why getting launcher context failed
  * network, tests: add a flag to skip a test asserting dual stack conf
  * Addressed comments
  * fix virtctl image-upload ignoring custom storage class
  * Add unit tests for Service patching
  * use informer for VirtualMachineRestores in restore webhook
  * staticcheck updates
  * don't allow creation of a VirtualMachineRestore if on is in progress
  * make VirtualMachineRestores owned by VM
  * wait for PVCs created from snapshots to be bound if not WaitForFirstConsumer
  * Correctly check VM run strategy
  * check running/runstrategy before restoring and one additional functional test
  * tighten up functional tests
  * initial functional tests for VM restore
  * restore controller generate events on completion and error
  * updates from rebase
  * add source UID to VMSnapshot status and verify source matches target when restoring
  * fix apiGroup handling
  * VM sestore webhook
  * restore unit tests
  * restore controller implementation
  * snapshot controller waits for no VMIs or pods using PVCs
  * add VirtualMachineRestore type and CRD
  * remove include/excludeVolumes
  * update VirtualMachineRestoreStatus object to include timestamp and error
  * add VirtualMachineRestore type and CRD
  * Fix overloaded 'v1.Patch' api field
  * Prevent delete and replace of service endpoints with ClusterIP == ""
  * Fix validation for self-signed cert and addressed comments
  * Add support for camel-case spellings of "userdata" and "networkdata"
  * tests, net: Add dual-stack checks for post migration connectivity
  * tests, net: Remove post migration connectivity workaround
  * Enhance operator functional tests to validate pods are torn down after kv cr is deleted
  * test: set kubevirt.io/memfd = false for k8s 1.16
  * Add annotation kubevirt.io/memfd
  * Unit tests to validate finalizer functionality on kubevirt objects
  * Restore ability to set finalizer on kubevirt objects
  * Unit tests to verify operator injected labels remain consistent
  * Restores operator managed by label for backwards/forwards compability during updates
  * Add mhenriks to approvers/reviewers list
  * introduce retryOnConflict to certificate infra test
  * tests, Make network policy tests dual stack compatible
  * make generate after git rebase
  * deps-updae && generate
  * Workaround for a not accessible CDI dependency bitbucket.org/ww/goautoneg
  * Update cdi in client-go and manifests/testing to v 1.21
  * Run make deps-update
  * Bumped CDI version to 1.21.0
  * virt-api: allow update of VM metadata and status during VM rename process
  * Rename option --allow-intermediate-certificates to --externally-name
  * Add unit test for cert-manager
  * Add option to allow client's intermediate certs to be used in building up the chain of trust in cert validation for virt-handler and virt-api
  * Add options to allow users to configure certificate and key file paths for virt-handler, virt-controller and virt-api to accommodate varying rules around certificate validation.
  * Limit CriticalAddonsOnly taint to a single compute
  * Add test-id's for VMI migration and lifecycle testcases
  * Add event for vmi failed render
  * test, masquerade: Add dual stack vmi to vmi ping
  * tests, Fix Network Policy Flakiness
  * tests, Add waitForNetworkPolicyDeletion
  * tests, Add skipNetworkPolicyRunningOnKindInfra for NetworkPolicy tests
  * tests, Remove SkipIfNotUseNetworkPolicy
  * tests, expecter: Centralize expecter helpers under expecter.go and login.go
  * Add unit tests for to make sure it won't accidentally break passing monitorNamespace and monitorServiceAccount parameters
  * add test_id to functional test
  * add openapi listType=atomic to patches
  * add func test for custom patches
  * add custom patches to kubevirt resources on creation
  * Fix issues of using default monitorNamespace and monitorServiceAccounta when those properities are not assigned
  * update: fixing and adding unit tests
  * test: add reserved hugepages
  * tests, skip migration fail test on kind ipv6 provider
  * test: add test for source in memorybacking
  * Add source in memorybacking
  * Set NUMA to use memfd
  * virt-operator: on update, roll over daemonsets first, then controllers
  * virt-operator: fix a copy-paste error
  * Add functional test for custom-port flag
  * Make use of stdout cleaner
  * Added functional test
  * Add option to run only VNC Proxy in virtctl
  * Keep a single go_test_default rule
  * Document on how to use the conformance tests
  * Add the first conformance test
  * Add wrapper binary for conformance tests
  * Detect the kubevirt install namespace dynamically
  * Fix issues that virt-operator cannot extract MonitorNamespace and MonitorServiceAccount from JSON.
  * tests, network: Test connectivity pre/post migration
  * tests, job: Convert WaitForJobTo* to a non-assert version.
  * Generate deepcopy for NUMA
  * add a NUMA schema element
  * Removal of unnecessary output
  * Added e2e test for unused memory metric
  * Fix virtctl build for linux-amd64
  * Adds new metric kubevirt_vmi_memory_unused_bytes

* Wed Sep 30 2020 James Fehlig <jfehlig@suse.com>
- Preparation for initial submission to SLE15 SP2
  jsc#ECO-2411

* Tue Sep 15 2020 dmueller@suse.com
- Update to version 0.33.0:
  * Enhance operator functional tests to validate pods are torn down after kv cr is deleted
  * Unit tests to validate finalizer functionality on kubevirt objects
  * Restore ability to set finalizer on kubevirt objects
  * Unit tests to verify operator injected labels remain consistent
  * Restores operator managed by label for backwards/forwards compability during updates
  * tests, migration: Validate dual stack VMI and Pod IP/s
  * tests, make primary_pod_network dual stack compatible
  * tests, Create ValidateVMIandPodIPMatch helper
  * Turn off modules for staging.
  * Fix verifying make targets
  * Give migration kill pods a name not based on their node name
  * Fix another flaky ertificate related unit test
  * Fix matching of Makefile vars to env for goveralls
  * Output what the new error is when an api violation occurs
  * tests: adapt test-id:4153 to dual-stack cluster
  * sriov-tests, checkMacAddress: remove sequential expecter cases
  * sriov tests: Add CNI version to sriov NAD
  * removeNamespaces: add informative failure reason
  * cluster-deploy.sh: cancel cdi deployment on sriov-lane
  * remove version from go.mod
  * Use PingFromVMConsole for ipv6 instead of trace route
  * tests, make test 1780 dual stack compatible
  * refactor virtctl image-upload args
  * tests,libvmi: Append passed options
  * Rebase on Goveralls
  * Export -mod=vendor to always use vendor
  * Update ldflag to point to right package
  * Increase memory limit for iscsi pod
  * deps-update to reflect state after rebase
  * Fix test to properly work with TLS 1.3
  * Update kubevirt builder image to use go1.13.14
  * Add required dependencies for functest image build
  * Check if new api rule violation was added
  * Pin bazel for builder
  * selinux: relabel /dev/null to container_file_t
  * selinux, virt-handler: relabel the clone device
  * selinux, virt-chroot: provide a command to relabel files
  * Add gradle install for builder to reenable swagger
  * Set libvirt to virtmaint-sig/for-kubevirt 5.0.0
  * Update builder image to include new goveralls version, remove ppc64le
  * Move coverage from travis to prow
  * Support VMI scheme multi IPs list in case of dual stack
  * Improve stability of fedora VM's login expecter
  * tests: Use new image for sriov tests
  * tests/containerdisks: add fedora-extended image
  * kubevirt/BUILD.bazel: push to cluster registry
  * containerdisks/ WORKSPACE, BUILD.bazel: add new image
  * containerdisks: add doc about container-disk images
  * Unit test to veriy migration target is cleaned when VMI is deleted
  * Unit test to ensure an error is returned if multiple container disk directories for the same vmi exist
  * Add unit test to verify stale clients are handled during pre migration target setup
  * abort migration if the vmi is deleted or in the process of being deleted
  * Add better logging to container disk mount/unmount
  * wait for virt-handler to come back online during migration fail func test case
  * ensure we detect the correct pod environment during isolation detection when migrating
  * ensure only we're mounting/unmounting the right pod's container disk during migration
  * gitignore: ignore files ending with ~
  * Ensures stale local data from failed migration target is cleaned before attempting to migrate again
  * Functional test to validate migration failures
  * Domain XML to be logged on info level
  * Fix the test default SMBIOS testcase
  * Add custom PCI tests
  * Fix bug in virtctl upload when using PVC without any annotations. In this case in code the annotations map is nil, and we attempted to set a value in that nil map causing a crash of virtctl.
  * Allow podman for normal build steps
  * Makefile: Control timestamp addition
  * Makefile: Add timestamps to make targets
  * Makefile: Use realpath instead of shell to calculate path
  * export local provider variables to the correct location
  * no need to verify the number of depoyed nodes for local provider
  * Use proper namespace in functional test
  * Fix doc string
  * Add --security-opt label:disable to bazel server version check On Fedora 32 with moby this fixes an selinux issue in the imega/jq container.
  * Fix tests binary release
  * tests: Add phoracek to approvers
  * create-tap: improve code readability
  * selinux: update the default launcher selinux type
  * create-tap: prevent FD leaking into the tap-maker
  * selinux: run virt-handler without categories
  * selinux: networking requires escalated selinuxLauncherType
  * selinux: create the tap device using launcher selinux label
  * create-tap: add a new cmd to virt-chroot
  * network: have the launcher pid for future tap device creation
  * Create tap devices w/ multi-queue support
  * masquerade/bridge binding: use pre-provisioned tap device
  * Create tap device on virt-handler
  * functests: Refactor VMI helpers
  * tests: Update the vmi instance after creation
  * tests: configureIPv6OnVMI remove unnecessary vmi parameter
  * tests, dual-stack: configure ipv6 on dual stack cluster vmi
  * Add all the missing test-ids
  * dual-stack: IsIpv6Enabled use podInterface addresses.
  * fix typo
  * Rename managed-by label to be literal
  * Don't add empty values to KubeVirtDeploymentConfig
  * Use more consistent config access function
  * Functional tests for product related labels
  * Add ProductName and Version labels to KubeVirt objects
  * Fix flaky certificate expiration unit test
  * tests, job: Rename RenderJob to NewJob and expose new args
  * Bump kubevirtci
  * tests, job: Use status condition to detect success/failure
  * use status updater to abstract enable/disable of VM status subresource
  * have to call UpdateStatus as well as Update otherwise status does not get updated, duh
  * UpdateStatus was not sufficient for certain snapshot controller updates
  * tests, console_test: use safe expect batcher
  * A low value of timeout in test setup causes failure in Azure.
  * Remove hidden `make generate` invocations
  * tests: change ping to use RetValue and PromptExpression
  * Test improvements: Use job instead of pod and fail fast while waiting for job.
  * tests: utils.RetValue no need to pass prompt
  * Remove domain label from VMI metrics
  * network: Add network-reviewers group
  * network: Move PodIP status test to network package
  * Fix clock timezone
  * set schedulable to true to test node-controller will respond to out of date heartbeat
  * add e2e test for virt-handler schedulable=false
  * virt-handler mark node as unschedulable until it is able to talk with kubelet
  * tests, ping: Extend the ping helper and generalize it
  * Check if the socket exists and not if the base directory exists
  * [virt-hanlder] test probing of cmd server socket
  * [virt-handler] test contanerDisk readiness checks
  * tests: [test_id:1778] remove redundant `sudo` and wait for prompt
  * tests: ExpectBatchWithValidatedSend error on BatchExpect other than BExp
  * [virt-handler] wait for containerDisks to become ready
  * [virt-handler] let virt-handler probe for virt-launcher readiness
  * [virt-launcher] Replace --readiness-file logic with socket moving
  * [virt-controller] Remove readiness probes and --readiness-file flag
  * Remove exec readiness probe on the containerDisk container
  * tests, ping: Use tests.PingFromVMConsole directly
  * tests, ping: Move the ping helper to the tests package
  * Add test approvers
  * Let prow run make generate instead of travis
  * tests: avoid line wrap on fedora console
  * tests, Fix test 1780 of vmi_networking_test.go
  * Unit test for ensuring local cleanup of vmi does not occur on non finalized vmi
  * Do not perform local cleanup of vmi until vmi is in a finalized state
  * network: Add dedicated network tests module
  * Add support to configure vmi disk I/O mode options
  * Add openapi validatior unit tests
  * tests: Remove redundant string declarment in RetValue arguments
  * tests: Rename tests.Retcode to tests.RetValue
  * test: Fix flaky test for "A long running process"
  * test: Removing redundent \n send from test_id:1779
  * test: Fix falkiness in guest memory failing tests and skip failing one
  * tests: Add missing `\n` to expect.BSnd to test_id:1753
  * Shorten the release job exectuion time on travis
  * k8s-reporter: get all config-map
  * tests: `GenerateHelloWorldServer` use `ExpectBatchWithValidatedSend`
  * tests: Avoid squential expect.BExp in test_id:1778
  * tests: Remove un-needed \n send from "Checking console text" expecter
  * tests: using `Retcode` to check the result of "echo $?"
  * tests: Changing `retcode` to contain the prompt
  * tests: Using ExpectBatchWithValidatedSend instead of expecter.ExpectBatch
  * test: Configure console on login
  * tests: Intorduce safe ExpectBatchWithValidatedSend
  * Bump kubevirtci to support dual stack on k8s-1.18
  * Let virt-operator roll out the status subresource activation
  * Enable the status subresource feature for the CRDs
  * Let virt-controller use the new UpdateStatus client functions
  * Make use of the /status subresource in the virt-api subresources
  * Add validation webhooks for /status updates
  * Add status updater helper functions
  * Add UpdateStatus and PatchStatus to the kubevirt client
  * vmiMetrics struct was recreated with better attributes
  * tests: Create containerdisk sub-package
  * tests: Create flags sub-package
  * Give the VM rename operation more time to create a new VM
  * Expose guest swap metrics
  * Use 'kill' instead of 'killall' for libvirtd in func test

* Fri Sep 11 2020 dmueller@suse.com
- add license/readmes
- Update to version 0.32.0:
  * Shorten the release job exectuion time on travis
  * libvirt expects memory value in bytes to be provided with correct units
  * Bump kubevirtci
  * flaky-finder: fix leading pipe bug
  * tests: skip dmidecode tests on ipv6 lanes
  * code inspection changes
  * Add unit test to verify domain resync period
  * Add resync period for syncing domains in virt-handler from each virt-launcher
  * tests: fix string equality tests
  * tests, vmi_config: Fix expecter false positives In these tests, BExp-ecting "pass" always worked,   because the command line was matched. Splitting the word in 2 on the command line ensures   the match to happen (or not) in the result. Also removed unused 'fail' echos.
  * virtctl cli error handling
  * Re-enabling test pointing to #2272

* Tue Jul 28 2020 James Fehlig <jfehlig@suse.com>
- spec: Add 'ExclusiveArch: x86_64' since currently kubevirt only
  builds for x86_64

* Wed Jul 22 2020 James Fehlig <jfehlig@suse.com>
- Split out container-disk to a separate package since it is used
  by virt-handler and virt-launcher

* Mon Jul 20 2020 James Fehlig <jfehlig@suse.com>
- Update to 0.31.0
  Dropped rename-chroot.patch since the upstream variant is included
  in this release

* Fri Jun 26 2020 James Fehlig <jfehlig@suse.com>
- Rename chroot utility to virt-chroot

* Wed Jun 24 2020 James Fehlig <jfehlig@suse.com>
- Add container-disk to virt-handler package

* Tue Jun 23 2020 James Fehlig <jfehlig@suse.com>
- Update to 0.30.0
  Dropped build-fix.patch since the upstream variant is included
  in this release

* Mon Jun 22 2020 James Fehlig <jfehlig@suse.com>
- Add building of virt-launcher

* Thu May 28 2020 James Fehlig <jfehlig@suse.com>
- Add building of virt-handler and virt-operator

* Mon May 11 2020 James Fehlig <jfehlig@suse.com>
- Add building of virt-api and virt-controller
- Fix build
  build-fix.patch

* Wed May  6 2020 James Fehlig <jfehlig@suse.com>
- Initial attempt to package kubevirt 0.29.0
