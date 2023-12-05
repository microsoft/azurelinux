#
# spec file for package containerized-data-importer
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
Name:           containerized-data-importer
Version:        1.57.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Packages
URL:            https://github.com/kubevirt/containerized-data-importer
Source0:        https://github.com/kubevirt/containerized-data-importer/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  golang
BuildRequires:  golang-packaging
BuildRequires:  libnbd-devel
BuildRequires:  pkgconfig
BuildRequires:  rsync
BuildRequires:  sed
Provides:       cdi = %{version}-%{release}
ExclusiveArch:  x86_64 aarch64

%description
Containerized-Data-Importer (CDI) is a persistent storage management add-on for Kubernetes

%package        api
Summary:        CDI API server
Group:          System/Packages
Provides:       cdi-apiserver = %{version}-%{release}

%description    api
The containerized-data-importer-api package provides the kubernetes API extension for CDI

%package        cloner
Summary:        Cloner for host assisted cloning
Group:          System/Packages

%description    cloner
Source and Target cloner image for host assisted cloning

%package        controller
Summary:        Controller for the data fetching service
Group:          System/Packages

%description    controller
Controller for the data fetching service for VM container images

%package        importer
Summary:        Data fetching service
Group:          System/Packages
Requires:       nbdkit

%description    importer
Data fetching service for VM container imagess

%package        operator
Summary:        Operator for the data fetching service
Group:          System/Packages

%description    operator
Operator for the data fetching service for VM container images

%package        uploadproxy
Summary:        Upload proxy for the data fetching service
Group:          System/Packages

%description    uploadproxy
Upload proxy for the data fetching service for VM container images

%package        uploadserver
Summary:        Upload server for the data fetching service
Group:          System/Packages

%description    uploadserver
Upload server for the data fetching service for VM container images

%package        manifests
Summary:        YAML manifests used to install CDI
Group:          System/Packages

%description    manifests
This contains the built YAML manifests used to install CDI into a
kubernetes installation with kubectl apply.

%prep
# Unpack the sources respecting the GOPATH directory structure expected by the
# go imports resolver. I.e. if DIR is in GOPATH then DIR/src/foo/bar can be
# imported as "foo/bar". The same 'visibility' rules apply to the local copies
# of external dependencies placed in 'vendor' directory when imported from the
# 'parent' package.
#
# Note: having bar symlink'ed to DIR/src/foo/bar does not seem to work. Looks
# like symlinks in go path are not resolved correctly. Hence the sources need
# to be 'physically' placed into the proper location.
%setup -q -n go/src/kubevirt.io/%{name} -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build

export GOPATH=%{_builddir}/go
export GOFLAGS+="-buildmode=pie -mod=vendor"
env \
CDI_SOURCE_DATE_EPOCH="$(date -r LICENSE +%s)" \
CDI_GIT_COMMIT='v%{version}' \
CDI_GIT_VERSION='v%{version}' \
CDI_GIT_TREE_STATE="clean" \
./hack/build/build-go.sh build \
	cmd/cdi-apiserver \
	cmd/cdi-cloner \
	cmd/cdi-controller \
	cmd/cdi-importer \
	cmd/cdi-uploadproxy \
	cmd/cdi-uploadserver \
	cmd/cdi-operator \
	%{nil}

./hack/build/build-manifests.sh

%install
mkdir -p %{buildroot}%{_bindir}

install -p -m 0755 _out/cmd/cdi-apiserver/cdi-apiserver %{buildroot}%{_bindir}/virt-cdi-apiserver

install -p -m 0755 cmd/cdi-cloner/cloner_startup.sh %{buildroot}%{_bindir}/
install -p -m 0755 _out/cmd/cdi-cloner/cdi-cloner %{buildroot}%{_bindir}/

install -p -m 0755 _out/cmd/cdi-controller/cdi-controller %{buildroot}%{_bindir}/virt-cdi-controller

install -p -m 0755 _out/cmd/cdi-importer/cdi-importer %{buildroot}%{_bindir}/virt-cdi-importer

install -p -m 0755 _out/cmd/cdi-operator/cdi-operator %{buildroot}%{_bindir}/virt-cdi-operator

install -p -m 0755 _out/cmd/cdi-uploadproxy/cdi-uploadproxy %{buildroot}%{_bindir}/virt-cdi-uploadproxy

