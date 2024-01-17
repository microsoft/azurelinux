#
# spec file for package rook
#
# Copyright (c) 2021 SUSE LLC
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


Summary:        Orchestrator for distributed storage systems in cloud-native environments
Name:           rook
Version:        1.6.2
Release:        15%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Filesystems
URL:            https://rook.io/
#Source0:       https://github.com/rook/rook/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/rook/rook/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz
Source98:       README
Source99:       update-tarball.sh
# When possible, a patch is preferred over link-time overrides because the patch will fail if the
# upstream source is updated without the package maintainers knowing. Patches reduce user error when
# creating a new SUSE release branch of Rook.
# Change the default FlexVolume dir path to support Kubic.
Patch0:         flexvolume-dir.patch
# Ceph version is needed to set correct container tag in manifests
BuildRequires:  ceph
# Rook requirements
BuildRequires:  curl
BuildRequires:  git
BuildRequires:  golang
# Go and spec requirements
BuildRequires:  golang-packaging
BuildRequires:  grep
BuildRequires:  xz
# From Ceph base container: github.com/ceph/ceph-container/src/daemon-base/...
Requires:       patterns-ceph-containers-ceph_base
# Rook runtime requirements - referenced from packages installed in Rook images
# From images/ceph/Dockerfile
Requires:       tini

%description
Rook is a cloud-native storage orchestrator for Kubernetes, providing
the platform, framework, and support for a diverse set of storage
solutions to integrate with cloud-native environments.

See https://github.com/rook/rook for more information.

################################################################################
# Rook FlexVolume driver metadata
################################################################################
%package rookflex
Summary:        Rook FlexVolume driver
Group:          System/Filesystems

%description rookflex
Rook uses FlexVolume to integrate with Kubernetes for performing storage
operations.

################################################################################
# Rook and Ceph manifests metadata
################################################################################
%package k8s-yaml
Summary:        Kubernetes YAML file manifests for deploying a Ceph cluster
Group:          System/Management
BuildRequires:  ceph
BuildArch:      noarch

%description k8s-yaml
This package contains examples of yaml files required to deploy and run the
Rook-Ceph operator and Ceph clusters in a Kubernetes cluster.

################################################################################
# Rook ceph operator helm charts
################################################################################
%package ceph-helm-charts
Summary:        Rook Ceph operator helm charts
Group:          System/Management
BuildArch:      noarch

%description ceph-helm-charts
Helm helps manage Kubernetes applications. Helm Charts define,
install, and upgrade Kubernetes applications. Rook is a
cloud-native storage orchestrator for Kubernetes, providing
the platform, framework, and support for a diverse set of storage
solutions to integrate with cloud-native environments.

This package contains Helm Charts for Rook.

################################################################################
# Build section
################################################################################
%define _buildshell /bin/bash

%prep
%autosetup -p1
tar -xf %{SOURCE1} --no-same-owner

%build
# remove symbols unsupported by k8s (+) from version
version_full=%{version}
version_noplus="${version_full//[+]/_}"
%global version_parsed "${version_noplus}-%{release}"

linker_flags=(
    # Set Rook version - absolutely required
    "-X" "github.com/rook/rook/pkg/version.Version=%{version_parsed}"
)
build_flags=("-ldflags" "${linker_flags[*]}" "-mod=vendor" "-v" "-a")