install -p -m 0755 _out/cmd/cdi-uploadserver/cdi-uploadserver %{buildroot}%{_bindir}/virt-cdi-uploadserver

# Install release manifests
mkdir -p %{buildroot}%{_datadir}/cdi/manifests/release
install -m 0644 _out/manifests/release/cdi-operator.yaml %{buildroot}%{_datadir}/cdi/manifests/release/
install -m 0644 _out/manifests/release/cdi-cr.yaml %{buildroot}%{_datadir}/cdi/manifests/release/

%files api
%license LICENSE
%doc README.md
%{_bindir}/virt-cdi-apiserver

%files cloner
%license LICENSE
%doc README.md
%{_bindir}/cloner_startup.sh
%{_bindir}/cdi-cloner

%files controller
%license LICENSE
%doc README.md
%{_bindir}/virt-cdi-controller

%files importer
%license LICENSE
%doc README.md
%{_bindir}/virt-cdi-importer

%files operator
%license LICENSE
%doc README.md
%{_bindir}/virt-cdi-operator

%files uploadproxy
%license LICENSE
%doc README.md
%{_bindir}/virt-cdi-uploadproxy

%files uploadserver
%license LICENSE
%doc README.md
%{_bindir}/virt-cdi-uploadserver

%files manifests
%license LICENSE
%doc README.md
%dir %{_datadir}/cdi
%dir %{_datadir}/cdi/manifests
%dir %{_datadir}/cdi/manifests/release
%{_datadir}/cdi/manifests

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.57.0-1
- Auto-upgrade to 1.57.0 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.55.0-16
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.55.0-15
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.55.0-14
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.55.0-13
- Bump release to rebuild with go 1.19.11

* Tue Jun 27 2023 Vince Perri <viperri@microsoft.com> - 1.55.0-12
- Add nbkdit as a dependency for the importer

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.55.0-11
- Bump release to rebuild with go 1.19.10

* Fri May 26 2023 Aditya Dubey <adityadubey@microsoft.com> - 1.55.0-0
- Update to verion 1.55.0

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.51.0-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.51.0-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.51.0-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.51.0-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.51.0-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.51.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.51.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Ameya Usgaonkar <ausgaonkar@microsoft.com> - 1.51.0-3
- Shorthand nomenclature for containerized-data-importer (cdi)
- Provide api as apiserver

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.51.0-2
- Bump release to rebuild against Go 1.18.5

* Wed Aug 3 2022 Ameya Usgaonkar <ausgaonkar@microsoft.com> - 1.51.0-1
- Initial changes to build for Mariner
- License verified
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)

* Fri Jul 15 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.51.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.51.0

* Tue Jun 21 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.50.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.50.0

* Tue May 31 2022 Caleb Crane <caleb.crane@suse.com>
- Update to version 1.49.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.49.0

* Mon Apr 25 2022 Caleb Crane <caleb.crane@suse.com>
- Update to version 1.48.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.48.0

* Mon Apr 11 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.47.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.47.0

* Fri Apr  1 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.46.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.46.0

* Thu Mar 10 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.45.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.45.0

* Fri Feb  4 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Pack only cdi-{cr,operator}.yaml into the manifests RPM

* Tue Feb  1 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.44.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.44.0

* Thu Jan 13 2022 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Enable build on aarch64

* Mon Jan 10 2022 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.43.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.43.0

* Sun Dec 19 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.42.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.42.0

* Fri Nov 26 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Detect SLE15 SP4 build environment

* Fri Nov 12 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.41.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.41.0

* Mon Oct 11 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.40.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.40.0

* Tue Aug 10 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.37.1
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.37.1

* Mon Jul 12 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.36.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.36.0

* Wed Jun 30 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Generate meta info for containers during rpm build

* Mon Jun 14 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Use registry.suse.com as the default fallback for sle
- Rename macro registry_path to kubevirt_registry_path
- Update to version 1.35.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.35.0

* Fri Jun  4 2021 Fabian Vogt <fvogt@suse.com>
- Add REGISTRY variable

* Thu May 20 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update to version 1.34.0
  Release notes https://github.com/kubevirt/containerized-data-importer/releases/tag/v1.34.0

* Thu May 20 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Disable changelog generation via tar_scm service (too verbose)

* Thu Apr 29 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Include release number into docker tag
- Add cdi_containers_meta build service

* Thu Apr 29 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Set default reg_path='registry.opensuse.org/kubevirt'
- Add _constraints file with disk requirements
- Drop CDI_VERSION env var since its not used during the build

* Wed Apr 21 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Preparation for submission to SLE15 SP2
  jsc#SLE-11089 jsc#ECO-3633

* Thu Apr 15 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Drop csv-generator

* Wed Apr  7 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Update registry path

* Fri Mar  5 2021 Vasily Ulyanov <vasily.ulyanov@suse.com>
- Fix import of vendor dependencies
  * Arrange the directory layout in buildroot
  * Drop manifest-build-fix.patch
  * Switch to Go 1.14 (used for upstream builds)

* Fri Feb 26 2021 James Fehlig <jfehlig@suse.com>
- Add a manifests package containing YAML manifests used to
  install CDI
  manifest-build-fix.patch

* Wed Feb 24 2021 jfehlig@suse.com
- Update to version 1.30.0:
  * Release to quay.io instead of docker (#1635)
  * Preallocation test did not run all scenarios (#1625)
  * Add diagnostic to flake test (#1626)
  * VDDK: avoid crash when specified disk isn't in VM. (#1639)
  * rename importController to uploadController in the upload-controller.go file (#1632)
  * Simplify shouldReconcile function arguments. (#1602)
  * Increase polling interval for upload annotation test (#1630)
  * Remove note about VDDK 7 restriction. (#1631)
  * Remove OLM integration code not removed in #982 (#1624)
  * Fix typos in doc/datavolumes.md (#1621)
  * Support cloning from Filesystem to Block and vice-versa (#1597)
  * Add error to DV when VDDK configmap is missing. (#1627)
  * Add focus for destructive tests. (#1614)
  * Wait for clone to succeed before checking MD5. (#1601)
  * doc: update url in doc/datavolumes.md. (#1609)
  * Enable tests for featuregates (#1600)
  * Make string we are checking for less specific to allow it pass for other platforms. (#1580)
  * Validate image fits in filesystem in a lot more cases. take filesystem overhead into account when resizing. (#1466)
  * Try to use the CDIConfig proxy URL if it is set, if not use port-forward (#1598)
  * Update kubevirtci (#1579)
  * Replaced file copying code with an existing utility function. (#1585)
  * Global preallocation setting is not taken into account correctly. (#1565)
  * Retry finding the pods for looking up the annotations. (#1583)
  * Make DeletePodByName always wait for the pod to stop existing. (#1584)
  * When cleaning up NFS disks, recursively delete their contents. (#1576)
  * Typedef for preallocation status (#1568)
  * Add Data Volume annotations documentation (#1582)
  * core: Preallocate blank block volumes (#1559)
  * Skip test 2555 if running on openshift (#1572)

* Tue Jan 26 2021 jfehlig@suse.com
- Update to version 1.29.0:
  * Document smartclone disable feature in markdown (#1571)
  * update cdi config docs (#1556)
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../containerized-data-importer/WORKSPACE -dry-run=false (#1569)
  * Reduce the noise from the filesystem overhead functionality (#1558)
  * VDDK: work with block devices better (BZ 1913756). (#1564)
  * Add a DV/PVC annotation "storage.bind.immediate.requested" (#1560)
  * Use nbdkit for direct stream for the http importer  (#1508)
  * Text-only changes missed in removing the Process phase (#1446) (#1562)
  * Compare logs while ignoring differences in spaces. (#1557)
  * update api for cert configuration (#1542)
  * core: Preallocate blank image disks as well (#1555)
  * Preallocation check all paths (#1535)
  * Remove temporary approver status.
  * Change verbosity for preallocation messages, avoid possible infinite loop (#1551)
  * Add test ids to strict reconciliation tests (#1546)
  * VDDK: more reliable transfers of full disks. (#1547)
  * Stop Using Deprecated Packages (#1548)
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../containerized-data-importer/WORKSPACE -dry-run=false (#1543)
  * Preallocation support (#1498)
  * VDDK: incremental copy with changed block tracking (#1517)
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/kubevirt/project-infra/../containerized-data-importer/WORKSPACE -dry-run=false (#1536)
  * Add maya-r to approver list.
  * Simplify file host, now a new image only has to be added to bazel. (#1534)
  * Update fedora 33 (#1486)
  * Allow passing default multus network annotation to transfer pods (#1532)
  * Try updating the node taint in a loop (#1510)
  * Add an API for disabling smart-cloning. (#1461)
  * Read-only clone source pods (#1524)
  * Clone source program calls tar instead of getting piped input.  This ensures we trap tar errors. (#1521)
  * Add strict reconciliation tests (#1505)
  * Allow specifying of the CONTAINER_DISK_IMAGE with a default of the current value. (#1515)
  * Designate CDI as CDIConfig authority (#1516)
  * Update builder to fedora 33 (#1511)
  * In the operator test there is a critical addons test that removes and (#1513)
  * Create a Datavolume if a coliding PVC with same name exists but is marked to delete (#1477)
  * Fix make target cluster-sync-cdi, add cluster-clean-cdi & cluster-clean-test-infra (#1503)
  * increase code coverage by moving utility functions from api packages (#1479)
  * Pass specific PVC annotations to the transfer pods (#1480)
  * Move configure_storage to test setup. (#1484)
  * Make sure the DV is the main resource and single source of truth for WaitForFirstConsumer. (#1499)
  * Controller support for Multistage Imports (#1450)
  * Pull less from dockerhub when running testsuite (#1478)
  * apiserver should serve up openapi spec (#1485)
  * VDDK: Add more debug logging around nbdkit. (#1465)
  * k8s-reporter: Add Endpoints logging (#1481)
  * Add CDIConfig to CDI (#1475)
  * Run bazelisk run //plugins/cmd/uploader:uploader -- -workspace /home/prow/go/src/github.com/fgimenez/project-infra/../../kubevirt/containerized-data-importer/WORKSPACE -dry-run=false
  * Wait for stray pods to terminate, destroy/re-create at AfterEach. (#1459)
  * Remove the "Process" data processor phase, simplify state machine. (#1446)
  * Scratch import bug (#1424)
  * Dump service resources after failed tests (#1463)
  * VDDK: replace qemu-img with libnbd (#1448)
  * update kubevirtci (#1457)
  * Update WORKSPACE packages to non-404 ones, and add a second mirror. (#1444)
  * Don't wait for NS to deleted in test before starting next test (#1439)

* Tue Oct 27 2020 James Fehlig <jfehlig@suse.com>
- spec: Fix binary names for several CDI components

* Mon Oct 26 2020 jfehlig@suse.com
- Update to version 1.25.0:
  * Update builder image to add libnbd (#1452)
  * Add make targets cluster-sync-cdi & cluster-sync-test-infra (#1451)
  * Add library function to determine if a PVC is waiting for first consu… (#1442)
  * Add test_ids for the tests (#1441)
  * Retry upload in case upload pod wasn't 100%% ready when attempting upload (#1440)
  * add finalizer to target PVC before creating clone source pod (#1429)
  * Make CDI infra deployments as critical addons. (#1361)
  * Fix cloning checking fsGroup test in case of use with OCS. (#1435)
  * Fix types.go vs code schema verification to actually fail if they are different. (#1428)
  * Add files used in OpenShift CI. (#1416)
  * Retry upload in case upload pod wasn't 100%% ready when attempting upload (#1437)
  * Check for expected changes after CDI upgrade (#1417)
  * Files in tar archives can have paths relative to ./ (#1432)
  * Attempt to schedula clone sourc/target pods on same node (#1426)
  * Touch ups for filesystem overhead test cases (#1427)
  * Fix imports for images with no info about MediaType. (#1413)
  * Fix size mismatch between source and target in smart clone tests. Ceph no longer (#1421)
  * use snappy compression for cloning instead of gzip (#1419)
  * Update to k8s.io/klog/v2, used by kubernetes 1.19 (#1409)

* Fri Oct 23 2020 jfehlig@suse.com
- Update to version 1.24.0:
  * add system:authorized to groups checked for clone auth (#1415)
  * Fixing CDIStatus generate-verify issues (#1412)
  * Reserve overhead when validating that a Filesystem has enough space (#1319)
  * Test behavior after client-side upload failure. (#1404)
  * Removed hard coded registry:5000 for vddk datasource test. (#1402)
  * Add library function to determine if a PVC has been populated fully. (#1400)
  * Remove dependency update when building the OR CI build image (#1386)
  * Add test_id for the test cases (#1398)
  * Fix incorrect region parsing from aws s3 endpoint (#1395)
  * Add functional test for cloning if source NS has enought quota and (#1387)

* Fri Oct 23 2020 James Fehlig <jfehlig@suse.com>
- Initial attempt at packaging CDI