for cmd in cmd/* ; do
  go build "${build_flags[@]}" -o $(basename $cmd) ./$cmd
done

%install
rook_bin_location=$PWD/
install_location=%{buildroot}%{_bindir}

install --mode=755 --directory "${install_location}"

for binary in rook rookflex ; do
    install --preserve-timestamps --mode=755 \
        --target-directory="${install_location}" \
        "${rook_bin_location}"/"${binary}"
done

# install Rook's toolbox script alongside main binary
install --preserve-timestamps --mode=755 \
    --target-directory="${install_location}" \
    images/ceph/toolbox.sh

# Install ALL sample yaml files
mkdir -p %{buildroot}%{_datadir}/k8s-yaml/rook/ceph
cp -pr cluster/examples/kubernetes/ceph/* %{buildroot}%{_datadir}/k8s-yaml/rook/ceph/
# Include ceph/csi directory, but move templates to /etc
cp -pr cluster/examples/kubernetes/ceph/csi %{buildroot}%{_datadir}/k8s-yaml/rook/ceph/
mkdir -p %{buildroot}%{_sysconfdir}/ceph-csi
mv %{buildroot}%{_datadir}/k8s-yaml/rook/ceph/csi/template/* %{buildroot}%{_sysconfdir}/ceph-csi/
rmdir %{buildroot}%{_datadir}/k8s-yaml/rook/ceph/csi/template
# Remove the flex directory as this is not supported at all
rm -rf %{buildroot}%{_datadir}/k8s-yaml/rook/ceph/flex

################################################################################
# Check that linker flags are applied
################################################################################
# re-set version variables to match those used in the build step
# remove symbols unsupported by k8s (+) from version
version_full=%{version}
version_noplus="${version_full//[+]/_}"
%global version_parsed "${version_noplus}-%{release}"
# strip off everything following + for the helm appVersion
%global helm_appVersion "${version_full%+*}"
%global helm_version "%{helm_appVersion}-%{RELEASE}"

# Check Rook version is properly set
rook_bin="$rook_bin_location"rook
bin_version="$("$rook_bin" version)"

if [[ ! "$bin_version" =~ "$version" ]]; then
    echo "Rook version not set correctly!"
    exit 1
fi

################################################################################
# Update manifests with images coming from Build Service
################################################################################
# set rook, ceph and ceph-csi container versions
sed -i -e "s|%{_prefix}/local/bin/toolbox.sh|%{_bindir}/toolbox.sh|g" %{buildroot}%{_datadir}/k8s-yaml/rook/ceph/toolbox*

# Install the helm charts
%define chart_yaml "%{buildroot}%{_datadir}/%{name}-ceph-helm-charts/operator/Chart.yaml"
%define values_yaml "%{buildroot}%{_datadir}/%{name}-ceph-helm-charts/operator/values.yaml"
mkdir -p %{buildroot}%{_datadir}/%{name}-ceph-helm-charts/operator
cp -pr cluster/charts/rook-ceph/* %{buildroot}%{_datadir}/%{name}-ceph-helm-charts/operator
# Copy example manifests to chart directory
mkdir %{buildroot}%{_datadir}/%{name}-ceph-helm-charts/operator/examples
cp -pr %{buildroot}%{_datadir}/k8s-yaml/rook/ceph/*  %{buildroot}%{_datadir}/%{name}-ceph-helm-charts/operator/examples
# appVersion should being with a 'v', even though the image tag currently does not
sed -i -e "/apiVersion/a appVersion: v%{helm_appVersion}" %{chart_yaml}
sed -i -e "s|\(version: \).*|\1%{helm_version}|" %{chart_yaml}
sed -i -e "s|\(.*tag: \)VERSION|\1%{helm_appVersion}|" %{values_yaml}

################################################################################
# Specify which files we built belong to each package
################################################################################
%files
%defattr(-,root,root,-)
%{_bindir}/rook
%{_bindir}/toolbox.sh
%config %{_sysconfdir}/ceph-csi
# Due to upstream's use of /usr/local/bin in their example yamls, create
# symlinks to avoid a difficult to find configuration problem
%post
[[ -e %{_prefix}/local/bin/toolbox.sh ]] || ln -s %{_bindir}/toolbox.sh %{_prefix}/local/bin/toolbox.sh
[[ -e %{_prefix}/local/bin/rook ]] || ln -s %{_bindir}/rook %{_prefix}/local/bin/rook

%postun
[[ -e %{_prefix}/local/bin/toolbox.sh ]] && rm %{_prefix}/local/bin/toolbox.sh
[[ -e %{_prefix}/local/bin/rook ]] && rm %{_prefix}/local/bin/rook

%files rookflex
%{_bindir}/rookflex

%files k8s-yaml
%dir %{_datarootdir}/k8s-yaml
%dir %{_datarootdir}/k8s-yaml/rook
%dir %{_datarootdir}/k8s-yaml/rook/ceph
%{_datadir}/k8s-yaml/rook/ceph/

%files ceph-helm-charts
%doc %{_datadir}/%{name}-ceph-helm-charts/operator/README.md
%{_datadir}/%{name}-ceph-helm-charts

################################################################################
# Finalize
################################################################################

# Rook RPMs aren't for users to install, just to be put in containers, so don't
# bother adding docs or changelog or anything

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-15
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.6.2-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.6.2-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.6.2-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.6.2-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.6.2-2
- Bump release to rebuild with golang 1.18.3

* Wed Sep 22 2021 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.6.2-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Remove unused/un-supported macro usage
- Remove opensuse specific csi build flags
- Remove integration test binaries and package

* Fri May  7 2021 Stefan Haas <stefan.haas@suse.com>
- Update to v1.6.2
  * Set base Ceph operator image and example deployments to v16.2.2
  * Update snapshot APIs from v1beta1 to v1
  * Documentation for creating static PVs
  * Allow setting primary-affinity for the OSD
  * Remove unneeded debug log statements
  * Preserve volume claim template annotations during upgrade
  * Allow re-creating erasure coded pool with different settings
  * Double mon failover timeout during a node drain
  * Remove unused volumesource schema from CephCluster CRD
  * Set the device class on raw mode osds
  * External cluster schema fix to allow not setting mons
  * Add phase to the CephFilesystem CRD
  * Generate full schema for volumeClaimTemplates in the CephCluster CRD
  * Automate upgrades for the MDS daemon to properly scale down and scale up
  * Add Vault KMS support for object stores
  * Ensure object store endpoint is initialized when creating an object user
  * Support for OBC operations when RGW is configured with TLS
  * Preserve the OSD topology affinity during upgrade for clusters on PVCs
  * Unify timeouts for various Ceph commands
  * Allow setting annotations on RGW service
  * Expand PVC size of mon daemons if requested
- Update to v1.6.1
  * Disable host networking by default in the CSI plugin with option to enable
  * Fix the schema for erasure-coded pools so replication size is not required
  * Improve node watcher for adding new OSDs
  * Operator base image updated to v16.2.1
  * Deployment examples updated to Ceph v15.2.11
  * Update Ceph-CSI to v3.3.1
  * Allow any device class for the OSDs in a pool instead of restricting the schema
  * Fix metadata OSDs for Ceph Pacific
  * Allow setting the initial CRUSH weight for an OSD
  * Fix object store health check in case SSL is enabled
  * Upgrades now ensure latest config flags are set for MDS and RGW
  * Suppress noisy RGW log entry for radosgw-admin commands
- Update to v1.6.0
  * Removed Storage Providers
  * CockroachDB
  * EdgeFS
  * YugabyteDB
  * Ceph
  * Support for creating OSDs via Drive Groups was removed.
  * Ceph Pacific (v16) support
  * CephFilesystemMirror CRD to support mirroring of CephFS volumes with Pacific
  * Ceph CSI Driver
  * CSI v3.3.0 driver enabled by default
  * Volume Replication Controller for improved RBD replication support
  * Multus support
  * GRPC metrics disabled by default
  * Ceph RGW
  * Extended the support of vault KMS configuration
  * Scale with multiple daemons with a single deployment instead of a separate deployment for each rgw daemon
  * OSDs
  * LVM is no longer used to provision OSDs
  * More efficient updates for multiple OSDs at the same time
  * Multiple Ceph mgr daemons are supported for stretch clusters
    and other clusters where HA of the mgr is critical (set count: 2 under mgr in the CephCluster CR)
  * Pod Disruption Budgets (PDBs) are enabled by default for Mon,
    RGW, MDS, and OSD daemons. See the disruption management settings.
  * Monitor failover can be disabled, for scenarios where
    maintenance is planned and automatic mon failover is not desired
  * CephClient CRD has been converted to use the controller-runtime library

* Wed Apr 21 2021 Stefan Haas <stefan.haas@suse.com>
- Update to v1.5.10
  * Ceph
  * Update Ceph-CSI to v3.2.1 (#7506)
  * Use latest Ceph API for setting dashboard and rgw credentials (#7641)
  * Redact secret info from reconcile diffs in debug logs (#7630)
  * Continue to get available devices if failed to get a device info (#7608)
  * Include RGW pods in list for rescheduling from failed node (#7537)
  * Enforce pg_auto_scaler on rgw pools (#7513)
  * Prevent voluntary mon drain while another mon is failing over (#7442)
  * Avoid restarting all encrypted OSDs on cluster growth (#7489)
  * Set secret type on external cluster script (#7473)
  * Fix init container "expand-encrypted-bluefs" for encrypted OSDs (#7466)
  * Fail pool creation if the sub failure domain is the same as the failure domain (#7284)
  * Set default backend for vault and remove temp key for encrypted OSDs (#7454)

* Wed Mar  3 2021 Stefan Haas <stefan.haas@suse.com>
- Update to v1.5.7
  * Ceph
  * CSI Troubleshooting Guide (#7157)
  * Print device information in OSD prepare logs (#7194)
  * Expose vault curl error in the OSD init container for KCS configurations (#7193)
  * Prevent re-using a device to configure an OSD on PVC from a previous cluster (#7170)
  * Remove crash collector if all Ceph pods moved off a node (#7160)
  * Add helm annotation to keep CRDs in the helm chart during uninstall (#7162)
  * Bind mgr modules to all interfaces instead of pod ip (#7151)
  * Check for orchestration cancellation while waiting for all OSDs to start (#7112)
  * Skip pdb reconcile on create and delete events (#7155)
  * Silence harmless errors in log when the operator is still initializing (#7056)
  * Add --extra-create-metadata flag to the CSI driver (#7147)
  * Add deviceClass to the object store schema (#7132)
  * Simplify the log-collector container name (#7133)
  * Skip csi detection if CSI is disabled (#6866)
  * Remove Rook pods stuck in terminating state on a failed node (#6999)
  * Timeout for rgw configuration to prevent stuck object store when no healthy OSDs (#7075)
  * Update lib bucket provisioner for OBCs (#7086)
- Drop csi-images-SUSE.patch

* Wed Nov 18 2020 Mike Latimer <mlatimer@suse.com>
- Derive CSI and sidecar image versions from code defaults rather
  than images found in the build service

* Fri Nov  6 2020 Mike Latimer <mlatimer@suse.com>
- Update to v1.4.7
  * Ceph
  * Log warning about v14.2.13 being an unsupported Ceph version due to
    errors creating new OSDs (#6545)
  * Disaster recovery guide for PVCs (#6452)
  * Set the deviceClass for OSDs in non-PVC clusters (#6545)
  * External cluster script to fail if prometheus port is not default (#6504)
  * Remove the osd pvc from the osd purge job (#6533)
  * External cluster script added additional checks for monitoring
    endpoint (#6473)
  * Ignore Ceph health error MDS_ALL_DOWN during reconciliation (#6494)
  * Add optional labels to mon pods (#6515)
  * Assert type for logging errors before using it (#6503)
  * Check for orphaned mon resources with every reconcile (#6493)
  * Update the mon PDBs if the maxUnavailable changed (#6469)
  * NFS
  * Update documentation and examples (#6455)

* Wed Oct 28 2020 Mike Latimer <mlatimer@suse.com>
- Drop OFFSET from cephcsi image tag

* Mon Oct 26 2020 Mike Latimer <mlatimer@suse.com>
- Update helm chart to use appropriate version prefix for the final registry
  destination (e.g. registry.suse.com or registry.opensuse.org)
- Improve consistency with image tags

* Tue Oct 20 2020 Mike Latimer <mlatimer@suse.com>
- Update to v1.4.6
  * Support IPv6 single-stack (#6283)
  * Only start a single CSI provisioner in single-node test clusters (#6437)
  * Raw mode OSD on LV-backed PVC (#6184)
  * Capture ceph-volume detailed log in non-pvc scenario on failure (#6426)
  * Add --upgrade option to external cluster script (#6392)
  * Capture stderr when executing ceph commands and write to log (#6395)
  * Reduce the retry count for the bucket health check for more accurate
    status (#6408)
  * Prevent closing of monitoring channel more than once (#6369)
  * Check underlying block status for encrypted OSDs (#6367)
- Add 'latest' and appVersion tags to helm chart
- Include sample manifests in helm chart

* Fri Oct  9 2020 Mike Latimer <mlatimer@suse.com>
- Set the helm chart version to the rook version

* Tue Oct  6 2020 Mike Latimer <mlatimer@suse.com>
- Minor fix to helm chart to ensure SemVer formatting
- Fix typo in sample cluster.yaml

* Tue Oct  6 2020 Joshua Hesketh <jhesketh@suse.com>
- Update the operator.yaml ConfigMap to reflect the default SUSE images
  that are used rather than upstreams.
- Fix indentation of patch tabs to match original

* Fri Oct  2 2020 Mike Latimer <mlatimer@suse.com>
- Update to v1.4.5
  * Update the CSI driver to v3.1.1 (#6340)
  * Fix drive group deployment failure (#6267)
  * Fix OBC upgrade from 1.3 to 1.4 external cluster (#6353)
  * Remove user unlink while deleting OBC (#6338)
  * Enable RBAC in the helm chart for enabling monitoring (#6352)
  * Disable encryption keyring parameter not necessary after
    opening block (#6350)
  * Improve reconcile performance in clusters with many OSDs on
    PVCs (#6330)
  * Only one external cluster secret supported in import script (#6343)
  * Allow OSD PVC template name to be set to any value (#6307)
  * OSD prepare job was failing due to low aio-max-nr setting (#6284)
  * During upgrade assume a pod spec changed if diff checking fails (#6272)
  * Merge config from rook-config-override configmap to the default global
    config file (#6252)
- Package all sample yaml files in rook-k8s-yaml

* Tue Sep 29 2020 Mike Latimer <mlatimer@suse.com>
- Update helm chart version to match rook product version plus
  the current release number

* Tue Sep 29 2020 Mike Latimer <mlatimer@suse.com>
- Update to v1.4.4
  * Upgrade to v1.4.3 for cluster-on-pvc hung due to changing label
    selectors on the mons (#6256)
  * Remove osd status configmap for nodes with long names (#6235)
  * Allow running rgw daemons from an external cluster (#6226)
- Create symlinks in /usr/local/bin for toolbox.sh and rook to
  ensure compatibility with upstream sample yamls

* Mon Sep 21 2020 Stefan Haas <stefan.haas@suse.com>
- fixed spec-file:
  * operator.yaml does not get changed to use the SUSE-images

* Thu Sep 17 2020 Mike Latimer <mlatimer@suse.com>
- helm chart, manifests:
  * fixed tolerations
  * Update SUSE documentation URL in NOTES.txt

* Thu Sep 17 2020 Mike Latimer <mlatimer@suse.com>
- ceph: fix drive group deployment failure (bsc#1176170)
- helm chart, manifests:
  * Add tolerations to cluster & CRDs
  * Require kubeVersion >= 1.11
  * Use rbac.authorization.k8s.io/v1
  * Add affinities for label schema
  * Set Rook log level to DEBUG
  * Remove FlexVolume agent
  * Require currentNamespaceOnly=true
  * Replace NOTES.txt with SUSE specific version

* Tue Sep 15 2020 Mike Latimer <mlatimer@suse.com>
- Include operator and common yamls in manifest package

* Sat Sep 12 2020 Mike Latimer <mlatimer@suse.com>
- Update to v1.4.3
  * The Ceph-CSI driver was being unexpectedly removed by the garbage
    collector in some clusters. For more details to apply a fix during
    the upgrade to this patch release, see these steps. (#616)
  * Add storageClassDeviceSet label to osd pods (#6225)
  * DNS suffix issue for OBCs in custom DNS suffix clusters (#6234)
  * Cleanup mon canary pvc if the failover failed (#6224)
  * Only enable mgr init container if the dashboard is enabled (#6198)
  * cephobjectstore monitoring goroutine must be stopped during
    uninstall (#6208)
  * Remove NParts and Cache_Size from MDCACHE block in the NFS
    configuration (#6207)
  * Purge a down osd with a job created by the admin (#6127)
  * Do not use label selector on external mgr service (#6142)
  * Allow uninstall even if volumes still exist with a new CephCluster
    setting (#6145)

* Thu Sep 10 2020 Mike Latimer <mlatimer@suse.com>
- Update to v1.4.2
  - Patch release focusing on small feature additions and bug fixes.
  * Improve check for LVM on the host to allow installing of OSDs (#6175)
  * Set the OSD prepare resource limits (#6118)
  * Allow memory limits below recommended settings (#6116)
  * Use full DNS suffix for object endpoint with OBCs (#6170)
  * Remove the CSI driver lifecycle preStop hook (#6141)
  * External cluster optional settings for provisioners (#6048)
  * Operator watches nodes that match OSD placement rules (#6156)
  * Allow user to add labels to the cluster daemon pods (#6084 #6082)
  * Fix vulnerability in package golang.org/x/text (#6136)
  * Add expansion support for encrypted osd on pvc (#6126)
  * Do not use realPath for OSDs on PVCs (#6120, @leseb)
  * Example object store manifests updated for consistency (#6123)
  * Separate topology spread constrinats for osd prepare jobs and
    osd daemons (#6103)
  * Pass CSI resources as strings in the helm chart (#6104)
  * Improve callCephVolume() for list and prepare (#6059)
  * Improved multus support for the CSI driver configuration (#5740)
  * Object store healthcheck yaml examples (#6090)
  * Add support for wal encrypted device on pvc (#6062)
  * Updated helm usage in documentation (#6086)
  * More details for RBD Mirroring documentation (#6083)
- Build process changes:
  - Set CSI sidecar versions through _service, and set all versions in
    code through a single patch file
    + csi-images-SUSE.patch
  - csi-dummy-images.patch
  - Use github.com/SUSE/rook and suse-release-1.4 tag in update.sh
  - Create module dependencies through _service, and store these dependencies
    in vendor.tar.gz (replacing rook-[version]-vendor.tar.xz)
  - Modify build commands to include "-mod=vendor" to use new vendor tarball
  - Add CSI sidecars as BuildRequires, in order to determine versions through
    _service process
  - Replace %%setup of vendor tarball with a simple tar extraction
  - Move registry detection to %%prep, and set correct registry through a
    search and replace on the SUSE_REGISTRY string
  - Use variables to track rook, ceph and cephcsi versions
  - Add '#!BuildTag', and 'appVersion' to chart.yaml
  - Add required versioning to helm chart
  - Leave ceph-csi templates in /etc, and include them in main rook package.
  - csi-template-paths.patch
  - Include only designated yaml examples in rook-k8s-yaml package

* Mon Aug 10 2020 Stefan Haas <stefan.haas@suse.com>
- Update to v1.4.0:
  * Ceph-CSI 3.0 is deployed by default
  * Multi Architecture docker images are published (amd64 and arm64)
  * Create/Delete beta snapshot for RBD, while support for Alpha snapshots is removed.
  * Create PVCs from RBD snapshots and PVCs
  * Support ROX volumes for RBD and CephFS
  * The dashboard for the ceph object store will be enabled if the dashboard module is enabled.
  * An admission controller enhances CRD validations (Experimental)
  * The admission controller is not enabled by default.
  * Support for Ceph CRDs is provided. Some validations for CephClusters are included and a framework for additional validations is in place for other CRDs.
  * RGW Multisite is available through new CRDs for zones, zone groups, and realms. (Experimental)
  * CephObjectStore CRD changes:
  * Health displayed in the Status field
  * Run health checks on the object store endpoint by creating a bucket and writing to it periodically.
  * The endpoint is stored for reference in the Status field
  * OSD changes:
  * OSDs on PVC now support multipath and crypt device types.
  * OSDs on PVC can now be encrypted by setting encrypted: true on the storageClassDeviceSet.
  * OSDs can now be provisioned using Ceph's Drive Groups definitions for Ceph Octopus v15.2.5+.
  * OSDs can be provisioned on the device path such as /dev/disk/by-path/pci-HHHH:HH:HH.H with colons (:)
  * A new CephRBDMirror CR will configure the RBD mirroring daemons. The RBD mirror settings were previously included in the CephCluster CR.
  * Multus support is improved, though still in experimental mode
  * Added support for the Whereabouts IPAM
  * CephCluster CRD changes:
  * Converted to use the controller-runtime framework
  * Added settings to configure health checks as well as pod liveness probes.
  * CephBlockPool CRD has a new field called parameters which allows to set any Ceph pool property on a given pool
  * OBC changes:
  * Updated the lib bucket provisioner version to support multithreading
  * Added support for quota, have options for object count and total size.
  * Prometheus monitoring for external clusters is now possible, refer to the external cluster section
  * The operator will check for the presence of the lvm2 package on the host where OSDs will run. If not available, the prepare job will fail. This will prevent issues of OSDs not restarting on node reboot.
  * Added a new label ceph_daemon_type to Ceph daemon pods.
  * Added a toolbox job example for running a script with Ceph commands, similar to running commands in the Rook toolbox.

* Wed May 27 2020 Stefan Haas <stefan.haas@suse.com>
- Update to v1.3.4:
  * Finalizer for OBC cleanup (#5436)
  * Remove invalid MDS deactivate command during upgrade (#5278)
  * Enable verbose logging for LVM commands (#5515)
  * Set external creds if admin key is available (#5507)
  * Fail more gracefully for an unsupported Ceph version (#5503)
  * Set pg_num_min on new rgw metadata pools (#5489)
  * Object store deployment failed to start on openshift (#5468)
  * Relax OBC error handling and user deletion (#5465)
  * Create missing secret on external cluster (#5450)
  * Python script to generate needed external cluster resources (#5388)
  * Docs: clarify required version of helm for upgrades (#5445)
  * CSI priority class example update (#5443)
  * Set test default pool size to one (#5428)
  * Remove invalid verbose params from lv activate (#5438)

* Wed Apr 22 2020 Stefan Haas <stefan.haas@suse.com>
- Update to v1.3.1:
  * Stop the pool controller from staying in a reconcile loop (#5173)
  * Update the rgw service port during upgrade (#5228)
- Removed orchestrator-cli-rename.patch as it got merged

* Mon Apr 20 2020 Stefan Haas <stefan.haas@suse.com>
- Update to v1.3.0:
  * Ceph: revert mgr to minimal privilege (#5183)
  * Enable the Ceph CSI v2.0.1 driver by default in Rook (#5162)
  * ceph: add liveness probe to mon, mds and osd daemons (#5128)
  * Ceph: prevent pre-existing lvms from wipe (#4966)

* Tue Mar 31 2020 Kristoffer Gronlund <kgronlund@suse.com>
- Update to v1.2.7 (bsc#1168160):
  * Apply the expected lower PG count for rgw metadata pools (#5091)
  * Reject devices smaller than 5GiB for OSDs (#5089)
  * Add extra check for filesystem to skip boot volumes for OSD configuration (#5022)
  * Avoid duplication of mon pod anti-affinity (#4998)
  * Update service monitor definition during upgrade (#5078)
  * Resizer container fix due to misinterpretation of the cephcsi version (#5073-1)
  * Set ResourceVersion for Prometheus rules (#4528)
  * Upgrade doc clarification for RBAC related to the helm chart (#5054)

* Wed Mar 18 2020 Kristoffer Gronlund <kgronlund@suse.com>
- Update to v1.2.6:
  * Update default Ceph version to v14.2.8 (#4960)
  * Fix for OSDs on PVCs that were crashing on Ceph v14.2.8 (#4960)
  * Mount /udev so the osds can discover device info (#5001)
  * Query for the topology.kubernetes.io labels in K8s 1.17 or newer for the CRUSH hierarchy (#4989)
  * Log a warning when useAllNodes is true, but nodes are defined in the cluster CR ([commit](https://github.com/rook/rook/pull/4974/commits/69c9ed4206f47644687733396d87022e93d312a3))

* Tue Mar 10 2020 Kristoffer Gronlund <kgronlund@suse.com>
- ceph: orchestrator cli name change
  * Add orchestrator-cli-rename.patch

* Thu Feb 20 2020 Kristoffer Gronlund <kgronlund@suse.com>
- ceph: populate CSI configmap for external cluster

* Tue Feb 18 2020 Kristoffer Gronlund <kgronlund@suse.com>
- Update to v1.2.4:
  * Stop garbage collector from deleting the CSI driver unexpectedly (#4820)
  * Upgrade legacy OSDs created with partitions created by Rook (#4799)
  * Ability to set the pool target_size_ratio (#4803)
  * Improve detection of drain-canaries and log significant nodedrain scheduling events (#4679)
  * Sort flexvolume docs and update for kubespray (#4747)
  * Add OpenShift common issues documentation (#4764)
  * Improved integration test when cleaning devices (#4796)

* Fri Jan 31 2020 Kristoffer Gronlund <kgronlund@suse.com>
- Package helm charts for the rook operator for ceph (SES-799)

* Mon Jan 27 2020 Kristoffer Gronlund <kgronlund@suse.com>
- Update to v1.2.2:
  * Allow multiple clusters to set useAllDevices (#4692)
  * Operator start all mons before checking quorum if they are all down (#4531)
  * Ability to disable the crash controller (#4533)
  * Document monitoring options for the cluster CR (#4698)
  * Apply node topology labels to PV-backed OSDs in upgrade from v1.1 (#4616)
  * Update examples to Ceph version v14.2.6 (#4653)
  * Allow integration tests in minimal config to run on multiple K8s versions (#4674)
  * Wrong pod name and hostname shown in alert CephMonHighNumberOfLeaderChanges (#4665)
  * Set hostname properly in the CRUSH map for non-portable OSDs on PVCs (#4658)
  * Update OpenShift example manifest to watch all namespaces for clusters (#4668)
  * Use min_size defaults set by Ceph instead of overriding with Rook's defaults (#4638)
  * CSI driver handling of upgrade from OCP 4.2 to OCP 4.3 (#4650-1)
  * Add support for the k8s 1.17 failure domain labels (#4626)
  * Add option to the cluster CR to continue upgrade even with unclean PGs (#4617)
  * Add K8s 1.11 back to the integration tests as the minimum version (#4673)
  * Fixed replication factor flag and the master addresses (#4625)

* Wed Jan  8 2020 Kristoffer Gronlund <kgronlund@suse.com>
- Update to v1.2.1:
  * Add missing env var  `ROOK_CEPH_MON_HOST` for OSDs (#4589)
  * Avoid logging sensitive info when debug logging is enabled (#4568)
  * Add missing vol mount for encrypted osds (#4583)
  * Bumping ceph-operator memory limit to 256Mi (#4561)
  * Fix object bucket provisioner when rgw not on port 80 (#4508)

* Fri Dec 20 2019 Kristoffer Gronlund <kgronlund@suse.com>
- Update to v1.2.0:
  * Security audit completed by Trail of Bits found no major concerns
  * Ceph: Added a new "crash collector" daemon to send crash telemetry
    to the Ceph dashboard, support for priority classes, and a new
    CephClient resource to create user credentials
  * The minimum version of Kubernetes supported by Rook changed from
    1.11 to 1.12.
  * Device filtering is now configurable for the user by adding an
    environment variable
    + A new environment variable DISCOVER_DAEMON_UDEV_BLACKLIST is
    added through which the user can blacklist the devices
    + If no device is specified, the default values will be used to
    blacklist the devices
  * The topology setting has been removed from the CephCluster CR. To
    configure the OSD topology, node labels must be applied.
  * See the OSD topology topic. This setting only affects OSDs when
    they are first created, thus OSDs will not be impacted during
    upgrade.
  * The topology settings only apply to bluestore OSDs on raw devices.
    The topology labels are not applied to directory-based OSDs.
  * Creation of new Filestore OSDs on disks is now deprecated.
    Filestore is in sustaining mode in Ceph.
    + The storeType storage config setting is now ignored
    + New OSDs created in directories are always Filestore type
    + New OSDs created on disks are always Bluestore type
    + Preexisting disks provisioned as Filestore OSDs will remain as
    Filestore OSDs
  * Rook will no longer automatically remove OSDs if nodes are removed
    from the cluster CR to avoid the risk of destroying OSDs
    unintentionally. To remove OSDs manually, see the new doc on OSD
    Management
- Update csi-dummy-images.patch
- Update flexvolume-dir.patch
- Drop outdated patch 0001-bsc-1152690-ceph-csi-Driver-will-fail-with-error.patch

* Tue Dec  3 2019 Kristoffer Gronlund <kgronlund@suse.com>
- Update rook to v1.1.7:
  * Skip osd prepare job creation if osd daemon exists for the pvc (#4277)
  * Stop osd process more quickly during pod shutdown to reduce IO unresponsiveness (#4328)
  * Add osd anti-affinity to the example of OSDs on PVCs (#4326)
  * Properly set app name on the cmdreporter (#4323)
  * Ensure disruption draining state is set and checked correctly (#4319)
  * Update LVM filter for OSDs on PVCs (#4312)
  * Fix topology logic for disruption drains (#4221)
  * Skip restorecon during ceph-volume configuration (#4260)
  * Added a note around snapshot CRD cleanup (#4302)
  * Storage utilization alert threshold and timing updated (#4286)
  * Silence disruption errors if necessary and add missing errors (#4288)
  * Create csi keys and secrets for external cluster (#4276)
  * Add retry to ObjectUser creation (#4149)

* Wed Nov  6 2019 Kristoffer Gronlund <kgronlund@suse.com>
- Update rook to v1.1.6:
  * Flex driver should not allow attach before detach on a different node (#3582)
  * Properly set the ceph-mgr annotations (#4195)
  * Only trigger an orchestration if the cluster CR changed (#4252)
  * Fix setting rbdGrpcMetricsPort in the helm chart (#4202)
  * Document all helm chart settings (#4202)
  * Support all layers of CRUSH map with node labels (#4236)
  * Skip orchestration restart on device config map update for osd on pvc (#4124)
  * Deduplicate tolerations collected for the drain canary pods (#4220)
  * Role bindings are missing for pod security policies (#3851)
  * Continue with orchestration if a single mon pod fails to start (#4146)
  * OSDs cannot call 'restorecon' when selinux is enabled (#4214)
  * Use the rook image for drain canary pods (#4213)
  * Allow setting of osd prepare resource limits (#4182)
  * Documentation for object bucket provisioning (#3882)

* Tue Nov  5 2019 Kristoffer Gronlund <kgronlund@suse.com>
- Update rook to v1.1.4:
  * OSD config overrides were ignored for some upgraded OSDs (#4161)
  * Enable restoring a cluster after disaster recovery (#4021)
  * Enable upgrade of OSDs configured on PVCs (#3996)
  * Automatically removing OSDs requires setting: removeOSDsIfOutAndSafeToRemove(#4116)
  * Rework csi keys and secrets to use minimal privileges (#4086)
  * Expose OSD prepare pod resource limits (#4083)
  * Minimum K8s version for running OSDs on PVCs is 1.13 (#4009)
  * Add 'rgw.buckets.non-ec' to list of RGW metadataPools (#4087)
  * Hide wrong error for clusterdisruption controller (#4094)
  * Multiple integration test fixes to improve CI stability (#4098)
  * Detect mount fstype more accurately in the flex driver (#4109)
  * Do not override mgr annotations (#4110)
  * Add OSDs to proper buckets in crush hierarchy with topology awareness (#4099)
  * More robust removal of cluster finalizer (#4090)
  * Take activeStandby into account for the CephFileSystem disruption budget (#4075)
  * Update the CSI CephFS registration directory name (#4070)
  * Fix incorrect Ceph CSI doc links (#4081)
  * Remove decimal places for osdMemoryTargetValue monitoring setting (#4046)
  * Relax pre-requisites for external cluster to allow connections to Luminous (#4025)
  * Avoid nodes getting stuck in OrchestrationStatusStarting during OSD config (#3817)
  * Make metrics and liveness port configurable (#4005)
  * Correct system namespace for CSI driver settings during upgrade (#4040)
- Update csi-dummy-images.patch
- Update csi-template-paths.patch
- Update 0001-bsc-1152690-ceph-csi-Driver-will-fail-with-error.patch

* Wed Oct  2 2019 Kristoffer Gronlund <kgronlund@suse.com>
- Force use of ceph kernel client driver (bsc#1152690)
- Add 0001-bsc-1152690-ceph-csi-Driver-will-fail-with-error.patch

* Tue Oct  1 2019 Blaine Gardner <blaine.gardner@suse.com>
- Define build shell as /bin/bash for usage of `=~` conditional (bsc#1152559)

* Mon Sep 30 2019 Blaine Gardner <blaine.gardner@suse.com>
- Fix csi-dummy-images.patch to work with Go linker's -X flag (bsc#1152559)
  + update linker flags themselves to remove comments from flags
  + add test to spec file to verify linker flags are working in future

* Thu Sep 26 2019 Blaine Gardner <blaine.gardner@suse.com>
- Fix 2 improper RPM spec variable references in specfile (bsc#1151909)

* Wed Sep 25 2019 Blaine Gardner <blaine.gardner@suse.com>
- Use lightweight git tags when determining Rook version from source in tarball script (bsc#1151909)
  + Build should now be tagged appropriately as version 1.1.1.0 instead of 1.1.0.x
- Override some Rook defaults with linker flags at build time:
  + CSI image -> SUSE image
  + FlexVolume dir (for Kubic)
- Add patches for:
  + updating CSI image to a dummy value later changed at linker time
  + updating CSI template paths to the ones installed by rook-k8s-manifests
  + update the FlexVolume dir path to be compatible with Kubic
- Remove previously applied SUSE-specific changes that are now taken care of by the above patches
- Add patch: csi-dummy-images.patch
- Add patch: csi-template-paths.patch
- Add patch: flexvolume-dir.patch

* Wed Sep 25 2019 Kristoffer Gronlund <kgronlund@suse.com>
- rook-k8s-yaml: Fix YAML indentation of cephcsi image value (bsc#1152008)

* Wed Sep 25 2019 Blaine Gardner <blaine.gardner@suse.com>
- Update Rook to match upstream version v1.1.1 (bsc#1151909)
  + Disable the flex driver by default in new clusters
  + MDB controller to use namespace for checking ceph status
  + CSI liveness container socket file
  + Add list of unusable directories paths
  + Remove helm incompatible chars from values.yaml
  + Fail NFS-ganesha if CephFS is not configured
  + Make lifecycle hook chown less verbose for OSDs
  + Configure LVM settings for rhel8 base image
  + Make kubelet path configurable in operator for csi (#392
  + OSD pods should always use hostname for node selector
  + Deactivate device from lvm when OSD pods are shutting down
  + Add CephNFS to OLM's CSV
  + Tolerations for drain detection canaries
  + Enable ceph-volume debug logs
  + Add documentation for CSI upgrades from v1.0 (#386
  + Add a new skipUpgradeChecks property to allow forcing upgrades
  + Include CSI image in helm chart values (#385
  + Use HTTP port if SSL is disabled
  + Enable SSL for dashboard by default
  + Enable msgr2 properly during upgrades
  + Nautilus v14.2.4 is the default Ceph image
  + Ensure the ceph-csi secret exists on upgrade
  + Disable the min PG warning if the pg_autoscaler is enabled
  + Disable the warning for bluestore warn on legacy statfs
- add SUSE-specific changes to manifests:
  + uncomment ROOK_CSI_CEPH_IMAGE var
  + set FlexVolume dir path for Kubic
  + add ROOK_CSI_*_TEMPLATE_PATH configs

* Mon Sep 16 2019 Kristoffer Gronlund <kgronlund@suse.com>
- rook-k8s-yaml: Revert to buildrequire for ceph (bsc#1151479)

* Fri Sep 13 2019 Blaine Gardner <blaine.gardner@suse.com>
- Update tar creation script
  + build rook tag 'v1.1.0' from 'suse-release-1.1' branch
- Update Rook to tag 'v1.1.0' (bsc#1151479)
  + fix HighMonLeaderChanges alert
  + add leases rules to CSI rules
  + only schedule node drain canaries on nodes with OSDs
  + increase sidecar timeout from 60s to 150s
  + use combined (stdout+stderr) output from ceph-volume
  + set command property for the OSD prepare init container blkdevmapper
  + change OSD DOWN message to debug level
  + discovery daemon: ignore updates on nbd devices

* Mon Sep  9 2019 Blaine Gardner <blaine.gardner@suse.com>
- Support upstream beta tags by replacing hyphens in release tag with tildes
  + RPMs sorts tildes before anything else to support vX.Y.0~beta.B coming before vX.Y.0

* Mon Sep  9 2019 Blaine Gardner <blaine.gardner@suse.com>
- Update tar creation script
  + fail on more types of script errors
  + exit properly on error
  + allow checking out tags
  + allow parsing tag versions with hyphens (e.g., v1.1.0-beta.1)
  + use revision (tag) 'v1.1.0-beta.1' from ('suse-release-1.1' branch)
- Update Rook to tag 'v1.1.0-beta.1'
  + support external Ceph clusters
  + fix osdsPerDevice config
  + add portable failure-domain label to OSD deployments
  + add bucket provisioner
  + use deployment with leader election instead of stateful set for CSI drivers
  + fix alerting & recording rules
  + fix race in create ObjectUser
  + support mon migrations without rebuilds when using PVCs
  + allow CRUSH map to be based on PVCs for PVC-based OSDs
  + fix md and dev ordering for ceph-volume batch operations
  + improve upgrades when a mon is down
  + fix service account name for CSI RBD provisioner
  + add -pidlimit flag for CephFS and RBD plugins for CSI driver
  + add image pull secrets option to manifests
  + remove OSD pods marked out if pod is more than an hour old
  + add --db-devices flag to ceph-volume provisioning & fix MB size bug
  + implement GRPC metrics for cephcsi
  + clean up verbose Ceph logging
  + update upgrade documentation for v1.1 release
  + remove unused attacher service account
  + add dynamic expansion to FlexVolume driver
  + fix random OSD pod failures when using PVCs
  + fix osd prepare panic
  + lower minimum OSD memory to 2GB
  + add ability to enable mgr modules via CRD (notably the pg_autoscaler module)
  + fix topologyAware on PVC-based OSDs
  + add support for OpenShift machine disruption budgets

* Fri Aug 23 2019 Kristoffer Gronlund <kgronlund@suse.com>
- Make rook-k8s-yaml require the matching ceph version
- Update rook to commit 692553221d8b18fec8aa3ccdc5872e51f05ca372:
  +  uncomment ROOK_CSI_CEPH_IMAGE var

* Fri Aug 16 2019 Jan Engelhardt <jengelh@inai.de>
- Trim redundant wording from description.

* Tue Aug 13 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Tech preview release for containers (bsc#1145433)

* Mon Aug 12 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Update Rook to commit e9abbf4831673a9a5545971532ae326e95f3ea60
  + enable the ceph-csi driver by default
  + remove csi default settings from yaml
  + add option to disable flex driver
  + allow the discovery daemon to be optional
  + automatically create the csi secret with the cluster
  + Allow to launch pods when memory request is set (but no memory limit)
  + ceph: chown with init container
  + ceph: when mons use pvc mount volume at subpath
- csi was merged to operator.yaml, sed to correct file

* Fri Aug  2 2019 Blaine Gardner <blaine.gardner@suse.com>
- Fix build broken with creation of new rook-integration helper files
- Put helper files into /usr/share/rook-integration dir
- Change name of 'integration' binary to 'rook-integration'

* Thu Aug  1 2019 Blaine Gardner <blaine.gardner@suse.com>
- Generate files which contain the names of all images used in the manifests produced by this build
  which are installed with the rook-integration package to assist the integration tooling.

* Thu Aug  1 2019 Blaine Gardner <blaine.gardner@suse.com>
- Update spec file to build rook-integration binary
  - Building test binaries is different from building main binaries, so manual steps needed
- Apply linker flags to rookflex binary also (just in case)
- Slightly rework rook-k8s-yaml summary description

* Fri Jul 26 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Correct toolbox location in manifest files

* Tue Jul 23 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Update Rook to commit 7a48482f5cd92397eef068d097ad233739ceae06
  + ceph: run ceph processes with the 'ceph' user
  + Correct typo about skipVolumeForDirectory's code comment
  + Fix: topologyAware does not pick up failure domains.
  + Correct typo about skipVolumeForDirectory's code comment

* Mon Jul 22 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Update Rook to commit 0141cfea50a7f80ff1ee67aa8cc7ad28edc79a64
  + OSD startup on SDN for error "Cannot assign requested address"
  + Change default frontend on nautilus to beast
  + RGW daemon updates:
    ~ Remove support for AllNodes where we would deploy one rgw per node on all the nodes
    ~ Each rgw deployed has its own cephx key
    ~ Upgrades will automatically transition these changes to the rgw daemons
  + Correct --ms-learn-addr-from-peer=false argument for ceph-osd
  + When updating the CephCluster CR to run unsupported octopus, fix operator panic
  + Add metrics for the flexvolume driver
  + Set the fully qualified apiVersion on the OwnerReferences for cleanup on OpenShift
  + Stop enforcing crush tunables for octopus warning
  + Apply the osd nautilus flag for upgrade
  + RGW: Set proper port syntax for beast in nautilus deployments
  + Stop creating initial crushmap to avoid incorrect crush map warning
  + Use correct rounding of PV size for binding of PVCs (for example G or Gi)
- Add psp to common.yaml

* Wed Jul 17 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Use ceph-base pattern instead of packages

* Fri Jul 12 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Fix sed expression to replace correct link

* Fri Jul 12 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Add ceph-csi as a dependency and update manifest link with it

* Thu Jul 11 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- correct version for Rook build that doesn's support "+"

* Tue Jul  9 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- noarch for the rook-k8s-yaml package
- update rook to a265cdf commit
  + added ROOK_CSI_* template pathes
- modify update script for none Go enviroment

* Mon Jul  8 2019 Blaine Gardner <blaine.gardner@suse.com>
- Fix subtly broken dependency (vendor dir) generation
- Generate two tarballs for builds to follow latest upstream best practices for Golang RPM builds
  + primary source tarball is unmodified from source code, and vendor dir is a separate tarball
- Add Rook toolbox script to main rook package
- Update manifests to use SUSE image for toolbox
- Update spec file dependencies
  + remove old Rook dependencies
  + add missing dependencies from the upstream Ceph image (notably nfs-ganesha and CSI requirements)
- Update build to include go build linker flag to set rook binary's internal version representation
- Remove FlexVolume config from manifests, as we intend to use CSI henceforth
- Update Rook to commit c4a3763b6415a118aedaee52eaf76cbdf6b0dabb
  + delay starting Rook system daemons until a CephCluster is created
  + stop setting CRUSH tunable automatically
  + use --ms-learn-addr-from-peer flag for OSDs for Ceph v14.2.2 and up - https://github.com/rook/rook/issues/3140
  + when appropriate, look for rook and tini binaries in PATH if not found in default location
  + set fully qualified apiVersion on OwnerReferences
  + OSDs marked out by Ceph will have their Kubernetes resources automatically cleaned up (will not be removed from CRUSH map)
  + add NodeAffinity to system daemons

* Wed Jul  3 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- restore package name and correct unique containers tags

* Tue Jun 18 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- changing package name as it couldn't comply to the container tag name
  + https://github.com/containers/image/issues/649

* Tue Jun 18 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Ceph added as a requirement to get it version for the container image
- Added service to strip Ceph version from ceph package
- Fixed sed for the container images names

* Tue Jun 18 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Update Rook to commit ad89e4f47e744c484b8e264e351f6276a42eedfc
  + change csi template path to match rook-k8s-yaml package files
- Fix update-tarball.sh to delete right files
- Add all manifests to the rook-k8s-yaml packages
- Fix rook binary location from /usr/local/bin/ to /usr/bin/

* Tue Jun 18 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Fix update-tarball.sh to ignore errors where is needed
- Update spec to include additional ceph-csi config files

* Mon Jun 17 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Adding additional files as Source to spec

* Mon Jun 17 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Update tarball generation script to get correct version
- Correct tarball name, spec version and package name
- Add new k8s-yaml package to distribute manifests files

* Tue May 21 2019 Denis Kondratenko <denis.kondratenko@suse.com>
- Update rook to commit 700cdd36fe9107733a717fac934c2bedd91fd290
- build from https://github.com/SUSE/rook/tree/suse-master
- based on Rook v1.0.0
- Ceph:
  + Ceph Nautilus (v14) is now supported by Rook
  + The Ceph-CSI driver is available for experimental mode
  + A CephNFS CRD will start NFS daemon(s) for exporting CephFS volumes or RGW buckets
  + The number of mons can be increased automatically when new nodes come online
  + OSDs provisioned by ceph-volume now supports metadataDevice and databaseSizeMB options

* Mon Apr 29 2019 Jan Fajerski <jan.fajerski@suse.com>
- Update rook to commit c43b57844e37a7909beb362d08ef85fffdd5fed4
- build from https://github.com/SUSE/rook/tree/suse-master
- Ceph:
  + Improve rbd hotplug selection
  + set default version to nautilus
  + improved OSD removal
  + clean shutdown of CephFS
  + improve logging
  + improved upgrade ochestration

* Mon Apr  8 2019 Jan Fajerski <jan.fajerski@suse.com>
- Update rook to commit 69936c170cb3913a539eacf963993e9bb3545e8a
- Cassandra: Fix the mount point for th
- Ceph:
  + Improve mon failover cleanup and operator restart during failover
  + Enable host ipc for osd encryption
  + Add missing "host path requires privileged" setting to the helm chart

* Tue Jan 29 2019 Jan Fajerski <jan.fajerski@suse.com>
- Update rook to commit 8e263cd9c31b0a310b0d1180e58ac843b432b14b
- Correctly capture and log the stderr output from child processes
- Allow disabling setting fsgroup when mounting a volume
- Allow configuration of SELinux relabeling
- Correctly set the secretKey used for cephfs mounts
- Set ceph-mgr privileges to prevent the dashboard from failing on rbd mirroring settings
- Correctly configure the ssl certificate for the RGW service
- Allow configuration of the dashboard port
- Allow disabling of ssl on the dashboard

* Thu Jan 17 2019 Jan Fajerski <jan.fajerski@suse.com>
- Update rook to commit d0cd8cec72176bf28a3ac0ba1457297151004f79
- Ceph CRDs have been declared stable V1.
- Ceph versioning is decoupled from the Rook version. Luminous and Mimic can be run in production, or Nautilus in experimental mode.
- Ceph upgrades are greatly simplified
- The minimum version of Kubernetes supported by Rook changed from 1.7 to 1.8

* Mon Jan 14 2019 Jan Fajerski <jan.fajerski@suse.com>
- install to /usr/local/bin as rook hardcodes this path for rookflex

* Tue Oct 30 2018 Jan Fajerski <jan.fajerski@suse.com>
- Update rook to commit bf2759e317c44c0ad0aaf635e04cbd72a002a5a0
- Refactor ceph containers to disconnect rook and ceph versions

* Thu Apr 26 2018 blaine.gardner@suse.com
- Update Rook build to use '-buildmode=pie' flag
- Version at commit e11b3d863728667ea018aa329f3ad907360473cf

* Tue Apr 24 2018 blaine.gardner@suse.com
- Initial submission
- Version at commit 71514921ad8e41ede6f2814e7004f0465e3dd0f7
- Modifications to upstream Rook to support SLE:
  - None
